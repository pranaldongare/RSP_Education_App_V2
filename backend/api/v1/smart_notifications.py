"""
Smart Notifications API - RSP Education Agent V2 Phase 1.3
REST API endpoints for intelligent notifications with optimal study times and achievement celebrations
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from pydantic import BaseModel
import logging

from database.database import get_db
from api.v1.auth import get_current_user
from database.models import Student
from services.smart_notifications_service import smart_notifications_service
from core.exceptions import AgentException

logger = logging.getLogger(__name__)

# Pydantic models for API requests/responses
class NotificationPreferencesRequest(BaseModel):
    """Request model for updating notification preferences"""
    study_reminders: bool = True
    achievement_celebrations: bool = True
    progress_milestones: bool = True
    streak_maintenance: bool = True
    preferred_reminder_time: int = 15  # minutes before optimal time
    celebration_intensity: str = "medium"  # low, medium, high
    notification_frequency: str = "balanced"  # minimal, balanced, frequent

class AchievementCelebrationRequest(BaseModel):
    """Request model for triggering achievement celebration"""
    achievement_type: str  # first_achievement, streak, subject_mastery, performance_improvement, etc.
    title: str
    description: str
    value: Optional[int] = None  # achievement value (streak days, score, etc.)
    subject: Optional[str] = None
    metadata: Optional[Dict] = None

class NotificationActionRequest(BaseModel):
    """Request model for notification actions"""
    notification_id: str
    action_taken: str  # start_session, snooze, dismiss, share, etc.
    metadata: Optional[Dict] = None

class StudyTimeRecommendationResponse(BaseModel):
    """Response model for study time recommendations"""
    recommended_hour: int
    confidence_score: float
    suggested_subject: str
    estimated_performance: float
    session_duration: int
    reasoning: str
    alternative_times: List[int]

class CelebrationPlanResponse(BaseModel):
    """Response model for celebration plans"""
    celebration_type: str
    intensity_level: int
    duration_ms: int
    title: str
    message: str
    emoji: str
    colors: List[str]
    sounds: List[str]
    follow_up_encouragement: str
    share_options: List[str]

class SmartNotificationResponse(BaseModel):
    """Response model for smart notifications"""
    notification_id: str
    notification_type: str
    priority: str
    title: str
    message: str
    emoji: str
    scheduled_time: str
    expires_at: str
    action_buttons: List[Dict]
    metadata: Dict
    companion_enhanced: bool
    personalization_data: Dict

# Create API router
router = APIRouter(prefix="/smart-notifications", tags=["Smart Notifications"])

@router.get("/study-time-recommendation")
async def get_study_time_recommendation(
    current_user: Student = Depends(get_current_user)
):
    """Get AI-powered optimal study time recommendation"""
    try:
        recommendation = await smart_notifications_service.analyze_optimal_study_times(
            student_id=current_user.student_id
        )
        
        return {
            "success": True,
            "message": f"🧠 Optimal study time analyzed for {current_user.name}!",
            "data": {
                "recommended_hour": recommendation.recommended_hour,
                "confidence_score": recommendation.confidence_score,
                "suggested_subject": recommendation.suggested_subject,
                "estimated_performance": recommendation.estimated_performance,
                "session_duration": recommendation.session_duration,
                "reasoning": recommendation.reasoning,
                "alternative_times": recommendation.alternative_times,
                "formatted_time": f"{recommendation.recommended_hour:02d}:00",
                "confidence_display": f"{recommendation.confidence_score:.0%}"
            },
            "user_context": {
                "student_id": current_user.student_id,
                "name": current_user.name,
                "grade": current_user.grade
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting study time recommendation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during recommendation generation"
        )

@router.post("/schedule-reminders")
async def schedule_study_reminders(
    current_user: Student = Depends(get_current_user)
):
    """Schedule intelligent study reminders based on patterns"""
    try:
        await smart_notifications_service.schedule_intelligent_reminders(
            student_id=current_user.student_id
        )
        
        return {
            "success": True,
            "message": f"🔔 Smart study reminders scheduled for {current_user.name}!",
            "reminder_info": {
                "message": "We've analyzed your learning patterns to schedule optimal study reminders",
                "features": [
                    "📊 Based on your peak performance hours",
                    "🎯 Personalized subject recommendations", 
                    "🐻 Enhanced with your AI companion's personality",
                    "⏰ Timed for maximum learning effectiveness"
                ]
            }
        }
        
    except Exception as e:
        logger.error(f"Error scheduling reminders: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during reminder scheduling"
        )

@router.post("/trigger-celebration")
async def trigger_achievement_celebration(
    request: AchievementCelebrationRequest,
    current_user: Student = Depends(get_current_user)
):
    """Trigger celebration for student achievement"""
    try:
        achievement_data = {
            "type": request.achievement_type,
            "title": request.title,
            "description": request.description,
            "value": request.value,
            "subject": request.subject,
            "metadata": request.metadata or {},
            "student_id": current_user.student_id,
            "timestamp": None  # Will be set by service
        }
        
        celebration_plan = await smart_notifications_service.trigger_achievement_celebration(
            student_id=current_user.student_id,
            achievement_data=achievement_data
        )
        
        return {
            "success": True,
            "message": f"🎉 Achievement celebration triggered for {current_user.name}!",
            "celebration": {
                "celebration_type": celebration_plan.celebration_type,
                "intensity_level": celebration_plan.intensity_level,
                "duration_ms": celebration_plan.duration_ms,
                "title": celebration_plan.title,
                "message": celebration_plan.message,
                "emoji": celebration_plan.emoji,
                "colors": celebration_plan.colors,
                "sounds": celebration_plan.sounds,
                "follow_up_encouragement": celebration_plan.follow_up_encouragement,
                "share_options": celebration_plan.share_options
            },
            "achievement": {
                "type": request.achievement_type,
                "title": request.title,
                "description": request.description
            }
        }
        
    except Exception as e:
        logger.error(f"Error triggering celebration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during celebration trigger"
        )

@router.post("/send-progress-updates")
async def send_progress_milestone_updates(
    stakeholders: List[str] = ["student", "parent"],
    current_user: Student = Depends(get_current_user)
):
    """Send progress milestone notifications to stakeholders"""
    try:
        await smart_notifications_service.send_progress_updates(
            student_id=current_user.student_id,
            stakeholders=stakeholders
        )
        
        return {
            "success": True,
            "message": f"📈 Progress milestone updates sent for {current_user.name}!",
            "update_info": {
                "stakeholders": stakeholders,
                "milestone_types": [
                    "🔥 Learning streak achievements",
                    "⏰ Study time milestones", 
                    "📚 Subject mastery progress",
                    "🏆 Performance improvements"
                ],
                "delivery_status": "Notifications queued for delivery"
            }
        }
        
    except Exception as e:
        logger.error(f"Error sending progress updates: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during progress update"
        )

@router.get("/pending")
async def get_pending_notifications(
    limit: int = 10,
    current_user: Student = Depends(get_current_user)
):
    """Get pending notifications for the current user"""
    try:
        notifications = await smart_notifications_service.get_pending_notifications(
            student_id=current_user.student_id,
            limit=limit
        )
        
        notifications_data = []
        for notification in notifications:
            notifications_data.append({
                "notification_id": notification.notification_id,
                "notification_type": notification.notification_type,
                "priority": notification.priority,
                "title": notification.title,
                "message": notification.message,
                "emoji": notification.emoji,
                "scheduled_time": notification.scheduled_time,
                "expires_at": notification.expires_at,
                "action_buttons": notification.action_buttons,
                "metadata": notification.metadata,
                "companion_enhanced": notification.companion_enhanced,
                "personalization_data": notification.personalization_data
            })
        
        return {
            "success": True,
            "message": f"📬 {len(notifications)} pending notifications for {current_user.name}!",
            "data": notifications_data,
            "summary": {
                "total_notifications": len(notifications),
                "types": list(set(n.notification_type for n in notifications)),
                "priorities": list(set(n.priority for n in notifications))
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting pending notifications: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during notification retrieval"
        )

@router.post("/mark-read")
async def mark_notification_read(
    request: NotificationActionRequest,
    current_user: Student = Depends(get_current_user)
):
    """Mark a notification as read and record action taken"""
    try:
        success = await smart_notifications_service.mark_notification_read(
            student_id=current_user.student_id,
            notification_id=request.notification_id,
            action_taken=request.action_taken
        )
        
        if success:
            return {
                "success": True,
                "message": f"✅ Notification marked as read for {current_user.name}!",
                "action_info": {
                    "notification_id": request.notification_id,
                    "action_taken": request.action_taken,
                    "metadata": request.metadata
                }
            }
        else:
            return {
                "success": False,
                "message": "Notification not found or already processed",
                "error": "Notification not found"
            }
        
    except Exception as e:
        logger.error(f"Error marking notification as read: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during notification update"
        )

@router.get("/preferences")
async def get_notification_preferences(
    current_user: Student = Depends(get_current_user)
):
    """Get notification preferences for the current user"""
    try:
        preferences = await smart_notifications_service.get_notification_preferences(
            student_id=current_user.student_id
        )
        
        return {
            "success": True,
            "message": f"⚙️ Notification preferences for {current_user.name}!",
            "data": preferences,
            "settings_info": {
                "customizable_options": [
                    "Study reminder timing",
                    "Achievement celebration intensity",
                    "Progress milestone frequency",
                    "Notification types to receive"
                ]
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting notification preferences: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during preferences retrieval"
        )

@router.post("/preferences")
async def update_notification_preferences(
    request: NotificationPreferencesRequest,
    current_user: Student = Depends(get_current_user)
):
    """Update notification preferences for the current user"""
    try:
        preferences = {
            "study_reminders": request.study_reminders,
            "achievement_celebrations": request.achievement_celebrations,
            "progress_milestones": request.progress_milestones,
            "streak_maintenance": request.streak_maintenance,
            "preferred_reminder_time": request.preferred_reminder_time,
            "celebration_intensity": request.celebration_intensity,
            "notification_frequency": request.notification_frequency
        }
        
        await smart_notifications_service.update_notification_preferences(
            student_id=current_user.student_id,
            preferences=preferences
        )
        
        return {
            "success": True,
            "message": f"⚙️ Notification preferences updated for {current_user.name}!",
            "updated_preferences": preferences,
            "confirmation": {
                "study_reminders": "enabled" if request.study_reminders else "disabled",
                "celebration_style": request.celebration_intensity,
                "reminder_timing": f"{request.preferred_reminder_time} minutes before optimal time"
            }
        }
        
    except Exception as e:
        logger.error(f"Error updating notification preferences: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during preferences update"
        )

@router.get("/history")
async def get_notification_history(
    limit: int = 50,
    current_user: Student = Depends(get_current_user)
):
    """Get notification history for the current user"""
    try:
        # Get notification history from service
        history = smart_notifications_service.notification_history.get(
            current_user.student_id, []
        )
        
        # Limit and format results
        recent_history = history[-limit:] if len(history) > limit else history
        
        # Calculate statistics
        total_notifications = len(history)
        types_count = {}
        actions_count = {}
        
        for entry in history:
            notification_type = entry.get('type', 'unknown')
            action = entry.get('action_taken', 'no_action')
            
            types_count[notification_type] = types_count.get(notification_type, 0) + 1
            actions_count[action] = actions_count.get(action, 0) + 1
        
        return {
            "success": True,
            "message": f"📋 Notification history for {current_user.name}!",
            "data": recent_history,
            "statistics": {
                "total_notifications": total_notifications,
                "showing_recent": len(recent_history),
                "types_breakdown": types_count,
                "actions_breakdown": actions_count,
                "engagement_rate": len([h for h in history if h.get('action_taken') != 'dismiss']) / max(total_notifications, 1)
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting notification history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during history retrieval"
        )

@router.post("/quick-celebration")
async def trigger_quick_celebration(
    achievement_title: str,
    achievement_type: str = "general",
    current_user: Student = Depends(get_current_user)
):
    """Quick endpoint to trigger a simple celebration"""
    try:
        achievement_data = {
            "type": achievement_type,
            "title": achievement_title,
            "description": f"Great work on: {achievement_title}",
            "value": 1,
            "student_id": current_user.student_id
        }
        
        celebration_plan = await smart_notifications_service.trigger_achievement_celebration(
            student_id=current_user.student_id,
            achievement_data=achievement_data
        )
        
        return {
            "success": True,
            "message": f"🎉 Quick celebration for {current_user.name}!",
            "celebration": {
                "type": celebration_plan.celebration_type,
                "message": celebration_plan.message,
                "emoji": celebration_plan.emoji,
                "duration_ms": celebration_plan.duration_ms,
                "intensity": celebration_plan.intensity_level,
                "follow_up": celebration_plan.follow_up_encouragement
            }
        }
        
    except Exception as e:
        logger.error(f"Error triggering quick celebration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during quick celebration"
        )

@router.get("/dashboard-summary")
async def get_notifications_dashboard_summary(
    current_user: Student = Depends(get_current_user)
):
    """Get comprehensive notifications dashboard summary"""
    try:
        # Get pending notifications
        pending = await smart_notifications_service.get_pending_notifications(
            student_id=current_user.student_id,
            limit=5
        )
        
        # Get preferences
        preferences = await smart_notifications_service.get_notification_preferences(
            student_id=current_user.student_id
        )
        
        # Get recent history
        history = smart_notifications_service.notification_history.get(
            current_user.student_id, []
        )
        recent_history = history[-10:] if len(history) > 10 else history
        
        # Get next study time recommendation
        recommendation = await smart_notifications_service.analyze_optimal_study_times(
            student_id=current_user.student_id
        )
        
        return {
            "success": True,
            "message": f"📊 Notifications dashboard for {current_user.name}!",
            "data": {
                "pending_notifications": {
                    "count": len(pending),
                    "high_priority": len([n for n in pending if n.priority == "high"]),
                    "types": list(set(n.notification_type for n in pending))
                },
                "preferences": preferences,
                "recent_activity": {
                    "total_received": len(history),
                    "recent_count": len(recent_history),
                    "engagement_rate": len([h for h in recent_history if h.get('action_taken') != 'dismiss']) / max(len(recent_history), 1)
                },
                "next_study_recommendation": {
                    "optimal_hour": recommendation.recommended_hour,
                    "formatted_time": f"{recommendation.recommended_hour:02d}:00",
                    "subject": recommendation.suggested_subject,
                    "confidence": f"{recommendation.confidence_score:.0%}",
                    "reasoning": recommendation.reasoning
                },
                "smart_features": [
                    "📊 AI-powered optimal study time analysis",
                    "🎉 Personalized achievement celebrations",
                    "🏆 Progress milestone tracking",
                    "🐻 Companion-enhanced messaging",
                    "⚙️ Customizable notification preferences"
                ]
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting notifications dashboard: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during dashboard generation"
        )