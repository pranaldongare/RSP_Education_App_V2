"""
Enhanced Analytics API - RSP Education Agent V2 Phase 1.2
REST API endpoints for Advanced Statistics Dashboard with real-time analytics and predictions
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from pydantic import BaseModel
import logging

from database.database import get_db
from api.v1.auth import get_current_user
from database.models import Student
from services.enhanced_analytics_service import enhanced_analytics_service
from core.exceptions import AgentException

logger = logging.getLogger(__name__)

# Pydantic models for API requests/responses
class SessionTrackingRequest(BaseModel):
    """Request model for tracking learning session data"""
    subject: str
    duration_minutes: int
    questions_answered: int = 0
    correct_answers: int = 0
    performance_score: float = 0.5
    engagement_score: float = 0.5
    difficulty_level: str = "moderate"
    completed: bool = True
    activities: List[Dict] = []
    break_count: int = 0
    first_break_at: int = 0
    interactions: int = 0
    active_minutes: Optional[int] = None

class DashboardResponse(BaseModel):
    """Response model for dashboard data"""
    learning_velocity: float
    engagement_score: float
    subject_breakdown: Dict[str, float]
    time_distribution: Dict[str, int]
    achievement_progress: Dict[str, float]
    recommended_actions: List[str]
    total_study_time: int
    streak_days: int
    completion_rate: float
    focus_score: float

class LearningPatternsResponse(BaseModel):
    """Response model for learning patterns"""
    peak_learning_hours: List[int]
    preferred_subjects: List[str]
    learning_style_indicators: Dict[str, float]
    attention_span_average: int
    difficulty_preference: str
    session_frequency: str
    optimal_session_length: int
    break_patterns: Dict[str, int]
    performance_trends: Dict[str, List[float]]

class PerformancePredictionResponse(BaseModel):
    """Response model for performance predictions"""
    next_session_score: float
    confidence_level: float
    recommended_difficulty: str
    optimal_study_time: str
    subjects_to_focus: List[str]
    predicted_completion_time: int
    success_probability: float
    intervention_needed: bool

class LearningInsightResponse(BaseModel):
    """Response model for learning insights"""
    insight_type: str
    title: str
    description: str
    confidence: float
    actionable_steps: List[str]
    priority: str
    category: str

# Create API router
router = APIRouter(prefix="/enhanced-analytics", tags=["Enhanced Analytics Dashboard"])

@router.get("/dashboard")
async def get_real_time_dashboard(
    current_user: Student = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive real-time dashboard data"""
    try:
        dashboard_data = await enhanced_analytics_service.generate_real_time_dashboard(
            student_id=current_user.student_id,
            db=db
        )
        
        return {
            "success": True,
            "message": f"📊 Real-time dashboard generated for {current_user.name}!",
            "data": {
                "learning_velocity": dashboard_data.learning_velocity,
                "engagement_score": dashboard_data.engagement_score,
                "subject_breakdown": dashboard_data.subject_breakdown,
                "time_distribution": dashboard_data.time_distribution,
                "achievement_progress": dashboard_data.achievement_progress,
                "recommended_actions": dashboard_data.recommended_actions,
                "total_study_time": dashboard_data.total_study_time,
                "streak_days": dashboard_data.streak_days,
                "completion_rate": dashboard_data.completion_rate,
                "focus_score": dashboard_data.focus_score
            },
            "user_context": {
                "student_id": current_user.student_id,
                "name": current_user.name,
                "grade": current_user.grade
            }
        }
        
    except AgentException as e:
        logger.error(f"Agent exception in dashboard generation: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to generate dashboard: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error in dashboard generation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during dashboard generation"
        )

@router.get("/learning-patterns")
async def get_learning_patterns(
    current_user: Student = Depends(get_current_user)
):
    """Get comprehensive learning pattern analysis"""
    try:
        patterns = await enhanced_analytics_service.track_learning_patterns(
            student_id=current_user.student_id
        )
        
        return {
            "success": True,
            "message": f"🧠 Learning patterns analyzed for {current_user.name}!",
            "data": {
                "peak_learning_hours": patterns.peak_learning_hours,
                "preferred_subjects": patterns.preferred_subjects,
                "learning_style_indicators": patterns.learning_style_indicators,
                "attention_span_average": patterns.attention_span_average,
                "difficulty_preference": patterns.difficulty_preference,
                "session_frequency": patterns.session_frequency,
                "optimal_session_length": patterns.optimal_session_length,
                "break_patterns": patterns.break_patterns,
                "performance_trends": patterns.performance_trends
            },
            "user_context": {
                "student_id": current_user.student_id,
                "name": current_user.name,
                "grade": current_user.grade
            }
        }
        
    except AgentException as e:
        logger.error(f"Agent exception in pattern analysis: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to analyze patterns: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error in pattern analysis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during pattern analysis"
        )

