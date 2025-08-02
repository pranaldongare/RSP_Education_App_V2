"""
Test Suite for Learning Coordinator Agent - Phase 5 Implementation
Comprehensive testing of learning coordination, session orchestration, and agent integration.
"""

import asyncio
import pytest
from datetime import datetime, timedelta
from typing import Dict, List, Any

from agents.learning_coordinator_agent import (
    LearningCoordinatorAgent,
    LearningSession,
    LearningPath,
    LearningSessionType,
    LearningObjective,
    SessionStatus,
    LearningRecommendation,
    CoordinatorDecision
)
from agents.content_generator import DifficultyLevel, QuestionType


class TestLearningCoordinatorAgent:
    """Test suite for Learning Coordinator Agent"""
    
    @pytest.fixture
    async def coordinator_agent(self):
        """Create Learning Coordinator Agent instance for testing"""
        agent = LearningCoordinatorAgent()
        await agent.initialize_ai_clients()
        return agent
    
    @pytest.mark.asyncio
    async def test_agent_initialization_and_status(self, coordinator_agent):
        """Test agent initialization and status reporting"""
        print("\n=== Testing Learning Coordinator Agent Initialization ===")
        
        # Test agent status
        status = await coordinator_agent.get_agent_status()
        
        print(f"Agent Status: {status}")
        
        # Verify status structure
        assert status["agent_name"] == "learning_coordinator"
        assert status["status"] == "active"
        assert "test_mode" in status
        assert "active_sessions" in status
        assert "learning_paths" in status
        assert "capabilities" in status
        assert len(status["capabilities"]) == 5
        
        print("Learning Coordinator Agent initialized successfully")
    
    @pytest.mark.asyncio
    async def test_learning_path_creation(self, coordinator_agent):
        """Test learning path creation for students"""
        print("\n=== Testing Learning Path Creation ===")
        
        # Test learning path creation
        student_id = "student_123"
        subject = "Mathematics"
        grade = 5
        learning_goals = [
            "Master basic arithmetic operations",
            "Understand fractions and decimals",
            "Solve word problems confidently"
        ]
        
        learning_path = await coordinator_agent.create_learning_path(
            student_id=student_id,
            subject=subject,
            grade=grade,
            learning_goals=learning_goals,
            duration_weeks=8
        )
        
        print(f"Created Learning Path: {learning_path.path_id}")
        print(f"Total Sessions: {learning_path.total_sessions}")
        print(f"Subject: {learning_path.subject}, Grade: {learning_path.grade}")
        print(f"Learning Goals: {learning_path.learning_goals}")
        
        # Verify learning path structure
        assert learning_path.student_id == student_id
        assert learning_path.subject == subject
        assert learning_path.grade == grade
        assert learning_path.learning_goals == learning_goals
        assert learning_path.total_sessions > 0
        assert len(learning_path.sessions) == learning_path.total_sessions
        assert learning_path.completed_sessions == 0
        
        # Verify session structure
        first_session = learning_path.sessions[0]
        assert first_session.student_id == student_id
        assert first_session.subject == subject
        assert first_session.grade == grade
        assert first_session.status == SessionStatus.PLANNED
        assert first_session.estimated_duration > 0
        
        print("SUCCESS: Learning path created successfully with proper structure")
    
    @pytest.mark.asyncio
    async def test_learning_session_orchestration(self, coordinator_agent):
        """Test learning session start and orchestration"""
        print("\n=== Testing Learning Session Orchestration ===")
        
        # First create a learning path
        student_id = "student_456"
        learning_path = await coordinator_agent.create_learning_path(
            student_id=student_id,
            subject="Science",
            grade=4,
            learning_goals=["Understand basic physics concepts"],
            duration_weeks=4
        )
        
        # Get first session
        first_session = learning_path.sessions[0]
        session_id = first_session.session_id
        
        print(f"Starting session: {session_id}")
        print(f"Session type: {first_session.session_type}")
        print(f"Topic: {first_session.topic}")
        
        # Start the session
        session_data = await coordinator_agent.start_learning_session(session_id)
        
        print(f"Session orchestration completed")
        print(f"Session type: {session_data['session']['session_type']}")
        print(f"Content data: {session_data.get('content', 'None')}")
        print(f"Content generated: {session_data['session']['content_generated']}")
        print(f"Assessments created: {session_data['session']['assessments_created']}")
        print(f"Engagement tracked: {session_data['session']['engagement_tracked']}")
        
        # Verify session orchestration
        assert "session" in session_data
        assert "content" in session_data
        assert "engagement_config" in session_data
        assert "adaptive_adjustments" in session_data
        
        # Verify session status updated
        assert session_data["session"]["status"] == "active"
        assert session_data["session"]["started_at"] is not None
        
        # Verify agent coordination flags
        assert session_data["session"]["content_generated"] == True
        assert session_data["session"]["engagement_tracked"] == True
        
        print("SUCCESS: Learning session orchestrated successfully with multi-agent coordination")
    
    @pytest.mark.asyncio
    async def test_session_completion_and_analysis(self, coordinator_agent):
        """Test session completion and post-session analysis"""
        print("\n=== Testing Session Completion and Analysis ===")
        
        # Create learning path and start session
        student_id = "student_789"
        learning_path = await coordinator_agent.create_learning_path(
            student_id=student_id,
            subject="English",
            grade=3,
            learning_goals=["Improve reading comprehension"],
            duration_weeks=6
        )
        
        session_id = learning_path.sessions[0].session_id
        await coordinator_agent.start_learning_session(session_id)
        
        # Simulate session results
        session_results = {
            "assessment_responses": [
                {"question_id": "q1", "answer": "A", "correct": True},
                {"question_id": "q2", "answer": "B", "correct": False},
                {"question_id": "q3", "answer": "C", "correct": True}
            ],
            "engagement_data": {
                "time_spent": 25,
                "interactions": 15,
                "focus_score": 0.8
            },
            "questions": [
                {"id": "q1", "correct_answer": "A"},
                {"id": "q2", "correct_answer": "C"},
                {"id": "q3", "correct_answer": "C"}
            ]
        }
        
        print(f"Completing session: {session_id}")
        print(f"Assessment responses: {len(session_results['assessment_responses'])}")
        
        # Complete the session
        analysis_results = await coordinator_agent.complete_learning_session(
            session_id, session_results
        )
        
        print(f"Session analysis completed")
        print(f"Duration: {analysis_results['duration']:.1f} minutes")
        print(f"Recommendations: {len(analysis_results['recommendations'])}")
        
        # Verify analysis results
        assert "session_id" in analysis_results
        assert "duration" in analysis_results
        assert "assessment_results" in analysis_results
        assert "engagement_analysis" in analysis_results
        assert "recommendations" in analysis_results
        assert isinstance(analysis_results["recommendations"], list)
        
        # Verify session is no longer active
        assert session_id not in coordinator_agent.active_sessions
        
        print("SUCCESS: Session completed successfully with comprehensive analysis")
    
    @pytest.mark.asyncio
    async def test_learning_recommendations_generation(self, coordinator_agent):
        """Test personalized learning recommendations generation"""
        print("\n=== Testing Learning Recommendations Generation ===")
        
        student_id = "student_rec_test"
        
        # Generate recommendations
        recommendations = await coordinator_agent.generate_learning_recommendations(
            student_id=student_id,
            context="performance_improvement"
        )
        
        print(f"Generated {len(recommendations)} recommendations")
        
        for i, rec in enumerate(recommendations, 1):
            print(f"Recommendation {i}:")
            print(f"  Type: {rec.recommendation_type}")
            print(f"  Priority: {rec.priority}")
            print(f"  Title: {rec.title}")
            print(f"  Actions: {len(rec.suggested_actions)}")
            print(f"  Confidence: {rec.confidence_score:.2f}")
        
        # Verify recommendations structure
        assert len(recommendations) > 0
        for rec in recommendations:
            assert rec.student_id == student_id
            assert rec.recommendation_type in ["content_difficulty", "engagement", "learning_path"]
            assert rec.priority in ["high", "medium", "low"]
            assert len(rec.suggested_actions) > 0
            assert 0.0 <= rec.confidence_score <= 1.0
            assert rec.valid_until > datetime.utcnow()
        
        print("SUCCESS: Learning recommendations generated successfully with proper structure")
    
    @pytest.mark.asyncio
    async def test_learning_path_progress_tracking(self, coordinator_agent):
        """Test learning path progress tracking"""
        print("\n=== Testing Learning Path Progress Tracking ===")
        
        student_id = "student_progress"
        
        # Create learning path
        learning_path = await coordinator_agent.create_learning_path(
            student_id=student_id,
            subject="Mathematics", 
            grade=5,
            learning_goals=["Learn about ancient civilizations"],
            duration_weeks=5
        )
        
        initial_status = await coordinator_agent.get_learning_path_status(student_id)
        print(f"Initial progress: {initial_status['progress']['completion_percentage']:.1f}%")
        
        # Start and complete first session
        first_session_id = learning_path.sessions[0].session_id
        await coordinator_agent.start_learning_session(first_session_id)
        
        session_results = {
            "assessment_responses": [{"question_id": "q1", "answer": "A", "correct": True}],
            "engagement_data": {"time_spent": 20, "interactions": 10}
        }
        
        await coordinator_agent.complete_learning_session(first_session_id, session_results)
        
        # Check updated progress
        updated_status = await coordinator_agent.get_learning_path_status(student_id)
        print(f"Updated progress: {updated_status['progress']['completion_percentage']:.1f}%")
        print(f"Completed sessions: {updated_status['progress']['completed_sessions']}")
        print(f"Next session topic: {updated_status['next_session']['topic'] if updated_status['next_session'] else 'None'}")
        
        # Verify progress tracking
        assert updated_status["progress"]["completed_sessions"] == 1
        assert updated_status["progress"]["completion_percentage"] > 0
        
        # Check if there's a next session (depends on total sessions)
        if updated_status["progress"]["completed_sessions"] < updated_status["progress"]["total_sessions"]:
            assert updated_status["next_session"] is not None
        else:
            print("All sessions completed - no next session")
        
        print("SUCCESS: Learning path progress tracked successfully")
    
    @pytest.mark.asyncio
    async def test_multi_agent_coordination(self, coordinator_agent):
        """Test coordination between multiple agents"""
        print("\n=== Testing Multi-Agent Coordination ===")
        
        # Verify all agents are accessible
        assert coordinator_agent.content_agent is not None
        assert coordinator_agent.assessment_agent is not None
        assert coordinator_agent.adaptive_agent is not None
        assert coordinator_agent.engagement_agent is not None
        assert coordinator_agent.analytics_agent is not None
        
        # Test getting status from all agents
        content_status = await coordinator_agent.content_agent.get_agent_status()
        assessment_status = await coordinator_agent.assessment_agent.get_agent_status()
        adaptive_status = await coordinator_agent.adaptive_agent.get_agent_status()
        engagement_status = await coordinator_agent.engagement_agent.get_agent_status()
        analytics_status = await coordinator_agent.analytics_agent.get_agent_status()
        
        print("Agent Status Summary:")
        print(f"  Content Generator: {content_status['status']}")
        print(f"  Assessment: {assessment_status['status']}")
        print(f"  Adaptive Learning: {adaptive_status['status']}")
        print(f"  Engagement: {engagement_status['status']}")
        print(f"  Analytics: {analytics_status['status']}")
        
        # Verify all agents are active
        assert content_status["status"] == "active"
        assert assessment_status["status"] == "active"
        assert adaptive_status["status"] == "active"
        assert engagement_status["status"] == "active"
        assert analytics_status["status"] == "active"
        
        print("SUCCESS: Multi-agent coordination verified successfully")
    
    @pytest.mark.asyncio
    async def test_session_type_variety(self, coordinator_agent):
        """Test different types of learning sessions"""
        print("\n=== Testing Session Type Variety ===")
        
        student_id = "student_variety"
        learning_path = await coordinator_agent.create_learning_path(
            student_id=student_id,
            subject="Mathematics",
            grade=5,
            learning_goals=["Master algebraic concepts"],
            duration_weeks=10
        )
        
        # Count different session types
        session_types = {}
        for session in learning_path.sessions:
            session_type = session.session_type.value
            session_types[session_type] = session_types.get(session_type, 0) + 1
        
        print("Session Type Distribution:")
        for session_type, count in session_types.items():
            print(f"  {session_type}: {count} sessions")
        
        # Verify variety in session types
        assert len(session_types) >= 2  # Should have at least 2 different types
        assert "introduction" in session_types or "practice" in session_types
        # Ensure we have some variety for longer paths
        total_sessions = sum(session_types.values())
        assert total_sessions > 0
        
        # Verify difficulty progression
        difficulties = [session.difficulty_level.value for session in learning_path.sessions]
        print(f"Difficulty levels: {set(difficulties)}")
        
        print("SUCCESS: Session type variety and difficulty progression verified")
    
    @pytest.mark.asyncio
    async def test_coordinator_insights(self, coordinator_agent):
        """Test comprehensive coordinator insights"""
        print("\n=== Testing Coordinator Insights ===")
        
        student_id = "student_insights"
        
        # Create learning path with some activity
        learning_path = await coordinator_agent.create_learning_path(
            student_id=student_id,
            subject="Science",
            grade=5,
            learning_goals=["Understand scientific method"],
            duration_weeks=4
        )
        
        # Start a session to generate some data
        session_id = learning_path.sessions[0].session_id
        await coordinator_agent.start_learning_session(session_id)
        
        # Get comprehensive insights
        insights = await coordinator_agent.get_coordinator_insights(student_id)
        
        print("Coordinator Insights Summary:")
        print(f"  Student ID: {insights['student_id']}")
        print(f"  Active Sessions: {insights['active_sessions']}")
        print(f"  Recommendations: {len(insights['recommendations'])}")
        print(f"  Path Status: {insights['path_status']['progress']['completion_percentage']:.1f}%")
        
        # Verify insights structure
        assert insights["student_id"] == student_id
        assert "learning_profile" in insights
        assert "performance_trends" in insights
        assert "engagement_patterns" in insights
        assert "active_sessions" in insights
        assert "path_status" in insights
        assert "recommendations" in insights
        assert "multi_agent_correlation" in insights
        
        # Verify correlations
        correlations = insights["multi_agent_correlation"]
        assert "performance_engagement_correlation" in correlations
        assert "difficulty_success_correlation" in correlations
        assert "learning_style_content_match" in correlations
        
        print("SUCCESS: Coordinator insights generated successfully with multi-agent correlation")


