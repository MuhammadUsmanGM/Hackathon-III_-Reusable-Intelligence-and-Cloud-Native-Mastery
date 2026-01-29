"""
Database Service for LearnFlow
Handles database operations for user data, lessons, progress, etc.
"""
import logging
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from contextlib import contextmanager
import os
from ..models.user import DBUser
from ..models.lesson import DBLesson
from ..models.progress import DBProgress

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self, database_url: str = None):
        # Use environment variable or default to PostgreSQL
        self.database_url = database_url or os.getenv("DATABASE_URL", "postgresql://postgres:secretpassword@localhost:5432/learnflow")
        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    @contextmanager
    def get_session(self):
        """Context manager for database sessions"""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database error: {str(e)}")
            raise
        finally:
            session.close()

    def init_database(self):
        """Initialize the database tables"""
        try:
            # Import all models to register them with SQLAlchemy
            from ..models.user import DBUser
            from ..models.lesson import DBLesson
            from ..models.progress import DBProgress

            # Create all tables
            from ..services.database import Base
            Base.metadata.create_all(bind=self.engine)

            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database: {str(e)}")
            raise

    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user"""
        try:
            with self.get_session() as session:
                # Check if user already exists
                existing_user = session.query(DBUser).filter(DBUser.email == user_data["email"]).first()
                if existing_user:
                    raise ValueError(f"User with email {user_data['email']} already exists")

                # Create new user
                db_user = DBUser(**user_data)
                session.add(db_user)

                # Flush to get the ID
                session.flush()

                # Return user data
                user_dict = {
                    "id": db_user.id,
                    "email": db_user.email,
                    "first_name": db_user.first_name,
                    "last_name": db_user.last_name,
                    "role": db_user.role,
                    "created_at": db_user.created_at.isoformat() if db_user.created_at else None
                }

                return user_dict
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            raise

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        try:
            with self.get_session() as session:
                db_user = session.query(DBUser).filter(DBUser.email == email).first()

                if not db_user:
                    return None

                return {
                    "id": db_user.id,
                    "email": db_user.email,
                    "first_name": db_user.first_name,
                    "last_name": db_user.last_name,
                    "role": db_user.role,
                    "created_at": db_user.created_at.isoformat() if db_user.created_at else None,
                    "updated_at": db_user.updated_at.isoformat() if db_user.updated_at else None
                }
        except Exception as e:
            logger.error(f"Error getting user by email: {str(e)}")
            raise

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        try:
            with self.get_session() as session:
                db_user = session.query(DBUser).filter(DBUser.id == user_id).first()

                if not db_user:
                    return None

                return {
                    "id": db_user.id,
                    "email": db_user.email,
                    "first_name": db_user.first_name,
                    "last_name": db_user.last_name,
                    "role": db_user.role,
                    "created_at": db_user.created_at.isoformat() if db_user.created_at else None,
                    "updated_at": db_user.updated_at.isoformat() if db_user.updated_at else None
                }
        except Exception as e:
            logger.error(f"Error getting user by ID: {str(e)}")
            raise

    def create_lesson(self, lesson_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new lesson"""
        try:
            with self.get_session() as session:
                # Check if lesson with same slug already exists
                existing_lesson = session.query(DBLesson).filter(DBLesson.slug == lesson_data["slug"]).first()
                if existing_lesson:
                    raise ValueError(f"Lesson with slug {lesson_data['slug']} already exists")

                # Create new lesson
                db_lesson = DBLesson(**lesson_data)
                session.add(db_lesson)

                # Flush to get the ID
                session.flush()

                # Return lesson data
                lesson_dict = {
                    "id": db_lesson.id,
                    "title": db_lesson.title,
                    "description": db_lesson.description,
                    "content": db_lesson.content,
                    "difficulty": db_lesson.difficulty,
                    "category": db_lesson.category,
                    "estimated_duration": db_lesson.estimated_duration,
                    "slug": db_lesson.slug,
                    "created_at": db_lesson.created_at.isoformat() if db_lesson.created_at else None
                }

                return lesson_dict
        except Exception as e:
            logger.error(f"Error creating lesson: {str(e)}")
            raise

    def get_lesson_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        """Get lesson by slug"""
        try:
            with self.get_session() as session:
                db_lesson = session.query(DBLesson).filter(DBLesson.slug == slug).first()

                if not db_lesson:
                    return None

                return {
                    "id": db_lesson.id,
                    "title": db_lesson.title,
                    "description": db_lesson.description,
                    "content": db_lesson.content,
                    "difficulty": db_lesson.difficulty,
                    "category": db_lesson.category,
                    "estimated_duration": db_lesson.estimated_duration,
                    "slug": db_lesson.slug,
                    "created_at": db_lesson.created_at.isoformat() if db_lesson.created_at else None,
                    "updated_at": db_lesson.updated_at.isoformat() if db_lesson.updated_at else None
                }
        except Exception as e:
            logger.error(f"Error getting lesson by slug: {str(e)}")
            raise

    def get_all_lessons(self) -> List[Dict[str, Any]]:
        """Get all lessons"""
        try:
            with self.get_session() as session:
                db_lessons = session.query(DBLesson).all()

                lessons = []
                for db_lesson in db_lessons:
                    lessons.append({
                        "id": db_lesson.id,
                        "title": db_lesson.title,
                        "description": db_lesson.description,
                        "difficulty": db_lesson.difficulty,
                        "category": db_lesson.category,
                        "estimated_duration": db_lesson.estimated_duration,
                        "slug": db_lesson.slug,
                        "created_at": db_lesson.created_at.isoformat() if db_lesson.created_at else None
                    })

                return lessons
        except Exception as e:
            logger.error(f"Error getting all lessons: {str(e)}")
            raise

    def create_progress(self, progress_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new progress record"""
        try:
            with self.get_session() as session:
                # Create new progress record
                db_progress = DBProgress(**progress_data)
                session.add(db_progress)

                # Flush to get the ID
                session.flush()

                # Return progress data
                progress_dict = {
                    "id": db_progress.id,
                    "user_id": db_progress.user_id,
                    "lesson_id": db_progress.lesson_id,
                    "status": db_progress.status,
                    "score": db_progress.score,
                    "time_spent": db_progress.time_spent,
                    "attempts": db_progress.attempts,
                    "metadata": db_progress.metadata,
                    "created_at": db_progress.created_at.isoformat() if db_progress.created_at else None
                }

                return progress_dict
        except Exception as e:
            logger.error(f"Error creating progress: {str(e)}")
            raise

    def get_user_progress(self, user_id: str) -> List[Dict[str, Any]]:
        """Get progress records for a user"""
        try:
            with self.get_session() as session:
                db_progress_records = session.query(DBProgress).filter(DBProgress.user_id == user_id).all()

                progress_list = []
                for db_progress in db_progress_records:
                    progress_list.append({
                        "id": db_progress.id,
                        "user_id": db_progress.user_id,
                        "lesson_id": db_progress.lesson_id,
                        "status": db_progress.status,
                        "score": db_progress.score,
                        "time_spent": db_progress.time_spent,
                        "attempts": db_progress.attempts,
                        "metadata": db_progress.metadata,
                        "created_at": db_progress.created_at.isoformat() if db_progress.created_at else None,
                        "updated_at": db_progress.updated_at.isoformat() if db_progress.updated_at else None
                    })

                return progress_list
        except Exception as e:
            logger.error(f"Error getting user progress: {str(e)}")
            raise

    def update_progress(self, user_id: str, lesson_id: str, progress_updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update progress for a user and lesson"""
        try:
            with self.get_session() as session:
                # Find existing progress record
                db_progress = session.query(DBProgress).filter(
                    DBProgress.user_id == user_id,
                    DBProgress.lesson_id == lesson_id
                ).first()

                if not db_progress:
                    # Create new progress record if it doesn't exist
                    new_progress_data = {
                        "user_id": user_id,
                        "lesson_id": lesson_id,
                        **progress_updates
                    }
                    return self.create_progress(new_progress_data)

                # Update existing progress record
                for key, value in progress_updates.items():
                    setattr(db_progress, key, value)

                # Return updated progress data
                return {
                    "id": db_progress.id,
                    "user_id": db_progress.user_id,
                    "lesson_id": db_progress.lesson_id,
                    "status": db_progress.status,
                    "score": db_progress.score,
                    "time_spent": db_progress.time_spent,
                    "attempts": db_progress.attempts,
                    "metadata": db_progress.metadata,
                    "created_at": db_progress.created_at.isoformat() if db_progress.created_at else None,
                    "updated_at": db_progress.updated_at.isoformat() if db_progress.updated_at else None
                }
        except Exception as e:
            logger.error(f"Error updating progress: {str(e)}")
            raise

    def health_check(self) -> bool:
        """Check if database connection is healthy"""
        try:
            with self.get_session() as session:
                # Execute a simple query
                result = session.execute(text("SELECT 1"))
                return result.fetchone()[0] == 1
        except Exception as e:
            logger.error(f"Database health check failed: {str(e)}")
            return False


# Global database service instance
db_service = DatabaseService()


def init_db_service(database_url: str = None):
    """
    Initialize the database service

    Args:
        database_url: Database connection URL
    """
    global db_service
    db_service = DatabaseService(database_url)

    # Initialize database tables
    db_service.init_database()

    logger.info("Database service initialized")


def get_db_service() -> DatabaseService:
    """
    Get the database service instance

    Returns:
        DatabaseService instance
    """
    return db_service