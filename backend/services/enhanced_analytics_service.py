"""
Enhanced Analytics Service - RSP Education Agent V2 Phase 1.2
Advanced Statistics Dashboard with real-time analytics, learning patterns, and predictions
"""

import asyncio
import json
import logging
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import random

from sqlalchemy.orm import Session
from database.models import Student
from core.exceptions import AgentException
from services.ai_companion_service import ai_companion_agent

logger = logging.getLogger(__name__)

class LearningStyle(Enum):
    VISUAL = "visual"
    AUDITORY = "auditory"
    KINESTHETIC = "kinesthetic"
    READING_WRITING = "reading_writing"

class DifficultyPreference(Enum):
    EASY = "easy"
    MODERATE = "moderate"
    CHALLENGING = "challenging"
    ADAPTIVE = "adaptive"

@dataclass
class DashboardData:
    """Real-time dashboard data with comprehensive learning metrics"""
    learning_velocity: float  # Questions per minute average
    engagement_score: float  # Overall engagement level (0-1)
    subject_breakdown: Dict[str, float]  # Time percentage by subject
    time_distribution: Dict[str, int]  # Minutes spent by hour of day
    achievement_progress: Dict[str, float]  # Progress toward goals
    recommended_actions: List[str]  # AI-recommended next steps
    total_study_time: int  # Total minutes studied
    streak_days: int  # Current learning streak
    completion_rate: float  # Assignment completion percentage
    focus_score: float  # Attention/focus quality metric

@dataclass
class LearningPatterns:
    """Student learning pattern analysis"""
    peak_learning_hours: List[int]  # Hours when student performs best
    preferred_subjects: List[str]  # Subjects with highest engagement
    learning_style_indicators: Dict[str, float]  # Learning style scores
    attention_span_average: int  # Average attention span in minutes
    difficulty_preference: str  # Preferred difficulty level
    session_frequency: str  # Daily, every other day, weekly, etc.
    optimal_session_length: int  # Optimal study session length
    break_patterns: Dict[str, int]  # When and how long breaks are taken
    performance_trends: Dict[str, List[float]]  # Performance over time by subject

@dataclass
class PerformancePrediction:
    """AI-powered performance predictions"""
    next_session_score: float  # Predicted performance for next session
    confidence_level: float  # Confidence in prediction (0-1)
    recommended_difficulty: str  # Suggested difficulty level
    optimal_study_time: str  # Best time for next session
    subjects_to_focus: List[str]  # Subjects needing attention
    predicted_completion_time: int  # Minutes to complete next task
    success_probability: float  # Probability of successful completion
    intervention_needed: bool  # Whether intervention is recommended

@dataclass
class LearningInsight:
    """Individual learning insight with actionable recommendations"""
    insight_type: str  # "strength", "improvement", "pattern", "prediction"
    title: str
    description: str
    confidence: float  # Confidence in insight (0-1)
    actionable_steps: List[str]
    priority: str  # "high", "medium", "low"
    category: str  # "performance", "engagement", "efficiency", "wellbeing"

@dataclass
class LearningMetrics:
    """Comprehensive learning metrics for analysis"""
    sessions_completed: int
    total_questions_answered: int
    average_accuracy: float
    time_on_task: int  # minutes
    engagement_events: int  # clicks, interactions, etc.
    help_requests: int
    mistakes_corrected: int
    achievements_unlocked: int
    peer_interactions: int
    self_assessments_completed: int

