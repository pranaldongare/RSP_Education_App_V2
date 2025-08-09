"""
Parent Dashboard Service - RSP Education Agent V2 Phase 2.1
Real-time progress monitoring, communication portal, and comprehensive reporting for parents
"""

import asyncio
import json
import logging
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

from sqlalchemy.orm import Session
from database.models import Student
from core.exceptions import AgentException
from services.ai_companion_service import ai_companion_agent
from services.enhanced_analytics_service import enhanced_analytics_service
from services.smart_notifications_service import smart_notifications_service

logger = logging.getLogger(__name__)

class AlertPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class CommunicationType(Enum):
    PROGRESS_UPDATE = "progress_update"
    ACHIEVEMENT = "achievement"
    CONCERN = "concern"
    REMINDER = "reminder"
    REPORT = "report"
    MESSAGE = "message"

@dataclass
class StudentProgress:
    """Student progress summary for parents"""
    student_id: str
    student_name: str
    grade: int
    current_streak: int
    total_study_hours: float
    weekly_progress: float  # Percentage progress this week
    subjects_studied: List[str]
    favorite_subject: str
    challenging_subject: str
    overall_performance: float  # 0-100 score
    engagement_level: str  # low, medium, high
    last_active: str  # ISO timestamp
    achievements_this_week: int
    completion_rate: float  # 0-1
    study_consistency: str  # inconsistent, regular, excellent

@dataclass
class LearningInsight:
    """Learning insights and recommendations for parents"""
    insight_id: str
    category: str  # performance, engagement, behavior, recommendation
    title: str
    description: str
    severity: str  # AlertPriority
    recommendation: str
    action_items: List[str]
    confidence: float  # 0-1
    detected_at: str  # ISO timestamp
    affects_subjects: List[str]
    estimated_impact: str  # low, medium, high

@dataclass
class ParentAlert:
    """Alert notifications for parents"""
    alert_id: str
    student_id: str
    alert_type: str  # CommunicationType
    priority: str  # AlertPriority
    title: str
    message: str
    details: Dict
    created_at: str
    expires_at: Optional[str]
    action_required: bool
    action_buttons: List[Dict]
    read: bool
    parent_response: Optional[str]

@dataclass
class PerformanceTrend:
    """Performance trend analysis"""
    subject: str
    current_score: float
    previous_score: float
    trend: str  # improving, declining, stable
    trend_percentage: float
    confidence: float
    time_period: str  # week, month
    sessions_analyzed: int
    recommendation: str

@dataclass
class WeeklyReport:
    """Comprehensive weekly report for parents"""
    report_id: str
    student_id: str
    week_start: str
    week_end: str
    total_study_time: float
    sessions_completed: int
    subjects_covered: List[str]
    achievements_earned: int
    overall_progress: float
    performance_trends: List[PerformanceTrend]
    key_insights: List[LearningInsight]
    recommendations: List[str]
    companion_summary: str  # AI companion's summary of the week
    parent_action_items: List[str]

