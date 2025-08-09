"""
Smart Notifications Service - RSP Education Agent V2 Phase 1.3
Intelligent notification system with optimal study times, achievement celebrations, and progress milestones
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
from services.enhanced_analytics_service import enhanced_analytics_service

logger = logging.getLogger(__name__)

class NotificationType(Enum):
    STUDY_REMINDER = "study_reminder"
    ACHIEVEMENT_CELEBRATION = "achievement_celebration"
    PROGRESS_MILESTONE = "progress_milestone"
    STREAK_MAINTENANCE = "streak_maintenance"
    BREAK_REMINDER = "break_reminder"
    ENCOURAGEMENT = "encouragement"
    CHALLENGE_INVITATION = "challenge_invitation"
    LEARNING_TIP = "learning_tip"

class NotificationPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class CelebrationType(Enum):
    CONFETTI = "confetti"
    BADGE_UNLOCK = "badge_unlock"
    COMPANION_DANCE = "companion_dance"
    FIREWORKS = "fireworks"
    RAINBOW = "rainbow"
    SPARKLES = "sparkles"
    TROPHY = "trophy"
    BALLOON_DROP = "balloon_drop"

@dataclass
class StudyTimeRecommendation:
    """Recommendation for optimal study time"""
    recommended_hour: int  # Hour of day (0-23)
    confidence_score: float  # Confidence in recommendation (0-1)
    suggested_subject: str  # Subject to focus on
    estimated_performance: float  # Expected performance score
    session_duration: int  # Recommended session length in minutes
    reasoning: str  # Why this time is recommended
    alternative_times: List[int]  # Alternative good times

@dataclass
class CelebrationPlan:
    """Plan for celebrating student achievements"""
    celebration_type: str  # Type of celebration
    intensity_level: int  # Intensity 1-10
    duration_ms: int  # Duration in milliseconds
    title: str  # Celebration title
    message: str  # Celebration message
    emoji: str  # Primary emoji
    colors: List[str]  # Celebration colors
    sounds: List[str]  # Sound effects
    follow_up_encouragement: str  # Message after celebration
    share_options: List[str]  # Options to share the achievement

@dataclass
class ProgressMilestone:
    """Progress milestone notification"""
    milestone_type: str  # Type of milestone
    title: str  # Milestone title
    description: str  # Detailed description
    progress_percentage: float  # Progress toward milestone
    current_value: int  # Current progress value
    target_value: int  # Target value for milestone
    estimated_completion: str  # Estimated completion time
    rewards: List[str]  # Rewards for reaching milestone
    next_steps: List[str]  # Suggested next steps

@dataclass
class SmartNotification:
    """Smart notification with all details"""
    notification_id: str
    notification_type: str
    priority: str
    title: str
    message: str
    emoji: str
    scheduled_time: str  # ISO timestamp
    expires_at: str  # ISO timestamp
    action_buttons: List[Dict]  # Interactive buttons
    metadata: Dict  # Additional data
    companion_enhanced: bool  # Whether companion personality was applied
    personalization_data: Dict  # Student-specific personalization

class SmartNotificationsService:
    """Smart Notifications Service with AI-powered timing and personalization"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.SmartNotificationsService")
        
        # In-memory storage for notifications (in production, use proper database)
        self.pending_notifications: Dict[str, List[SmartNotification]] = {}
        self.notification_history: Dict[str, List[Dict]] = {}
        self.user_preferences: Dict[str, Dict] = {}
        
        # Celebration templates
        self.celebration_templates = {
            "first_achievement": {
                "type": CelebrationType.CONFETTI.value,
                "intensity": 8,
                "duration": 3000,
                "message": "Congratulations on your first achievement! This is just the beginning of your amazing journey!"
            },
            "streak_milestone": {
                "type": CelebrationType.FIREWORKS.value,
                "intensity": 9,
                "duration": 4000,
                "message": "Incredible! Your dedication to learning is truly inspiring!"
            },
            "subject_mastery": {
                "type": CelebrationType.TROPHY.value,
                "intensity": 10,
                "duration": 5000,
                "message": "Outstanding! You've shown real mastery of this subject!"
            },
            "performance_breakthrough": {
                "type": CelebrationType.RAINBOW.value,
                "intensity": 7,
                "duration": 3500,
                "message": "Amazing breakthrough! Your hard work is really paying off!"
            },
            "consistent_learning": {
                "type": CelebrationType.SPARKLES.value,
                "intensity": 6,
                "duration": 2500,
                "message": "Your consistency is remarkable! Keep up the excellent work!"
            }
        }
        
    async def analyze_optimal_study_times(self, student_id: str) -> StudyTimeRecommendation:
        """Analyze student data to find optimal study times"""
        try:
            # Get learning patterns from enhanced analytics
            patterns = await enhanced_analytics_service.track_learning_patterns(student_id)
            
            # Get companion context for personalization
            companion_context = ai_companion_agent.get_companion_context_for_agent(student_id, "notifications")
            
            # Determine best hour based on patterns
            if patterns.peak_learning_hours:
                recommended_hour = patterns.peak_learning_hours[0]
                confidence_score = 0.9
                reasoning = f"Based on your learning history, you perform best around {recommended_hour}:00"
            else:
                # Default recommendations based on grade and general patterns
                companion_name = companion_context.get('student_name', 'student')
                grade = companion_context.get('grade', 5)
                
                if grade <= 5:
                    recommended_hour = 16  # 4 PM for younger students
                    reasoning = "Afternoon is typically great for elementary students"
                elif grade <= 8:
                    recommended_hour = 15  # 3 PM for middle school
                    reasoning = "Mid-afternoon works well for middle school students"
                else:
                    recommended_hour = 14  # 2 PM for high school
                    reasoning = "Early afternoon is optimal for focused study"
                
                confidence_score = 0.6
            
            # Suggest subject based on patterns and companion context
            preferred_subjects = patterns.preferred_subjects
            struggle_areas = companion_context.get('struggle_areas', [])
            
            if struggle_areas:
                suggested_subject = struggle_areas[0]
                reasoning += f". Focus on {suggested_subject} to improve your skills"
            elif preferred_subjects:
                suggested_subject = preferred_subjects[0]
                reasoning += f". Continue building on your strength in {suggested_subject}"
            else:
                suggested_subject = "Math"  # Default
            
            # Estimate performance and session duration
            estimated_performance = 0.75 + (confidence_score * 0.2)
            session_duration = patterns.optimal_session_length
            
            # Alternative times
            alternative_times = patterns.peak_learning_hours[1:4] if len(patterns.peak_learning_hours) > 1 else []
            
            recommendation = StudyTimeRecommendation(
                recommended_hour=recommended_hour,
                confidence_score=confidence_score,
                suggested_subject=suggested_subject,
                estimated_performance=estimated_performance,
                session_duration=session_duration,
                reasoning=reasoning,
                alternative_times=alternative_times
            )
            
            self.logger.info(f"Generated study time recommendation for student: {student_id}")
            return recommendation
            
        except Exception as e:
            self.logger.error(f"Failed to analyze optimal study times for {student_id}: {e}")
            # Return default recommendation
            return StudyTimeRecommendation(
                recommended_hour=15,
                confidence_score=0.5,
                suggested_subject="General",
                estimated_performance=0.7,
                session_duration=25,
                reasoning="General afternoon study time recommendation",
                alternative_times=[14, 16, 17]
            )

    async def schedule_intelligent_reminders(self, student_id: str) -> None:
        """Schedule intelligent study reminders based on patterns"""
        try:
            # Get study time recommendation
            recommendation = await self.analyze_optimal_study_times(student_id)
            
            # Get companion context for personalized messaging
            companion_context = ai_companion_agent.get_companion_context_for_agent(student_id, "notifications")
            student_name = companion_context.get('student_name', 'champion')
            current_mood = companion_context.get('current_mood', 'happy')
            
            # Create personalized reminder message
            if current_mood == 'excited':
                base_message = f"Hey {student_name}! Ready for an amazing learning session? 🚀"
            elif current_mood == 'encouraging':
                base_message = f"You've got this, {student_name}! Time to shine in your studies! ⭐"
            elif current_mood == 'playful':
                base_message = f"Learning time, {student_name}! Let's make it fun and exciting! 🎮"
            else:
                base_message = f"Perfect time to learn, {student_name}! Your brain is ready! 🧠"
            
            # Enhance message with companion personality
            enhanced_message = ai_companion_agent.get_personalized_response_for_agent(
                student_id, "notifications", base_message
            )
            
            # Calculate reminder time (15 minutes before recommended time)
            now = datetime.now()
            reminder_time = now.replace(hour=recommendation.recommended_hour, minute=0, second=0, microsecond=0)
            if reminder_time <= now:
                reminder_time += timedelta(days=1)  # Schedule for tomorrow
            reminder_time -= timedelta(minutes=15)  # 15 minutes before
            
            # Create notification
            notification = SmartNotification(
                notification_id=f"study_reminder_{student_id}_{int(reminder_time.timestamp())}",
                notification_type=NotificationType.STUDY_REMINDER.value,
                priority=NotificationPriority.MEDIUM.value,
                title="🧠 Perfect Time to Learn!",
                message=enhanced_message,
                emoji="🧠",
                scheduled_time=reminder_time.isoformat(),
                expires_at=(reminder_time + timedelta(hours=2)).isoformat(),
                action_buttons=[
                    {"text": "Start Learning 🚀", "action": "start_session", "subject": recommendation.suggested_subject},
                    {"text": "Remind me in 30 min", "action": "snooze", "duration": 30},
                    {"text": "Not now", "action": "dismiss"}
                ],
                metadata={
                    "recommendation": asdict(recommendation),
                    "confidence": recommendation.confidence_score,
                    "suggested_subject": recommendation.suggested_subject
                },
                companion_enhanced=True,
                personalization_data={
                    "student_name": student_name,
                    "mood": current_mood,
                    "companion_available": companion_context.get('companion_available', False)
                }
            )
            
            # Store notification
            if student_id not in self.pending_notifications:
                self.pending_notifications[student_id] = []
            self.pending_notifications[student_id].append(notification)
            
            self.logger.info(f"Scheduled intelligent reminder for student: {student_id} at {reminder_time}")
            
        except Exception as e:
            self.logger.error(f"Failed to schedule reminders for {student_id}: {e}")

    async def trigger_achievement_celebration(self, student_id: str, achievement_data: Dict) -> CelebrationPlan:
        """Trigger celebration for student achievement"""
        try:
            # Get companion context for personalized celebration
            companion_context = ai_companion_agent.get_companion_context_for_agent(student_id, "notifications")
            student_name = companion_context.get('student_name', 'champion')
            
            # Determine celebration type based on achievement
            achievement_type = achievement_data.get('type', 'general')
            achievement_value = achievement_data.get('value', 0)
            
            # Select appropriate celebration template
            if achievement_type == 'first_achievement':
                template = self.celebration_templates['first_achievement']
            elif achievement_type == 'streak' and achievement_value >= 7:
                template = self.celebration_templates['streak_milestone']
            elif achievement_type == 'subject_mastery':
                template = self.celebration_templates['subject_mastery']
            elif achievement_type == 'performance_improvement':
                template = self.celebration_templates['performance_breakthrough']
            else:
                template = self.celebration_templates['consistent_learning']
            
            # Get companion mood for celebration intensity adjustment
            current_mood = companion_context.get('current_mood', 'happy')
            intensity_modifier = 1.0
            
            if current_mood == 'excited':
                intensity_modifier = 1.2
            elif current_mood == 'proud':
                intensity_modifier = 1.1
            elif current_mood == 'concerned':
                intensity_modifier = 0.8
            
            # Calculate celebration parameters
            celebration_type = template['type']
            intensity_level = min(10, int(template['intensity'] * intensity_modifier))
            duration_ms = int(template['duration'] * intensity_modifier)
            
            # Create personalized celebration message
            base_message = template['message']
            personalized_message = f"{student_name}, {base_message.lower()}"
            
            # Enhance with companion personality
            enhanced_message = ai_companion_agent.get_personalized_response_for_agent(
                student_id, "celebrations", personalized_message
            )
            
            # Select celebration elements
            celebration_emojis = {
                'confetti': '🎉',
                'fireworks': '🎆',
                'trophy': '🏆',
                'rainbow': '🌈',
                'sparkles': '✨',
                'badge_unlock': '🎖️',
                'companion_dance': '🐻',
                'balloon_drop': '🎈'
            }
            
            celebration_colors = {
                'confetti': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'],
                'fireworks': ['#FF1744', '#FF9100', '#00E676', '#2979FF'],
                'trophy': ['#FFD700', '#FFA500', '#FF6347'],
                'rainbow': ['#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#0000FF', '#4B0082', '#9400D3'],
                'sparkles': ['#FFD700', '#FFFF00', '#FFF8DC'],
                'badge_unlock': ['#4CAF50', '#2196F3', '#FF9800'],
                'companion_dance': ['#FF69B4', '#98FB98', '#87CEEB'],
                'balloon_drop': ['#FF1493', '#00CED1', '#FFD700', '#32CD32']
            }
            
            # Generate follow-up encouragement
            follow_up_messages = [
                f"You're on fire, {student_name}! What's next on your learning adventure?",
                f"Amazing work, {student_name}! Ready to tackle your next challenge?",
                f"Incredible progress, {student_name}! I'm so proud of you!",
                f"You rock, {student_name}! Let's keep this momentum going!",
                f"Outstanding achievement, {student_name}! You inspire me!"
            ]
            
            follow_up = random.choice(follow_up_messages)
            enhanced_follow_up = ai_companion_agent.get_personalized_response_for_agent(
                student_id, "celebrations", follow_up
            )
            
            # Create celebration plan
            celebration_plan = CelebrationPlan(
                celebration_type=celebration_type,
                intensity_level=intensity_level,
                duration_ms=duration_ms,
                title=f"🎉 {achievement_data.get('title', 'Amazing Achievement')}!",
                message=enhanced_message,
                emoji=celebration_emojis.get(celebration_type, '🎉'),
                colors=celebration_colors.get(celebration_type, ['#FF6B6B', '#4ECDC4']),
                sounds=['cheer', 'applause', 'success_bell'],
                follow_up_encouragement=enhanced_follow_up,
                share_options=['Share with Friends', 'Tell My Parents', 'Post to Class']
            )
            
            # Create celebration notification
            celebration_notification = SmartNotification(
                notification_id=f"celebration_{student_id}_{int(datetime.now().timestamp())}",
                notification_type=NotificationType.ACHIEVEMENT_CELEBRATION.value,
                priority=NotificationPriority.HIGH.value,
                title=celebration_plan.title,
                message=celebration_plan.message,
                emoji=celebration_plan.emoji,
                scheduled_time=datetime.now().isoformat(),
                expires_at=(datetime.now() + timedelta(minutes=10)).isoformat(),
                action_buttons=[
                    {"text": "Continue Learning 🚀", "action": "continue_session"},
                    {"text": "Share Achievement 📱", "action": "share", "options": celebration_plan.share_options},
                    {"text": "Celebrate More! 🎉", "action": "replay_celebration"}
                ],
                metadata={
                    "celebration_plan": asdict(celebration_plan),
                    "achievement_data": achievement_data,
                    "intensity": intensity_level
                },
                companion_enhanced=True,
                personalization_data={
                    "student_name": student_name,
                    "celebration_type": celebration_type,
                    "mood": current_mood
                }
            )
            
            # Store notification
            if student_id not in self.pending_notifications:
                self.pending_notifications[student_id] = []
            self.pending_notifications[student_id].append(celebration_notification)
            
            self.logger.info(f"Triggered achievement celebration for student: {student_id}")
            return celebration_plan
            
        except Exception as e:
            self.logger.error(f"Failed to trigger celebration for {student_id}: {e}")
            # Return default celebration
            return CelebrationPlan(
                celebration_type=CelebrationType.CONFETTI.value,
                intensity_level=5,
                duration_ms=3000,
                title="🎉 Great Job!",
                message="Congratulations on your achievement!",
                emoji="🎉",
                colors=['#FF6B6B', '#4ECDC4'],
                sounds=['cheer'],
                follow_up_encouragement="Keep up the amazing work!",
                share_options=['Share with Friends']
            )

    async def send_progress_updates(self, student_id: str, stakeholders: List[str]) -> None:
        """Send progress milestone notifications"""
        try:
            # Get comprehensive analytics for progress assessment
            dashboard_data = await enhanced_analytics_service.generate_real_time_dashboard(student_id, None)
            patterns = await enhanced_analytics_service.track_learning_patterns(student_id)
            
            # Get companion context
            companion_context = ai_companion_agent.get_companion_context_for_agent(student_id, "notifications")
            student_name = companion_context.get('student_name', 'Student')
            
            # Identify significant milestones
            milestones = []
            
            # Learning streak milestone
            if dashboard_data.streak_days > 0 and dashboard_data.streak_days % 7 == 0:
                milestones.append(ProgressMilestone(
                    milestone_type="learning_streak",
                    title=f"🔥 {dashboard_data.streak_days}-Day Learning Streak!",
                    description=f"{student_name} has maintained consistent learning for {dashboard_data.streak_days} days straight!",
                    progress_percentage=1.0,
                    current_value=dashboard_data.streak_days,
                    target_value=dashboard_data.streak_days,
                    estimated_completion="Achieved!",
                    rewards=["Streak Master Badge", "Bonus XP Points", "Special Recognition"],
                    next_steps=[f"Continue streak to reach {dashboard_data.streak_days + 7} days", "Maintain daily learning habit"]
                ))
            
            # Study time milestone
            hours_studied = dashboard_data.total_study_time / 60
            if hours_studied >= 10 and int(hours_studied) % 10 == 0:
                milestones.append(ProgressMilestone(
                    milestone_type="study_time",
                    title=f"⏰ {int(hours_studied)} Hours of Learning!",
                    description=f"{student_name} has dedicated {int(hours_studied)} hours to learning!",
                    progress_percentage=1.0,
                    current_value=int(hours_studied),
                    target_value=int(hours_studied),
                    estimated_completion="Achieved!",
                    rewards=["Time Master Certificate", "Study Champion Badge"],
                    next_steps=[f"Aim for {int(hours_studied) + 10} hours", "Maintain quality study sessions"]
                ))
            
            # Subject mastery progress
            for subject in patterns.preferred_subjects[:3]:  # Top 3 subjects
                # Simulate progress calculation (in real implementation, this would come from actual performance data)
                progress = min(0.9, dashboard_data.completion_rate + random.uniform(0.1, 0.2))
                if progress >= 0.8:
                    milestones.append(ProgressMilestone(
                        milestone_type="subject_progress",
                        title=f"📚 {subject} Mastery Progress",
                        description=f"{student_name} is showing excellent progress in {subject}!",
                        progress_percentage=progress,
                        current_value=int(progress * 100),
                        target_value=100,
                        estimated_completion="Soon!" if progress < 0.95 else "Almost there!",
                        rewards=["Subject Expert Badge", "Advanced Content Unlock"],
                        next_steps=[f"Complete remaining {subject} exercises", "Take advanced assessment"]
                    ))
            
            # Create milestone notifications
            for milestone in milestones:
                # Personalize message with companion
                base_message = milestone.description
                enhanced_message = ai_companion_agent.get_personalized_response_for_agent(
                    student_id, "milestones", base_message
                )
                
                milestone_notification = SmartNotification(
                    notification_id=f"milestone_{milestone.milestone_type}_{student_id}_{int(datetime.now().timestamp())}",
                    notification_type=NotificationType.PROGRESS_MILESTONE.value,
                    priority=NotificationPriority.MEDIUM.value,
                    title=milestone.title,
                    message=enhanced_message,
                    emoji="🏆",
                    scheduled_time=datetime.now().isoformat(),
                    expires_at=(datetime.now() + timedelta(hours=24)).isoformat(),
                    action_buttons=[
                        {"text": "View Progress Details", "action": "view_progress"},
                        {"text": "Share Milestone", "action": "share_milestone"},
                        {"text": "Continue Learning", "action": "continue_session"}
                    ],
                    metadata={
                        "milestone": asdict(milestone),
                        "stakeholders": stakeholders,
                        "progress_data": dashboard_data.__dict__
                    },
                    companion_enhanced=True,
                    personalization_data={
                        "student_name": student_name,
                        "milestone_type": milestone.milestone_type
                    }
                )
                
                # Store notification
                if student_id not in self.pending_notifications:
                    self.pending_notifications[student_id] = []
                self.pending_notifications[student_id].append(milestone_notification)
            
            self.logger.info(f"Generated {len(milestones)} progress milestone notifications for student: {student_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to send progress updates for {student_id}: {e}")

    async def get_pending_notifications(self, student_id: str, limit: int = 10) -> List[SmartNotification]:
        """Get pending notifications for a student"""
        try:
            notifications = self.pending_notifications.get(student_id, [])
            
            # Filter by current time (only show notifications that should be displayed now)
            now = datetime.now()
            current_notifications = []
            
            for notification in notifications:
                scheduled_time = datetime.fromisoformat(notification.scheduled_time)
                expires_at = datetime.fromisoformat(notification.expires_at)
                
                if scheduled_time <= now <= expires_at:
                    current_notifications.append(notification)
            
            # Sort by priority and scheduled time
            priority_order = {'urgent': 4, 'high': 3, 'medium': 2, 'low': 1}
            current_notifications.sort(
                key=lambda n: (priority_order.get(n.priority, 1), n.scheduled_time),
                reverse=True
            )
            
            return current_notifications[:limit]
            
        except Exception as e:
            self.logger.error(f"Failed to get pending notifications for {student_id}: {e}")
            return []

    async def mark_notification_read(self, student_id: str, notification_id: str, action_taken: str = None) -> bool:
        """Mark a notification as read and optionally record action taken"""
        try:
            notifications = self.pending_notifications.get(student_id, [])
            
            # Find and remove the notification
            updated_notifications = []
            notification_found = False
            
            for notification in notifications:
                if notification.notification_id == notification_id:
                    notification_found = True
                    
                    # Record in history
                    if student_id not in self.notification_history:
                        self.notification_history[student_id] = []
                    
                    self.notification_history[student_id].append({
                        'notification_id': notification_id,
                        'type': notification.notification_type,
                        'read_at': datetime.now().isoformat(),
                        'action_taken': action_taken,
                        'metadata': notification.metadata
                    })
                    
                    # Keep only last 100 history entries
                    if len(self.notification_history[student_id]) > 100:
                        self.notification_history[student_id] = self.notification_history[student_id][-100:]
                    
                else:
                    updated_notifications.append(notification)
            
            if notification_found:
                self.pending_notifications[student_id] = updated_notifications
                self.logger.info(f"Marked notification {notification_id} as read for student: {student_id}")
            
            return notification_found
            
        except Exception as e:
            self.logger.error(f"Failed to mark notification as read for {student_id}: {e}")
            return False

    async def get_notification_preferences(self, student_id: str) -> Dict:
        """Get notification preferences for a student"""
        return self.user_preferences.get(student_id, {
            'study_reminders': True,
            'achievement_celebrations': True,
            'progress_milestones': True,
            'streak_maintenance': True,
            'preferred_reminder_time': 15,  # minutes before optimal time
            'celebration_intensity': 'medium',
            'notification_frequency': 'balanced'
        })

    async def update_notification_preferences(self, student_id: str, preferences: Dict) -> None:
        """Update notification preferences for a student"""
        try:
            self.user_preferences[student_id] = preferences
            self.logger.info(f"Updated notification preferences for student: {student_id}")
        except Exception as e:
            self.logger.error(f"Failed to update preferences for {student_id}: {e}")

    def _clean_expired_notifications(self) -> None:
        """Clean up expired notifications (should be called periodically)"""
        try:
            now = datetime.now()
            
            for student_id in self.pending_notifications:
                valid_notifications = []
                
                for notification in self.pending_notifications[student_id]:
                    expires_at = datetime.fromisoformat(notification.expires_at)
                    if expires_at > now:
                        valid_notifications.append(notification)
                
                self.pending_notifications[student_id] = valid_notifications
            
            self.logger.info("Cleaned up expired notifications")
            
        except Exception as e:
            self.logger.error(f"Failed to clean expired notifications: {e}")

# Global Smart Notifications service instance
smart_notifications_service = SmartNotificationsService()