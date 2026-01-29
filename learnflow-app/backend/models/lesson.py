from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class LessonBase(BaseModel):
    title: str
    description: str
    content: str
    difficulty: str  # beginner, intermediate, advanced
    category: str
    estimated_duration: int  # in minutes

class LessonCreate(LessonBase):
    pass

class LessonUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    difficulty: Optional[str] = None
    category: Optional[str] = None
    estimated_duration: Optional[int] = None

class Lesson(LessonBase):
    id: str
    slug: str
    created_at: datetime
    updated_at: datetime
    prerequisites: List[str] = []
    objectives: List[str] = []

    class Config:
        from_attributes = True