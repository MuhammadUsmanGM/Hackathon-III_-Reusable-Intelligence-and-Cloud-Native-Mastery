"""
AI Service for LearnFlow
Handles communication with AI agents and manages AI-related functionality
"""
import asyncio
import logging
from typing import Dict, Any, List
from agents.agent_manager import AgentManager
from agents.triage_agent import TriageAgent
from agents.concepts_agent import ConceptsAgent
from agents.code_review_agent import CodeReviewAgent
from agents.debug_agent import DebugAgent
from agents.exercise_agent import ExerciseAgent
from agents.progress_agent import ProgressAgent

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.agent_manager = AgentManager()
        self.triage_agent = TriageAgent()
        self.concepts_agent = ConceptsAgent()
        self.code_review_agent = CodeReviewAgent()
        self.debug_agent = DebugAgent()
        self.exercise_agent = ExerciseAgent()
        self.progress_agent = ProgressAgent()

    async def process_tutor_request(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process a tutoring request using the appropriate AI agent

        Args:
            user_input: The user's request or question
            context: Additional context information

        Returns:
            Response from the AI agent
        """
        try:
            # Route the request to the appropriate agent based on content
            response = await self.agent_manager.route_request(user_input, context)

            # Log the interaction
            logger.info(f"Processed AI request for user: {context.get('student_id', 'unknown') if context else 'unknown'}")

            return response
        except Exception as e:
            logger.error(f"Error processing AI request: {str(e)}")
            return {
                "agent": "error",
                "message": "Sorry, I encountered an error processing your request. Please try again.",
                "error": str(e)
            }

    async def get_concept_explanation(self, concept_name: str) -> Dict[str, Any]:
        """
        Get explanation for a specific programming concept

        Args:
            concept_name: Name of the concept to explain

        Returns:
            Explanation of the concept
        """
        try:
            return self.concepts_agent.get_concept_explanation(concept_name)
        except Exception as e:
            logger.error(f"Error getting concept explanation: {str(e)}")
            return {
                "error": str(e),
                "message": f"Could not find explanation for concept: {concept_name}"
            }

    async def review_code(self, code: str) -> Dict[str, Any]:
        """
        Review code and provide suggestions for improvement

        Args:
            code: Code to review

        Returns:
            Code review results
        """
        try:
            # Create a mock context for the code review agent
            context = {"source": "frontend_request"}
            result = await self.code_review_agent.process(code, context)
            return result
        except Exception as e:
            logger.error(f"Error reviewing code: {str(e)}")
            return {
                "error": str(e),
                "message": "Could not review code at this time"
            }

    async def debug_code(self, code: str, error_msg: str = "") -> Dict[str, Any]:
        """
        Help debug code with error message if available

        Args:
            code: Code to debug
            error_msg: Optional error message to help with debugging

        Returns:
            Debug analysis results
        """
        try:
            user_input = f"Please help debug this code: {code}"
            if error_msg:
                user_input += f"\nError message: {error_msg}"

            context = {"source": "frontend_request"}
            result = await self.debug_agent.process(user_input, context)
            return result
        except Exception as e:
            logger.error(f"Error debugging code: {str(e)}")
            return {
                "error": str(e),
                "message": "Could not debug code at this time"
            }

    async def evaluate_exercise_solution(self, exercise_id: str, solution: str) -> Dict[str, Any]:
        """
        Evaluate a student's exercise solution

        Args:
            exercise_id: ID of the exercise
            solution: Student's solution code

        Returns:
            Evaluation results
        """
        try:
            user_input = f"Evaluate this solution for exercise {exercise_id}: {solution}"
            context = {"exercise_id": exercise_id, "source": "exercise_evaluation"}
            result = await self.exercise_agent.process(user_input, context)
            return result
        except Exception as e:
            logger.error(f"Error evaluating exercise solution: {str(e)}")
            return {
                "error": str(e),
                "message": "Could not evaluate solution at this time"
            }

    async def get_student_progress(self, student_id: str) -> Dict[str, Any]:
        """
        Get student progress information

        Args:
            student_id: ID of the student

        Returns:
            Student progress information
        """
        try:
            progress = await self.progress_agent.get_student_progress(student_id)
            return progress
        except Exception as e:
            logger.error(f"Error getting student progress: {str(e)}")
            return {
                "error": str(e),
                "message": "Could not retrieve progress at this time"
            }

    async def get_learning_recommendations(self, student_id: str) -> List[Dict[str, Any]]:
        """
        Get personalized learning recommendations for a student

        Args:
            student_id: ID of the student

        Returns:
            List of learning recommendations
        """
        try:
            recommendations = await self.progress_agent.get_recommendations(student_id)
            return recommendations
        except Exception as e:
            logger.error(f"Error getting learning recommendations: {str(e)}")
            return [
                {
                    "type": "error",
                    "priority": "low",
                    "title": "Error Retrieving Recommendations",
                    "description": f"Could not get recommendations: {str(e)}"
                }
            ]