"""
Parent Dashboard API - RSP Education Agent V2 Phase 2.1
REST API endpoints for real-time parent monitoring, communication, and comprehensive reporting
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from pydantic import BaseModel, EmailStr
import logging

from database.database import get_db
from api.v1.auth import get_current_user
from database.models import Student
from services.parent_dashboard_service import parent_dashboard_service
from core.exceptions import AgentException

logger = logging.getLogger(__name__)

# Pydantic models for API requests/responses
class ParentMessageRequest(BaseModel):
    """Request model for parent-to-student messages"""
    student_id: str
    message: str
    parent_email: EmailStr
    message_type: str = "encouragement"  # encouragement, reminder, question, praise

class AlertResponseRequest(BaseModel):
    """Request model for parent alert responses"""
    alert_id: str
    parent_email: EmailStr
    response: Optional[str] = None
    action_taken: str  # acknowledged, contacted_teacher, scheduled_talk, sent_message

class ProgressFilterRequest(BaseModel):
    """Request model for progress filtering"""
    subjects: Optional[List[str]] = None
    date_range: Optional[str] = "week"  # week, month, quarter
    include_insights: bool = True
    alert_types: Optional[List[str]] = None

class StudentProgressResponse(BaseModel):
    """Response model for student progress"""
    student_id: str
    student_name: str
    grade: int
    current_streak: int
    total_study_hours: float
    weekly_progress: float
    subjects_studied: List[str]
    favorite_subject: str
    challenging_subject: str
    overall_performance: float
    engagement_level: str
    last_active: str
    achievements_this_week: int
    completion_rate: float
    study_consistency: str

class LearningInsightResponse(BaseModel):
    """Response model for learning insights"""
    insight_id: str
    category: str
    title: str
    description: str
    severity: str
    recommendation: str
    action_items: List[str]
    confidence: float
    detected_at: str
    affects_subjects: List[str]
    estimated_impact: str

class ParentAlertResponse(BaseModel):
    """Response model for parent alerts"""
    alert_id: str
    student_id: str
    alert_type: str
    priority: str
    title: str
    message: str
    details: Dict
    created_at: str
    expires_at: Optional[str]
    action_required: bool
    action_buttons: List[Dict]
    read: bool
    parent_response: Optional[str]

# Create API router
router = APIRouter(prefix="/parent-dashboard", tags=["Parent Dashboard"])

@router.get("/student-progress/{student_id}")
async def get_student_progress(
    student_id: str,
    current_user: Student = Depends(get_current_user)
):
    """Get comprehensive student progress for parent dashboard"""
    try:
        # In production, verify parent-student relationship
        progress = await parent_dashboard_service.get_student_progress(student_id)
        
        return {
            "success": True,
            "message": f"📊 Complete progress report for {progress.student_name}!",
            "data": {
                "student_id": progress.student_id,
                "student_name": progress.student_name,
                "grade": progress.grade,
                "current_streak": progress.current_streak,
                "total_study_hours": progress.total_study_hours,
                "weekly_progress": progress.weekly_progress,
                "subjects_studied": progress.subjects_studied,
                "favorite_subject": progress.favorite_subject,
                "challenging_subject": progress.challenging_subject,
                "overall_performance": progress.overall_performance,
                "engagement_level": progress.engagement_level,
                "last_active": progress.last_active,
                "achievements_this_week": progress.achievements_this_week,
                "completion_rate": progress.completion_rate,
                "study_consistency": progress.study_consistency
            },
            "progress_summary": {
                "status": "excellent" if progress.overall_performance > 80 else "good" if progress.overall_performance > 60 else "needs_attention",
                "key_strengths": [
                    f"Strong performance in {progress.favorite_subject}",
                    f"Maintaining {progress.current_streak}-day learning streak" if progress.current_streak > 0 else "Ready to start new learning streak",
                    f"{progress.engagement_level.title()} engagement level"
                ],
                "areas_for_improvement": [
                    f"Additional support needed in {progress.challenging_subject}",
                    "Maintain consistent daily study routine" if progress.study_consistency != "excellent" else "Keep up excellent study habits"
                ],
                "parent_tips": [
                    f"Celebrate their {progress.achievements_this_week} achievements this week!",
                    f"Encourage continued learning in {progress.favorite_subject}",
                    "Regular check-ins help maintain motivation"
                ]
            }
        }
        
    except AgentException as e:
        logger.error(f"Error getting student progress: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error getting student progress: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during progress retrieval"
        )

@router.get("/learning-insights/{student_id}")
async def get_learning_insights(
    student_id: str,
    limit: int = Query(10, description="Maximum number of insights to return"),
    current_user: Student = Depends(get_current_user)
):
    """Get learning insights and recommendations for parents"""
    try:
        insights = await parent_dashboard_service.get_learning_insights(student_id, limit)
        
        insights_data = []
        for insight in insights:
            insights_data.append({
                "insight_id": insight.insight_id,
                "category": insight.category,
                "title": insight.title,
                "description": insight.description,
                "severity": insight.severity,
                "recommendation": insight.recommendation,
                "action_items": insight.action_items,
                "confidence": insight.confidence,
                "detected_at": insight.detected_at,
                "affects_subjects": insight.affects_subjects,
                "estimated_impact": insight.estimated_impact
            })
        
        return {
            "success": True,
            "message": f"💡 {len(insights)} learning insights generated for parent guidance!",
            "data": insights_data,
            "insights_summary": {
                "total_insights": len(insights),
                "high_priority": len([i for i in insights if i.severity == "high"]),
                "categories": list(set(i.category for i in insights)),
                "actionable_recommendations": len([i for i in insights if i.action_items]),
                "overall_confidence": sum(i.confidence for i in insights) / len(insights) if insights else 0
            },
            "parent_guidance": {
                "how_to_use": [
                    "Review insights regularly to understand learning patterns",
                    "Focus on high-priority items first",
                    "Use action items as conversation starters with your child",
                    "Celebrate improvements and progress"
                ],
                "recommended_actions": [
                    "Discuss insights with your child in a supportive manner",
                    "Implement suggested action items gradually",
                    "Monitor changes in learning behavior",
                    "Contact teachers for additional support if needed"
                ]
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting learning insights: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during insights generation"
        )

@router.get("/weekly-report/{student_id}")
async def get_weekly_report(
    student_id: str,
    week_offset: int = Query(0, description="Week offset (0=current, -1=last week, etc.)"),
    current_user: Student = Depends(get_current_user)
):
    """Generate comprehensive weekly report for parents"""
    try:
        report = await parent_dashboard_service.generate_weekly_report(student_id, week_offset)
        
        # Format performance trends
        trends_data = []
        for trend in report.performance_trends:
            trends_data.append({
                "subject": trend.subject,
                "current_score": trend.current_score,
                "previous_score": trend.previous_score,
                "trend": trend.trend,
                "trend_percentage": trend.trend_percentage,
                "confidence": trend.confidence,
                "time_period": trend.time_period,
                "sessions_analyzed": trend.sessions_analyzed,
                "recommendation": trend.recommendation
            })
        
        # Format key insights
        insights_data = []
        for insight in report.key_insights:
            insights_data.append({
                "insight_id": insight.insight_id,
                "category": insight.category,
                "title": insight.title,
                "description": insight.description,
                "severity": insight.severity,
                "recommendation": insight.recommendation,
                "action_items": insight.action_items
            })
        
        return {
            "success": True,
            "message": f"📈 Comprehensive weekly report generated for {report.week_start} to {report.week_end}!",
            "data": {
                "report_id": report.report_id,
                "student_id": report.student_id,
                "week_period": {
                    "start": report.week_start,
                    "end": report.week_end,
                    "description": "This week" if week_offset == 0 else f"{abs(week_offset)} week{'s' if abs(week_offset) > 1 else ''} ago"
                },
                "summary_metrics": {
                    "total_study_time": report.total_study_time,
                    "sessions_completed": report.sessions_completed,
                    "subjects_covered": report.subjects_covered,
                    "achievements_earned": report.achievements_earned,
                    "overall_progress": report.overall_progress
                },
                "performance_trends": trends_data,
                "key_insights": insights_data,
                "recommendations": report.recommendations,
                "companion_summary": report.companion_summary,
                "parent_action_items": report.parent_action_items
            },
            "report_highlights": {
                "strongest_subject": trends_data[0]["subject"] if trends_data else "General Learning",
                "improvement_areas": [t["subject"] for t in trends_data if t["trend"] == "declining"],
                "week_rating": "excellent" if report.overall_progress > 80 else "good" if report.overall_progress > 60 else "needs_attention",
                "next_week_focus": report.recommendations[0] if report.recommendations else "Continue current learning trajectory"
            }
        }
        
    except AgentException as e:
        logger.error(f"Error generating weekly report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error generating weekly report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during report generation"
        )

@router.get("/alerts")
async def get_parent_alerts(
    parent_email: str = Query(..., description="Parent email address"),
    limit: int = Query(20, description="Maximum number of alerts to return"),
    priority_filter: Optional[str] = Query(None, description="Filter by priority: low, medium, high, urgent"),
    current_user: Student = Depends(get_current_user)
):
    """Get alerts for a parent"""
    try:
        alerts = await parent_dashboard_service.get_parent_alerts(parent_email, limit)
        
        # Apply priority filter if specified
        if priority_filter:
            alerts = [alert for alert in alerts if alert.priority == priority_filter]
        
        alerts_data = []
        for alert in alerts:
            alerts_data.append({
                "alert_id": alert.alert_id,
                "student_id": alert.student_id,
                "alert_type": alert.alert_type,
                "priority": alert.priority,
                "title": alert.title,
                "message": alert.message,
                "details": alert.details,
                "created_at": alert.created_at,
                "expires_at": alert.expires_at,
                "action_required": alert.action_required,
                "action_buttons": alert.action_buttons,
                "read": alert.read,
                "parent_response": alert.parent_response
            })
        
        return {
            "success": True,
            "message": f"📬 {len(alerts)} parent alerts retrieved!",
            "data": alerts_data,
            "alerts_summary": {
                "total_alerts": len(alerts),
                "unread_alerts": len([a for a in alerts if not a.read]),
                "urgent_alerts": len([a for a in alerts if a.priority == "urgent"]),
                "action_required": len([a for a in alerts if a.action_required and not a.read]),
                "alert_types": list(set(a.alert_type for a in alerts)),
                "priority_breakdown": {
                    "urgent": len([a for a in alerts if a.priority == "urgent"]),
                    "high": len([a for a in alerts if a.priority == "high"]),
                    "medium": len([a for a in alerts if a.priority == "medium"]),
                    "low": len([a for a in alerts if a.priority == "low"])
                }
            },
            "parent_guidance": {
                "priority_actions": [
                    "Address urgent alerts immediately",
                    "Review high-priority concerns within 24 hours",
                    "Acknowledge achievement alerts to encourage your child",
                    "Use action buttons for quick responses"
                ]
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting parent alerts: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during alerts retrieval"
        )

@router.post("/alerts/mark-read")
async def mark_alert_read(
    request: AlertResponseRequest,
    current_user: Student = Depends(get_current_user)
):
    """Mark an alert as read with optional parent response"""
    try:
        success = await parent_dashboard_service.mark_alert_read(
            parent_email=request.parent_email,
            alert_id=request.alert_id,
            response=request.response
        )
        
        if success:
            return {
                "success": True,
                "message": "✅ Alert marked as read successfully!",
                "data": {
                    "alert_id": request.alert_id,
                    "action_taken": request.action_taken,
                    "response_recorded": request.response is not None,
                    "parent_email": request.parent_email
                },
                "next_steps": {
                    "continue_monitoring": "Keep tracking your child's progress",
                    "follow_up": "Monitor for any changes or improvements",
                    "communication": "Consider discussing with your child if action was taken"
                }
            }
        else:
            return {
                "success": False,
                "message": "Alert not found or already processed",
                "error": "Alert not found"
            }
        
    except Exception as e:
        logger.error(f"Error marking alert as read: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during alert update"
        )

@router.post("/send-message")
async def send_message_to_student(
    request: ParentMessageRequest,
    current_user: Student = Depends(get_current_user)
):
    """Send message from parent to student"""
    try:
        result = await parent_dashboard_service.send_message_to_student(
            student_id=request.student_id,
            parent_email=request.parent_email,
            message=request.message
        )
        
        if result["success"]:
            return {
                "success": True,
                "message": f"💌 Message sent to student successfully!",
                "data": {
                    "message_id": result["message_id"],
                    "student_id": request.student_id,
                    "message_type": request.message_type,
                    "parent_email": request.parent_email,
                    "sent_at": "now"
                },
                "delivery_info": {
                    "status": "delivered",
                    "notification_sent": True,
                    "will_appear_in": ["Student notifications", "Learning companion messages"],
                    "estimated_read_time": "Within next study session"
                }
            }
        else:
            return {
                "success": False,
                "message": "Failed to send message",
                "error": result.get("error", "Unknown error")
            }
        
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during message sending"
        )

@router.get("/communication-history/{student_id}")
async def get_communication_history(
    student_id: str,
    limit: int = Query(50, description="Maximum number of messages to return"),
    current_user: Student = Depends(get_current_user)
):
    """Get communication history for a student"""
    try:
        messages = await parent_dashboard_service.get_communication_history(student_id, limit)
        
        return {
            "success": True,
            "message": f"💬 {len(messages)} communication messages retrieved!",
            "data": messages,
            "communication_summary": {
                "total_messages": len(messages),
                "recent_messages": len([m for m in messages if (datetime.now() - datetime.fromisoformat(m["timestamp"])).days <= 7]),
                "message_types": list(set(m.get("type", "unknown") for m in messages)),
                "unread_messages": len([m for m in messages if not m.get("read", True)]),
                "last_communication": messages[0]["timestamp"] if messages else None
            },
            "communication_tips": [
                "Regular communication helps maintain motivation",
                "Acknowledge your child's efforts and achievements",
                "Use encouraging language to support learning",
                "Ask open-ended questions about their learning experience"
            ]
        }
        
    except Exception as e:
        logger.error(f"Error getting communication history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during communication history retrieval"
        )

@router.get("/dashboard-summary/{student_id}")
async def get_parent_dashboard_summary(
    student_id: str,
    current_user: Student = Depends(get_current_user)
):
    """Get comprehensive parent dashboard summary"""
    try:
        # Get all dashboard components
        progress = await parent_dashboard_service.get_student_progress(student_id)
        insights = await parent_dashboard_service.get_learning_insights(student_id, limit=3)
        parent_email = f"parent_{student_id}@example.com"  # Mock parent email
        alerts = await parent_dashboard_service.get_parent_alerts(parent_email, limit=5)
        
        return {
            "success": True,
            "message": f"📊 Complete parent dashboard summary for {progress.student_name}!",
            "data": {
                "student_overview": {
                    "name": progress.student_name,
                    "grade": progress.grade,
                    "overall_status": "excellent" if progress.overall_performance > 80 else "good" if progress.overall_performance > 60 else "needs_attention",
                    "current_streak": progress.current_streak,
                    "engagement_level": progress.engagement_level,
                    "weekly_progress": progress.weekly_progress
                },
                "quick_stats": {
                    "study_hours_this_week": progress.total_study_hours,
                    "achievements_earned": progress.achievements_this_week,
                    "completion_rate": f"{progress.completion_rate:.1%}",
                    "favorite_subject": progress.favorite_subject,
                    "subjects_studied": len(progress.subjects_studied)
                },
                "alerts_summary": {
                    "total_alerts": len(alerts),
                    "unread_alerts": len([a for a in alerts if not a.read]),
                    "urgent_alerts": len([a for a in alerts if a.priority == "urgent"]),
                    "recent_alerts": [
                        {
                            "title": alert.title,
                            "type": alert.alert_type,
                            "priority": alert.priority,
                            "created_at": alert.created_at
                        } for alert in alerts[:3]
                    ]
                },
                "key_insights": [
                    {
                        "title": insight.title,
                        "category": insight.category,
                        "severity": insight.severity,
                        "recommendation": insight.recommendation
                    } for insight in insights
                ],
                "recommended_actions": [
                    f"Review {progress.student_name}'s progress in {progress.challenging_subject}",
                    f"Celebrate their achievements in {progress.favorite_subject}",
                    "Check and respond to any urgent alerts",
                    "Send an encouraging message to maintain motivation"
                ]
            },
            "dashboard_health": {
                "monitoring_active": True,
                "last_updated": progress.last_active,
                "data_freshness": "real-time",
                "alert_system": "active",
                "communication_channel": "open"
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting dashboard summary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during dashboard summary generation"
        )