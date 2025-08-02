#!/usr/bin/env python3
"""
Simple test script for Content Generator Agent
"""

import asyncio
import logging
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.content_generator import (
    ContentGeneratorAgent,
    ContentRequest,
    ContentType,
    DifficultyLevel,
    QuestionRequest,
    QuestionType
)

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def test_curriculum_access():
    """Test basic curriculum access"""
    print("=" * 50)
    print("Testing Curriculum Access")
    print("=" * 50)
    
    try:
        agent = ContentGeneratorAgent()
        
        # Test curriculum initialization
        curriculum = agent.curriculum
        
        # Test searching for a math topic
        math_topics = await curriculum.search_topics("place value", "Mathematics", 3)
        print(f"Found Math topics for 'place value': {len(math_topics)}")
        for topic in math_topics:
            print(f"  - Grade {topic['grade']}: {topic['topic']} (Chapter: {topic['chapter']})")
        
        # Test getting topic details  
        topic_details = await curriculum.get_topic_details("Mathematics", 3, "Place Value in 3-digit Numbers")
        if topic_details:
            print(f"\nTopic Details for 'Place Value in 3-digit Numbers':")
            print(f"  Code: {topic_details['code']}")
            print(f"  Chapter: {topic_details['chapter']}")
            print(f"  Learning Objectives: {topic_details['learning_objectives']}")
            print(f"  Prerequisites: {topic_details['prerequisites']}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Curriculum test failed: {e}")
        return False

async def test_agent_status():
    """Test agent status and initialization"""
    print("\n" + "=" * 50)
    print("Testing Agent Status")
    print("=" * 50)
    
    try:
        agent = ContentGeneratorAgent()
        status = await agent.get_agent_status()
        
        print("Agent Status:")
        print(f"  Name: {status['name']}")
        print(f"  Status: {status['status']}")
        print(f"  OpenAI Model Available: {status['models_available']['openai']}")
        print(f"  Anthropic Model Available: {status['models_available']['anthropic']}")
        print(f"  Supported Content Types: {status['supported_content_types']}")
        print(f"  Curriculum Loaded: {status['curriculum_loaded']}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Agent status test failed: {e}")
        return False

async def test_content_request_creation():
    """Test content request model creation"""
    print("\n" + "=" * 50)
    print("Testing Content Request Creation")
    print("=" * 50)
    
    try:
        # Test creating content request
        content_request = ContentRequest(
            subject="Mathematics",
            grade=3,
            topic="Place Value in 3-digit Numbers",
            content_type=ContentType.EXPLANATION,
            difficulty=DifficultyLevel.INTERMEDIATE
        )
        
        print("Content Request Created Successfully:")
        print(f"  Subject: {content_request.subject}")
        print(f"  Grade: {content_request.grade}")
        print(f"  Topic: {content_request.topic}")
        print(f"  Content Type: {content_request.content_type}")
        print(f"  Difficulty: {content_request.difficulty}")
        
        # Test creating question request
        question_request = QuestionRequest(
            subject="Mathematics",
            grade=3,
            topic="Place Value in 3-digit Numbers",
            question_type=QuestionType.MCQ,
            difficulty=DifficultyLevel.INTERMEDIATE,
            num_questions=2
        )
        
        print("\nQuestion Request Created Successfully:")
        print(f"  Subject: {question_request.subject}")
        print(f"  Question Type: {question_request.question_type}")
        print(f"  Number of Questions: {question_request.num_questions}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Request creation test failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("RSP Education Agent V2 - Content Generator Test Suite")
    print("=" * 60)
    
    tests = [
        ("Curriculum Access", test_curriculum_access),
        ("Agent Status", test_agent_status), 
        ("Request Creation", test_content_request_creation)
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
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "[PASS]" if result else "[FAIL]"
        print(f"{test_name:<20} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("SUCCESS: All tests passed! Content Generator Agent is working correctly.")
        return 0
    else:
        print("WARNING: Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)