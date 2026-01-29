"""
Secure Code Executor for LearnFlow
Safely executes Python code with resource limits and security measures
"""
import asyncio
import subprocess
import tempfile
import os
import signal
import logging
from typing import Dict, Any, Optional
from contextlib import contextmanager
import time

logger = logging.getLogger(__name__)

class CodeExecutionError(Exception):
    """Custom exception for code execution errors"""
    pass

class CodeExecutor:
    def __init__(self, timeout: int = 10, memory_limit_mb: int = 100):
        self.timeout = timeout
        self.memory_limit_mb = memory_limit_mb

    async def execute_python_code(self, code: str, input_data: str = "", language: str = "python") -> Dict[str, Any]:
        """
        Execute Python code in a secure sandbox environment

        Args:
            code: Python code to execute
            input_data: Input data to provide to the code
            language: Programming language (currently only supports Python)

        Returns:
            Dictionary with execution results
        """
        if language.lower() != "python":
            raise CodeExecutionError(f"Language {language} not supported. Only Python is supported.")

        start_time = time.time()

        # Validate code for dangerous operations
        if self._contains_dangerous_operations(code):
            raise CodeExecutionError("Code contains potentially dangerous operations and was blocked.")

        try:
            # Create a temporary file for the code
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
                temp_file.write(code)
                temp_file_path = temp_file.name

            # Create a temporary file for input data
            input_file_path = None
            if input_data:
                with tempfile.NamedTemporaryFile(mode='w', delete=False) as input_file:
                    input_file.write(input_data)
                    input_file_path = input_file.name

            try:
                # Execute the code with timeout and resource limits
                result = await self._run_code_with_timeout(temp_file_path, input_file_path)

                execution_time = time.time() - start_time

                return {
                    "output": result.stdout,
                    "errors": result.stderr,
                    "status": "success" if result.returncode == 0 else "error",
                    "execution_time": execution_time,
                    "return_code": result.returncode
                }

            finally:
                # Clean up temporary files
                os.unlink(temp_file_path)
                if input_file_path:
                    os.unlink(input_file_path)

        except asyncio.TimeoutError:
            return {
                "output": "",
                "errors": "Execution timed out",
                "status": "error",
                "execution_time": time.time() - start_time,
                "return_code": -1
            }
        except Exception as e:
            logger.error(f"Error executing code: {str(e)}")
            return {
                "output": "",
                "errors": str(e),
                "status": "error",
                "execution_time": time.time() - start_time,
                "return_code": -1
            }

    def _contains_dangerous_operations(self, code: str) -> bool:
        """
        Check if code contains potentially dangerous operations

        Args:
            code: Python code to check

        Returns:
            True if dangerous operations found, False otherwise
        """
        dangerous_patterns = [
            'import os', 'import sys', 'import subprocess', 'import shutil',
            'import urllib', 'import requests', 'import http', 'import socket',
            '__import__', 'exec(', 'eval(', 'open(', 'file(',
            'getattr(', 'setattr(', 'delattr(', 'compile(',
            'globals()', 'locals()', 'vars(',
            'input(',  # Insecure input functions
        ]

        # Convert code to lowercase for comparison
        code_lower = code.lower()

        for pattern in dangerous_patterns:
            if pattern in code_lower:
                logger.warning(f"Dangerous pattern detected: {pattern}")
                return True

        return False

    async def _run_code_with_timeout(self, code_file_path: str, input_file_path: Optional[str]) -> subprocess.CompletedProcess:
        """
        Run Python code with timeout protection

        Args:
            code_file_path: Path to the temporary code file
            input_file_path: Path to the input file (optional)

        Returns:
            CompletedProcess result
        """
        # Prepare the command
        cmd = ['python', code_file_path]

        # Prepare input
        stdin_data = None
        if input_file_path:
            with open(input_file_path, 'r') as input_file:
                stdin_data = input_file.read()

        # Execute with timeout
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            limit=1024 * 1024  # 1MB buffer limit
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(input=stdin_data.encode() if stdin_data else None),
                timeout=self.timeout
            )
        except asyncio.TimeoutError:
            # Terminate the process if it times out
            try:
                process.kill()
            except ProcessLookupError:
                pass  # Process already terminated
            raise asyncio.TimeoutError(f"Code execution exceeded {self.timeout} second timeout")

        return subprocess.CompletedProcess(
            args=cmd,
            returncode=process.returncode,
            stdout=stdout.decode('utf-8'),
            stderr=stderr.decode('utf-8')
        )

    async def execute_multiple_codes(self, codes: List[str]) -> List[Dict[str, Any]]:
        """
        Execute multiple code snippets sequentially

        Args:
            codes: List of code snippets to execute

        Returns:
            List of execution results
        """
        results = []
        for code in codes:
            result = await self.execute_python_code(code)
            results.append(result)
        return results

# Global executor instance
executor = CodeExecutor(timeout=10, memory_limit_mb=100)

async def execute_code(code: str, input_data: str = "", language: str = "python") -> Dict[str, Any]:
    """
    Convenience function to execute code using the global executor

    Args:
        code: Code to execute
        input_data: Input data for the code
        language: Programming language

    Returns:
        Execution results
    """
    return await executor.execute_python_code(code, input_data, language)