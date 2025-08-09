"""
Database Configuration and Setup
Handles database connection and table creation
"""

import asyncio
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config.settings import settings


logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models"""
    pass


# Create async engine
try:
    engine = create_async_engine(
        settings.database_url,
        echo=settings.debug,
        future=True
    )
except Exception as e:
    logger.warning(f"Database engine creation failed: {e}. Using fallback configuration.")
    # Fallback for development/testing
    engine = create_async_engine(
        "sqlite+aiosqlite:///./rsp_education.db",
        echo=settings.debug,
        future=True
    )

# Create session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def create_tables():
    """
    Create database tables if they don't exist
    """
    try:
        logger.info("Creating database tables...")
        
        # Import all models to ensure they're registered with metadata
        from database.models import (
            Student, LearningProfile, Content, Assessment, AssessmentResult,
            LearningSession, SessionActivity, VoiceInteraction, SystemMetrics, UserSession
        )
        
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info("Database tables created successfully")
        
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise


async def get_db_session():
    """
    Dependency to get database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()