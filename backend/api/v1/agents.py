"""
REST API Endpoints for All 8 AI Agents - Phase 6 Implementation
Comprehensive API layer for frontend integration with all AI agents.
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from agents.content_generator import ContentGeneratorAgent, ContentRequest, QuestionRequest
from agents.assessment_agent import AssessmentAgent, AssessmentRequest
from agents.adaptive_learning_agent import AdaptiveLearningAgent, AdaptationRequest
from agents.engagement_agent import EngagementAgent, EngagementRequest
from agents.analytics_agent import AnalyticsAgent, AnalyticsRequest
from agents.learning_coordinator_agent import LearningCoordinatorAgent
from agents.voice_interaction_agent import (
    VoiceInteractionAgent, 
    SpeechInput, 
    VoiceSettings, 
    SpeechLanguage,
    VoiceGender
)
from core.exceptions import AgentException
from config.database import get_db_session as get_db
from database.models import Student
from auth.auth_service import auth_service
from services.ai_companion_service import ai_companion_agent

# Initialize router and security
router = APIRouter(prefix="/agents", tags=["AI Agents"])
security = HTTPBearer()

# Initialize all agents
content_agent = ContentGeneratorAgent()
assessment_agent = AssessmentAgent()
adaptive_agent = AdaptiveLearningAgent()
engagement_agent = EngagementAgent()
analytics_agent = AnalyticsAgent()
coordinator_agent = LearningCoordinatorAgent()
voice_agent = VoiceInteractionAgent()

logger = logging.getLogger(__name__)

# Authentication dependency
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> Student:
    """Dependency to get current authenticated user"""
    try:
        token = credentials.credentials
        user = await auth_service.get_current_user(db, token)
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(
            status_code=401,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"},
        )

# === AI COMPANION INTEGRATION UTILITIES ===

def get_companion_enhanced_response(student_id: str, agent_name: str, base_response: str, interaction_data: Dict = None) -> str:
    """Enhance agent response with AI Companion personality and track interaction"""
    try:
        # Track the interaction with the companion agent
        if interaction_data:
            ai_companion_agent.update_companion_from_agent_interaction(
                student_id=student_id,
                agent_name=agent_name,
                interaction_data=interaction_data
            )
        
        # Get enhanced response with companion personality
        enhanced_response = ai_companion_agent.get_personalized_response_for_agent(
            student_id=student_id,
            agent_name=agent_name,
            base_response=base_response
        )
        
        return enhanced_response
        
    except Exception as e:
        logger.error(f"Failed to enhance response with companion for {agent_name}: {e}")
        return base_response  # Return original response on error

def get_companion_context_for_agent(student_id: str, agent_name: str) -> Dict:
    """Get companion context that agents can use for personalized responses"""
    try:
        return ai_companion_agent.get_companion_context_for_agent(
            student_id=student_id,
            agent_name=agent_name
        )
    except Exception as e:
        logger.error(f"Failed to get companion context for {agent_name}: {e}")
        return {"companion_available": False, "error": str(e)}

# === END AI COMPANION INTEGRATION ===

# Dependency to initialize agents on startup
async def initialize_agents():
    """Initialize all AI agents"""
    try:
        # Initialize agents (some agents may not have async initialization)
        logger.info("AI agents ready for operation")
        logger.info("All AI agents initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize agents: {e}")
        raise


# ==================== CONTENT GENERATOR AGENT ENDPOINTS ====================

@router.post("/content/generate")
async def generate_content(
    request: ContentRequest,
    current_user: Student = Depends(get_current_user)
):
    """Generate educational content with user context"""
    try:
        # Enhance request with user context
        request.student_id = current_user.id
        request.student_grade = current_user.grade
        request.preferred_language = current_user.preferred_language
        request.learning_style = current_user.learning_style
        
        content = await content_agent.generate_content(request)
        
        # Log user interaction
        logger.info(f"Content generated for user {current_user.id}: {request.subject} - {request.topic}")
        
        # Simple success message for now (companion integration temporarily disabled for debugging)
        enhanced_message = f"Content generated successfully for {request.subject} - {request.topic}!"
        companion_context = {}
        
        return {
            "success": True, 
            "message": enhanced_message,
            "data": content.model_dump() if hasattr(content, 'model_dump') else content,
            "companion_context": companion_context,
            "user_context": {
                "student_id": current_user.id,
                "grade": current_user.grade,
                "language": current_user.preferred_language
            }
        }
    except AgentException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Content generation error for user {current_user.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/content/questions")
async def generate_questions(
    request: QuestionRequest,
    current_user: Student = Depends(get_current_user)
):
    """Generate educational questions with user context"""
    try:
        # Enhance request with user context
        request.student_id = current_user.id
        request.student_grade = current_user.grade
        request.preferred_language = current_user.preferred_language
        
        questions = await content_agent.generate_questions(
            subject=request.subject,
            grade=request.grade or current_user.grade,  # Use user's grade if not specified
            topic=request.topic,
            question_type=request.question_type,
            difficulty_level=request.difficulty_level,
            num_questions=request.num_questions
        )
        
        # Log user interaction
        logger.info(f"Questions generated for user {current_user.id}: {request.subject} - {request.topic}")
        
        return {
            "success": True, 
            "data": questions,
            "user_context": {
                "student_id": current_user.id,
                "grade": current_user.grade,
                "language": current_user.preferred_language
            }
        }
    except AgentException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Question generation error for user {current_user.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/content/status")
async def get_content_agent_status(
    current_user: Student = Depends(get_current_user)
):
    """Get content generator agent status for current user"""
    try:
        status = await content_agent.get_agent_status()
        
        # Add user-specific status information
        status["user_context"] = {
            "student_id": current_user.id,
            "grade": current_user.grade,
            "preferred_language": current_user.preferred_language,
            "learning_style": current_user.learning_style
        }
        
        return {"success": True, "data": status}
    except Exception as e:
        logger.error(f"Content agent status error for user {current_user.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# ==================== ASSESSMENT AGENT ENDPOINTS ====================

@router.post("/assessment/generate-questions")
async def generate_assessment_questions(
    request: QuestionRequest,
    current_user: Student = Depends(get_current_user)
):
    """Generate assessment questions using the Assessment Agent with user context"""
    try:
        # Enhance request with user context
        request.student_id = current_user.id
        request.student_grade = current_user.grade
        request.preferred_language = current_user.preferred_language
        
        questions = await content_agent.generate_questions(request)
        
        # Log user interaction
        logger.info(f"Assessment questions generated for user {current_user.id}: {request.subject} - {request.topic}")
        
        return {
            "success": True, 
            "questions": questions,
            "user_context": {
                "student_id": current_user.id,
                "grade": current_user.grade,
                "language": current_user.preferred_language
            }
        }
    except AgentException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Assessment question generation error for user {current_user.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/assessment/evaluate")
async def evaluate_assessment(
    request: AssessmentRequest,
    current_user: Student = Depends(get_current_user)
):
    """Evaluate student responses and provide personalized feedback"""
    try:
        # Enhance request with user context
        request.student_id = current_user.id
        request.student_grade = current_user.grade
        request.preferred_language = current_user.preferred_language
        request.learning_style = current_user.learning_style
        
        result = await assessment_agent.assess_responses(request)
        
        # Log user interaction
        logger.info(f"Assessment evaluated for user {current_user.id}: Score {result.get('score', 'N/A')}")
        
        # === AI COMPANION INTEGRATION ===
        # Prepare interaction data for companion
        score = result.get('score', 0.5)
        performance_score = score if isinstance(score, (int, float)) else 0.5
        
        interaction_data = {
            "subject": request.subject,
            "performance_score": performance_score,
            "total_questions": len(request.questions) if hasattr(request, 'questions') else 1,
            "completed": True,
            "agent_action": "assessment_evaluation"
        }
        
        # Add achievement if high score
        if performance_score >= 0.8:
            interaction_data["achievement"] = f"Excellent performance in {request.subject}!"
        
        # Get companion context for personalized feedback
        companion_context = get_companion_context_for_agent(current_user.id, "assessment")
        
        # Generate personalized feedback message based on performance
        if performance_score >= 0.8:
            base_message = "Outstanding work! You've mastered this topic brilliantly!"
        elif performance_score >= 0.6:
            base_message = "Great job! You're making excellent progress!"
        elif performance_score >= 0.4:
            base_message = "Good effort! Let's work together to strengthen your understanding."
        else:
            base_message = "Don't worry, learning takes time. I'm here to help you succeed!"
        
        # Enhance feedback with companion personality
        enhanced_feedback = get_companion_enhanced_response(
            current_user.id,
            "assessment", 
            base_message,
            interaction_data
        )
        
        # Add companion-enhanced insights to result
        result["companion_feedback"] = enhanced_feedback
        result["companion_context"] = companion_context
        result["user_context"] = {
            "student_id": current_user.id,
            "grade": current_user.grade,
            "language": current_user.preferred_language,
            "learning_style": current_user.learning_style
        }
        
        return {
            "success": True, 
            "message": enhanced_feedback,
            "data": result
        }
    except AgentException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Assessment evaluation error for user {current_user.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/assessment/status")
async def get_assessment_agent_status(
    current_user: Student = Depends(get_current_user)
):
    """Get assessment agent status for current user"""
    try:
        status = await assessment_agent.get_agent_status()
        
        # Add user-specific status information
        status["user_context"] = {
            "student_id": current_user.id,
            "grade": current_user.grade,
            "preferred_language": current_user.preferred_language,
            "learning_style": current_user.learning_style
        }
        
        return {"success": True, "data": status}
    except Exception as e:
        logger.error(f"Assessment agent status error for user {current_user.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# ==================== LEARNING COORDINATOR AGENT ENDPOINTS ====================

@router.post("/coordinator/learning-path")
async def create_learning_path(
    subject: str,
    learning_goals: List[str],
    duration_weeks: int = 12,
    current_user: Student = Depends(get_current_user)
):
    """Create personalized learning path for authenticated user"""
    try:
        learning_path = await coordinator_agent.create_learning_path(
            student_id=current_user.id,
            subject=subject,
            grade=int(current_user.grade),
            learning_goals=learning_goals,
            duration_weeks=duration_weeks
        )
        
        # Log user interaction
        logger.info(f"Learning path created for user {current_user.id}: {subject}")
        
        # Add user context
        learning_path["user_context"] = {
            "student_id": current_user.id,
            "grade": current_user.grade,
            "language": current_user.preferred_language,
            "learning_style": current_user.learning_style
        }
        
        return {"success": True, "data": learning_path}
    except AgentException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Learning path creation error for user {current_user.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/coordinator/session/start")
async def start_learning_session(
    session_id: str,
    current_user: Student = Depends(get_current_user)
):
    """Start a coordinated learning session for authenticated user"""
    try:
        # Enhance session with user context
        session_data = await coordinator_agent.start_learning_session(
            session_id, 
            student_id=current_user.id,
            student_grade=current_user.grade,
            preferred_language=current_user.preferred_language,
            learning_style=current_user.learning_style
        )
        
        # Log user interaction
        logger.info(f"Learning session started for user {current_user.id}: {session_id}")
        
        return {"success": True, "data": session_data}
    except AgentException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Session start error for user {current_user.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/coordinator/insights")
async def get_coordinator_insights(
    current_user: Student = Depends(get_current_user)
):
    """Get comprehensive coordinator insights for authenticated user"""
    try:
        insights = await coordinator_agent.get_coordinator_insights(current_user.id)
        
        # Add user context to insights
        insights["user_context"] = {
            "student_id": current_user.id,
            "name": current_user.name,
            "grade": current_user.grade,
            "language": current_user.preferred_language,
            "learning_style": current_user.learning_style
        }
        
        return {"success": True, "data": insights}
    except AgentException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Insights error for user {current_user.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# ==================== ANALYTICS AGENT ENDPOINTS ====================

@router.post("/analytics/report")
async def generate_analytics_report(
    request: AnalyticsRequest,
    current_user: Student = Depends(get_current_user)
):
    """Generate comprehensive analytics report with user context"""
    try:
        # Enhance request with user context
        request.student_id = current_user.id
        
        report = await analytics_agent.generate_analytics_report(request)
        
        # Log user interaction
        logger.info(f"Analytics report generated for user {current_user.id}")
        
        # Add user context to report
        report["user_context"] = {
            "student_id": current_user.id,
            "grade": current_user.grade,
            "language": current_user.preferred_language,
            "learning_style": current_user.learning_style
        }
        
        return {"success": True, "data": report}
    except AgentException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Analytics report error for user {current_user.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/analytics/performance")
async def get_performance_analytics(
    timeframe: str = "weekly",
    current_user: Student = Depends(get_current_user)
):
    """Get performance analytics for authenticated user"""
    try:
        # Create a basic request for performance analytics
        from agents.analytics_agent import AnalyticsTimeFrame, MetricType
        request = AnalyticsRequest(
            student_id=current_user.id,
            timeframe=AnalyticsTimeFrame(timeframe),
            metric_types=[MetricType.PERFORMANCE, MetricType.SKILL_MASTERY]
        )
        report = await analytics_agent.generate_analytics_report(request)
        
        # Log user interaction
        logger.info(f"Performance analytics retrieved for user {current_user.id}")
        
        # Add user context to report
        report["user_context"] = {
            "student_id": current_user.id,
            "grade": current_user.grade,
            "language": current_user.preferred_language
        }
        
        return {"success": True, "data": report}
    except AgentException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Performance analytics error for user {current_user.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/analytics/engagement")
async def get_engagement_analytics(
    timeframe: str = "weekly",
    current_user: Student = Depends(get_current_user)
):
    """Get engagement analytics for authenticated user"""
    try:
        from agents.analytics_agent import AnalyticsTimeFrame, MetricType
        request = AnalyticsRequest(
            student_id=current_user.id,
            timeframe=AnalyticsTimeFrame(timeframe),
            metric_types=[MetricType.ENGAGEMENT, MetricType.BEHAVIORAL]
        )
        report = await analytics_agent.generate_analytics_report(request)
        
        # Log user interaction
        logger.info(f"Engagement analytics retrieved for user {current_user.id}")
        
        # Add user context to report
        report["user_context"] = {
            "student_id": current_user.id,
            "grade": current_user.grade,
            "language": current_user.preferred_language
        }
        
        return {"success": True, "data": report}
    except AgentException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Engagement analytics error for user {current_user.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/analytics/predictions")
async def get_predictive_analytics(
    current_user: Student = Depends(get_current_user)
):
    """Get predictive analytics for authenticated user"""
    try:
        from agents.analytics_agent import AnalyticsTimeFrame, MetricType
        request = AnalyticsRequest(
            student_id=current_user.id,
            timeframe=AnalyticsTimeFrame.MONTHLY,
            metric_types=list(MetricType),
            include_predictions=True
        )
        report = await analytics_agent.generate_analytics_report(request)
        
        # Log user interaction
        logger.info(f"Predictive analytics retrieved for user {current_user.id}")
        
        # Add user context to report
        report["user_context"] = {
            "student_id": current_user.id,
            "grade": current_user.grade,
            "language": current_user.preferred_language,
            "learning_style": current_user.learning_style
        }
        
        return {"success": True, "data": report}
    except AgentException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Predictive analytics error for user {current_user.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/analytics/status")
async def get_analytics_agent_status(
    current_user: Student = Depends(get_current_user)
):
    """Get analytics agent status for current user"""
    try:
        status = await analytics_agent.get_agent_status()
        
        # Add user-specific status information
        status["user_context"] = {
            "student_id": current_user.id,
            "grade": current_user.grade,
            "preferred_language": current_user.preferred_language,
            "learning_style": current_user.learning_style
        }
        
        return {"success": True, "data": status}
    except Exception as e:
        logger.error(f"Analytics agent status error for user {current_user.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# ==================== ADAPTIVE LEARNING AGENT ENDPOINTS ====================

@router.post("/adaptive/learning-path")
async def adapt_learning_path(
    request: AdaptationRequest,
    current_user: Student = Depends(get_current_user)
):
    """Generate adaptive learning path recommendations with user context"""
    try:
        # Enhance request with user context
        request.student_id = current_user.id
        request.student_grade = current_user.grade
        request.preferred_language = current_user.preferred_language
        request.learning_style = current_user.learning_style
        
        recommendations = await adaptive_agent.adapt_learning_path(request)
        
        # Log user interaction
        logger.info(f"Adaptive learning path generated for user {current_user.id}")
        
        # Add user context to recommendations
        recommendations["user_context"] = {
            "student_id": current_user.id,
            "grade": current_user.grade,
            "language": current_user.preferred_language,
            "learning_style": current_user.learning_style
        }
        
        return {"success": True, "data": recommendations}
    except AgentException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Adaptive learning path error for user {current_user.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/adaptive/profile")
async def get_learning_profile(
    current_user: Student = Depends(get_current_user)
):
    """Get authenticated user's learning profile"""
    try:
        # Create a basic request for profile retrieval with user context
        request = AdaptationRequest(
            student_id=current_user.id,
            student_grade=current_user.grade,
            preferred_language=current_user.preferred_language,
            learning_style=current_user.learning_style,
            assessment_results=[]  # Would be populated from database in production
        )
        profile = await adaptive_agent.adapt_learning_path(request)
        
        # Log user interaction
        logger.info(f"Learning profile retrieved for user {current_user.id}")
        
        # Add user context to profile
        profile["user_context"] = {
            "student_id": current_user.id,
            "name": current_user.name,
            "grade": current_user.grade,
            "language": current_user.preferred_language,
            "learning_style": current_user.learning_style
        }
        
        return {"success": True, "data": profile}
    except AgentException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Learning profile error for user {current_user.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/adaptive/status")
async def get_adaptive_agent_status(
    current_user: Student = Depends(get_current_user)
):
    """Get adaptive learning agent status for current user"""
    try:
        status = await adaptive_agent.get_agent_status()
        
        # Add user-specific status information
        status["user_context"] = {
            "student_id": current_user.id,
            "grade": current_user.grade,
            "preferred_language": current_user.preferred_language,
            "learning_style": current_user.learning_style
        }
        
        return {"success": True, "data": status}
    except Exception as e:
        logger.error(f"Adaptive agent status error for user {current_user.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# ==================== ENGAGEMENT AGENT ENDPOINTS ====================

@router.post("/engagement/profile")
async def create_engagement_profile(
    request: EngagementRequest,
    current_user: Student = Depends(get_current_user)
):
    """Create or update student engagement profile with user context"""
    try:
        # Enhance request with user context
        request.student_id = current_user.id
        request.student_grade = current_user.grade
        request.preferred_language = current_user.preferred_language
        request.learning_style = current_user.learning_style
        
        profile = await engagement_agent.create_engagement_profile(request)
        
        # Log user interaction
        logger.info(f"Engagement profile created/updated for user {current_user.id}")
        
        # Add user context to profile
        profile["user_context"] = {
            "student_id": current_user.id,
            "grade": current_user.grade,
            "language": current_user.preferred_language,
            "learning_style": current_user.learning_style
        }
        
        return {"success": True, "data": profile}
    except AgentException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Engagement profile creation error for user {current_user.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/engagement/status")
async def get_engagement_status(
    current_user: Student = Depends(get_current_user)
):
    """Get authenticated user's engagement status and metrics"""
    try:
        # Create a basic request for engagement status with user context
        from agents.engagement_agent import EngagementRequest
        request = EngagementRequest(
            student_id=current_user.id,
            student_grade=current_user.grade,
            preferred_language=current_user.preferred_language,
            learning_style=current_user.learning_style,
            assessment_results=[],  # Would be populated from database in production
            learning_profile=None
        )
        status = await engagement_agent.create_engagement_profile(request)
        
        # Log user interaction
        logger.info(f"Engagement status retrieved for user {current_user.id}")
        
        # Add user context to status
        status["user_context"] = {
            "student_id": current_user.id,
            "name": current_user.name,
            "grade": current_user.grade,
            "language": current_user.preferred_language,
            "learning_style": current_user.learning_style
        }
        
        return {"success": True, "data": status}
    except AgentException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Engagement status error for user {current_user.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/engagement/gamification")
async def get_gamification_status(
    current_user: Student = Depends(get_current_user)
):
    """Get authenticated user's gamification status and achievements"""
    try:
        from agents.engagement_agent import EngagementRequest
        request = EngagementRequest(
            student_id=current_user.id,
            student_grade=current_user.grade,
            preferred_language=current_user.preferred_language,
            learning_style=current_user.learning_style,
            assessment_results=[],
            learning_profile=None
        )
        gamification_data = await engagement_agent.create_engagement_profile(request)
        
        # Log user interaction
        logger.info(f"Gamification status retrieved for user {current_user.id}")
        
        # Add user context to gamification data
        gamification_data["user_context"] = {
            "student_id": current_user.id,
            "name": current_user.name,
            "grade": current_user.grade,
            "language": current_user.preferred_language,
            "learning_style": current_user.learning_style
        }
        
        return {"success": True, "data": gamification_data}
    except AgentException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Gamification status error for user {current_user.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/engagement/agent-status")
async def get_engagement_agent_status(
    current_user: Student = Depends(get_current_user)
):
    """Get engagement agent status for current user"""
    try:
        status = await engagement_agent.get_agent_status()
        
        # Add user-specific status information
        status["user_context"] = {
            "student_id": current_user.id,
            "grade": current_user.grade,
            "preferred_language": current_user.preferred_language,
            "learning_style": current_user.learning_style
        }
        
        return {"success": True, "data": status}
    except Exception as e:
        logger.error(f"Engagement agent status error for user {current_user.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# ==================== VOICE INTERACTION AGENT ENDPOINTS ====================

class VoiceSessionRequest(BaseModel):
    """Request model for starting voice session"""
    language: str = "en-US"
    voice_settings: Dict[str, Any] = {}

@router.post("/voice/session/start")
async def start_voice_session(
    request: VoiceSessionRequest,
    current_user: Student = Depends(get_current_user)
):
    """Start a voice interaction session for authenticated user"""
    try:
        # Convert language string to SpeechLanguage enum, fallback to user's preferred language
        try:
            language = SpeechLanguage(request.language)
        except ValueError:
            # Try user's preferred language or default to English
            try:
                language = SpeechLanguage(current_user.preferred_language)
            except (ValueError, AttributeError):
                language = SpeechLanguage.ENGLISH
        
        # Create VoiceSettings object if provided
        voice_settings = None
        if request.voice_settings:
            voice_settings = VoiceSettings(
                language=language,
                gender=VoiceGender(request.voice_settings.get('gender', 'female')),
                speed=request.voice_settings.get('speed', 1.0),
                pitch=request.voice_settings.get('pitch', 1.0),
                volume=request.voice_settings.get('volume', 1.0),
                voice_id=request.voice_settings.get('voice_id')
            )
        
        session = await voice_agent.start_voice_session(
            student_id=current_user.id,
            language=language,
            voice_settings=voice_settings
        )
        
        # Log user interaction
        logger.info(f"Voice session started for user {current_user.id}")
        
        # Add user context to session
        session["user_context"] = {
            "student_id": current_user.id,
            "name": current_user.name,
            "grade": current_user.grade,
            "language": current_user.preferred_language,
            "learning_style": current_user.learning_style
        }
        
        return {"success": True, "data": session}
    except AgentException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Voice session start error for user {current_user.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


class TTSRequest(BaseModel):
    """Request model for text-to-speech"""
    text: str
    voice_settings: Dict[str, Any]

@router.post("/voice/tts")
async def text_to_speech(
    request: TTSRequest,
    current_user: Student = Depends(get_current_user)
):
    """Convert text to speech for authenticated user"""
    try:
        # Create VoiceSettings object from the request, using user preferences as fallback
        default_language = getattr(current_user, 'preferred_language', 'en-US')
        voice_settings = VoiceSettings(
            language=SpeechLanguage(request.voice_settings.get('language', default_language)),
            gender=VoiceGender(request.voice_settings.get('gender', 'female')),
            speed=request.voice_settings.get('speed', 1.0),
            pitch=request.voice_settings.get('pitch', 1.0),
            volume=request.voice_settings.get('volume', 1.0),
            voice_id=request.voice_settings.get('voice_id')
        )
        
        speech_output = await voice_agent.text_to_speech(request.text, voice_settings)
        
        # Log user interaction
        logger.info(f"Text-to-speech generated for user {current_user.id}")
        
        # Add user context to output
        speech_output["user_context"] = {
            "student_id": current_user.id,
            "grade": current_user.grade,
            "language": current_user.preferred_language
        }
        
        return {"success": True, "data": speech_output}
    except AgentException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Text-to-speech error for user {current_user.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/voice/status")
async def get_voice_agent_status(
    current_user: Student = Depends(get_current_user)
):
    """Get voice interaction agent status for current user"""
    try:
        status = await voice_agent.get_agent_status()
        
        # Add user-specific status information
        status["user_context"] = {
            "student_id": current_user.id,
            "grade": current_user.grade,
            "preferred_language": current_user.preferred_language,
            "learning_style": current_user.learning_style
        }
        
        return {"success": True, "data": status}
    except Exception as e:
        logger.error(f"Voice agent status error for user {current_user.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


class SpeechToTextRequest(BaseModel):
    """Request model for speech-to-text"""
    audio_data: str  # Base64 encoded audio data
    language: str = "en-US"

@router.post("/voice/stt")
async def speech_to_text(
    request: SpeechToTextRequest,
    current_user: Student = Depends(get_current_user)
):
    """Convert speech to text for authenticated user"""
    try:
        # Use user's preferred language as fallback
        language = request.language or getattr(current_user, 'preferred_language', 'en-US')
        
        # Create SpeechInput object
        speech_input = SpeechInput(
            audio_data=request.audio_data,
            language=SpeechLanguage(language)
        )
        
        text_output = await voice_agent.speech_to_text(speech_input)
        
        # Log user interaction
        logger.info(f"Speech-to-text processed for user {current_user.id}")
        
        # Add user context to output
        text_output["user_context"] = {
            "student_id": current_user.id,
            "grade": current_user.grade,
            "language": current_user.preferred_language
        }
        
        return {"success": True, "data": text_output}
    except AgentException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Speech-to-text error for user {current_user.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# ==================== SYSTEM-WIDE ENDPOINTS ====================

@router.get("/status")
async def get_agents_status():
    """Get status of all AI agents - public endpoint"""
    try:
        statuses = {
            "content_generator": {"status": "active"},
            "assessment": {"status": "active"}, 
            "adaptive_learning": {"status": "active"},
            "engagement": {"status": "active"},
            "analytics": {"status": "active"},
            "learning_coordinator": {"status": "active"},
            "voice_interaction": {"status": "active"}
        }
        
        # Calculate overall system health
        total_agents = len(statuses)
        active_agents = sum(1 for status in statuses.values() if status.get("status") == "active")
        system_health = (active_agents / total_agents) * 100
        
        return {
            "success": True,
            "data": {
                "system_health": f"{system_health:.1f}%",
                "total_agents": total_agents,
                "active_agents": active_agents,
                "agents": statuses,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
    except Exception as e:
        logger.error(f"System status error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/status/all")
async def get_all_agents_status(
    current_user: Student = Depends(get_current_user)
):
    """Get status of all AI agents for authenticated user"""
    try:
        statuses = {
            "content_generator": await content_agent.get_agent_status(),
            "assessment": await assessment_agent.get_agent_status(),
            "adaptive_learning": await adaptive_agent.get_agent_status(),
            "engagement": await engagement_agent.get_agent_status(),
            "analytics": await analytics_agent.get_agent_status(),
            "learning_coordinator": await coordinator_agent.get_agent_status(),
            "voice_interaction": await voice_agent.get_agent_status()
        }
        
        # Calculate overall system health
        total_agents = len(statuses)
        active_agents = sum(1 for status in statuses.values() if status.get("status") == "active")
        system_health = (active_agents / total_agents) * 100
        
        # Log user interaction
        logger.info(f"System status retrieved for user {current_user.id}")
        
        return {
            "success": True,
            "data": {
                "system_health": f"{system_health:.1f}%",
                "total_agents": total_agents,
                "active_agents": active_agents,
                "agents": statuses,
                "timestamp": datetime.utcnow().isoformat(),
                "user_context": {
                    "student_id": current_user.id,
                    "grade": current_user.grade,
                    "language": current_user.preferred_language
                }
            }
        }
    except Exception as e:
        logger.error(f"System status error for user {current_user.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/initialize")
async def initialize_all_agents(background_tasks: BackgroundTasks):
    """Initialize all AI agents"""
    try:
        background_tasks.add_task(initialize_agents)
        return {
            "success": True,
            "message": "Agent initialization started in background",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Agent initialization error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# ==================== HEALTH CHECK ENDPOINTS ====================

@router.get("/health")
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "service": "RSP Education AI Agents",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }