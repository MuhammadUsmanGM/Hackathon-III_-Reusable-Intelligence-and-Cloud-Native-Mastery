"""
Progress Tracking API endpoints for LearnFlow
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any, List
import asyncio

from ...services.learnflow_service import get_learnflow_service

router = APIRouter()

@router.get("/{user_id}")
async def get_user_progress(user_id: str):
    """
    Get progress information for a user
    """
    try:
        # Get the LearnFlow service
        service = get_learnflow_service()

        # Get user progress
        progress = await service.get_user_progress(user_id)

        return progress

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving progress: {str(e)}")

@router.post("/update")
async def update_user_progress(request_data: Dict[str, Any]):
    """
    Update progress for a user
    """
    try:
        user_id = request_data.get("user_id")
        lesson_id = request_data.get("lesson_id")
        progress_data = request_data.get("progress_data", {})

        if not user_id or not lesson_id:
            raise HTTPException(status_code=400, detail="user_id and lesson_id are required")

        # Get the LearnFlow service
        service = get_learnflow_service()

        # Update user progress
        result = await service.update_user_progress(user_id, lesson_id, progress_data)

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating progress: {str(e)}")

@router.get("/{user_id}/recommendations")
async def get_learning_recommendations(user_id: str):
    """
    Get personalized learning recommendations for a user
    """
    try:
        # Get the LearnFlow service
        service = get_learnflow_service()

        # Get recommendations
        recommendations = await service.get_learning_recommendations(user_id)

        return recommendations

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving recommendations: {str(e)}")