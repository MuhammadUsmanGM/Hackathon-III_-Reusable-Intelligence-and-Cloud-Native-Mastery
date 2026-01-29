"""
Lesson Management API endpoints for LearnFlow
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import uuid
from datetime import datetime

from ...services.database.db_service import get_db_service
from ...models.lesson import LessonCreate

router = APIRouter()

@router.get("/")
async def get_all_lessons():
    """
    Get all available lessons
    """
    try:
        # Get the database service
        db_service = get_db_service()

        # Get all lessons
        lessons = db_service.get_all_lessons()

        return {
            "lessons": lessons,
            "count": len(lessons)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving lessons: {str(e)}")

@router.get("/{lesson_id}")
async def get_lesson(lesson_id: str):
    """
    Get a specific lesson by ID
    """
    try:
        # For now, return a mock lesson
        # In a real implementation, this would fetch from the database
        return {
            "id": lesson_id,
            "title": "Sample Lesson",
            "description": "This is a sample lesson for demonstration purposes",
            "content": "# Sample Lesson\n\nThis is the content of the sample lesson.\n\n## Topics Covered\n\n- Topic 1\n- Topic 2\n- Topic 3",
            "difficulty": "beginner",
            "category": "programming",
            "estimated_duration": 15,
            "slug": f"sample-lesson-{lesson_id}",
            "created_at": datetime.utcnow().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving lesson: {str(e)}")

@router.get("/by-slug/{slug}")
async def get_lesson_by_slug(slug: str):
    """
    Get a lesson by its slug
    """
    try:
        # Get the database service
        db_service = get_db_service()

        # Get lesson by slug
        lesson = db_service.get_lesson_by_slug(slug)

        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")

        return lesson

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving lesson: {str(e)}")

@router.post("/")
async def create_lesson(lesson_data: LessonCreate):
    """
    Create a new lesson
    """
    try:
        # Generate a slug if not provided
        if not lesson_data.slug:
            # Create a slug from the title (simplified)
            import re
            title_slug = re.sub(r'[^\w\s-]', '', lesson_data.title.lower())
            title_slug = re.sub(r'[-\s]+', '-', title_slug.strip())
            lesson_data.slug = title_slug

        # Get the database service
        db_service = get_db_service()

        # Create the lesson
        created_lesson = db_service.create_lesson(lesson_data.model_dump())

        return created_lesson

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating lesson: {str(e)}")