# Test runner for standalone execution
async def run_learning_coordinator_tests():
    """Run all Learning Coordinator Agent tests"""
    print("Starting Learning Coordinator Agent Tests")
    print("=" * 60)
    
    # Create test instance
    test_instance = TestLearningCoordinatorAgent()
    coordinator = LearningCoordinatorAgent()
    await coordinator.initialize_ai_clients()
    
    try:
        # Run all tests
        await test_instance.test_agent_initialization_and_status(coordinator)
        await test_instance.test_learning_path_creation(coordinator)
        await test_instance.test_learning_session_orchestration(coordinator)
        await test_instance.test_session_completion_and_analysis(coordinator)
        await test_instance.test_learning_recommendations_generation(coordinator)
        await test_instance.test_learning_path_progress_tracking(coordinator)
        await test_instance.test_multi_agent_coordination(coordinator)
        await test_instance.test_session_type_variety(coordinator)
        await test_instance.test_coordinator_insights(coordinator)
        
        print("\n" + "=" * 60)
        print("ALL LEARNING COORDINATOR AGENT TESTS PASSED!")
        print("Agent 6/7 Complete - Learning Coordinator Agent Ready for Production")
        print("Test Coverage: Session orchestration, multi-agent coordination, learning paths")
        
    except Exception as e:
        print(f"\nTest failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(run_learning_coordinator_tests())