class ParentDashboardService:
    """Parent Dashboard Service with real-time monitoring and communication"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.ParentDashboardService")
        
        # In-memory storage for real-time data (in production, use Redis or similar)
        self.active_sessions: Dict[str, Dict] = {}  # student_id -> session_data
        self.parent_alerts: Dict[str, List[ParentAlert]] = {}  # parent_email -> alerts
        self.communication_history: Dict[str, List[Dict]] = {}  # student_id -> messages
        self.performance_cache: Dict[str, Dict] = {}  # student_id -> cached performance data
        
        # Alert thresholds and configuration
        self.alert_thresholds = {
            "low_engagement": 0.3,  # Below 30% engagement
            "performance_drop": 0.15,  # 15% performance drop
            "study_streak_break": 2,  # 2 days without studying
            "completion_rate_low": 0.5,  # Below 50% completion rate
            "excessive_study_time": 4.0,  # More than 4 hours per day
        }

    async def get_student_progress(self, student_id: str) -> StudentProgress:
        """Get comprehensive student progress for parent dashboard"""
        try:
            # Get real-time dashboard data
            dashboard_data = await enhanced_analytics_service.generate_real_time_dashboard(student_id, None)
            
            # Get learning patterns
            patterns = await enhanced_analytics_service.track_learning_patterns(student_id)
            
            # Get companion context for personality insights
            companion_context = ai_companion_agent.get_companion_context_for_agent(student_id, "parent_dashboard")
            
            # Determine engagement level
            engagement_score = dashboard_data.engagement_score
            if engagement_score > 0.7:
                engagement_level = "high"
            elif engagement_score > 0.4:
                engagement_level = "medium"
            else:
                engagement_level = "low"
            
            # Determine study consistency
            if dashboard_data.streak_days >= 7:
                consistency = "excellent"
            elif dashboard_data.streak_days >= 3:
                consistency = "regular"
            else:
                consistency = "inconsistent"
            
            # Calculate weekly progress (mock calculation)
            weekly_progress = min(100.0, (dashboard_data.completion_rate * 100) + 
                                (engagement_score * 20) + 
                                (dashboard_data.streak_days * 5))
            
            # Get favorite and challenging subjects
            favorite_subject = patterns.preferred_subjects[0] if patterns.preferred_subjects else "General"
            challenging_subject = "Math"  # Would be determined from performance data
            
            # Count achievements this week (mock calculation)
            achievements_this_week = min(dashboard_data.streak_days, 7) + \
                                   (3 if dashboard_data.completion_rate > 0.8 else 1)
            
            progress = StudentProgress(
                student_id=student_id,
                student_name=companion_context.get('student_name', 'Student'),
                grade=companion_context.get('grade', 5),
                current_streak=dashboard_data.streak_days,
                total_study_hours=dashboard_data.total_study_time / 60.0,  # Convert to hours
                weekly_progress=weekly_progress,
                subjects_studied=patterns.preferred_subjects,
                favorite_subject=favorite_subject,
                challenging_subject=challenging_subject,
                overall_performance=dashboard_data.completion_rate * 100,
                engagement_level=engagement_level,
                last_active=datetime.now().isoformat(),
                achievements_this_week=achievements_this_week,
                completion_rate=dashboard_data.completion_rate,
                study_consistency=consistency
            )
            
            # Cache for quick access
            self.performance_cache[student_id] = asdict(progress)
            
            # Check for alerts
            await self._check_and_generate_alerts(student_id, progress)
            
            self.logger.info(f"Generated student progress for: {student_id}")
            return progress
            
        except Exception as e:
            self.logger.error(f"Failed to get student progress for {student_id}: {e}")
            raise AgentException(f"Progress monitoring failed: {e}")

    async def get_learning_insights(self, student_id: str, limit: int = 10) -> List[LearningInsight]:
        """Generate learning insights and recommendations for parents"""
        try:
            # Get dashboard and pattern data
            dashboard_data = await enhanced_analytics_service.generate_real_time_dashboard(student_id, None)
            patterns = await enhanced_analytics_service.track_learning_patterns(student_id)
            insights_data = await enhanced_analytics_service.generate_actionable_insights(student_id)
            
            learning_insights = []
            
            # Convert analytics insights to parent-friendly insights
            for insight in insights_data:
                # Create parent-friendly insight
                parent_insight = LearningInsight(
                    insight_id=str(uuid.uuid4()),
                    category=insight.get('category', 'performance'),
                    title=f"Learning Insight: {insight.get('title', 'General Observation')}",
                    description=self._make_parent_friendly(insight.get('description', '')),
                    severity=insight.get('priority', 'medium'),
                    recommendation=self._generate_parent_recommendation(insight),
                    action_items=self._generate_parent_action_items(insight),
                    confidence=insight.get('confidence', 0.7),
                    detected_at=datetime.now().isoformat(),
                    affects_subjects=insight.get('subjects', []),
                    estimated_impact=insight.get('priority', 'medium')
                )
                learning_insights.append(parent_insight)
            
            # Add custom insights based on patterns
            if dashboard_data.engagement_score < 0.5:
                learning_insights.append(LearningInsight(
                    insight_id=str(uuid.uuid4()),
                    category="engagement",
                    title="Low Engagement Detected",
                    description=f"Your child's engagement level is currently {dashboard_data.engagement_score:.1%}. This may indicate they need more interactive or varied learning approaches.",
                    severity=AlertPriority.HIGH.value,
                    recommendation="Consider incorporating more hands-on activities or taking breaks between study sessions.",
                    action_items=[
                        "Schedule shorter, more frequent study sessions",
                        "Introduce gamified learning elements",
                        "Take regular breaks during study time",
                        "Discuss learning preferences with your child"
                    ],
                    confidence=0.8,
                    detected_at=datetime.now().isoformat(),
                    affects_subjects=patterns.preferred_subjects,
                    estimated_impact="high"
                ))
            
            if dashboard_data.streak_days == 0:
                learning_insights.append(LearningInsight(
                    insight_id=str(uuid.uuid4()),
                    category="behavior",
                    title="Study Routine Interrupted",
                    description="Your child hasn't studied recently, which may affect learning momentum and retention.",
                    severity=AlertPriority.MEDIUM.value,
                    recommendation="Gently encourage your child to resume their learning routine with a favorite subject.",
                    action_items=[
                        "Start with a short, easy session",
                        "Choose their favorite subject to rebuild momentum",
                        "Set up a consistent daily study time",
                        "Create a positive study environment"
                    ],
                    confidence=0.9,
                    detected_at=datetime.now().isoformat(),
                    affects_subjects=["All subjects"],
                    estimated_impact="medium"
                ))
            
            return learning_insights[:limit]
            
        except Exception as e:
            self.logger.error(f"Failed to generate learning insights for {student_id}: {e}")
            return []

    async def generate_weekly_report(self, student_id: str, week_offset: int = 0) -> WeeklyReport:
        """Generate comprehensive weekly report for parents"""
        try:
            # Calculate week boundaries
            today = datetime.now()
            week_start = today - timedelta(days=today.weekday() + (week_offset * 7))
            week_end = week_start + timedelta(days=6)
            
            # Get analytics data
            dashboard_data = await enhanced_analytics_service.generate_real_time_dashboard(student_id, None)
            patterns = await enhanced_analytics_service.track_learning_patterns(student_id)
            insights = await self.get_learning_insights(student_id, limit=5)
            
            # Get companion summary
            companion_context = ai_companion_agent.get_companion_context_for_agent(student_id, "parent_dashboard")
            companion_summary = ai_companion_agent.get_personalized_response_for_agent(
                student_id, "parent_report", 
                f"This week, {companion_context.get('student_name', 'your child')} showed great dedication to learning!"
            )
            
            # Generate performance trends
            performance_trends = []
            for subject in patterns.preferred_subjects[:3]:
                # Mock trend calculation (in real implementation, this would use historical data)
                current_score = 75.0 + (hash(subject) % 20)
                previous_score = current_score + ((hash(subject) % 21) - 10)
                
                trend = "stable"
                trend_percentage = 0.0
                if current_score > previous_score + 5:
                    trend = "improving"
                    trend_percentage = ((current_score - previous_score) / previous_score) * 100
                elif current_score < previous_score - 5:
                    trend = "declining"
                    trend_percentage = ((previous_score - current_score) / previous_score) * 100
                
                performance_trends.append(PerformanceTrend(
                    subject=subject,
                    current_score=current_score,
                    previous_score=previous_score,
                    trend=trend,
                    trend_percentage=abs(trend_percentage),
                    confidence=0.8,
                    time_period="week",
                    sessions_analyzed=5,
                    recommendation=f"Continue practicing {subject}" if trend != "declining" else f"Consider additional support in {subject}"
                ))
            
            # Generate recommendations
            recommendations = [
                f"Maintain the current {dashboard_data.streak_days}-day learning streak!",
                "Consider exploring new subjects to broaden learning scope",
                "Regular study breaks help maintain focus and engagement",
                "Celebrate achievements to maintain motivation"
            ]
            
            # Generate parent action items
            parent_action_items = [
                "Review weekly progress with your child",
                "Discuss favorite subjects and learning experiences",
                "Address any challenging areas with additional support",
                "Plan fun learning activities for the upcoming week"
            ]
            
            report = WeeklyReport(
                report_id=str(uuid.uuid4()),
                student_id=student_id,
                week_start=week_start.isoformat(),
                week_end=week_end.isoformat(),
                total_study_time=dashboard_data.total_study_time / 60.0,  # Convert to hours
                sessions_completed=dashboard_data.sessions_completed,
                subjects_covered=patterns.preferred_subjects,
                achievements_earned=min(dashboard_data.streak_days, 7) + 2,
                overall_progress=dashboard_data.completion_rate * 100,
                performance_trends=performance_trends,
                key_insights=insights,
                recommendations=recommendations,
                companion_summary=companion_summary,
                parent_action_items=parent_action_items
            )
            
            self.logger.info(f"Generated weekly report for student: {student_id}")
            return report
            
        except Exception as e:
            self.logger.error(f"Failed to generate weekly report for {student_id}: {e}")
            raise AgentException(f"Report generation failed: {e}")

    async def get_parent_alerts(self, parent_email: str, limit: int = 20) -> List[ParentAlert]:
        """Get alerts for a parent"""
        alerts = self.parent_alerts.get(parent_email, [])
        return sorted(alerts, key=lambda x: x.created_at, reverse=True)[:limit]

    async def mark_alert_read(self, parent_email: str, alert_id: str, response: str = None) -> bool:
        """Mark an alert as read with optional parent response"""
        try:
            alerts = self.parent_alerts.get(parent_email, [])
            
            for alert in alerts:
                if alert.alert_id == alert_id:
                    alert.read = True
                    if response:
                        alert.parent_response = response
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to mark alert as read: {e}")
            return False

    async def send_message_to_student(self, student_id: str, parent_email: str, message: str) -> Dict:
        """Send message from parent to student"""
        try:
            message_data = {
                "message_id": str(uuid.uuid4()),
                "from": parent_email,
                "to": student_id,
                "message": message,
                "timestamp": datetime.now().isoformat(),
                "type": "parent_to_student",
                "read": False
            }
            
            # Store in communication history
            if student_id not in self.communication_history:
                self.communication_history[student_id] = []
            self.communication_history[student_id].append(message_data)
            
            # Create notification for student
            await smart_notifications_service.schedule_intelligent_reminders(student_id)
            
            self.logger.info(f"Message sent from parent to student {student_id}")
            return {"success": True, "message_id": message_data["message_id"]}
            
        except Exception as e:
            self.logger.error(f"Failed to send message: {e}")
            return {"success": False, "error": str(e)}

    async def get_communication_history(self, student_id: str, limit: int = 50) -> List[Dict]:
        """Get communication history for a student"""
        messages = self.communication_history.get(student_id, [])
        return sorted(messages, key=lambda x: x["timestamp"], reverse=True)[:limit]

    async def _check_and_generate_alerts(self, student_id: str, progress: StudentProgress) -> None:
        """Check progress and generate alerts for parents if needed"""
        try:
            # Get parent email (would come from database in real implementation)
            parent_email = f"parent_{student_id}@example.com"  # Mock parent email
            
            alerts = []
            
            # Check for low engagement
            if progress.engagement_level == "low":
                alerts.append(ParentAlert(
                    alert_id=str(uuid.uuid4()),
                    student_id=student_id,
                    alert_type=CommunicationType.CONCERN.value,
                    priority=AlertPriority.HIGH.value,
                    title="Low Engagement Alert",
                    message=f"{progress.student_name} is showing low engagement in their studies. Consider discussing their learning experience with them.",
                    details={
                        "engagement_level": progress.engagement_level,
                        "completion_rate": progress.completion_rate,
                        "suggestions": [
                            "Try shorter study sessions",
                            "Incorporate more interactive elements",
                            "Take regular breaks",
                            "Discuss learning preferences"
                        ]
                    },
                    created_at=datetime.now().isoformat(),
                    expires_at=(datetime.now() + timedelta(days=7)).isoformat(),
                    action_required=True,
                    action_buttons=[
                        {"text": "Send Encouragement", "action": "send_message"},
                        {"text": "Schedule Discussion", "action": "schedule_talk"},
                        {"text": "Contact Teacher", "action": "contact_teacher"}
                    ],
                    read=False,
                    parent_response=None
                ))
            
            # Check for broken study streak
            if progress.current_streak == 0:
                alerts.append(ParentAlert(
                    alert_id=str(uuid.uuid4()),
                    student_id=student_id,
                    alert_type=CommunicationType.REMINDER.value,
                    priority=AlertPriority.MEDIUM.value,
                    title="Study Streak Reminder",
                    message=f"{progress.student_name} hasn't studied recently. A gentle reminder might help them get back on track!",
                    details={
                        "last_study_session": progress.last_active,
                        "favorite_subject": progress.favorite_subject,
                        "suggestions": [
                            f"Start with {progress.favorite_subject} - their favorite!",
                            "Keep the session short and fun",
                            "Celebrate getting back into the routine"
                        ]
                    },
                    created_at=datetime.now().isoformat(),
                    expires_at=(datetime.now() + timedelta(days=3)).isoformat(),
                    action_required=False,
                    action_buttons=[
                        {"text": "Send Reminder", "action": "send_reminder"},
                        {"text": "View Progress", "action": "view_progress"}
                    ],
                    read=False,
                    parent_response=None
                ))
            
            # Check for achievements
            if progress.achievements_this_week > 3:
                alerts.append(ParentAlert(
                    alert_id=str(uuid.uuid4()),
                    student_id=student_id,
                    alert_type=CommunicationType.ACHIEVEMENT.value,
                    priority=AlertPriority.LOW.value,
                    title="Great Progress This Week!",
                    message=f"🎉 {progress.student_name} earned {progress.achievements_this_week} achievements this week! They're doing fantastic!",
                    details={
                        "achievements": progress.achievements_this_week,
                        "study_streak": progress.current_streak,
                        "completion_rate": f"{progress.completion_rate:.1%}",
                        "celebration_ideas": [
                            "Acknowledge their hard work",
                            "Plan a fun learning activity",
                            "Share their success with family"
                        ]
                    },
                    created_at=datetime.now().isoformat(),
                    expires_at=None,  # Achievement alerts don't expire
                    action_required=False,
                    action_buttons=[
                        {"text": "Send Congratulations", "action": "send_praise"},
                        {"text": "View Achievements", "action": "view_achievements"}
                    ],
                    read=False,
                    parent_response=None
                ))
            
            # Store alerts
            if parent_email not in self.parent_alerts:
                self.parent_alerts[parent_email] = []
            
            # Add new alerts (avoid duplicates)
            existing_types = {alert.alert_type for alert in self.parent_alerts[parent_email][-10:]}
            new_alerts = [alert for alert in alerts if alert.alert_type not in existing_types]
            
            self.parent_alerts[parent_email].extend(new_alerts)
            
            # Keep only recent alerts (last 50)
            self.parent_alerts[parent_email] = self.parent_alerts[parent_email][-50:]
            
        except Exception as e:
            self.logger.error(f"Failed to check and generate alerts: {e}")

    def _make_parent_friendly(self, description: str) -> str:
        """Convert technical descriptions to parent-friendly language"""
        replacements = {
            "engagement score": "interest level",
            "completion rate": "how much they finish",
            "learning velocity": "learning speed",
            "performance metrics": "how well they're doing",
            "cognitive load": "mental effort required",
            "retention rate": "how much they remember"
        }
        
        result = description
        for technical, friendly in replacements.items():
            result = result.replace(technical, friendly)
        
        return result

    def _generate_parent_recommendation(self, insight: Dict) -> str:
        """Generate parent-friendly recommendations"""
        category = insight.get('category', 'general')
        
        recommendations = {
            'performance': "Consider reviewing this area together and providing extra practice opportunities.",
            'engagement': "Try incorporating more interactive or hands-on learning activities.",
            'efficiency': "Help your child find their optimal study environment and schedule.",
            'wellbeing': "Ensure your child is getting enough rest and taking regular breaks."
        }
        
        return recommendations.get(category, "Keep supporting your child's learning journey with encouragement and patience.")

    def _generate_parent_action_items(self, insight: Dict) -> List[str]:
        """Generate actionable items for parents"""
        category = insight.get('category', 'general')
        
        action_items = {
            'performance': [
                "Schedule regular review sessions",
                "Create practice opportunities",
                "Celebrate small improvements",
                "Consider additional resources if needed"
            ],
            'engagement': [
                "Ask about their learning experience",
                "Try new learning approaches",
                "Make learning more interactive",
                "Connect learning to their interests"
            ],
            'efficiency': [
                "Help establish a study routine",
                "Create a distraction-free environment",
                "Discuss optimal study times",
                "Encourage regular breaks"
            ],
            'wellbeing': [
                "Monitor stress levels",
                "Ensure adequate rest",
                "Encourage physical activity",
                "Maintain a positive learning atmosphere"
            ]
        }
        
        return action_items.get(category, [
            "Support your child's learning journey",
            "Maintain open communication",
            "Celebrate their efforts and achievements"
        ])

# Global Parent Dashboard service instance
parent_dashboard_service = ParentDashboardService()