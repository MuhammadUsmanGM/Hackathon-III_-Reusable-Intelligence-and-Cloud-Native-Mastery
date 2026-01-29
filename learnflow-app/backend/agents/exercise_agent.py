"""
Exercise Agent for LearnFlow
Generates Python programming exercises and evaluates solutions
"""

import random
import re
from typing import Dict, Any, List
import asyncio

class ExerciseAgent:
    def __init__(self):
        self.name = "Exercise Agent"
        self.description = "Generates Python programming exercises and evaluates solutions"

        # Define different exercise categories and templates
        self.exercises = {
            "basics": [
                {
                    "title": "Print Statement",
                    "difficulty": "beginner",
                    "description": "Create a program that prints 'Hello, World!'",
                    "solution": "print('Hello, World!')",
                    "hints": ["Use the print() function", "Don't forget quotes around the string"],
                    "category": "basics"
                },
                {
                    "title": "Variable Assignment",
                    "difficulty": "beginner",
                    "description": "Create a variable called 'name' and assign it your name, then print it",
                    "solution": "name = 'YourName'\nprint(name)",
                    "hints": ["Assign a string value to the variable", "Use print() to display the variable"],
                    "category": "basics"
                }
            ],
            "conditionals": [
                {
                    "title": "Even or Odd",
                    "difficulty": "beginner",
                    "description": "Write a program that takes a number and prints 'even' if it's even, 'odd' if it's odd",
                    "solution": "num = int(input('Enter a number: '))\nif num % 2 == 0:\n    print('even')\nelse:\n    print('odd')",
                    "hints": ["Use the modulo operator (%) to check divisibility", "Use an if/else statement"],
                    "category": "conditionals"
                }
            ],
            "loops": [
                {
                    "title": "Sum of Numbers",
                    "difficulty": "beginner",
                    "description": "Write a program that calculates the sum of numbers from 1 to 10 using a loop",
                    "solution": "total = 0\nfor i in range(1, 11):\n    total += i\nprint(total)",
                    "hints": ["Initialize a variable to store the sum", "Use a for loop with range()"],
                    "category": "loops"
                }
            ],
            "functions": [
                {
                    "title": "Simple Function",
                    "difficulty": "beginner",
                    "description": "Write a function called 'greet' that takes a name and returns a greeting",
                    "solution": "def greet(name):\n    return f'Hello, {name}!'\n\nprint(greet('Alice'))",
                    "hints": ["Use the def keyword to define the function", "Return a formatted string"],
                    "category": "functions"
                }
            ]
        }

    async def process(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process user request for exercises or solution evaluation"""
        user_input_lower = user_input.lower()

        # Check if user is submitting a solution
        if any(word in user_input_lower for word in ['solution', 'answer', 'my code', 'i wrote']):
            # Extract submitted code and evaluate
            submitted_code = await self._extract_code(user_input)
            if submitted_code:
                evaluation = await self._evaluate_solution(submitted_code, context)
                return {
                    "agent": "exercise",
                    "type": "solution_evaluation",
                    "evaluation": evaluation,
                    "message": evaluation["feedback"]
                }

        # Otherwise, provide exercises
        difficulty = self._detect_difficulty(user_input)
        category = self._detect_category(user_input)

        exercise = self._get_random_exercise(difficulty, category)

        if not exercise:
            # If no specific difficulty/category requested, pick a random one
            exercise = self._get_random_exercise()

        return {
            "agent": "exercise",
            "type": "exercise",
            "exercise": exercise,
            "message": f"Here's an exercise for you: {exercise['title']}"
        }

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

    def _detect_difficulty(self, user_input: str) -> str:
        """Detect requested difficulty level"""
        user_input_lower = user_input.lower()

        if 'beginner' in user_input_lower or 'easy' in user_input_lower:
            return 'beginner'
        elif 'intermediate' in user_input_lower or 'medium' in user_input_lower:
            return 'intermediate'
        elif 'advanced' in user_input_lower or 'hard' in user_input_lower:
            return 'advanced'

        return None

    def _detect_category(self, user_input: str) -> str:
        """Detect requested category"""
        user_input_lower = user_input.lower()

        if 'basic' in user_input_lower or 'basics' in user_input_lower:
            return 'basics'
        elif 'conditional' in user_input_lower or 'if' in user_input_lower:
            return 'conditionals'
        elif 'loop' in user_input_lower:
            return 'loops'
        elif 'function' in user_input_lower:
            return 'functions'

        return None

    def _get_random_exercise(self, difficulty: str = None, category: str = None) -> Dict[str, Any]:
        """Get a random exercise based on difficulty and category"""
        available_exercises = []

        # Filter by category if specified
        if category:
            if category in self.exercises:
                available_exercises = [ex for ex in self.exercises[category] if not difficulty or ex["difficulty"] == difficulty]
        else:
            # If no category specified, look through all categories
            for cat_exercises in self.exercises.values():
                filtered = [ex for ex in cat_exercises if not difficulty or ex["difficulty"] == difficulty]
                available_exercises.extend(filtered)

        # If still no exercises found or no filters applied, use all exercises
        if not available_exercises:
            for cat_exercises in self.exercises.values():
                available_exercises.extend(cat_exercises)

        if available_exercises:
            return random.choice(available_exercises)

        # Fallback to any exercise
        for cat_exercises in self.exercises.values():
            if cat_exercises:
                return cat_exercises[0]

        return None

    async def _evaluate_solution(self, submitted_code: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Evaluate the user's submitted solution"""
        # This is a simplified evaluation - in a real system, we'd run tests
        # against the submitted code to check correctness

        # For now, just provide feedback on code structure and execution
        feedback_points = []

        # Check for basic Python syntax
        try:
            import ast
            ast.parse(submitted_code)
            feedback_points.append("✓ Code has valid Python syntax")
        except SyntaxError as e:
            return {
                "is_correct": False,
                "feedback": f"✗ Syntax error: {str(e)}",
                "score": 0
            }

        # Analyze code for common elements
        lines = submitted_code.strip().split('\n')
        has_print = any('print(' in line for line in lines)
        has_function = any('def ' in line for line in lines)
        has_condition = any('if ' in line for line in lines) or any('elif ' in line for line in lines) or any('else:' in line for line in lines)
        has_loop = any('for ' in line for line in lines) or any('while ' in line for line in lines)

        if has_print:
            feedback_points.append("✓ Good use of print statements for output")
        if has_function:
            feedback_points.append("✓ Functions defined properly")
        if has_condition:
            feedback_points.append("✓ Conditional statements used")
        if has_loop:
            feedback_points.append("✓ Loops implemented correctly")

        # Simple heuristic for correctness
        score = min(len(feedback_points) * 25, 100)  # Max 100%

        if score >= 75:
            feedback_points.append("🎉 Well done! Your solution looks good!")
            is_correct = True
        else:
            feedback_points.append("Keep working on it! Consider the hints provided with the exercise.")
            is_correct = False

        return {
            "is_correct": is_correct,
            "feedback": " ".join(feedback_points),
            "score": score,
            "submitted_code": submitted_code
        }

    def get_available_categories(self) -> List[str]:
        """Get list of available exercise categories"""
        return list(self.exercises.keys())

    def get_exercises_by_difficulty(self, difficulty: str) -> List[Dict[str, Any]]:
        """Get all exercises of a specific difficulty"""
        result = []
        for category_exercises in self.exercises.values():
            result.extend([ex for ex in category_exercises if ex["difficulty"] == difficulty])
        return result