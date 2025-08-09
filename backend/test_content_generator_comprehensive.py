#!/usr/bin/env python3
"""
Comprehensive Content Generator Testing Script
Tests the content generator agent across multiple subjects, grades, and content types
"""

import asyncio
import json
import sys
import time
from typing import Dict, List
sys.path.append('.')

from agents.content_generator import ContentGeneratorAgent, ContentRequest
from config.settings import settings

class ContentGeneratorTester:
    def __init__(self):
        self.agent = ContentGeneratorAgent()
        self.test_results = []
        
    async def test_scenario(self, scenario_name: str, request_data: dict):
        """Test a single content generation scenario"""
        print(f"\n🧪 Testing: {scenario_name}")
        print(f"📋 Request: {json.dumps(request_data, indent=2)}")
        
        start_time = time.time()
        try:
            request = ContentRequest(**request_data)
            result = await self.agent.generate_content(request)
            end_time = time.time()
            
            # Analyze the result
            content_length = len(result.content) if hasattr(result, 'content') else 0
            response_time = end_time - start_time
            
            test_result = {
                'scenario': scenario_name,
                'request': request_data,
                'success': True,
                'content_length': content_length,
                'response_time': response_time,
                'result_type': str(type(result)),
                'content_preview': result.content[:200] + "..." if hasattr(result, 'content') and len(result.content) > 200 else getattr(result, 'content', 'No content attribute'),
                'learning_objectives': getattr(result, 'learning_objectives', []),
                'estimated_time': getattr(result, 'estimated_time', 0),
                'prerequisites': getattr(result, 'prerequisites', [])
            }
            
            print(f"✅ SUCCESS")
            print(f"📏 Content Length: {content_length} characters")
            print(f"⏱️  Response Time: {response_time:.2f} seconds") 
            print(f"🎯 Learning Objectives: {len(test_result['learning_objectives'])}")
            print(f"📖 Content Preview: {test_result['content_preview'][:150]}...")
            
        except Exception as e:
            end_time = time.time()
            test_result = {
                'scenario': scenario_name,
                'request': request_data,
                'success': False,
                'error': str(e),
                'response_time': end_time - start_time,
                'content_length': 0
            }
            print(f"❌ FAILED: {str(e)}")
            
        self.test_results.append(test_result)
        return test_result
    
    async def run_comprehensive_tests(self):
        """Run comprehensive content generator tests"""
        print("🚀 Starting Comprehensive Content Generator Testing")
        print(f"🔑 API Keys Status:")
        print(f"   OpenAI: {'✅ Configured' if settings.openai_api_key else '❌ Missing'}")
        print(f"   Anthropic: {'✅ Configured' if settings.anthropic_api_key else '❌ Missing'}")
        print(f"   OpenAI Model: {settings.openai_model}")
        print(f"   Anthropic Model: {settings.anthropic_model}")
        
        # Test scenarios across different subjects, grades, and content types
        test_scenarios = [
            # Mathematics tests
            {
                'name': 'Mathematics - Grade 1 - Basic Addition',
                'data': {
                    'topic': 'Addition of single digit numbers',
                    'subject': 'Mathematics',
                    'grade': 1,
                    'content_type': 'explanation',
                    'difficulty': 'beginner'
                }
            },
            {
                'name': 'Mathematics - Grade 8 - Algebra',
                'data': {
                    'topic': 'Linear Equations',
                    'subject': 'Mathematics',
                    'grade': 8,
                    'content_type': 'explanation',
                    'difficulty': 'intermediate'
                }
            },
            {
                'name': 'Mathematics - Grade 12 - Calculus',
                'data': {
                    'topic': 'Derivatives',
                    'subject': 'Mathematics', 
                    'grade': 12,
                    'content_type': 'explanation',
                    'difficulty': 'advanced'
                }
            },
            
            # Science tests
            {
                'name': 'Science - Grade 3 - Plants',
                'data': {
                    'topic': 'Parts of a Plant',
                    'subject': 'Science',
                    'grade': 3,
                    'content_type': 'explanation',
                    'difficulty': 'beginner'
                }
            },
            {
                'name': 'Science - Grade 7 - Physics',
                'data': {
                    'topic': 'Force and Motion',
                    'subject': 'Science',
                    'grade': 7,
                    'content_type': 'explanation',
                    'difficulty': 'intermediate'
                }
            },
            {
                'name': 'Science - Grade 10 - Chemistry',
                'data': {
                    'topic': 'Chemical Bonding',
                    'subject': 'Science',
                    'grade': 10,
                    'content_type': 'explanation',
                    'difficulty': 'advanced'
                }
            },
            
            # English tests
            {
                'name': 'English - Grade 2 - Reading',
                'data': {
                    'topic': 'Reading comprehension strategies',
                    'subject': 'English',
                    'grade': 2,
                    'content_type': 'explanation',
                    'difficulty': 'beginner'
                }
            },
            {
                'name': 'English - Grade 9 - Literature',
                'data': {
                    'topic': 'Poetry Analysis',
                    'subject': 'English',
                    'grade': 9,
                    'content_type': 'explanation',
                    'difficulty': 'intermediate'
                }
            },
            
            # Social Studies tests
            {
                'name': 'Social Studies - Grade 6 - History',
                'data': {
                    'topic': 'Ancient Civilizations',
                    'subject': 'Social Studies',
                    'grade': 6,
                    'content_type': 'explanation',
                    'difficulty': 'intermediate'
                }
            },
            
            # Different content types
            {
                'name': 'Mathematics - Example Content Type',
                'data': {
                    'topic': 'Fractions',
                    'subject': 'Mathematics',
                    'grade': 5,
                    'content_type': 'example',
                    'difficulty': 'intermediate'
                }
            },
            {
                'name': 'Science - Exercise Content Type',
                'data': {
                    'topic': 'Solar System',
                    'subject': 'Science',
                    'grade': 4,
                    'content_type': 'exercise',
                    'difficulty': 'beginner'
                }
            }
        ]
        
        # Run all test scenarios
        for scenario in test_scenarios:
            await self.test_scenario(scenario['name'], scenario['data'])
            await asyncio.sleep(1)  # Small delay between tests
        
        # Generate summary report
        await self.generate_summary_report()
    
    async def generate_summary_report(self):
        """Generate comprehensive test summary"""
        print("\n" + "="*70)
        print("📊 COMPREHENSIVE CONTENT GENERATOR TEST REPORT")
        print("="*70)
        
        total_tests = len(self.test_results)
        successful_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - successful_tests
        
        print(f"📈 Overall Results:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Successful: {successful_tests} ✅")
        print(f"   Failed: {failed_tests} ❌")
        print(f"   Success Rate: {(successful_tests/total_tests)*100:.1f}%")
        
        if successful_tests > 0:
            successful_results = [r for r in self.test_results if r['success']]
            avg_length = sum(r['content_length'] for r in successful_results) / len(successful_results)
            avg_response_time = sum(r['response_time'] for r in successful_results) / len(successful_results)
            
            print(f"\n📊 Performance Metrics (Successful Tests):")
            print(f"   Average Content Length: {avg_length:.0f} characters")
            print(f"   Average Response Time: {avg_response_time:.2f} seconds")
            print(f"   Min Content Length: {min(r['content_length'] for r in successful_results)}")
            print(f"   Max Content Length: {max(r['content_length'] for r in successful_results)}")
        
        print(f"\n📝 Detailed Results:")
        for i, result in enumerate(self.test_results, 1):
            status = "✅" if result['success'] else "❌"
            print(f"   {i:2d}. {status} {result['scenario']}")
            if result['success']:
                print(f"       Length: {result['content_length']} chars, Time: {result['response_time']:.2f}s")
            else:
                print(f"       Error: {result.get('error', 'Unknown error')}")
        
        if failed_tests > 0:
            print(f"\n⚠️  Failed Test Details:")
            for result in self.test_results:
                if not result['success']:
                    print(f"   ❌ {result['scenario']}")
                    print(f"      Request: {result['request']}")
                    print(f"      Error: {result.get('error', 'Unknown')}")
        
        print("\n" + "="*70)

async def main():
    """Main test execution"""
    tester = ContentGeneratorTester()
    await tester.run_comprehensive_tests()

if __name__ == "__main__":
    asyncio.run(main())