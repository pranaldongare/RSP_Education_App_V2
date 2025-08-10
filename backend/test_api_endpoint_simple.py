#!/usr/bin/env python3
"""
API Endpoint vs Direct Agent Functionality Test (Simplified)
Tests both API endpoint and direct agent calls to compare functionality
"""

import asyncio
import json
import sys
import time
import httpx
sys.path.append('.')

from agents.content_generator import ContentGeneratorAgent, ContentRequest

class APIEndpointTester:
    def __init__(self):
        self.agent = ContentGeneratorAgent()
        self.base_url = "http://127.0.0.1:8000"  # Backend API base URL
        self.access_token = None
        
    async def authenticate(self):
        """Authenticate and get access token"""
        print("Authenticating with backend API...")
        
        # Register test user if needed
        register_data = {
            "name": "Content Test User",
            "email": "contenttest@example.com",
            "password": "testpass123",
            "student_id": "CT001",
            "grade": 8,
            "phone": "1234567890",
            "school": "Test School",
            "parent_email": "parent@example.com",
            "preferred_language": "English",
            "learning_style": "Visual"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                register_response = await client.post(f"{self.base_url}/api/v1/auth/register", json=register_data)
            if register_response.status_code == 201:
                print("SUCCESS: Test user registered successfully")
            elif register_response.status_code == 400:
                print("INFO: Test user already exists, proceeding to login")
        except Exception as e:
            print(f"WARNING: Registration failed or user exists: {e}")
        
        # Login to get token
        login_data = {
            "email": "contenttest@example.com",
            "password": "testpass123"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                login_response = await client.post(f"{self.base_url}/api/v1/auth/login", json=login_data)
            if login_response.status_code == 200:
                login_result = login_response.json()
                self.access_token = login_result.get("access_token")
                print("SUCCESS: Authentication successful")
                return True
            else:
                print(f"FAILED: Login failed with status: {login_response.status_code}")
                return False
        except Exception as e:
            print(f"ERROR: Login error: {e}")
            return False
    
    async def test_direct_agent_call(self, test_request):
        """Test direct agent call"""
        print("Testing Direct Agent Call...")
        start_time = time.time()
        
        try:
            request = ContentRequest(**test_request)
            result = await self.agent.generate_content(request)
            end_time = time.time()
            
            return {
                'success': True,
                'response_time': end_time - start_time,
                'content_length': len(result.content),
                'content_preview': result.content[:200] + "...",
                'learning_objectives_count': len(result.learning_objectives),
                'estimated_time': result.estimated_time,
                'prerequisites_count': len(result.prerequisites),
                'result_type': 'GeneratedContent object'
            }
        except Exception as e:
            end_time = time.time()
            return {
                'success': False,
                'error': str(e),
                'response_time': end_time - start_time
            }
    
    async def test_api_endpoint_call(self, test_request):
        """Test API endpoint call"""
        print("Testing API Endpoint Call...")
        start_time = time.time()
        
        if not self.access_token:
            return {
                'success': False,
                'error': 'No access token available',
                'response_time': 0
            }
        
        try:
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/v1/agents/content-generator",
                    json=test_request,
                    headers=headers,
                    timeout=30,
                )

            end_time = time.time()

            if response.status_code == 200:
                result_data = response.json()
                content_data = result_data.get('content', {})

                return {
                    'success': True,
                    'response_time': end_time - start_time,
                    'content_length': len(str(content_data.get('content', ''))),
                    'content_preview': str(content_data.get('content', ''))[:200] + "...",
                    'learning_objectives_count': len(content_data.get('learning_objectives', [])),
                    'estimated_time': content_data.get('estimated_time', 0),
                    'prerequisites_count': len(content_data.get('prerequisites', [])),
                    'result_type': 'API JSON response',
                    'status_code': response.status_code,
                }
            else:
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}: {response.text[:200]}",
                    'response_time': end_time - start_time,
                    'status_code': response.status_code,
                }
        except Exception as e:
            end_time = time.time()
            return {
                'success': False,
                'error': str(e),
                'response_time': end_time - start_time,
            }
    
    async def run_comparison_test(self):
        """Run comprehensive comparison between direct agent and API endpoint"""
        print("Starting API Endpoint vs Direct Agent Comparison Test")
        print("=" * 70)
        
        # Authenticate first
        auth_success = await self.authenticate()
        if not auth_success:
            print("ERROR: Authentication failed, cannot test API endpoints")
            return
        
        # Test scenarios
        test_scenarios = [
            {
                'name': 'Mathematics - Grade 5 - Basic Fractions',
                'data': {
                    'topic': 'Adding Fractions with Same Denominator',
                    'subject': 'Mathematics',
                    'grade': 5,
                    'content_type': 'explanation',
                    'difficulty': 'beginner'
                }
            },
            {
                'name': 'Science - Grade 7 - Physics',
                'data': {
                    'topic': 'Simple Machines',
                    'subject': 'Science',
                    'grade': 7,
                    'content_type': 'example',
                    'difficulty': 'intermediate'
                }
            }
        ]
        
        comparison_results = []
        
        for scenario in test_scenarios:
            print(f"\n" + "="*50)
            print(f"Testing Scenario: {scenario['name']}")
            print(f"Request Data: {json.dumps(scenario['data'], indent=2)}")
            
            # Test direct agent call
            direct_result = await self.test_direct_agent_call(scenario['data'])
            
            # Test API endpoint call
            api_result = await self.test_api_endpoint_call(scenario['data'])
            
            # Compare results
            comparison = {
                'scenario': scenario['name'],
                'direct_agent': direct_result,
                'api_endpoint': api_result,
            }
            
            comparison_results.append(comparison)
            
            # Print immediate results
            print(f"\nComparison Results:")
            print(f"Direct Agent: {'SUCCESS' if direct_result['success'] else 'FAILED'} - {direct_result.get('response_time', 0):.2f}s")
            print(f"API Endpoint: {'SUCCESS' if api_result['success'] else 'FAILED'} - {api_result.get('response_time', 0):.2f}s")
            
            if direct_result['success'] and api_result['success']:
                length_diff = abs(direct_result['content_length'] - api_result['content_length'])
                objectives_match = direct_result['learning_objectives_count'] == api_result['learning_objectives_count']
                
                print(f"Content Length Match: {'YES' if length_diff < 100 else 'NO'} (diff: {length_diff})")
                print(f"Learning Objectives Match: {'YES' if objectives_match else 'NO'}")
                print(f"Direct Content Preview: {direct_result['content_preview'][:100]}...")
                print(f"API Content Preview: {api_result['content_preview'][:100]}...")
            else:
                if not direct_result['success']:
                    print(f"Direct Agent Error: {direct_result.get('error', 'Unknown')}")
                if not api_result['success']:
                    print(f"API Endpoint Error: {api_result.get('error', 'Unknown')}")
        
        # Generate final comparison report
        await self.generate_comparison_report(comparison_results)
    
    async def generate_comparison_report(self, results):
        """Generate comprehensive comparison report"""
        print("\n" + "=" * 70)
        print("COMPREHENSIVE API ENDPOINT vs DIRECT AGENT COMPARISON REPORT")
        print("=" * 70)
        
        total_tests = len(results)
        direct_successes = sum(1 for r in results if r['direct_agent']['success'])
        api_successes = sum(1 for r in results if r['api_endpoint']['success'])
        
        print(f"\nOverall Results:")
        print(f"   Total Test Scenarios: {total_tests}")
        print(f"   Direct Agent Successes: {direct_successes}/{total_tests} ({(direct_successes/total_tests)*100:.1f}%)")
        print(f"   API Endpoint Successes: {api_successes}/{total_tests} ({(api_successes/total_tests)*100:.1f}%)")
        
        successful_comparisons = [r for r in results if r['direct_agent']['success'] and r['api_endpoint']['success']]
        
        if successful_comparisons:
            avg_direct_time = sum(r['direct_agent']['response_time'] for r in successful_comparisons) / len(successful_comparisons)
            avg_api_time = sum(r['api_endpoint']['response_time'] for r in successful_comparisons) / len(successful_comparisons)
            
            print(f"\nPerformance Comparison (Successful Tests):")
            print(f"   Average Direct Agent Response Time: {avg_direct_time:.2f} seconds")
            print(f"   Average API Endpoint Response Time: {avg_api_time:.2f} seconds")
            print(f"   API Overhead: {(avg_api_time - avg_direct_time):.2f} seconds")
        
        print(f"\nDetailed Test Results:")
        for i, result in enumerate(results, 1):
            direct = result['direct_agent']
            api = result['api_endpoint']
            
            print(f"\n   {i}. {result['scenario']}")
            print(f"      Direct Agent: {'SUCCESS' if direct['success'] else 'FAILED'}")
            if direct['success']:
                print(f"        - Content Length: {direct['content_length']} chars")
                print(f"        - Response Time: {direct['response_time']:.2f}s")
                print(f"        - Learning Objectives: {direct['learning_objectives_count']}")
            else:
                print(f"        - Error: {direct.get('error', 'Unknown')}")
            
            print(f"      API Endpoint: {'SUCCESS' if api['success'] else 'FAILED'}")
            if api['success']:
                print(f"        - Content Length: {api['content_length']} chars")
                print(f"        - Response Time: {api['response_time']:.2f}s")
                print(f"        - Learning Objectives: {api['learning_objectives_count']}")
                print(f"        - Status Code: {api.get('status_code', 'N/A')}")
            else:
                print(f"        - Error: {api.get('error', 'Unknown')}")
        
        print(f"\nSUMMARY:")
        if direct_successes == total_tests and api_successes == total_tests:
            print("   EXCELLENT: Both direct agent and API endpoint work perfectly")
        elif direct_successes == total_tests or api_successes == total_tests:
            print("   GOOD: One method works perfectly, issues with the other")
        else:
            print("   NEEDS ATTENTION: Issues with both methods")
        
        print("=" * 70)

async def main():
    """Main test execution"""
    tester = APIEndpointTester()
    await tester.run_comparison_test()

if __name__ == "__main__":
    asyncio.run(main())