"""
API v1 endpoints for LearnFlow
"""
from fastapi import APIRouter

# Import all API routes
from . import users, lessons, progress, tutor, code

# Create main API router
api_router = APIRouter()

# Include all API routes
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(lessons.router, prefix="/lessons", tags=["lessons"])
api_router.include_router(progress.router, prefix="/progress", tags=["progress"])
api_router.include_router(tutor.router, prefix="/tutor", tags=["tutor"])
api_router.include_router(code.router, prefix="/code", tags=["code"])