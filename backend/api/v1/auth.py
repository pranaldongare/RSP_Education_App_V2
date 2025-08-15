"""
Authentication API Endpoints - RSP Education Agent V2
Handles user registration, login, logout, and session management.
"""

from fastapi import APIRouter, HTTPException, Depends, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from datetime import datetime
import logging

from config.database import get_db_session as get_db
from database.models import Student
from auth.auth_service import (
    auth_service, UserRegistration, UserLogin, TokenResponse
)
from core.exceptions import AgentException

# Initialize router and security
router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()
logger = logging.getLogger(__name__)

def get_client_info(request: Request) -> Dict[str, str]:
    """Extract client information from request"""
    return {
        "user_agent": request.headers.get("user-agent", ""),
        "ip_address": request.client.host if request.client else "unknown"
    }

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
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/register", response_model=TokenResponse)
async def register_user(
    registration: UserRegistration,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user"""
    try:
        client_info = get_client_info(request)
        token_response = await auth_service.register_user(
            db, registration, 
            client_info["user_agent"], 
            client_info["ip_address"]
        )
        
        logger.info(f"User registered successfully: {registration.email}")
        return token_response
        
    except AgentException as e:
        logger.warning(f"Registration failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(status_code=500, detail="Registration failed")


@router.post("/login", response_model=TokenResponse)
async def login_user(
    login: UserLogin,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Login user and create session"""
    try:
        client_info = get_client_info(request)
        token_response = await auth_service.login_user(
            db, login,
            client_info["user_agent"],
            client_info["ip_address"]
        )
        
        logger.info(f"User logged in successfully: {login.email}")
        return token_response
        
    except AgentException as e:
        logger.warning(f"Login failed: {e}")
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail="Login failed")

@router.post("/refresh", response_model=TokenResponse)
async def refresh_access_token(
    refresh_request: Dict[str, str],
    db: AsyncSession = Depends(get_db)
):
    """Refresh access token using refresh token"""
    try:
        refresh_token = refresh_request.get("refresh_token")
        if not refresh_token:
            raise HTTPException(status_code=400, detail="Refresh token required")
        
        token_response = await auth_service.refresh_token(db, refresh_token)
        return token_response
        
    except AgentException as e:
        logger.warning(f"Token refresh failed: {e}")
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(status_code=500, detail="Token refresh failed")

@router.post("/logout")
async def logout_user(
    current_user: Student = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Logout user and invalidate session"""
    try:
        token = credentials.credentials
        success = await auth_service.logout_user(db, token)
        
        if success:
            logger.info(f"User logged out successfully: {current_user.id}")
            return {"message": "Logged out successfully"}
        else:
            raise HTTPException(status_code=400, detail="Logout failed")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Logout error: {e}")
        raise HTTPException(status_code=500, detail="Logout failed")

@router.get("/me")
async def get_current_user_info(
    current_user: Student = Depends(get_current_user)
):
    """Get current user information"""
    return {
        "student_id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "grade": current_user.grade,
        "preferred_language": current_user.preferred_language,
        "phone": current_user.phone,
        "school": current_user.school,
        "parent_email": current_user.parent_email,
        "last_login": current_user.last_login.isoformat() if current_user.last_login else None,
        "login_count": current_user.login_count,
        "created_at": current_user.created_at.isoformat(),
        "learning_style": current_user.learning_style,
        "preferences": current_user.preferences or {}
    }

@router.put("/profile")
async def update_user_profile(
    profile_update: Dict[str, Any],
    current_user: Student = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update user profile information"""
    try:
        # Allowed fields for update
        allowed_fields = {
            "name", "phone", "school", "parent_email", 
            "preferred_language", "learning_style", "preferences"
        }
        
        # Update allowed fields
        for field, value in profile_update.items():
            if field in allowed_fields and hasattr(current_user, field):
                setattr(current_user, field, value)
        
        current_user.updated_at = datetime.utcnow()
        db.commit()
        
        logger.info(f"Profile updated for user: {current_user.id}")
        return {"message": "Profile updated successfully"}
        
    except Exception as e:
        db.rollback()
        logger.error(f"Profile update error: {e}")
        raise HTTPException(status_code=500, detail="Profile update failed")

@router.get("/sessions")
async def get_user_sessions(
    current_user: Student = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's active sessions"""
    try:
        from database.models import UserSession
        sessions = db.query(UserSession).filter(
            UserSession.student_id == current_user.id,
            UserSession.is_active == True
        ).all()
        
        session_list = []
        for session in sessions:
            session_list.append({
                "id": session.id,
                "created_at": session.created_at.isoformat(),
                "last_accessed": session.last_accessed.isoformat(),
                "expires_at": session.expires_at.isoformat(),
                "device_type": session.device_type,
                "ip_address": session.ip_address,
                "user_agent": session.user_agent[:100] if session.user_agent else None
            })
        
        return {"sessions": session_list}
        
    except Exception as e:
        logger.error(f"Get sessions error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get sessions")

@router.delete("/sessions/{session_id}")
async def revoke_session(
    session_id: int,
    current_user: Student = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Revoke a specific session"""
    try:
        from database.models import UserSession
        session = db.query(UserSession).filter(
            UserSession.id == session_id,
            UserSession.student_id == current_user.id,
            UserSession.is_active == True
        ).first()
        
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session.is_active = False
        db.commit()
        
        logger.info(f"Session revoked: {session_id} for user: {current_user.id}")
        return {"message": "Session revoked successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Session revoke error: {e}")
        raise HTTPException(status_code=500, detail="Failed to revoke session")

@router.post("/change-password")
async def change_password(
    password_change: Dict[str, str],
    current_user: Student = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Change user password"""
    try:
        current_password = password_change.get("current_password")
        new_password = password_change.get("new_password")
        
        if not current_password or not new_password:
            raise HTTPException(status_code=400, detail="Current and new passwords required")
        
        if len(new_password) < 6:
            raise HTTPException(status_code=400, detail="New password must be at least 6 characters")
        
        # Verify current password
        if not auth_service.verify_password(current_password, current_user.password_hash):
            raise HTTPException(status_code=400, detail="Current password is incorrect")
        
        # Update password
        current_user.password_hash = auth_service.hash_password(new_password)
        current_user.updated_at = datetime.utcnow()
        
        # Invalidate all other sessions
        from database.models import UserSession
        db.query(UserSession).filter(
            UserSession.student_id == current_user.id,
            UserSession.is_active == True
        ).update({"is_active": False})
        
        db.commit()
        
        logger.info(f"Password changed for user: {current_user.id}")
        return {"message": "Password changed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Password change error: {e}")
        raise HTTPException(status_code=500, detail="Password change failed")

@router.get("/validate")
async def validate_token(
    current_user: Student = Depends(get_current_user)
):
    """Validate current authentication token"""
    return {
        "valid": True,
        "user_id": current_user.id,
        "email": current_user.email
    }
