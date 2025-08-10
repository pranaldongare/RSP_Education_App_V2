"""
API Router v1 - Phase 6 Production Integration
Main router for all API endpoints including comprehensive AI agents
"""

from fastapi import APIRouter
from api.v1.content import router as content_router
from api.v1.agents import router as agents_router
from api.v1.auth import router as auth_router
from api.v1.ai_companion import router as ai_companion_router
from api.v1.enhanced_analytics import router as enhanced_analytics_router
from api.v1.smart_notifications import router as smart_notifications_router
from api.v1.offline_support import router as offline_support_router
from api.v1.parent_dashboard import router as parent_dashboard_router
from api.v1.collaborative_learning import router as collaborative_learning_router
from api.v1.advanced_gamification import router as advanced_gamification_router


# Create main API router
api_router = APIRouter()

# Include sub-routers
api_router.include_router(auth_router)  # Authentication endpoints
api_router.include_router(content_router)
api_router.include_router(agents_router)  # All 7 AI agents endpoints
api_router.include_router(ai_companion_router)  # AI Companion Agent (8th Agent)
api_router.include_router(enhanced_analytics_router)  # Enhanced Analytics Dashboard
api_router.include_router(smart_notifications_router)  # Smart Notifications System
api_router.include_router(offline_support_router)  # Offline Support Foundation
api_router.include_router(parent_dashboard_router)  # Parent Dashboard & Communication
api_router.include_router(collaborative_learning_router)  # Collaborative Learning Features
api_router.include_router(advanced_gamification_router)  # Advanced Gamification Features


@api_router.get("/")
async def api_root():
    """API root endpoint"""
    return {
        "message": "RSP Education Agent API v1 - Production Ready + Enhanced AI Companion + Advanced Analytics + Smart Notifications + Offline Support + Parent Dashboard + Collaborative Learning + Advanced Gamification",
        "version": "2.7.0", 
        "description": "Complete AI tutoring system with 8 specialized agents + AI Companion + Advanced Analytics + Smart Notifications + Offline Mobile Support + Real-time Parent Monitoring + Collaborative Learning Features + Quest-based Learning & Virtual Rewards",
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
            "voice_interaction": "/agents/voice",
            "ai_companion": "/ai-companion"
        },
        "enhanced_analytics": {
            "dashboard": "/enhanced-analytics/dashboard",
            "learning_patterns": "/enhanced-analytics/learning-patterns",
            "performance_prediction": "/enhanced-analytics/performance-prediction",
            "insights": "/enhanced-analytics/insights",
            "track_session": "/enhanced-analytics/track-session",
            "summary": "/enhanced-analytics/summary",
            "learning_velocity": "/enhanced-analytics/learning-velocity",
            "engagement_heatmap": "/enhanced-analytics/engagement-heatmap"
        },
        "smart_notifications": {
            "study_time_recommendation": "/smart-notifications/study-time-recommendation",
            "schedule_reminders": "/smart-notifications/schedule-reminders",
            "trigger_celebration": "/smart-notifications/trigger-celebration",
            "send_progress_updates": "/smart-notifications/send-progress-updates",
            "pending": "/smart-notifications/pending",
            "mark_read": "/smart-notifications/mark-read",
            "preferences": "/smart-notifications/preferences",
            "history": "/smart-notifications/history",
            "quick_celebration": "/smart-notifications/quick-celebration",
            "dashboard_summary": "/smart-notifications/dashboard-summary"
        },
        "offline_support": {
            "cache_content": "/offline-support/cache-content",
            "cached_content": "/offline-support/cached-content/{content_id}",
            "offline_content": "/offline-support/offline-content",
            "cache_lesson_plan": "/offline-support/cache-lesson-plan",
            "cache_assessment": "/offline-support/cache-assessment",
            "cache_materials": "/offline-support/cache-materials",
            "sync_progress": "/offline-support/sync-progress",
            "capabilities": "/offline-support/capabilities",
            "smart_preload": "/offline-support/smart-preload",
            "clear_cache": "/offline-support/clear-cache",
            "sync_status": "/offline-support/sync-status"
        },
        "parent_dashboard": {
            "student_progress": "/parent-dashboard/student-progress/{student_id}",
            "learning_insights": "/parent-dashboard/learning-insights/{student_id}",
            "weekly_report": "/parent-dashboard/weekly-report/{student_id}",
            "alerts": "/parent-dashboard/alerts",
            "mark_alert_read": "/parent-dashboard/alerts/mark-read",
            "send_message": "/parent-dashboard/send-message",
            "communication_history": "/parent-dashboard/communication-history/{student_id}",
            "dashboard_summary": "/parent-dashboard/dashboard-summary/{student_id}"
        },
        "collaborative_learning": {
            "create_study_group": "/collaborative-learning/study-groups/create",
            "discover_study_groups": "/collaborative-learning/study-groups/discover",
            "join_study_group": "/collaborative-learning/study-groups/join",
            "create_tutoring_session": "/collaborative-learning/peer-tutoring/create-session",
            "create_collaborative_project": "/collaborative-learning/projects/create",
            "student_groups": "/collaborative-learning/student-groups/{student_id}",
            "collaboration_insights": "/collaborative-learning/insights/{group_id}",
            "dashboard_summary": "/collaborative-learning/dashboard-summary"
        },
        "advanced_gamification": {
            "create_quest": "/advanced-gamification/quests/create",
            "available_quests": "/advanced-gamification/quests/available",
            "start_quest": "/advanced-gamification/quests/start",
            "update_quest_progress": "/advanced-gamification/quests/progress",
            "character_progression": "/advanced-gamification/character/progression",
            "rewards_collection": "/advanced-gamification/rewards/collection",
            "create_competition": "/advanced-gamification/competitions/create",
            "active_competitions": "/advanced-gamification/competitions/active",
            "leaderboards": "/advanced-gamification/leaderboards/{leaderboard_type}",
            "dashboard_summary": "/advanced-gamification/dashboard-summary"
        },
        "system": {
            "health": "/agents/health",
            "status": "/agents/status/all",
            "initialize": "/agents/initialize"
        },
        "docs": "/docs"
    }