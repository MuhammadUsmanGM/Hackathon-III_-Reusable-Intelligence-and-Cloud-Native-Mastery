"""
Code Review Agent for LearnFlow
Reviews Python code and suggests improvements
"""

import ast
import re
from typing import Dict, Any, List
import asyncio

class CodeReviewAgent:
    def __init__(self):
        self.name = "Code Review Agent"
        self.description = "Reviews Python code and suggests improvements"

    async def process(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process user's code for review"""
        # Extract code from user input if present
        code_snippet = await self._extract_code(user_input)

        if code_snippet:
            review_results = await self._review_code(code_snippet)

            response = {
                "agent": "code_review",
                "original_code": code_snippet,
                "review": review_results,
                "suggestions": review_results.get("suggestions", []),
                "issues_found": len(review_results.get("issues", [])),
                "confidence": 0.9,
                "message": f"Code review complete. Found {len(review_results.get('issues', []))} issues and provided {len(review_results.get('suggestions', []))} suggestions."
            }
        else:
            response = {
                "agent": "code_review",
                "message": "Please provide Python code for me to review. Include your code in triple backticks (```python ... ```).",
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

    async def _review_code(self, code: str) -> Dict[str, Any]:
        """Perform code review on the provided code"""
        issues = []
        suggestions = []

        try:
            # Parse the code to check for syntax errors
            tree = ast.parse(code)
        except SyntaxError as e:
            issues.append({
                "type": "syntax_error",
                "severity": "high",
                "line": getattr(e, 'lineno', 0),
                "message": f"Syntax error: {str(e)}"
            })
            return {"issues": issues, "suggestions": suggestions}

        # Perform various checks
        issues.extend(self._check_naming_conventions(tree, code))
        issues.extend(self._check_for_common_issues(tree, code))
        suggestions.extend(self._suggest_improvements(tree, code))

        return {"issues": issues, "suggestions": suggestions}

    def _check_naming_conventions(self, tree: ast.AST, code: str) -> List[Dict[str, Any]]:
        """Check for Python naming convention issues"""
        issues = []
        lines = code.split('\n')

        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                # Variable assignment
                if not self._is_valid_variable_name(node.id):
                    issues.append({
                        "type": "naming_convention",
                        "severity": "medium",
                        "line": node.lineno,
                        "message": f"Variable '{node.id}' doesn't follow Python naming conventions. Use snake_case for variables."
                    })
            elif isinstance(node, ast.FunctionDef):
                # Function definition
                if not self._is_valid_function_name(node.name):
                    issues.append({
                        "type": "naming_convention",
                        "severity": "medium",
                        "line": node.lineno,
                        "message": f"Function '{node.name}' doesn't follow Python naming conventions. Use snake_case for functions."
                    })
            elif isinstance(node, ast.ClassDef):
                # Class definition
                if not self._is_valid_class_name(node.name):
                    issues.append({
                        "type": "naming_convention",
                        "severity": "medium",
                        "line": node.lineno,
                        "message": f"Class '{node.name}' doesn't follow Python naming conventions. Use PascalCase for classes."
                    })

        return issues

    def _is_valid_variable_name(self, name: str) -> bool:
        """Check if variable name follows snake_case convention"""
        import re
        return bool(re.match(r'^[a-z][a-z0-9_]*$', name))

    def _is_valid_function_name(self, name: str) -> bool:
        """Check if function name follows snake_case convention"""
        return self._is_valid_variable_name(name)

    def _is_valid_class_name(self, name: str) -> bool:
        """Check if class name follows PascalCase convention"""
        import re
        return bool(re.match(r'^[A-Z][a-zA-Z0-9]*$', name))

    def _check_for_common_issues(self, tree: ast.AST, code: str) -> List[Dict[str, Any]]:
        """Check for common Python issues"""
        issues = []
        lines = code.split('\n')

        for node in ast.walk(tree):
            # Check for bare except clauses
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                issues.append({
                    "type": "best_practice",
                    "severity": "high",
                    "line": node.lineno,
                    "message": "Avoid bare except clauses. Use 'except Exception:' instead of bare 'except:'."
                })

            # Check for hardcoded passwords/credentials
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and hasattr(node, 'value') and isinstance(node.value, ast.Constant):
                        if isinstance(node.value.value, str):
                            lower_val = node.value.value.lower()
                            if any(cred_word in lower_val for cred_word in ['password', 'secret', 'token', 'key']):
                                issues.append({
                                    "type": "security",
                                    "severity": "high",
                                    "line": node.lineno,
                                    "message": f"Avoid hardcoding sensitive information like '{target.id}'. Use environment variables instead."
                                })

        return issues

    def _suggest_improvements(self, tree: ast.AST, code: str) -> List[Dict[str, Any]]:
        """Suggest code improvements"""
        suggestions = []
        lines = code.split('\n')

        # Check for magic numbers
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                # Skip common constants
                if node.value in [0, 1, 2, 10, 100, 1000]:
                    continue

                suggestions.append({
                    "type": "improvement",
                    "severity": "low",
                    "line": node.lineno,
                    "message": f"Consider defining the number {node.value} as a named constant for better readability."
                })

        # Check for print statements that might be debugging
        for node in ast.walk(tree):
            if (isinstance(node, ast.Call) and
                isinstance(node.func, ast.Name) and
                node.func.id == 'print'):

                # Check if it's likely a debugging print
                if len(node.args) > 0 and isinstance(node.args[0], ast.Constant):
                    arg_value = node.args[0].value
                    if isinstance(arg_value, str) and ('debug' in arg_value.lower() or
                                                      'temp' in arg_value.lower() or
                                                      'test' in arg_value.lower()):
                        suggestions.append({
                            "type": "cleanup",
                            "severity": "medium",
                            "line": node.lineno,
                            "message": "Remove debugging print statements before production."
                        })

        return suggestions

    def provide_best_practices_advice(self) -> List[str]:
        """Provide general Python best practices advice"""
        return [
            "Use meaningful variable names that describe what the variable represents",
            "Follow PEP 8 style guide for Python code",
            "Write docstrings for functions and classes",
            "Use type hints for better code clarity",
            "Keep functions small and focused on a single responsibility",
            "Use list comprehensions when appropriate for cleaner code",
            "Handle exceptions appropriately rather than ignoring them"
        ]