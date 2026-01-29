"""
Main LearnFlow Service
Integrates all services and handles business logic
"""
import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

from .ai.ai_service import AIService
from .code_execution.code_executor import execute_code
from .kafka.kafka_service import kafka_service, send_user_interaction, send_progress_update, send_ai_interaction
from .database.db_service import db_service, get_db_service
from ..models.user import UserCreate
from ..models.progress import ProgressUpdate

logger = logging.getLogger(__name__)

class LearnFlowService:
    def __init__(self):
        self.ai_service = AIService()

    async def initialize(self):
        """Initialize all services"""
        # Initialize Kafka service
        await kafka_service.init_kafka_service()

        # Initialize database service
        # Note: This would normally be called separately during app startup
        # db_service.init_db_service()

        logger.info("LearnFlow service initialized")

    async def process_tutor_request(self, user_id: str, message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process a tutoring request from a user

        Args:
            user_id: ID of the user making the request
            message: The user's message or question
            context: Additional context information

        Returns:
            Response from the AI tutor
        """
        try:
            # Add user info to context
            full_context = {
                "student_id": user_id,
                "timestamp": datetime.utcnow().isoformat(),
                **(context or {})
            }

            # Process the request with the AI service
            ai_response = await self.ai_service.process_tutor_request(message, full_context)

            # Send AI interaction event to Kafka
            await send_ai_interaction(
                user_id=user_id,
                query=message,
                response=ai_response.get("message", ""),
                agent_type=ai_response.get("agent", "unknown")
            )

            # Send user interaction event to Kafka
            await send_user_interaction(
                user_id=user_id,
                interaction_type="tutor_request",
                data={
                    "query": message,
                    "response_agent": ai_response.get("agent"),
                    "response_confidence": ai_response.get("confidence")
                }
            )

            return ai_response
        except Exception as e:
            logger.error(f"Error processing tutor request: {str(e)}")
            return {
                "agent": "error",
                "message": "Sorry, I encountered an error processing your request. Please try again.",
                "error": str(e)
            }

    async def execute_user_code(self, user_id: str, code: str, input_data: str = "") -> Dict[str, Any]:
        """
        Execute code submitted by a user

        Args:
            user_id: ID of the user submitting the code
            code: Code to execute
            input_data: Input data for the code

        Returns:
            Execution results
        """
        try:
            # Execute the code
            execution_result = await execute_code(code, input_data)

            # Send user interaction event to Kafka
            await send_user_interaction(
                user_id=user_id,
                interaction_type="code_execution",
                data={
                    "code_preview": code[:100] + "..." if len(code) > 100 else code,
                    "execution_status": execution_result["status"],
                    "execution_time": execution_result["execution_time"]
                }
            )

            return execution_result
        except Exception as e:
            logger.error(f"Error executing user code: {str(e)}")
            return {
                "output": "",
                "errors": str(e),
                "status": "error",
                "execution_time": 0,
                "return_code": -1
            }

    async def get_user_progress(self, user_id: str) -> Dict[str, Any]:
        """
        Get progress information for a user

        Args:
            user_id: ID of the user

        Returns:
            User progress information
        """
        try:
            # Get progress from AI service
            ai_progress = await self.ai_service.get_student_progress(user_id)

            # Get progress from database
            db_progress = db_service.get_user_progress(user_id)

            # Combine both results
            combined_progress = {
                **ai_progress,
                "db_progress_records": db_progress,
                "last_updated": datetime.utcnow().isoformat()
            }

            return combined_progress
        except Exception as e:
            logger.error(f"Error getting user progress: {str(e)}")
            return {
                "error": str(e),
                "message": "Could not retrieve progress at this time"
            }

    async def update_user_progress(self, user_id: str, lesson_id: str, progress_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update progress for a user

        Args:
            user_id: ID of the user
            lesson_id: ID of the lesson
            progress_data: Progress data to update

        Returns:
            Updated progress information
        """
        try:
            # Update progress in database
            updated_progress = db_service.update_progress(user_id, lesson_id, progress_data)

            # Send progress update event to Kafka
            await send_progress_update(
                user_id=user_id,
                progress_data={
                    "lesson_id": lesson_id,
                    "updated_fields": progress_data,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )

            # Update progress in AI service
            context = {"student_id": user_id, "lesson_id": lesson_id}
            await self.ai_service.process_tutor_request(
                f"Update progress for lesson {lesson_id}",
                context
            )

            return updated_progress
        except Exception as e:
            logger.error(f"Error updating user progress: {str(e)}")
            return {
                "error": str(e),
                "message": "Could not update progress at this time"
            }

    async def get_learning_recommendations(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get personalized learning recommendations for a user

        Args:
            user_id: ID of the user

        Returns:
            List of learning recommendations
        """
        try:
            recommendations = await self.ai_service.get_learning_recommendations(user_id)

            # Send user interaction event to Kafka
            await send_user_interaction(
                user_id=user_id,
                interaction_type="get_recommendations",
                data={
                    "num_recommendations": len(recommendations),
                    "timestamp": datetime.utcnow().isoformat()
                }
            )

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

    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new user

        Args:
            user_data: User information

        Returns:
            Created user information
        """
        try:
            # Create user in database
            created_user = db_service.create_user(user_data)

            # Send user interaction event to Kafka
            await send_user_interaction(
                user_id=created_user["id"],
                interaction_type="user_created",
                data={
                    "user_email": created_user["email"],
                    "user_role": created_user["role"],
                    "timestamp": datetime.utcnow().isoformat()
                }
            )

            return created_user
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            raise

    async def review_code(self, user_id: str, code: str) -> Dict[str, Any]:
        """
        Review code submitted by a user

        Args:
            user_id: ID of the user
            code: Code to review

        Returns:
            Code review results
        """
        try:
            # Review the code with AI
            review_result = await self.ai_service.review_code(code)

            # Send user interaction event to Kafka
            await send_user_interaction(
                user_id=user_id,
                interaction_type="code_review",
                data={
                    "code_preview": code[:100] + "..." if len(code) > 100 else code,
                    "num_issues_found": len(review_result.get("review", {}).get("issues", [])),
                    "num_suggestions": len(review_result.get("review", {}).get("suggestions", []))
                }
            )

            # Send AI interaction event to Kafka
            await send_ai_interaction(
                user_id=user_id,
                query=f"Review this code: {code[:50]}...",
                response=f"Found {len(review_result.get('review', {}).get('issues', []))} issues",
                agent_type="code_review"
            )

            return review_result
        except Exception as e:
            logger.error(f"Error reviewing code: {str(e)}")
            return {
                "error": str(e),
                "message": "Could not review code at this time"
            }

    async def debug_code(self, user_id: str, code: str, error_msg: str = "") -> Dict[str, Any]:
        """
        Debug code submitted by a user

        Args:
            user_id: ID of the user
            code: Code to debug
            error_msg: Optional error message

        Returns:
            Debug results
        """
        try:
            # Debug the code with AI
            debug_result = await self.ai_service.debug_code(code, error_msg)

            # Send user interaction event to Kafka
            await send_user_interaction(
                user_id=user_id,
                interaction_type="code_debug",
                data={
                    "code_preview": code[:100] + "..." if len(code) > 100 else code,
                    "has_error_msg": bool(error_msg),
                    "debug_result_type": debug_result.get("debug_analysis", {}).get("error_type", "unknown")
                }
            )

            return debug_result
        except Exception as e:
            logger.error(f"Error debugging code: {str(e)}")
            return {
                "error": str(e),
                "message": "Could not debug code at this time"
            }

    async def evaluate_exercise_solution(self, user_id: str, exercise_id: str, solution: str) -> Dict[str, Any]:
        """
        Evaluate a user's exercise solution

        Args:
            user_id: ID of the user
            exercise_id: ID of the exercise
            solution: User's solution

        Returns:
            Evaluation results
        """
        try:
            # Evaluate the solution with AI
            evaluation = await self.ai_service.evaluate_exercise_solution(exercise_id, solution)

            # Update progress based on evaluation
            if evaluation.get("evaluation", {}).get("is_correct"):
                await self.update_user_progress(
                    user_id=user_id,
                    lesson_id=exercise_id,
                    progress_data={
                        "status": "completed",
                        "score": evaluation["evaluation"].get("score", 0),
                        "attempts": 1
                    }
                )

            # Send user interaction event to Kafka
            await send_user_interaction(
                user_id=user_id,
                interaction_type="exercise_evaluation",
                data={
                    "exercise_id": exercise_id,
                    "solution_preview": solution[:100] + "..." if len(solution) > 100 else solution,
                    "is_correct": evaluation.get("evaluation", {}).get("is_correct", False),
                    "score": evaluation["evaluation"].get("score", 0)
                }
            )

            return evaluation
        except Exception as e:
            logger.error(f"Error evaluating exercise solution: {str(e)}")
            return {
                "error": str(e),
                "message": "Could not evaluate solution at this time"
            }


# Global LearnFlow service instance
learnflow_service = LearnFlowService()


async def init_learnflow_service():
    """
    Initialize the LearnFlow service
    """
    await learnflow_service.initialize()
    logger.info("LearnFlow service initialized globally")


def get_learnflow_service() -> LearnFlowService:
    """
    Get the LearnFlow service instance

    Returns:
        LearnFlowService instance
    """
    return learnflow_service