"""
AI Companion Agent API - RSP Education Agent V2 Phase 1 (8th Agent)
REST API endpoints for the AI Companion Agent with shared memory architecture
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from pydantic import BaseModel
import logging

from database.database import get_db
from api.v1.auth import get_current_user
from database.models import Student
from services.ai_companion_service import ai_companion_agent
from core.exceptions import AgentException

logger = logging.getLogger(__name__)

# Pydantic models for API requests/responses
class CompanionInitializeRequest(BaseModel):
    companion_name: Optional[str] = "Buddy Bear"
    personality_preferences: Optional[List[str]] = None

class InteractionAnalysisRequest(BaseModel):
    performance_score: Optional[float] = 0.5
    time_spent_minutes: Optional[int] = 5
    attempts: Optional[int] = 1
    completed: Optional[bool] = True
    subject: Optional[str] = "general"
    achievement: Optional[str] = None

class ResponseGenerationRequest(BaseModel):
    context: str
    agent_name: Optional[str] = "general"

class InteractionTrackingRequest(BaseModel):
    agent_name: str
    interaction_data: Dict
    subject: Optional[str] = "general"
    performance_score: Optional[float] = None
    achievement: Optional[str] = None

class CompanionContextResponse(BaseModel):
    companion_available: bool
    companion_name: Optional[str] = None
    current_mood: Optional[str] = None
    personality_traits: Optional[List[str]] = None
    interaction_count: Optional[int] = 0
    student_name: Optional[str] = None
    favorite_subjects: Optional[List[str]] = None
    struggle_areas: Optional[List[str]] = None
    recent_achievements: Optional[List[Dict]] = None
    engagement_level: Optional[float] = None
    encouragement_needed: Optional[bool] = False
    celebration_worthy: Optional[bool] = False
    agent_integration: Optional[Dict] = None

# Create API router
router = APIRouter(prefix="/ai-companion", tags=["AI Companion Agent"])

@router.post("/initialize")
async def initialize_companion(
    request: CompanionInitializeRequest,
    current_user: Student = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Initialize AI companion for authenticated student"""
    try:
        companion_profile = await ai_companion_agent.initialize_companion(
            student_id=current_user.student_id,
            db=db
        )
        
        return {
            "success": True,
            "message": f"🐻 Welcome! Your AI companion '{companion_profile.companion_name}' is ready to learn with you!",
            "companion": {
                "name": companion_profile.companion_name,
                "personality_traits": companion_profile.personality_traits,
                "current_mood": companion_profile.current_mood,
                "interaction_count": companion_profile.interaction_count
            }
        }
        
    except AgentException as e:
        logger.error(f"Agent exception in companion initialization: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to initialize companion: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error in companion initialization: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during companion initialization"
        )

@router.post("/analyze-interaction")
async def analyze_interaction(
    request: InteractionAnalysisRequest,
    current_user: Student = Depends(get_current_user)
):
    """Analyze student interaction for mood and engagement detection"""
    try:
        interaction_data = {
            "performance_score": request.performance_score,
            "time_spent_minutes": request.time_spent_minutes,
            "attempts": request.attempts,
            "completed": request.completed,
            "subject": request.subject
        }
        
        analysis = await ai_companion_agent.analyze_interaction(
            student_id=current_user.student_id,
            interaction_data=interaction_data
        )
        
        return {
            "success": True,
            "analysis": {
                "sentiment_score": analysis.sentiment_score,
                "performance_trend": analysis.performance_trend,
                "frustration_indicators": analysis.frustration_indicators,
                "success_indicators": analysis.success_indicators,
                "engagement_level": analysis.engagement_level
            }
        }
        
    except Exception as e:
        logger.error(f"Error in interaction analysis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze interaction"
        )

@router.post("/update-mood")
async def update_companion_mood(
    request: InteractionAnalysisRequest,
    current_user: Student = Depends(get_current_user)
):
    """Update companion mood based on interaction analysis"""
    try:
        # First analyze the interaction
        interaction_data = {
            "performance_score": request.performance_score,
            "time_spent_minutes": request.time_spent_minutes,
            "attempts": request.attempts,
            "completed": request.completed,
            "subject": request.subject
        }
        
        analysis = await ai_companion_agent.analyze_interaction(
            student_id=current_user.student_id,
            interaction_data=interaction_data
        )
        
        # Update mood based on analysis
        mood_state = await ai_companion_agent.update_mood(
            student_id=current_user.student_id,
            interaction_analysis=analysis
        )
        
        return {
            "success": True,
            "message": f"🐻 Companion mood updated based on your learning session!",
            "mood_state": {
                "current_mood": mood_state.current_mood,
                "confidence_level": mood_state.confidence_level,
                "suggested_interaction_style": mood_state.suggested_interaction_style,
                "encouragement_level": mood_state.encouragement_level,
                "factors": mood_state.factors
            }
        }
        
    except AgentException as e:
        logger.error(f"Agent exception in mood update: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update mood: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error in mood update: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update companion mood"
        )

