"""
Concepts Agent for LearnFlow
Explains Python programming concepts with examples and exercises
"""

import asyncio
from typing import Dict, Any, List
import re

class ConceptsAgent:
    def __init__(self):
        self.name = "Concepts Agent"
        self.description = "Explains Python programming concepts with examples"

        # Predefined concepts with explanations
        self.concepts = {
            "variables": {
                "title": "Variables",
                "explanation": "Variables are containers for storing data values. In Python, you don't need to declare the type of variable before using it.",
                "example": "```python\n# Creating variables\nname = \"Alice\"\nage = 25\nheight = 5.6\n\nprint(name)\nprint(age)\nprint(height)\n```",
                "exercise": "Create three variables: one for your name (string), one for your age (integer), and one for your favorite number (float). Print all three variables."
            },
            "data_types": {
                "title": "Data Types",
                "explanation": "Python has several built-in data types including integers, floats, strings, booleans, lists, tuples, and dictionaries.",
                "example": "```python\n# Different data types\ninteger_var = 42\nfloat_var = 3.14\nstring_var = \"Hello\"\nbool_var = True\nlist_var = [1, 2, 3]\ndict_var = {\"key\": \"value\"}\n\nprint(type(integer_var))  # <class 'int'>\n```",
                "exercise": "Create variables of each data type mentioned (integer, float, string, boolean, list, dictionary). Use the type() function to print the type of each variable."
            },
            "conditionals": {
                "title": "Conditionals (if/elif/else)",
                "explanation": "Conditional statements allow you to execute different blocks of code based on certain conditions.",
                "example": "```python\n# Conditional statements\nage = 18\n\nif age >= 18:\n    print(\"You are an adult\")\nelif age >= 13:\n    print(\"You are a teenager\")\nelse:\n    print(\"You are a child\")\n```",
                "exercise": "Write a program that takes a number as input and prints whether it's positive, negative, or zero."
            },
            "loops": {
                "title": "Loops (for/while)",
                "explanation": "Loops allow you to execute a block of code multiple times. Python has for loops and while loops.",
                "example": "```python\n# For loop\nfruits = [\"apple\", \"banana\", \"cherry\"]\nfor fruit in fruits:\n    print(fruit)\n\n# While loop\ncount = 0\nwhile count < 5:\n    print(count)\n    count += 1\n```",
                "exercise": "Write a for loop that prints the numbers 1 to 10. Then write a while loop that prints the numbers 10 down to 1."
            },
            "functions": {
                "title": "Functions",
                "explanation": "Functions are blocks of code that perform a specific task. You can pass data to functions and get results back.",
                "example": "```python\n# Defining a function\ndef greet(name):\n    return f\"Hello, {name}!\"\n\n# Calling the function\nmessage = greet(\"Alice\")\nprint(message)  # Output: Hello, Alice!\n\n# Function with multiple parameters\ndef add_numbers(a, b):\n    return a + b\n\nresult = add_numbers(5, 3)\nprint(result)  # Output: 8\n```",
                "exercise": "Write a function that takes two numbers as parameters and returns their product. Test the function with different inputs."
            }
        }

    async def process(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process user request for concept explanation"""
        concept_requested = await self._identify_concept(user_input)

        if concept_requested and concept_requested in self.concepts:
            concept_data = self.concepts[concept_requested]

            response = {
                "agent": "concepts",
                "concept": concept_requested,
                "title": concept_data["title"],
                "explanation": concept_data["explanation"],
                "example": concept_data["example"],
                "exercise": concept_data["exercise"],
                "confidence": 0.9,
                "message": f"Here's an explanation of {concept_data['title']}:"
            }
        else:
            # If no specific concept found, provide general Python concepts overview
            available_concepts = list(self.concepts.keys())
            response = {
                "agent": "concepts",
                "available_concepts": available_concepts,
                "message": f"I can explain the following Python concepts: {', '.join(available_concepts)}. Please ask about a specific concept you'd like to learn about.",
                "confidence": 0.8
            }

        return response

    async def _identify_concept(self, user_input: str) -> str:
        """Identify which concept the user is asking about"""
        user_input_lower = user_input.lower()

        # Map common terms to concept keys
        term_to_concept = {
            "variable": "variables",
            "data type": "data_types",
            "data type": "data_types",
            "conditional": "conditionals",
            "if statement": "conditionals",
            "if else": "conditionals",
            "loop": "loops",
            "for loop": "loops",
            "while loop": "loops",
            "function": "functions",
            "def": "functions",
            "define function": "functions"
        }

        # Check for exact matches first
        for term, concept in term_to_concept.items():
            if term in user_input_lower:
                return concept

        # Check for concept keys directly
        for concept in self.concepts.keys():
            if concept.replace("_", " ") in user_input_lower or concept in user_input_lower:
                return concept

        return None

    def get_concept_explanation(self, concept_name: str) -> Dict[str, Any]:
        """Get explanation for a specific concept"""
        if concept_name in self.concepts:
            return self.concepts[concept_name]
        return None

    def get_all_concepts(self) -> List[str]:
        """Get list of all available concepts"""
        return list(self.concepts.keys())