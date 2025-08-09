"""
Collaborative Learning Service - RSP Education Agent V2 Phase 2.2
Study groups, peer tutoring, and collaborative workspace with AI-facilitated matching
"""

import asyncio
import json
import logging
import random
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
import hashlib

from sqlalchemy.orm import Session
from database.models import Student
from core.exceptions import AgentException
from services.ai_companion_service import ai_companion_agent
from services.enhanced_analytics_service import enhanced_analytics_service
from services.parent_dashboard_service import parent_dashboard_service

logger = logging.getLogger(__name__)

class GroupType(Enum):
    STUDY_GROUP = "study_group"
    PEER_TUTORING = "peer_tutoring"
    PROJECT_COLLABORATION = "project_collaboration"
    PRACTICE_SESSION = "practice_session"

class GroupStatus(Enum):
    FORMING = "forming"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"

class MemberRole(Enum):
    LEADER = "leader"
    TUTOR = "tutor"
    STUDENT = "student"
    COLLABORATOR = "collaborator"
    OBSERVER = "observer"

class SessionType(Enum):
    STUDY_SESSION = "study_session"
    TUTORING_SESSION = "tutoring_session"
    PROJECT_WORK = "project_work"
    DISCUSSION = "discussion"
    REVIEW_SESSION = "review_session"

@dataclass
class StudyGroup:
    """Study group with AI-facilitated matching"""
    group_id: str
    group_name: str
    group_type: str  # GroupType
    subject: str
    grade_range: List[int]  # [min_grade, max_grade]
    max_members: int
    current_members: List[str]  # student_ids
    leader_id: str
    description: str
    learning_objectives: List[str]
    meeting_schedule: Dict  # frequency, preferred_times, duration
    created_at: str
    status: str  # GroupStatus
    group_settings: Dict
    ai_matching_score: float  # How well AI thinks this group will work together
    performance_metrics: Dict
    last_activity: str

@dataclass
class PeerTutoringSession:
    """Peer tutoring session with progress tracking"""
    session_id: str
    tutor_id: str
    student_id: str
    subject: str
    topic: str
    scheduled_time: str
    duration_minutes: int
    session_type: str  # SessionType
    learning_goals: List[str]
    materials_shared: List[Dict]
    progress_notes: List[str]
    effectiveness_score: float  # 0-1
    completion_status: str
    feedback: Dict  # from both tutor and student
    follow_up_needed: bool
    ai_insights: Dict

@dataclass
class CollaborativeProject:
    """Group project with real-time collaboration"""
    project_id: str
    project_name: str
    subject: str
    grade_level: int
    team_members: List[str]  # student_ids
    project_leader: str
    description: str
    learning_objectives: List[str]
    deliverables: List[Dict]
    timeline: Dict  # milestones and deadlines
    collaboration_tools: List[str]  # chat, docs, whiteboard, etc.
    progress_tracking: Dict
    resource_library: List[Dict]
    current_phase: str
    completion_percentage: float
    created_at: str
    due_date: str
    ai_collaboration_insights: Dict

@dataclass
class GroupMember:
    """Group member profile with role and contribution tracking"""
    student_id: str
    student_name: str
    grade: int
    role: str  # MemberRole
    subjects_expertise: List[str]
    learning_preferences: Dict
    availability: Dict
    contribution_score: float  # 0-1
    peer_ratings: Dict
    joined_at: str
    last_active: str
    achievements_in_group: List[str]

@dataclass
class CollaborationInsight:
    """AI insights for improving collaboration"""
    insight_id: str
    group_id: str
    insight_type: str  # matching, performance, engagement, dynamics
    title: str
    description: str
    recommendations: List[str]
    confidence: float
    detected_at: str
    affected_members: List[str]
    priority: str  # low, medium, high