@router.get("/performance-prediction")
async def get_performance_prediction(
    current_user: Student = Depends(get_current_user)
):
    """Get AI-powered performance predictions"""
    try:
        predictions = await enhanced_analytics_service.predict_performance(
            student_id=current_user.student_id
        )
        
        return {
            "success": True,
            "message": f"🔮 Performance predictions generated for {current_user.name}!",
            "data": {
                "next_session_score": predictions.next_session_score,
                "confidence_level": predictions.confidence_level,
                "recommended_difficulty": predictions.recommended_difficulty,
                "optimal_study_time": predictions.optimal_study_time,
                "subjects_to_focus": predictions.subjects_to_focus,
                "predicted_completion_time": predictions.predicted_completion_time,
                "success_probability": predictions.success_probability,
                "intervention_needed": predictions.intervention_needed
            },
            "user_context": {
                "student_id": current_user.student_id,
                "name": current_user.name,
                "grade": current_user.grade
            }
        }
        
    except AgentException as e:
        logger.error(f"Agent exception in performance prediction: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to predict performance: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error in performance prediction: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during performance prediction"
        )

@router.get("/insights")
async def get_learning_insights(
    current_user: Student = Depends(get_current_user)
):
    """Get actionable learning insights with AI recommendations"""
    try:
        insights = await enhanced_analytics_service.generate_insights(
            student_id=current_user.student_id
        )
        
        insights_data = []
        for insight in insights:
            insights_data.append({
                "insight_type": insight.insight_type,
                "title": insight.title,
                "description": insight.description,
                "confidence": insight.confidence,
                "actionable_steps": insight.actionable_steps,
                "priority": insight.priority,
                "category": insight.category
            })
        
        return {
            "success": True,
            "message": f"💡 {len(insights)} learning insights generated for {current_user.name}!",
            "data": insights_data,
            "user_context": {
                "student_id": current_user.student_id,
                "name": current_user.name,
                "grade": current_user.grade
            }
        }
        
    except Exception as e:
        logger.error(f"Error generating insights: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during insight generation"
        )

@router.post("/track-session")
async def track_learning_session(
    request: SessionTrackingRequest,
    current_user: Student = Depends(get_current_user)
):
    """Track learning session data for analytics"""
    try:
        # Prepare session data
        session_data = {
            "subject": request.subject,
            "duration_minutes": request.duration_minutes,
            "questions_answered": request.questions_answered,
            "correct_answers": request.correct_answers,
            "performance_score": request.performance_score,
            "engagement_score": request.engagement_score,
            "difficulty_level": request.difficulty_level,
            "completed": request.completed,
            "activities": request.activities,
            "break_count": request.break_count,
            "first_break_at": request.first_break_at,
            "interactions": request.interactions,
            "active_minutes": request.active_minutes or request.duration_minutes,
            "timestamp": None  # Will be set by service
        }
        
        # Track session data
        enhanced_analytics_service.track_session_data(
            student_id=current_user.student_id,
            session_data=session_data
        )
        
        return {
            "success": True,
            "message": f"📈 Session data tracked successfully for {current_user.name}!",
            "session_summary": {
                "subject": request.subject,
                "duration": f"{request.duration_minutes} minutes",
                "performance": f"{request.performance_score:.1%}",
                "questions_answered": request.questions_answered,
                "completed": request.completed
            }
        }
        
    except Exception as e:
        logger.error(f"Error tracking session data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during session tracking"
        )

