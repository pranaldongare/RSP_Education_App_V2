#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Suite for Analytics Agent - Phase 4
Tests all learning analytics functionality including metrics calculation, insight generation, and predictive modeling.
"""

import sys
import os
import asyncio
import logging
from typing import List, Dict
from datetime import datetime, timedelta

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.analytics_agent import (
    AnalyticsAgent, AnalyticsRequest, AnalyticsReport, AnalyticsMetric,
    LearningInsight, SubjectAnalytics, LearningJourney, PredictiveModel,
    MetricType, AnalyticsTimeFrame, InsightType
)
from agents.assessment_agent import (
    AssessmentResult, StudentResponse, AssessmentType, FeedbackLevel, 
    ScoreType, PerformanceMetrics, FeedbackItem
)
from agents.content_generator import DifficultyLevel, QuestionType
from agents.adaptive_learning_agent import (
    LearningProfile, LearningStyle, LearningPace, LearningStyleIndicator
)
from agents.engagement_agent import (
    StudentEngagementProfile, EngagementLevel, MotivationType, EngagementEvent
)

# Configure logging to suppress unnecessary output during testing
logging.basicConfig(level=logging.WARNING)


async def test_agent_initialization():
    """Test Analytics Agent initialization"""
    print("\n" + "="*50)
    print("Testing Analytics Agent Initialization")
    print("="*50)
    
    try:
        agent = AnalyticsAgent()
        
        # Test agent status
        status = await agent.get_agent_status()
        
        print("Analytics Agent Status:")
        print(f"  Name: {status['name']}")
        print(f"  Status: {status['status']}")
        print(f"  OpenAI Model Available: {status['models_available']['openai']}")
        print(f"  Anthropic Model Available: {status['models_available']['anthropic']}")
        print(f"  Supported Metric Types: {status['supported_metric_types']}")
        print(f"  Supported Timeframes: {status['supported_timeframes']}")
        print(f"  Curriculum Loaded: {status['curriculum_loaded']}")
        print(f"  OpenAI Model Available: {status['models_available']['openai']}")
        print(f"  Anthropic Model Available: {status['models_available']['anthropic']}")
        
        assert status['name'] == "AnalyticsAgent"
        assert status['status'] == "active"
        assert status['curriculum_loaded'] == True
        assert len(status['supported_metric_types']) > 0
        assert status['models_available']['openai'] == True or status['models_available']['anthropic'] == True
        
        print("[PASS] Analytics Agent initialization test PASSED")
        return True
        
    except Exception as e:
        print(f"[FAIL] Analytics Agent initialization test FAILED: {e}")
        return False


async def test_metrics_calculation():
    """Test calculation of various learning metrics"""
    print("\n" + "="*50)
    print("Testing Metrics Calculation")
    print("="*50)
    
    try:
        agent = AnalyticsAgent()
        
        # Create sample assessment results with performance trend
        assessment_results = await create_sample_assessment_results()
        
        # Create sample learning profile
        learning_profile = create_sample_learning_profile()
        
        # Calculate different types of metrics
        metric_types = [MetricType.PERFORMANCE, MetricType.ENGAGEMENT, MetricType.LEARNING_PACE]
        
        metrics = await agent._calculate_key_metrics(
            student_id="test_student",
            assessment_results=assessment_results,
            learning_profile=learning_profile,
            engagement_profile=None,
            timeframe=AnalyticsTimeFrame.MONTHLY,
            metric_types=metric_types
        )
        
        print("Calculated Metrics:")
        for metric in metrics:
            print(f"  {metric.metric_type}: {metric.value:.3f}")
            print(f"    Label: {metric.metric_name}")
            print(f"    Description: {metric.description}")
            if metric.trend_direction:
                print(f"    Trend: {metric.trend_direction}")
            print()
        
        # Verify metrics
        assert len(metrics) >= 3
        performance_metrics = [m for m in metrics if m.metric_type == MetricType.PERFORMANCE]
        assert len(performance_metrics) > 0
        
        # Check metric values are reasonable
        for metric in metrics:
            assert 0.0 <= metric.value <= 100.0, f"Metric value {metric.value} out of range"
            assert len(metric.metric_name) > 0
            assert len(metric.description) > 0
        
        print("[PASS] Metrics Calculation test PASSED")
        return True
        
    except Exception as e:
        print(f"[FAIL] Metrics Calculation test FAILED: {e}")
        return False


async def test_insight_generation():
    """Test generation of learning insights"""
    print("\n" + "="*50)
    print("Testing Insight Generation")
    print("="*50)
    
    try:
        agent = AnalyticsAgent()
        
        # Create sample metrics
        metrics = [
            AnalyticsMetric(
                metric_id="perf_001",
                metric_name="Overall Performance",
                metric_type=MetricType.PERFORMANCE,
                value=85.5,
                timeframe=AnalyticsTimeFrame.WEEKLY,
                trend_direction="improving",
                benchmark_comparison=75.0,
                percentile_rank=75
            ),
            AnalyticsMetric(
                metric_id="eng_001",
                metric_name="Engagement Level",
                metric_type=MetricType.ENGAGEMENT,
                value=72.0,
                timeframe=AnalyticsTimeFrame.WEEKLY,
                trend_direction="stable",
                benchmark_comparison=60.0,
                percentile_rank=60
            ),
            AnalyticsMetric(
                metric_id="pace_001",
                metric_name="Learning Pace",
                metric_type=MetricType.LEARNING_PACE,
                value=90.0,
                timeframe=AnalyticsTimeFrame.WEEKLY,
                trend_direction="improving",
                benchmark_comparison=80.0,
                percentile_rank=80
            )
        ]
        
        # Create sample learning profile
        learning_profile = create_sample_learning_profile()
        
        # Generate insights
        insights = await agent._generate_insights(
            metrics=metrics,
            learning_profile=learning_profile,
            engagement_profile=None
        )
        
        print("Generated Insights:")
        for insight in insights:
            print(f"  {insight.insight_type}: {insight.title}")
            print(f"    Description: {insight.description}")
            print(f"    Confidence: {insight.confidence:.2f}")
            print(f"    Severity: {insight.severity}")
            if insight.recommendations:
                print(f"    Recommendations: {insight.recommendations}")
            print()
        
        # Verify insights
        assert len(insights) > 0
        
        # Check for different types of insights
        insight_types = [insight.insight_type for insight in insights]
        assert InsightType.PERFORMANCE in insight_types or InsightType.LEARNING_PATTERN in insight_types
        
        # Verify insight quality
        for insight in insights:
            assert 0.0 <= insight.confidence <= 1.0
            assert 1 <= insight.severity <= 5
            assert len(insight.title) > 0
            assert len(insight.description) > 0
        
        print("[PASS] Insight Generation test PASSED")
        return True
        
    except Exception as e:
        print(f"[FAIL] Insight Generation test FAILED: {e}")
        return False


async def test_subject_analytics():
    """Test subject-specific analytics"""
    print("\n" + "="*50)
    print("Testing Subject Analytics")
    print("="*50)
    
    try:
        agent = AnalyticsAgent()
        
        # Create subject-specific assessment results
        math_results = await create_subject_assessment_results("Mathematics", [0.6, 0.7, 0.8, 0.85])
        science_results = await create_subject_assessment_results("Science", [0.5, 0.6, 0.5, 0.7])
        
        all_results = math_results + science_results
        
        # Perform subject analytics
        subject_analytics = await agent._perform_subject_analytics(all_results)
        
        print("Subject Analytics:")
        for subject, analytics in subject_analytics.items():
            print(f"  {subject}:")
            print(f"    Average Score: {analytics.average_score:.2f}")
            print(f"    Mastery Level: {analytics.mastery_level}")
            print(f"    Progress Trend: {analytics.progress_trend}")
            print(f"    Time Spent: {analytics.time_spent_minutes} minutes")
            print(f"    Strengths: {analytics.strengths}")
            print(f"    Weaknesses: {analytics.weaknesses}")
            print(f"    Next Recommendations: {analytics.next_recommendations}")
            print()
        
        # Verify analytics
        assert len(subject_analytics) == 2
        assert "Mathematics" in subject_analytics
        assert "Science" in subject_analytics
        
        # Check mathematics analytics
        math_analytics = subject_analytics["Mathematics"]
        assert math_analytics.average_score > 0.6  # Should show good performance
        assert math_analytics.performance_trend == "improving"  # Should show improvement
        
        # Check science analytics
        science_analytics = subject_analytics["Science"]
        assert science_analytics.average_score > 0.0
        
        print("[PASS] Subject Analytics test PASSED")
        return True
        
    except Exception as e:
        print(f"[FAIL] Subject Analytics test FAILED: {e}")
        return False


async def test_learning_journey_tracking():
    """Test learning journey visualization and tracking"""
    print("\n" + "="*50)
    print("Testing Learning Journey Tracking")
    print("="*50)
    
    try:
        agent = AnalyticsAgent()
        
        # Create assessment results over time
        assessment_results = await create_time_series_assessment_results()
        
        # Create learning journey
        learning_journey = await agent._create_learning_journey(
            student_id="journey_student",
            assessment_results=assessment_results,
            timeframe=AnalyticsTimeFrame.QUARTERLY
        )
        
        print("Learning Journey:")
        print(f"  Student: {learning_journey.student_id}")
        print(f"  Timeframe: {learning_journey.timeframe}")
        print(f"  Total Sessions: {learning_journey.total_learning_sessions}")
        print(f"  Total Time: {learning_journey.total_time_spent_minutes} minutes")
        print(f"  Milestones Achieved: {learning_journey.milestones_achieved}")
        print(f"  Overall Progress: {learning_journey.overall_progress_percentage:.1f}%")
        
        print("\n  Key Milestones:")
        for milestone in learning_journey.key_milestones[:5]:
            print(f"    • {milestone}")
        
        print("\n  Progress Timeline (sample points):")
        for point in learning_journey.progress_timeline[:5]:
            print(f"    {point['date']}: {point['subject']} - {point['score']:.2f}")
        
        # Verify learning journey
        assert learning_journey.student_id == "journey_student"
        assert learning_journey.total_learning_sessions > 0
        assert learning_journey.total_time_spent_minutes > 0
        assert 0.0 <= learning_journey.overall_progress_percentage <= 100.0
        assert len(learning_journey.progress_timeline) > 0
        assert len(learning_journey.key_milestones) > 0
        
        print("[PASS] Learning Journey Tracking test PASSED")
        return True
        
    except Exception as e:
        print(f"[FAIL] Learning Journey Tracking test FAILED: {e}")
        return False


async def test_predictive_modeling():
    """Test predictive modeling for student outcomes"""
    print("\n" + "="*50)
    print("Testing Predictive Modeling")
    print("="*50)
    
    try:
        agent = AnalyticsAgent()
        
        # Create assessment results and learning profile
        assessment_results = await create_sample_assessment_results()
        learning_profile = create_sample_learning_profile()
        
        # Generate predictive models
        predictive_models = await agent._build_predictive_models(
            assessment_results=assessment_results,
            learning_profile=learning_profile,
            engagement_profile=None
        )
        
        print("Predictive Models:")
        for model in predictive_models:
            print(f"  {model.model_type}:")
            print(f"    Prediction: {model.prediction:.3f}")
            print(f"    Confidence: {model.confidence:.3f}")
            print(f"    Time Horizon: {model.time_horizon_days} days")
            print(f"    Key Factors: {model.key_factors}")
            if model.recommendations:
                print(f"    Recommendations: {model.recommendations[:2]}")  # First 2
            print()
        
        # Verify models
        assert len(predictive_models) > 0
        
        # Check for different model types
        model_types = [model.model_type for model in predictive_models]
        expected_types = ["performance_prediction", "engagement_prediction"]
        assert any(t in model_types for t in expected_types)
        
        # Verify model quality
        for model in predictive_models:
            assert 0.0 <= model.prediction <= 1.0
            assert 0.0 <= model.confidence <= 1.0
            assert model.time_horizon_days > 0
            assert len(model.key_factors) > 0
        
        print("[PASS] Predictive Modeling test PASSED")
        return True
        
    except Exception as e:
        print(f"[FAIL] Predictive Modeling test FAILED: {e}")
        return False


async def test_peer_comparison():
    """Test peer comparison analytics"""
    print("\n" + "="*50)
    print("Testing Peer Comparison")
    print("="*50)
    
    try:
        agent = AnalyticsAgent()
        
        # Create test metrics
        test_metrics = [
            AnalyticsMetric(
                metric_id="math_perf_001",
                metric_name="Math Performance",
                metric_type=MetricType.PERFORMANCE,
                value=78.5,
                description="Mathematics average score",
                timeframe=AnalyticsTimeFrame.MONTHLY
            ),
            AnalyticsMetric(
                metric_id="eng_001",
                metric_name="Engagement Score",
                metric_type=MetricType.ENGAGEMENT,
                value=85.0,
                description="Overall engagement level",
                timeframe=AnalyticsTimeFrame.MONTHLY
            )
        ]
        
        # Perform peer comparison
        compared_metrics = await agent._perform_peer_comparison(
            student_metrics=test_metrics,
            grade=3,
            timeframe=AnalyticsTimeFrame.MONTHLY
        )
        
        print("Peer Comparison Results:")
        for metric in compared_metrics:
            print(f"  {metric.metric_name}:")
            print(f"    Student Value: {metric.value:.2f}")
            print(f"    Percentile: {metric.percentile_rank:.1f}")
            print(f"    Description: {metric.description}")
            print()
        
        # Verify comparison results
        assert len(compared_metrics) == 2
        
        for metric in compared_metrics:
            assert hasattr(metric, 'percentile_rank')
            assert metric.percentile_rank is not None
            assert 0.0 <= metric.percentile_rank <= 100.0
        
        print("[PASS] Peer Comparison test PASSED")
        return True
        
    except Exception as e:
        print(f"[FAIL] Peer Comparison test FAILED: {e}")
        return False


async def test_complete_analytics_report():
    """Test complete analytics report generation"""
    print("\n" + "="*50)
    print("Testing Complete Analytics Report Generation")
    print("="*50)
    
    try:
        agent = AnalyticsAgent()
        
        # Create comprehensive test data
        assessment_results = await create_sample_assessment_results()
        learning_profile = create_sample_learning_profile()
        engagement_profile = create_sample_engagement_profile()
        
        # Create analytics request
        request = AnalyticsRequest(
            student_id="analytics_test_student",
            assessment_results=assessment_results,
            learning_profile=learning_profile,
            engagement_profile=engagement_profile,
            timeframe=AnalyticsTimeFrame.MONTHLY,
            requested_metrics=[MetricType.PERFORMANCE, MetricType.ENGAGEMENT, MetricType.LEARNING_PACE],
            include_predictions=True,
            include_peer_comparison=True
        )
        
        # Generate complete analytics report
        report = await agent.generate_analytics_report(request)
        
        print("Complete Analytics Report:")
        print(f"  Student ID: {report.student_id}")
        print(f"  Timeframe: {report.timeframe}")
        print(f"  Report Generated: {report.generated_at}")
        
        print(f"\n  Key Metrics ({len(report.key_metrics)} total):")
        for metric in report.key_metrics[:3]:
            print(f"    • {metric.metric_name}: {metric.value:.2f}")
        
        print(f"\n  Insights ({len(report.insights)} total):")
        for insight in report.insights[:3]:
            print(f"    • {insight.title} (confidence: {insight.confidence:.2f})")
        
        print(f"\n  Subject Analytics:")
        for subject, analytics in report.subject_analytics.items():
            print(f"    {subject}: {analytics.average_score:.2f} avg, {analytics.progress_trend}")
        
        print(f"\n  Learning Journey:")
        print(f"    Progress: {report.learning_journey.overall_progress_percentage:.1f}%")
        print(f"    Sessions: {report.learning_journey.total_learning_sessions}")
        print(f"    Time: {report.learning_journey.total_time_spent_minutes} min")
        
        print(f"\n  Predictive Models ({len(report.predictive_models)} total):")
        for model in report.predictive_models:
            print(f"    {model.model_type}: {model.prediction:.2f} (conf: {model.confidence:.2f})")
        
        # Verify complete report
        assert report.student_id == "analytics_test_student"
        assert report.timeframe == AnalyticsTimeFrame.LAST_MONTH
        assert len(report.key_metrics) >= 3
        assert len(report.insights) > 0
        assert len(report.subject_analytics) > 0
        assert report.learning_journey is not None
        assert len(report.predictive_models) > 0
        assert report.generated_at is not None
        
        # Verify data quality
        for metric in report.key_metrics:
            if metric.percentile_rank is not None:
                assert 0.0 <= metric.percentile_rank <= 100.0
        
        for insight in report.insights:
            assert 0.0 <= insight.confidence <= 1.0
            assert 1 <= insight.severity <= 5
        
        print("[PASS] Complete Analytics Report Generation test PASSED")
        return True
        
    except Exception as e:
        print(f"[FAIL] Complete Analytics Report Generation test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_trend_analysis():
    """Test trend analysis capabilities"""
    print("\n" + "="*50)
    print("Testing Trend Analysis")
    print("="*50)
    
    try:
        agent = AnalyticsAgent()
        
        # Test different trend patterns
        test_patterns = {
            "improving": [0.5, 0.6, 0.7, 0.8, 0.85],
            "declining": [0.8, 0.7, 0.6, 0.5, 0.4],
            "stable": [0.7, 0.7, 0.7, 0.7, 0.7],
            "volatile": [0.5, 0.8, 0.4, 0.9, 0.6]
        }
        
        print("Trend Analysis Results:")
        for pattern_name, scores in test_patterns.items():
            trend = await agent._analyze_trend(scores)
            
            print(f"  {pattern_name.title()} Pattern:")
            print(f"    Direction: {trend['trend_direction']}")
            print(f"    Slope: {trend['slope']:.4f}")
            print(f"    R-squared: {trend['r_squared']:.3f}")
            print()
        
        # Verify trend analysis
        improving_trend = await agent._analyze_trend(test_patterns["improving"])
        assert improving_trend["trend_direction"] == "improving"
        
        declining_trend = await agent._analyze_trend(test_patterns["declining"])
        assert declining_trend["trend_direction"] == "declining"
        
        stable_trend = await agent._analyze_trend(test_patterns["stable"])
        assert stable_trend["trend_direction"] == "stable"
        
        # Verify trend strength scores are reasonable
        for pattern_name, scores in test_patterns.items():
            trend = await agent._analyze_trend(scores)
            assert 0.0 <= trend["trend_strength"] <= 1.0
        
        print("[PASS] Trend Analysis test PASSED")
        return True
        
    except Exception as e:
        print(f"[FAIL] Trend Analysis test FAILED: {e}")
        return False


async def test_performance_recommendations():
    """Test performance-based recommendations"""
    print("\n" + "="*50)
    print("Testing Performance Recommendations")
    print("="*50)
    
    try:
        agent = AnalyticsAgent()
        
        # Create varied performance scenarios
        scenarios = [
            ("High Performer", 0.9, "stable"),
            ("Struggling Student", 0.4, "declining"),
            ("Improving Student", 0.6, "improving"),
            ("Inconsistent Performer", 0.7, "stable")
        ]
        
        print("Performance Recommendations:")
        
        for scenario_name, avg_performance, trend in scenarios:
            recommendations = agent._generate_performance_recommendations(
                average_performance=avg_performance,
                performance_trend=trend,
                subject_weaknesses=["Fractions", "Word Problems"],
                learning_style_preferences=[LearningStyle.VISUAL]
            )
            
            print(f"  {scenario_name}:")
            for rec in recommendations[:3]:  # Show top 3 recommendations
                print(f"    • {rec}")
            print()
        
        # Test specific scenario
        recommendations = agent._generate_performance_recommendations(
            average_performance=0.4,
            performance_trend="declining",
            subject_weaknesses=["Basic Math", "Problem Solving"],
            learning_style_preferences=[LearningStyle.VISUAL, LearningStyle.KINESTHETIC]
        )
        
        # Verify recommendations
        assert len(recommendations) > 0
        assert any("foundational" in rec.lower() or "basic" in rec.lower() for rec in recommendations)
        
        print("[PASS] Performance Recommendations test PASSED")
        return True
        
    except Exception as e:
        print(f"[FAIL] Performance Recommendations test FAILED: {e}")
        return False


# Helper functions for creating test data
async def create_sample_assessment_results() -> List[AssessmentResult]:
    """Create sample assessment results for testing"""
    results = []
    
    subjects = ["Mathematics", "Science", "English"]
    scores = [0.6, 0.7, 0.75, 0.8]  # Improving trend
    
    for i, score in enumerate(scores):
        subject = subjects[i % len(subjects)]
        
        feedback_items = [
            FeedbackItem(
                question_id=f"q{i}_1",
                is_correct=score > 0.6,
                score=score,
                feedback_text="Test feedback",
                explanation="Test explanation",
                improvement_suggestions=["Practice more"],
                concepts_demonstrated=["Basic concepts"] if score > 0.6 else [],
                concepts_to_review=["Fundamentals"] if score <= 0.6 else [],
                difficulty_assessment=DifficultyLevel.INTERMEDIATE
            )
        ]
        
        performance_metrics = PerformanceMetrics(
            total_questions=1,
            correct_answers=1 if score > 0.6 else 0,
            partial_credit_answers=0,
            incorrect_answers=0 if score > 0.6 else 1,
            overall_score=score,
            completion_time=60 + i*10,
            subject_mastery_level=DifficultyLevel.INTERMEDIATE,
            strengths=["Problem solving"] if score > 0.7 else [],
            areas_for_improvement=["Accuracy"] if score <= 0.7 else [],
            recommended_next_topics=["Advanced topics"]
        )
        
        result = AssessmentResult(
            student_id="test_student",
            assessment_id=f"test_{i}",
            assessment_type=AssessmentType.FORMATIVE,
            subject=subject,
            grade=3,
            topic=f"{subject} basics",
            feedback_items=feedback_items,
            performance_metrics=performance_metrics,
            overall_feedback="Keep practicing",
            learning_path_adjustments=[],
            confidence_indicators={"overall": score},
            assessed_at=datetime.utcnow() - timedelta(days=7-i*2)
        )
        
        results.append(result)
    
    return results


async def create_subject_assessment_results(subject: str, scores: List[float]) -> List[AssessmentResult]:
    """Create assessment results for a specific subject"""
    results = []
    
    for i, score in enumerate(scores):
        feedback_items = [
            FeedbackItem(
                question_id=f"{subject.lower()}_q{i}",
                is_correct=score > 0.5,
                score=score,
                feedback_text=f"{subject} feedback",
                explanation=f"{subject} explanation",
                improvement_suggestions=["Practice more"],
                concepts_demonstrated=[f"{subject} skills"] if score > 0.5 else [],
                concepts_to_review=["Basics"] if score <= 0.5 else [],
                difficulty_assessment=DifficultyLevel.INTERMEDIATE
            )
        ]
        
        performance_metrics = PerformanceMetrics(
            total_questions=1,
            correct_answers=1 if score > 0.5 else 0,
            partial_credit_answers=0,
            incorrect_answers=0 if score > 0.5 else 1,
            overall_score=score,
            completion_time=60,
            subject_mastery_level=DifficultyLevel.INTERMEDIATE,
            strengths=[],
            areas_for_improvement=[],
            recommended_next_topics=[]
        )
        
        result = AssessmentResult(
            student_id="subject_test_student",
            assessment_id=f"{subject.lower()}_{i}",
            assessment_type=AssessmentType.FORMATIVE,
            subject=subject,
            grade=3,
            topic=f"{subject} Topic {i+1}",
            feedback_items=feedback_items,
            performance_metrics=performance_metrics,
            overall_feedback=f"{subject} assessment {i+1}",
            learning_path_adjustments=[],
            confidence_indicators={"overall": score},
            assessed_at=datetime.utcnow() - timedelta(days=10-i*2)
        )
        
        results.append(result)
    
    return results


async def create_time_series_assessment_results() -> List[AssessmentResult]:
    """Create assessment results over time for journey tracking"""
    results = []
    
    subjects = ["Mathematics", "Science"]
    base_date = datetime.utcnow() - timedelta(days=30)
    
    for day in range(0, 30, 3):  # Every 3 days
        for subject in subjects:
            # Simulate improvement over time
            progress = day / 30.0
            score = 0.5 + (progress * 0.3)  # Improve from 50% to 80%
            
            feedback_items = [
                FeedbackItem(
                    question_id=f"journey_q{day}_{subject}",
                    is_correct=score > 0.6,
                    score=score,
                    feedback_text="Journey feedback",
                    explanation="Journey explanation",
                    improvement_suggestions=[],
                    concepts_demonstrated=[f"{subject} progress"],
                    concepts_to_review=[],
                    difficulty_assessment=DifficultyLevel.INTERMEDIATE
                )
            ]
            
            performance_metrics = PerformanceMetrics(
                total_questions=1,
                correct_answers=1 if score > 0.6 else 0,
                partial_credit_answers=0,
                incorrect_answers=0 if score > 0.6 else 1,
                overall_score=score,
                completion_time=45,
                subject_mastery_level=DifficultyLevel.INTERMEDIATE,
                strengths=[],
                areas_for_improvement=[],
                recommended_next_topics=[]
            )
            
            result = AssessmentResult(
                student_id="journey_student",
                assessment_id=f"journey_{day}_{subject}",
                assessment_type=AssessmentType.FORMATIVE,
                subject=subject,
                grade=3,
                topic=f"{subject} Day {day}",
                feedback_items=feedback_items,
                performance_metrics=performance_metrics,
                overall_feedback="Journey progress",
                learning_path_adjustments=[],
                confidence_indicators={"overall": score},
                assessed_at=base_date + timedelta(days=day)
            )
            
            results.append(result)
    
    return results


def create_sample_learning_profile() -> LearningProfile:
    """Create a sample learning profile"""
    return LearningProfile(
        student_id="test_student",
        preferred_learning_styles=[
            LearningStyleIndicator(
                style=LearningStyle.VISUAL,
                confidence=0.8,
                evidence=["Strong visual reasoning"]
            ),
            LearningStyleIndicator(
                style=LearningStyle.KINESTHETIC,
                confidence=0.6,
                evidence=["Learns through practice"]
            )
        ],
        learning_pace=LearningPace.MODERATE,
        current_difficulty_level={
            "Mathematics": DifficultyLevel.INTERMEDIATE,
            "Science": DifficultyLevel.BEGINNER
        },
        attention_span_minutes=25,
        weak_concepts={
            "Mathematics": ["Fractions", "Word Problems"],
            "Science": ["Force and Motion"]
        },
        strong_concepts={
            "Mathematics": ["Addition", "Subtraction"],
            "Science": ["Plant Life"]
        }
    )


def create_sample_engagement_profile() -> StudentEngagementProfile:
    """Create a sample engagement profile"""
    return StudentEngagementProfile(
        student_id="test_student",
        current_engagement_level=EngagementLevel.MODERATE,
        motivation_types=[MotivationType.INTRINSIC, MotivationType.ACHIEVEMENT],
        engagement_history=[
            EngagementEvent(
                student_id="test_student",
                event_type="practice_completed",
                engagement_score=0.7,
                duration_minutes=20,
                subject="Mathematics",
                timestamp=datetime.utcnow() - timedelta(days=1)
            ),
            EngagementEvent(
                student_id="test_student", 
                event_type="assessment_taken",
                engagement_score=0.8,
                duration_minutes=30,
                subject="Science",
                timestamp=datetime.utcnow() - timedelta(days=2)
            )
        ],
        total_learning_time_minutes=150,
        average_session_duration=25,
        preferred_learning_times=["10:00-11:00", "15:00-16:00"],
        distraction_indicators=["rushes through questions"],
        motivation_triggers=["visual rewards", "progress tracking"]
    )


async def run_all_tests():
    """Run all Analytics Agent tests"""
    print("RSP Education Agent V2 - Analytics Agent Test Suite")
    print("=" * 65)
    
    tests = [
        ("Agent Initialization", test_agent_initialization),
        ("Metrics Calculation", test_metrics_calculation),
        ("Insight Generation", test_insight_generation),
        ("Subject Analytics", test_subject_analytics),
        ("Learning Journey Tracking", test_learning_journey_tracking),
        ("Predictive Modeling", test_predictive_modeling),
        ("Peer Comparison", test_peer_comparison),
        ("Complete Analytics Report", test_complete_analytics_report),
        ("Trend Analysis", test_trend_analysis),
        ("Performance Recommendations", test_performance_recommendations)
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
    print("ANALYTICS AGENT TEST SUMMARY")
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
        print("SUCCESS: All tests passed! Analytics Agent is working correctly.")
        print("\nANALYTICS AGENT STATUS: READY FOR PRODUCTION")
    else:
        print(f"WARNING: {failed} test(s) failed. Please review and fix issues.")
    
    return failed == 0


if __name__ == "__main__":
    asyncio.run(run_all_tests())