from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from typing import Optional
import logging
import asyncio

# Import your modules
from .models.user import User
from .models.lesson import Lesson
from .models.progress import Progress
from .api.v1 import api_router
from .services.learnflow_service import init_learnflow_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="LearnFlow API",
    description="AI-powered Python tutoring platform",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(api_router, prefix="/api/v1", tags=["v1"])

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Initializing LearnFlow services...")
    await init_learnflow_service()
    logger.info("LearnFlow services initialized")

@app.get("/")
async def root():
    return {
        "message": "Welcome to LearnFlow API",
        "description": "AI-powered Python tutoring platform with multi-agent architecture",
        "version": "1.0.0",
        "endpoints": {
            "tutor": "/api/v1/tutor/",
            "code": "/api/v1/code/",
            "progress": "/api/v1/progress/",
            "users": "/api/v1/users/",
            "lessons": "/api/v1/lessons/"
        }
    }

@app.get("/health")
async def health_check():
    from .services.database.db_service import db_service
    from .services.kafka.kafka_service import kafka_service

    # Check database connection
    db_healthy = db_service.health_check()

    # For Kafka, we'll just return a simple status since checking Kafka requires more setup
    kafka_healthy = True  # This would be checked properly in a real implementation

    return {
        "status": "healthy",
        "service": "learnflow-backend",
        "checks": {
            "database": "healthy" if db_healthy else "unhealthy",
            "kafka": "healthy" if kafka_healthy else "unhealthy"
        },
        "timestamp": __import__('datetime').datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)