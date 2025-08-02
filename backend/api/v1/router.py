"""
API Router v1 - Phase 6 Production Integration
Main router for all API endpoints including comprehensive AI agents
"""

from fastapi import APIRouter
from api.v1.content import router as content_router
from api.v1.agents import router as agents_router
from api.v1.auth import router as auth_router


# Create main API router
api_router = APIRouter()

# Include sub-routers
api_router.include_router(auth_router)  # Authentication endpoints
api_router.include_router(content_router)
api_router.include_router(agents_router)  # All 7 AI agents endpoints


@api_router.get("/")
async def api_root():
    """API root endpoint"""
    return {
        "message": "RSP Education Agent API v1 - Production Ready",
        "version": "2.0.0",
        "description": "Complete AI tutoring system with 7 specialized agents",
        "authentication": {
            "register": "/auth/register",
            "login": "/auth/login",
            "logout": "/auth/logout",
            "profile": "/auth/me",
            "refresh": "/auth/refresh"
        },
        "agents": {
            "content_generator": "/agents/content",
            "assessment": "/agents/assessment", 
            "adaptive_learning": "/agents/adaptive",
            "engagement": "/agents/engagement",
            "analytics": "/agents/analytics",
            "learning_coordinator": "/agents/coordinator",
            "voice_interaction": "/agents/voice"
        },
        "system": {
            "health": "/agents/health",
            "status": "/agents/status/all",
            "initialize": "/agents/initialize"
        },
        "docs": "/docs"
    }