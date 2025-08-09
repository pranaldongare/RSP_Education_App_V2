"""
Collaborative Learning API - RSP Education Agent V2 Phase 2.2
REST API endpoints for study groups, peer tutoring, and collaborative projects
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from pydantic import BaseModel
import logging

from database.database import get_db
from api.v1.auth import get_current_user
from database.models import Student
from services.collaborative_learning_service import collaborative_learning_service
from core.exceptions import AgentException

logger = logging.getLogger(__name__)

# Pydantic models for API requests/responses
class CreateStudyGroupRequest(BaseModel):
    """Request model for creating a study group"""
    group_name: str
    subject: str
    grade_range: List[int]  # [min_grade, max_grade]
    max_members: int = 6
    description: str = ""
    learning_objectives: Optional[List[str]] = None

class JoinGroupRequest(BaseModel):
    """Request model for joining a study group"""
    group_id: str
    student_id: str

class CreateTutoringSessionRequest(BaseModel):
    """Request model for creating a peer tutoring session"""
    tutor_id: str
    student_id: str
    subject: str
    topic: str
    scheduled_time: str  # ISO timestamp
    duration_minutes: int = 45

class CreateProjectRequest(BaseModel):
    """Request model for creating a collaborative project"""
    project_name: str
    subject: str
    grade_level: int
    description: str
    due_date: str  # ISO timestamp
    team_size: int = 4

class StudyGroupResponse(BaseModel):
    """Response model for study groups"""
    group_id: str
    group_name: str
    group_type: str
    subject: str
    grade_range: List[int]
    max_members: int
    current_members: List[str]
    leader_id: str
    description: str
    learning_objectives: List[str]
    meeting_schedule: Dict
    created_at: str
    status: str
    ai_matching_score: float
    performance_metrics: Dict

class PeerTutoringSessionResponse(BaseModel):
    """Response model for peer tutoring sessions"""
    session_id: str
    tutor_id: str
    student_id: str
    subject: str
    topic: str
    scheduled_time: str
    duration_minutes: int
    session_type: str
    learning_goals: List[str]
    effectiveness_score: float
    completion_status: str
    ai_insights: Dict

class CollaborativeProjectResponse(BaseModel):
    """Response model for collaborative projects"""
    project_id: str
    project_name: str
    subject: str
    grade_level: int
    team_members: List[str]
    project_leader: str
    description: str
    learning_objectives: List[str]
    timeline: Dict
    current_phase: str
    completion_percentage: float
    created_at: str
    due_date: str

# Create API router
router = APIRouter(prefix="/collaborative-learning", tags=["Collaborative Learning"])

@router.post("/study-groups/create")
async def create_study_group(
    request: CreateStudyGroupRequest,
    current_user: Student = Depends(get_current_user)
):
    """Create a new study group with AI-optimized settings"""
    try:
        study_group = await collaborative_learning_service.create_study_group(
            creator_id=current_user.student_id,
            group_name=request.group_name,
            subject=request.subject,
            grade_range=request.grade_range,
            max_members=request.max_members,
            description=request.description,
            learning_objectives=request.learning_objectives
        )
        
        return {
            "success": True,
            "message": f"👥 Study group '{request.group_name}' created successfully for {current_user.name}!",
            "data": {
                "group_id": study_group.group_id,
                "group_name": study_group.group_name,
                "group_type": study_group.group_type,
                "subject": study_group.subject,
                "grade_range": study_group.grade_range,
                "max_members": study_group.max_members,
                "current_members": study_group.current_members,
                "leader_id": study_group.leader_id,
                "description": study_group.description,
                "learning_objectives": study_group.learning_objectives,
                "meeting_schedule": study_group.meeting_schedule,
                "created_at": study_group.created_at,
                "status": study_group.status,
                "ai_matching_score": study_group.ai_matching_score
            },
            "group_features": {
                "ai_peer_matching": "Enabled - Find compatible study partners",
                "collaborative_tools": ["Group chat", "Resource sharing", "Progress tracking"],
                "meeting_coordination": "AI-optimized scheduling based on member availability",
                "progress_insights": "Real-time collaboration analytics and recommendations"
            },
            "next_steps": [
                "Invite compatible students to join your group",
                "Set up your first group study session",
                "Share learning resources and materials",
                "Use AI insights to optimize group collaboration"
            ]
        }
        
    except AgentException as e:
        logger.error(f"Error creating study group: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error creating study group: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during study group creation"
        )

@router.get("/study-groups/discover")
async def discover_study_groups(
    subject: Optional[str] = Query(None, description="Filter by subject"),
    limit: int = Query(10, description="Maximum number of groups to return"),
    current_user: Student = Depends(get_current_user)
):
    """Discover compatible study groups using AI matching"""
    try:
        compatible_groups = await collaborative_learning_service.find_compatible_groups(
            student_id=current_user.student_id,
            subject=subject,
            limit=limit
        )
        
        groups_data = []
        for group in compatible_groups:
            groups_data.append({
                "group_id": group.group_id,
                "group_name": group.group_name,
                "subject": group.subject,
                "grade_range": group.grade_range,
                "current_members_count": len(group.current_members),
                "max_members": group.max_members,
                "description": group.description,
                "learning_objectives": group.learning_objectives,
                "meeting_schedule": group.meeting_schedule,
                "status": group.status,
                "ai_matching_score": group.ai_matching_score,
                "compatibility_rating": "excellent" if group.ai_matching_score > 0.8 else "good" if group.ai_matching_score > 0.6 else "moderate"
            })
        
        return {
            "success": True,
            "message": f"🔍 Found {len(compatible_groups)} compatible study groups for {current_user.name}!",
            "data": groups_data,
            "discovery_summary": {
                "total_groups_found": len(compatible_groups),
                "subjects_available": list(set(g.subject for g in compatible_groups)),
                "grade_ranges": list(set(f"{g.grade_range[0]}-{g.grade_range[1]}" for g in compatible_groups)),
                "average_compatibility": sum(g.ai_matching_score for g in compatible_groups) / len(compatible_groups) if compatible_groups else 0
            },
            "matching_features": {
                "ai_compatibility_scoring": "Groups ranked by learning style, availability, and academic compatibility",
                "personalized_recommendations": "Based on your learning patterns and preferences",
                "grade_appropriate": "Groups matched to your academic level",
                "subject_alignment": "Groups focused on your areas of interest and study needs"
            }
        }
        
    except Exception as e:
        logger.error(f"Error discovering study groups: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during group discovery"
        )

@router.post("/study-groups/join")
async def join_study_group(
    request: JoinGroupRequest,
    current_user: Student = Depends(get_current_user)
):
    """Join a study group with AI compatibility verification"""
    try:
        success = await collaborative_learning_service.join_study_group(
            student_id=request.student_id,
            group_id=request.group_id
        )
        
        if success:
            return {
                "success": True,
                "message": f"🎉 Successfully joined the study group! Welcome to collaborative learning, {current_user.name}!",
                "data": {
                    "group_id": request.group_id,
                    "student_id": request.student_id,
                    "joined_at": "now",
                    "member_role": "student"
                },
                "welcome_package": {
                    "group_benefits": [
                        "📚 Collaborative study sessions with peers",
                        "🤝 Peer support and knowledge sharing",
                        "📊 AI-powered learning insights and recommendations",
                        "⏰ Optimized meeting scheduling based on group availability"
                    ],
                    "getting_started": [
                        "Introduce yourself to the group",
                        "Share your learning goals and preferences",
                        "Participate in upcoming group activities",
                        "Use collaboration tools for better learning"
                    ]
                }
            }
        else:
            return {
                "success": False,
                "message": "Unable to join study group",
                "error": "Group may be full, inactive, or you may already be a member"
            }
        
    except Exception as e:
        logger.error(f"Error joining study group: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during group joining"
        )

@router.post("/peer-tutoring/create-session")
async def create_peer_tutoring_session(
    request: CreateTutoringSessionRequest,
    current_user: Student = Depends(get_current_user)
):
    """Create a peer tutoring session with AI-enhanced planning"""
    try:
        session = await collaborative_learning_service.create_peer_tutoring_session(
            tutor_id=request.tutor_id,
            student_id=request.student_id,
            subject=request.subject,
            topic=request.topic,
            scheduled_time=request.scheduled_time,
            duration_minutes=request.duration_minutes
        )
        
        return {
            "success": True,
            "message": f"🎓 Peer tutoring session created successfully for {current_user.name}!",
            "data": {
                "session_id": session.session_id,
                "tutor_id": session.tutor_id,
                "student_id": session.student_id,
                "subject": session.subject,
                "topic": session.topic,
                "scheduled_time": session.scheduled_time,
                "duration_minutes": session.duration_minutes,
                "session_type": session.session_type,
                "learning_goals": session.learning_goals,
                "ai_insights": session.ai_insights
            },
            "session_features": {
                "ai_learning_goals": "Personalized learning objectives based on student needs",
                "progress_tracking": "Real-time tracking of learning progress and effectiveness",
                "peer_feedback": "Mutual feedback system for continuous improvement",
                "resource_sharing": "Share and access learning materials during sessions"
            },
            "preparation_tips": [
                "Review the topic beforehand to maximize session effectiveness",
                "Prepare specific questions or problem areas to discuss",
                "Have learning materials and resources ready",
                "Create a distraction-free learning environment"
            ]
        }
        
    except AgentException as e:
        logger.error(f"Error creating tutoring session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error creating tutoring session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during tutoring session creation"
        )

@router.post("/projects/create")
async def create_collaborative_project(
    request: CreateProjectRequest,
    current_user: Student = Depends(get_current_user)
):
    """Create a collaborative project with AI-enhanced planning"""
    try:
        project = await collaborative_learning_service.create_collaborative_project(
            creator_id=current_user.student_id,
            project_name=request.project_name,
            subject=request.subject,
            grade_level=request.grade_level,
            description=request.description,
            due_date=request.due_date,
            team_size=request.team_size
        )
        
        return {
            "success": True,
            "message": f"🚀 Collaborative project '{request.project_name}' created successfully for {current_user.name}!",
            "data": {
                "project_id": project.project_id,
                "project_name": project.project_name,
                "subject": project.subject,
                "grade_level": project.grade_level,
                "team_members": project.team_members,
                "project_leader": project.project_leader,
                "description": project.description,
                "learning_objectives": project.learning_objectives,
                "deliverables": project.deliverables,
                "timeline": project.timeline,
                "collaboration_tools": project.collaboration_tools,
                "current_phase": project.current_phase,
                "completion_percentage": project.completion_percentage,
                "due_date": project.due_date,
                "ai_collaboration_insights": project.ai_collaboration_insights
            },
            "project_features": {
                "collaboration_tools": ["Real-time chat", "Document sharing", "Virtual whiteboard", "Video calls"],
                "progress_tracking": "AI-powered project milestone tracking and analytics",
                "role_management": "Smart role assignment based on student strengths",
                "resource_library": "Shared library for project materials and references"
            },
            "success_tips": project.ai_collaboration_insights["collaboration_tips"]
        }
        
    except AgentException as e:
        logger.error(f"Error creating collaborative project: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error creating collaborative project: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during project creation"
        )

@router.get("/student-groups/{student_id}")
async def get_student_groups(
    student_id: str,
    current_user: Student = Depends(get_current_user)
):
    """Get all groups and projects a student is part of"""
    try:
        student_groups = await collaborative_learning_service.get_student_groups(student_id)
        
        return {
            "success": True,
            "message": f"📋 Retrieved all collaborative learning activities for student!",
            "data": {
                "study_groups": [
                    {
                        "group_id": group.group_id,
                        "group_name": group.group_name,
                        "subject": group.subject,
                        "status": group.status,
                        "member_count": len(group.current_members),
                        "role": "leader" if group.leader_id == student_id else "member",
                        "last_activity": group.last_activity
                    } for group in student_groups["study_groups"]
                ],
                "tutoring_sessions": [
                    {
                        "session_id": session.session_id,
                        "subject": session.subject,
                        "topic": session.topic,
                        "role": "tutor" if session.tutor_id == student_id else "student",
                        "scheduled_time": session.scheduled_time,
                        "completion_status": session.completion_status,
                        "effectiveness_score": session.effectiveness_score
                    } for session in student_groups["tutoring_sessions"]
                ],
                "collaborative_projects": [
                    {
                        "project_id": project.project_id,
                        "project_name": project.project_name,
                        "subject": project.subject,
                        "role": "leader" if project.project_leader == student_id else "member",
                        "current_phase": project.current_phase,
                        "completion_percentage": project.completion_percentage,
                        "due_date": project.due_date
                    } for project in student_groups["collaborative_projects"]
                ]
            },
            "activity_summary": {
                "total_study_groups": len(student_groups["study_groups"]),
                "active_tutoring_sessions": len([s for s in student_groups["tutoring_sessions"] if s.completion_status != "completed"]),
                "ongoing_projects": len([p for p in student_groups["collaborative_projects"] if p.completion_percentage < 100]),
                "leadership_roles": len([g for g in student_groups["study_groups"] if g.leader_id == student_id]) + 
                                   len([p for p in student_groups["collaborative_projects"] if p.project_leader == student_id])
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting student groups: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during student groups retrieval"
        )

@router.get("/insights/{group_id}")
async def get_collaboration_insights(
    group_id: str,
    current_user: Student = Depends(get_current_user)
):
    """Get AI insights for improving group collaboration"""
    try:
        insights = await collaborative_learning_service.get_collaboration_insights(group_id)
        
        insights_data = []
        for insight in insights:
            insights_data.append({
                "insight_id": insight.insight_id,
                "insight_type": insight.insight_type,
                "title": insight.title,
                "description": insight.description,
                "recommendations": insight.recommendations,
                "confidence": insight.confidence,
                "detected_at": insight.detected_at,
                "affected_members": insight.affected_members,
                "priority": insight.priority
            })
        
        return {
            "success": True,
            "message": f"🔍 Generated {len(insights)} collaboration insights for group optimization!",
            "data": insights_data,
            "insights_summary": {
                "total_insights": len(insights),
                "high_priority": len([i for i in insights if i.priority == "high"]),
                "insight_categories": list(set(i.insight_type for i in insights)),
                "actionable_recommendations": sum(len(i.recommendations) for i in insights),
                "overall_confidence": sum(i.confidence for i in insights) / len(insights) if insights else 0
            },
            "optimization_areas": {
                "group_dynamics": "Insights on member interaction and collaboration patterns",
                "learning_effectiveness": "Recommendations for improving group learning outcomes",
                "engagement_enhancement": "Strategies to boost participation and motivation",
                "performance_optimization": "Data-driven suggestions for better group performance"
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting collaboration insights: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during insights retrieval"
        )

@router.get("/dashboard-summary")
async def get_collaborative_learning_dashboard(
    current_user: Student = Depends(get_current_user)
):
    """Get comprehensive collaborative learning dashboard summary"""
    try:
        student_groups = await collaborative_learning_service.get_student_groups(current_user.student_id)
        
        # Calculate summary statistics
        active_groups = len([g for g in student_groups["study_groups"] if g.status == "active"])
        pending_sessions = len([s for s in student_groups["tutoring_sessions"] if s.completion_status == "scheduled"])
        ongoing_projects = len([p for p in student_groups["collaborative_projects"] if p.completion_percentage < 100])
        
        return {
            "success": True,
            "message": f"📊 Comprehensive collaborative learning dashboard for {current_user.name}!",
            "data": {
                "overview": {
                    "active_study_groups": active_groups,
                    "pending_tutoring_sessions": pending_sessions,
                    "ongoing_projects": ongoing_projects,
                    "total_collaborative_activities": active_groups + pending_sessions + ongoing_projects
                },
                "recent_activities": {
                    "newest_group": student_groups["study_groups"][0].group_name if student_groups["study_groups"] else None,
                    "next_tutoring_session": student_groups["tutoring_sessions"][0].scheduled_time if student_groups["tutoring_sessions"] else None,
                    "active_project": student_groups["collaborative_projects"][0].project_name if student_groups["collaborative_projects"] else None
                },
                "collaboration_stats": {
                    "groups_led": len([g for g in student_groups["study_groups"] if g.leader_id == current_user.student_id]),
                    "tutoring_as_tutor": len([s for s in student_groups["tutoring_sessions"] if s.tutor_id == current_user.student_id]),
                    "tutoring_as_student": len([s for s in student_groups["tutoring_sessions"] if s.student_id == current_user.student_id]),
                    "projects_leading": len([p for p in student_groups["collaborative_projects"] if p.project_leader == current_user.student_id])
                },
                "recommended_actions": [
                    "Join a study group in your favorite subject" if active_groups == 0 else "Continue engaging with your study groups",
                    "Offer peer tutoring in your strongest subjects" if len([s for s in student_groups["tutoring_sessions"] if s.tutor_id == current_user.student_id]) == 0 else "Keep helping peers through tutoring",
                    "Start a collaborative project with classmates" if ongoing_projects == 0 else "Focus on completing ongoing projects",
                    "Explore new subjects through collaborative learning"
                ]
            },
            "collaboration_benefits": {
                "peer_learning": "Learn from and teach fellow students",
                "social_skills": "Develop teamwork and communication abilities",
                "knowledge_retention": "Improve understanding through collaborative discussion",
                "motivation_boost": "Stay motivated through peer support and accountability"
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting collaborative learning dashboard: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during dashboard generation"
        )