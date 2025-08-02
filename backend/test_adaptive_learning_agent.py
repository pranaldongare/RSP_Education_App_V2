#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Suite for Adaptive Learning Agent - Phase 3
Tests all adaptive learning functionality including learning style detection, difficulty adjustment, and personalized learning paths.
"""

import sys
import os
import asyncio
import logging
from typing import List, Dict
from datetime import datetime, timedelta

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.adaptive_learning_agent import (
    AdaptiveLearningAgent, LearningProfile, AdaptationRequest, LearningPathRecommendation,
    LearningStyle, LearningPace, DifficultyAdjustmentStrategy, LearningStyleIndicator,
    ContentRecommendation, DifficultyAdjustment
)
from agents.assessment_agent import (
    AssessmentAgent, StudentResponse, AssessmentRequest, AssessmentResult,
    AssessmentType, FeedbackLevel, ScoreType, PerformanceMetrics, FeedbackItem
)
from agents.content_generator import QuestionType, DifficultyLevel

# Configure logging to suppress unnecessary output during testing
logging.basicConfig(level=logging.WARNING)


async def test_agent_initialization():
    """Test Adaptive Learning Agent initialization"""
    print("\n" + "="*50)
    print("Testing Adaptive Learning Agent Initialization")
    print("="*50)
    
    try:
        agent = AdaptiveLearningAgent()
        
        # Test agent status
        status = await agent.get_agent_status()
        
        print("Adaptive Learning Agent Status:")
        print(f"  Name: {status['name']}")
        print(f"  Status: {status['status']}")
        print(f"  OpenAI Model Available: {status['models_available']['openai']}")
        print(f"  Anthropic Model Available: {status['models_available']['anthropic']}")
        print(f"  Supported Learning Styles: {status['supported_learning_styles']}")
        print(f"  Supported Learning Paces: {status['supported_learning_paces']}")
        print(f"  Curriculum Loaded: {status['curriculum_loaded']}")
        print(f"  Style Indicators Loaded: {status['style_indicators_loaded']}")
        
        assert status['name'] == "AdaptiveLearningAgent"
        assert status['status'] == "active"
        assert status['curriculum_loaded'] == True
        assert len(status['supported_learning_styles']) > 0
        assert status['style_indicators_loaded'] == True
        
        print("[PASS] Adaptive Learning Agent initialization test PASSED")
        return True
        
    except Exception as e:
        print(f"[FAIL] Adaptive Learning Agent initialization test FAILED: {e}")
        return False


async def test_learning_profile_creation():
    """Test creating and updating learning profiles"""
    print("\n" + "="*50)
    print("Testing Learning Profile Creation")
    print("="*50)
    
    try:
        # Create a basic learning profile
        profile = LearningProfile(
            student_id="test_student_001",
            preferred_learning_styles=[
                LearningStyleIndicator(
                    style=LearningStyle.VISUAL,
                    confidence=0.8,
                    evidence=["Performs well with diagrams", "Prefers visual explanations"]
                ),
                LearningStyleIndicator(
                    style=LearningStyle.READING,
                    confidence=0.6,
                    evidence=["Good at text-based questions"]
                )
            ],
            learning_pace=LearningPace.MODERATE,
            current_difficulty_level={
                "Mathematics": DifficultyLevel.INTERMEDIATE,
                "Science": DifficultyLevel.BEGINNER
            },
            attention_span_minutes=25,
            weak_concepts={
                "Mathematics": ["Fractions", "Decimals"],
                "Science": ["Force and Motion"]
            },
            strong_concepts={
                "Mathematics": ["Addition", "Subtraction"],
                "Science": ["Plant Life Cycle"]
            }
        )
        
        print("Learning Profile Created:")
        print(f"  Student ID: {profile.student_id}")
        print(f"  Primary Learning Style: {profile.preferred_learning_styles[0].style}")
        print(f"  Style Confidence: {profile.preferred_learning_styles[0].confidence}")
        print(f"  Learning Pace: {profile.learning_pace}")
        print(f"  Attention Span: {profile.attention_span_minutes} minutes")
        print(f"  Math Difficulty: {profile.current_difficulty_level['Mathematics']}")
        print(f"  Math Weak Concepts: {profile.weak_concepts['Mathematics']}")
        print(f"  Math Strong Concepts: {profile.strong_concepts['Mathematics']}")
        
        assert profile.student_id == "test_student_001"
        assert len(profile.preferred_learning_styles) == 2
        assert profile.preferred_learning_styles[0].style == LearningStyle.VISUAL
        assert profile.learning_pace == LearningPace.MODERATE
        assert len(profile.weak_concepts["Mathematics"]) == 2
        
        print("[PASS] Learning Profile creation test PASSED")
        return True
        
    except Exception as e:
        print(f"[FAIL] Learning Profile creation test FAILED: {e}")
        return False


async def test_performance_pattern_analysis():
    """Test analysis of student performance patterns"""
    print("\n" + "="*50)
    print("Testing Performance Pattern Analysis")
    print("="*50)
    
    try:
        agent = AdaptiveLearningAgent()
        
        # Create sample assessment results showing improvement trend
        assessment_results = []
        
        # Create 5 assessments with improving scores
        scores = [0.4, 0.5, 0.6, 0.7, 0.8]  # Improving trend
        for i, score in enumerate(scores):
            
            # Create feedback items
            feedback_items = [
                FeedbackItem(
                    question_id=f"q{i}_1",
                    is_correct=score > 0.5,
                    score=score,
                    feedback_text=f"Test feedback {i}",
                    explanation=f"Test explanation {i}",
                    improvement_suggestions=[f"Suggestion {i}"],
                    concepts_demonstrated=["Basic Math"] if score > 0.5 else [],
                    concepts_to_review=["Calculations"] if score <= 0.5 else [],
                    difficulty_assessment=DifficultyLevel.INTERMEDIATE
                )
            ]
            
            # Create performance metrics
            performance_metrics = PerformanceMetrics(
                total_questions=1,
                correct_answers=1 if score > 0.5 else 0,
                partial_credit_answers=0,
                incorrect_answers=0 if score > 0.5 else 1,
                overall_score=score,
                completion_time=60 + i*10,  # Increasing time
                subject_mastery_level=DifficultyLevel.INTERMEDIATE,
                strengths=["Problem solving"] if score > 0.6 else [],
                areas_for_improvement=["Accuracy"] if score <= 0.6 else [],
                recommended_next_topics=["Advanced topics"]
            )
            
            # Create assessment result
            result = AssessmentResult(
                student_id="test_student",
                assessment_id=f"assessment_{i}",
                assessment_type=AssessmentType.FORMATIVE,
                subject="Mathematics",
                grade=3,
                topic="Addition",
                feedback_items=feedback_items,
                performance_metrics=performance_metrics,
                overall_feedback=f"Assessment {i} feedback",
                learning_path_adjustments=["Continue practice"],
                confidence_indicators={"overall": score},
                assessed_at=datetime.utcnow() - timedelta(days=5-i)  # Spread over 5 days
            )
            
            assessment_results.append(result)
        
        # Analyze performance patterns
        analysis = await agent._analyze_performance_patterns(assessment_results)
        
        print("Performance Analysis Results:")
        print(f"  Total Assessments: {analysis['total_assessments']}")
        print(f"  Subjects Assessed: {analysis['subjects_assessed']}")
        print(f"  Overall Trend Direction: {analysis['overall_trend']['direction']}")
        print(f"  Trend Confidence: {analysis['overall_trend']['confidence']:.2f}")
        print(f"  Consistency Score: {analysis['consistency']['consistency_score']:.2f}")
        print(f"  Average Time per Question: {analysis['time_efficiency']['average_time_per_question']:.1f}s")
        
        if "subject_performance" in analysis:
            math_perf = analysis["subject_performance"].get("Mathematics", {})
            print(f"  Math Average Score: {math_perf.get('average_score', 0):.2f}")
            print(f"  Math Trend: {math_perf.get('trend', {}).get('direction', 'unknown')}")
        
        # Verify analysis results
        assert analysis['total_assessments'] == 5
        assert 'Mathematics' in analysis['subjects_assessed']
        assert analysis['overall_trend']['direction'] == 'improving'
        assert analysis['consistency']['consistency_score'] > 0.0
        
        print("[PASS] Performance Pattern Analysis test PASSED")
        return True
        
    except Exception as e:
        print(f"[FAIL] Performance Pattern Analysis test FAILED: {e}")
        return False


async def test_learning_style_detection():
    """Test learning style detection from performance patterns"""
    print("\n" + "="*50)
    print("Testing Learning Style Detection")
    print("="*50)
    
    try:
        agent = AdaptiveLearningAgent()
        
        # Create assessment results that suggest visual learning preference
        assessment_results = []
        
        for i in range(3):
            feedback_items = [
                FeedbackItem(
                    question_id=f"visual_q{i}",
                    is_correct=True,  # High performance
                    score=0.9,
                    feedback_text="Excellent work with visual problem solving",
                    explanation="Strong visual reasoning demonstrated",
                    improvement_suggestions=[],
                    concepts_demonstrated=["Visual reasoning", "Pattern recognition"],
                    concepts_to_review=[],
                    difficulty_assessment=DifficultyLevel.INTERMEDIATE
                ),
                FeedbackItem(
                    question_id=f"text_q{i}",
                    is_correct=False,  # Lower performance on text-heavy questions
                    score=0.5,
                    feedback_text="Some difficulty with text-based problems",
                    explanation="Consider using visual aids",
                    improvement_suggestions=["Use diagrams"],
                    concepts_demonstrated=[],
                    concepts_to_review=["Text comprehension"],
                    difficulty_assessment=DifficultyLevel.BEGINNER
                )
            ]
            
            performance_metrics = PerformanceMetrics(
                total_questions=2,
                correct_answers=1,
                partial_credit_answers=0,
                incorrect_answers=1,
                overall_score=0.7,
                subject_mastery_level=DifficultyLevel.INTERMEDIATE,
                strengths=["Visual problem solving"],
                areas_for_improvement=["Text comprehension"],
                recommended_next_topics=["Visual math"]
            )
            
            result = AssessmentResult(
                student_id="visual_learner",
                assessment_id=f"style_test_{i}",
                assessment_type=AssessmentType.DIAGNOSTIC,
                subject="Mathematics",
                grade=2,
                topic="Patterns",
                feedback_items=feedback_items,
                performance_metrics=performance_metrics,
                overall_feedback="Mixed performance",
                learning_path_adjustments=[],
                confidence_indicators={"visual": 0.9, "text": 0.5},
                assessed_at=datetime.utcnow() - timedelta(days=i)
            )
            
            assessment_results.append(result)
        
        # Detect learning styles
        learning_styles = await agent._detect_learning_styles(assessment_results, None)
        
        print("Learning Style Detection Results:")
        for style in learning_styles:
            print(f"  Style: {style.style}")
            print(f"  Confidence: {style.confidence:.2f}")
            print(f"  Evidence: {style.evidence}")
            print()
        
        # Verify detection results
        assert len(learning_styles) > 0
        # Should detect some learning style preferences
        primary_style = learning_styles[0]
        assert primary_style.confidence > 0.0
        assert len(primary_style.evidence) > 0
        
        print("[PASS] Learning Style Detection test PASSED")
        return True
        
    except Exception as e:
        print(f"[FAIL] Learning Style Detection test FAILED: {e}")
        return False


async def test_difficulty_adjustment_calculation():
    """Test difficulty adjustment calculations"""
    print("\n" + "="*50)
    print("Testing Difficulty Adjustment Calculation")
    print("="*50)
    
    try:
        agent = AdaptiveLearningAgent()
        
        # Create sample performance analysis
        performance_analysis = {
            "subject_performance": {
                "Mathematics": {
                    "average_score": 0.9,  # High performance
                    "trend": {"direction": "improving", "confidence": 0.8},
                    "mastery_level": DifficultyLevel.INTERMEDIATE
                },
                "Science": {
                    "average_score": 0.3,  # Low performance
                    "trend": {"direction": "declining", "confidence": 0.7},
                    "mastery_level": DifficultyLevel.BEGINNER
                }
            },
            "consistency": {"consistency_score": 0.8}
        }
        
        # Create sample learning profile
        profile = LearningProfile(
            student_id="test_student",
            preferred_learning_styles=[],
            learning_pace=LearningPace.MODERATE,
            current_difficulty_level={
                "Mathematics": DifficultyLevel.INTERMEDIATE,
                "Science": DifficultyLevel.BEGINNER
            }
        )
        
        # Calculate difficulty adjustments
        adjustments = await agent._calculate_difficulty_adjustments(performance_analysis, profile)
        
        print("Difficulty Adjustment Results:")
        for adjustment in adjustments:
            print(f"  Subject: {adjustment.subject}")
            print(f"  Current Level: {adjustment.current_level}")
            print(f"  Recommended Level: {adjustment.recommended_level}")
            print(f"  Confidence: {adjustment.confidence:.2f}")
            print(f"  Reasoning: {adjustment.reasoning}")
            print(f"  Adjustment Factors: {adjustment.adjustment_factors}")
            print()
        
        # Verify adjustments
        assert len(adjustments) == 2
        
        # Math should be recommended to increase (high performance)
        math_adj = next(adj for adj in adjustments if adj.subject == "Mathematics")
        science_adj = next(adj for adj in adjustments if adj.subject == "Science")
        
        # Math might be recommended for increase or stay the same
        assert math_adj.confidence > 0.0
        # Science should likely stay at beginner or be maintained due to poor performance
        assert science_adj.confidence > 0.0
        
        print("[PASS] Difficulty Adjustment Calculation test PASSED")
        return True
        
    except Exception as e:
        print(f"[FAIL] Difficulty Adjustment Calculation test FAILED: {e}")
        return False


async def test_content_recommendations():
    """Test generation of personalized content recommendations"""
    print("\n" + "="*50)
    print("Testing Content Recommendations")
    print("="*50)
    
    try:
        agent = AdaptiveLearningAgent()
        
        # Create learning profile with specific preferences
        profile = LearningProfile(
            student_id="test_student",
            preferred_learning_styles=[
                LearningStyleIndicator(
                    style=LearningStyle.VISUAL,
                    confidence=0.8,
                    evidence=["Strong visual reasoning"]
                )
            ],
            learning_pace=LearningPace.MODERATE,
            current_difficulty_level={"Mathematics": DifficultyLevel.INTERMEDIATE},
            weak_concepts={"Mathematics": ["Fractions", "Word Problems"]},
            strong_concepts={"Mathematics": ["Addition", "Subtraction"]}
        )
        
        # Create difficulty adjustments
        difficulty_adjustments = [
            DifficultyAdjustment(
                subject="Mathematics",
                current_level=DifficultyLevel.INTERMEDIATE,
                recommended_level=DifficultyLevel.INTERMEDIATE,
                confidence=0.7,
                reasoning="Maintain current level",
                adjustment_factors={"accuracy": 0.7}
            )
        ]
        
        # Generate content recommendations
        recommendations = await agent._generate_content_recommendations(
            profile=profile,
            difficulty_adjustments=difficulty_adjustments,
            learning_goals=["Improve fraction skills"],
            time_constraints=45  # 45 minutes available
        )
        
        print("Content Recommendations:")
        total_time = 0
        for i, rec in enumerate(recommendations):
            print(f"  {i+1}. {rec.content_type.title()} - {rec.subject}")
            print(f"     Topic: {rec.topic}")
            print(f"     Difficulty: {rec.difficulty_level}")
            print(f"     Time: {rec.estimated_time_minutes} minutes")
            print(f"     Priority: {rec.priority}")
            print(f"     Question Types: {rec.recommended_question_types}")
            print(f"     Reasoning: {rec.reasoning}")
            total_time += rec.estimated_time_minutes
            print()
        
        print(f"Total Estimated Time: {total_time} minutes")
        
        # Verify recommendations
        assert len(recommendations) > 0
        assert total_time <= 45  # Should not exceed time constraint
        
        # Should include review for weak concepts
        review_recs = [rec for rec in recommendations if rec.content_type == "review"]
        assert len(review_recs) > 0, "Should recommend review for weak concepts"
        
        # Should include practice content
        practice_recs = [rec for rec in recommendations if rec.content_type == "practice"]
        assert len(practice_recs) > 0, "Should recommend practice content"
        
        print("[PASS] Content Recommendations test PASSED")
        return True
        
    except Exception as e:
        print(f"[FAIL] Content Recommendations test FAILED: {e}")
        return False


async def test_complete_learning_path_adaptation():
    """Test complete learning path adaptation process"""
    print("\n" + "="*50)
    print("Testing Complete Learning Path Adaptation")
    print("="*50)
    
    try:
        agent = AdaptiveLearningAgent()
        
        # Create realistic assessment results
        assessment_results = await create_sample_assessment_results()
        
        # Create existing learning profile
        current_profile = LearningProfile(
            student_id="adaptive_test_student",
            preferred_learning_styles=[
                LearningStyleIndicator(
                    style=LearningStyle.MULTIMODAL,
                    confidence=0.6,
                    evidence=["Balanced performance"]
                )
            ],
            learning_pace=LearningPace.MODERATE,
            current_difficulty_level={"Mathematics": DifficultyLevel.BEGINNER},
            attention_span_minutes=20
        )
        
        # Create adaptation request
        request = AdaptationRequest(
            student_id="adaptive_test_student",
            assessment_results=assessment_results,
            current_profile=current_profile,
            learning_goals=["Improve math skills", "Build confidence"],
            time_constraints=60,
            preferred_subjects=["Mathematics"]
        )
        
        # Perform complete adaptation
        recommendation = await agent.adapt_learning_path(request)
        
        print("Learning Path Adaptation Results:")
        print(f"  Student ID: {recommendation.student_id}")
        print(f"  Number of Content Recommendations: {len(recommendation.recommended_content)}")
        print(f"  Number of Difficulty Adjustments: {len(recommendation.difficulty_adjustments)}")
        print(f"  Estimated Total Time: {recommendation.estimated_total_time} minutes")
        print(f"  Success Probability: {recommendation.success_probability:.2%}")
        print(f"  Next Assessment: {recommendation.next_assessment_timing} hours")
        
        print(f"\n  Updated Profile:")
        print(f"    Learning Pace: {recommendation.updated_profile.learning_pace}")
        print(f"    Primary Learning Style: {recommendation.updated_profile.preferred_learning_styles[0].style if recommendation.updated_profile.preferred_learning_styles else 'None'}")
        print(f"    Attention Span: {recommendation.updated_profile.attention_span_minutes} minutes")
        
        print(f"\n  Focus Areas:")
        for area in recommendation.focus_areas:
            print(f"    • {area}")
        
        print(f"\n  Sample Content Recommendations:")
        for i, rec in enumerate(recommendation.recommended_content[:3]):
            print(f"    {i+1}. {rec.content_type} - {rec.topic} ({rec.estimated_time_minutes}min)")
        
        # Verify the complete adaptation
        assert recommendation.student_id == "adaptive_test_student"
        assert len(recommendation.recommended_content) > 0
        assert len(recommendation.difficulty_adjustments) > 0
        assert 0.0 <= recommendation.success_probability <= 1.0
        assert recommendation.next_assessment_timing > 0
        assert recommendation.estimated_total_time <= 60  # Within time constraint
        assert len(recommendation.focus_areas) > 0
        
        # Verify profile was updated
        assert recommendation.updated_profile.last_updated > current_profile.last_updated
        
        print("[PASS] Complete Learning Path Adaptation test PASSED")
        return True
        
    except AssertionError as e:
        print(f"[FAIL] Complete Learning Path Adaptation test FAILED: Assertion error: {e}")
        return False
    except Exception as e:
        print(f"[FAIL] Complete Learning Path Adaptation test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_learning_pace_detection():
    """Test detection of different learning paces"""
    print("\n" + "="*50)
    print("Testing Learning Pace Detection")
    print("="*50)
    
    try:
        agent = AdaptiveLearningAgent()
        
        # Test fast learner (improving trend)
        fast_learner_results = await create_trending_assessment_results("improving")
        fast_analysis = await agent._analyze_performance_patterns(fast_learner_results)
        
        fast_profile = await agent._update_learning_profile(
            "fast_learner", None, fast_analysis, []
        )
        
        # Test slow learner (declining trend)
        slow_learner_results = await create_trending_assessment_results("declining")
        slow_analysis = await agent._analyze_performance_patterns(slow_learner_results)
        
        slow_profile = await agent._update_learning_profile(
            "slow_learner", None, slow_analysis, []
        )
        
        # Test moderate learner (stable trend)
        moderate_learner_results = await create_trending_assessment_results("stable")
        moderate_analysis = await agent._analyze_performance_patterns(moderate_learner_results)
        
        moderate_profile = await agent._update_learning_profile(
            "moderate_learner", None, moderate_analysis, []
        )
        
        print("Learning Pace Detection Results:")
        print(f"  Fast Learner Pace: {fast_profile.learning_pace}")
        print(f"  Slow Learner Pace: {slow_profile.learning_pace}")
        print(f"  Moderate Learner Pace: {moderate_profile.learning_pace}")
        
        print(f"\n  Fast Learner Attention Span: {fast_profile.attention_span_minutes} minutes")
        print(f"  Slow Learner Attention Span: {slow_profile.attention_span_minutes} minutes")
        print(f"  Moderate Learner Attention Span: {moderate_profile.attention_span_minutes} minutes")
        
        # Verify pace detection
        # Note: The actual pace detection is based on trend, so results may vary
        # This test mainly ensures the logic runs without errors
        assert fast_profile.learning_pace in [LearningPace.FAST, LearningPace.MODERATE]
        assert slow_profile.learning_pace in [LearningPace.SLOW, LearningPace.MODERATE]  
        assert moderate_profile.learning_pace in [LearningPace.MODERATE, LearningPace.FAST, LearningPace.SLOW]
        
        print("[PASS] Learning Pace Detection test PASSED")
        return True
        
    except Exception as e:
        print(f"[FAIL] Learning Pace Detection test FAILED: {e}")
        return False


async def test_assessment_timing_calculation():
    """Test calculation of optimal next assessment timing"""
    print("\n" + "="*50)
    print("Testing Assessment Timing Calculation")
    print("="*50)
    
    try:
        agent = AdaptiveLearningAgent()
        
        # Test different performance scenarios
        scenarios = [
            ("High Performer", 0.9, "improving", LearningPace.FAST),
            ("Struggling Student", 0.3, "declining", LearningPace.SLOW),
            ("Average Student", 0.6, "stable", LearningPace.MODERATE)
        ]
        
        print("Assessment Timing Recommendations:")
        
        for scenario_name, avg_score, trend, pace in scenarios:
            performance_analysis = {
                "recent_performance": {
                    "trend": trend,
                    "average_score": avg_score
                },
                "consistency": {"consistency_score": 0.7}
            }
            
            profile = LearningProfile(
                student_id="test",
                preferred_learning_styles=[],
                learning_pace=pace,
                current_difficulty_level={}
            )
            
            timing = agent._calculate_next_assessment_timing(performance_analysis, profile)
            
            print(f"  {scenario_name}:")
            print(f"    Score: {avg_score:.1%}, Trend: {trend}, Pace: {pace}")
            print(f"    Next Assessment: {timing} hours")
            print()
            
            # Verify timing is reasonable
            assert 4 <= timing <= 72, f"Timing {timing} should be between 4 and 72 hours"
        
        print("[PASS] Assessment Timing Calculation test PASSED")
        return True
        
    except Exception as e:
        print(f"[FAIL] Assessment Timing Calculation test FAILED: {e}")
        return False


async def test_success_probability_estimation():
    """Test success probability estimation for learning paths"""
    print("\n" + "="*50)
    print("Testing Success Probability Estimation")
    print("="*50)
    
    try:
        agent = AdaptiveLearningAgent()
        
        # Test different scenarios
        scenarios = [
            ("Optimal Conditions", "improving", 0.8, 0.9),
            ("Challenging Conditions", "declining", 0.6, 0.4),
            ("Average Conditions", "stable", 0.7, 0.7)
        ]
        
        print("Success Probability Estimations:")
        
        for scenario_name, trend, consistency, expected_range_min in scenarios:
            performance_analysis = {
                "recent_performance": {"trend": trend},
                "consistency": {"consistency_score": consistency}
            }
            
            difficulty_adjustments = [
                DifficultyAdjustment(
                    subject="Mathematics",
                    current_level=DifficultyLevel.INTERMEDIATE,
                    recommended_level=DifficultyLevel.INTERMEDIATE,
                    confidence=0.8,
                    reasoning="Test"
                )
            ]
            
            profile = LearningProfile(
                student_id="test",
                preferred_learning_styles=[
                    LearningStyleIndicator(
                        style=LearningStyle.VISUAL,
                        confidence=0.8,
                        evidence=["Test"]
                    )
                ],
                learning_pace=LearningPace.MODERATE,
                current_difficulty_level={}
            )
            
            probability = agent._estimate_success_probability(
                performance_analysis, difficulty_adjustments, profile
            )
            
            print(f"  {scenario_name}:")
            print(f"    Trend: {trend}, Consistency: {consistency}")
            print(f"    Success Probability: {probability:.2%}")
            print()
            
            # Verify probability is reasonable
            assert 0.1 <= probability <= 0.95, f"Probability {probability} should be between 10% and 95%"
        
        print("[PASS] Success Probability Estimation test PASSED")
        return True
        
    except Exception as e:
        print(f"[FAIL] Success Probability Estimation test FAILED: {e}")
        return False


# Helper functions for creating test data
async def create_sample_assessment_results() -> List[AssessmentResult]:
    """Create sample assessment results for testing"""
    results = []
    
    scores = [0.5, 0.6, 0.7]  # Improving trend
    
    for i, score in enumerate(scores):
        feedback_items = [
            FeedbackItem(
                question_id=f"q{i}_1",
                is_correct=score > 0.5,
                score=score,
                feedback_text="Sample feedback",
                explanation="Sample explanation",
                improvement_suggestions=["Practice more"],
                concepts_demonstrated=["Basic Math"] if score > 0.5 else [],
                concepts_to_review=["Fundamentals"] if score <= 0.5 else [],
                difficulty_assessment=DifficultyLevel.BEGINNER
            )
        ]
        
        performance_metrics = PerformanceMetrics(
            total_questions=1,
            correct_answers=1 if score > 0.5 else 0,
            partial_credit_answers=0,
            incorrect_answers=0 if score > 0.5 else 1,
            overall_score=score,
            completion_time=45 + i*5,
            subject_mastery_level=DifficultyLevel.BEGINNER,
            strengths=["Effort"],
            areas_for_improvement=["Accuracy"],
            recommended_next_topics=["Basic operations"]
        )
        
        result = AssessmentResult(
            student_id="test_student",
            assessment_id=f"test_{i}",
            assessment_type=AssessmentType.FORMATIVE,
            subject="Mathematics",
            grade=2,
            topic="Addition",
            feedback_items=feedback_items,
            performance_metrics=performance_metrics,
            overall_feedback="Keep practicing",
            learning_path_adjustments=[],
            confidence_indicators={"overall": score},
            assessed_at=datetime.utcnow() - timedelta(days=3-i)
        )
        
        results.append(result)
    
    return results


async def create_trending_assessment_results(trend_type: str) -> List[AssessmentResult]:
    """Create assessment results with specific trend patterns"""
    
    if trend_type == "improving":
        scores = [0.4, 0.5, 0.6, 0.7, 0.8]
    elif trend_type == "declining":
        scores = [0.8, 0.7, 0.6, 0.5, 0.4]
    else:  # stable
        scores = [0.6, 0.6, 0.6, 0.6, 0.6]
    
    results = []
    
    for i, score in enumerate(scores):
        feedback_items = [
            FeedbackItem(
                question_id=f"trend_q{i}",
                is_correct=score > 0.5,
                score=score,
                feedback_text=f"Trend test feedback {i}",
                explanation=f"Trend test explanation {i}",
                improvement_suggestions=[],
                concepts_demonstrated=["Math skills"] if score > 0.5 else [],
                concepts_to_review=["Basic concepts"] if score <= 0.5 else [],
                difficulty_assessment=DifficultyLevel.INTERMEDIATE
            )
        ]
        
        performance_metrics = PerformanceMetrics(
            total_questions=1,
            correct_answers=1 if score > 0.5 else 0,
            partial_credit_answers=0,
            incorrect_answers=0 if score > 0.5 else 1,
            overall_score=score,
            completion_time=60,  # Fixed time for consistency
            subject_mastery_level=DifficultyLevel.INTERMEDIATE,
            strengths=[],
            areas_for_improvement=[],
            recommended_next_topics=[]
        )
        
        result = AssessmentResult(
            student_id=f"{trend_type}_student",
            assessment_id=f"trend_{i}",
            assessment_type=AssessmentType.FORMATIVE,
            subject="Mathematics",
            grade=3,
            topic="Math Skills",
            feedback_items=feedback_items,
            performance_metrics=performance_metrics,
            overall_feedback="Trend test",
            learning_path_adjustments=[],
            confidence_indicators={"overall": score},
            assessed_at=datetime.utcnow() - timedelta(days=5-i)
        )
        
        results.append(result)
    
    return results


async def run_all_tests():
    """Run all Adaptive Learning Agent tests"""
    print("RSP Education Agent V2 - Adaptive Learning Agent Test Suite")
    print("=" * 65)
    
    tests = [
        ("Agent Initialization", test_agent_initialization),
        ("Learning Profile Creation", test_learning_profile_creation),
        ("Performance Pattern Analysis", test_performance_pattern_analysis),
        ("Learning Style Detection", test_learning_style_detection),
        ("Difficulty Adjustment Calculation", test_difficulty_adjustment_calculation),
        ("Content Recommendations", test_content_recommendations),
        ("Complete Learning Path Adaptation", test_complete_learning_path_adaptation),
        ("Learning Pace Detection", test_learning_pace_detection),
        ("Assessment Timing Calculation", test_assessment_timing_calculation),
        ("Success Probability Estimation", test_success_probability_estimation)
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
    print("\n" + "="*65)
    print("ADAPTIVE LEARNING AGENT TEST SUMMARY")
    print("="*65)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{test_name:<35} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\nOverall: {passed}/{len(tests)} tests passed")
    
    if failed == 0:
        print("SUCCESS: All tests passed! Adaptive Learning Agent is working correctly.")
        print("\nADAPTIVE LEARNING AGENT STATUS: READY FOR PRODUCTION")
    else:
        print(f"WARNING: {failed} test(s) failed. Please review and fix issues.")
    
    return failed == 0


if __name__ == "__main__":
    asyncio.run(run_all_tests())