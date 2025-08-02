"""
Analytics Agent - Phase 4 Implementation
Provides comprehensive learning analytics, performance insights, and educational data intelligence.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime, timedelta
from enum import Enum
import statistics
import json
from collections import defaultdict

from pydantic import BaseModel, Field
import openai
from anthropic import Anthropic

from config.settings import settings
from core.curriculum import CBSECurriculum
from core.exceptions import AgentException
from agents.content_generator import DifficultyLevel, QuestionType
from agents.assessment_agent import AssessmentResult, PerformanceMetrics
from agents.adaptive_learning_agent import LearningProfile, LearningStyle, LearningPace
from agents.engagement_agent import StudentEngagementProfile, EngagementLevel, MotivationType


class AnalyticsTimeFrame(str, Enum):
    """Time frames for analytics"""
    DAILY = "daily"
    WEEKLY = "weekly" 
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"
    ALL_TIME = "all_time"


class MetricType(str, Enum):
    """Types of metrics to analyze"""
    PERFORMANCE = "performance"        # Academic performance metrics
    ENGAGEMENT = "engagement"          # Student engagement metrics
    LEARNING_PACE = "learning_pace"    # Learning speed and consistency
    CONTENT_USAGE = "content_usage"    # Content interaction patterns
    SKILL_MASTERY = "skill_mastery"    # Subject and skill proficiency
    BEHAVIORAL = "behavioral"          # Learning behavior patterns


class InsightType(str, Enum):
    """Types of insights generated"""
    STRENGTH = "strength"              # Areas where student excels
    WEAKNESS = "weakness"              # Areas needing improvement
    TREND = "trend"                    # Performance/behavior trends
    PREDICTION = "prediction"          # Future performance predictions
    RECOMMENDATION = "recommendation"  # Actionable recommendations
    ALERT = "alert"                    # Important attention items


class AnalyticsMetric(BaseModel):
    """Individual analytics metric"""
    metric_id: str
    metric_name: str
    metric_type: MetricType
    value: float
    description: str = Field(default="", description="Description of the metric")
    unit: str = Field(default="", description="Unit of measurement")
    timeframe: AnalyticsTimeFrame
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    trend_direction: str = Field(default="stable", description="improving, declining, stable")
    benchmark_comparison: Optional[float] = Field(default=None, description="Comparison to peer average")
    percentile_rank: Optional[int] = Field(default=None, ge=0, le=100)
    last_updated: datetime = Field(default_factory=datetime.utcnow)


class LearningInsight(BaseModel):
    """Individual learning insight"""
    insight_id: str
    insight_type: InsightType
    title: str
    description: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    severity: int = Field(default=3, ge=1, le=5, description="1=low, 5=critical")
    supporting_data: Dict[str, Any] = Field(default_factory=dict)
    actionable_items: List[str] = Field(default_factory=list)
    related_subjects: List[str] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=datetime.utcnow)


class SubjectAnalytics(BaseModel):
    """Analytics for a specific subject"""
    subject: str
    grade: int
    overall_mastery: float = Field(..., ge=0.0, le=1.0)
    performance_trend: str = Field(default="stable")
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    topic_mastery: Dict[str, float] = Field(default_factory=dict)
    skill_gaps: List[str] = Field(default_factory=list)
    recommended_focus_areas: List[str] = Field(default_factory=list)
    estimated_time_to_mastery: int = Field(default=0, description="Hours needed for full mastery")


class LearningJourney(BaseModel):
    """Student's learning journey over time"""
    student_id: str
    journey_start: datetime
    total_learning_hours: float
    subjects_covered: List[str]
    milestones_achieved: List[str] = Field(default_factory=list)
    challenges_overcome: List[str] = Field(default_factory=list)
    learning_velocity: float = Field(default=0.0, description="Topics mastered per week")
    consistency_score: float = Field(default=0.0, ge=0.0, le=1.0)
    breakthrough_moments: List[Dict[str, Any]] = Field(default_factory=list)


class PeerComparison(BaseModel):
    """Comparison with peer performance"""
    student_percentile: int = Field(..., ge=0, le=100)
    grade_average: float
    subject_rankings: Dict[str, int] = Field(default_factory=dict)
    relative_strengths: List[str] = Field(default_factory=list)
    improvement_areas: List[str] = Field(default_factory=list)
    peer_group_size: int = Field(default=0)


class PredictiveModel(BaseModel):
    """Predictive analytics for student outcomes"""
    student_id: str
    prediction_type: str  # "performance", "engagement", "mastery"
    predicted_outcome: Dict[str, float] = Field(default_factory=dict)
    confidence_interval: Tuple[float, float] = Field(default=(0.0, 1.0))
    prediction_accuracy: float = Field(default=0.0, ge=0.0, le=1.0)
    key_factors: List[str] = Field(default_factory=list)
    prediction_horizon_days: int = Field(default=30)
    model_version: str = Field(default="v1.0")


class AnalyticsReport(BaseModel):
    """Comprehensive analytics report"""
    student_id: str
    report_id: str
    report_type: str = Field(default="comprehensive")
    timeframe: AnalyticsTimeFrame
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Core metrics
    key_metrics: List[AnalyticsMetric] = Field(default_factory=list)
    learning_insights: List[LearningInsight] = Field(default_factory=list)
    subject_analytics: List[SubjectAnalytics] = Field(default_factory=list)
    
    # Advanced analytics
    learning_journey: Optional[LearningJourney] = Field(default=None)
    peer_comparison: Optional[PeerComparison] = Field(default=None)
    predictive_models: List[PredictiveModel] = Field(default_factory=list)
    
    # Summary
    overall_summary: str = Field(default="")
    priority_recommendations: List[str] = Field(default_factory=list)
    success_probability: float = Field(default=0.5, ge=0.0, le=1.0)


