from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class ProgressBase(BaseModel):
    user_id: str
    lesson_id: str
    status: str  # not_started, in_progress, completed
    score: Optional[float] = None
    time_spent: int  # in seconds
    attempts: int = 0

class ProgressUpdate(ProgressBase):
    pass

class Progress(ProgressBase):
    id: str
    created_at: datetime
    updated_at: datetime
    metadata: Optional[Dict[str, Any]] = {}

    class Config:
        from_attributes = True