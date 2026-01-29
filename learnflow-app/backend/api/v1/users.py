"""
User Management API endpoints for LearnFlow
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import uuid
from datetime import datetime

from ...services.learnflow_service import get_learnflow_service
from ...models.user import UserCreate

router = APIRouter()

@router.post("/")
async def create_user(user_data: UserCreate):
    """
    Create a new user
    """
    try:
        # Generate a unique ID if not provided
        if not user_data.id:
            user_data.id = str(uuid.uuid4())

        # Get the LearnFlow service
        service = get_learnflow_service()

        # Create the user
        created_user = await service.create_user(user_data.model_dump())

        return created_user

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

@router.get("/{user_id}")
async def get_user(user_id: str):
    """
    Get user information by ID
    """
    try:
        # For now, we'll return a mock user
        # In a real implementation, this would fetch from the database
        return {
            "id": user_id,
            "email": "user@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "role": "student",
            "created_at": datetime.utcnow().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving user: {str(e)}")

@router.get("/")
async def get_users():
    """
    Get all users (for admin purposes)
    """
    try:
        # For now, return a mock list of users
        # In a real implementation, this would fetch from the database
        return {
            "users": [
                {
                    "id": "user-1",
                    "email": "john@example.com",
                    "first_name": "John",
                    "last_name": "Doe",
                    "role": "student"
                }
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving users: {str(e)}")