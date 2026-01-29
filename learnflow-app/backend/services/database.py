from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func
from contextlib import contextmanager
import os
from typing import Generator

# Use environment variables or defaults
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:secretpassword@localhost:5432/learnflow")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Example model definition (would be expanded in real implementation)
class DBUser(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(String, default="student")
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class DBLesson(Base):
    __tablename__ = "lessons"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    content = Column(Text)
    difficulty = Column(String)
    category = Column(String)
    estimated_duration = Column(Integer)
    slug = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class DBProgress(Base):
    __tablename__ = "progress"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    lesson_id = Column(String, index=True)
    status = Column(String, default="not_started")
    score = Column(Integer)
    time_spent = Column(Integer, default=0)
    attempts = Column(Integer, default=0)
    metadata = Column(String)  # JSON as text
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# Create tables
def init_db():
    Base.metadata.create_all(bind=engine)