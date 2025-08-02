#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Suite for Assessment Agent - Phase 3
Tests all assessment functionality including evaluation, feedback, and progress tracking.
"""

import sys
import os
import asyncio
import logging
from typing import List, Dict

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.assessment_agent import (
    AssessmentAgent, StudentResponse, AssessmentRequest, AssessmentResult,
    AssessmentType, FeedbackLevel, ScoreType, LearningProgress
)
from agents.content_generator import QuestionType, DifficultyLevel

# Configure logging to suppress unnecessary output during testing
logging.basicConfig(level=logging.WARNING)


async def test_agent_initialization():
    """Test Assessment Agent initialization"""
    print("\n" + "="*50)
    print("Testing Assessment Agent Initialization")
    print("="*50)
    
    try:
        agent = AssessmentAgent()
        
        # Test agent status
        status = await agent.get_agent_status()
        
        print("Assessment Agent Status:")
        print(f"  Name: {status['name']}")
        print(f"  Status: {status['status']}")
        print(f"  OpenAI Model Available: {status['models_available']['openai']}")
        print(f"  Anthropic Model Available: {status['models_available']['anthropic']}")
        print(f"  Supported Assessment Types: {status['supported_assessment_types']}")
        print(f"  Supported Feedback Levels: {status['supported_feedback_levels']}")
        print(f"  Curriculum Loaded: {status['curriculum_loaded']}")
        
        assert status['name'] == "AssessmentAgent"
        assert status['status'] == "active"
        assert status['curriculum_loaded'] == True
        assert len(status['supported_assessment_types']) > 0
        
        print("[PASS] Assessment Agent initialization test PASSED")
        return True
        
    except Exception as e:
        print(f"[FAIL] Assessment Agent initialization test FAILED: {e}")
        return False


async def test_student_response_creation():
    """Test creating student response objects"""
    print("\n" + "="*50)
    print("Testing Student Response Creation")
    print("="*50)
    
    try:
        # Test MCQ response
        mcq_response = StudentResponse(
            question_id="mcq_001",
            student_answer="B",
            question_text="What is 2 + 2?",
            correct_answer="B",
            question_type=QuestionType.MCQ,
            options=["A. 3", "B. 4", "C. 5", "D. 6"],
            time_taken=30
        )
        
        # Test short answer response
        short_response = StudentResponse(
            question_id="short_001",
            student_answer="The answer is 4 because 2 plus 2 equals 4",
            question_text="Explain what 2 + 2 equals and why",
            correct_answer="4, because addition combines quantities",
            question_type=QuestionType.SHORT_ANSWER,
            time_taken=120
        )
        
        print("MCQ Response Created:")
        print(f"  Question ID: {mcq_response.question_id}")
        print(f"  Question Type: {mcq_response.question_type}")
        print(f"  Student Answer: {mcq_response.student_answer}")
        print(f"  Correct Answer: {mcq_response.correct_answer}")
        
        print("\nShort Answer Response Created:")
        print(f"  Question ID: {short_response.question_id}")
        print(f"  Question Type: {short_response.question_type}")
        print(f"  Student Answer: {short_response.student_answer[:50]}...")
        print(f"  Time Taken: {short_response.time_taken} seconds")
        
        print("[PASS] Student Response creation test PASSED")
        return True
        
    except Exception as e:
        print(f"[FAIL] Student Response creation test FAILED: {e}")
        return False


async def test_assessment_request_creation():
    """Test creating assessment request objects"""
    print("\n" + "="*50)
    print("Testing Assessment Request Creation")
    print("="*50)
    
    try:
        responses = [
            StudentResponse(
                question_id="q1",
                student_answer="4",
                question_text="What is 2 + 2?",
                correct_answer="4",
                question_type=QuestionType.SHORT_ANSWER
            ),
            StudentResponse(
                question_id="q2",
                student_answer="6",
                question_text="What is 3 + 3?",
                correct_answer="6",
                question_type=QuestionType.SHORT_ANSWER
            )
        ]
        
        request = AssessmentRequest(
            student_id="student_123",
            responses=responses,
            assessment_type=AssessmentType.FORMATIVE,
            feedback_level=FeedbackLevel.DETAILED,
            score_type=ScoreType.PARTIAL,
            subject="Mathematics",
            grade=3,
            topic="Place Value in 3-digit Numbers"
        )
        
        print("Assessment Request Created:")
        print(f"  Student ID: {request.student_id}")
        print(f"  Number of Responses: {len(request.responses)}")
        print(f"  Assessment Type: {request.assessment_type}")
        print(f"  Feedback Level: {request.feedback_level}")
        print(f"  Subject: {request.subject}")
        print(f"  Grade: {request.grade}")
        print(f"  Topic: {request.topic}")
        
        print("[PASS] Assessment Request creation test PASSED")
        return True
        
    except Exception as e:
        print(f"[FAIL] Assessment Request creation test FAILED: {e}")
        return False


async def test_single_answer_assessment():
    """Test assessing a single correct answer"""
    print("\n" + "="*50)
    print("Testing Single Answer Assessment")
    print("="*50)
    
    try:
        agent = AssessmentAgent()
        
        # Create a simple correct response
        correct_response = StudentResponse(
            question_id="simple_001",
            student_answer="4",
            question_text="What is 2 + 2?",
            correct_answer="4",
            question_type=QuestionType.SHORT_ANSWER,
            time_taken=15
        )
        
        request = AssessmentRequest(
            student_id="test_student",
            responses=[correct_response],
            assessment_type=AssessmentType.FORMATIVE,
            feedback_level=FeedbackLevel.DETAILED,
            subject="Mathematics",
            grade=1,
            topic="Addition up to 9"
        )
        
        # Assess the response
        result = await agent.assess_responses(request)
        
        print("Assessment Result:")
        print(f"  Student ID: {result.student_id}")
        print(f"  Overall Score: {result.performance_metrics.overall_score:.2%}")
        print(f"  Correct Answers: {result.performance_metrics.correct_answers}")
        print(f"  Total Questions: {result.performance_metrics.total_questions}")
        print(f"  Mastery Level: {result.performance_metrics.subject_mastery_level}")
        
        print("\nFirst Feedback Item:")
        feedback = result.feedback_items[0]
        print(f"  Is Correct: {feedback.is_correct}")
        print(f"  Score: {feedback.score}")
        print(f"  Feedback: {feedback.feedback_text[:100]}...")
        print(f"  Concepts Demonstrated: {feedback.concepts_demonstrated}")
        
        assert result.performance_metrics.correct_answers == 1
        assert result.performance_metrics.total_questions == 1
        assert result.performance_metrics.overall_score == 1.0
        assert feedback.is_correct == True
        assert feedback.score == 1.0
        
        print("[PASS] Single Answer assessment test PASSED")
        return True
        
    except Exception as e:
        print(f"[FAIL] Single Answer assessment test FAILED: {e}")
        return False


async def test_multiple_choice_assessment():
    """Test assessing multiple choice questions"""
    print("\n" + "="*50)
    print("Testing Multiple Choice Assessment")
    print("="*50)
    
    try:
        agent = AssessmentAgent()
        
        # Create MCQ responses - mix of correct and incorrect
        responses = [
            StudentResponse(
                question_id="mcq_001",
                student_answer="B",
                question_text="What is the result of 5 + 3?",
                correct_answer="B",
                question_type=QuestionType.MCQ,
                options=["A. 7", "B. 8", "C. 9", "D. 10"]
            ),
            StudentResponse(
                question_id="mcq_002", 
                student_answer="C",
                question_text="Which is the largest number?",
                correct_answer="A",
                question_type=QuestionType.MCQ,
                options=["A. 100", "B. 50", "C. 75", "D. 25"]
            ),
            StudentResponse(
                question_id="mcq_003",
                student_answer="A",
                question_text="What is 10 - 4?",
                correct_answer="A",
                question_type=QuestionType.MCQ,
                options=["A. 6", "B. 7", "C. 8", "D. 9"]
            )
        ]
        
        request = AssessmentRequest(
            student_id="mcq_test_student",
            responses=responses,
            assessment_type=AssessmentType.SUMMATIVE,
            feedback_level=FeedbackLevel.COMPREHENSIVE,
            score_type=ScoreType.BINARY,  # MCQs are typically binary
            subject="Mathematics",
            grade=2,
            topic="Place Value"
        )
        
        result = await agent.assess_responses(request)
        
        print("MCQ Assessment Result:")
        print(f"  Total Questions: {result.performance_metrics.total_questions}")
        print(f"  Correct Answers: {result.performance_metrics.correct_answers}")
        print(f"  Incorrect Answers: {result.performance_metrics.incorrect_answers}")
        print(f"  Overall Score: {result.performance_metrics.overall_score:.2%}")
        
        print(f"\nDetailed Results:")
        for i, feedback in enumerate(result.feedback_items):
            print(f"  Question {i+1}: {'CORRECT' if feedback.is_correct else 'INCORRECT'} (Score: {feedback.score})")
        
        print(f"\nOverall Feedback:")
        print(f"  {result.overall_feedback[:200]}...")
        
        # Should have 2 correct, 1 incorrect
        assert result.performance_metrics.total_questions == 3
        assert result.performance_metrics.correct_answers == 2
        assert result.performance_metrics.incorrect_answers == 1
        assert abs(result.performance_metrics.overall_score - 0.667) < 0.01  # 2/3 ≈ 0.667
        
        print("[PASS] Multiple Choice assessment test PASSED")
        return True
        
    except Exception as e:
        print(f"[FAIL] Multiple Choice assessment test FAILED: {e}")
        return False


async def test_partial_credit_scoring():
    """Test partial credit scoring for text-based answers"""
    print("\n" + "="*50)
    print("Testing Partial Credit Scoring")
    print("="*50)
    
    try:
        agent = AssessmentAgent()
        
        responses = [
            # Completely correct answer
            StudentResponse(
                question_id="partial_001",
                student_answer="Photosynthesis is the process by which plants make food using sunlight, water, and carbon dioxide",
                question_text="Explain what photosynthesis is",
                correct_answer="Photosynthesis is the process by which plants make food using sunlight, water, and carbon dioxide",
                question_type=QuestionType.SHORT_ANSWER
            ),
            # Partially correct answer (missing some details)
            StudentResponse(
                question_id="partial_002",
                student_answer="Plants use sunlight to make food",
                question_text="Explain what photosynthesis is",
                correct_answer="Photosynthesis is the process by which plants make food using sunlight, water, and carbon dioxide",
                question_type=QuestionType.SHORT_ANSWER
            ),
            # Incorrect answer
            StudentResponse(
                question_id="partial_003",
                student_answer="Purple elephants fly",
                question_text="Explain what photosynthesis is", 
                correct_answer="Photosynthesis is the process by which plants make food using sunlight, water, and carbon dioxide",
                question_type=QuestionType.SHORT_ANSWER
            )
        ]
        
        request = AssessmentRequest(
            student_id="partial_test_student",
            responses=responses,
            assessment_type=AssessmentType.FORMATIVE,
            feedback_level=FeedbackLevel.COMPREHENSIVE,
            score_type=ScoreType.PARTIAL,
            subject="Science",
            grade=4,
            topic="Plant Life Cycle"
        )
        
        result = await agent.assess_responses(request)
        
        print("Partial Credit Assessment Results:")
        for i, (response, feedback) in enumerate(zip(responses, result.feedback_items)):
            print(f"\n--- Response {i+1} ---")
            print(f"Student Answer: {response.student_answer}")
            print(f"Score: {feedback.score:.2f}")
            print(f"Is Correct: {feedback.is_correct}")
            print(f"Feedback: {feedback.feedback_text[:150]}...")
            
        print(f"\nOverall Performance:")
        print(f"  Overall Score: {result.performance_metrics.overall_score:.2%}")
        print(f"  Correct Answers: {result.performance_metrics.correct_answers}")
        print(f"  Partial Credit: {result.performance_metrics.partial_credit_answers}")
        print(f"  Incorrect: {result.performance_metrics.incorrect_answers}")
        
        # Verify different scoring levels
        assert result.feedback_items[0].score == 1.0  # Perfect answer
        assert 0.0 < result.feedback_items[1].score < 1.0  # Partial credit
        assert result.feedback_items[2].score == 0.0  # Incorrect answer
        
        print("[PASS] Partial Credit scoring test PASSED")
        return True
        
    except Exception as e:
        print(f"[FAIL] Partial Credit scoring test FAILED: {e}")
        return False


async def test_feedback_levels():
    """Test different feedback levels (basic, detailed, comprehensive)"""
    print("\n" + "="*50)
    print("Testing Different Feedback Levels")
    print("="*50)
    
    try:
        agent = AssessmentAgent()
        
        # Same response, different feedback levels
        base_response = StudentResponse(
            question_id="feedback_001",
            student_answer="5",
            question_text="What is 3 + 2?",
            correct_answer="5",
            question_type=QuestionType.SHORT_ANSWER
        )
        
        feedback_levels = [FeedbackLevel.BASIC, FeedbackLevel.DETAILED, FeedbackLevel.COMPREHENSIVE]
        
        for level in feedback_levels:
            request = AssessmentRequest(
                student_id="feedback_test_student",
                responses=[base_response],
                assessment_type=AssessmentType.FORMATIVE,
                feedback_level=level,
                subject="Mathematics",
                grade=1,
                topic="Addition up to 9"
            )
            
            result = await agent.assess_responses(request)
            feedback = result.feedback_items[0]
            
            print(f"\n--- {level.value.upper()} Feedback ---")
            print(f"Feedback Length: {len(feedback.feedback_text)} characters")
            print(f"Feedback: {feedback.feedback_text}")
            print(f"Improvement Suggestions: {len(feedback.improvement_suggestions)} items")
            
            # Basic should be shortest, comprehensive should be longest
            if level == FeedbackLevel.BASIC:
                assert len(feedback.feedback_text) < 100
            elif level == FeedbackLevel.COMPREHENSIVE:
                assert len(feedback.feedback_text) > 200
                assert len(feedback.improvement_suggestions) > 0
        
        print("[PASS] Feedback Levels test PASSED")
        return True
        
    except Exception as e:
        print(f"[FAIL] Feedback Levels test FAILED: {e}")
        return False


async def test_performance_metrics():
    """Test calculation of performance metrics"""
    print("\n" + "="*50)
    print("Testing Performance Metrics Calculation")
    print("="*50)
    
    try:
        agent = AssessmentAgent()
        
        # Create varied responses to test metrics
        responses = [
            # Correct answers
            StudentResponse(
                question_id="q1", student_answer="correct1", question_text="Question 1", 
                correct_answer="correct1", question_type=QuestionType.SHORT_ANSWER, time_taken=30
            ),
            StudentResponse(
                question_id="q2", student_answer="correct2", question_text="Question 2", 
                correct_answer="correct2", question_type=QuestionType.MCQ, time_taken=20
            ),
            # Partially correct
            StudentResponse(
                question_id="q3", student_answer="partial answer", question_text="Question 3", 
                correct_answer="complete answer with more detail", question_type=QuestionType.LONG_ANSWER, time_taken=90
            ),
            # Incorrect
            StudentResponse(
                question_id="q4", student_answer="wrong", question_text="Question 4", 
                correct_answer="right", question_type=QuestionType.TRUE_FALSE, time_taken=15
            ),
            StudentResponse(
                question_id="q5", student_answer="also wrong", question_text="Question 5", 
                correct_answer="correct", question_type=QuestionType.FILL_BLANK, time_taken=25
            )
        ]
        
        request = AssessmentRequest(
            student_id="metrics_test_student",
            responses=responses,
            assessment_type=AssessmentType.SUMMATIVE,
            feedback_level=FeedbackLevel.DETAILED,
            score_type=ScoreType.PARTIAL,
            subject="Mathematics",
            grade=3,
            topic="Place Value in 3-digit Numbers"
        )
        
        result = await agent.assess_responses(request)
        metrics = result.performance_metrics
        
        print("Performance Metrics:")
        print(f"  Total Questions: {metrics.total_questions}")
        print(f"  Correct Answers: {metrics.correct_answers}")
        print(f"  Partial Credit Answers: {metrics.partial_credit_answers}")
        print(f"  Incorrect Answers: {metrics.incorrect_answers}")
        print(f"  Overall Score: {metrics.overall_score:.2%}")
        print(f"  Completion Time: {metrics.completion_time} seconds")
        print(f"  Subject Mastery Level: {metrics.subject_mastery_level}")
        
        print(f"\nStrengths:")
        for strength in metrics.strengths:
            print(f"  • {strength}")
            
        print(f"\nAreas for Improvement:")
        for area in metrics.areas_for_improvement:
            print(f"  • {area}")
            
        print(f"\nRecommended Next Topics:")
        for topic in metrics.recommended_next_topics:
            print(f"  • {topic}")
        
        # Verify calculations
        assert metrics.total_questions == 5
        assert metrics.correct_answers + metrics.partial_credit_answers + metrics.incorrect_answers == 5
        assert metrics.completion_time == 180  # Sum of all time_taken values
        assert 0.0 <= metrics.overall_score <= 1.0
        
        print("[PASS] Performance Metrics test PASSED")
        return True
        
    except Exception as e:
        print(f"[FAIL] Performance Metrics test FAILED: {e}")
        return False


async def test_learning_progress_tracking():
    """Test learning progress tracking over multiple assessments"""
    print("\n" + "="*50)
    print("Testing Learning Progress Tracking")
    print("="*50)
    
    try:
        agent = AssessmentAgent()
        
        # Simulate multiple assessment results over time
        assessment_results = []
        
        # First assessment (poor performance)
        responses1 = [
            StudentResponse(
                question_id="q1", student_answer="wrong1", question_text="Question 1", 
                correct_answer="correct1", question_type=QuestionType.SHORT_ANSWER
            ),
            StudentResponse(
                question_id="q2", student_answer="wrong2", question_text="Question 2", 
                correct_answer="correct2", question_type=QuestionType.SHORT_ANSWER
            )
        ]
        
        request1 = AssessmentRequest(
            student_id="progress_student",
            responses=responses1,
            assessment_type=AssessmentType.DIAGNOSTIC,
            feedback_level=FeedbackLevel.DETAILED,
            subject="Mathematics",
            grade=1,
            topic="Addition up to 9"
        )
        
        result1 = await agent.assess_responses(request1)
        assessment_results.append(result1)
        
        # Second assessment (improved performance)
        responses2 = [
            StudentResponse(
                question_id="q3", student_answer="correct1", question_text="Question 3", 
                correct_answer="correct1", question_type=QuestionType.SHORT_ANSWER
            ),
            StudentResponse(
                question_id="q4", student_answer="mostly correct answer", question_text="Question 4", 
                correct_answer="completely correct answer", question_type=QuestionType.SHORT_ANSWER
            )
        ]
        
        request2 = AssessmentRequest(
            student_id="progress_student",
            responses=responses2,
            assessment_type=AssessmentType.FORMATIVE,
            feedback_level=FeedbackLevel.DETAILED,
            subject="Mathematics",
            grade=1,
            topic="Addition up to 9"
        )
        
        result2 = await agent.assess_responses(request2)
        assessment_results.append(result2)
        
        # Track progress
        progress_tracking = await agent.track_learning_progress("progress_student", assessment_results)
        
        print("Learning Progress Tracking:")
        print(f"  Number of concepts tracked: {len(progress_tracking)}")
        
        for progress in progress_tracking:
            print(f"\n  Concept: {progress.concept}")
            print(f"    Mastery Level: {progress.mastery_level:.2%}")
            print(f"    Attempts: {progress.attempts_count}")
            print(f"    Improvement Rate: {progress.improvement_rate:.3f}")
            print(f"    Last Score: {progress.last_assessment_score:.2f}")
            print(f"    Recommended Practice Time: {progress.recommended_practice_time} minutes")
        
        # Verify progress tracking
        assert len(progress_tracking) > 0
        for progress in progress_tracking:
            assert 0.0 <= progress.mastery_level <= 1.0
            assert progress.attempts_count > 0
            assert progress.recommended_practice_time > 0
        
        print("[PASS] Learning Progress Tracking test PASSED")
        return True
        
    except Exception as e:
        print(f"[FAIL] Learning Progress Tracking test FAILED: {e}")
        return False


async def test_different_subjects():
    """Test assessment across different subjects"""
    print("\n" + "="*50)
    print("Testing Different Subjects Assessment")
    print("="*50)
    
    try:
        agent = AssessmentAgent()
        subjects_tested = 0
        
        # Test Mathematics
        math_response = StudentResponse(
            question_id="math_001",
            student_answer="The answer is 12 because 4 times 3 equals 12",
            question_text="What is 4 × 3?",
            correct_answer="12",
            question_type=QuestionType.SHORT_ANSWER
        )
        
        math_request = AssessmentRequest(
            student_id="subject_test_student",
            responses=[math_response],
            assessment_type=AssessmentType.FORMATIVE,
            feedback_level=FeedbackLevel.DETAILED,
            subject="Mathematics",
            grade=3,
            topic="Place Value in 3-digit Numbers"
        )
        
        math_result = await agent.assess_responses(math_request)
        print(f"--- Mathematics Assessment ---")
        print(f"Score: {math_result.performance_metrics.overall_score:.2%}")
        print(f"Mastery Level: {math_result.performance_metrics.subject_mastery_level}")
        subjects_tested += 1
        
        # Test Science  
        science_response = StudentResponse(
            question_id="science_001",
            student_answer="Animals have better hearing and smell than humans",
            question_text="How do animal senses compare to human senses?",
            correct_answer="Many animals have superior senses compared to humans, with enhanced hearing, smell, and other specialized abilities",
            question_type=QuestionType.LONG_ANSWER
        )
        
        science_request = AssessmentRequest(
            student_id="subject_test_student",
            responses=[science_response],
            assessment_type=AssessmentType.FORMATIVE,
            feedback_level=FeedbackLevel.DETAILED,
            subject="Science",
            grade=5,
            topic="Human Senses and Animal Senses"
        )
        
        science_result = await agent.assess_responses(science_request)
        print(f"--- Science Assessment ---")
        print(f"Score: {science_result.performance_metrics.overall_score:.2%}")
        print(f"Mastery Level: {science_result.performance_metrics.subject_mastery_level}")
        subjects_tested += 1
        
        # Test English
        english_response = StudentResponse(
            question_id="english_001",
            student_answer="The story is about a brave boy who helps others",
            question_text="What is the main theme of the story?",
            correct_answer="The story explores themes of courage, helping others, and growing up",
            question_type=QuestionType.SHORT_ANSWER
        )
        
        english_request = AssessmentRequest(
            student_id="subject_test_student", 
            responses=[english_response],
            assessment_type=AssessmentType.FORMATIVE,
            feedback_level=FeedbackLevel.DETAILED,
            subject="English",
            grade=2,
            topic="Simple Story Reading"
        )
        
        english_result = await agent.assess_responses(english_request)
        print(f"--- English Assessment ---")
        print(f"Score: {english_result.performance_metrics.overall_score:.2%}")
        print(f"Mastery Level: {english_result.performance_metrics.subject_mastery_level}")
        subjects_tested += 1
        
        print(f"\n[SUMMARY] Successfully tested {subjects_tested} subjects")
        assert subjects_tested == 3
        
        print("[PASS] Different Subjects assessment test PASSED")
        return True
        
    except Exception as e:
        print(f"[FAIL] Different Subjects assessment test FAILED: {e}")
        return False


async def run_all_tests():
    """Run all Assessment Agent tests"""
    print("RSP Education Agent V2 - Assessment Agent Test Suite")
    print("=" * 60)
    
    tests = [
        ("Agent Initialization", test_agent_initialization),
        ("Student Response Creation", test_student_response_creation),
        ("Assessment Request Creation", test_assessment_request_creation),
        ("Single Answer Assessment", test_single_answer_assessment),
        ("Multiple Choice Assessment", test_multiple_choice_assessment),
        ("Partial Credit Scoring", test_partial_credit_scoring),
        ("Feedback Levels", test_feedback_levels),
        ("Performance Metrics", test_performance_metrics),
        ("Learning Progress Tracking", test_learning_progress_tracking),
        ("Different Subjects", test_different_subjects)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n[TEST] Running {test_name} test...")
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"[ERROR] {test_name} test encountered an error: {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "="*60)
    print("ASSESSMENT AGENT TEST SUMMARY")
    print("="*60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{test_name:<30} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\nOverall: {passed}/{len(tests)} tests passed")
    
    if failed == 0:
        print("SUCCESS: All tests passed! Assessment Agent is working correctly.")
        print("\nASSESSMENT AGENT STATUS: READY FOR PRODUCTION")
    else:
        print(f"WARNING: {failed} test(s) failed. Please review and fix issues.")
    
    return failed == 0


if __name__ == "__main__":
    asyncio.run(run_all_tests())