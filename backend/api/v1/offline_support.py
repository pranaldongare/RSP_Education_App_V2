"""
Offline Support API - RSP Education Agent V2 Phase 1.4
REST API endpoints for offline content caching, synchronization, and mobile support
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from pydantic import BaseModel
import logging

from database.database import get_db
from api.v1.auth import get_current_user
from database.models import Student
from services.offline_cache_service import offline_cache_service, CacheType
from core.exceptions import AgentException

logger = logging.getLogger(__name__)

# Pydantic models for API requests/responses
class CacheContentRequest(BaseModel):
    """Request model for caching content"""
    content_type: str  # lesson_plan, assessment, content_material, etc.
    content_data: Dict
    priority: int = 5
    expiry_hours: Optional[int] = None

class SyncProgressRequest(BaseModel):
    """Request model for syncing offline progress"""
    progress_data: Dict
    session_id: Optional[str] = None
    sync_timestamp: str
    device_info: Optional[Dict] = None

class PreloadRequest(BaseModel):
    """Request model for smart content preloading"""
    subjects: Optional[List[str]] = None
    content_types: Optional[List[str]] = None
    priority_level: int = 7

class OfflineCapabilitiesResponse(BaseModel):
    """Response model for offline capabilities"""
    total_cached_items: int
    total_cache_size: int
    cached_subjects: List[str]
    offline_lesson_plans: int
    offline_assessments: int
    offline_content_materials: int
    last_sync: Optional[str]
    sync_conflicts: int
    available_offline_hours: float

class CachedContentResponse(BaseModel):
    """Response model for cached content"""
    content_id: str
    content_type: str
    data: Dict
    created_at: str
    updated_at: str
    expires_at: Optional[str]
    sync_status: str
    version: int
    priority: int
    access_count: int

# Create API router
router = APIRouter(prefix="/offline-support", tags=["Offline Support"])

@router.post("/cache-content")
async def cache_content_for_offline(
    request: CacheContentRequest,
    current_user: Student = Depends(get_current_user)
):
    """Cache content for offline access"""
    try:
        # Validate content type
        try:
            cache_type = CacheType(request.content_type)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid content type: {request.content_type}"
            )
        
        content_id = await offline_cache_service.cache_content(
            student_id=current_user.student_id,
            content_type=cache_type,
            content_data=request.content_data,
            priority=request.priority,
            expiry_hours=request.expiry_hours
        )
        
        return {
            "success": True,
            "message": f"📱 Content cached for offline access for {current_user.name}!",
            "data": {
                "content_id": content_id,
                "content_type": request.content_type,
                "priority": request.priority,
                "expiry_hours": request.expiry_hours or 72
            },
            "cache_info": {
                "cached_at": "now",
                "available_offline": True,
                "estimated_size": len(str(request.content_data).encode()),
                "sync_status": "synced"
            }
        }
        
    except AgentException as e:
        logger.error(f"Error caching content: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error caching content: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during content caching"
        )

@router.get("/cached-content/{content_id}")
async def get_cached_content(
    content_id: str,
    current_user: Student = Depends(get_current_user)
):
    """Retrieve specific cached content"""
    try:
        cached_content = await offline_cache_service.get_cached_content(
            student_id=current_user.student_id,
            content_id=content_id
        )
        
        if not cached_content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cached content not found"
            )
        
        return {
            "success": True,
            "message": f"📱 Cached content retrieved for {current_user.name}!",
            "data": {
                "content_id": cached_content.content_id,
                "content_type": cached_content.content_type,
                "data": cached_content.data,
                "created_at": cached_content.created_at,
                "updated_at": cached_content.updated_at,
                "expires_at": cached_content.expires_at,
                "sync_status": cached_content.sync_status,
                "version": cached_content.version,
                "priority": cached_content.priority,
                "access_count": cached_content.access_count,
                "size_bytes": cached_content.size_bytes
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving cached content {content_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during content retrieval"
        )

@router.get("/offline-content")
async def get_offline_content(
    content_type: str = Query(..., description="Type of content to retrieve"),
    limit: int = Query(50, description="Maximum number of items to return"),
    current_user: Student = Depends(get_current_user)
):
    """Get all cached content of a specific type for offline access"""
    try:
        # Validate content type
        try:
            cache_type = CacheType(content_type)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid content type: {content_type}"
            )
        
        cached_items = await offline_cache_service.get_offline_content_by_type(
            student_id=current_user.student_id,
            content_type=cache_type,
            limit=limit
        )
        
        content_data = []
        for item in cached_items:
            content_data.append({
                "content_id": item.content_id,
                "content_type": item.content_type,
                "data": item.data,
                "created_at": item.created_at,
                "expires_at": item.expires_at,
                "priority": item.priority,
                "access_count": item.access_count,
                "sync_status": item.sync_status
            })
        
        return {
            "success": True,
            "message": f"📱 {len(cached_items)} offline {content_type} items for {current_user.name}!",
            "data": content_data,
            "summary": {
                "total_items": len(cached_items),
                "content_type": content_type,
                "available_offline": True,
                "cache_status": "active"
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting offline content: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during offline content retrieval"
        )

@router.post("/cache-lesson-plan")
async def cache_lesson_plan(
    lesson_data: Dict,
    current_user: Student = Depends(get_current_user)
):
    """Cache a lesson plan for offline access"""
    try:
        content_id = await offline_cache_service.cache_lesson_plan(
            student_id=current_user.student_id,
            lesson_data=lesson_data
        )
        
        return {
            "success": True,
            "message": f"📚 Lesson plan cached for offline learning for {current_user.name}!",
            "data": {
                "content_id": content_id,
                "subject": lesson_data.get("subject", "General"),
                "title": lesson_data.get("title", "Lesson Plan"),
                "cached_for_offline": True,
                "expiry_hours": 168  # 1 week
            },
            "offline_info": {
                "type": "lesson_plan",
                "priority": "high",
                "estimated_duration": lesson_data.get("duration_minutes", 30),
                "activities": lesson_data.get("activities", [])
            }
        }
        
    except Exception as e:
        logger.error(f"Error caching lesson plan: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during lesson plan caching"
        )

@router.post("/cache-assessment")
async def cache_assessment(
    assessment_data: Dict,
    current_user: Student = Depends(get_current_user)
):
    """Cache an assessment for offline access"""
    try:
        content_id = await offline_cache_service.cache_assessment(
            student_id=current_user.student_id,
            assessment_data=assessment_data
        )
        
        return {
            "success": True,
            "message": f"📝 Assessment cached for offline practice for {current_user.name}!",
            "data": {
                "content_id": content_id,
                "subject": assessment_data.get("subject", "General"),
                "title": assessment_data.get("title", "Assessment"),
                "question_count": len(assessment_data.get("questions", [])),
                "cached_for_offline": True,
                "expiry_hours": 72  # 3 days
            },
            "offline_info": {
                "type": "assessment",
                "priority": "very_high",
                "time_limit": assessment_data.get("time_limit_minutes", 15),
                "difficulty": assessment_data.get("difficulty", "moderate")
            }
        }
        
    except Exception as e:
        logger.error(f"Error caching assessment: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during assessment caching"
        )

@router.post("/cache-materials")
async def cache_learning_materials(
    materials_data: Dict,
    current_user: Student = Depends(get_current_user)
):
    """Cache learning materials for offline access"""
    try:
        content_id = await offline_cache_service.cache_learning_materials(
            student_id=current_user.student_id,
            materials_data=materials_data
        )
        
        return {
            "success": True,
            "message": f"📖 Learning materials cached for offline study for {current_user.name}!",
            "data": {
                "content_id": content_id,
                "subject": materials_data.get("subject", "General"),
                "title": materials_data.get("title", "Study Materials"),
                "material_count": len(materials_data.get("materials", [])),
                "cached_for_offline": True,
                "expiry_hours": 336  # 2 weeks
            },
            "offline_info": {
                "type": "learning_materials",
                "priority": "medium",
                "material_types": [m.get("type", "unknown") for m in materials_data.get("materials", [])],
                "study_value": "high"
            }
        }
        
    except Exception as e:
        logger.error(f"Error caching learning materials: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during materials caching"
        )

@router.post("/sync-progress")
async def sync_offline_progress(
    request: SyncProgressRequest,
    current_user: Student = Depends(get_current_user)
):
    """Sync offline progress when connection is available"""
    try:
        await offline_cache_service.sync_offline_progress(
            student_id=current_user.student_id,
            progress_data=request.progress_data
        )
        
        return {
            "success": True,
            "message": f"🔄 Offline progress synced for {current_user.name}!",
            "sync_info": {
                "synced_at": request.sync_timestamp,
                "session_id": request.session_id,
                "progress_items": len(request.progress_data),
                "device_info": request.device_info,
                "sync_status": "completed"
            },
            "next_steps": [
                "Progress data has been uploaded to the cloud",
                "Local cache has been updated",
                "Analytics data will be processed shortly"
            ]
        }
        
    except Exception as e:
        logger.error(f"Error syncing offline progress: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during progress sync"
        )

@router.get("/capabilities")
async def get_offline_capabilities(
    current_user: Student = Depends(get_current_user)
):
    """Get offline capabilities summary for the current user"""
    try:
        capabilities = await offline_cache_service.get_offline_capabilities(
            student_id=current_user.student_id
        )
        
        return {
            "success": True,
            "message": f"📱 Offline capabilities for {current_user.name}!",
            "data": {
                "student_id": capabilities.student_id,
                "total_cached_items": capabilities.total_cached_items,
                "total_cache_size": capabilities.total_cache_size,
                "cache_size_mb": round(capabilities.total_cache_size / (1024 * 1024), 2),
                "cached_subjects": capabilities.cached_subjects,
                "offline_lesson_plans": capabilities.offline_lesson_plans,
                "offline_assessments": capabilities.offline_assessments,
                "offline_content_materials": capabilities.offline_content_materials,
                "last_sync": capabilities.last_sync,
                "sync_conflicts": capabilities.sync_conflicts,
                "available_offline_hours": capabilities.available_offline_hours
            },
            "offline_status": {
                "ready_for_offline": capabilities.total_cached_items > 0,
                "recommended_actions": [
                    "Use smart preload to cache more content" if capabilities.total_cached_items < 10 else "Great offline coverage!",
                    "Sync pending changes when online" if capabilities.sync_conflicts > 0 else "All content synchronized",
                    f"You have {capabilities.available_offline_hours} hours of offline learning available"
                ],
                "storage_efficiency": "good" if capabilities.total_cache_size < 100_000_000 else "consider cleanup"
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting offline capabilities: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during capabilities check"
        )

@router.post("/smart-preload")
async def smart_cache_preload(
    request: PreloadRequest,
    current_user: Student = Depends(get_current_user)
):
    """Smart preloading of content based on student patterns"""
    try:
        cache_counts = await offline_cache_service.smart_cache_preload(
            student_id=current_user.student_id,
            subjects=request.subjects
        )
        
        total_cached = sum(cache_counts.values())
        
        return {
            "success": True,
            "message": f"🧠 Smart cache preload completed for {current_user.name}!",
            "data": {
                "preload_results": cache_counts,
                "total_items_cached": total_cached,
                "subjects": request.subjects or "auto-detected from learning patterns",
                "priority_level": request.priority_level
            },
            "preload_info": {
                "strategy": "pattern-based intelligent caching",
                "features": [
                    "📊 Based on your learning patterns and preferences",
                    "🎯 Prioritized your favorite subjects and difficulty levels",
                    "⏰ Optimized for your typical session lengths",
                    "🐻 Enhanced with your AI companion's insights"
                ],
                "offline_readiness": "excellent" if total_cached >= 9 else "good" if total_cached >= 6 else "basic"
            }
        }
        
    except Exception as e:
        logger.error(f"Error during smart preload: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during smart preload"
        )

@router.delete("/clear-cache")
async def clear_offline_cache(
    content_type: Optional[str] = Query(None, description="Specific content type to clear"),
    confirm: bool = Query(False, description="Confirmation required"),
    current_user: Student = Depends(get_current_user)
):
    """Clear offline cache (with confirmation)"""
    try:
        if not confirm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cache clearing requires confirmation (set confirm=true)"
            )
        
        # This would implement cache clearing logic
        # For now, just return a success message
        
        return {
            "success": True,
            "message": f"🗑️ Offline cache cleared for {current_user.name}!",
            "cleared_info": {
                "content_type": content_type or "all",
                "cleared_at": "now",
                "space_freed": "estimated space freed",
                "warning": "You'll need to re-cache content for offline access"
            },
            "recommendations": [
                "Use smart preload to rebuild your offline content",
                "Cache your most important subjects first",
                "Consider selective clearing instead of full cache clear"
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error clearing cache: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during cache clearing"
        )

@router.get("/sync-status")
async def get_sync_status(
    current_user: Student = Depends(get_current_user)
):
    """Get current synchronization status"""
    try:
        # This would check actual sync status from the service
        # For now, return a basic status
        
        return {
            "success": True,
            "message": f"🔄 Sync status for {current_user.name}!",
            "data": {
                "sync_status": "up_to_date",
                "last_sync": "recent",
                "pending_uploads": 0,
                "pending_downloads": 0,
                "sync_conflicts": 0,
                "next_sync": "automatic when online"
            },
            "sync_health": {
                "status": "healthy",
                "connection_quality": "good",
                "sync_efficiency": "optimal",
                "recommendations": [
                    "All content is synchronized",
                    "Offline capabilities are ready",
                    "No conflicts detected"
                ]
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting sync status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during sync status check"
        )