"""
Database Configuration - RSP Education Agent V2
Phase 6: Production Database Setup

SQLAlchemy database configuration with connection pooling,
migration support, and production optimizations.
"""
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
from typing import Generator
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
class DatabaseConfig:
    """Database configuration settings"""
    
    # Database URL (supports SQLite, PostgreSQL, MySQL)
    DATABASE_URL = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./rsp_education_fresh.db"
    )
    
    # Connection pool settings
    POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "5"))
    MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "10"))
    POOL_TIMEOUT = int(os.getenv("DB_POOL_TIMEOUT", "30"))
    POOL_RECYCLE = int(os.getenv("DB_POOL_RECYCLE", "3600"))
    
    # Query settings
    ECHO_QUERIES = os.getenv("DB_ECHO", "false").lower() == "true"
    
    @classmethod
    def get_engine_kwargs(cls):
        """Get engine configuration kwargs"""
        kwargs = {
            "echo": cls.ECHO_QUERIES,
        }
        
        # Add connection pooling for non-SQLite databases
        if not cls.DATABASE_URL.startswith("sqlite"):
            kwargs.update({
                "poolclass": QueuePool,
                "pool_size": cls.POOL_SIZE,
                "max_overflow": cls.MAX_OVERFLOW,
                "pool_timeout": cls.POOL_TIMEOUT,
                "pool_recycle": cls.POOL_RECYCLE,
                "pool_pre_ping": True,  # Verify connections before use
            })
        
        return kwargs

# Create database engine
engine = create_engine(
    DatabaseConfig.DATABASE_URL,
    **DatabaseConfig.get_engine_kwargs()
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()

class DatabaseManager:
    """Database management utilities"""
    
    def __init__(self):
        self.engine = engine
        self.SessionLocal = SessionLocal
    
    def create_tables(self):
        """Create all database tables"""
        try:
            from .models import Base
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create database tables: {e}")
            raise
    
    def drop_tables(self):
        """Drop all database tables (use with caution!)"""
        try:
            from .models import Base
            Base.metadata.drop_all(bind=self.engine)
            logger.info("Database tables dropped successfully")
        except Exception as e:
            logger.error(f"Failed to drop database tables: {e}")
            raise
    
    def get_table_info(self):
        """Get information about database tables"""
        metadata = MetaData()
        metadata.reflect(bind=self.engine)
        
        table_info = {}
        for table_name, table in metadata.tables.items():
            table_info[table_name] = {
                "columns": [col.name for col in table.columns],
                "indexes": [idx.name for idx in table.indexes],
                "foreign_keys": [fk.column.name for fk in table.foreign_keys]
            }
        
        return table_info
    
    @contextmanager
    def get_db_session(self) -> Generator[Session, None, None]:
        """Get database session with automatic cleanup"""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()
    
    def health_check(self) -> bool:
        """Check database connectivity"""
        try:
            with self.get_db_session() as session:
                session.execute("SELECT 1")
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False

# Global database manager instance
db_manager = DatabaseManager()

# Dependency for FastAPI
def get_database_session() -> Generator[Session, None, None]:
    """Dependency function for FastAPI to get database session"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

# Alias for compatibility
get_db = get_database_session

# Database initialization functions
def init_database():
    """Initialize database with tables and initial data"""
    logger.info("Initializing database...")
    
    # Create tables
    db_manager.create_tables()
    
    # Add initial data if needed
    _create_initial_data()
    
    logger.info("Database initialization completed")

def _create_initial_data():
    """Create initial data for the database"""
    from .models import SystemMetrics
    
    with db_manager.get_db_session() as session:
        # Check if initial data already exists
        existing_metrics = session.query(SystemMetrics).first()
        if existing_metrics:
            logger.info("Initial data already exists, skipping creation")
            return
        
        # Create initial system metrics
        initial_metrics = [
            SystemMetrics(
                metric_name="system_initialization",
                metric_value=1.0,
                component="database",
                metric_data={"status": "initialized", "version": "1.0"}
            )
        ]
        
        for metric in initial_metrics:
            session.add(metric)
        
        logger.info("Initial data created successfully")

# Migration utilities
class MigrationManager:
    """Database migration management"""
    
    def __init__(self):
        self.engine = engine
    
    def backup_database(self, backup_path: str = None):
        """Create database backup (SQLite only)"""
        if not DatabaseConfig.DATABASE_URL.startswith("sqlite"):
            logger.warning("Backup is only supported for SQLite databases")
            return False
        
        try:
            import shutil
            db_path = DatabaseConfig.DATABASE_URL.replace("sqlite:///", "")
            backup_path = backup_path or f"{db_path}.backup"
            shutil.copy2(db_path, backup_path)
            logger.info(f"Database backed up to: {backup_path}")
            return True
        except Exception as e:
            logger.error(f"Database backup failed: {e}")
            return False
    
    def get_schema_version(self) -> str:
        """Get current database schema version"""
        try:
            with db_manager.get_db_session() as session:
                result = session.execute(
                    "SELECT metric_data FROM system_metrics WHERE metric_name = 'schema_version' ORDER BY recorded_at DESC LIMIT 1"
                ).fetchone()
                
                if result and result[0]:
                    return result[0].get("version", "1.0")
                return "1.0"
        except Exception:
            return "1.0"
    
    def update_schema_version(self, version: str):
        """Update schema version"""
        from .models import SystemMetrics
        
        with db_manager.get_db_session() as session:
            version_metric = SystemMetrics(
                metric_name="schema_version",
                metric_value=float(version) if version.replace(".", "").isdigit() else 1.0,
                component="database",
                metric_data={"version": version, "updated_by": "migration"}
            )
            session.add(version_metric)

# Global migration manager
migration_manager = MigrationManager()

# Export commonly used items
__all__ = [
    "engine",
    "SessionLocal", 
    "Base",
    "DatabaseManager",
    "db_manager",
    "get_database_session",
    "get_db",
    "init_database",
    "migration_manager"
]