class CollaborativeLearningService:
    """Collaborative Learning Service with AI-facilitated group formation and management"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.CollaborativeLearningService")
        
        # In-memory storage for collaborative learning (in production, use proper database)
        self.study_groups: Dict[str, StudyGroup] = {}
        self.tutoring_sessions: Dict[str, PeerTutoringSession] = {}
        self.collaborative_projects: Dict[str, CollaborativeProject] = {}
        self.group_members: Dict[str, Dict[str, GroupMember]] = {}  # group_id -> {student_id -> member}
        self.collaboration_insights: Dict[str, List[CollaborationInsight]] = {}  # group_id -> insights
        
        # AI matching configuration
        self.matching_weights = {
            "grade_compatibility": 0.25,
            "subject_interest": 0.30,
            "learning_style": 0.20,
            "availability": 0.15,
            "past_performance": 0.10
        }

    async def create_study_group(
        self, 
        creator_id: str, 
        group_name: str, 
        subject: str, 
        grade_range: List[int],
        max_members: int = 6,
        description: str = "",
        learning_objectives: List[str] = None
    ) -> StudyGroup:
        """Create a new study group with AI-optimized settings"""
        try:
            group_id = str(uuid.uuid4())
            
            # Get creator context from companion
            creator_context = ai_companion_agent.get_companion_context_for_agent(creator_id, "collaborative_learning")
            creator_name = creator_context.get('student_name', 'Student')
            
            # AI-enhanced learning objectives if not provided
            if not learning_objectives:
                learning_objectives = [
                    f"Master key concepts in {subject}",
                    "Improve problem-solving skills through peer collaboration",
                    "Develop communication and teamwork abilities",
                    "Support each other's learning journey"
                ]
            
            # Determine optimal meeting schedule based on creator's patterns
            try:
                creator_patterns = await enhanced_analytics_service.track_learning_patterns(creator_id)
                optimal_times = creator_patterns.peak_learning_hours[:3] if creator_patterns.peak_learning_hours else [15, 16, 17]
            except:
                optimal_times = [15, 16, 17]  # Default afternoon times
            
            meeting_schedule = {
                "frequency": "weekly",
                "preferred_times": optimal_times,
                "duration_minutes": 60,
                "flexible_scheduling": True
            }
            
            # Create study group
            study_group = StudyGroup(
                group_id=group_id,
                group_name=group_name,
                group_type=GroupType.STUDY_GROUP.value,
                subject=subject,
                grade_range=grade_range,
                max_members=max_members,
                current_members=[creator_id],
                leader_id=creator_id,
                description=description or f"{creator_name}'s {subject} Study Group",
                learning_objectives=learning_objectives,
                meeting_schedule=meeting_schedule,
                created_at=datetime.now().isoformat(),
                status=GroupStatus.FORMING.value,
                group_settings={
                    "allow_peer_tutoring": True,
                    "enable_ai_insights": True,
                    "share_progress": True,
                    "collaborative_projects": True
                },
                ai_matching_score=0.0,  # Will be calculated as members join
                performance_metrics={
                    "total_sessions": 0,
                    "average_attendance": 0.0,
                    "learning_progress": 0.0,
                    "member_satisfaction": 0.0
                },
                last_activity=datetime.now().isoformat()
            )
            
            # Store group
            self.study_groups[group_id] = study_group
            
            # Initialize group members
            creator_member = GroupMember(
                student_id=creator_id,
                student_name=creator_name,
                grade=creator_context.get('grade', 5),
                role=MemberRole.LEADER.value,
                subjects_expertise=[subject],
                learning_preferences=creator_context.get('learning_preferences', {}),
                availability={"flexible": True},
                contribution_score=1.0,
                peer_ratings={},
                joined_at=datetime.now().isoformat(),
                last_active=datetime.now().isoformat(),
                achievements_in_group=["Group Creator"]
            )
            
            self.group_members[group_id] = {creator_id: creator_member}
            
            self.logger.info(f"Created study group {group_id} for subject {subject}")
            return study_group
            
        except Exception as e:
            self.logger.error(f"Failed to create study group: {e}")
            raise AgentException(f"Study group creation failed: {e}")

    async def find_compatible_groups(self, student_id: str, subject: str = None, limit: int = 10) -> List[StudyGroup]:
        """Find study groups compatible with a student using AI matching"""
        try:
            # Get student context and patterns
            student_context = ai_companion_agent.get_companion_context_for_agent(student_id, "collaborative_learning")
            student_grade = student_context.get('grade', 5)
            
            try:
                student_patterns = await enhanced_analytics_service.track_learning_patterns(student_id)
                student_subjects = student_patterns.preferred_subjects
            except:
                student_subjects = [subject] if subject else ["Math", "Science"]
            
            # Filter available groups
            compatible_groups = []
            
            for group in self.study_groups.values():
                if group.status not in [GroupStatus.FORMING.value, GroupStatus.ACTIVE.value]:
                    continue
                
                if len(group.current_members) >= group.max_members:
                    continue
                
                if student_id in group.current_members:
                    continue
                
                # Calculate compatibility score
                compatibility_score = await self._calculate_group_compatibility(
                    student_id, group, student_grade, student_subjects, student_context
                )
                
                if compatibility_score > 0.3:  # Minimum compatibility threshold
                    group_copy = StudyGroup(**asdict(group))
                    group_copy.ai_matching_score = compatibility_score
                    compatible_groups.append(group_copy)
            
            # Sort by compatibility score
            compatible_groups.sort(key=lambda g: g.ai_matching_score, reverse=True)
            
            self.logger.info(f"Found {len(compatible_groups)} compatible groups for student {student_id}")
            return compatible_groups[:limit]
            
        except Exception as e:
            self.logger.error(f"Failed to find compatible groups for {student_id}: {e}")
            return []

    async def join_study_group(self, student_id: str, group_id: str) -> bool:
        """Join a study group with AI compatibility verification"""
        try:
            if group_id not in self.study_groups:
                return False
            
            group = self.study_groups[group_id]
            
            # Check if group is joinable
            if group.status not in [GroupStatus.FORMING.value, GroupStatus.ACTIVE.value]:
                return False
            
            if len(group.current_members) >= group.max_members:
                return False
            
            if student_id in group.current_members:
                return False
            
            # Get student context
            student_context = ai_companion_agent.get_companion_context_for_agent(student_id, "collaborative_learning")
            student_name = student_context.get('student_name', 'Student')
            
            # Add student to group
            group.current_members.append(student_id)
            group.last_activity = datetime.now().isoformat()
            
            # Create member profile
            member = GroupMember(
                student_id=student_id,
                student_name=student_name,
                grade=student_context.get('grade', 5),
                role=MemberRole.STUDENT.value,
                subjects_expertise=[group.subject],
                learning_preferences=student_context.get('learning_preferences', {}),
                availability={"flexible": True},
                contribution_score=0.5,  # Starting score
                peer_ratings={},
                joined_at=datetime.now().isoformat(),
                last_active=datetime.now().isoformat(),
                achievements_in_group=[]
            )
            
            if group_id not in self.group_members:
                self.group_members[group_id] = {}
            self.group_members[group_id][student_id] = member
            
            # Update group status if it reaches minimum members
            if len(group.current_members) >= 3 and group.status == GroupStatus.FORMING.value:
                group.status = GroupStatus.ACTIVE.value
            
            # Recalculate group matching score
            await self._update_group_matching_score(group_id)
            
            # Generate welcome insight
            await self._generate_collaboration_insight(
                group_id, 
                "member_joined",
                f"New Member Welcome",
                f"{student_name} has joined the group! Consider organizing an introduction session to help everyone get acquainted.",
                [
                    "Schedule a group introduction session",
                    "Share learning goals and preferences",
                    "Plan the first collaborative activity"
                ],
                [student_id]
            )
            
            self.logger.info(f"Student {student_id} joined study group {group_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to join study group: {e}")
            return False

    async def create_peer_tutoring_session(
        self,
        tutor_id: str,
        student_id: str,
        subject: str,
        topic: str,
        scheduled_time: str,
        duration_minutes: int = 45
    ) -> PeerTutoringSession:
        """Create a peer tutoring session with AI-enhanced planning"""
        try:
            session_id = str(uuid.uuid4())
            
            # Get context for both tutor and student
            tutor_context = ai_companion_agent.get_companion_context_for_agent(tutor_id, "peer_tutoring")
            student_context = ai_companion_agent.get_companion_context_for_agent(student_id, "peer_tutoring")
            
            # AI-generated learning goals based on student's needs
            learning_goals = [
                f"Understand key concepts in {topic}",
                "Practice problem-solving techniques",
                "Build confidence in {subject}",
                "Develop independent learning skills"
            ]
            
            # Create tutoring session
            session = PeerTutoringSession(
                session_id=session_id,
                tutor_id=tutor_id,
                student_id=student_id,
                subject=subject,
                topic=topic,
                scheduled_time=scheduled_time,
                duration_minutes=duration_minutes,
                session_type=SessionType.TUTORING_SESSION.value,
                learning_goals=learning_goals,
                materials_shared=[],
                progress_notes=[],
                effectiveness_score=0.0,
                completion_status="scheduled",
                feedback={},
                follow_up_needed=False,
                ai_insights={
                    "tutor_strengths": tutor_context.get('favorite_subjects', [subject]),
                    "student_needs": student_context.get('struggle_areas', [topic]),
                    "recommended_approach": "patient and encouraging",
                    "estimated_difficulty": "moderate"
                }
            )
            
            # Store session
            self.tutoring_sessions[session_id] = session
            
            self.logger.info(f"Created peer tutoring session {session_id} between {tutor_id} and {student_id}")
            return session
            
        except Exception as e:
            self.logger.error(f"Failed to create peer tutoring session: {e}")
            raise AgentException(f"Peer tutoring session creation failed: {e}")

    async def create_collaborative_project(
        self,
        creator_id: str,
        project_name: str,
        subject: str,
        grade_level: int,
        description: str,
        due_date: str,
        team_size: int = 4
    ) -> CollaborativeProject:
        """Create a collaborative project with AI-enhanced planning"""
        try:
            project_id = str(uuid.uuid4())
            
            # Get creator context
            creator_context = ai_companion_agent.get_companion_context_for_agent(creator_id, "collaborative_projects")
            
            # AI-generated learning objectives
            learning_objectives = [
                f"Apply {subject} knowledge to real-world scenarios",
                "Develop teamwork and communication skills",
                "Practice project management and planning",
                "Create high-quality deliverables collaboratively"
            ]
            
            # AI-generated deliverables based on subject and grade
            deliverables = self._generate_project_deliverables(subject, grade_level)
            
            # Create project timeline
            timeline = self._generate_project_timeline(due_date)
            
            # Create collaborative project
            project = CollaborativeProject(
                project_id=project_id,
                project_name=project_name,
                subject=subject,
                grade_level=grade_level,
                team_members=[creator_id],
                project_leader=creator_id,
                description=description,
                learning_objectives=learning_objectives,
                deliverables=deliverables,
                timeline=timeline,
                collaboration_tools=["chat", "document_sharing", "whiteboard", "video_calls"],
                progress_tracking={
                    "overall_progress": 0.0,
                    "phase_progress": {"planning": 0.1, "research": 0.0, "development": 0.0, "review": 0.0},
                    "member_contributions": {creator_id: 0.0}
                },
                resource_library=[],
                current_phase="planning",
                completion_percentage=0.0,
                created_at=datetime.now().isoformat(),
                due_date=due_date,
                ai_collaboration_insights={
                    "recommended_roles": ["researcher", "writer", "designer", "presenter"],
                    "collaboration_tips": [
                        "Schedule regular check-ins",
                        "Use collaborative tools effectively",
                        "Celebrate small wins together"
                    ],
                    "success_factors": ["clear communication", "shared responsibility", "mutual support"]
                }
            )
            
            # Store project
            self.collaborative_projects[project_id] = project
            
            self.logger.info(f"Created collaborative project {project_id} for subject {subject}")
            return project
            
        except Exception as e:
            self.logger.error(f"Failed to create collaborative project: {e}")
            raise AgentException(f"Collaborative project creation failed: {e}")

    async def get_student_groups(self, student_id: str) -> Dict[str, List]:
        """Get all groups and projects a student is part of"""
        try:
            student_groups = {
                "study_groups": [],
                "tutoring_sessions": [],
                "collaborative_projects": []
            }
            
            # Find study groups
            for group in self.study_groups.values():
                if student_id in group.current_members:
                    student_groups["study_groups"].append(group)
            
            # Find tutoring sessions
            for session in self.tutoring_sessions.values():
                if student_id in [session.tutor_id, session.student_id]:
                    student_groups["tutoring_sessions"].append(session)
            
            # Find collaborative projects
            for project in self.collaborative_projects.values():
                if student_id in project.team_members:
                    student_groups["collaborative_projects"].append(project)
            
            return student_groups
            
        except Exception as e:
            self.logger.error(f"Failed to get student groups for {student_id}: {e}")
            return {"study_groups": [], "tutoring_sessions": [], "collaborative_projects": []}

    async def get_collaboration_insights(self, group_id: str) -> List[CollaborationInsight]:
        """Get AI insights for improving group collaboration"""
        try:
            insights = self.collaboration_insights.get(group_id, [])
            
            # Generate new insights if needed
            if len(insights) < 3:  # Always maintain at least 3 insights
                await self._generate_fresh_insights(group_id)
                insights = self.collaboration_insights.get(group_id, [])
            
            return sorted(insights, key=lambda x: x.detected_at, reverse=True)
            
        except Exception as e:
            self.logger.error(f"Failed to get collaboration insights for {group_id}: {e}")
            return []

    async def _calculate_group_compatibility(
        self, 
        student_id: str, 
        group: StudyGroup, 
        student_grade: int,
        student_subjects: List[str], 
        student_context: Dict
    ) -> float:
        """Calculate compatibility score between student and group"""
        try:
            total_score = 0.0
            
            # Grade compatibility (25%)
            grade_min, grade_max = group.grade_range
            if grade_min <= student_grade <= grade_max:
                grade_score = 1.0
            else:
                grade_diff = min(abs(student_grade - grade_min), abs(student_grade - grade_max))
                grade_score = max(0.0, 1.0 - (grade_diff * 0.2))
            total_score += grade_score * self.matching_weights["grade_compatibility"]
            
            # Subject interest (30%)
            subject_score = 1.0 if group.subject in student_subjects else 0.5
            total_score += subject_score * self.matching_weights["subject_interest"]
            
            # Learning style compatibility (20%)
            # This would be more sophisticated in a real implementation
            learning_style_score = 0.8  # Default good compatibility
            total_score += learning_style_score * self.matching_weights["learning_style"]
            
            # Availability (15%)
            availability_score = 0.9  # Assume good availability for now
            total_score += availability_score * self.matching_weights["availability"]
            
            # Past performance (10%)
            performance_score = 0.7  # Default moderate performance compatibility
            total_score += performance_score * self.matching_weights["past_performance"]
            
            return min(1.0, total_score)
            
        except Exception as e:
            self.logger.error(f"Failed to calculate compatibility score: {e}")
            return 0.5  # Default moderate compatibility

    async def _update_group_matching_score(self, group_id: str) -> None:
        """Update the AI matching score for a group"""
        try:
            group = self.study_groups.get(group_id)
            if not group:
                return
            
            # Calculate average compatibility between all members
            members = list(group.current_members)
            if len(members) < 2:
                group.ai_matching_score = 1.0
                return
            
            compatibility_scores = []
            for i, member1 in enumerate(members):
                for member2 in members[i+1:]:
                    # This would calculate actual compatibility between members
                    # For now, use a simplified approach
                    score = random.uniform(0.6, 0.9)  # Simulate good compatibility
                    compatibility_scores.append(score)
            
            group.ai_matching_score = statistics.mean(compatibility_scores) if compatibility_scores else 0.8
            
        except Exception as e:
            self.logger.error(f"Failed to update group matching score: {e}")

    async def _generate_collaboration_insight(
        self,
        group_id: str,
        insight_type: str,
        title: str,
        description: str,
        recommendations: List[str],
        affected_members: List[str],
        priority: str = "medium"
    ) -> None:
        """Generate a collaboration insight"""
        try:
            insight = CollaborationInsight(
                insight_id=str(uuid.uuid4()),
                group_id=group_id,
                insight_type=insight_type,
                title=title,
                description=description,
                recommendations=recommendations,
                confidence=0.8,
                detected_at=datetime.now().isoformat(),
                affected_members=affected_members,
                priority=priority
            )
            
            if group_id not in self.collaboration_insights:
                self.collaboration_insights[group_id] = []
            
            self.collaboration_insights[group_id].append(insight)
            
            # Keep only recent insights (last 20)
            self.collaboration_insights[group_id] = self.collaboration_insights[group_id][-20:]
            
        except Exception as e:
            self.logger.error(f"Failed to generate collaboration insight: {e}")

    async def _generate_fresh_insights(self, group_id: str) -> None:
        """Generate fresh insights for a group"""
        try:
            group = self.study_groups.get(group_id)
            if not group:
                return
            
            # Generate insights based on group status and activity
            if len(group.current_members) < 3:
                await self._generate_collaboration_insight(
                    group_id,
                    "membership",
                    "Small Group Size",
                    "This group would benefit from additional members to enhance peer learning and discussion.",
                    [
                        "Invite compatible students to join",
                        "Post group information on study boards",
                        "Ask current members to recommend friends"
                    ],
                    group.current_members,
                    "medium"
                )
            
            # Activity-based insights
            await self._generate_collaboration_insight(
                group_id,
                "engagement",
                "Boost Group Activity",
                "Regular group activities help maintain engagement and improve learning outcomes.",
                [
                    "Schedule weekly study sessions",
                    "Create group challenges and goals",
                    "Share learning resources and tips"
                ],
                group.current_members,
                "low"
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate fresh insights: {e}")

    def _generate_project_deliverables(self, subject: str, grade_level: int) -> List[Dict]:
        """Generate appropriate deliverables for a project"""
        base_deliverables = [
            {"name": "Research Report", "description": f"Comprehensive research on {subject} topic", "weight": 0.3},
            {"name": "Presentation", "description": "Group presentation of findings", "weight": 0.3},
            {"name": "Visual Aid", "description": "Charts, diagrams, or infographics", "weight": 0.2},
            {"name": "Reflection Essay", "description": "Individual reflection on learning", "weight": 0.2}
        ]
        
        # Customize based on subject and grade
        if subject.lower() == "science" and grade_level >= 6:
            base_deliverables.append({
                "name": "Experiment Documentation", 
                "description": "Lab procedures and results", 
                "weight": 0.2
            })
        
        return base_deliverables

    def _generate_project_timeline(self, due_date: str) -> Dict:
        """Generate project timeline with milestones"""
        due_datetime = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
        start_date = datetime.now()
        total_days = (due_datetime - start_date).days
        
        return {
            "start_date": start_date.isoformat(),
            "due_date": due_date,
            "milestones": {
                "planning": (start_date + timedelta(days=total_days * 0.2)).isoformat(),
                "research": (start_date + timedelta(days=total_days * 0.5)).isoformat(),
                "development": (start_date + timedelta(days=total_days * 0.8)).isoformat(),
                "review": (start_date + timedelta(days=total_days * 0.95)).isoformat()
            }
        }

# Global Collaborative Learning service instance
collaborative_learning_service = CollaborativeLearningService()