@router.get("/summary")
async def get_analytics_summary(
    current_user: Student = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive analytics summary combining all features"""
    try:
        # Get all analytics data
        dashboard_data = await enhanced_analytics_service.generate_real_time_dashboard(
            student_id=current_user.student_id,
            db=db
        )
        
        patterns = await enhanced_analytics_service.track_learning_patterns(
            student_id=current_user.student_id
        )
        
        predictions = await enhanced_analytics_service.predict_performance(
            student_id=current_user.student_id
        )
        
        insights = await enhanced_analytics_service.generate_insights(
            student_id=current_user.student_id
        )
        
        # Create comprehensive summary
        summary = {
            "dashboard": {
                "learning_velocity": dashboard_data.learning_velocity,
                "engagement_score": dashboard_data.engagement_score,
                "total_study_time": dashboard_data.total_study_time,
                "streak_days": dashboard_data.streak_days,
                "completion_rate": dashboard_data.completion_rate,
                "focus_score": dashboard_data.focus_score
            },
            "patterns": {
                "peak_learning_hours": patterns.peak_learning_hours,
                "preferred_subjects": patterns.preferred_subjects[:3],  # Top 3
                "attention_span_average": patterns.attention_span_average,
                "difficulty_preference": patterns.difficulty_preference,
                "optimal_session_length": patterns.optimal_session_length
            },
            "predictions": {
                "next_session_score": predictions.next_session_score,
                "confidence_level": predictions.confidence_level,
                "optimal_study_time": predictions.optimal_study_time,
                "success_probability": predictions.success_probability,
                "intervention_needed": predictions.intervention_needed
            },
            "top_insights": [
                {
                    "title": insight.title,
                    "priority": insight.priority,
                    "category": insight.category,
                    "actionable_steps": insight.actionable_steps[:2]  # Top 2 steps
                }
                for insight in insights[:3]  # Top 3 insights
            ],
            "recommendations": dashboard_data.recommended_actions[:3]  # Top 3 recommendations
        }
        
        return {
            "success": True,
            "message": f"📊 Complete analytics summary for {current_user.name}!",
            "data": summary,
            "user_context": {
                "student_id": current_user.student_id,
                "name": current_user.name,
                "grade": current_user.grade
            }
        }
        
    except Exception as e:
        logger.error(f"Error generating analytics summary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during summary generation"
        )

@router.get("/learning-velocity")
async def get_learning_velocity(
    timeframe: str = "week",  # week, month, all
    current_user: Student = Depends(get_current_user)
):
    """Get detailed learning velocity analytics"""
    try:
        dashboard_data = await enhanced_analytics_service.generate_real_time_dashboard(
            student_id=current_user.student_id,
            db=None
        )
        
        # Get session data for velocity calculation
        sessions = enhanced_analytics_service.learning_sessions.get(current_user.student_id, [])
        
        # Filter by timeframe
        from datetime import datetime, timedelta
        now = datetime.now()
        
        if timeframe == "week":
            cutoff = now - timedelta(days=7)
        elif timeframe == "month":
            cutoff = now - timedelta(days=30)
        else:
            cutoff = datetime.min
        
        filtered_sessions = []
        for session in sessions:
            timestamp = session.get('timestamp')
            if timestamp:
                try:
                    session_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    if session_time >= cutoff:
                        filtered_sessions.append(session)
                except:
                    continue
        
        # Calculate velocity metrics
        total_questions = sum(session.get('questions_answered', 0) for session in filtered_sessions)
        total_time = sum(session.get('duration_minutes', 0) for session in filtered_sessions)
        velocity = total_questions / max(total_time, 1)
        
        # Calculate daily averages
        days_in_period = (now - cutoff).days if timeframe != "all" else 30
        questions_per_day = total_questions / max(days_in_period, 1)
        minutes_per_day = total_time / max(days_in_period, 1)
        
        return {
            "success": True,
            "message": f"⚡ Learning velocity analytics for {timeframe} period!",
            "data": {
                "current_velocity": dashboard_data.learning_velocity,
                "period_velocity": velocity,
                "total_questions": total_questions,
                "total_time_minutes": total_time,
                "questions_per_day": questions_per_day,
                "minutes_per_day": minutes_per_day,
                "sessions_analyzed": len(filtered_sessions),
                "timeframe": timeframe
            }
        }
        
    except Exception as e:
        logger.error(f"Error calculating learning velocity: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during velocity calculation"
        )

@router.get("/engagement-heatmap")
async def get_engagement_heatmap(
    current_user: Student = Depends(get_current_user)
):
    """Get engagement heatmap data by hour and day"""
    try:
        sessions = enhanced_analytics_service.learning_sessions.get(current_user.student_id, [])
        
        # Initialize heatmap data
        heatmap = {}
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        for day in days:
            heatmap[day] = {}
            for hour in range(24):
                heatmap[day][hour] = 0.0
        
        # Process sessions
        for session in sessions:
            timestamp = session.get('timestamp')
            engagement = session.get('engagement_score', 0.5)
            
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    day_name = dt.strftime('%A')
                    hour = dt.hour
                    
                    # Update heatmap with engagement score
                    if day_name in heatmap:
                        current_value = heatmap[day_name][hour]
                        # Average with existing value if any
                        if current_value > 0:
                            heatmap[day_name][hour] = (current_value + engagement) / 2
                        else:
                            heatmap[day_name][hour] = engagement
                except:
                    continue
        
        return {
            "success": True,
            "message": f"🔥 Engagement heatmap generated for {current_user.name}!",
            "data": {
                "heatmap": heatmap,
                "max_engagement": max(
                    max(day_data.values()) for day_data in heatmap.values()
                ),
                "peak_day": max(
                    heatmap.keys(), 
                    key=lambda day: max(heatmap[day].values())
                ),
                "peak_hour": max(
                    range(24),
                    key=lambda hour: max(heatmap[day][hour] for day in days)
                )
            }
        }
        
    except Exception as e:
        logger.error(f"Error generating engagement heatmap: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during heatmap generation"
        )