"""
Tutor API endpoints for LearnFlow
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import asyncio

from ...services.learnflow_service import get_learnflow_service
from ...services.ai.ai_service import AIService

router = APIRouter()

@router.post("/")
async def process_tutor_request(request_data: Dict[str, Any]):
    """
    Process a tutoring request from the frontend
    """
    try:
        # Extract required fields
        user_id = request_data.get("user_id")
        message = request_data.get("message")
        context = request_data.get("context", {})

        if not user_id or not message:
            raise HTTPException(status_code=400, detail="user_id and message are required")

        # Get the LearnFlow service
        service = get_learnflow_service()

        # Process the request
        result = await service.process_tutor_request(user_id, message, context)

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing tutor request: {str(e)}")

@router.post("/explain-concept")
async def explain_concept(request_data: Dict[str, Any]):
    """
    Get explanation for a specific programming concept
    """
    try:
        concept_name = request_data.get("concept")

        if not concept_name:
            raise HTTPException(status_code=400, detail="concept is required")

        # Get the AI service
        ai_service = AIService()

        # Get concept explanation
        explanation = await ai_service.get_concept_explanation(concept_name)

        return explanation

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting concept explanation: {str(e)}")

@router.post("/review-code")
async def review_code(request_data: Dict[str, Any]):
    """
    Review code and provide suggestions
    """
    try:
        user_id = request_data.get("user_id")
        code_text = request_data.get("code")

        if not user_id or not code_text:
            raise HTTPException(status_code=400, detail="user_id and code are required")

        # Get the LearnFlow service
        service = get_learnflow_service()

        # Review the code
        result = await service.review_code(user_id, code_text)

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reviewing code: {str(e)}")

@router.post("/debug-code")
async def debug_code_endpoint(request_data: Dict[str, Any]):
    """
    Debug code with potential error message
    """
    try:
        user_id = request_data.get("user_id")
        code_text = request_data.get("code")
        error_msg = request_data.get("error", "")

        if not user_id or not code_text:
            raise HTTPException(status_code=400, detail="user_id and code are required")

        # Get the LearnFlow service
        service = get_learnflow_service()

        # Debug the code
        result = await service.debug_code(user_id, code_text, error_msg)

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error debugging code: {str(e)}")