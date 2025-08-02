#!/usr/bin/env python3
"""
Simple Authentication Flow Test - RSP Education Agent V2
Tests the basic authentication system and agent endpoints
"""

import asyncio
import aiohttp
import json
from datetime import datetime

async def test_auth_flow():
    """Test basic authentication flow"""
    base_url = "http://localhost:8000/api/v1"
    
    async with aiohttp.ClientSession() as session:
        print("Starting Authentication Flow Test")
        print("=" * 50)
        
        # Test 1: Register User
        print("\n1. Testing User Registration...")
        test_user = {
            "name": "Test Student",
            "email": f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com",
            "password": "testpass123",
            "grade": "10",
            "preferred_language": "en"
        }
        
        try:
            async with session.post(f"{base_url}/auth/register", 
                                  headers={"Content-Type": "application/json"},
                                  json=test_user) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    access_token = data.get("access_token")
                    user_info = data.get("user_info")
                    print(f"[PASS] User registered: {user_info.get('name')}")
                else:
                    print(f"[FAIL] Registration failed: {resp.status}")
                    return False
        except Exception as e:
            print(f"[FAIL] Registration error: {e}")
            return False
        
        if not access_token:
            print("[FAIL] No access token received")
            return False
        
        # Test 2: Test authenticated endpoint
        print("\n2. Testing Content Generator Agent...")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        
        content_data = {
            "subject": "Mathematics",
            "grade": 10,
            "topic": "Algebra",
            "content_type": "lesson",
            "difficulty_level": "INTERMEDIATE"
        }
        
        try:
            async with session.post(f"{base_url}/agents/content/generate",
                                  headers=headers,
                                  json=content_data) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    user_context = data.get("user_context", {})
                    print(f"[PASS] Content generated for user {user_context.get('student_id')}")
                else:
                    print(f"[FAIL] Content generation failed: {resp.status}")
                    error_data = await resp.json()
                    print(f"    Error: {error_data}")
        except Exception as e:
            print(f"[FAIL] Content generation error: {e}")
        
        # Test 3: Test Analytics Agent
        print("\n3. Testing Analytics Agent...")
        analytics_data = {
            "timeframe": "weekly",
            "metrics": ["performance"]
        }
        
        try:
            async with session.post(f"{base_url}/agents/analytics/report",
                                  headers=headers,
                                  json=analytics_data) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    print("[PASS] Analytics report generated")
                else:
                    print(f"[FAIL] Analytics failed: {resp.status}")
        except Exception as e:
            print(f"[FAIL] Analytics error: {e}")
        
        # Test 4: Test unauthenticated access
        print("\n4. Testing Unauthenticated Access...")
        try:
            async with session.post(f"{base_url}/agents/content/generate",
                                  headers={"Content-Type": "application/json"},
                                  json=content_data) as resp:
                if resp.status == 401:
                    print("[PASS] Correctly rejected unauthenticated request")
                else:
                    print(f"[FAIL] Should have returned 401, got {resp.status}")
        except Exception as e:
            print(f"[FAIL] Unauthenticated test error: {e}")
        
        print("\n" + "=" * 50)
        print("Basic Authentication Test Complete")
        return True

if __name__ == "__main__":
    asyncio.run(test_auth_flow())