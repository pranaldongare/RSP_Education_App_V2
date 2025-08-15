#!/usr/bin/env python3
"""
Test async database operations directly
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.database import get_db_session, engine
from database.models import Student
from sqlalchemy import select
import logging

logging.basicConfig(level=logging.INFO)

async def test_async_db():
    """Test basic async database operations"""
    try:
        print("Testing async database connection...")
        
        # Test database connection
        async with engine.begin() as conn:
            result = await conn.execute(select(1))
            print(f"Database connection test: {result.scalar()}")
        
        # Test async session
        async for db in get_db_session():
            print("Got async database session")
            
            # Test simple query
            stmt = select(Student).limit(1)
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()
            print(f"Found user: {user.name if user else 'No users found'}")
            
            # Test insert
            new_student = Student(
                id="TEST123",
                name="Test User",
                email="test_async@example.com",
                password_hash="test_hash",
                grade="5"
            )
            
            db.add(new_student)
            await db.commit()
            print("Successfully created test user with async operations!")
            
            # Cleanup
            await db.delete(new_student)
            await db.commit()
            print("Cleaned up test user")
            
            break
        
        print("All async operations completed successfully!")
        
    except Exception as e:
        print(f"Error in async database test: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(test_async_db())
    sys.exit(exit_code)