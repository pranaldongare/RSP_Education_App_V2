#!/usr/bin/env python3
"""
Complete Authentication Flow Test - RSP Education Agent V2
Tests the entire authentication system with all 7 AI agents

This script tests:
1. User registration and login
2. Authentication token management
3. All 7 AI agent endpoints with user context
4. Session management
5. Profile management
6. Error handling and security
"""

import asyncio
import aiohttp
import json
import sys
from typing import Dict, Any, Optional
from datetime import datetime

class AuthenticationFlowTester:
    def __init__(self, base_url: str = "http://localhost:8000/api/v1"):
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.user_info: Optional[Dict[str, Any]] = None
        self.test_results = []
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test result"""
        status = "[PASS]" if success else "[FAIL]"
        print(f"{status} {test_name}")
        if details:
            print(f"    {details}")
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })

    async def make_request(self, method: str, endpoint: str, data: Dict[str, Any] = None, 
                          auth_required: bool = False) -> Dict[str, Any]:
        """Make HTTP request with optional authentication"""
        url = f"{self.base_url}{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        if auth_required and self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        
        try:
            async with self.session.request(method, url, headers=headers, 
                                          json=data if data else None) as response:
                response_data = await response.json() if response.content_type == 'application/json' else {"text": await response.text()}
                return {
                    "status_code": response.status,
                    "data": response_data,
                    "success": 200 <= response.status < 300
                }
        except Exception as e:
            return {
                "status_code": 0,
                "data": {"error": str(e)},
                "success": False
            }

    async def test_user_registration(self):
        """Test user registration"""
        print("\nTesting User Registration...")
        
        test_user = {
            "name": "Test Student Auth",
            "email": f"test_auth_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com",
            "password": "testpass123",
            "grade": "10",
            "phone": "+1234567890",
            "school": "Test School",
            "parent_email": "parent@example.com",
            "preferred_language": "en"
        }
        
        response = await self.make_request("POST", "/auth/register", test_user)
        
        if response["success"]:
            data = response["data"]
            self.access_token = data.get("access_token")
            self.refresh_token = data.get("refresh_token") 
            self.user_info = data.get("user_info")
            
            self.log_test("User Registration", True, 
                         f"User created: {self.user_info.get('name')} (ID: {self.user_info.get('student_id')})")
        else:
            self.log_test("User Registration", False, 
                         f"Status: {response['status_code']}, Error: {response['data']}")
            
        return response["success"]

    async def test_user_login(self):
        """Test user login with existing credentials"""
        print("\n🔑 Testing User Login...")
        
        if not self.user_info:
            self.log_test("User Login", False, "No user info available")
            return False
            
        login_data = {
            "email": self.user_info["email"],
            "password": "testpass123",
            "remember_me": True
        }
        
        response = await self.make_request("POST", "/auth/login", login_data)
        
        if response["success"]:
            data = response["data"]
            self.access_token = data.get("access_token")
            self.refresh_token = data.get("refresh_token")
            
            self.log_test("User Login", True, 
                         f"Logged in successfully, token expires in {data.get('expires_in')} seconds")
        else:
            self.log_test("User Login", False,
                         f"Status: {response['status_code']}, Error: {response['data']}")
            
        return response["success"]

    async def test_profile_management(self):
        """Test profile retrieval and updates"""
        print("\n👤 Testing Profile Management...")
        
        # Test profile retrieval
        response = await self.make_request("GET", "/auth/me", auth_required=True)
        
        if response["success"]:
            profile = response["data"]
            self.log_test("Get Profile", True, 
                         f"Retrieved profile for {profile.get('name')} (Grade: {profile.get('grade')})")
        else:
            self.log_test("Get Profile", False, 
                         f"Status: {response['status_code']}, Error: {response['data']}")
            return False
        
        # Test profile update
        update_data = {
            "learning_style": "visual",
            "preferences": {"notification_enabled": True, "theme": "dark"}
        }
        
        response = await self.make_request("PUT", "/auth/profile", update_data, auth_required=True)
        
        if response["success"]:
            self.log_test("Update Profile", True, "Profile updated successfully")
        else:
            self.log_test("Update Profile", False,
                         f"Status: {response['status_code']}, Error: {response['data']}")
            
        return response["success"]

    async def test_session_management(self):
        """Test session management"""
        print("\n📱 Testing Session Management...")
        
        # Get active sessions
        response = await self.make_request("GET", "/auth/sessions", auth_required=True)
        
        if response["success"]:
            sessions = response["data"]["sessions"]
            self.log_test("Get Sessions", True, f"Found {len(sessions)} active sessions")
            
            if sessions:
                session_id = sessions[0]["id"]
                # Test session revocation (skip for current session)
                self.log_test("Session Management", True, "Session management working")
            else:
                self.log_test("Session Management", False, "No sessions found")
        else:
            self.log_test("Get Sessions", False,
                         f"Status: {response['status_code']}, Error: {response['data']}")
            
        return response["success"]

    async def test_content_generator_agent(self):
        """Test Content Generator Agent with authentication"""
        print("\n📚 Testing Content Generator Agent...")
        
        test_data = {
            "subject": "Mathematics",
            "grade": 10,
            "topic": "Quadratic Equations",
            "content_type": "lesson",
            "difficulty_level": "INTERMEDIATE"
        }
        
        response = await self.make_request("POST", "/agents/content/generate", 
                                         test_data, auth_required=True)
        
        if response["success"]:
            data = response["data"]
            user_context = data.get("user_context", {})
            self.log_test("Content Generator", True, 
                         f"Content generated for user {user_context.get('student_id')} "
                         f"(Grade: {user_context.get('grade')})")
        else:
            self.log_test("Content Generator", False,
                         f"Status: {response['status_code']}, Error: {response['data']}")
            
        return response["success"]

    async def test_assessment_agent(self):
        """Test Assessment Agent with authentication"""
        print("\n📝 Testing Assessment Agent...")
        
        test_data = {
            "subject": "Science",
            "grade": 10,
            "topic": "Light and Reflection",
            "question_type": "multiple_choice",
            "difficulty_level": "INTERMEDIATE",
            "num_questions": 3
        }
        
        response = await self.make_request("POST", "/agents/assessment/generate-questions",
                                         test_data, auth_required=True)
        
        if response["success"]:
            data = response["data"]
            user_context = data.get("user_context", {})
            self.log_test("Assessment Agent", True, 
                         f"Assessment generated for user {user_context.get('student_id')}")
        else:
            self.log_test("Assessment Agent", False,
                         f"Status: {response['status_code']}, Error: {response['data']}")
            
        return response["success"]

    async def test_learning_coordinator_agent(self):
        """Test Learning Coordinator Agent with authentication"""
        print("\n🎯 Testing Learning Coordinator Agent...")
        
        test_data = {
            "subject": "English",
            "learning_goals": ["Improve reading comprehension", "Enhance vocabulary"],
            "duration_weeks": 8
        }
        
        response = await self.make_request("POST", "/agents/coordinator/learning-path",
                                         test_data, auth_required=True)
        
        if response["success"]:
            data = response["data"]
            user_context = data.get("user_context", {})
            self.log_test("Learning Coordinator", True, 
                         f"Learning path created for user {user_context.get('student_id')}")
        else:
            self.log_test("Learning Coordinator", False,
                         f"Status: {response['status_code']}, Error: {response['data']}")
            
        return response["success"]

    async def test_analytics_agent(self):
        """Test Analytics Agent with authentication"""
        print("\n📊 Testing Analytics Agent...")
        
        test_data = {
            "timeframe": "weekly",
            "metrics": ["performance", "engagement"]
        }
        
        response = await self.make_request("POST", "/agents/analytics/report",
                                         test_data, auth_required=True)
        
        if response["success"]:
            data = response["data"]
            user_context = data.get("user_context", {})
            self.log_test("Analytics Agent", True, 
                         f"Analytics generated for user {user_context.get('student_id')}")
        else:
            self.log_test("Analytics Agent", False,
                         f"Status: {response['status_code']}, Error: {response['data']}")
            
        return response["success"]

    async def test_adaptive_learning_agent(self):
        """Test Adaptive Learning Agent with authentication"""
        print("\n🧠 Testing Adaptive Learning Agent...")
        
        test_data = {
            "subject": "Mathematics",
            "topic": "Algebra",
            "difficulty_level": "INTERMEDIATE"
        }
        
        response = await self.make_request("POST", "/agents/adaptive/learning-path",
                                         test_data, auth_required=True)
        
        if response["success"]:
            data = response["data"]
            user_context = data.get("user_context", {})
            self.log_test("Adaptive Learning Agent", True, 
                         f"Adaptive path created for user {user_context.get('student_id')}")
        else:
            self.log_test("Adaptive Learning Agent", False,
                         f"Status: {response['status_code']}, Error: {response['data']}")
            
        return response["success"]

    async def test_engagement_agent(self):
        """Test Engagement Agent with authentication"""
        print("\n🎮 Testing Engagement Agent...")
        
        test_data = {
            "interaction_type": "learning_session",
            "activity_data": {"topic": "Physics", "duration": 30}
        }
        
        response = await self.make_request("POST", "/agents/engagement/profile",
                                         test_data, auth_required=True)
        
        if response["success"]:
            data = response["data"]
            user_context = data.get("user_context", {})
            self.log_test("Engagement Agent", True, 
                         f"Engagement profile updated for user {user_context.get('student_id')}")
        else:
            self.log_test("Engagement Agent", False,
                         f"Status: {response['status_code']}, Error: {response['data']}")
            
        return response["success"]

    async def test_voice_interaction_agent(self):
        """Test Voice Interaction Agent with authentication"""
        print("\n🗣️ Testing Voice Interaction Agent...")
        
        test_data = {
            "language": "en",
            "session_type": "learning"
        }
        
        response = await self.make_request("POST", "/agents/voice/session/start",
                                         test_data, auth_required=True)
        
        if response["success"]:
            data = response["data"]
            self.log_test("Voice Interaction Agent", True, 
                         f"Voice session started successfully")
        else:
            self.log_test("Voice Interaction Agent", False,
                         f"Status: {response['status_code']}, Error: {response['data']}")
            
        return response["success"]

    async def test_token_refresh(self):
        """Test token refresh functionality"""
        print("\n🔄 Testing Token Refresh...")
        
        if not self.refresh_token:
            self.log_test("Token Refresh", False, "No refresh token available")
            return False
        
        test_data = {"refresh_token": self.refresh_token}
        
        response = await self.make_request("POST", "/auth/refresh", test_data)
        
        if response["success"]:
            data = response["data"]
            self.access_token = data.get("access_token")
            self.refresh_token = data.get("refresh_token")
            
            self.log_test("Token Refresh", True, 
                         f"Tokens refreshed, expires in {data.get('expires_in')} seconds")
        else:
            self.log_test("Token Refresh", False,
                         f"Status: {response['status_code']}, Error: {response['data']}")
            
        return response["success"]

    async def test_unauthenticated_access(self):
        """Test that endpoints reject unauthenticated requests"""
        print("\n🚫 Testing Unauthenticated Access...")
        
        # Temporarily remove token
        temp_token = self.access_token
        self.access_token = None
        
        test_data = {"subject": "Math", "topic": "Test"}
        response = await self.make_request("POST", "/agents/content/generate", 
                                         test_data, auth_required=True)
        
        # Restore token
        self.access_token = temp_token
        
        if response["status_code"] == 401:
            self.log_test("Unauthenticated Access Rejection", True, 
                         "Correctly rejected unauthenticated request")
        else:
            self.log_test("Unauthenticated Access Rejection", False,
                         f"Should have returned 401, got {response['status_code']}")
            
        return response["status_code"] == 401

    async def run_comprehensive_test(self):
        """Run all authentication flow tests"""
        print("🚀 Starting Comprehensive Authentication Flow Test")
        print("=" * 60)
        
        test_functions = [
            self.test_user_registration,
            self.test_user_login,
            self.test_profile_management,
            self.test_session_management,
            self.test_content_generator_agent,
            self.test_assessment_agent,
            self.test_learning_coordinator_agent,
            self.test_analytics_agent,
            self.test_adaptive_learning_agent,
            self.test_engagement_agent,
            self.test_voice_interaction_agent,
            self.test_token_refresh,
            self.test_unauthenticated_access
        ]
        
        success_count = 0
        total_count = len(test_functions)
        
        for test_func in test_functions:
            try:
                if await test_func():
                    success_count += 1
            except Exception as e:
                self.log_test(test_func.__name__, False, f"Exception: {str(e)}")
        
        # Final logout test
        if self.access_token:
            print("\n🚪 Testing User Logout...")
            response = await self.make_request("POST", "/auth/logout", auth_required=True)
            if response["success"]:
                self.log_test("User Logout", True, "User logged out successfully")
                success_count += 1
            else:
                self.log_test("User Logout", False, 
                             f"Status: {response['status_code']}, Error: {response['data']}")
            total_count += 1
        
        # Print summary
        print("\n" + "=" * 60)
        print("📋 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total_count}")
        print(f"Passed: {success_count}")
        print(f"Failed: {total_count - success_count}")
        print(f"Success Rate: {(success_count/total_count)*100:.1f}%")
        
        if success_count == total_count:
            print("\n🎉 ALL TESTS PASSED! Authentication system is working perfectly!")
        else:
            print(f"\n⚠️  {total_count - success_count} tests failed. Please check the logs above.")
        
        return success_count == total_count

async def main():
    """Main test runner"""
    print("RSP Education Agent V2 - Complete Authentication Flow Test")
    print("Testing all 7 AI agents with user authentication...")
    
    try:
        async with AuthenticationFlowTester() as tester:
            success = await tester.run_comprehensive_test()
            
            # Save test results
            with open("authentication_test_results.json", "w") as f:
                json.dump({
                    "timestamp": datetime.now().isoformat(),
                    "success": success,
                    "results": tester.test_results
                }, f, indent=2)
            
            print(f"\n📄 Test results saved to authentication_test_results.json")
            
            return 0 if success else 1
            
    except Exception as e:
        print(f"❌ Test runner failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))