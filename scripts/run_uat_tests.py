#!/usr/bin/env python3
"""
UAT Test Execution Script - RSP Education Agent V2
Automated test runner for User Acceptance Testing

Usage: python run_uat_tests.py [--category all|api|frontend|integration]
"""

import asyncio
import json
import requests
import subprocess
import time
from datetime import datetime
from typing import Dict, List, Any
import argparse
import sys
import os

class UATTestRunner:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.frontend_url = "http://localhost:3000"
        self.results = {
            "test_date": datetime.now().isoformat(),
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "blocked": 0,
            "test_categories": {},
            "issues_found": [],
            "detailed_results": []
        }
    
    def log_test_result(self, test_name: str, category: str, passed: bool, 
                       details: str = "", error_msg: str = ""):
        """Log individual test result"""
        result = {
            "test_name": test_name,
            "category": category,
            "passed": passed,
            "timestamp": datetime.now().isoformat(),
            "details": details,
            "error_message": error_msg
        }
        
        self.results["detailed_results"].append(result)
        self.results["total_tests"] += 1
        
        if passed:
            self.results["passed"] += 1
            print(f"✅ {test_name}: PASSED")
        else:
            self.results["failed"] += 1
            print(f"❌ {test_name}: FAILED - {error_msg}")
            self.results["issues_found"].append({
                "test": test_name,
                "category": category,
                "error": error_msg,
                "details": details
            })
    
    def test_system_health(self) -> None:
        """Test basic system health and connectivity"""
        print("\n🔍 Testing System Health...")
        
        # Test 1.1: Backend Health Check
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                self.log_test_result("Backend Health Check", "infrastructure", True)
            else:
                self.log_test_result("Backend Health Check", "infrastructure", False, 
                                   error_msg=f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test_result("Backend Health Check", "infrastructure", False, 
                               error_msg=str(e))
        
        # Test 1.2: API Root Endpoint
        try:
            response = requests.get(f"{self.base_url}/api/v1/", timeout=5)
            if response.status_code == 200 and "agents" in response.json():
                self.log_test_result("API Root Endpoint", "infrastructure", True)
            else:
                self.log_test_result("API Root Endpoint", "infrastructure", False,
                                   error_msg="Invalid API response")
        except Exception as e:
            self.log_test_result("API Root Endpoint", "infrastructure", False,
                               error_msg=str(e))
        
        # Test 1.3: Frontend Accessibility  
        try:
            response = requests.get(self.frontend_url, timeout=5)
            if response.status_code == 200:
                self.log_test_result("Frontend Accessibility", "infrastructure", True)
            else:
                self.log_test_result("Frontend Accessibility", "infrastructure", False,
                                   error_msg=f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test_result("Frontend Accessibility", "infrastructure", False,
                               error_msg=str(e))
    
    def test_ai_agents(self) -> None:
        """Test all AI agent endpoints"""
        print("\n🤖 Testing AI Agents...")
        
        # Test Content Generator Agent
        try:
            payload = {
                "grade": "5",
                "subject": "Mathematics",
                "topic": "Fractions",
                "content_type": "lesson",
                "difficulty": "medium",
                "learning_objectives": ["Understand basic fractions"]
            }
            response = requests.post(f"{self.base_url}/api/v1/agents/content/generate",
                                   json=payload, timeout=10)
            
            if response.status_code in [200, 202]:
                self.log_test_result("Content Generator Agent", "ai_agents", True)
            else:
                self.log_test_result("Content Generator Agent", "ai_agents", False,
                                   error_msg=f"Status: {response.status_code}")
        except Exception as e:
            self.log_test_result("Content Generator Agent", "ai_agents", False,
                               error_msg=str(e))
        
        # Test Assessment Agent
        try:
            payload = {
                "grade": "5",
                "subject": "Mathematics",
                "topic": "Fractions",
                "difficulty": "medium",
                "question_count": 5,
                "question_types": ["multiple_choice"]
            }
            response = requests.post(f"{self.base_url}/api/v1/agents/assessment/generate",
                                   json=payload, timeout=10)
            
            if response.status_code in [200, 202]:
                self.log_test_result("Assessment Agent", "ai_agents", True)
            else:
                self.log_test_result("Assessment Agent", "ai_agents", False,
                                   error_msg=f"Status: {response.status_code}")
        except Exception as e:
            self.log_test_result("Assessment Agent", "ai_agents", False,
                               error_msg=str(e))
        
        # Test Adaptive Learning Agent
        try:
            payload = {
                "student_id": "uat_test_student",
                "performance_data": {"mathematics": 0.75},
                "completed_topics": ["fractions"],
                "skill_levels": {"problem_solving": 0.7}
            }
            response = requests.post(f"{self.base_url}/api/v1/agents/adaptive/profile/update",
                                   json=payload, timeout=10)
            
            if response.status_code in [200, 202]:
                self.log_test_result("Adaptive Learning Agent", "ai_agents", True)
            else:
                self.log_test_result("Adaptive Learning Agent", "ai_agents", False,
                                   error_msg=f"Status: {response.status_code}")
        except Exception as e:
            self.log_test_result("Adaptive Learning Agent", "ai_agents", False,
                               error_msg=str(e))
        
        # Test Voice Interaction Agent
        try:
            response = requests.get(f"{self.base_url}/api/v1/agents/voice/capabilities",
                                  timeout=5)
            
            if response.status_code in [200, 202]:
                self.log_test_result("Voice Interaction Agent", "ai_agents", True)
            else:
                self.log_test_result("Voice Interaction Agent", "ai_agents", False,
                                   error_msg=f"Status: {response.status_code}")
        except Exception as e:
            self.log_test_result("Voice Interaction Agent", "ai_agents", False,
                               error_msg=str(e))
        
        # Test Learning Coordinator Agent
        try:
            payload = {
                "student_id": "uat_test_student",
                "session_type": "adaptive_learning",
                "preferences": {"subjects": ["Mathematics"]}
            }
            response = requests.post(f"{self.base_url}/api/v1/agents/coordinator/initialize",
                                   json=payload, timeout=10)
            
            if response.status_code in [200, 202]:
                self.log_test_result("Learning Coordinator Agent", "ai_agents", True)
            else:
                self.log_test_result("Learning Coordinator Agent", "ai_agents", False,
                                   error_msg=f"Status: {response.status_code}")
        except Exception as e:
            self.log_test_result("Learning Coordinator Agent", "ai_agents", False,
                               error_msg=str(e))
    
    def test_performance(self) -> None:
        """Test system performance"""
        print("\n⚡ Testing Performance...")
        
        # Test Response Time
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/health", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200 and response_time < 5.0:
                self.log_test_result("Response Time Test", "performance", True,
                                   details=f"Response time: {response_time:.2f}s")
            else:
                self.log_test_result("Response Time Test", "performance", False,
                                   error_msg=f"Slow response: {response_time:.2f}s")
        except Exception as e:
            self.log_test_result("Response Time Test", "performance", False,
                               error_msg=str(e))
        
        # Test Concurrent Requests
        try:
            import concurrent.futures
            import threading
            
            def make_request():
                return requests.get(f"{self.base_url}/health", timeout=5)
            
            start_time = time.time()
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                futures = [executor.submit(make_request) for _ in range(10)]
                results = [future.result() for future in concurrent.futures.as_completed(futures)]
            
            total_time = time.time() - start_time
            success_count = sum(1 for r in results if r.status_code == 200)
            
            if success_count >= 8 and total_time < 10:  # 80% success rate
                self.log_test_result("Concurrent Requests Test", "performance", True,
                                   details=f"Success: {success_count}/10, Time: {total_time:.2f}s")
            else:
                self.log_test_result("Concurrent Requests Test", "performance", False,
                                   error_msg=f"Success: {success_count}/10, Time: {total_time:.2f}s")
        except Exception as e:
            self.log_test_result("Concurrent Requests Test", "performance", False,
                               error_msg=str(e))
    
    def test_error_handling(self) -> None:
        """Test error handling and edge cases"""
        print("\n🚨 Testing Error Handling...")
        
        # Test Invalid Input Handling
        try:
            payload = {
                "grade": "invalid",
                "subject": "",
                "topic": "",
                "content_type": "",
                "difficulty": "",
                "learning_objectives": []
            }
            response = requests.post(f"{self.base_url}/api/v1/agents/content/generate",
                                   json=payload, timeout=5)
            
            if response.status_code in [400, 422]:  # Proper error codes
                self.log_test_result("Invalid Input Handling", "security", True,
                                   details=f"Proper error code: {response.status_code}")
            else:
                self.log_test_result("Invalid Input Handling", "security", False,
                                   error_msg=f"Unexpected status: {response.status_code}")
        except Exception as e:
            self.log_test_result("Invalid Input Handling", "security", False,
                               error_msg=str(e))
        
        # Test Non-existent Endpoint
        try:
            response = requests.get(f"{self.base_url}/api/v1/nonexistent", timeout=5)
            
            if response.status_code == 404:
                self.log_test_result("404 Handling", "security", True)
            else:
                self.log_test_result("404 Handling", "security", False,
                                   error_msg=f"Status: {response.status_code}")
        except Exception as e:
            self.log_test_result("404 Handling", "security", False,
                               error_msg=str(e))
    
    def check_database_integration(self) -> None:
        """Run database integration tests"""
        print("\n🗄️ Testing Database Integration...")
        
        try:
            # Run the existing API integration test
            result = subprocess.run([
                sys.executable, "test_api_integration.py"
            ], cwd="backend", capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                self.log_test_result("Database Integration", "integration", True,
                                   details="API integration tests passed")
            else:
                self.log_test_result("Database Integration", "integration", False,
                                   error_msg=f"Exit code: {result.returncode}")
        except Exception as e:
            self.log_test_result("Database Integration", "integration", False,
                               error_msg=str(e))
    
    def generate_report(self) -> None:
        """Generate final UAT report"""
        print("\n📊 Generating UAT Report...")
        
        # Calculate pass rate
        pass_rate = (self.results["passed"] / self.results["total_tests"] * 100) if self.results["total_tests"] > 0 else 0
        
        # Generate summary
        print("\n" + "="*50)
        print("UAT EXECUTION SUMMARY REPORT")
        print("="*50)
        print(f"Test Date: {self.results['test_date']}")
        print(f"Total Tests: {self.results['total_tests']}")
        print(f"Passed: {self.results['passed']}")
        print(f"Failed: {self.results['failed']}")
        print(f"Pass Rate: {pass_rate:.1f}%")
        print()
        
        # Show failed tests
        if self.results["issues_found"]:
            print("ISSUES FOUND:")
            for issue in self.results["issues_found"]:
                print(f"❌ {issue['test']} ({issue['category']}): {issue['error']}")
        else:
            print("✅ No issues found!")
        
        print()
        
        # Recommendation
        if pass_rate >= 90:
            print("🎉 RECOMMENDATION: ACCEPT - Ready for production")
        elif pass_rate >= 70:
            print("⚠️ RECOMMENDATION: CONDITIONAL ACCEPT - Minor issues to fix")
        else:
            print("🚫 RECOMMENDATION: REJECT - Major issues require resolution")
        
        # Save detailed results
        with open("uat_test_results.json", "w") as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: uat_test_results.json")
    
    def run_all_tests(self) -> None:
        """Run all UAT test categories"""
        print("🚀 Starting Complete UAT Test Suite...")
        print(f"Backend URL: {self.base_url}")
        print(f"Frontend URL: {self.frontend_url}")
        
        self.test_system_health()
        self.test_ai_agents()
        self.test_performance()
        self.test_error_handling()
        self.check_database_integration()
        
        self.generate_report()
    
    def run_category(self, category: str) -> None:
        """Run specific test category"""
        print(f"🚀 Running UAT Tests - Category: {category}")
        
        if category == "infrastructure":
            self.test_system_health()
        elif category == "ai_agents":
            self.test_ai_agents()
        elif category == "performance":
            self.test_performance()
        elif category == "security":
            self.test_error_handling()
        elif category == "integration":
            self.check_database_integration()
        else:
            print(f"Unknown category: {category}")
            return
        
        self.generate_report()

def main():
    parser = argparse.ArgumentParser(description="RSP Education Agent V2 UAT Test Runner")
    parser.add_argument("--category", choices=["all", "infrastructure", "ai_agents", "performance", "security", "integration"],
                        default="all", help="Test category to run")
    parser.add_argument("--backend-url", default="http://localhost:8000", help="Backend URL")
    parser.add_argument("--frontend-url", default="http://localhost:3000", help="Frontend URL")
    
    args = parser.parse_args()
    
    # Check if services are running
    print("🔍 Checking if services are running...")
    try:
        response = requests.get(f"{args.backend_url}/health", timeout=5)
        if response.status_code != 200:
            print(f"❌ Backend not accessible at {args.backend_url}")
            print("Please start the backend service first:")
            print("cd backend && uvicorn main:app --reload")
            sys.exit(1)
    except:
        print(f"❌ Backend not accessible at {args.backend_url}")
        print("Please start the backend service first:")
        print("cd backend && uvicorn main:app --reload")
        sys.exit(1)
    
    print("✅ Backend service is running")
    
    # Initialize test runner
    runner = UATTestRunner(args.backend_url)
    runner.frontend_url = args.frontend_url
    
    # Run tests
    if args.category == "all":
        runner.run_all_tests()
    else:
        runner.run_category(args.category)

if __name__ == "__main__":
    main()