@router.post("/generate-response")
async def generate_personalized_response(
    request: ResponseGenerationRequest,
    current_user: Student = Depends(get_current_user)
):
    """Generate personalized response from AI companion"""
    try:
        # Get current companion state (simplified for direct response generation)
        companion_context = ai_companion_agent.get_companion_context_for_agent(
            student_id=current_user.student_id,
            agent_name=request.agent_name or "general"
        )
        
        if not companion_context.get("companion_available"):
            return {
                "success": True,
                "response": {
                    "message": f"🐻 {request.context}",
                    "emoji": "🐻",
                    "tone": "friendly_casual",
                    "follow_up_suggestions": ["Keep learning!", "Try another question!", "You're doing great!"],
                    "celebration_level": 5
                }
            }
        
        # For full response generation, we'd need mood state
        # For now, return enhanced response using companion context
        enhanced_response = ai_companion_agent.get_personalized_response_for_agent(
            student_id=current_user.student_id,
            agent_name=request.agent_name or "general",
            base_response=request.context
        )
        
        return {
            "success": True,
            "response": {
                "message": enhanced_response,
                "emoji": "🐻",
                "tone": companion_context.get("agent_integration", {}).get("suggested_tone", "friendly_casual"),
                "follow_up_suggestions": ["What would you like to learn next?", "Ready for another challenge?", "Great job so far!"],
                "celebration_level": 6 if companion_context.get("celebration_worthy") else 4
            }
        }
        
    except Exception as e:
        logger.error(f"Error in response generation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate personalized response"
        )

@router.post("/track-interaction")
async def track_agent_interaction(
    request: InteractionTrackingRequest,
    current_user: Student = Depends(get_current_user)
):
    """Track interaction from any agent for companion memory"""
    try:
        interaction_data = request.interaction_data.copy()
        
        # Add optional fields if provided
        if request.subject:
            interaction_data["subject"] = request.subject
        if request.performance_score is not None:
            interaction_data["performance_score"] = request.performance_score
        if request.achievement:
            interaction_data["achievement"] = request.achievement
            
        # Update companion memory
        ai_companion_agent.update_companion_from_agent_interaction(
            student_id=current_user.student_id,
            agent_name=request.agent_name,
            interaction_data=interaction_data
        )
        
        return {
            "success": True,
            "message": f"🐻 Interaction with {request.agent_name} tracked successfully!"
        }
        
    except Exception as e:
        logger.error(f"Error tracking agent interaction: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to track interaction"
        )

@router.get("/context/{agent_name}")
async def get_companion_context(
    agent_name: str,
    current_user: Student = Depends(get_current_user)
):
    """Get companion context for specific agent (used by other agents)"""
    try:
        context = ai_companion_agent.get_companion_context_for_agent(
            student_id=current_user.student_id,
            agent_name=agent_name
        )
        
        return {
            "success": True,
            "context": context
        }
        
    except Exception as e:
        logger.error(f"Error getting companion context for {agent_name}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get companion context"
        )

@router.get("/status")
async def get_companion_status(
    current_user: Student = Depends(get_current_user)
):
    """Get current companion status and statistics"""
    try:
        status_data = await ai_companion_agent.get_companion_status(
            student_id=current_user.student_id
        )
        
        if "error" in status_data:
            return {
                "success": False,
                "message": "🐻 Companion not found. Initialize your companion first!",
                "status": status_data
            }
        
        return {
            "success": True,
            "message": f"🐻 Here's your companion {status_data.get('companion_name', 'Buddy Bear')} status!",
            "status": status_data
        }
        
    except Exception as e:
        logger.error(f"Error getting companion status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get companion status"
        )

@router.post("/enhance-response")
async def enhance_agent_response(
    agent_name: str,
    base_response: str,
    current_user: Student = Depends(get_current_user)
):
    """Enhance any agent's response with companion personality (used by other agents)"""
    try:
        enhanced_response = ai_companion_agent.get_personalized_response_for_agent(
            student_id=current_user.student_id,
            agent_name=agent_name,
            base_response=base_response
        )
        
        return {
            "success": True,
            "original_response": base_response,
            "enhanced_response": enhanced_response
        }
        
    except Exception as e:
        logger.error(f"Error enhancing response for {agent_name}: {e}")
        # Return original response on error
        return {
            "success": True,
            "original_response": base_response,
            "enhanced_response": base_response,
            "note": "Enhancement failed, returned original response"
        }