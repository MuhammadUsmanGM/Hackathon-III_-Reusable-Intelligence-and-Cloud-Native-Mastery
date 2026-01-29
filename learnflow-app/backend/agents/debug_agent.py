"""
Debug Agent for LearnFlow
Helps students debug their Python code
"""

import ast
import traceback
import re
from typing import Dict, Any, List
import asyncio
import sys
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr

class DebugAgent:
    def __init__(self):
        self.name = "Debug Agent"
        self.description = "Helps students debug their Python code"

    async def process(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process user's debugging request"""
        # Extract code and error from user input
        code_snippet = await self._extract_code(user_input)
        error_message = await self._extract_error(user_input)

        if code_snippet:
            debug_result = await self._debug_code(code_snippet, error_message)

            response = {
                "agent": "debug",
                "original_code": code_snippet,
                "debug_analysis": debug_result,
                "suggested_fixes": debug_result.get("suggested_fixes", []),
                "error_type": debug_result.get("error_type", "unknown"),
                "confidence": 0.9,
                "message": f"Debug analysis complete. Identified {debug_result.get('error_type', 'unknown')} error."
            }
        else:
            response = {
                "agent": "debug",
                "message": "Please provide the code that's causing issues. Include your error message if available.",
                "confidence": 0.8
            }

        return response

    async def _extract_code(self, user_input: str) -> str:
        """Extract Python code from user input"""
        # Look for code in triple backticks
        code_pattern = r'```(?:python)?\n?(.*?)```'
        matches = re.findall(code_pattern, user_input, re.DOTALL)

        if matches:
            return matches[0].strip()

        # If no backticks, check if the entire input looks like code
        lines = user_input.strip().split('\n')
        if len(lines) > 1:
            # Simple heuristic: if multiple lines with Python-like syntax
            python_indicators = ['def ', 'import ', 'class ', '=', 'if ', 'for ', 'while ', 'print(']
            indicators_found = sum(1 for indicator in python_indicators if any(indicator in line for line in lines))

            if indicators_found > 0:
                return user_input

        return ""

    async def _extract_error(self, user_input: str) -> str:
        """Extract error message from user input"""
        # Look for common error patterns
        error_patterns = [
            r'Traceback \(most recent call last\):\n.*?(?=^\w|\Z)',
            r'(?:Error|Exception):\s*(.*?)(?:\n|$)',
            r'(\w+Error):\s*(.*?)(?:\n|$)'
        ]

        for pattern in error_patterns:
            match = re.search(pattern, user_input, re.MULTILINE | re.DOTALL)
            if match:
                return match.group(0).strip()

        return ""

    async def _debug_code(self, code: str, error_msg: str = "") -> Dict[str, Any]:
        """Analyze and debug the provided code"""
        issues = []
        suggested_fixes = []

        # First, check for syntax errors
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            issues.append({
                "type": "syntax_error",
                "severity": "critical",
                "line": e.lineno or 0,
                "column": e.offset or 0,
                "message": f"SyntaxError: {str(e.msg)}",
                "code_line": code.split('\n')[e.lineno - 1] if e.lineno and e.lineno <= len(code.split('\n')) else ""
            })
            suggested_fixes.extend(self._suggest_syntax_fixes(str(e.msg), code, e.lineno))
            return {
                "issues": issues,
                "suggested_fixes": suggested_fixes,
                "error_type": "syntax_error"
            }

        # If no syntax errors, try to run the code safely
        if not issues:
            execution_result = await self._safe_execute_code(code)
            if execution_result["has_error"]:
                issues.append({
                    "type": "runtime_error",
                    "severity": "critical",
                    "error_type": execution_result["error_type"],
                    "message": execution_result["error_message"],
                    "traceback": execution_result["traceback"]
                })
                suggested_fixes.extend(self._analyze_runtime_error(execution_result["error_type"], execution_result["error_message"], code))

        # Perform static analysis for common bugs
        static_issues = self._static_analysis(tree, code)
        issues.extend(static_issues)

        error_type = "none"
        if any(issue["type"] == "syntax_error" for issue in issues):
            error_type = "syntax_error"
        elif any(issue["type"] == "runtime_error" for issue in issues):
            error_type = "runtime_error"
        elif issues:
            error_type = "logical_error"

        return {
            "issues": issues,
            "suggested_fixes": suggested_fixes,
            "error_type": error_type
        }

    def _suggest_syntax_fixes(self, error_msg: str, code: str, line_no: int = None) -> List[str]:
        """Suggest fixes for syntax errors"""
        fixes = []

        if "invalid syntax" in error_msg.lower():
            fixes.append("Check for missing colons, parentheses, brackets, or quotes.")

        if "unexpected EOF" in error_msg.lower():
            fixes.append("Make sure all code blocks are properly closed with correct indentation.")

        if "EOL while scanning string literal" in error_msg.lower():
            fixes.append("Check for unclosed quotes in strings.")

        if line_no and line_no <= len(code.split('\n')):
            line = code.split('\n')[line_no - 1]
            if line.count('(') != line.count(')'):
                fixes.append("Check for mismatched parentheses.")
            if line.count('[') != line.count(']'):
                fixes.append("Check for mismatched square brackets.")
            if line.count('{') != line.count('}'):
                fixes.append("Check for mismatched curly braces.")

        return fixes

    def _static_analysis(self, tree: ast.AST, code: str) -> List[Dict[str, Any]]:
        """Perform static analysis to find potential bugs"""
        issues = []
        lines = code.split('\n')

        for node in ast.walk(tree):
            # Check for undefined variables
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                # This is a simplification - in a real system, we'd need proper scoping analysis
                pass

            # Check for potential division by zero
            if (isinstance(node, ast.BinOp) and
                isinstance(node.op, ast.Div) and
                isinstance(node.right, ast.Constant) and
                node.right.value == 0):
                issues.append({
                    "type": "potential_bug",
                    "severity": "high",
                    "line": node.lineno,
                    "message": "Potential division by zero detected",
                    "code_line": lines[node.lineno - 1] if node.lineno <= len(lines) else ""
                })

            # Check for modifying loop variable inside for loop
            if isinstance(node, ast.For):
                for inner_node in ast.walk(node):
                    if (isinstance(inner_node, ast.Name) and
                        isinstance(inner_node.ctx, ast.Store) and
                        isinstance(inner_node.id, str) and
                        inner_node.id == node.target.id):
                        issues.append({
                            "type": "potential_bug",
                            "severity": "medium",
                            "line": inner_node.lineno,
                            "message": f"Modifying loop variable '{inner_node.id}' inside for loop may cause unexpected behavior",
                            "code_line": lines[inner_node.lineno - 1] if inner_node.lineno <= len(lines) else ""
                        })

        return issues

    async def _safe_execute_code(self, code: str) -> Dict[str, Any]:
        """Safely execute code and capture any runtime errors"""
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        stdout_capture = StringIO()
        stderr_capture = StringIO()

        try:
            # Redirect stdout and stderr to capture output
            sys.stdout = stdout_capture
            sys.stderr = stderr_capture

            # Execute the code
            local_vars = {}
            exec(code, {}, local_vars)

            # Restore stdout and stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr

            return {
                "has_error": False,
                "output": stdout_capture.getvalue(),
                "errors": stderr_capture.getvalue(),
                "local_vars": local_vars
            }
        except Exception as e:
            # Restore stdout and stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr

            # Capture the traceback
            tb_str = traceback.format_exc()

            return {
                "has_error": True,
                "error_type": type(e).__name__,
                "error_message": str(e),
                "traceback": tb_str
            }

    def _analyze_runtime_error(self, error_type: str, error_msg: str, code: str) -> List[str]:
        """Analyze runtime errors and suggest fixes"""
        fixes = []

        if error_type == "NameError":
            fixes.append(f"Check if '{error_msg.split('\"')[1] if '\"' in error_msg else 'the variable'}' is defined before use.")

        elif error_type == "TypeError":
            fixes.append("Check if you're using the correct data types for operations.")
            fixes.append("Ensure you're not trying to perform invalid operations on incompatible types.")

        elif error_type == "IndexError":
            fixes.append("Check if your list/string indices are within valid range.")
            fixes.append("Verify the length of your data structures before accessing by index.")

        elif error_type == "KeyError":
            fixes.append("Check if the dictionary key exists before accessing it.")
            fixes.append("Use .get() method or 'in' operator to check for key existence.")

        elif error_type == "AttributeError":
            fixes.append(f"Check if the object has the attribute '{error_msg.split('\"')[1] if '\"' in error_msg else 'mentioned'}'.")
            fixes.append("Verify you're calling the correct method or accessing the correct property.")

        elif error_type == "ValueError":
            fixes.append("Check if the values you're using are of the expected type/format.")

        elif error_type == "ZeroDivisionError":
            fixes.append("Add a check to ensure the divisor is not zero before division.")

        return fixes