class EnhancedAnalyticsService:
    """Enhanced Analytics Service with real-time dashboard and predictive capabilities"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.EnhancedAnalyticsService")
        
        # In-memory storage for learning analytics (in production, use proper database)
        self.student_analytics: Dict[str, Dict] = {}
        self.learning_sessions: Dict[str, List[Dict]] = {}
        self.performance_history: Dict[str, List[Dict]] = {}
        
    async def generate_real_time_dashboard(self, student_id: str, db: Session) -> DashboardData:
        """Generate comprehensive real-time dashboard data"""
        try:
            # Get or initialize student analytics
            analytics = self._get_student_analytics(student_id)
            
            # Calculate learning velocity (questions per minute)
            learning_velocity = self._calculate_learning_velocity(student_id)
            
            # Calculate engagement score
            engagement_score = await self._calculate_engagement_score(student_id)
            
            # Get subject breakdown
            subject_breakdown = self._calculate_subject_breakdown(student_id)
            
            # Get time distribution by hour
            time_distribution = self._calculate_time_distribution(student_id)
            
            # Calculate achievement progress
            achievement_progress = self._calculate_achievement_progress(student_id)
            
            # Generate AI-powered recommendations
            recommended_actions = await self._generate_recommendations(student_id)
            
            # Calculate additional metrics
            total_study_time = analytics.get('total_study_time', 0)
            streak_days = self._calculate_streak_days(student_id)
            completion_rate = self._calculate_completion_rate(student_id)
            focus_score = self._calculate_focus_score(student_id)
            
            dashboard = DashboardData(
                learning_velocity=learning_velocity,
                engagement_score=engagement_score,
                subject_breakdown=subject_breakdown,
                time_distribution=time_distribution,
                achievement_progress=achievement_progress,
                recommended_actions=recommended_actions,
                total_study_time=total_study_time,
                streak_days=streak_days,
                completion_rate=completion_rate,
                focus_score=focus_score
            )
            
            self.logger.info(f"Generated real-time dashboard for student: {student_id}")
            return dashboard
            
        except Exception as e:
            self.logger.error(f"Failed to generate dashboard for {student_id}: {e}")
            raise AgentException(f"Dashboard generation failed: {e}")

    async def track_learning_patterns(self, student_id: str) -> LearningPatterns:
        """Analyze and track student learning patterns"""
        try:
            sessions = self.learning_sessions.get(student_id, [])
            
            # Analyze peak learning hours
            peak_hours = self._analyze_peak_learning_hours(sessions)
            
            # Identify preferred subjects
            preferred_subjects = self._identify_preferred_subjects(student_id)
            
            # Calculate learning style indicators
            learning_style_indicators = self._calculate_learning_style_indicators(student_id)
            
            # Calculate average attention span
            attention_span = self._calculate_attention_span(sessions)
            
            # Determine difficulty preference
            difficulty_preference = self._determine_difficulty_preference(student_id)
            
            # Analyze session frequency
            session_frequency = self._analyze_session_frequency(sessions)
            
            # Calculate optimal session length
            optimal_length = self._calculate_optimal_session_length(sessions)
            
            # Analyze break patterns
            break_patterns = self._analyze_break_patterns(sessions)
            
            # Calculate performance trends
            performance_trends = self._calculate_performance_trends(student_id)
            
            patterns = LearningPatterns(
                peak_learning_hours=peak_hours,
                preferred_subjects=preferred_subjects,
                learning_style_indicators=learning_style_indicators,
                attention_span_average=attention_span,
                difficulty_preference=difficulty_preference,
                session_frequency=session_frequency,
                optimal_session_length=optimal_length,
                break_patterns=break_patterns,
                performance_trends=performance_trends
            )
            
            self.logger.info(f"Analyzed learning patterns for student: {student_id}")
            return patterns
            
        except Exception as e:
            self.logger.error(f"Failed to analyze learning patterns for {student_id}: {e}")
            raise AgentException(f"Pattern analysis failed: {e}")

    async def predict_performance(self, student_id: str) -> PerformancePrediction:
        """Generate AI-powered performance predictions"""
        try:
            # Get historical performance data
            history = self.performance_history.get(student_id, [])
            patterns = await self.track_learning_patterns(student_id)
            
            # Predict next session score based on trends
            next_session_score = self._predict_next_session_score(history, patterns)
            
            # Calculate confidence level
            confidence_level = self._calculate_prediction_confidence(history)
            
            # Recommend difficulty level
            recommended_difficulty = self._recommend_difficulty_level(student_id, patterns)
            
            # Suggest optimal study time
            optimal_study_time = self._suggest_optimal_study_time(patterns)
            
            # Identify subjects to focus on
            subjects_to_focus = self._identify_focus_subjects(student_id, patterns)
            
            # Predict completion time
            predicted_completion_time = self._predict_completion_time(student_id, patterns)
            
            # Calculate success probability
            success_probability = self._calculate_success_probability(student_id, history)
            
            # Determine if intervention is needed
            intervention_needed = self._assess_intervention_need(student_id, history, patterns)
            
            prediction = PerformancePrediction(
                next_session_score=next_session_score,
                confidence_level=confidence_level,
                recommended_difficulty=recommended_difficulty,
                optimal_study_time=optimal_study_time,
                subjects_to_focus=subjects_to_focus,
                predicted_completion_time=predicted_completion_time,
                success_probability=success_probability,
                intervention_needed=intervention_needed
            )
            
            self.logger.info(f"Generated performance prediction for student: {student_id}")
            return prediction
            
        except Exception as e:
            self.logger.error(f"Failed to predict performance for {student_id}: {e}")
            raise AgentException(f"Performance prediction failed: {e}")

    async def generate_insights(self, student_id: str) -> List[LearningInsight]:
        """Generate actionable learning insights using AI analysis"""
        try:
            insights = []
            
            # Get analytics data
            dashboard = await self.generate_real_time_dashboard(student_id, None)
            patterns = await self.track_learning_patterns(student_id)
            predictions = await self.predict_performance(student_id)
            
            # Generate strength insights
            if dashboard.engagement_score > 0.8:
                insights.append(LearningInsight(
                    insight_type="strength",
                    title="Excellent Engagement Level",
                    description=f"Your engagement score of {dashboard.engagement_score:.1%} shows you're highly motivated and focused during learning sessions.",
                    confidence=0.9,
                    actionable_steps=[
                        "Maintain current study routine",
                        "Consider taking on more challenging topics",
                        "Share your learning strategies with peers"
                    ],
                    priority="medium",
                    category="engagement"
                ))
            
            # Generate improvement insights
            if dashboard.completion_rate < 0.6:
                insights.append(LearningInsight(
                    insight_type="improvement",
                    title="Focus on Task Completion",
                    description=f"Your completion rate of {dashboard.completion_rate:.1%} suggests opportunities to improve task finishing.",
                    confidence=0.8,
                    actionable_steps=[
                        "Break large tasks into smaller chunks",
                        "Set specific completion goals for each session",
                        "Use the Pomodoro technique for better focus"
                    ],
                    priority="high",
                    category="performance"
                ))
            
            # Generate pattern insights
            if patterns.peak_learning_hours:
                peak_hour = patterns.peak_learning_hours[0]
                insights.append(LearningInsight(
                    insight_type="pattern",
                    title="Optimal Learning Time Identified",
                    description=f"You perform best around {peak_hour}:00. Your focus and retention are highest during this time.",
                    confidence=0.85,
                    actionable_steps=[
                        f"Schedule important study sessions around {peak_hour}:00",
                        "Tackle challenging subjects during your peak hours",
                        "Use off-peak times for review and practice"
                    ],
                    priority="medium",
                    category="efficiency"
                ))
            
            # Generate prediction insights
            if predictions.intervention_needed:
                insights.append(LearningInsight(
                    insight_type="prediction",
                    title="Early Support Recommended",
                    description="Our AI analysis suggests you might benefit from additional support in some areas.",
                    confidence=predictions.confidence_level,
                    actionable_steps=[
                        "Schedule a session with your tutor",
                        "Focus on fundamental concepts before advancing",
                        "Use additional practice resources"
                    ],
                    priority="high",
                    category="wellbeing"
                ))
            
            # Generate subject-specific insights
            if patterns.preferred_subjects:
                top_subject = patterns.preferred_subjects[0]
                insights.append(LearningInsight(
                    insight_type="strength",
                    title=f"Strong Affinity for {top_subject}",
                    description=f"You show exceptional engagement and performance in {top_subject}.",
                    confidence=0.9,
                    actionable_steps=[
                        f"Consider advanced topics in {top_subject}",
                        f"Help peers who struggle with {top_subject}",
                        f"Explore career paths related to {top_subject}"
                    ],
                    priority="low",
                    category="engagement"
                ))
            
            self.logger.info(f"Generated {len(insights)} insights for student: {student_id}")
            return insights
            
        except Exception as e:
            self.logger.error(f"Failed to generate insights for {student_id}: {e}")
            return []

    def track_session_data(self, student_id: str, session_data: Dict) -> None:
        """Track learning session data for analytics"""
        try:
            if student_id not in self.learning_sessions:
                self.learning_sessions[student_id] = []
            
            # Add timestamp if not present
            if 'timestamp' not in session_data:
                session_data['timestamp'] = datetime.now().isoformat()
            
            self.learning_sessions[student_id].append(session_data)
            
            # Keep only last 100 sessions
            if len(self.learning_sessions[student_id]) > 100:
                self.learning_sessions[student_id] = self.learning_sessions[student_id][-100:]
            
            # Update aggregated analytics
            self._update_student_analytics(student_id, session_data)
            
            self.logger.info(f"Tracked session data for student: {student_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to track session data for {student_id}: {e}")

    def _get_student_analytics(self, student_id: str) -> Dict:
        """Get or initialize student analytics data"""
        if student_id not in self.student_analytics:
            self.student_analytics[student_id] = {
                'total_study_time': 0,
                'total_questions': 0,
                'total_correct': 0,
                'sessions_count': 0,
                'subjects': {},
                'last_session': None,
                'streak_start': datetime.now().isoformat()
            }
        return self.student_analytics[student_id]

    def _calculate_learning_velocity(self, student_id: str) -> float:
        """Calculate questions answered per minute"""
        sessions = self.learning_sessions.get(student_id, [])
        if not sessions:
            return 0.0
        
        total_questions = sum(session.get('questions_answered', 0) for session in sessions[-10:])  # Last 10 sessions
        total_time = sum(session.get('duration_minutes', 0) for session in sessions[-10:])
        
        return total_questions / max(total_time, 1)

    async def _calculate_engagement_score(self, student_id: str) -> float:
        """Calculate overall engagement score"""
        sessions = self.learning_sessions.get(student_id, [])
        if not sessions:
            return 0.5
        
        recent_sessions = sessions[-5:]  # Last 5 sessions
        
        # Factors: completion rate, time spent, interaction frequency
        completion_scores = [session.get('completion_rate', 0.5) for session in recent_sessions]
        time_scores = [min(session.get('duration_minutes', 0) / 30.0, 1.0) for session in recent_sessions]  # Normalize to 30 min
        interaction_scores = [min(session.get('interactions', 0) / 50.0, 1.0) for session in recent_sessions]  # Normalize to 50 interactions
        
        # Weighted average
        engagement = (
            statistics.mean(completion_scores) * 0.4 +
            statistics.mean(time_scores) * 0.3 +
            statistics.mean(interaction_scores) * 0.3
        )
        
        return min(engagement, 1.0)

    def _calculate_subject_breakdown(self, student_id: str) -> Dict[str, float]:
        """Calculate time percentage spent on each subject"""
        sessions = self.learning_sessions.get(student_id, [])
        if not sessions:
            return {}
        
        subject_time = {}
        total_time = 0
        
        for session in sessions[-20:]:  # Last 20 sessions
            subject = session.get('subject', 'Unknown')
            duration = session.get('duration_minutes', 0)
            subject_time[subject] = subject_time.get(subject, 0) + duration
            total_time += duration
        
        # Convert to percentages
        if total_time > 0:
            return {subject: (time / total_time) for subject, time in subject_time.items()}
        return {}

    def _calculate_time_distribution(self, student_id: str) -> Dict[str, int]:
        """Calculate minutes spent by hour of day"""
        sessions = self.learning_sessions.get(student_id, [])
        hour_distribution = {}
        
        for session in sessions:
            timestamp = session.get('timestamp')
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    hour = str(dt.hour)
                    duration = session.get('duration_minutes', 0)
                    hour_distribution[hour] = hour_distribution.get(hour, 0) + duration
                except:
                    continue
        
        return hour_distribution

    def _calculate_achievement_progress(self, student_id: str) -> Dict[str, float]:
        """Calculate progress toward various achievements"""
        analytics = self._get_student_analytics(student_id)
        
        return {
            "Questions Master": min(analytics.get('total_questions', 0) / 1000.0, 1.0),
            "Study Streak": min(self._calculate_streak_days(student_id) / 30.0, 1.0),
            "Subject Explorer": min(len(analytics.get('subjects', {})) / 10.0, 1.0),
            "Accuracy Expert": analytics.get('total_correct', 0) / max(analytics.get('total_questions', 1), 1),
            "Time Warrior": min(analytics.get('total_study_time', 0) / 6000.0, 1.0)  # 100 hours
        }

    async def _generate_recommendations(self, student_id: str) -> List[str]:
        """Generate AI-powered recommendations"""
        try:
            # Get companion context for personalized recommendations
            companion_context = ai_companion_agent.get_companion_context_for_agent(student_id, "analytics")
            
            recommendations = []
            analytics = self._get_student_analytics(student_id)
            
            # Analyze performance and suggest actions
            if analytics.get('total_questions', 0) < 10:
                recommendations.append("🎯 Complete more practice questions to improve your skills")
            
            if self._calculate_streak_days(student_id) == 0:
                recommendations.append("🔥 Start a learning streak by studying consistently each day")
            
            # Companion-enhanced recommendations
            if companion_context.get('companion_available'):
                mood = companion_context.get('current_mood', 'happy')
                if mood == 'concerned':
                    recommendations.append("💪 Your AI companion notices you might need extra support - don't hesitate to ask for help!")
                elif mood == 'excited':
                    recommendations.append("🚀 Your AI companion is excited about your progress - keep up the amazing work!")
            
            if not recommendations:
                recommendations.append("📚 Keep up the great learning momentum!")
            
            return recommendations[:5]  # Limit to 5 recommendations
            
        except Exception as e:
            return ["📚 Continue your learning journey - you're doing great!"]

    def _calculate_streak_days(self, student_id: str) -> int:
        """Calculate current learning streak in days"""
        sessions = self.learning_sessions.get(student_id, [])
        if not sessions:
            return 0
        
        # Simple streak calculation based on consecutive days with sessions
        dates = set()
        for session in sessions:
            timestamp = session.get('timestamp')
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    dates.add(dt.date())
                except:
                    continue
        
        if not dates:
            return 0
        
        # Check consecutive days from today backwards
        today = datetime.now().date()
        streak = 0
        current_date = today
        
        while current_date in dates:
            streak += 1
            current_date -= timedelta(days=1)
        
        return streak

    def _calculate_completion_rate(self, student_id: str) -> float:
        """Calculate task completion rate"""
        sessions = self.learning_sessions.get(student_id, [])
        if not sessions:
            return 0.0
        
        completed_sessions = sum(1 for session in sessions[-10:] if session.get('completed', False))
        return completed_sessions / min(len(sessions), 10)

    def _calculate_focus_score(self, student_id: str) -> float:
        """Calculate focus/attention quality score"""
        sessions = self.learning_sessions.get(student_id, [])
        if not sessions:
            return 0.5
        
        recent_sessions = sessions[-5:]
        focus_scores = []
        
        for session in recent_sessions:
            # Factors: time on task vs total time, minimal breaks, consistent pace
            duration = session.get('duration_minutes', 0)
            active_time = session.get('active_minutes', duration)  # Time actually engaged
            breaks = session.get('break_count', 0)
            
            if duration > 0:
                focus_score = (active_time / duration) * max(0.5, 1 - (breaks * 0.1))
                focus_scores.append(min(focus_score, 1.0))
        
        return statistics.mean(focus_scores) if focus_scores else 0.5

    def _analyze_peak_learning_hours(self, sessions: List[Dict]) -> List[int]:
        """Analyze when student performs best"""
        hour_performance = {}
        
        for session in sessions:
            timestamp = session.get('timestamp')
            performance = session.get('performance_score', 0.5)
            
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    hour = dt.hour
                    
                    if hour not in hour_performance:
                        hour_performance[hour] = []
                    hour_performance[hour].append(performance)
                except:
                    continue
        
        # Calculate average performance by hour
        hour_averages = {
            hour: statistics.mean(scores) 
            for hour, scores in hour_performance.items() 
            if len(scores) >= 2  # Need at least 2 sessions
        }
        
        # Return top 3 hours sorted by performance
        sorted_hours = sorted(hour_averages.items(), key=lambda x: x[1], reverse=True)
        return [hour for hour, _ in sorted_hours[:3]]

    def _identify_preferred_subjects(self, student_id: str) -> List[str]:
        """Identify subjects student prefers based on engagement"""
        sessions = self.learning_sessions.get(student_id, [])
        subject_engagement = {}
        
        for session in sessions:
            subject = session.get('subject')
            engagement = session.get('engagement_score', 0.5)
            duration = session.get('duration_minutes', 0)
            
            if subject and duration > 5:  # Valid session
                if subject not in subject_engagement:
                    subject_engagement[subject] = []
                subject_engagement[subject].append(engagement)
        
        # Calculate average engagement by subject
        subject_averages = {
            subject: statistics.mean(scores)
            for subject, scores in subject_engagement.items()
            if len(scores) >= 2
        }
        
        # Return subjects sorted by engagement
        sorted_subjects = sorted(subject_averages.items(), key=lambda x: x[1], reverse=True)
        return [subject for subject, _ in sorted_subjects[:5]]

    def _calculate_learning_style_indicators(self, student_id: str) -> Dict[str, float]:
        """Calculate learning style indicators based on behavior"""
        sessions = self.learning_sessions.get(student_id, [])
        
        # Initialize style scores
        style_scores = {
            "visual": 0.0,
            "auditory": 0.0,
            "kinesthetic": 0.0,
            "reading_writing": 0.0
        }
        
        for session in sessions:
            # Analyze session activities to infer learning style preferences
            activities = session.get('activities', [])
            
            for activity in activities:
                activity_type = activity.get('type', '')
                engagement = activity.get('engagement', 0.5)
                
                # Map activities to learning styles
                if 'visual' in activity_type or 'diagram' in activity_type or 'image' in activity_type:
                    style_scores['visual'] += engagement
                elif 'audio' in activity_type or 'voice' in activity_type or 'speech' in activity_type:
                    style_scores['auditory'] += engagement
                elif 'interactive' in activity_type or 'drag' in activity_type or 'game' in activity_type:
                    style_scores['kinesthetic'] += engagement
                elif 'text' in activity_type or 'reading' in activity_type or 'writing' in activity_type:
                    style_scores['reading_writing'] += engagement
        
        # Normalize scores
        total_score = sum(style_scores.values()) or 1
        return {style: score / total_score for style, score in style_scores.items()}

    def _calculate_attention_span(self, sessions: List[Dict]) -> int:
        """Calculate average attention span in minutes"""
        focused_durations = []
        
        for session in sessions:
            duration = session.get('duration_minutes', 0)
            breaks = session.get('break_count', 0)
            
            if duration > 0 and breaks >= 0:
                # Estimate focused time between breaks
                if breaks == 0:
                    focused_durations.append(duration)
                else:
                    avg_focused_time = duration / (breaks + 1)
                    focused_durations.append(avg_focused_time)
        
        return int(statistics.mean(focused_durations)) if focused_durations else 25

    def _determine_difficulty_preference(self, student_id: str) -> str:
        """Determine preferred difficulty level"""
        sessions = self.learning_sessions.get(student_id, [])
        difficulty_performance = {}
        
        for session in sessions:
            difficulty = session.get('difficulty_level')
            performance = session.get('performance_score', 0.5)
            engagement = session.get('engagement_score', 0.5)
            
            if difficulty:
                if difficulty not in difficulty_performance:
                    difficulty_performance[difficulty] = []
                # Combined metric of performance and engagement
                combined_score = (performance + engagement) / 2
                difficulty_performance[difficulty].append(combined_score)
        
        # Find difficulty with best combined performance and engagement
        best_difficulty = "moderate"  # default
        best_score = 0
        
        for difficulty, scores in difficulty_performance.items():
            if len(scores) >= 2:  # Need sufficient data
                avg_score = statistics.mean(scores)
                if avg_score > best_score:
                    best_score = avg_score
                    best_difficulty = difficulty
        
        return best_difficulty

    def _analyze_session_frequency(self, sessions: List[Dict]) -> str:
        """Analyze how frequently student studies"""
        if not sessions:
            return "irregular"
        
        # Get dates of sessions
        dates = []
        for session in sessions:
            timestamp = session.get('timestamp')
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    dates.append(dt.date())
                except:
                    continue
        
        if len(dates) < 3:
            return "irregular"
        
        # Calculate average days between sessions
        dates.sort()
        intervals = [(dates[i] - dates[i-1]).days for i in range(1, len(dates))]
        avg_interval = statistics.mean(intervals)
        
        if avg_interval <= 1.2:
            return "daily"
        elif avg_interval <= 2.5:
            return "every_other_day"
        elif avg_interval <= 4:
            return "few_times_week"
        elif avg_interval <= 8:
            return "weekly"
        else:
            return "irregular"

    def _calculate_optimal_session_length(self, sessions: List[Dict]) -> int:
        """Calculate optimal session length based on performance"""
        length_performance = {}
        
        for session in sessions:
            duration = session.get('duration_minutes', 0)
            performance = session.get('performance_score', 0.5)
            engagement = session.get('engagement_score', 0.5)
            
            if duration >= 5:  # Valid session length
                # Group into ranges
                if duration <= 15:
                    range_key = "short"
                elif duration <= 30:
                    range_key = "medium"
                elif duration <= 60:
                    range_key = "long"
                else:
                    range_key = "very_long"
                
                if range_key not in length_performance:
                    length_performance[range_key] = []
                
                combined_score = (performance + engagement) / 2
                length_performance[range_key].append(combined_score)
        
        # Find best performing length range
        best_range = "medium"
        best_score = 0
        
        for range_key, scores in length_performance.items():
            if len(scores) >= 2:
                avg_score = statistics.mean(scores)
                if avg_score > best_score:
                    best_score = avg_score
                    best_range = range_key
        
        # Map to actual minutes
        range_mapping = {
            "short": 15,
            "medium": 25,
            "long": 45,
            "very_long": 60
        }
        
        return range_mapping.get(best_range, 25)

    def _analyze_break_patterns(self, sessions: List[Dict]) -> Dict[str, int]:
        """Analyze when and how long breaks are taken"""
        break_data = {
            "average_break_frequency": 0,  # breaks per hour
            "average_break_duration": 0,   # minutes
            "preferred_break_timing": 20   # minutes into session
        }
        
        total_breaks = 0
        total_duration = 0
        break_timings = []
        
        for session in sessions:
            duration = session.get('duration_minutes', 0)
            breaks = session.get('break_count', 0)
            break_timing = session.get('first_break_at', 0)
            
            if duration > 0:
                total_breaks += breaks
                total_duration += duration
                
                if break_timing > 0:
                    break_timings.append(break_timing)
        
        if total_duration > 0:
            break_data["average_break_frequency"] = int((total_breaks / total_duration) * 60)  # per hour
        
        if break_timings:
            break_data["preferred_break_timing"] = int(statistics.mean(break_timings))
        
        return break_data

    def _calculate_performance_trends(self, student_id: str) -> Dict[str, List[float]]:
        """Calculate performance trends by subject over time"""
        sessions = self.learning_sessions.get(student_id, [])
        subject_trends = {}
        
        for session in sessions[-20:]:  # Last 20 sessions
            subject = session.get('subject')
            performance = session.get('performance_score', 0.5)
            
            if subject:
                if subject not in subject_trends:
                    subject_trends[subject] = []
                subject_trends[subject].append(performance)
        
        return subject_trends

    def _predict_next_session_score(self, history: List[Dict], patterns: LearningPatterns) -> float:
        """Predict performance for next session"""
        if not history:
            return 0.7  # Optimistic default
        
        recent_scores = [session.get('performance_score', 0.5) for session in history[-5:]]
        
        # Simple trend analysis
        if len(recent_scores) >= 3:
            # Calculate trend (improving, declining, stable)
            trend = (recent_scores[-1] - recent_scores[0]) / len(recent_scores)
            base_prediction = recent_scores[-1] + trend
        else:
            base_prediction = statistics.mean(recent_scores)
        
        # Adjust based on patterns
        if patterns.attention_span_average > 30:
            base_prediction += 0.05  # Good attention span
        
        if patterns.difficulty_preference == "challenging":
            base_prediction += 0.03  # Likes challenges
        
        return max(0.0, min(1.0, base_prediction))

    def _calculate_prediction_confidence(self, history: List[Dict]) -> float:
        """Calculate confidence in predictions based on data quality"""
        if len(history) < 3:
            return 0.3  # Low confidence with little data
        elif len(history) < 10:
            return 0.7  # Medium confidence
        else:
            # Higher confidence with more data and consistent patterns
            recent_scores = [session.get('performance_score', 0.5) for session in history[-10:]]
            variance = statistics.stdev(recent_scores) if len(recent_scores) > 1 else 0.5
            
            # Lower variance = higher confidence
            confidence = max(0.5, 1.0 - variance)
            return min(0.95, confidence)

    def _recommend_difficulty_level(self, student_id: str, patterns: LearningPatterns) -> str:
        """Recommend optimal difficulty level"""
        current_preference = patterns.difficulty_preference
        
        # Get recent performance
        sessions = self.learning_sessions.get(student_id, [])
        if sessions:
            recent_performance = statistics.mean([
                session.get('performance_score', 0.5) 
                for session in sessions[-3:]
            ])
            
            # Adjust difficulty based on performance
            if recent_performance > 0.85:
                # Performing very well, can handle more challenge
                if current_preference == "easy":
                    return "moderate"
                elif current_preference == "moderate":
                    return "challenging"
                else:
                    return current_preference
            elif recent_performance < 0.6:
                # Struggling, reduce difficulty
                if current_preference == "challenging":
                    return "moderate"
                elif current_preference == "moderate":
                    return "easy"
                else:
                    return current_preference
        
        return current_preference

    def _suggest_optimal_study_time(self, patterns: LearningPatterns) -> str:
        """Suggest optimal time for next study session"""
        if patterns.peak_learning_hours:
            peak_hour = patterns.peak_learning_hours[0]
            return f"{peak_hour:02d}:00"
        
        # Default suggestions based on common patterns
        return "14:00"  # 2 PM is often good for focus

    def _identify_focus_subjects(self, student_id: str, patterns: LearningPatterns) -> List[str]:
        """Identify subjects that need focus"""
        sessions = self.learning_sessions.get(student_id, [])
        subject_performance = {}
        
        for session in sessions[-10:]:  # Recent sessions
            subject = session.get('subject')
            performance = session.get('performance_score', 0.5)
            
            if subject:
                if subject not in subject_performance:
                    subject_performance[subject] = []
                subject_performance[subject].append(performance)
        
        # Find subjects with below-average performance
        struggling_subjects = []
        for subject, scores in subject_performance.items():
            if len(scores) >= 2:
                avg_score = statistics.mean(scores)
                if avg_score < 0.7:  # Below 70%
                    struggling_subjects.append(subject)
        
        return struggling_subjects[:3]  # Top 3 subjects needing focus

    def _predict_completion_time(self, student_id: str, patterns: LearningPatterns) -> int:
        """Predict time needed to complete next task"""
        sessions = self.learning_sessions.get(student_id, [])
        
        if sessions:
            recent_durations = [
                session.get('duration_minutes', 30) 
                for session in sessions[-5:]
                if session.get('completed', False)
            ]
            
            if recent_durations:
                avg_duration = statistics.mean(recent_durations)
                # Adjust based on attention span
                if patterns.attention_span_average < 20:
                    return int(avg_duration * 1.2)  # May take longer
                else:
                    return int(avg_duration)
        
        return 30  # Default 30 minutes

    def _calculate_success_probability(self, student_id: str, history: List[Dict]) -> float:
        """Calculate probability of successful completion"""
        if not history:
            return 0.7  # Optimistic default
        
        recent_completions = [
            session.get('completed', False) 
            for session in history[-10:]
        ]
        
        completion_rate = sum(recent_completions) / len(recent_completions)
        
        # Also consider performance scores
        recent_scores = [
            session.get('performance_score', 0.5) 
            for session in history[-10:]
        ]
        
        avg_performance = statistics.mean(recent_scores)
        
        # Combined probability
        probability = (completion_rate * 0.6) + (avg_performance * 0.4)
        return min(0.95, probability)

    def _assess_intervention_need(self, student_id: str, history: List[Dict], patterns: LearningPatterns) -> bool:
        """Assess whether student needs intervention/support"""
        if not history:
            return False
        
        # Check for concerning patterns
        recent_performance = [
            session.get('performance_score', 0.5) 
            for session in history[-5:]
        ]
        
        recent_engagement = [
            session.get('engagement_score', 0.5) 
            for session in history[-5:]
        ]
        
        # Red flags
        avg_performance = statistics.mean(recent_performance) if recent_performance else 0.5
        avg_engagement = statistics.mean(recent_engagement) if recent_engagement else 0.5
        
        # Multiple concerning indicators
        concerns = 0
        
        if avg_performance < 0.5:
            concerns += 1
        if avg_engagement < 0.4:
            concerns += 1
        if patterns.attention_span_average < 10:
            concerns += 1
        if len(patterns.preferred_subjects) == 0:
            concerns += 1
        
        return concerns >= 2

    def _update_student_analytics(self, student_id: str, session_data: Dict) -> None:
        """Update aggregated analytics for student"""
        analytics = self._get_student_analytics(student_id)
        
        # Update totals
        analytics['total_study_time'] += session_data.get('duration_minutes', 0)
        analytics['total_questions'] += session_data.get('questions_answered', 0)
        analytics['total_correct'] += session_data.get('correct_answers', 0)
        analytics['sessions_count'] += 1
        analytics['last_session'] = session_data.get('timestamp')
        
        # Update subject data
        subject = session_data.get('subject')
        if subject:
            if subject not in analytics['subjects']:
                analytics['subjects'][subject] = {
                    'time_spent': 0,
                    'questions': 0,
                    'correct': 0,
                    'sessions': 0
                }
            
            analytics['subjects'][subject]['time_spent'] += session_data.get('duration_minutes', 0)
            analytics['subjects'][subject]['questions'] += session_data.get('questions_answered', 0)
            analytics['subjects'][subject]['correct'] += session_data.get('correct_answers', 0)
            analytics['subjects'][subject]['sessions'] += 1

# Global Enhanced Analytics service instance
enhanced_analytics_service = EnhancedAnalyticsService()