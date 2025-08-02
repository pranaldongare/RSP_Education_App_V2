"""
Database Models - RSP Education Agent V2
Phase 6: Production Database Setup

SQLAlchemy models for production deployment with proper relationships
and indexing for optimal performance.
"""
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Float, Boolean, 
    ForeignKey, JSON, Index, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional, Dict, Any, List

Base = declarative_base()

class UserSession(Base):
    """User session management for authentication"""
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True)
    student_id = Column(String(50), ForeignKey("students.id"), nullable=False)
    session_token = Column(String(255), unique=True, nullable=False)
    refresh_token = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now())
    expires_at = Column(DateTime, nullable=False)
    last_accessed = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)
    
    # Session metadata
    user_agent = Column(String(500), nullable=True)
    ip_address = Column(String(45), nullable=True)
    device_type = Column(String(50), nullable=True)
    
    # Relationship
    student = relationship("Student", backref="sessions")
    
    __table_args__ = (
        Index('idx_session_token', 'session_token'),
        Index('idx_session_expires', 'expires_at'),
        Index('idx_session_student', 'student_id'),
    )

class Student(Base):
    """Student profile and preferences with authentication"""
    __tablename__ = "students"
    
    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    grade = Column(String(10), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Authentication and session management
    last_login = Column(DateTime, nullable=True)
    login_count = Column(Integer, default=0)
    
    # Preferences and settings
    preferences = Column(JSON)
    learning_style = Column(String(50))
    preferred_language = Column(String(10), default="en")
    
    # Profile information
    phone = Column(String(20), nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    school = Column(String(100), nullable=True)
    parent_email = Column(String(100), nullable=True)
    
    # Relationships
    learning_sessions = relationship("LearningSession", back_populates="student")
    assessments = relationship("Assessment", back_populates="student")
    learning_profile = relationship("LearningProfile", back_populates="student", uselist=False)
    
    __table_args__ = (
        Index('idx_student_grade', 'grade'),
        Index('idx_student_created', 'created_at'),
    )

class LearningProfile(Base):
    """Adaptive learning profile for each student"""
    __tablename__ = "learning_profiles"
    
    id = Column(Integer, primary_key=True)
    student_id = Column(String(50), ForeignKey("students.id"), unique=True)
    
    # Learning characteristics
    learning_pace = Column(String(20))  # slow, medium, fast
    preferred_difficulty = Column(String(20))  # easy, medium, hard
    skill_levels = Column(JSON)  # Subject-wise skill levels
    learning_patterns = Column(JSON)  # Identified learning patterns
    
    # Performance metrics
    overall_performance = Column(Float, default=0.0)
    consistency_score = Column(Float, default=0.0)
    engagement_level = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    student = relationship("Student", back_populates="learning_profile")
    
    __table_args__ = (
        Index('idx_profile_student', 'student_id'),
        Index('idx_profile_performance', 'overall_performance'),
    )

class Content(Base):
    """Generated educational content"""
    __tablename__ = "content"
    
    id = Column(String(50), primary_key=True)
    title = Column(String(200), nullable=False)
    content_type = Column(String(50), nullable=False)  # lesson, explanation, example
    
    # Educational metadata
    grade = Column(String(10), nullable=False)
    subject = Column(String(50), nullable=False)
    topic = Column(String(100), nullable=False)
    difficulty = Column(String(20), nullable=False)
    
    # Content data
    content_data = Column(JSON)  # Actual content structure
    learning_objectives = Column(JSON)  # List of learning objectives
    estimated_duration = Column(Integer)  # Minutes
    
    # Generation metadata
    generated_by = Column(String(50))  # Agent that generated content
    generation_params = Column(JSON)  # Parameters used for generation
    
    # Quality metrics
    quality_score = Column(Float)
    validation_status = Column(String(20), default="pending")
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    assessments = relationship("Assessment", back_populates="content")
    session_activities = relationship("SessionActivity", back_populates="content")
    
    __table_args__ = (
        Index('idx_content_subject_topic', 'subject', 'topic'),
        Index('idx_content_grade_difficulty', 'grade', 'difficulty'),
        Index('idx_content_created', 'created_at'),
    )

class Assessment(Base):
    """Assessments and their metadata"""
    __tablename__ = "assessments"
    
    id = Column(String(50), primary_key=True)
    title = Column(String(200), nullable=False)
    
    # Educational metadata
    grade = Column(String(10), nullable=False)
    subject = Column(String(50), nullable=False)
    topic = Column(String(100), nullable=False)
    difficulty = Column(String(20), nullable=False)
    
    # Assessment structure
    questions = Column(JSON)  # List of questions with options and answers
    total_marks = Column(Integer, nullable=False)
    estimated_duration = Column(Integer)  # Minutes
    
    # References
    student_id = Column(String(50), ForeignKey("students.id"))
    content_id = Column(String(50), ForeignKey("content.id"), nullable=True)
    
    # Generation metadata
    generated_by = Column(String(50))
    generation_params = Column(JSON)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    student = relationship("Student", back_populates="assessments")
    content = relationship("Content", back_populates="assessments")
    results = relationship("AssessmentResult", back_populates="assessment")
    
    __table_args__ = (
        Index('idx_assessment_student', 'student_id'),
        Index('idx_assessment_subject_topic', 'subject', 'topic'),
        Index('idx_assessment_created', 'created_at'),
    )

class AssessmentResult(Base):
    """Results of completed assessments"""
    __tablename__ = "assessment_results"
    
    id = Column(String(50), primary_key=True)
    assessment_id = Column(String(50), ForeignKey("assessments.id"))
    student_id = Column(String(50), ForeignKey("students.id"))
    
    # Results data
    responses = Column(JSON)  # Student responses
    total_score = Column(Float, nullable=False)
    max_score = Column(Integer, nullable=False)
    percentage = Column(Float, nullable=False)
    
    # Performance metrics
    time_taken = Column(Integer)  # Seconds
    question_results = Column(JSON)  # Detailed question-wise results
    
    # AI Analysis
    performance_insights = Column(JSON)
    improvement_suggestions = Column(JSON)
    skill_analysis = Column(JSON)
    
    # Timestamps
    started_at = Column(DateTime)
    completed_at = Column(DateTime, default=func.now())
    
    # Relationships
    assessment = relationship("Assessment", back_populates="results")
    student = relationship("Student")
    
    __table_args__ = (
        Index('idx_result_student', 'student_id'),
        Index('idx_result_assessment', 'assessment_id'),
        Index('idx_result_completed', 'completed_at'),
        UniqueConstraint('assessment_id', 'student_id', name='uq_assessment_student'),
    )

class LearningSession(Base):
    """Learning session records"""
    __tablename__ = "learning_sessions"
    
    id = Column(String(50), primary_key=True)
    student_id = Column(String(50), ForeignKey("students.id"))
    
    # Session metadata
    session_type = Column(String(50))  # adaptive_learning, assessment, review
    subject = Column(String(50))
    topics_covered = Column(JSON)  # List of topics
    
    # Session metrics
    duration = Column(Integer)  # Minutes
    activities_completed = Column(Integer, default=0)
    overall_performance = Column(Float)
    engagement_score = Column(Float)
    
    # AI Coordinator data
    coordinator_insights = Column(JSON)
    personalization_data = Column(JSON)
    next_recommendations = Column(JSON)
    
    # Timestamps
    started_at = Column(DateTime, default=func.now())
    ended_at = Column(DateTime)
    
    # Relationships
    student = relationship("Student", back_populates="learning_sessions")
    activities = relationship("SessionActivity", back_populates="session")
    
    __table_args__ = (
        Index('idx_session_student', 'student_id'),
        Index('idx_session_started', 'started_at'),
        Index('idx_session_subject', 'subject'),
    )

class SessionActivity(Base):
    """Individual activities within learning sessions"""
    __tablename__ = "session_activities"
    
    id = Column(String(50), primary_key=True)
    session_id = Column(String(50), ForeignKey("learning_sessions.id"))
    content_id = Column(String(50), ForeignKey("content.id"), nullable=True)
    
    # Activity metadata
    activity_type = Column(String(50))  # content_review, practice, assessment
    activity_data = Column(JSON)  # Activity-specific data
    
    # Performance data
    completion_rate = Column(Float)  # 0.0 to 1.0
    time_spent = Column(Integer)  # Seconds
    performance_score = Column(Float)
    difficulty_level = Column(String(20))
    
    # AI Analysis
    outcome_analysis = Column(JSON)
    adaptation_applied = Column(JSON)  # Any adaptive changes made
    
    # Timestamps
    started_at = Column(DateTime, default=func.now())
    completed_at = Column(DateTime)
    
    # Relationships
    session = relationship("LearningSession", back_populates="activities")
    content = relationship("Content", back_populates="session_activities")
    
    __table_args__ = (
        Index('idx_activity_session', 'session_id'),
        Index('idx_activity_content', 'content_id'),
        Index('idx_activity_started', 'started_at'),
    )

class VoiceInteraction(Base):
    """Voice interaction records"""
    __tablename__ = "voice_interactions"
    
    id = Column(String(50), primary_key=True)
    student_id = Column(String(50), ForeignKey("students.id"))
    session_id = Column(String(50), ForeignKey("learning_sessions.id"), nullable=True)
    
    # Voice data
    interaction_type = Column(String(50))  # command, conversation, feedback
    language = Column(String(10))
    
    # Audio processing data
    input_text = Column(Text)  # Transcribed text
    response_text = Column(Text)  # AI response
    confidence_score = Column(Float)
    processing_time = Column(Float)  # Seconds
    
    # Context and analysis
    context_data = Column(JSON)
    intent_analysis = Column(JSON)
    emotion_analysis = Column(JSON)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    student = relationship("Student")
    session = relationship("LearningSession")
    
    __table_args__ = (
        Index('idx_voice_student', 'student_id'),
        Index('idx_voice_session', 'session_id'),
        Index('idx_voice_created', 'created_at'),
    )

class SystemMetrics(Base):
    """System performance and usage metrics"""
    __tablename__ = "system_metrics"
    
    id = Column(Integer, primary_key=True)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float, nullable=False)
    metric_data = Column(JSON)  # Additional metric data
    
    # Context
    component = Column(String(50))  # Which AI agent or system component
    session_id = Column(String(50), nullable=True)
    student_id = Column(String(50), nullable=True)
    
    # Timestamp
    recorded_at = Column(DateTime, default=func.now())
    
    __table_args__ = (
        Index('idx_metrics_name_component', 'metric_name', 'component'),
        Index('idx_metrics_recorded', 'recorded_at'),
    )