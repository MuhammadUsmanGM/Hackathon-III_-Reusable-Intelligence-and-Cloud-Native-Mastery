"""
Code Execution API endpoints for LearnFlow
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any
import asyncio

from ...services.learnflow_service import get_learnflow_service
from ...services.code_execution.code_executor import execute_code

router = APIRouter()

@router.post("/")
async def execute_user_code(request_data: Dict[str, Any]):
    """
    Execute code submitted by a user
    """
    try:
        user_id = request_data.get("user_id")
        code_text = request_data.get("code")
        input_data = request_data.get("input", "")
        language = request_data.get("language", "python")

        if not user_id or not code_text:
            raise HTTPException(status_code=400, detail="user_id and code are required")

        # Get the LearnFlow service
        service = get_learnflow_service()

        # Execute the code
        result = await service.execute_user_code(user_id, code_text, input_data)

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing code: {str(e)}")

@router.post("/evaluate-exercise")
async def evaluate_exercise_solution(request_data: Dict[str, Any]):
    """
    Evaluate a user's exercise solution
    """
    try:
        user_id = request_data.get("user_id")
        exercise_id = request_data.get("exercise_id")
        solution = request_data.get("solution")

        if not user_id or not exercise_id or not solution:
            raise HTTPException(
                status_code=400,
                detail="user_id, exercise_id, and solution are required"
            )

        # Get the LearnFlow service
        service = get_learnflow_service()

        # Evaluate the solution
        result = await service.evaluate_exercise_solution(user_id, exercise_id, solution)

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating solution: {str(e)}")