#!/usr/bin/env python3
"""
Complete User Flow Test - Registration to Assessment Report
Tests the entire student learning journey for UAT readiness
"""

import requests
import json
import sys
import time

BASE_URL = "http://127.0.0.1:8000"
FRONTEND_URL = "http://127.0.0.1:3000"

class UserFlowTester:
    def __init__(self):
        self.session = requests.Session()
        self.access_token = None
        self.user_id = None
        self.test_results = []
    
    def log_result(self, test_name, success, message=""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        self.test_results.append({
            "test": test_name,
            "status": status,
            "message": message
        })
        print(f"{status}: {test_name} - {message}")
    
    def test_user_registration(self):
        """Test Step 1: User Registration"""
        print("\n🔐 TESTING USER REGISTRATION")
        print("=" * 50)
        
        test_user = {
            "username": f"test_student_{int(time.time())}",
            "email": f"test{int(time.time())}@example.com",
            "password": "testpassword123",
            "full_name": "Test Student",
            "grade": 3,
            "preferred_language": "English"
        }
        
        try:
            response = self.session.post(f"{BASE_URL}/auth/register", json=test_user)
            
            if response.status_code == 201:
                data = response.json()
                self.access_token = data.get("access_token")
                self.user_id = data.get("user", {}).get("id")
                self.session.headers.update({"Authorization": f"Bearer {self.access_token}"})
                self.log_result("User Registration", True, f"User ID: {self.user_id}")
                return True
            else:
                self.log_result("User Registration", False, f"Status: {response.status_code}, Error: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("User Registration", False, f"Exception: {e}")
            return False
    
    def test_user_login(self):
        """Test Step 2: User Login (if registration worked)"""
        print("\n🔑 TESTING USER LOGIN")
        print("=" * 40)
        
        if not self.access_token:
            self.log_result("User Login", False, "No access token from registration")
            return False
        
        try:
            # Test protected endpoint to verify authentication
            response = self.session.get(f"{BASE_URL}/user/profile")
            
            if response.status_code == 200:
                data = response.json()
                self.log_result("User Login/Authentication", True, f"Profile loaded for: {data.get('username')}")
                return True
            else:
                self.log_result("User Login/Authentication", False, f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_result("User Login/Authentication", False, f"Exception: {e}")
            return False
    
    def test_curriculum_selection(self):
        """Test Step 3: Grade/Subject/Topic Selection"""
        print("\n📚 TESTING CURRICULUM SELECTION")
        print("=" * 45)
        
        try:
            # Test curriculum endpoint
            response = self.session.get(f"{BASE_URL}/curriculum")
            
            if response.status_code == 200:
                data = response.json()
                subjects = data.get("subjects", [])
                if subjects:
                    self.log_result("Curriculum Loading", True, f"Found {len(subjects)} subjects")
                    
                    # Test specific subject curriculum
                    response = self.session.get(f"{BASE_URL}/curriculum/science/3")
                    if response.status_code == 200:
                        curriculum_data = response.json()
                        chapters = curriculum_data.get("chapters", [])
                        total_topics = sum(len(ch.get("topics", [])) for ch in chapters)
                        self.log_result("Subject Curriculum Access", True, f"Science Grade 3: {len(chapters)} chapters, {total_topics} topics")
                        return True
                    else:
                        self.log_result("Subject Curriculum Access", False, f"Status: {response.status_code}")
                        return False
                else:
                    self.log_result("Curriculum Loading", False, "No subjects found")
                    return False
            else:
                self.log_result("Curriculum Loading", False, f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_result("Curriculum Selection", False, f"Exception: {e}")
            return False
    
    def test_ai_content_generation(self):
        """Test Step 4: AI Learning Content Generation"""
        print("\n🤖 TESTING AI CONTENT GENERATION")
        print("=" * 45)
        
        try:
            # Test content generation for a specific topic
            content_request = {
                "topic": "Living Things Around Us",
                "subject": "Science",
                "grade": 3,
                "content_type": "explanation",
                "difficulty_level": "beginner"
            }
            
            response = self.session.post(f"{BASE_URL}/content/generate", json=content_request)
            
            if response.status_code == 200:
                data = response.json()
                content = data.get("content", "")
                if len(content) > 100:  # Meaningful content generated
                    self.log_result("AI Content Generation", True, f"Generated {len(content)} characters of learning content")
                    return True
                else:
                    self.log_result("AI Content Generation", False, "Content too short or empty")
                    return False
            else:
                self.log_result("AI Content Generation", False, f"Status: {response.status_code}, Error: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("AI Content Generation", False, f"Exception: {e}")
            return False
    
    def test_adaptive_assessment(self):
        """Test Step 5: Adaptive Assessment System"""
        print("\n📝 TESTING ADAPTIVE ASSESSMENT")
        print("=" * 45)
        
        try:
            # Test assessment question generation
            assessment_request = {
                "topic": "Living Things Around Us",
                "subject": "Science", 
                "grade": 3,
                "question_count": 5,
                "difficulty_level": "beginner"
            }
            
            response = self.session.post(f"{BASE_URL}/assessment/generate", json=assessment_request)
            
            if response.status_code == 200:
                data = response.json()
                questions = data.get("questions", [])
                if len(questions) > 0:
                    self.log_result("Adaptive Assessment Generation", True, f"Generated {len(questions)} assessment questions")
                    
                    # Test assessment submission and adaptation
                    answers = [{"question_id": i, "answer": "A", "is_correct": True} for i in range(len(questions))]
                    submission_request = {
                        "assessment_id": data.get("assessment_id"),
                        "answers": answers
                    }
                    
                    response = self.session.post(f"{BASE_URL}/assessment/submit", json=submission_request)
                    if response.status_code == 200:
                        result_data = response.json()
                        score = result_data.get("score", 0)
                        self.log_result("Assessment Submission", True, f"Score: {score}%")
                        return True
                    else:
                        self.log_result("Assessment Submission", False, f"Status: {response.status_code}")
                        return False
                else:
                    self.log_result("Adaptive Assessment Generation", False, "No questions generated")
                    return False
            else:
                self.log_result("Adaptive Assessment Generation", False, f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_result("Adaptive Assessment", False, f"Exception: {e}")
            return False
    
    def test_exam_and_report(self):
        """Test Step 6: Exam System and Assessment Report"""
        print("\n📊 TESTING EXAM & ASSESSMENT REPORTING")
        print("=" * 50)
        
        try:
            # Test exam creation
            exam_request = {
                "subject": "Science",
                "grade": 3,
                "topic": "Living Things Around Us",
                "exam_type": "chapter_test",
                "duration_minutes": 30
            }
            
            response = self.session.post(f"{BASE_URL}/exam/create", json=exam_request)
            
            if response.status_code == 200:
                data = response.json()
                exam_id = data.get("exam_id")
                self.log_result("Exam Creation", True, f"Exam ID: {exam_id}")
                
                # Test assessment report generation
                response = self.session.get(f"{BASE_URL}/analytics/progress/{self.user_id}")
                if response.status_code == 200:
                    report_data = response.json()
                    self.log_result("Assessment Report Generation", True, f"Report generated with {len(report_data.get('subjects', {}))} subjects")
                    return True
                else:
                    self.log_result("Assessment Report Generation", False, f"Status: {response.status_code}")
                    return False
            else:
                self.log_result("Exam Creation", False, f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_result("Exam & Assessment Report", False, f"Exception: {e}")
            return False
    
    def test_gamification_features(self):
        """Test Step 7: Gamification System"""
        print("\n🎮 TESTING GAMIFICATION FEATURES")
        print("=" * 45)
        
        try:
            # Test XP and achievement tracking
            response = self.session.get(f"{BASE_URL}/gamification/profile/{self.user_id}")
            
            if response.status_code == 200:
                data = response.json()
                xp = data.get("total_xp", 0)
                achievements = data.get("achievements", [])
                level = data.get("level", 1)
                self.log_result("Gamification Profile", True, f"Level {level}, {xp} XP, {len(achievements)} achievements")
                return True
            else:
                self.log_result("Gamification Profile", False, f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_result("Gamification Features", False, f"Exception: {e}")
            return False
    
    def test_analytics_tracking(self):
        """Test Step 8: Analytics and Progress Tracking"""
        print("\n📈 TESTING ANALYTICS & PROGRESS TRACKING")
        print("=" * 50)
        
        try:
            # Test analytics dashboard
            response = self.session.get(f"{BASE_URL}/analytics/dashboard/{self.user_id}")
            
            if response.status_code == 200:
                data = response.json()
                study_time = data.get("total_study_time", 0)
                topics_completed = data.get("topics_completed", 0)
                self.log_result("Analytics Dashboard", True, f"Study time: {study_time} min, Topics: {topics_completed}")
                return True
            else:
                self.log_result("Analytics Dashboard", False, f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_result("Analytics Tracking", False, f"Exception: {e}")
            return False
    
    def test_ai_agents_integration(self):
        """Test Step 9: All 8 AI Agents Integration"""
        print("\n🧠 TESTING AI AGENTS INTEGRATION")
        print("=" * 45)
        
        try:
            # Test agents status
            response = self.session.get(f"{BASE_URL}/agents/status")
            
            if response.status_code == 200:
                data = response.json()
                agents = data.get("agents", {})
                active_agents = sum(1 for agent in agents.values() if agent.get("status") == "active")
                self.log_result("AI Agents Status", True, f"{active_agents} agents active out of {len(agents)}")
                return True
            else:
                self.log_result("AI Agents Status", False, f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_result("AI Agents Integration", False, f"Exception: {e}")
            return False
    
    def run_complete_flow_test(self):
        """Run the complete user flow test"""
        print("🚀 RSP EDUCATION AGENT V2 - COMPLETE USER FLOW TEST")
        print("=" * 65)
        print("Testing: Student Registration → Login → Subject Selection → Learning → Assessment → Exam → Report")
        print("=" * 65)
        
        # Run all test steps
        tests = [
            self.test_user_registration,
            self.test_user_login,
            self.test_curriculum_selection,
            self.test_ai_content_generation,
            self.test_adaptive_assessment,
            self.test_exam_and_report,
            self.test_gamification_features,
            self.test_analytics_tracking,
            self.test_ai_agents_integration
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test in tests:
            try:
                if test():
                    passed_tests += 1
            except Exception as e:
                print(f"❌ Test failed with exception: {e}")
        
        # Final Summary
        print(f"\n📊 FINAL UAT READINESS SUMMARY")
        print("=" * 50)
        print(f"Tests Passed: {passed_tests}/{total_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if passed_tests == total_tests:
            print("🎉 ALL TESTS PASSED - SYSTEM READY FOR UAT!")
        elif passed_tests >= total_tests * 0.8:
            print("✅ MOSTLY READY - Minor issues to address")
        else:
            print("⚠️ SIGNIFICANT ISSUES - Need attention before UAT")
        
        print(f"\nDetailed Test Results:")
        for result in self.test_results:
            print(f"{result['status']}: {result['test']} - {result['message']}")
        
        return passed_tests == total_tests

if __name__ == "__main__":
    tester = UserFlowTester()
    tester.run_complete_flow_test()