"""
Triage Agent for LearnFlow
Initial assessment of student needs and routing to appropriate agents
"""

import asyncio
from typing import Dict, Any, List
from enum import Enum

class StudentLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class TriageAgent:
    def __init__(self):
        self.name = "Triage Agent"
        self.description = "Assesses student needs and routes to appropriate agents"

    async def process(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process user input and assess their needs"""
        assessment = await self._assess_needs(user_input, context)

        response = {
            "agent": "triage",
            "assessment": assessment,
            "recommendation": assessment.get("recommended_agent"),
            "confidence": assessment.get("confidence", 0.8),
            "next_steps": assessment.get("next_steps", []),
            "message": self._generate_response(assessment)
        }

        return response

    async def _assess_needs(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Assess the student's needs based on their input"""
        # Analyze the user's input to determine their level and needs
        input_lower = user_input.lower()

        # Assess programming level based on keywords
        level_indicators = {
            StudentLevel.BEGINNER: [
                'print', 'variable', 'string', 'number', 'input', 'output', 'hello world',
                'if', 'else', 'loop', 'for loop', 'while loop', 'function', 'list', 'dictionary'
            ],
            StudentLevel.INTERMEDIATE: [
                'class', 'object', 'inheritance', 'method', 'exception', 'file', 'module',
                'import', 'package', 'decorator', 'generator', 'iterator', 'lambda'
            ],
            StudentLevel.ADVANCED: [
                'thread', 'async', 'concurrent', 'optimization', 'design pattern', 'algorithm',
                'data structure', 'memory', 'performance', 'framework', 'architecture'
            ]
        }

        detected_level = StudentLevel.BEGINNER  # Default to beginner

        for level, indicators in level_indicators.items():
            if any(indicator in input_lower for indicator in indicators):
                detected_level = level
                break

        # Determine what kind of help is needed
        needs_keywords = {
            "debugging": ['error', 'bug', 'fix', 'not working', 'problem', 'issue'],
            "learning_concept": ['what is', 'explain', 'how does', 'understand', 'concept', 'topic'],
            "code_review": ['review', 'improve', 'better', 'optimize', 'style', 'best practice'],
            "exercise": ['practice', 'exercise', 'challenge', 'problem', 'solve']
        }

        needs = []
        for need, keywords in needs_keywords.items():
            if any(keyword in input_lower for keyword in keywords):
                needs.append(need)

        # Determine recommended agent based on needs
        recommended_agent = "triage"  # Default
        if "debugging" in needs:
            recommended_agent = "debug"
        elif "learning_concept" in needs:
            recommended_agent = "concepts"
        elif "code_review" in needs:
            recommended_agent = "code_review"
        elif "exercise" in needs:
            recommended_agent = "exercise"

        return {
            "detected_level": detected_level.value,
            "identified_needs": needs,
            "recommended_agent": recommended_agent,
            "confidence": 0.8,
            "next_steps": self._suggest_next_steps(detected_level, needs)
        }

    def _suggest_next_steps(self, level: StudentLevel, needs: List[str]) -> List[str]:
        """Suggest next steps based on assessment"""
        suggestions = []

        if level == StudentLevel.BEGINNER:
            suggestions.extend([
                "Start with basic Python concepts",
                "Try simple exercises to build confidence",
                "Focus on understanding syntax and basic constructs"
            ])
        elif level == StudentLevel.INTERMEDIATE:
            suggestions.extend([
                "Practice object-oriented programming concepts",
                "Work on more complex problem-solving",
                "Learn about exception handling and file operations"
            ])
        elif level == StudentLevel.ADVANCED:
            suggestions.extend([
                "Explore advanced Python features",
                "Study design patterns and architecture",
                "Focus on performance optimization"
            ])

        if "debugging" in needs:
            suggestions.append("Let me help you debug your code")
        if "learning_concept" in needs:
            suggestions.append("I can explain that concept in detail")
        if "code_review" in needs:
            suggestions.append("I can review your code and suggest improvements")
        if "exercise" in needs:
            suggestions.append("I can provide practice exercises")

        return suggestions

    def _generate_response(self, assessment: Dict[str, Any]) -> str:
        """Generate a human-readable response"""
        level = assessment["detected_level"]
        needs = assessment["identified_needs"]

        response_parts = [
            f"I've assessed your needs as a {level} Python learner.",
            f"Based on your input, you seem to need help with: {', '.join(needs) if needs else 'general Python learning'}."
        ]

        if assessment["recommended_agent"] != "triage":
            response_parts.append(f"I recommend routing you to our {assessment['recommended_agent'].replace('_', ' ')} agent.")

        response_parts.append("Here are some suggested next steps:")
        for i, step in enumerate(assessment["next_steps"][:2]):  # Limit to 2 suggestions
            response_parts.append(f"- {step}")

        return " ".join(response_parts)