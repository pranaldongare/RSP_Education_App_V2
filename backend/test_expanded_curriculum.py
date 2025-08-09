#!/usr/bin/env python3
"""
Test Expanded Curriculum with Content Generator
Tests the content generation capabilities with the newly expanded Mathematics and Science curricula
"""

import asyncio
import sys
import json
from typing import Dict, List
sys.path.append('.')

from core.curriculum import CBSECurriculum, Subject
from agents.content_generator import ContentGeneratorAgent, ContentRequest
from expand_mathematics_curriculum import MathematicsExpansion
from expand_science_curriculum import ScienceExpansion

class ExpandedCurriculumTester:
    def __init__(self):
        self.curriculum = CBSECurriculum()
        self.content_agent = ContentGeneratorAgent()
        self.math_expander = MathematicsExpansion()
        self.science_expander = ScienceExpansion()
        self.test_results = {}
        
    async def test_expanded_curriculum_content_generation(self):
        """Test content generation with expanded curriculum"""
        print("TESTING EXPANDED CURRICULUM CONTENT GENERATION")
        print("=" * 60)
        
        await self.test_mathematics_expanded_content()
        await self.test_science_expanded_content()
        await self.generate_test_summary()
    
    async def test_mathematics_expanded_content(self):
        """Test Mathematics expanded curriculum content generation"""
        print("\n1. TESTING MATHEMATICS EXPANDED CURRICULUM")
        print("-" * 50)
        
        # Test sample topics from each expanded grade
        math_test_cases = [
            {"grade": 1, "topic": "Counting Numbers 1-20", "expected_difficulty": "beginner"},
            {"grade": 1, "topic": "Addition up to 20", "expected_difficulty": "beginner"},
            {"grade": 2, "topic": "Place Value - Tens and Ones", "expected_difficulty": "intermediate"},
            {"grade": 2, "topic": "Addition with Regrouping", "expected_difficulty": "intermediate"},
            {"grade": 3, "topic": "Multiplication Tables and Facts", "expected_difficulty": "intermediate"},
            {"grade": 3, "topic": "Division with Remainders", "expected_difficulty": "advanced"},
            {"grade": 4, "topic": "Advanced Multiplication", "expected_difficulty": "advanced"},
            {"grade": 4, "topic": "Area and Perimeter", "expected_difficulty": "advanced"},
            {"grade": 5, "topic": "Decimal Operations", "expected_difficulty": "advanced"},
            {"grade": 5, "topic": "Percentage Introduction", "expected_difficulty": "advanced"}
        ]
        
        math_results = await self.test_content_generation_batch("Mathematics", math_test_cases)
        self.test_results["mathematics"] = math_results
        
        # Display results
        successful = sum(1 for result in math_results if result["success"])
        total = len(math_results)
        success_rate = (successful / total) * 100
        
        print(f"\nMATHEMATICS TEST RESULTS:")
        print(f"  Total Tests: {total}")
        print(f"  Successful: {successful}")
        print(f"  Success Rate: {success_rate:.1f}%")
        
        for result in math_results:
            status = "✓" if result["success"] else "✗"
            print(f"  {status} Grade {result['grade']}: {result['topic'][:40]}...")
    
    async def test_science_expanded_content(self):
        """Test Science expanded curriculum content generation"""
        print("\n2. TESTING SCIENCE EXPANDED CURRICULUM")
        print("-" * 50)
        
        # Test sample topics from each expanded grade
        science_test_cases = [
            {"grade": 1, "topic": "Living Things Around Us", "expected_difficulty": "beginner"},
            {"grade": 1, "topic": "Animals in Our Environment", "expected_difficulty": "beginner"},
            {"grade": 2, "topic": "Parts of a Plant", "expected_difficulty": "beginner"},
            {"grade": 2, "topic": "Healthy Food Habits", "expected_difficulty": "intermediate"},
            {"grade": 3, "topic": "Life Cycle of Plants", "expected_difficulty": "intermediate"},
            {"grade": 3, "topic": "Our Sense Organs", "expected_difficulty": "intermediate"},
            {"grade": 4, "topic": "Plant Structure and Functions", "expected_difficulty": "intermediate"},
            {"grade": 4, "topic": "Food Chains and Webs", "expected_difficulty": "advanced"},
            {"grade": 5, "topic": "Plant and Animal Interdependence", "expected_difficulty": "advanced"},
            {"grade": 5, "topic": "States of Matter", "expected_difficulty": "intermediate"}
        ]
        
        science_results = await self.test_content_generation_batch("Science", science_test_cases)
        self.test_results["science"] = science_results
        
        # Display results
        successful = sum(1 for result in science_results if result["success"])
        total = len(science_results)
        success_rate = (successful / total) * 100
        
        print(f"\nSCIENCE TEST RESULTS:")
        print(f"  Total Tests: {total}")
        print(f"  Successful: {successful}")
        print(f"  Success Rate: {success_rate:.1f}%")
        
        for result in science_results:
            status = "✓" if result["success"] else "✗"
            print(f"  {status} Grade {result['grade']}: {result['topic'][:40]}...")
    
    async def test_content_generation_batch(self, subject: str, test_cases: List[Dict]) -> List[Dict]:
        """Test content generation for a batch of topics"""
        results = []
        
        for case in test_cases:
            try:
                request = ContentRequest(
                    subject=subject,
                    grade=case['grade'],
                    topic=case['topic'],
                    content_type='explanation',
                    difficulty=case['expected_difficulty']
                )
                
                result = await self.content_agent.generate_content(request)
                
                test_result = {
                    'subject': subject,
                    'grade': case['grade'],
                    'topic': case['topic'],
                    'success': True,
                    'content_length': len(result.content),
                    'objectives_count': len(result.learning_objectives),
                    'estimated_time': result.estimated_time,
                    'difficulty_requested': case['expected_difficulty'],
                    'error': None
                }
                results.append(test_result)
                
            except Exception as e:
                test_result = {
                    'subject': subject,
                    'grade': case['grade'],
                    'topic': case['topic'],
                    'success': False,
                    'error': str(e),
                    'difficulty_requested': case['expected_difficulty']
                }
                results.append(test_result)
        
        return results
    
    async def generate_test_summary(self):
        """Generate comprehensive test summary"""
        print("\n3. COMPREHENSIVE TEST SUMMARY")
        print("=" * 60)
        
        # Calculate overall statistics
        all_results = []
        all_results.extend(self.test_results.get("mathematics", []))
        all_results.extend(self.test_results.get("science", []))
        
        total_tests = len(all_results)
        successful_tests = sum(1 for result in all_results if result["success"])
        overall_success_rate = (successful_tests / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"OVERALL EXPANDED CURRICULUM TEST RESULTS:")
        print(f"  Total Content Generation Tests: {total_tests}")
        print(f"  Successful Generations: {successful_tests}")
        print(f"  Overall Success Rate: {overall_success_rate:.1f}%")
        
        # Success by subject
        math_successful = sum(1 for result in self.test_results.get("mathematics", []) if result["success"])
        math_total = len(self.test_results.get("mathematics", []))
        science_successful = sum(1 for result in self.test_results.get("science", []) if result["success"])
        science_total = len(self.test_results.get("science", []))
        
        print(f"\nSUBJECT-WISE RESULTS:")
        print(f"  Mathematics: {math_successful}/{math_total} ({(math_successful/math_total)*100:.1f}%)")
        print(f"  Science: {science_successful}/{science_total} ({(science_successful/science_total)*100:.1f}%)")
        
        # Success by difficulty level
        difficulty_stats = {}
        for result in all_results:
            if result["success"]:
                difficulty = result.get("difficulty_requested", "unknown")
                if difficulty not in difficulty_stats:
                    difficulty_stats[difficulty] = {"successful": 0, "total": 0}
                difficulty_stats[difficulty]["successful"] += 1
            
            difficulty = result.get("difficulty_requested", "unknown")
            if difficulty not in difficulty_stats:
                difficulty_stats[difficulty] = {"successful": 0, "total": 0}
            difficulty_stats[difficulty]["total"] += 1
        
        print(f"\nDIFFICULTY LEVEL RESULTS:")
        for difficulty, stats in difficulty_stats.items():
            success_rate = (stats["successful"] / stats["total"]) * 100 if stats["total"] > 0 else 0
            print(f"  {difficulty.title()}: {stats['successful']}/{stats['total']} ({success_rate:.1f}%)")
        
        # Average content metrics
        successful_results = [r for r in all_results if r["success"]]
        if successful_results:
            avg_content_length = sum(r.get("content_length", 0) for r in successful_results) / len(successful_results)
            avg_objectives = sum(r.get("objectives_count", 0) for r in successful_results) / len(successful_results)
            avg_time = sum(r.get("estimated_time", 0) for r in successful_results) / len(successful_results)
            
            print(f"\nCONTENT QUALITY METRICS:")
            print(f"  Average Content Length: {avg_content_length:.0f} characters")
            print(f"  Average Learning Objectives: {avg_objectives:.1f}")
            print(f"  Average Estimated Time: {avg_time:.1f} minutes")
        
        # Final assessment
        if overall_success_rate >= 90:
            status = "EXCELLENT - Expanded curriculum ready for production"
        elif overall_success_rate >= 80:
            status = "GOOD - Minor issues to address"
        elif overall_success_rate >= 70:
            status = "FAIR - Some improvements needed"
        else:
            status = "POOR - Major fixes required"
        
        print(f"\nFINAL ASSESSMENT: {status}")
        
        # Next steps
        print(f"\nNEXT STEPS:")
        if overall_success_rate >= 80:
            print(f"  ✓ Mathematics and Science curriculum expansions are working well")
            print(f"  → Proceed to expand English and Social Studies curricula")
            print(f"  → Continue with missing subjects (Hindi, Computer Science, etc.)")
        else:
            print(f"  ⚠ Review and fix content generation issues")
            print(f"  → Check curriculum data structure and agent integration")
        
        print("=" * 60)

async def main():
    """Main test execution"""
    tester = ExpandedCurriculumTester()
    await tester.test_expanded_curriculum_content_generation()

if __name__ == "__main__":
    asyncio.run(main())