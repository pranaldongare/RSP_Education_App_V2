#!/usr/bin/env python3
"""
Test FastAPI startup without full initialization
"""

import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_imports():
    """Test if we can import all required modules"""
    print("=" * 50)
    print("Testing FastAPI Import Dependencies")
    print("=" * 50)
    
    try:
        print("Testing FastAPI imports...")
        import uvicorn
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        print("[PASS] FastAPI imports successful")
        
        print("Testing Pydantic settings...")
        from pydantic_settings import BaseSettings
        print("[PASS] Pydantic settings import successful")
        
        print("Testing config imports...")
        from config.settings import settings
        print("[PASS] Settings import successful")
        print(f"  App name: {settings.app_name}")
        print(f"  Debug mode: {settings.debug}")
        print(f"  Server: {settings.server_host}:{settings.server_port}")
        
        print("Testing core imports...")
        from core.exceptions import AppException
        print("[PASS] Core exceptions import successful")
        
        print("Testing logging setup...")
        from core.logging import setup_logging
        print("[PASS] Logging setup import successful")
        
        print("Testing database imports...")
        from config.database import create_tables
        print("[PASS] Database imports successful")
        
        print("Testing API router imports...")
        from api.v1.router import api_router
        print("[PASS] API router import successful")
        
        print("Testing agent imports...")
        from agents.coordinator import AgentCoordinator
        from agents.content_generator import ContentGeneratorAgent
        print("[PASS] Agent imports successful")
        
        return True
        
    except ImportError as e:
        print(f"[FAIL] Import error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_basic_app_creation():
    """Test creating a basic FastAPI app"""
    print("\n" + "=" * 50)
    print("Testing FastAPI App Creation")
    print("=" * 50)
    
    try:
        from fastapi import FastAPI
        from config.settings import settings
        
        # Create basic app without lifespan
        app = FastAPI(
            title="RSP Education Agent API - Test",
            description="Test instance",
            version="2.0.0-test",
            docs_url="/docs",
        )
        
        print("[PASS] FastAPI app created successfully")
        print(f"  Title: {app.title}")
        print(f"  Version: {app.version}")
        
        # Test basic route
        @app.get("/test")
        async def test_endpoint():
            return {"status": "test_ok", "message": "FastAPI is working"}
        
        print("[PASS] Test route added successfully")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] App creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_agent_coordinator():
    """Test agent coordinator initialization"""
    print("\n" + "=" * 50)
    print("Testing Agent Coordinator")
    print("=" * 50)
    
    try:
        from agents.coordinator import AgentCoordinator
        
        coordinator = AgentCoordinator()
        print("[PASS] Agent coordinator created")
        
        # Test initialization
        await coordinator.initialize()
        print("[PASS] Agent coordinator initialized")
        
        # Test status
        status = await coordinator.get_status()
        print("[PASS] Agent coordinator status retrieved")
        print(f"  Status: {status['status']}")
        print(f"  Total agents: {status['total_agents']}")
        
        # Test shutdown
        await coordinator.shutdown()
        print("[PASS] Agent coordinator shut down")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] Agent coordinator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all startup tests"""
    print("RSP Education Agent V2 - FastAPI Startup Test Suite")
    print("=" * 60)
    
    tests = [
        ("Import Dependencies", test_imports),
        ("Basic App Creation", test_basic_app_creation),
        ("Agent Coordinator", test_agent_coordinator)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            print(f"\n[TEST] Running {test_name} test...")
            result = await test_func()
            results[test_name] = result
            if result:
                print(f"[PASS] {test_name} test PASSED")
            else:
                print(f"[FAIL] {test_name} test FAILED")
        except Exception as e:
            print(f"[ERROR] {test_name} test FAILED with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("FASTAPI STARTUP TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "[PASS]" if result else "[FAIL]"
        print(f"{test_name:<20} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("SUCCESS: FastAPI backend is ready to start!")
        print("\nTo start the server, run:")
        print("  python main.py")
        print("  OR")
        print("  uvicorn main:app --reload")
        return 0
    else:
        print("WARNING: Some startup tests failed. Check dependencies.")
        return 1

if __name__ == "__main__":
    import asyncio
    exit_code = asyncio.run(main())
    sys.exit(exit_code)