class AnalyticsRequest(BaseModel):
    """Request for analytics generation"""
    student_id: str
    timeframe: AnalyticsTimeFrame = Field(default=AnalyticsTimeFrame.WEEKLY)
    metric_types: List[MetricType] = Field(default_factory=lambda: list(MetricType))
    include_predictions: bool = Field(default=True)
    include_peer_comparison: bool = Field(default=False)
    assessment_results: List[AssessmentResult] = Field(default_factory=list)
    learning_profile: Optional[LearningProfile] = Field(default=None)
    engagement_profile: Optional[StudentEngagementProfile] = Field(default=None)
    custom_filters: Dict[str, Any] = Field(default_factory=dict)


class AnalyticsAgent:
    """
    Analytics Agent for comprehensive learning analytics and insights
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.AnalyticsAgent")
        self.curriculum = CBSECurriculum()
        self.openai_model = None
        self.anthropic_model = None
        self._initialize_models()
        
        # Analytics configurations
        self.metric_weights = {
            MetricType.PERFORMANCE: 0.25,
            MetricType.ENGAGEMENT: 0.20,
            MetricType.LEARNING_PACE: 0.15,
            MetricType.CONTENT_USAGE: 0.15,
            MetricType.SKILL_MASTERY: 0.15,
            MetricType.BEHAVIORAL: 0.10
        }
        
        # Benchmark data (simplified - in production would come from database)
        self.benchmarks = {
            "grade_1": {"performance": 0.65, "engagement": 0.70, "mastery": 0.60},
            "grade_2": {"performance": 0.68, "engagement": 0.72, "mastery": 0.65},
            "grade_3": {"performance": 0.70, "engagement": 0.73, "mastery": 0.68},
            "grade_4": {"performance": 0.72, "engagement": 0.74, "mastery": 0.70},
            "grade_5": {"performance": 0.74, "engagement": 0.75, "mastery": 0.72}
        }

    def _initialize_models(self):
        """Initialize AI models for analytics"""
        try:
            if hasattr(settings, 'openai_api_key') and settings.openai_api_key:
                openai.api_key = settings.openai_api_key
                self.openai_model = "gpt-4-turbo-preview"
                
            if hasattr(settings, 'anthropic_api_key') and settings.anthropic_api_key:
                self.anthropic_model = Anthropic(api_key=settings.anthropic_api_key)
                
            self.logger.info("Analytics AI models initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize AI models: {e}")
            self.logger.warning("Continuing without AI models for testing purposes")

    async def generate_analytics_report(self, request: AnalyticsRequest) -> AnalyticsReport:
        """
        Main method to generate comprehensive analytics report
        """
        try:
            self.logger.info(f"Generating analytics report for student {request.student_id}")
            
            # Generate key metrics
            key_metrics = await self._calculate_key_metrics(
                request.student_id, request.assessment_results, request.learning_profile,
                request.engagement_profile, request.timeframe, request.metric_types
            )
            
            # Generate learning insights
            learning_insights = await self._generate_learning_insights(
                request.student_id, key_metrics, request.assessment_results,
                request.learning_profile, request.engagement_profile
            )
            
            # Generate subject analytics
            subject_analytics = await self._analyze_subject_performance(
                request.assessment_results, request.learning_profile
            )
            
            # Generate learning journey
            learning_journey = await self._create_learning_journey(
                request.student_id, request.assessment_results, request.engagement_profile
            )
            
            # Generate peer comparison if requested
            peer_comparison = None
            if request.include_peer_comparison:
                peer_comparison = await self._generate_peer_comparison(
                    request.student_id, key_metrics, request.learning_profile
                )
            
            # Generate predictive models if requested
            predictive_models = []
            if request.include_predictions:
                predictive_models = await self._generate_predictive_models(
                    request.student_id, key_metrics, request.assessment_results,
                    request.learning_profile, request.engagement_profile
                )
            
            # Generate overall summary and recommendations
            overall_summary = await self._generate_overall_summary(
                key_metrics, learning_insights, subject_analytics
            )
            
            priority_recommendations = self._generate_priority_recommendations(
                learning_insights, subject_analytics, predictive_models
            )
            
            # Calculate success probability
            success_probability = self._calculate_success_probability(
                key_metrics, learning_insights, predictive_models
            )
            
            report = AnalyticsReport(
                student_id=request.student_id,
                report_id=f"analytics_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{request.student_id}",
                timeframe=request.timeframe,
                key_metrics=key_metrics,
                learning_insights=learning_insights,
                subject_analytics=subject_analytics,
                learning_journey=learning_journey,
                peer_comparison=peer_comparison,
                predictive_models=predictive_models,
                overall_summary=overall_summary,
                priority_recommendations=priority_recommendations,
                success_probability=success_probability
            )
            
            self.logger.info(f"Analytics report generated for student {request.student_id}")
            return report
            
        except Exception as e:
            self.logger.error(f"Analytics report generation failed: {e}")
            raise AgentException(f"Analytics report generation failed: {e}")

    async def _calculate_key_metrics(
        self,
        student_id: str,
        assessment_results: List[AssessmentResult],
        learning_profile: Optional[LearningProfile],
        engagement_profile: Optional[StudentEngagementProfile],
        timeframe: AnalyticsTimeFrame,
        metric_types: List[MetricType]
    ) -> List[AnalyticsMetric]:
        """Calculate key performance and learning metrics"""
        
        metrics = []
        
        # Performance metrics
        if MetricType.PERFORMANCE in metric_types and assessment_results:
            performance_scores = [r.performance_metrics.overall_score for r in assessment_results]
            
            metrics.append(AnalyticsMetric(
                metric_id="avg_performance",
                metric_name="Average Performance",
                metric_type=MetricType.PERFORMANCE,
                value=statistics.mean(performance_scores),
                description="Average academic performance across all assessments",
                unit="score",
                timeframe=timeframe,
                trend_direction=self._calculate_trend(performance_scores),
                percentile_rank=self._calculate_percentile_rank(statistics.mean(performance_scores))
            ))
            
            # Performance consistency
            consistency = 1.0 - (statistics.stdev(performance_scores) if len(performance_scores) > 1 else 0.0)
            metrics.append(AnalyticsMetric(
                metric_id="performance_consistency",
                metric_name="Performance Consistency",
                metric_type=MetricType.PERFORMANCE,
                value=max(0.0, consistency),
                description="Consistency of performance across assessments",
                unit="consistency",
                timeframe=timeframe
            ))
        
        # Engagement metrics
        if MetricType.ENGAGEMENT in metric_types and engagement_profile:
            metrics.append(AnalyticsMetric(
                metric_id="engagement_score",
                metric_name="Engagement Score",
                metric_type=MetricType.ENGAGEMENT,
                value=engagement_profile.engagement_score,
                description="Overall student engagement with learning content",
                unit="score",
                timeframe=timeframe,
                percentile_rank=self._calculate_percentile_rank(engagement_profile.engagement_score)
            ))
            
            metrics.append(AnalyticsMetric(
                metric_id="session_frequency",
                metric_name="Learning Session Frequency",
                metric_type=MetricType.ENGAGEMENT,
                value=engagement_profile.interaction_frequency,
                description="Frequency of learning session interactions per day",
                unit="sessions/day",
                timeframe=timeframe
            ))
        
        # Learning pace metrics
        if MetricType.LEARNING_PACE in metric_types and learning_profile:
            pace_score = {"slow": 0.3, "moderate": 0.6, "fast": 0.9}.get(
                learning_profile.learning_pace.value, 0.6
            )
            
            metrics.append(AnalyticsMetric(
                metric_id="learning_pace",
                metric_name="Learning Pace",
                metric_type=MetricType.LEARNING_PACE,
                value=pace_score,
                description="Rate of learning progress and adaptation speed",
                unit="pace",
                timeframe=timeframe
            ))
        
        # Content usage metrics
        if MetricType.CONTENT_USAGE in metric_types and assessment_results:
            total_questions = sum(r.performance_metrics.total_questions for r in assessment_results)
            avg_time = statistics.mean([
                r.performance_metrics.completion_time or 0 
                for r in assessment_results
            ]) if assessment_results else 0
            
            metrics.append(AnalyticsMetric(
                metric_id="content_usage",
                metric_name="Content Interaction Volume",
                metric_type=MetricType.CONTENT_USAGE,
                value=total_questions,
                description="Total number of questions and content interactions",
                unit="questions",
                timeframe=timeframe
            ))
            
            if avg_time > 0:
                metrics.append(AnalyticsMetric(
                    metric_id="avg_response_time",
                    metric_name="Average Response Time",
                    metric_type=MetricType.CONTENT_USAGE,
                    value=avg_time / 60.0,  # Convert to minutes
                    description="Average time spent responding to questions",
                    unit="minutes",
                    timeframe=timeframe
                ))
        
        # Skill mastery metrics
        if MetricType.SKILL_MASTERY in metric_types and assessment_results:
            subject_mastery = {}
            for result in assessment_results:
                subject = result.subject
                if subject not in subject_mastery:
                    subject_mastery[subject] = []
                subject_mastery[subject].append(result.performance_metrics.overall_score)
            
            for subject, scores in subject_mastery.items():
                metrics.append(AnalyticsMetric(
                    metric_id=f"mastery_{subject.lower()}",
                    metric_name=f"{subject} Mastery",
                    metric_type=MetricType.SKILL_MASTERY,
                    value=statistics.mean(scores),
                    description=f"Average mastery level in {subject}",
                    unit="mastery",
                    timeframe=timeframe,
                    trend_direction=self._calculate_trend(scores)
                ))
        
        # Behavioral metrics
        if MetricType.BEHAVIORAL in metric_types:
            if engagement_profile:
                metrics.append(AnalyticsMetric(
                    metric_id="help_seeking_rate",
                    metric_name="Help Seeking Rate",
                    metric_type=MetricType.BEHAVIORAL,
                    value=engagement_profile.help_seeking_rate,
                    description="Frequency of seeking help when struggling",
                    unit="rate",
                    timeframe=timeframe
                ))
                
                metrics.append(AnalyticsMetric(
                    metric_id="challenge_acceptance",
                    metric_name="Challenge Acceptance Rate",
                    metric_type=MetricType.BEHAVIORAL,
                    value=engagement_profile.challenge_acceptance_rate,
                    description="Rate of accepting challenging content and tasks",
                    unit="rate",
                    timeframe=timeframe
                ))
        
        return metrics

    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction from a series of values"""
        if len(values) < 2:
            return "stable"
        
        # Simple linear trend
        n = len(values)
        sum_x = sum(range(n))
        sum_y = sum(values)
        sum_xy = sum(i * values[i] for i in range(n))
        sum_x2 = sum(i * i for i in range(n))
        
        if n * sum_x2 - sum_x * sum_x == 0:
            slope = 0
        else:
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        
        if slope > 0.05:
            return "improving"
        elif slope < -0.05:
            return "declining"
        else:
            return "stable"

    def _calculate_percentile_rank(self, score: float) -> int:
        """Calculate percentile rank (simplified)"""
        # In production, this would compare against actual peer data
        # For now, use a simple mapping
        if score >= 0.9:
            return 95
        elif score >= 0.8:
            return 80
        elif score >= 0.7:
            return 65
        elif score >= 0.6:
            return 50
        elif score >= 0.5:
            return 35
        elif score >= 0.4:
            return 20
        else:
            return 10

    async def _generate_learning_insights(
        self,
        student_id: str,
        metrics: List[AnalyticsMetric],
        assessment_results: List[AssessmentResult],
        learning_profile: Optional[LearningProfile],
        engagement_profile: Optional[StudentEngagementProfile]
    ) -> List[LearningInsight]:
        """Generate actionable learning insights"""
        
        insights = []
        
        # Performance insights
        performance_metrics = [m for m in metrics if m.metric_type == MetricType.PERFORMANCE]
        if performance_metrics:
            avg_performance = next(m for m in performance_metrics if m.metric_id == "avg_performance")
            
            if avg_performance.value >= 0.8:
                insights.append(LearningInsight(
                    insight_id=f"strength_high_performance_{student_id}",
                    insight_type=InsightType.STRENGTH,
                    title="Strong Academic Performance",
                    description=f"Consistently high performance with {avg_performance.value:.1%} average score",
                    confidence=0.9,
                    severity=2,
                    supporting_data={"avg_score": avg_performance.value},
                    actionable_items=["Consider advanced topics", "Explore enrichment activities"],
                    related_subjects=list(set(r.subject for r in assessment_results))
                ))
            elif avg_performance.value < 0.5:
                insights.append(LearningInsight(
                    insight_id=f"weakness_low_performance_{student_id}",
                    insight_type=InsightType.WEAKNESS,
                    title="Below Average Performance",
                    description=f"Performance at {avg_performance.value:.1%} indicates need for additional support",
                    confidence=0.85,
                    severity=4,
                    supporting_data={"avg_score": avg_performance.value},
                    actionable_items=["Review fundamentals", "Increase practice time", "Consider tutoring"],
                    related_subjects=list(set(r.subject for r in assessment_results))
                ))
        
        # Engagement insights
        if engagement_profile:
            if engagement_profile.current_engagement_level in [EngagementLevel.VERY_LOW, EngagementLevel.LOW]:
                insights.append(LearningInsight(
                    insight_id=f"alert_low_engagement_{student_id}",
                    insight_type=InsightType.ALERT,
                    title="Low Engagement Alert",
                    description=f"Engagement level is {engagement_profile.current_engagement_level.value}",
                    confidence=0.9,
                    severity=5,
                    supporting_data={"engagement_level": engagement_profile.current_engagement_level.value},
                    actionable_items=["Implement motivation strategies", "Adjust content difficulty", "Increase gamification"]
                ))
            
            if engagement_profile.streak_days > 7:
                insights.append(LearningInsight(
                    insight_id=f"strength_consistency_{student_id}",
                    insight_type=InsightType.STRENGTH,
                    title="Excellent Learning Consistency",
                    description=f"Maintained learning streak for {engagement_profile.streak_days} days",
                    confidence=0.95,
                    severity=1,
                    supporting_data={"streak_days": engagement_profile.streak_days},
                    actionable_items=["Celebrate achievement", "Set higher goals"]
                ))
        
        # Learning pace insights
        if learning_profile:
            pace = learning_profile.learning_pace
            if pace == LearningPace.FAST:
                insights.append(LearningInsight(
                    insight_id=f"strength_fast_learner_{student_id}",
                    insight_type=InsightType.STRENGTH,
                    title="Fast Learning Pace",
                    description="Student demonstrates rapid concept acquisition",
                    confidence=0.8,
                    severity=2,
                    supporting_data={"learning_pace": pace.value},
                    actionable_items=["Provide advanced challenges", "Increase content complexity"]
                ))
            elif pace == LearningPace.SLOW:
                insights.append(LearningInsight(
                    insight_id=f"recommendation_pace_support_{student_id}",
                    insight_type=InsightType.RECOMMENDATION,
                    title="Provide Additional Learning Support",
                    description="Student would benefit from extended practice time",
                    confidence=0.75,
                    severity=3,
                    supporting_data={"learning_pace": pace.value},
                    actionable_items=["Allow more time per topic", "Provide step-by-step guidance", "Offer additional practice"]
                ))
        
        # Trend insights
        trend_metrics = [m for m in metrics if hasattr(m, 'trend_direction')]
        improving_trends = [m for m in trend_metrics if m.trend_direction == "improving"]
        declining_trends = [m for m in trend_metrics if m.trend_direction == "declining"]
        
        if improving_trends:
            insights.append(LearningInsight(
                insight_id=f"trend_positive_{student_id}",
                insight_type=InsightType.TREND,
                title="Positive Learning Trend",
                description=f"Showing improvement in {len(improving_trends)} key metrics",
                confidence=0.8,
                severity=2,
                supporting_data={"improving_metrics": len(improving_trends)},
                actionable_items=["Continue current strategies", "Monitor progress"]
            ))
        
        if declining_trends:
            insights.append(LearningInsight(
                insight_id=f"trend_concerning_{student_id}",
                insight_type=InsightType.TREND,
                title="Declining Performance Trend",
                description=f"Showing decline in {len(declining_trends)} key metrics",
                confidence=0.8,
                severity=4,
                supporting_data={"declining_metrics": len(declining_trends)},
                actionable_items=["Investigate causes", "Adjust learning approach", "Provide additional support"]
            ))
        
        return insights

    async def _analyze_subject_performance(
        self,
        assessment_results: List[AssessmentResult],
        learning_profile: Optional[LearningProfile]
    ) -> List[SubjectAnalytics]:
        """Analyze performance by subject"""
        
        subject_analytics = []
        
        # Group results by subject
        subjects = defaultdict(list)
        for result in assessment_results:
            subjects[result.subject].append(result)
        
        for subject, results in subjects.items():
            # Calculate overall mastery
            overall_scores = [r.performance_metrics.overall_score for r in results]
            overall_mastery = statistics.mean(overall_scores) if overall_scores else 0.0
            
            # Determine performance trend
            performance_trend = self._calculate_trend(overall_scores)
            
            # Identify strengths and weaknesses
            strengths = []
            weaknesses = []
            topic_mastery = {}
            
            for result in results:
                topic = result.topic
                score = result.performance_metrics.overall_score
                topic_mastery[topic] = score
                
                if score >= 0.8:
                    strengths.append(topic)
                elif score < 0.5:
                    weaknesses.append(topic)
            
            # Identify skill gaps (topics with consistently low performance)
            skill_gaps = [topic for topic, score in topic_mastery.items() if score < 0.4]
            
            # Recommend focus areas
            recommended_focus_areas = []
            if weaknesses:
                recommended_focus_areas.extend(weaknesses[:3])  # Top 3 weak areas
            if not strengths and not weaknesses:
                recommended_focus_areas.append("Continue balanced practice")
            
            # Estimate time to mastery (simplified calculation)
            current_mastery = overall_mastery
            if current_mastery < 0.8:
                remaining_mastery = 0.8 - current_mastery
                estimated_hours = int(remaining_mastery * 40)  # Rough estimate
            else:
                estimated_hours = 0
            
            # Determine grade (from first result - assuming same grade for subject)
            grade = results[0].grade if results else 1
            
            subject_analytics.append(SubjectAnalytics(
                subject=subject,
                grade=grade,
                overall_mastery=overall_mastery,
                performance_trend=performance_trend,
                strengths=list(set(strengths)),
                weaknesses=list(set(weaknesses)),
                topic_mastery=topic_mastery,
                skill_gaps=skill_gaps,
                recommended_focus_areas=recommended_focus_areas,
                estimated_time_to_mastery=estimated_hours
            ))
        
        return subject_analytics

    async def _create_learning_journey(
        self,
        student_id: str,
        assessment_results: List[AssessmentResult],
        engagement_profile: Optional[StudentEngagementProfile]
    ) -> LearningJourney:
        """Create learning journey visualization"""
        
        if not assessment_results:
            return LearningJourney(
                student_id=student_id,
                journey_start=datetime.utcnow(),
                total_learning_hours=0.0,
                subjects_covered=[]
            )
        
        # Calculate journey metrics
        journey_start = min(r.assessed_at for r in assessment_results)
        subjects_covered = list(set(r.subject for r in assessment_results))
        
        # Calculate total learning time (from assessment completion times)
        total_time_seconds = sum(
            r.performance_metrics.completion_time or 0 
            for r in assessment_results
        )
        total_learning_hours = total_time_seconds / 3600.0
        
        # Identify milestones (high scores, streaks, improvements)
        milestones_achieved = []
        for result in assessment_results:
            if result.performance_metrics.overall_score >= 0.9:
                milestones_achieved.append(f"Perfect score in {result.subject} - {result.topic}")
            if result.performance_metrics.correct_answers == result.performance_metrics.total_questions:
                milestones_achieved.append(f"100% accuracy in {result.topic}")
        
        # Identify challenges overcome
        challenges_overcome = []
        previous_scores = {}
        for result in sorted(assessment_results, key=lambda x: x.assessed_at):
            subject = result.subject
            current_score = result.performance_metrics.overall_score
            
            if subject in previous_scores:
                if current_score > previous_scores[subject] + 0.2:  # 20% improvement
                    challenges_overcome.append(f"Significant improvement in {subject}")
            
            previous_scores[subject] = current_score
        
        # Calculate learning velocity (topics mastered per week)
        weeks_elapsed = (datetime.utcnow() - journey_start).days / 7.0
        topics_mastered = sum(1 for r in assessment_results if r.performance_metrics.overall_score >= 0.7)
        learning_velocity = topics_mastered / max(weeks_elapsed, 1)
        
        # Calculate consistency score
        if engagement_profile:
            consistency_score = 1.0 - engagement_profile.disengagement_risk
        else:
            # Calculate from assessment frequency
            assessment_dates = [r.assessed_at.date() for r in assessment_results]
            unique_dates = len(set(assessment_dates))
            days_elapsed = (datetime.utcnow().date() - journey_start.date()).days
            consistency_score = min(unique_dates / max(days_elapsed, 1), 1.0)
        
        # Identify breakthrough moments
        breakthrough_moments = []
        for result in assessment_results:
            if result.performance_metrics.overall_score >= 0.95:
                breakthrough_moments.append({
                    "date": result.assessed_at.isoformat(),
                    "subject": result.subject,
                    "topic": result.topic,
                    "achievement": "Near-perfect performance",
                    "score": result.performance_metrics.overall_score
                })
        
        return LearningJourney(
            student_id=student_id,
            journey_start=journey_start,
            total_learning_hours=total_learning_hours,
            subjects_covered=subjects_covered,
            milestones_achieved=milestones_achieved[:5],  # Top 5
            challenges_overcome=challenges_overcome[:3],  # Top 3
            learning_velocity=learning_velocity,
            consistency_score=consistency_score,
            breakthrough_moments=breakthrough_moments[-3:]  # Most recent 3
        )

    async def _generate_peer_comparison(
        self,
        student_id: str,
        metrics: List[AnalyticsMetric],
        learning_profile: Optional[LearningProfile]
    ) -> PeerComparison:
        """Generate peer comparison data"""
        
        # Get grade level for comparison
        grade = 1
        if learning_profile:
            grade = list(learning_profile.current_difficulty_level.values())[0] if learning_profile.current_difficulty_level else 1
        
        # Get benchmark data for grade
        grade_key = f"grade_{grade}"
        grade_benchmarks = self.benchmarks.get(grade_key, self.benchmarks["grade_1"])
        
        # Calculate student percentile based on performance metrics
        performance_metrics = [m for m in metrics if m.metric_type == MetricType.PERFORMANCE]
        if performance_metrics:
            avg_performance = statistics.mean(m.value for m in performance_metrics)
            student_percentile = self._calculate_percentile_rank(avg_performance)
        else:
            student_percentile = 50
        
        # Calculate subject rankings
        subject_rankings = {}
        mastery_metrics = [m for m in metrics if m.metric_type == MetricType.SKILL_MASTERY]
        for metric in mastery_metrics:
            subject = metric.metric_name.replace(" Mastery", "")
            subject_rankings[subject] = self._calculate_percentile_rank(metric.value)
        
        # Identify relative strengths and improvement areas
        relative_strengths = []
        improvement_areas = []
        
        for subject, percentile in subject_rankings.items():
            if percentile >= 75:
                relative_strengths.append(f"Above average in {subject}")
            elif percentile <= 25:
                improvement_areas.append(f"Below average in {subject}")
        
        return PeerComparison(
            student_percentile=student_percentile,
            grade_average=grade_benchmarks.get("performance", 0.7),
            subject_rankings=subject_rankings,
            relative_strengths=relative_strengths,
            improvement_areas=improvement_areas,
            peer_group_size=100  # Simulated peer group size
        )

    async def _generate_predictive_models(
        self,
        student_id: str,
        metrics: List[AnalyticsMetric],
        assessment_results: List[AssessmentResult],
        learning_profile: Optional[LearningProfile],
        engagement_profile: Optional[StudentEngagementProfile]
    ) -> List[PredictiveModel]:
        """Generate predictive models for future performance"""
        
        predictive_models = []
        
        # Performance prediction
        performance_metrics = [m for m in metrics if m.metric_type == MetricType.PERFORMANCE]
        if performance_metrics:
            current_performance = statistics.mean(m.value for m in performance_metrics)
            
            # Simple trend-based prediction
            trend_adjustment = 0.0
            if any(m.trend_direction == "improving" for m in performance_metrics):
                trend_adjustment = 0.1
            elif any(m.trend_direction == "declining" for m in performance_metrics):
                trend_adjustment = -0.1
            
            predicted_performance = max(0.0, min(1.0, current_performance + trend_adjustment))
            confidence_lower = max(0.0, predicted_performance - 0.15)
            confidence_upper = min(1.0, predicted_performance + 0.15)
            
            predictive_models.append(PredictiveModel(
                student_id=student_id,
                prediction_type="performance",
                predicted_outcome={"overall_score": predicted_performance},
                confidence_interval=(confidence_lower, confidence_upper),
                prediction_accuracy=0.75,  # Estimated model accuracy
                key_factors=["Current performance trend", "Learning consistency", "Engagement level"],
                prediction_horizon_days=30
            ))
        
        # Engagement prediction
        if engagement_profile:
            current_engagement = engagement_profile.engagement_score
            risk_level = engagement_profile.disengagement_risk
            
            # Predict engagement stability
            predicted_engagement = max(0.0, min(1.0, current_engagement - (risk_level * 0.5)))
            
            predictive_models.append(PredictiveModel(
                student_id=student_id,
                prediction_type="engagement",
                predicted_outcome={"engagement_score": predicted_engagement},
                confidence_interval=(predicted_engagement - 0.2, predicted_engagement + 0.1),
                prediction_accuracy=0.7,
                key_factors=["Current engagement level", "Risk factors", "Motivation patterns"],
                prediction_horizon_days=14
            ))
        
        # Mastery prediction
        if assessment_results:
            subjects = set(r.subject for r in assessment_results)
            for subject in subjects:
                subject_results = [r for r in assessment_results if r.subject == subject]
                current_mastery = statistics.mean(r.performance_metrics.overall_score for r in subject_results)
                
                # Predict time to reach mastery threshold (0.8)
                if current_mastery < 0.8:
                    improvement_needed = 0.8 - current_mastery
                    # Estimate based on current learning rate
                    predicted_days = int(improvement_needed * 60)  # Rough estimate
                    
                    predictive_models.append(PredictiveModel(
                        student_id=student_id,
                        prediction_type="mastery",
                        predicted_outcome={
                            f"{subject}_mastery_date": predicted_days,
                            f"{subject}_probability": max(0.3, 1.0 - improvement_needed)
                        },
                        confidence_interval=(0.5, 0.9),
                        prediction_accuracy=0.65,
                        key_factors=[f"Current {subject} performance", "Learning pace", "Practice consistency"],
                        prediction_horizon_days=predicted_days
                    ))
        
        return predictive_models

    async def _generate_overall_summary(
        self,
        metrics: List[AnalyticsMetric],
        insights: List[LearningInsight],
        subject_analytics: List[SubjectAnalytics]
    ) -> str:
        """Generate overall summary of analytics"""
        
        summary_parts = []
        
        # Performance summary
        performance_metrics = [m for m in metrics if m.metric_type == MetricType.PERFORMANCE]
        if performance_metrics:
            avg_performance = statistics.mean(m.value for m in performance_metrics)
            summary_parts.append(f"Overall academic performance: {avg_performance:.1%}")
        
        # Engagement summary
        engagement_metrics = [m for m in metrics if m.metric_type == MetricType.ENGAGEMENT]
        if engagement_metrics:
            avg_engagement = statistics.mean(m.value for m in engagement_metrics)
            summary_parts.append(f"Student engagement level: {avg_engagement:.1%}")
        
        # Subject performance summary
        if subject_analytics:
            best_subject = max(subject_analytics, key=lambda s: s.overall_mastery)
            worst_subject = min(subject_analytics, key=lambda s: s.overall_mastery)
            
            summary_parts.append(f"Strongest subject: {best_subject.subject} ({best_subject.overall_mastery:.1%})")
            if best_subject != worst_subject:
                summary_parts.append(f"Focus needed: {worst_subject.subject} ({worst_subject.overall_mastery:.1%})")
        
        # Insights summary
        strengths = [i for i in insights if i.insight_type == InsightType.STRENGTH]
        concerns = [i for i in insights if i.insight_type in [InsightType.WEAKNESS, InsightType.ALERT]]
        
        if strengths:
            summary_parts.append(f"Key strengths identified: {len(strengths)}")
        if concerns:
            summary_parts.append(f"Areas needing attention: {len(concerns)}")
        
        return " | ".join(summary_parts) if summary_parts else "Comprehensive analytics generated successfully."

    def _generate_priority_recommendations(
        self,
        insights: List[LearningInsight],
        subject_analytics: List[SubjectAnalytics],
        predictive_models: List[PredictiveModel]
    ) -> List[str]:
        """Generate priority recommendations based on analytics"""
        
        recommendations = []
        
        # High-priority recommendations from insights
        high_priority_insights = [i for i in insights if i.severity >= 4]
        for insight in high_priority_insights[:3]:  # Top 3
            if insight.actionable_items:
                recommendations.extend(insight.actionable_items[:2])  # Top 2 per insight
        
        # Subject-specific recommendations
        weak_subjects = [s for s in subject_analytics if s.overall_mastery < 0.6]
        for subject in weak_subjects[:2]:  # Top 2 weak subjects
            recommendations.append(f"Increase practice time in {subject.subject}")
            if subject.recommended_focus_areas:
                recommendations.append(f"Focus on {subject.recommended_focus_areas[0]} in {subject.subject}")
        
        # Predictive model recommendations
        performance_predictions = [p for p in predictive_models if p.prediction_type == "performance"]
        for prediction in performance_predictions:
            predicted_score = prediction.predicted_outcome.get("overall_score", 0.5)
            if predicted_score < 0.6:
                recommendations.append("Implement additional learning support to prevent performance decline")
        
        # Remove duplicates and limit to top 5
        unique_recommendations = list(dict.fromkeys(recommendations))
        return unique_recommendations[:5]

    def _calculate_success_probability(
        self,
        metrics: List[AnalyticsMetric],
        insights: List[LearningInsight],
        predictive_models: List[PredictiveModel]
    ) -> float:
        """Calculate overall success probability"""
        
        base_probability = 0.7
        
        # Adjust based on performance metrics
        performance_metrics = [m for m in metrics if m.metric_type == MetricType.PERFORMANCE]
        if performance_metrics:
            avg_performance = statistics.mean(m.value for m in performance_metrics)
            base_probability += (avg_performance - 0.5) * 0.3
        
        # Adjust based on engagement metrics
        engagement_metrics = [m for m in metrics if m.metric_type == MetricType.ENGAGEMENT]
        if engagement_metrics:
            avg_engagement = statistics.mean(m.value for m in engagement_metrics)
            base_probability += (avg_engagement - 0.5) * 0.2
        
        # Adjust based on insights
        strengths = len([i for i in insights if i.insight_type == InsightType.STRENGTH])
        concerns = len([i for i in insights if i.insight_type in [InsightType.WEAKNESS, InsightType.ALERT]])
        
        if strengths > concerns:
            base_probability += 0.1
        elif concerns > strengths:
            base_probability -= 0.1
        
        # Adjust based on predictive models
        for model in predictive_models:
            if model.prediction_type == "performance":
                predicted_score = model.predicted_outcome.get("overall_score", 0.5)
                if predicted_score > 0.7:
                    base_probability += 0.05
                elif predicted_score < 0.5:
                    base_probability -= 0.05
        
        return max(0.1, min(base_probability, 0.95))

    async def _generate_insights(
        self, 
        student_id: str, 
        assessment_results: List[AssessmentResult],
        learning_profile: LearningProfile,
        engagement_profile: Optional[StudentEngagementProfile] = None
    ) -> List[LearningInsight]:
        """Generate learning insights from assessment data"""
        insights = []
        
        if not assessment_results:
            return insights
            
        # Performance trend insight
        performance_scores = [r.performance_metrics.overall_score for r in assessment_results]
        trend = self._calculate_trend(performance_scores)
        
        if trend == "improving":
            insights.append(LearningInsight(
                insight_id=f"perf_trend_{student_id}",
                insight_type=InsightType.TREND,
                title="Performance Improving",
                description="Student shows consistent improvement in academic performance",
                confidence=0.85,
                severity=2,
                supporting_data={"scores": performance_scores, "trend": trend},
                actionable_items=["Continue current learning approach", "Consider advancing to next level"]
            ))
        elif trend == "declining":
            insights.append(LearningInsight(
                insight_id=f"perf_decline_{student_id}",
                insight_type=InsightType.WEAKNESS,
                title="Performance Declining",
                description="Student performance shows declining trend - intervention needed",
                confidence=0.80,
                severity=4,
                supporting_data={"scores": performance_scores, "trend": trend},
                actionable_items=["Review learning materials", "Increase practice sessions", "Consider tutoring"]
            ))
        
        # Learning style insight
        if learning_profile.learning_style:
            insights.append(LearningInsight(
                insight_id=f"learning_style_{student_id}",
                insight_type=InsightType.STRENGTH,
                title=f"{learning_profile.learning_style.title()} Learning Style Detected",
                description=f"Student learns best through {learning_profile.learning_style} methods",
                confidence=learning_profile.learning_style_confidence,
                severity=2,
                supporting_data={"learning_style": learning_profile.learning_style},
                actionable_items=[f"Provide more {learning_profile.learning_style} learning materials"]
            ))
        
        return insights

    async def _perform_subject_analytics(
        self, 
        student_id: str,
        assessment_results: List[AssessmentResult]
    ) -> Dict[str, SubjectAnalytics]:
        """Perform detailed analytics for each subject"""
        subject_analytics = {}
        
        # Group assessments by subject
        subjects_data = {}
        for result in assessment_results:
            subject = result.subject
            if subject not in subjects_data:
                subjects_data[subject] = []
            subjects_data[subject].append(result)
        
        # Generate analytics for each subject
        for subject, results in subjects_data.items():
            scores = [r.performance_metrics.overall_score for r in results]
            
            subject_analytics[subject] = SubjectAnalytics(
                subject=subject,
                total_assessments=len(results),
                average_score=statistics.mean(scores),
                score_trend=self._calculate_trend(scores),
                performance_trend=self._calculate_trend(scores),
                consistency_score=max(0.0, 1.0 - (statistics.stdev(scores) / statistics.mean(scores)) if len(scores) > 1 else 1.0),
                time_spent_minutes=sum(r.time_taken_seconds for r in results) // 60,
                strengths=[f"Strong performance in {subject}"] if statistics.mean(scores) > 0.8 else [],
                weaknesses=[f"Needs improvement in {subject}"] if statistics.mean(scores) < 0.6 else [],
                recommendations=[
                    f"Continue practicing {subject} concepts",
                    f"Review challenging topics in {subject}"
                ]
            )
        
        return subject_analytics

    async def _build_predictive_models(
        self,
        student_id: str,
        assessment_results: List[AssessmentResult],
        learning_profile: LearningProfile,
        engagement_profile: Optional[StudentEngagementProfile] = None
    ) -> List[PredictiveModel]:
        """Build predictive models for student performance"""
        models = []
        
        if not assessment_results:
            return models
        
        # Performance prediction model
        performance_scores = [r.performance_metrics.overall_score for r in assessment_results]
        current_avg = statistics.mean(performance_scores)
        trend = self._calculate_trend(performance_scores)
        
        # Simple prediction based on trend
        if trend == "improving":
            predicted_performance = min(1.0, current_avg + 0.1)
        elif trend == "declining":
            predicted_performance = max(0.0, current_avg - 0.1)
        else:
            predicted_performance = current_avg
        
        models.append(PredictiveModel(
            model_type="performance_prediction",
            model_name="Performance Trend Predictor",
            prediction=predicted_performance,
            confidence=0.75,
            time_horizon_days=30,
            key_factors=["recent_performance_trend", "consistency_score", "learning_pace"],
            supporting_data={
                "current_avg": current_avg,
                "trend": trend,
                "data_points": len(performance_scores)
            }
        ))
        
        # Engagement prediction model (if engagement profile available)
        if engagement_profile:
            engagement_prediction = min(1.0, engagement_profile.engagement_score + 0.05)
            
            models.append(PredictiveModel(
                model_type="engagement_prediction",
                model_name="Engagement Level Predictor",
                prediction=engagement_prediction,
                confidence=0.70,
                time_horizon_days=14,
                key_factors=["interaction_frequency", "session_duration", "challenge_acceptance"],
                supporting_data={
                    "current_engagement": engagement_profile.engagement_score,
                    "interaction_freq": engagement_profile.interaction_frequency
                }
            ))
        
        return models

    async def _analyze_trend(
        self,
        data_points: List[float],
        timeframe: AnalyticsTimeFrame = AnalyticsTimeFrame.MONTHLY
    ) -> Dict[str, Any]:
        """Analyze trends in data over time"""
        if len(data_points) < 2:
            return {
                "trend_direction": "stable",
                "trend_strength": 0.0,
                "slope": 0.0,
                "r_squared": 0.0,
                "data_points": len(data_points)
            }
        
        # Simple linear regression analysis
        n = len(data_points)
        x_values = list(range(n))
        y_values = data_points
        
        # Calculate slope
        x_mean = statistics.mean(x_values)
        y_mean = statistics.mean(y_values)
        
        numerator = sum((x_values[i] - x_mean) * (y_values[i] - y_mean) for i in range(n))
        denominator = sum((x_values[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            slope = 0
        else:
            slope = numerator / denominator
        
        # Determine trend direction and strength
        if abs(slope) < 0.01:
            trend_direction = "stable"
            trend_strength = 0.0
        elif slope > 0:
            trend_direction = "improving"
            trend_strength = min(1.0, abs(slope) * 10)
        else:
            trend_direction = "declining"
            trend_strength = min(1.0, abs(slope) * 10)
        
        # Calculate R-squared (simplified)
        y_pred = [slope * x + (y_mean - slope * x_mean) for x in x_values]
        ss_res = sum((y_values[i] - y_pred[i]) ** 2 for i in range(n))
        ss_tot = sum((y_values[i] - y_mean) ** 2 for i in range(n))
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        return {
            "trend_direction": trend_direction,
            "trend_strength": trend_strength,
            "slope": slope,
            "r_squared": max(0.0, r_squared),
            "data_points": n,
            "timeframe": timeframe.value
        }

    async def get_agent_status(self) -> Dict[str, Any]:
        """Get agent status and health"""
        return {
            "name": "AnalyticsAgent",
            "status": "active",
            "models_available": {
                "openai": self.openai_model is not None,
                "anthropic": self.anthropic_model is not None
            },
            "supported_timeframes": [t.value for t in AnalyticsTimeFrame],
            "supported_metric_types": [mt.value for mt in MetricType],
            "supported_insight_types": [it.value for it in InsightType],
            "benchmark_grades_available": list(self.benchmarks.keys()),
            "metric_weights_configured": len(self.metric_weights) > 0,
            "curriculum_loaded": self.curriculum is not None
        }