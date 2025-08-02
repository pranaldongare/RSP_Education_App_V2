#!/usr/bin/env python3
"""
Advanced test script for Content Generator Agent - Testing actual content generation
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

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def test_content_generation():
    """Test actual content generation"""
    print("=" * 60)
    print("Testing Content Generation")
    print("=" * 60)
    
    try:
        agent = ContentGeneratorAgent()
        
        # Test content generation for Mathematics
        content_request = ContentRequest(
            subject="Mathematics",
            grade=3,
            topic="Place Value in 3-digit Numbers",
            content_type=ContentType.EXPLANATION,
            difficulty=DifficultyLevel.INTERMEDIATE,
            learning_objectives=[
                "Understand the concept of hundreds, tens, and ones",
                "Read and write 3-digit numbers correctly"
            ]
        )
        
        print("Generating content...")
        generated_content = await agent.generate_content(content_request)
        
        print("\n[SUCCESS] Content Generated:")
        print(f"Subject: {generated_content.subject}")
        print(f"Grade: {generated_content.grade}")
        print(f"Topic: {generated_content.topic}")
        print(f"Content Type: {generated_content.content_type}")
        print(f"Difficulty: {generated_content.difficulty}")
        print(f"Estimated Time: {generated_content.estimated_time} minutes")
        print(f"Learning Objectives: {generated_content.learning_objectives}")
        print(f"Prerequisites: {generated_content.prerequisites}")
        print(f"Generated At: {generated_content.generated_at}")
        
        print(f"\n[CONTENT PREVIEW]:")
        print("-" * 40)
        content_preview = generated_content.content[:500] + "..." if len(generated_content.content) > 500 else generated_content.content
        print(content_preview)
        print("-" * 40)
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Content generation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_question_generation():
    """Test question generation"""
    print("\n" + "=" * 60)
    print("Testing Question Generation")
    print("=" * 60)
    
    try:
        agent = ContentGeneratorAgent()
        
        # Test MCQ generation
        question_request = QuestionRequest(
            subject="Mathematics",
            grade=3,
            topic="Place Value in 3-digit Numbers",
            question_type=QuestionType.MCQ,
            difficulty=DifficultyLevel.INTERMEDIATE,
            num_questions=2
        )
        
        print("Generating questions...")
        generated_questions = await agent.generate_questions(question_request)
        
        print(f"\n[SUCCESS] Generated {len(generated_questions)} questions:")
        
        for i, question in enumerate(generated_questions, 1):
            print(f"\n--- Question {i} ---")
            print(f"Question: {question.question}")
            print(f"Type: {question.question_type}")
            if question.options:
                print(f"Options: {question.options}")
            print(f"Correct Answer: {question.correct_answer}")
            print(f"Explanation: {question.explanation}")
            print(f"Learning Objective: {question.learning_objective}")
            print(f"Difficulty: {question.difficulty}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Question generation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_explanation_generation():
    """Test explanation generation"""
    print("\n" + "=" * 60)
    print("Testing Explanation Generation")
    print("=" * 60)
    
    try:
        agent = ContentGeneratorAgent()
        
        # Test explanation generation
        print("Generating explanation for 'Place Value' concept...")
        explanation = await agent.generate_explanation(
            topic="Place Value in 3-digit Numbers",
            subject="Mathematics",
            grade=3,
            concept="Place Value",
            difficulty=DifficultyLevel.INTERMEDIATE
        )
        
        print("\n[SUCCESS] Explanation Generated:")
        print("-" * 40)
        explanation_preview = explanation[:600] + "..." if len(explanation) > 600 else explanation
        print(explanation_preview)
        print("-" * 40)
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Explanation generation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_different_subjects():
    """Test content generation for different subjects"""
    print("\n" + "=" * 60)
    print("Testing Different Subjects")
    print("=" * 60)
    
    test_cases = [
        {
            "subject": "Science", 
            "grade": 5, 
            "topic": "Human Senses and Animal Senses",
            "content_type": ContentType.EXAMPLE
        },
        {
            "subject": "English", 
            "grade": 2, 
            "topic": "Simple Story Reading",
            "content_type": ContentType.EXERCISE
        }
    ]
    
    success_count = 0
    
    for i, test_case in enumerate(test_cases, 1):
        try:
            print(f"\n--- Test Case {i}: {test_case['subject']} Grade {test_case['grade']} ---")
            
            agent = ContentGeneratorAgent()
            request = ContentRequest(**test_case, difficulty=DifficultyLevel.BEGINNER)
            
            content = await agent.generate_content(request)
            
            print(f"[SUCCESS] Generated {test_case['content_type'].value} for {test_case['subject']}")
            print(f"Topic: {content.topic}")
            print(f"Estimated Time: {content.estimated_time} minutes")
            print(f"Learning Objectives Count: {len(content.learning_objectives)}")
            
            success_count += 1
            
        except Exception as e:
            print(f"[ERROR] Failed for {test_case['subject']}: {e}")
    
    print(f"\n[SUMMARY] {success_count}/{len(test_cases)} subject tests passed")
    return success_count == len(test_cases)

async def main():
    """Run all advanced tests"""
    print("RSP Education Agent V2 - Advanced Content Generation Test Suite")
    print("=" * 70)
    print("Testing actual content generation functionality...")
    
    tests = [
        ("Content Generation", test_content_generation),
        ("Question Generation", test_question_generation),
        ("Explanation Generation", test_explanation_generation),
        ("Different Subjects", test_different_subjects)
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
    print("\n" + "=" * 70)
    print("ADVANCED TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "[PASS]" if result else "[FAIL]"
        print(f"{test_name:<25} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("SUCCESS: All advanced tests passed! Content Generator Agent is fully functional.")
        print("\nCONTENT GENERATOR AGENT STATUS: READY FOR PRODUCTION")
        return 0
    else:
        print("WARNING: Some advanced tests failed. Content Generator needs refinement.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)