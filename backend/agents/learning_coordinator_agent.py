"""
Learning Coordinator Agent - Phase 5 Implementation
Orchestrates all AI agents to create personalized, adaptive learning experiences.
Manages learning sessions, coordinates agent interactions, and optimizes learning pathways.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime, timedelta
from enum import Enum
import statistics
import json

from pydantic import BaseModel, Field
import openai
from anthropic import Anthropic

from config.settings import settings
from core.curriculum import CBSECurriculum
from core.exceptions import AgentException
from agents.content_generator import ContentGeneratorAgent, ContentRequest, DifficultyLevel, QuestionType
from agents.assessment_agent import AssessmentAgent, AssessmentResult, PerformanceMetrics
from agents.adaptive_learning_agent import AdaptiveLearningAgent, LearningProfile, LearningStyle
from agents.engagement_agent import EngagementAgent, EngagementLevel, MotivationType
from agents.analytics_agent import AnalyticsAgent, AnalyticsReport, SubjectAnalytics


class LearningSessionType(str, Enum):
    """Types of learning sessions"""
    INTRODUCTION = "introduction"      # Introducing new concepts
    PRACTICE = "practice"             # Practicing learned concepts
    ASSESSMENT = "assessment"         # Formal assessment
    REVIEW = "review"                # Reviewing previous material
    REMEDIATION = "remediation"      # Addressing learning gaps
    ENRICHMENT = "enrichment"        # Advanced/enrichment content


class LearningObjective(str, Enum):
    """Learning objectives for sessions"""
    UNDERSTAND = "understand"         # Conceptual understanding
    APPLY = "apply"                  # Application of knowledge
    ANALYZE = "analyze"              # Analysis and critical thinking
    SYNTHESIZE = "synthesize"        # Creating new knowledge
    EVALUATE = "evaluate"            # Evaluation and judgment
    REMEMBER = "remember"            # Memorization and recall


class SessionStatus(str, Enum):
    """Session status"""
    PLANNED = "planned"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class LearningSession(BaseModel):
    """Individual learning session"""
    session_id: str
    student_id: str
    subject: str
    grade: int
    topic: str
    session_type: LearningSessionType
    objectives: List[LearningObjective]
    difficulty_level: DifficultyLevel
    estimated_duration: int = Field(description="Duration in minutes")
    status: SessionStatus = SessionStatus.PLANNED
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    content_generated: bool = False
    assessments_created: bool = False
    engagement_tracked: bool = False
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class LearningPath(BaseModel):
    """Complete learning path for a student"""
    path_id: str
    student_id: str
    subject: str
    grade: int
    total_sessions: int
    completed_sessions: int = 0
    sessions: List[LearningSession] = []
    learning_goals: List[str] = []
    estimated_completion_weeks: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class LearningRecommendation(BaseModel):
    """Learning recommendation from coordinator"""
    recommendation_id: str
    student_id: str
    recommendation_type: str
    priority: str = Field(description="high, medium, low")
    title: str
    description: str
    suggested_actions: List[str]
    reasoning: str
    confidence_score: float = Field(ge=0.0, le=1.0)
    valid_until: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class CoordinatorDecision(BaseModel):
    """Coordinator decision based on multi-agent analysis"""
    decision_id: str
    student_id: str
    context: str
    agents_consulted: List[str]
    decision: str
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class LearningCoordinatorAgent:
    """
    Learning Coordinator Agent - Orchestrates all other agents for personalized learning
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.LearningCoordinatorAgent")
        self.curriculum = CBSECurriculum()
        
        # Initialize other agents
        self.content_agent = ContentGeneratorAgent()
        self.assessment_agent = AssessmentAgent()
        self.adaptive_agent = AdaptiveLearningAgent()
        self.engagement_agent = EngagementAgent()
        self.analytics_agent = AnalyticsAgent()
        
        # AI models for coordination intelligence
        self.openai_client = None
        self.anthropic_client = None
        self.test_mode = True
        
        # Active learning sessions
        self.active_sessions: Dict[str, LearningSession] = {}
        self.learning_paths: Dict[str, LearningPath] = {}
        
        self.logger.info("Learning Coordinator Agent initialized")

    async def initialize_ai_clients(self):
        """Initialize AI clients if API keys are available"""
        try:
            if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "test-key":
                self.openai_client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
                self.test_mode = False
                self.logger.info("OpenAI client initialized")
            
            if settings.ANTHROPIC_API_KEY and settings.ANTHROPIC_API_KEY != "test-key":
                self.anthropic_client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
                self.logger.info("Anthropic client initialized")
                
        except Exception as e:
            self.logger.warning(f"AI client initialization failed: {e}")
            self.test_mode = True

    async def get_agent_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "agent_name": "learning_coordinator",
            "status": "active",
            "test_mode": self.test_mode,
            "active_sessions": len(self.active_sessions),
            "learning_paths": len(self.learning_paths),
            "capabilities": [
                "session_orchestration",
                "learning_path_creation",
                "agent_coordination",
                "personalized_recommendations",
                "adaptive_learning_flow"
            ],
            "initialized_at": datetime.utcnow().isoformat()
        }

    async def create_learning_path(
        self,
        student_id: str,
        subject: str,
        grade: int,
        learning_goals: List[str],
        duration_weeks: int = 12
    ) -> LearningPath:
        """Create personalized learning path for student"""
        try:
            # Get student profile from adaptive learning agent (simplified for test mode)
            learning_profile = {"average_performance": 0.7, "learning_style": "visual"}
            
            # Get curriculum topics from subject curriculum
            subject_curriculum = await self.curriculum.get_subject_curriculum(subject, grade)
            if not subject_curriculum:
                raise AgentException(f"No curriculum found for {subject} grade {grade}")
            
            # Extract topics from chapters
            topics = []
            for chapter in subject_curriculum.chapters:
                topics.extend(chapter.topics)
            
            # Generate learning path sessions
            sessions = []
            session_count = 0
            
            for topic in topics[:min(len(topics), duration_weeks * 2)]:  # 2 sessions per week
                session_count += 1
                
                # Determine session type based on learning progress
                session_type = self._determine_session_type(session_count, topic)
                
                # Set difficulty based on student profile
                difficulty = self._determine_difficulty(learning_profile, topic)
                
                # Create session
                session = LearningSession(
                    session_id=f"session_{student_id}_{session_count}",
                    student_id=student_id,
                    subject=subject,
                    grade=grade,
                    topic=topic.name if hasattr(topic, 'name') else str(topic),
                    session_type=session_type,
                    objectives=self._determine_objectives(session_type, topic.name if hasattr(topic, 'name') else str(topic)),
                    difficulty_level=difficulty,
                    estimated_duration=self._estimate_duration(session_type, difficulty)
                )
                
                sessions.append(session)
            
            # Create learning path
            path = LearningPath(
                path_id=f"path_{student_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                student_id=student_id,
                subject=subject,
                grade=grade,
                total_sessions=len(sessions),
                sessions=sessions,
                learning_goals=learning_goals,
                estimated_completion_weeks=duration_weeks
            )
            
            self.learning_paths[path.path_id] = path
            self.logger.info(f"Created learning path {path.path_id} with {len(sessions)} sessions")
            
            return path
            
        except Exception as e:
            self.logger.error(f"Error creating learning path: {e}")
            raise AgentException(f"Failed to create learning path: {str(e)}")

    async def start_learning_session(self, session_id: str) -> Dict[str, Any]:
        """Start a learning session with full agent coordination"""
        try:
            # Find session in learning paths
            session = None
            for path in self.learning_paths.values():
                for s in path.sessions:
                    if s.session_id == session_id:
                        session = s
                        break
                if session:
                    break
            
            if not session:
                raise AgentException(f"Session {session_id} not found")
            
            if session.status != SessionStatus.PLANNED:
                raise AgentException(f"Session {session_id} is not in planned state")
            
            # Update session status
            session.status = SessionStatus.ACTIVE
            session.started_at = datetime.utcnow()
            self.active_sessions[session_id] = session
            
            # Coordinate with all agents to prepare session
            session_data = await self._orchestrate_session_preparation(session)
            
            # Update session data with current session state (with updated flags)
            session_data["session"] = session.dict()
            
            self.logger.info(f"Started learning session {session_id}")
            return session_data
            
        except Exception as e:
            self.logger.error(f"Error starting session {session_id}: {e}")
            raise AgentException(f"Failed to start session: {str(e)}")

    async def _orchestrate_session_preparation(self, session: LearningSession) -> Dict[str, Any]:
        """Orchestrate all agents to prepare a learning session"""
        try:
            session_data = {
                "session": session.dict(),
                "content": None,
                "assessments": None,
                "engagement_config": None,
                "adaptive_adjustments": None
            }
            
            # 1. Generate content using Content Generator Agent
            if session.session_type in [LearningSessionType.INTRODUCTION, LearningSessionType.PRACTICE]:
                if self.test_mode:
                    # Test mode - simulate content generation
                    session_data["content"] = {"content": f"Test content for {session.topic}", "type": "explanation"}
                    session.content_generated = True
                else:
                    content_request = ContentRequest(
                        subject=session.subject,
                        grade=session.grade,
                        topic=session.topic,  # Already converted to string in session creation
                        content_type="explanation",
                        difficulty_level=session.difficulty_level,
                        learning_objectives=session.objectives
                    )
                    
                    content = await self.content_agent.generate_content(content_request)
                    session_data["content"] = content
                    session.content_generated = True
            
            # 2. Generate assessments using Assessment Agent
            if session.session_type in [LearningSessionType.ASSESSMENT, LearningSessionType.PRACTICE]:
                if self.test_mode:
                    # Test mode - simulate assessment generation
                    session_data["assessments"] = {"questions": [{"id": "q1", "question": f"Test question about {session.topic}"}]}
                    session.assessments_created = True
                else:
                    questions = await self.content_agent.generate_questions(
                        subject=session.subject,
                        grade=session.grade,
                        topic=session.topic,
                        question_type=QuestionType.MCQ,
                        difficulty_level=session.difficulty_level,
                        num_questions=5
                    )
                    session_data["assessments"] = questions
                    session.assessments_created = True
            
            # 3. Configure engagement using Engagement Agent (simplified for test mode)
            engagement_config = {"gamification_enabled": True, "motivation_type": "achievement"}
            session_data["engagement_config"] = engagement_config
            session.engagement_tracked = True
            
            # 4. Get adaptive adjustments from Adaptive Learning Agent (simplified for test mode)
            adaptive_adjustments = {"difficulty_adjustment": "maintain", "learning_style": "visual"}
            session_data["adaptive_adjustments"] = adaptive_adjustments
            
            return session_data
            
        except Exception as e:
            self.logger.error(f"Error orchestrating session preparation: {e}")
            raise

    async def complete_learning_session(
        self,
        session_id: str,
        session_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Complete a learning session and coordinate post-session analysis"""
        try:
            session = self.active_sessions.get(session_id)
            if not session:
                raise AgentException(f"Active session {session_id} not found")
            
            # Update session status
            session.status = SessionStatus.COMPLETED
            session.completed_at = datetime.utcnow()
            
            # Coordinate post-session analysis with all agents
            analysis_results = await self._orchestrate_post_session_analysis(
                session, session_results
            )
            
            # Remove from active sessions
            del self.active_sessions[session_id]
            
            # Update learning path progress
            await self._update_learning_path_progress(session)
            
            self.logger.info(f"Completed learning session {session_id}")
            return analysis_results
            
        except Exception as e:
            self.logger.error(f"Error completing session {session_id}: {e}")
            raise AgentException(f"Failed to complete session: {str(e)}")

    async def _orchestrate_post_session_analysis(
        self,
        session: LearningSession,
        session_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Orchestrate post-session analysis across all agents"""
        try:
            analysis = {
                "session_id": session.session_id,
                "duration": (session.completed_at - session.started_at).total_seconds() / 60,
                "assessment_results": None,
                "engagement_analysis": None,
                "learning_progress": None,
                "recommendations": []
            }
            
            # 1. Process assessment results if available
            if "assessment_responses" in session_results:
                if self.test_mode:
                    # Test mode - simulate assessment results
                    analysis["assessment_results"] = {
                        "score": 0.67,
                        "correct_answers": 2,
                        "total_questions": 3,
                        "feedback": "Good performance with room for improvement"
                    }
                else:
                    # Production would use actual assessment agent
                    pass  # assessment_result = await self.assessment_agent.assess_responses(...)
                
                # Update adaptive learning with performance data (simplified for test mode)
                pass  # Would update learning profile in production
            
            # 2. Analyze engagement (simplified for test mode)
            if "engagement_data" in session_results:
                engagement_analysis = {"engagement_level": "high", "time_spent": session_results["engagement_data"].get("time_spent", 20)}
                analysis["engagement_analysis"] = engagement_analysis
            
            # 3. Update analytics (simplified for test mode)
            pass  # Would update analytics in production
            
            # 4. Generate recommendations
            recommendations = await self._generate_session_recommendations(
                session, analysis
            )
            analysis["recommendations"] = recommendations
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error in post-session analysis: {e}")
            raise

    async def generate_learning_recommendations(
        self,
        student_id: str,
        context: str = "general"
    ) -> List[LearningRecommendation]:
        """Generate personalized learning recommendations"""
        try:
            # Gather data from all agents (simplified for test mode)
            learning_profile = {"average_performance": 0.7, "learning_style": "visual"}
            performance_analytics = {"average_score": 0.75, "improvement_trend": "positive"}
            engagement_analytics = {"engagement_level": "high", "session_frequency": 0.8}
            
            recommendations = []
            
            # Generate recommendations based on multi-agent analysis
            if self.test_mode:
                # Test mode recommendations
                recommendations = [
                    LearningRecommendation(
                        recommendation_id=f"rec_{student_id}_1",
                        student_id=student_id,
                        recommendation_type="content_difficulty",
                        priority="medium",
                        title="Adjust Content Difficulty",
                        description="Based on recent performance, consider adjusting content difficulty",
                        suggested_actions=[
                            "Increase practice problems",
                            "Review prerequisite concepts",
                            "Add visual learning aids"
                        ],
                        reasoning="Student showing consistent 75% performance, ready for slight increase",
                        confidence_score=0.85,
                        valid_until=datetime.utcnow() + timedelta(days=7)
                    ),
                    LearningRecommendation(
                        recommendation_id=f"rec_{student_id}_2",
                        student_id=student_id,
                        recommendation_type="engagement",
                        priority="high",
                        title="Boost Engagement",
                        description="Engagement metrics suggest need for more interactive content",
                        suggested_actions=[
                            "Add gamification elements",
                            "Include collaborative activities",
                            "Provide immediate feedback"
                        ],
                        reasoning="Engagement level dropping over past 3 sessions",
                        confidence_score=0.78,
                        valid_until=datetime.utcnow() + timedelta(days=5)
                    )
                ]
            else:
                # AI-powered recommendations
                recommendations = await self._generate_ai_recommendations(
                    student_id, learning_profile, performance_analytics, engagement_analytics
                )
            
            self.logger.info(f"Generated {len(recommendations)} recommendations for student {student_id}")
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error generating recommendations: {e}")
            raise AgentException(f"Failed to generate recommendations: {str(e)}")

    def _determine_session_type(self, session_number: int, topic: str) -> LearningSessionType:
        """Determine session type based on sequence and topic"""
        if session_number == 1:
            return LearningSessionType.INTRODUCTION
        elif session_number % 5 == 0:
            return LearningSessionType.ASSESSMENT
        elif session_number % 3 == 0:
            return LearningSessionType.REVIEW
        else:
            return LearningSessionType.PRACTICE

    def _determine_difficulty(self, learning_profile: Optional[Dict], topic: str) -> DifficultyLevel:
        """Determine difficulty level based on learning profile"""
        if not learning_profile:
            return DifficultyLevel.INTERMEDIATE
        
        # Simple logic - can be enhanced with ML
        avg_performance = learning_profile.get("average_performance", 0.7)
        if avg_performance >= 0.85:
            return DifficultyLevel.ADVANCED
        elif avg_performance >= 0.65:
            return DifficultyLevel.INTERMEDIATE
        else:
            return DifficultyLevel.BEGINNER

    def _determine_objectives(self, session_type: LearningSessionType, topic: str) -> List[LearningObjective]:
        """Determine learning objectives based on session type"""
        if session_type == LearningSessionType.INTRODUCTION:
            return [LearningObjective.UNDERSTAND, LearningObjective.REMEMBER]
        elif session_type == LearningSessionType.PRACTICE:
            return [LearningObjective.APPLY, LearningObjective.ANALYZE]
        elif session_type == LearningSessionType.ASSESSMENT:
            return [LearningObjective.APPLY, LearningObjective.EVALUATE]
        elif session_type == LearningSessionType.REVIEW:
            return [LearningObjective.REMEMBER, LearningObjective.UNDERSTAND]
        else:
            return [LearningObjective.UNDERSTAND, LearningObjective.APPLY]

    def _estimate_duration(self, session_type: LearningSessionType, difficulty: DifficultyLevel) -> int:
        """Estimate session duration in minutes"""
        base_duration = {
            LearningSessionType.INTRODUCTION: 30,
            LearningSessionType.PRACTICE: 25,
            LearningSessionType.ASSESSMENT: 40,
            LearningSessionType.REVIEW: 20,
            LearningSessionType.REMEDIATION: 35,
            LearningSessionType.ENRICHMENT: 30
        }
        
        duration = base_duration.get(session_type, 25)
        
        # Adjust for difficulty
        if difficulty == DifficultyLevel.ADVANCED:
            duration += 10
        elif difficulty == DifficultyLevel.BEGINNER:
            duration -= 5
        
        return max(15, duration)  # Minimum 15 minutes

    async def _update_learning_path_progress(self, session: LearningSession):
        """Update learning path progress after session completion"""
        for path in self.learning_paths.values():
            if session.student_id == path.student_id:
                path.completed_sessions += 1
                path.last_updated = datetime.utcnow()
                break

    async def _generate_session_recommendations(
        self,
        session: LearningSession,
        analysis: Dict[str, Any]
    ) -> List[str]:
        """Generate recommendations based on session analysis"""
        recommendations = []
        
        # Assessment-based recommendations
        if analysis.get("assessment_results"):
            score = analysis["assessment_results"].get("score", 0)
            if score < 0.6:
                recommendations.append("Consider reviewing prerequisite concepts")
                recommendations.append("Add more practice problems at current difficulty")
            elif score > 0.9:
                recommendations.append("Ready for increased difficulty level")
                recommendations.append("Consider enrichment activities")
        
        # Engagement-based recommendations
        if analysis.get("engagement_analysis"):
            engagement_level = analysis["engagement_analysis"].get("level")
            if engagement_level in ["low", "very_low"]:
                recommendations.append("Incorporate more interactive elements")
                recommendations.append("Consider gamification strategies")
        
        return recommendations

    async def _generate_ai_recommendations(
        self,
        student_id: str,
        learning_profile: Dict,
        performance_analytics: Dict,
        engagement_analytics: Dict
    ) -> List[LearningRecommendation]:
        """Generate AI-powered recommendations (when not in test mode)"""
        # Placeholder for AI-powered recommendation generation
        # This would use OpenAI/Anthropic APIs to analyze student data
        # and generate personalized recommendations
        return []

    async def get_learning_path_status(self, student_id: str) -> Dict[str, Any]:
        """Get learning path status for student"""
        student_paths = [
            path for path in self.learning_paths.values()
            if path.student_id == student_id
        ]
        
        if not student_paths:
            return {"status": "no_active_paths"}
        
        # Return most recent path
        latest_path = max(student_paths, key=lambda p: p.created_at)
        
        return {
            "path_id": latest_path.path_id,
            "subject": latest_path.subject,
            "grade": latest_path.grade,
            "progress": {
                "completed_sessions": latest_path.completed_sessions,
                "total_sessions": latest_path.total_sessions,
                "completion_percentage": (latest_path.completed_sessions / latest_path.total_sessions) * 100
            },
            "next_session": self._get_next_session(latest_path),
            "estimated_completion": latest_path.estimated_completion_weeks
        }

    def _get_next_session(self, path: LearningPath) -> Optional[Dict[str, Any]]:
        """Get next planned session in learning path"""
        for session in path.sessions:
            if session.status == SessionStatus.PLANNED:
                return {
                    "session_id": session.session_id,
                    "topic": session.topic,
                    "session_type": session.session_type.value,
                    "estimated_duration": session.estimated_duration
                }
        return None

    async def get_coordinator_insights(self, student_id: str) -> Dict[str, Any]:
        """Get comprehensive coordinator insights for student"""
        try:
            # Gather insights from all agents (simplified for test mode)
            insights = {
                "student_id": student_id,
                "learning_profile": {"average_performance": 0.7, "learning_style": "visual"},
                "performance_trends": {"average_score": 0.75, "improvement_trend": "positive"},
                "engagement_patterns": {"engagement_level": "high", "session_frequency": 0.8},
                "active_sessions": len([s for s in self.active_sessions.values() if s.student_id == student_id]),
                "path_status": await self.get_learning_path_status(student_id),
                "recommendations": await self.generate_learning_recommendations(student_id),
                "coordinator_decisions": [],  # Recent decisions made by coordinator
                "multi_agent_correlation": self._analyze_agent_correlations(student_id)
            }
            
            return insights
            
        except Exception as e:
            self.logger.error(f"Error getting coordinator insights: {e}")
            raise AgentException(f"Failed to get insights: {str(e)}")

    def _analyze_agent_correlations(self, student_id: str) -> Dict[str, Any]:
        """Analyze correlations between different agent outputs"""
        # Placeholder for correlation analysis
        return {
            "performance_engagement_correlation": 0.75,
            "difficulty_success_correlation": 0.82,
            "learning_style_content_match": 0.88,
            "motivation_completion_correlation": 0.69
        }