#!/usr/bin/env python3
"""
Database Table Creation Script
Run this to create all database tables for RSP Education Agent V2
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.database import create_tables
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def main():
    """Create all database tables"""
    try:
        print("Creating RSP Education database tables...")
        await create_tables()
        print("SUCCESS: Database tables created successfully!")
        print("INFO: You can now register users and use authentication!")
        
    except Exception as e:
        print(f"ERROR: Error creating database tables: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)