"""
Engagement Agent - Phase 4 Implementation
Manages student motivation, gamification, engagement tracking, and behavioral incentives.
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
from agents.content_generator import DifficultyLevel, QuestionType
from agents.assessment_agent import AssessmentResult, PerformanceMetrics
from agents.adaptive_learning_agent import LearningProfile, LearningStyle


class EngagementLevel(str, Enum):
    """Student engagement levels"""
    VERY_LOW = "very_low"      # Disengaged, needs immediate intervention
    LOW = "low"                # Below average engagement
    MODERATE = "moderate"      # Average engagement
    HIGH = "high"              # Above average engagement  
    VERY_HIGH = "very_high"    # Highly engaged and motivated


class MotivationType(str, Enum):
    """Types of motivation"""
    INTRINSIC = "intrinsic"    # Internal satisfaction and curiosity
    EXTRINSIC = "extrinsic"    # External rewards and recognition
    SOCIAL = "social"          # Peer interaction and collaboration
    ACHIEVEMENT = "achievement" # Goal completion and mastery
    AUTONOMY = "autonomy"      # Choice and control over learning


class GamificationElement(str, Enum):
    """Gamification elements available"""
    POINTS = "points"          # Earning points for activities
    BADGES = "badges"          # Achievement badges
    LEVELS = "levels"          # Progressive levels
    STREAKS = "streaks"        # Consecutive activity streaks
    CHALLENGES = "challenges"   # Special challenges and quests
    LEADERBOARDS = "leaderboards" # Competitive rankings
    ACHIEVEMENTS = "achievements"  # Milestone achievements


class EngagementMetric(BaseModel):
    """Individual engagement metric"""
    metric_name: str
    value: float = Field(..., ge=0.0, le=1.0, description="Metric value between 0.0 and 1.0")
    weight: float = Field(default=1.0, ge=0.0, description="Weight of this metric")
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    trend_direction: str = Field(default="stable", description="improving, declining, or stable")


class StudentEngagementProfile(BaseModel):
    """Comprehensive engagement profile for a student"""
    student_id: str
    current_engagement_level: EngagementLevel
    engagement_score: float = Field(..., ge=0.0, le=1.0)
    motivation_types: List[MotivationType] = Field(default_factory=list)
    preferred_gamification: List[GamificationElement] = Field(default_factory=list)
    
    # Engagement metrics
    session_duration_avg: float = Field(default=0.0, description="Average session duration in minutes")
    completion_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    interaction_frequency: float = Field(default=0.0, description="Interactions per day")
    help_seeking_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    challenge_acceptance_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    
    # Behavioral indicators
    streak_days: int = Field(default=0, ge=0)
    total_points: int = Field(default=0, ge=0)
    badges_earned: List[str] = Field(default_factory=list)
    current_level: int = Field(default=1, ge=1)
    
    # Risk indicators
    disengagement_risk: float = Field(default=0.0, ge=0.0, le=1.0)
    intervention_needed: bool = Field(default=False)
    last_active: Optional[datetime] = Field(default=None)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class EngagementEvent(BaseModel):
    """Individual engagement event"""
    student_id: str
    event_type: str  # "session_start", "question_answered", "badge_earned", etc.
    event_data: Dict[str, Any] = Field(default_factory=dict)
    engagement_impact: float = Field(default=0.0, ge=-1.0, le=1.0)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class GamificationReward(BaseModel):
    """Reward for gamification"""
    reward_id: str
    reward_type: GamificationElement
    title: str
    description: str
    points_value: int = Field(default=0, ge=0)
    badge_icon: Optional[str] = Field(default=None)
    requirements: Dict[str, Any] = Field(default_factory=dict)
    rarity: str = Field(default="common", description="common, rare, epic, legendary")


class MotivationIntervention(BaseModel):
    """Intervention to improve motivation"""
    intervention_id: str
    student_id: str
    intervention_type: str  # "encouragement", "goal_setting", "reward", "break_suggestion"
    title: str
    message: str
    suggested_actions: List[str] = Field(default_factory=list)
    gamification_elements: List[GamificationElement] = Field(default_factory=list)
    priority: int = Field(default=3, ge=1, le=5)
    estimated_impact: float = Field(default=0.5, ge=0.0, le=1.0)
    expires_at: Optional[datetime] = Field(default=None)


class EngagementAnalysis(BaseModel):
    """Analysis of student engagement patterns"""
    student_id: str
    analysis_period_days: int
    engagement_trends: Dict[str, float] = Field(default_factory=dict)
    behavioral_patterns: Dict[str, Any] = Field(default_factory=dict)
    risk_factors: List[str] = Field(default_factory=list)
    positive_indicators: List[str] = Field(default_factory=list)
    recommended_interventions: List[MotivationIntervention] = Field(default_factory=list)
    gamification_effectiveness: Dict[str, float] = Field(default_factory=dict)


class EngagementRequest(BaseModel):
    """Request for engagement analysis and recommendations"""
    student_id: str
    assessment_results: List[AssessmentResult] = Field(default_factory=list)
    learning_profile: Optional[LearningProfile] = Field(default=None)
    engagement_events: List[EngagementEvent] = Field(default_factory=list)
    current_engagement_profile: Optional[StudentEngagementProfile] = Field(default=None)
    analysis_period_days: int = Field(default=7, ge=1, le=30)
    intervention_preferences: List[str] = Field(default_factory=list)


class EngagementRecommendation(BaseModel):
    """Complete engagement recommendation"""
    student_id: str
    updated_engagement_profile: StudentEngagementProfile
    engagement_analysis: EngagementAnalysis
    immediate_interventions: List[MotivationIntervention]
    gamification_rewards: List[GamificationReward]
    long_term_strategies: List[str] = Field(default_factory=list)
    monitoring_schedule: Dict[str, int] = Field(default_factory=dict)  # metric -> check frequency in hours
    success_probability: float = Field(..., ge=0.0, le=1.0)


class EngagementAgent:
    """
    Engagement Agent for managing student motivation and gamification
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.EngagementAgent")
        self.curriculum = CBSECurriculum()
        self.openai_model = None
        self.anthropic_model = None
        self._initialize_models()
        
        # Engagement scoring weights
        self.engagement_weights = {
            "session_duration": 0.15,
            "completion_rate": 0.25, 
            "interaction_frequency": 0.15,
            "help_seeking": 0.10,
            "challenge_acceptance": 0.15,
            "streak_maintenance": 0.10,
            "progress_consistency": 0.10
        }
        
        # Gamification reward templates
        self.reward_templates = self._initialize_reward_templates()
        
        # Motivation type indicators
        self.motivation_indicators = {
            MotivationType.INTRINSIC: [
                "explores additional content", "asks questions", "experiments with concepts",
                "shows curiosity", "enjoys learning process"
            ],
            MotivationType.EXTRINSIC: [
                "motivated by points", "likes badges", "responds to rewards",
                "competitive behavior", "seeks recognition"
            ],
            MotivationType.SOCIAL: [
                "prefers group activities", "shares achievements", "seeks peer interaction",
                "collaborative learning", "social recognition important"
            ],
            MotivationType.ACHIEVEMENT: [
                "goal-oriented", "completes challenges", "tracks progress",
                "focuses on mastery", "celebrates milestones"
            ],
            MotivationType.AUTONOMY: [
                "prefers choice", "self-directed learning", "customizes experience",
                "independent work", "controls pace"
            ]
        }

    def _initialize_models(self):
        """Initialize AI models for engagement analysis"""
        try:
            if hasattr(settings, 'openai_api_key') and settings.openai_api_key:
                openai.api_key = settings.openai_api_key
                self.openai_model = "gpt-4-turbo-preview"
                
            if hasattr(settings, 'anthropic_api_key') and settings.anthropic_api_key:
                self.anthropic_model = Anthropic(api_key=settings.anthropic_api_key)
                
            self.logger.info("Engagement AI models initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize AI models: {e}")
            self.logger.warning("Continuing without AI models for testing purposes")

    def _initialize_reward_templates(self) -> Dict[str, GamificationReward]:
        """Initialize gamification reward templates"""
        return {
            "first_answer": GamificationReward(
                reward_id="first_answer",
                reward_type=GamificationElement.POINTS,
                title="First Answer",
                description="Answered your first question!",
                points_value=10,
                requirements={"questions_answered": 1},
                rarity="common"
            ),
            "streak_7": GamificationReward(
                reward_id="streak_7",
                reward_type=GamificationElement.BADGES,
                title="Week Warrior",
                description="Maintained a 7-day learning streak!",
                points_value=100,
                badge_icon="FIRE",
                requirements={"consecutive_days": 7},
                rarity="rare"
            ),
            "perfect_score": GamificationReward(
                reward_id="perfect_score",
                reward_type=GamificationElement.BADGES,
                title="Perfect Score",
                description="Achieved 100% on an assessment!",
                points_value=50,
                badge_icon="TARGET",
                requirements={"assessment_score": 1.0},
                rarity="epic"
            ),
            "level_up": GamificationReward(
                reward_id="level_up",
                reward_type=GamificationElement.LEVELS,
                title="Level Up!",
                description="Advanced to the next level!",
                points_value=25,
                requirements={"level_increase": 1},
                rarity="common"
            ),
            "challenge_master": GamificationReward(
                reward_id="challenge_master",
                reward_type=GamificationElement.ACHIEVEMENTS,
                title="Challenge Master",
                description="Completed 10 difficult challenges!",
                points_value=200,
                badge_icon="TROPHY",
                requirements={"difficult_challenges": 10},
                rarity="legendary"
            )
        }

    async def analyze_engagement(self, request: EngagementRequest) -> EngagementRecommendation:
        """
        Main method to analyze student engagement and generate recommendations
        """
        try:
            self.logger.info(f"Analyzing engagement for student {request.student_id}")
            
            # Analyze engagement patterns from events and assessments
            engagement_analysis = await self._analyze_engagement_patterns(
                request.engagement_events, request.assessment_results, request.analysis_period_days
            )
            
            # Update or create engagement profile
            updated_profile = await self._update_engagement_profile(
                request.student_id, request.current_engagement_profile, 
                engagement_analysis, request.learning_profile
            )
            
            # Detect motivation types
            motivation_types = await self._detect_motivation_types(
                request.engagement_events, request.assessment_results, request.learning_profile
            )
            updated_profile.motivation_types = motivation_types
            
            # Generate immediate interventions
            immediate_interventions = await self._generate_interventions(
                updated_profile, engagement_analysis, request.intervention_preferences
            )
            
            # Check for available gamification rewards
            gamification_rewards = await self._check_gamification_rewards(
                updated_profile, request.engagement_events
            )
            
            # Generate long-term engagement strategies
            long_term_strategies = self._generate_long_term_strategies(
                updated_profile, engagement_analysis
            )
            
            # Create monitoring schedule
            monitoring_schedule = self._create_monitoring_schedule(updated_profile)
            
            # Estimate success probability
            success_probability = self._estimate_intervention_success(
                updated_profile, immediate_interventions, engagement_analysis
            )
            
            recommendation = EngagementRecommendation(
                student_id=request.student_id,
                updated_engagement_profile=updated_profile,
                engagement_analysis=engagement_analysis,
                immediate_interventions=immediate_interventions,
                gamification_rewards=gamification_rewards,
                long_term_strategies=long_term_strategies,
                monitoring_schedule=monitoring_schedule,
                success_probability=success_probability
            )
            
            self.logger.info(f"Engagement analysis completed for student {request.student_id}")
            return recommendation
            
        except Exception as e:
            self.logger.error(f"Engagement analysis failed: {e}")
            raise AgentException(f"Engagement analysis failed: {e}")

    async def _analyze_engagement_patterns(
        self,
        engagement_events: List[EngagementEvent],
        assessment_results: List[AssessmentResult],
        analysis_period_days: int
    ) -> EngagementAnalysis:
        """Analyze patterns in student engagement"""
        
        if not engagement_events and not assessment_results:
            return EngagementAnalysis(
                student_id="unknown",
                analysis_period_days=analysis_period_days,
                engagement_trends={"insufficient_data": 0.0}
            )
        
        student_id = engagement_events[0].student_id if engagement_events else assessment_results[0].student_id
        
        # Calculate engagement trends
        engagement_trends = {}
        
        # Session patterns
        if engagement_events:
            session_events = [e for e in engagement_events if e.event_type == "session_start"]
            if session_events:
                daily_sessions = {}
                for event in session_events:
                    date_key = event.timestamp.date()
                    daily_sessions[date_key] = daily_sessions.get(date_key, 0) + 1
                
                engagement_trends["daily_sessions"] = statistics.mean(daily_sessions.values()) if daily_sessions else 0.0
                engagement_trends["session_consistency"] = len(daily_sessions) / analysis_period_days
        
        # Assessment engagement
        if assessment_results:
            recent_results = [r for r in assessment_results 
                            if (datetime.utcnow() - r.assessed_at).days <= analysis_period_days]
            
            if recent_results:
                engagement_trends["assessment_frequency"] = len(recent_results) / analysis_period_days
                engagement_trends["average_performance"] = statistics.mean(
                    r.performance_metrics.overall_score for r in recent_results
                )
                
                # Time engagement
                completion_times = [r.performance_metrics.completion_time 
                                  for r in recent_results if r.performance_metrics.completion_time]
                if completion_times:
                    engagement_trends["average_time_investment"] = statistics.mean(completion_times) / 60.0  # minutes
        
        # Behavioral patterns
        behavioral_patterns = {
            "peak_activity_times": self._identify_peak_times(engagement_events),
            "preferred_content_types": self._identify_content_preferences(engagement_events, assessment_results),
            "interaction_patterns": self._analyze_interaction_patterns(engagement_events),
            "challenge_behavior": self._analyze_challenge_behavior(engagement_events)
        }
        
        # Risk factors
        risk_factors = []
        positive_indicators = []
        
        if engagement_trends.get("session_consistency", 0) < 0.3:
            risk_factors.append("Inconsistent learning sessions")
        else:
            positive_indicators.append("Regular learning pattern")
            
        if engagement_trends.get("average_performance", 0) < 0.5:
            risk_factors.append("Low assessment performance")
        elif engagement_trends.get("average_performance", 0) > 0.7:
            positive_indicators.append("Strong academic performance")
        
        # Calculate overall engagement score
        overall_engagement = self._calculate_overall_engagement(engagement_trends, behavioral_patterns)
        
        return EngagementAnalysis(
            student_id=student_id,
            analysis_period_days=analysis_period_days,
            engagement_trends=engagement_trends,
            behavioral_patterns=behavioral_patterns,
            risk_factors=risk_factors,
            positive_indicators=positive_indicators,
            gamification_effectiveness=self._analyze_gamification_effectiveness(engagement_events)
        )

    def _identify_peak_times(self, engagement_events: List[EngagementEvent]) -> Dict[str, int]:
        """Identify when student is most active"""
        hour_counts = {}
        
        for event in engagement_events:
            hour = event.timestamp.hour
            hour_counts[hour] = hour_counts.get(hour, 0) + 1
        
        # Return top 3 most active hours
        sorted_hours = sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_hours[:3])

    def _identify_content_preferences(
        self, 
        engagement_events: List[EngagementEvent],
        assessment_results: List[AssessmentResult]
    ) -> Dict[str, float]:
        """Identify preferred content types and subjects"""
        preferences = {}
        
        # From assessment results
        for result in assessment_results:
            subject = result.subject
            score = result.performance_metrics.overall_score
            
            if subject not in preferences:
                preferences[subject] = []
            preferences[subject].append(score)
        
        # Average performance by subject as preference indicator
        for subject, scores in preferences.items():
            preferences[subject] = statistics.mean(scores)
        
        return preferences

    def _analyze_interaction_patterns(self, engagement_events: List[EngagementEvent]) -> Dict[str, Any]:
        """Analyze how student interacts with the system"""
        patterns = {
            "help_seeking_frequency": 0.0,
            "hint_usage": 0.0,
            "retry_attempts": 0.0,
            "feature_usage": {}
        }
        
        total_events = len(engagement_events)
        if total_events == 0:
            return patterns
        
        help_events = len([e for e in engagement_events if e.event_type == "help_requested"])
        hint_events = len([e for e in engagement_events if e.event_type == "hint_used"])
        retry_events = len([e for e in engagement_events if e.event_type == "question_retried"])
        
        patterns["help_seeking_frequency"] = help_events / total_events
        patterns["hint_usage"] = hint_events / total_events
        patterns["retry_attempts"] = retry_events / total_events
        
        # Feature usage
        feature_counts = {}
        for event in engagement_events:
            event_type = event.event_type
            feature_counts[event_type] = feature_counts.get(event_type, 0) + 1
        
        patterns["feature_usage"] = feature_counts
        
        return patterns

    def _analyze_challenge_behavior(self, engagement_events: List[EngagementEvent]) -> Dict[str, float]:
        """Analyze how student responds to challenges"""
        behavior = {
            "challenge_acceptance_rate": 0.0,
            "challenge_completion_rate": 0.0,
            "difficulty_preference": 0.5  # 0=easy, 1=hard
        }
        
        challenge_offered = len([e for e in engagement_events if e.event_type == "challenge_offered"])
        challenge_accepted = len([e for e in engagement_events if e.event_type == "challenge_accepted"])
        challenge_completed = len([e for e in engagement_events if e.event_type == "challenge_completed"])
        
        if challenge_offered > 0:
            behavior["challenge_acceptance_rate"] = challenge_accepted / challenge_offered
        
        if challenge_accepted > 0:
            behavior["challenge_completion_rate"] = challenge_completed / challenge_accepted
        
        return behavior

    def _analyze_gamification_effectiveness(self, engagement_events: List[EngagementEvent]) -> Dict[str, float]:
        """Analyze effectiveness of different gamification elements"""
        effectiveness = {}
        
        for element in GamificationElement:
            element_events = [e for e in engagement_events 
                            if element.value in str(e.event_data).lower()]
            
            if element_events:
                avg_impact = statistics.mean(e.engagement_impact for e in element_events)
                effectiveness[element.value] = max(0.0, avg_impact)
            else:
                effectiveness[element.value] = 0.0
        
        return effectiveness

    def _calculate_overall_engagement(
        self, 
        engagement_trends: Dict[str, float],
        behavioral_patterns: Dict[str, Any]
    ) -> float:
        """Calculate overall engagement score"""
        
        score = 0.5  # Base score
        
        # Session consistency boost
        consistency = engagement_trends.get("session_consistency", 0.0)
        score += consistency * 0.2
        
        # Performance boost
        performance = engagement_trends.get("average_performance", 0.5)
        score += (performance - 0.5) * 0.2
        
        # Activity frequency boost
        activity = engagement_trends.get("daily_sessions", 0.0)
        normalized_activity = min(activity / 3.0, 1.0)  # 3 sessions per day = max
        score += normalized_activity * 0.1
        
        # Interaction quality
        interactions = behavioral_patterns.get("interaction_patterns", {})
        help_seeking = interactions.get("help_seeking_frequency", 0.0)
        if 0.1 <= help_seeking <= 0.3:  # Healthy help-seeking
            score += 0.1
        
        return max(0.0, min(score, 1.0))

    async def _update_engagement_profile(
        self,
        student_id: str,
        current_profile: Optional[StudentEngagementProfile],
        engagement_analysis: EngagementAnalysis,
        learning_profile: Optional[LearningProfile]
    ) -> StudentEngagementProfile:
        """Update or create student engagement profile"""
        
        if current_profile:
            updated_profile = current_profile.model_copy()
        else:
            updated_profile = StudentEngagementProfile(
                student_id=student_id,
                current_engagement_level=EngagementLevel.MODERATE,
                engagement_score=0.5
            )
        
        # Update engagement score
        overall_engagement = self._calculate_overall_engagement(
            engagement_analysis.engagement_trends,
            engagement_analysis.behavioral_patterns
        )
        updated_profile.engagement_score = overall_engagement
        
        # Update engagement level
        if overall_engagement >= 0.8:
            updated_profile.current_engagement_level = EngagementLevel.VERY_HIGH
        elif overall_engagement >= 0.6:
            updated_profile.current_engagement_level = EngagementLevel.HIGH
        elif overall_engagement >= 0.4:
            updated_profile.current_engagement_level = EngagementLevel.MODERATE
        elif overall_engagement >= 0.2:
            updated_profile.current_engagement_level = EngagementLevel.LOW
        else:
            updated_profile.current_engagement_level = EngagementLevel.VERY_LOW
        
        # Update metrics from analysis
        trends = engagement_analysis.engagement_trends
        updated_profile.session_duration_avg = trends.get("average_time_investment", 0.0)
        updated_profile.interaction_frequency = trends.get("daily_sessions", 0.0)
        
        patterns = engagement_analysis.behavioral_patterns
        challenge_behavior = patterns.get("challenge_behavior", {})
        updated_profile.challenge_acceptance_rate = challenge_behavior.get("challenge_acceptance_rate", 0.0)
        
        # Update risk assessment
        updated_profile.disengagement_risk = 1.0 - overall_engagement
        updated_profile.intervention_needed = len(engagement_analysis.risk_factors) > 2
        
        # Update gamification preferences based on effectiveness
        effectiveness = engagement_analysis.gamification_effectiveness
        preferred_elements = [
            GamificationElement(element) for element, score in effectiveness.items()
            if score > 0.5
        ]
        updated_profile.preferred_gamification = preferred_elements[:3]  # Top 3
        
        updated_profile.updated_at = datetime.utcnow()
        
        return updated_profile

    async def _detect_motivation_types(
        self,
        engagement_events: List[EngagementEvent],
        assessment_results: List[AssessmentResult],
        learning_profile: Optional[LearningProfile]
    ) -> List[MotivationType]:
        """Detect primary motivation types for the student"""
        
        motivation_scores = {mt: 0.0 for mt in MotivationType}
        
        # Analyze events for motivation indicators
        for event in engagement_events:
            event_type = event.event_type
            event_data = event.event_data
            
            # Intrinsic motivation indicators
            if event_type in ["content_explored", "question_asked", "concept_investigated"]:
                motivation_scores[MotivationType.INTRINSIC] += 0.1
            
            # Extrinsic motivation indicators
            if event_type in ["badge_earned", "points_awarded", "level_advanced"]:
                motivation_scores[MotivationType.EXTRINSIC] += 0.1
            
            # Achievement motivation indicators
            if event_type in ["challenge_completed", "goal_reached", "milestone_achieved"]:
                motivation_scores[MotivationType.ACHIEVEMENT] += 0.1
            
            # Social motivation indicators
            if event_type in ["shared_achievement", "peer_interaction", "group_activity"]:
                motivation_scores[MotivationType.SOCIAL] += 0.1
            
            # Autonomy motivation indicators
            if event_type in ["customized_setting", "chose_topic", "self_paced"]:
                motivation_scores[MotivationType.AUTONOMY] += 0.1
        
        # Consider learning style for motivation type correlation
        if learning_profile and learning_profile.preferred_learning_styles:
            primary_style = learning_profile.preferred_learning_styles[0].style
            
            if primary_style == LearningStyle.VISUAL:
                motivation_scores[MotivationType.ACHIEVEMENT] += 0.2
            elif primary_style == LearningStyle.AUDITORY:
                motivation_scores[MotivationType.SOCIAL] += 0.2
            elif primary_style == LearningStyle.KINESTHETIC:
                motivation_scores[MotivationType.INTRINSIC] += 0.2
            elif primary_style == LearningStyle.READING:
                motivation_scores[MotivationType.AUTONOMY] += 0.2
        
        # Return top motivation types
        sorted_motivations = sorted(motivation_scores.items(), key=lambda x: x[1], reverse=True)
        return [motivation for motivation, score in sorted_motivations[:3] if score > 0.1]

    async def _generate_interventions(
        self,
        engagement_profile: StudentEngagementProfile,
        engagement_analysis: EngagementAnalysis,
        intervention_preferences: List[str]
    ) -> List[MotivationIntervention]:
        """Generate targeted motivation interventions"""
        
        interventions = []
        
        # Low engagement interventions
        if engagement_profile.current_engagement_level in [EngagementLevel.VERY_LOW, EngagementLevel.LOW]:
            
            interventions.append(MotivationIntervention(
                intervention_id=f"encouragement_{engagement_profile.student_id}",
                student_id=engagement_profile.student_id,
                intervention_type="encouragement",
                title="You're Doing Great!",
                message="Every expert was once a beginner. Keep going - you're making progress!",
                suggested_actions=[
                    "Try an easier topic to build confidence",
                    "Take a short break if needed",
                    "Review your recent achievements"
                ],
                gamification_elements=[GamificationElement.POINTS, GamificationElement.BADGES],
                priority=5,
                estimated_impact=0.3
            ))
        
        # Streak building intervention
        if engagement_profile.streak_days < 3:
            interventions.append(MotivationIntervention(
                intervention_id=f"streak_building_{engagement_profile.student_id}",
                student_id=engagement_profile.student_id,
                intervention_type="habit_building",
                title="Build Your Learning Streak",
                message="Learning a little each day builds strong habits. Can you study for just 10 minutes today?",
                suggested_actions=[
                    "Set a daily reminder",
                    "Start with one easy question",
                    "Choose your favorite subject"
                ],
                gamification_elements=[GamificationElement.STREAKS, GamificationElement.POINTS],
                priority=3,
                estimated_impact=0.4
            ))
        
        # Challenge intervention for high performers
        if engagement_profile.current_engagement_level == EngagementLevel.VERY_HIGH:
            interventions.append(MotivationIntervention(
                intervention_id=f"advanced_challenge_{engagement_profile.student_id}",
                student_id=engagement_profile.student_id,
                intervention_type="challenge",
                title="Ready for a Challenge?",
                message="You've been doing amazing! Want to try something more challenging?",
                suggested_actions=[
                    "Attempt a harder difficulty level",
                    "Try a new subject area",
                    "Complete a special challenge quest"
                ],
                gamification_elements=[GamificationElement.CHALLENGES, GamificationElement.ACHIEVEMENTS],
                priority=2,
                estimated_impact=0.6
            ))
        
        # Break suggestion for overengaged students
        if engagement_profile.session_duration_avg > 60:  # More than 1 hour average
            interventions.append(MotivationIntervention(
                intervention_id=f"break_suggestion_{engagement_profile.student_id}",
                student_id=engagement_profile.student_id,
                intervention_type="break_suggestion",
                title="Time for a Break?",
                message="You've been studying hard! Remember to take breaks to stay fresh and focused.",
                suggested_actions=[
                    "Take a 10-minute break",
                    "Do some physical activity",
                    "Come back when you feel refreshed"
                ],
                gamification_elements=[],
                priority=4,
                estimated_impact=0.3,
                expires_at=datetime.utcnow() + timedelta(hours=1)
            ))
        
        # Motivation-type specific interventions
        for motivation_type in engagement_profile.motivation_types:
            if motivation_type == MotivationType.SOCIAL:
                interventions.append(MotivationIntervention(
                    intervention_id=f"social_{engagement_profile.student_id}",
                    student_id=engagement_profile.student_id,
                    intervention_type="social_engagement",
                    title="Learn with Friends",
                    message="Learning is more fun with others! Share your progress with friends or family.",
                    suggested_actions=[
                        "Share an achievement",
                        "Challenge a friend",
                        "Join a study group"
                    ],
                    gamification_elements=[GamificationElement.LEADERBOARDS],
                    priority=3,
                    estimated_impact=0.5
                ))
        
        return interventions

    async def _check_gamification_rewards(
        self,
        engagement_profile: StudentEngagementProfile,
        engagement_events: List[EngagementEvent]
    ) -> List[GamificationReward]:
        """Check for earned gamification rewards"""
        
        rewards = []
        
        # Count various achievements from events
        question_events = [e for e in engagement_events if e.event_type == "question_answered"]
        consecutive_days = engagement_profile.streak_days
        
        # First answer reward
        if len(question_events) == 1 and "first_answer" not in engagement_profile.badges_earned:
            rewards.append(self.reward_templates["first_answer"])
        
        # Streak rewards
        if consecutive_days >= 7 and "streak_7" not in engagement_profile.badges_earned:
            rewards.append(self.reward_templates["streak_7"])
        
        # Perfect score rewards (would need assessment data)
        # This would be checked against recent assessment results
        
        # Level up rewards
        # This would be based on points accumulated
        
        return rewards

    def _generate_long_term_strategies(
        self,
        engagement_profile: StudentEngagementProfile,
        engagement_analysis: EngagementAnalysis
    ) -> List[str]:
        """Generate long-term engagement strategies"""
        
        strategies = []
        
        # Based on engagement level
        if engagement_profile.current_engagement_level == EngagementLevel.VERY_LOW:
            strategies.extend([
                "Focus on building basic learning habits with minimal daily commitments",
                "Use immediate, small rewards to create positive associations",
                "Gradually increase session duration as engagement improves",
                "Consider one-on-one support or tutoring"
            ])
        elif engagement_profile.current_engagement_level == EngagementLevel.HIGH:
            strategies.extend([
                "Introduce advanced topics and challenging content",
                "Provide opportunities for peer mentoring or teaching",
                "Create long-term learning projects and goals",
                "Encourage exploration of related subjects"
            ])
        
        # Based on motivation types
        for motivation_type in engagement_profile.motivation_types:
            if motivation_type == MotivationType.INTRINSIC:
                strategies.append("Provide opportunities for self-directed learning and exploration")
            elif motivation_type == MotivationType.EXTRINSIC:
                strategies.append("Maintain consistent reward systems and recognition programs")
            elif motivation_type == MotivationType.SOCIAL:
                strategies.append("Create group learning opportunities and peer interaction")
            elif motivation_type == MotivationType.ACHIEVEMENT:
                strategies.append("Set clear milestones and celebrate goal completions")
            elif motivation_type == MotivationType.AUTONOMY:
                strategies.append("Provide choices in content, pace, and learning paths")
        
        # Based on risk factors
        for risk_factor in engagement_analysis.risk_factors:
            if "inconsistent" in risk_factor.lower():
                strategies.append("Implement reminder systems and habit-building techniques")
            elif "low performance" in risk_factor.lower():
                strategies.append("Adjust content difficulty and provide additional support")
        
        return list(set(strategies))  # Remove duplicates

    def _create_monitoring_schedule(self, engagement_profile: StudentEngagementProfile) -> Dict[str, int]:
        """Create monitoring schedule based on engagement level"""
        
        base_schedule = {
            "engagement_score": 24,      # Check daily
            "session_frequency": 12,     # Check twice daily
            "performance_trends": 72,    # Check every 3 days
            "risk_assessment": 48        # Check every 2 days
        }
        
        # Adjust frequency based on engagement level and risk
        if engagement_profile.current_engagement_level == EngagementLevel.VERY_LOW:
            # More frequent monitoring for at-risk students
            base_schedule = {k: v // 2 for k, v in base_schedule.items()}
        elif engagement_profile.current_engagement_level == EngagementLevel.VERY_HIGH:
            # Less frequent monitoring for highly engaged students
            base_schedule = {k: int(v * 1.5) for k, v in base_schedule.items()}
        
        return base_schedule

    def _estimate_intervention_success(
        self,
        engagement_profile: StudentEngagementProfile,
        interventions: List[MotivationIntervention],
        engagement_analysis: EngagementAnalysis
    ) -> float:
        """Estimate probability of intervention success"""
        
        base_probability = 0.6  # Base 60% success probability
        
        # Adjust based on current engagement level
        engagement_adjustments = {
            EngagementLevel.VERY_LOW: -0.2,
            EngagementLevel.LOW: -0.1,
            EngagementLevel.MODERATE: 0.0,
            EngagementLevel.HIGH: 0.1,
            EngagementLevel.VERY_HIGH: 0.05  # Slight boost, but already high
        }
        
        base_probability += engagement_adjustments.get(engagement_profile.current_engagement_level, 0.0)
        
        # Adjust based on intervention quality and fit
        if interventions:
            avg_estimated_impact = statistics.mean(i.estimated_impact for i in interventions)
            base_probability += (avg_estimated_impact - 0.5) * 0.2
        
        # Adjust based on motivation type alignment
        if engagement_profile.motivation_types:
            base_probability += len(engagement_profile.motivation_types) * 0.05
        
        # Adjust based on positive indicators vs risk factors
        positive_count = len(engagement_analysis.positive_indicators)
        risk_count = len(engagement_analysis.risk_factors)
        
        if positive_count > risk_count:
            base_probability += 0.1
        elif risk_count > positive_count:
            base_probability -= 0.1
        
        return max(0.1, min(base_probability, 0.95))

    async def get_agent_status(self) -> Dict[str, Any]:
        """Get agent status and health"""
        return {
            "name": "EngagementAgent",
            "status": "active",
            "models_available": {
                "openai": self.openai_model is not None,
                "anthropic": self.anthropic_model is not None
            },
            "supported_engagement_levels": [level.value for level in EngagementLevel],
            "supported_motivation_types": [mt.value for mt in MotivationType],
            "gamification_elements": [ge.value for ge in GamificationElement],
            "reward_templates_loaded": len(self.reward_templates),
            "engagement_weights_configured": len(self.engagement_weights) > 0,
            "curriculum_loaded": self.curriculum is not None
        }