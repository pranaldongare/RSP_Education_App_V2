"""
Offline Cache Service - RSP Education Agent V2 Phase 1.4
Content caching for mobile users with offline support and smart synchronization
"""

import asyncio
import json
import logging
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, asdict
from enum import Enum
import sqlite3
import os
from pathlib import Path

from sqlalchemy.orm import Session
from database.models import Student
from core.exceptions import AgentException
from services.ai_companion_service import ai_companion_agent
from services.enhanced_analytics_service import enhanced_analytics_service

logger = logging.getLogger(__name__)

class CacheType(Enum):
    LESSON_PLAN = "lesson_plan"
    ASSESSMENT = "assessment"
    CONTENT_MATERIAL = "content_material"
    USER_PROGRESS = "user_progress"
    COMPANION_DATA = "companion_data"
    ANALYTICS_DATA = "analytics_data"
    SETTINGS = "settings"

class SyncStatus(Enum):
    SYNCED = "synced"
    PENDING_UPLOAD = "pending_upload"
    PENDING_DOWNLOAD = "pending_download"
    CONFLICT = "conflict"
    ERROR = "error"

@dataclass
class CachedContent:
    """Cached content item with metadata"""
    content_id: str
    content_type: str  # CacheType
    data: Dict
    created_at: str  # ISO timestamp
    updated_at: str  # ISO timestamp
    expires_at: Optional[str]  # ISO timestamp
    sync_status: str  # SyncStatus
    version: int
    checksum: str
    size_bytes: int
    priority: int  # 1-10, higher = more important
    access_count: int
    last_accessed: str  # ISO timestamp

@dataclass
class SyncOperation:
    """Synchronization operation"""
    operation_id: str
    operation_type: str  # upload, download, delete
    content_id: str
    status: str  # pending, in_progress, completed, failed
    created_at: str
    completed_at: Optional[str]
    error_message: Optional[str]
    retry_count: int
    metadata: Dict

@dataclass
class OfflineCapabilities:
    """Offline capabilities for a student"""
    student_id: str
    total_cached_items: int
    total_cache_size: int
    cached_subjects: List[str]
    offline_lesson_plans: int
    offline_assessments: int
    offline_content_materials: int
    last_sync: Optional[str]
    sync_conflicts: int
    available_offline_hours: float  # Estimated hours of offline content

class OfflineCacheService:
    """Offline Cache Service with smart content caching and synchronization"""
    
    def __init__(self, cache_dir: str = "cache", db_path: str = "cache/offline_cache.db"):
        self.logger = logging.getLogger(f"{__name__}.OfflineCacheService")
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.db_path = db_path
        
        # Initialize SQLite database for cache metadata
        self._init_cache_database()
        
        # Cache configuration
        self.max_cache_size = 500 * 1024 * 1024  # 500MB max cache
        self.default_expiry_hours = 72  # 3 days default expiry
        self.sync_batch_size = 20
        self.max_retry_attempts = 3
        
        # In-memory cache for frequently accessed items
        self.memory_cache: Dict[str, CachedContent] = {}
        self.sync_queue: List[SyncOperation] = []
        
    def _init_cache_database(self):
        """Initialize SQLite database for cache metadata"""
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS cached_content (
                        content_id TEXT PRIMARY KEY,
                        student_id TEXT NOT NULL,
                        content_type TEXT NOT NULL,
                        data_json TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL,
                        expires_at TEXT,
                        sync_status TEXT NOT NULL,
                        version INTEGER NOT NULL,
                        checksum TEXT NOT NULL,
                        size_bytes INTEGER NOT NULL,
                        priority INTEGER NOT NULL,
                        access_count INTEGER DEFAULT 0,
                        last_accessed TEXT NOT NULL
                    )
                """)
                
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS sync_operations (
                        operation_id TEXT PRIMARY KEY,
                        student_id TEXT NOT NULL,
                        operation_type TEXT NOT NULL,
                        content_id TEXT NOT NULL,
                        status TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        completed_at TEXT,
                        error_message TEXT,
                        retry_count INTEGER DEFAULT 0,
                        metadata_json TEXT
                    )
                """)
                
                # Create indexes for better performance
                conn.execute("CREATE INDEX IF NOT EXISTS idx_student_content ON cached_content(student_id, content_type)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_sync_status ON cached_content(sync_status)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_expires_at ON cached_content(expires_at)")
                
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"Failed to initialize cache database: {e}")
            raise

    async def cache_content(
        self, 
        student_id: str, 
        content_type: CacheType, 
        content_data: Dict,
        priority: int = 5,
        expiry_hours: Optional[int] = None
    ) -> str:
        """Cache content for offline access"""
        try:
            # Generate content ID based on content and student
            content_id = self._generate_content_id(student_id, content_type.value, content_data)
            
            # Calculate expiry time
            expiry_hours = expiry_hours or self.default_expiry_hours
            expires_at = datetime.now() + timedelta(hours=expiry_hours)
            
            # Calculate checksum and size
            data_json = json.dumps(content_data, sort_keys=True)
            checksum = hashlib.md5(data_json.encode()).hexdigest()
            size_bytes = len(data_json.encode())
            
            # Create cached content object
            cached_content = CachedContent(
                content_id=content_id,
                content_type=content_type.value,
                data=content_data,
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat(),
                expires_at=expires_at.isoformat(),
                sync_status=SyncStatus.SYNCED.value,
                version=1,
                checksum=checksum,
                size_bytes=size_bytes,
                priority=priority,
                access_count=0,
                last_accessed=datetime.now().isoformat()
            )
            
            # Check cache size limits
            await self._manage_cache_size(student_id, size_bytes)
            
            # Store in database
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO cached_content 
                    (content_id, student_id, content_type, data_json, created_at, updated_at, 
                     expires_at, sync_status, version, checksum, size_bytes, priority, 
                     access_count, last_accessed)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    content_id, student_id, content_type.value, data_json,
                    cached_content.created_at, cached_content.updated_at, cached_content.expires_at,
                    cached_content.sync_status, cached_content.version, cached_content.checksum,
                    cached_content.size_bytes, cached_content.priority, cached_content.access_count,
                    cached_content.last_accessed
                ))
                conn.commit()
            
            # Add to memory cache if high priority
            if priority >= 8:
                self.memory_cache[content_id] = cached_content
            
            self.logger.info(f"Cached content {content_id} for student {student_id}")
            return content_id
            
        except Exception as e:
            self.logger.error(f"Failed to cache content for {student_id}: {e}")
            raise AgentException(f"Cache operation failed: {e}")

    async def get_cached_content(self, student_id: str, content_id: str) -> Optional[CachedContent]:
        """Retrieve cached content by ID"""
        try:
            # Check memory cache first
            if content_id in self.memory_cache:
                cached_content = self.memory_cache[content_id]
                await self._update_access_stats(content_id)
                return cached_content
            
            # Check database
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT * FROM cached_content 
                    WHERE content_id = ? AND student_id = ?
                """, (content_id, student_id))
                
                row = cursor.fetchone()
                if not row:
                    return None
                
                # Check if expired
                if row[6]:  # expires_at
                    expires_at = datetime.fromisoformat(row[6])
                    if expires_at < datetime.now():
                        # Content expired, remove it
                        await self._remove_expired_content(content_id)
                        return None
                
                # Create CachedContent object
                cached_content = CachedContent(
                    content_id=row[0],
                    content_type=row[2],
                    data=json.loads(row[3]),
                    created_at=row[4],
                    updated_at=row[5],
                    expires_at=row[6],
                    sync_status=row[7],
                    version=row[8],
                    checksum=row[9],
                    size_bytes=row[10],
                    priority=row[11],
                    access_count=row[12],
                    last_accessed=row[13]
                )
                
                # Update access stats
                await self._update_access_stats(content_id)
                
                # Add to memory cache if frequently accessed
                if cached_content.access_count > 5:
                    self.memory_cache[content_id] = cached_content
                
                return cached_content
                
        except Exception as e:
            self.logger.error(f"Failed to get cached content {content_id}: {e}")
            return None

    async def get_offline_content_by_type(self, student_id: str, content_type: CacheType, limit: int = 50) -> List[CachedContent]:
        """Get all cached content of a specific type for offline access"""
        try:
            cached_items = []
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT * FROM cached_content 
                    WHERE student_id = ? AND content_type = ?
                    AND (expires_at IS NULL OR expires_at > ?)
                    ORDER BY priority DESC, last_accessed DESC
                    LIMIT ?
                """, (student_id, content_type.value, datetime.now().isoformat(), limit))
                
                for row in cursor.fetchall():
                    cached_content = CachedContent(
                        content_id=row[0],
                        content_type=row[2],
                        data=json.loads(row[3]),
                        created_at=row[4],
                        updated_at=row[5],
                        expires_at=row[6],
                        sync_status=row[7],
                        version=row[8],
                        checksum=row[9],
                        size_bytes=row[10],
                        priority=row[11],
                        access_count=row[12],
                        last_accessed=row[13]
                    )
                    cached_items.append(cached_content)
            
            return cached_items
            
        except Exception as e:
            self.logger.error(f"Failed to get offline content for {student_id}: {e}")
            return []

    async def cache_lesson_plan(self, student_id: str, lesson_data: Dict) -> str:
        """Cache a lesson plan for offline access"""
        return await self.cache_content(
            student_id=student_id,
            content_type=CacheType.LESSON_PLAN,
            content_data=lesson_data,
            priority=8,  # High priority for lesson plans
            expiry_hours=168  # 1 week expiry
        )

    async def cache_assessment(self, student_id: str, assessment_data: Dict) -> str:
        """Cache an assessment for offline access"""
        return await self.cache_content(
            student_id=student_id,
            content_type=CacheType.ASSESSMENT,
            content_data=assessment_data,
            priority=9,  # Very high priority for assessments
            expiry_hours=72  # 3 days expiry
        )

    async def cache_learning_materials(self, student_id: str, materials_data: Dict) -> str:
        """Cache learning materials for offline access"""
        return await self.cache_content(
            student_id=student_id,
            content_type=CacheType.CONTENT_MATERIAL,
            content_data=materials_data,
            priority=7,  # Good priority for materials
            expiry_hours=336  # 2 weeks expiry
        )

    async def sync_offline_progress(self, student_id: str, progress_data: Dict) -> None:
        """Sync offline progress when connection is available"""
        try:
            # Cache the progress data with pending upload status
            content_id = await self.cache_content(
                student_id=student_id,
                content_type=CacheType.USER_PROGRESS,
                content_data=progress_data,
                priority=10  # Highest priority for progress data
            )
            
            # Mark for upload sync
            await self._mark_for_sync(content_id, "upload")
            
            # Try to sync immediately if online
            await self._attempt_sync_operation(student_id)
            
        except Exception as e:
            self.logger.error(f"Failed to sync offline progress for {student_id}: {e}")

    async def get_offline_capabilities(self, student_id: str) -> OfflineCapabilities:
        """Get offline capabilities summary for a student"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Get total cached items and size
                cursor = conn.execute("""
                    SELECT COUNT(*), SUM(size_bytes) FROM cached_content 
                    WHERE student_id = ? AND (expires_at IS NULL OR expires_at > ?)
                """, (student_id, datetime.now().isoformat()))
                
                total_items, total_size = cursor.fetchone()
                total_items = total_items or 0
                total_size = total_size or 0
                
                # Get cached subjects
                cursor = conn.execute("""
                    SELECT DISTINCT data_json FROM cached_content 
                    WHERE student_id = ? AND content_type IN (?, ?, ?)
                    AND (expires_at IS NULL OR expires_at > ?)
                """, (student_id, CacheType.LESSON_PLAN.value, CacheType.ASSESSMENT.value, 
                     CacheType.CONTENT_MATERIAL.value, datetime.now().isoformat()))
                
                subjects = set()
                for (data_json,) in cursor.fetchall():
                    try:
                        data = json.loads(data_json)
                        if 'subject' in data:
                            subjects.add(data['subject'])
                    except:
                        continue
                
                # Get content type counts
                cursor = conn.execute("""
                    SELECT content_type, COUNT(*) FROM cached_content 
                    WHERE student_id = ? AND (expires_at IS NULL OR expires_at > ?)
                    GROUP BY content_type
                """, (student_id, datetime.now().isoformat()))
                
                type_counts = dict(cursor.fetchall())
                
                # Get last sync time
                cursor = conn.execute("""
                    SELECT MAX(completed_at) FROM sync_operations 
                    WHERE student_id = ? AND status = 'completed'
                """, (student_id,))
                
                last_sync = cursor.fetchone()[0]
                
                # Get sync conflicts
                cursor = conn.execute("""
                    SELECT COUNT(*) FROM cached_content 
                    WHERE student_id = ? AND sync_status = ?
                """, (student_id, SyncStatus.CONFLICT.value))
                
                sync_conflicts = cursor.fetchone()[0]
                
                # Estimate available offline hours (rough calculation)
                lesson_plans = type_counts.get(CacheType.LESSON_PLAN.value, 0)
                assessments = type_counts.get(CacheType.ASSESSMENT.value, 0)
                materials = type_counts.get(CacheType.CONTENT_MATERIAL.value, 0)
                
                # Assume 30 min per lesson, 20 min per assessment, 15 min per material
                offline_hours = (lesson_plans * 0.5) + (assessments * 0.33) + (materials * 0.25)
                
                return OfflineCapabilities(
                    student_id=student_id,
                    total_cached_items=total_items,
                    total_cache_size=total_size,
                    cached_subjects=list(subjects),
                    offline_lesson_plans=type_counts.get(CacheType.LESSON_PLAN.value, 0),
                    offline_assessments=type_counts.get(CacheType.ASSESSMENT.value, 0),
                    offline_content_materials=type_counts.get(CacheType.CONTENT_MATERIAL.value, 0),
                    last_sync=last_sync,
                    sync_conflicts=sync_conflicts,
                    available_offline_hours=round(offline_hours, 1)
                )
                
        except Exception as e:
            self.logger.error(f"Failed to get offline capabilities for {student_id}: {e}")
            return OfflineCapabilities(
                student_id=student_id,
                total_cached_items=0,
                total_cache_size=0,
                cached_subjects=[],
                offline_lesson_plans=0,
                offline_assessments=0,
                offline_content_materials=0,
                last_sync=None,
                sync_conflicts=0,
                available_offline_hours=0.0
            )

    async def smart_cache_preload(self, student_id: str, subjects: List[str] = None) -> Dict[str, int]:
        """Smart preloading of content based on student patterns"""
        try:
            # Get learning patterns from analytics
            patterns = await enhanced_analytics_service.track_learning_patterns(student_id)
            
            # Get companion context for personalization
            companion_context = ai_companion_agent.get_companion_context_for_agent(student_id, "offline_cache")
            
            # Determine what to cache based on patterns
            cache_counts = {
                "lesson_plans": 0,
                "assessments": 0,
                "materials": 0
            }
            
            # Use provided subjects or preferred subjects from patterns
            target_subjects = subjects or patterns.preferred_subjects[:3] or ["Math", "Science", "English"]
            
            # Cache lesson plans for preferred subjects
            for subject in target_subjects:
                # Create sample lesson plan (in real implementation, this would fetch from content service)
                lesson_data = {
                    "subject": subject,
                    "title": f"Offline {subject} Lesson",
                    "content": f"Comprehensive {subject} lesson for offline learning",
                    "difficulty": patterns.difficulty_preference,
                    "duration_minutes": patterns.optimal_session_length,
                    "activities": ["reading", "practice", "assessment"],
                    "cached_for_offline": True,
                    "companion_enhanced": True
                }
                
                await self.cache_lesson_plan(student_id, lesson_data)
                cache_counts["lesson_plans"] += 1
                
                # Cache assessment for this subject
                assessment_data = {
                    "subject": subject,
                    "title": f"Offline {subject} Assessment",
                    "questions": [
                        {
                            "id": f"q_{i}",
                            "question": f"{subject} practice question {i}",
                            "options": ["A", "B", "C", "D"],
                            "correct_answer": "A",
                            "difficulty": patterns.difficulty_preference
                        }
                        for i in range(5)  # 5 questions per assessment
                    ],
                    "time_limit_minutes": 15,
                    "cached_for_offline": True
                }
                
                await self.cache_assessment(student_id, assessment_data)
                cache_counts["assessments"] += 1
                
                # Cache learning materials
                materials_data = {
                    "subject": subject,
                    "title": f"{subject} Study Materials",
                    "materials": [
                        {"type": "notes", "content": f"{subject} study notes"},
                        {"type": "examples", "content": f"{subject} worked examples"},
                        {"type": "practice", "content": f"{subject} practice problems"}
                    ],
                    "cached_for_offline": True
                }
                
                await self.cache_learning_materials(student_id, materials_data)
                cache_counts["materials"] += 1
            
            self.logger.info(f"Smart cache preload completed for {student_id}: {cache_counts}")
            return cache_counts
            
        except Exception as e:
            self.logger.error(f"Failed smart cache preload for {student_id}: {e}")
            return {"lesson_plans": 0, "assessments": 0, "materials": 0}

    def _generate_content_id(self, student_id: str, content_type: str, content_data: Dict) -> str:
        """Generate unique content ID"""
        content_hash = hashlib.md5(json.dumps(content_data, sort_keys=True).encode()).hexdigest()
        return f"{student_id}_{content_type}_{content_hash[:12]}"

    async def _manage_cache_size(self, student_id: str, new_content_size: int) -> None:
        """Manage cache size by removing old/low-priority content if needed"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Get current cache size
                cursor = conn.execute("""
                    SELECT SUM(size_bytes) FROM cached_content WHERE student_id = ?
                """, (student_id,))
                
                current_size = cursor.fetchone()[0] or 0
                
                # Check if we need to free space
                if current_size + new_content_size > self.max_cache_size:
                    # Remove expired content first
                    conn.execute("""
                        DELETE FROM cached_content 
                        WHERE student_id = ? AND expires_at < ?
                    """, (student_id, datetime.now().isoformat()))
                    
                    # If still need space, remove low-priority, least-accessed content
                    space_needed = (current_size + new_content_size) - self.max_cache_size
                    
                    cursor = conn.execute("""
                        SELECT content_id, size_bytes FROM cached_content 
                        WHERE student_id = ? 
                        ORDER BY priority ASC, access_count ASC, last_accessed ASC
                    """, (student_id,))
                    
                    removed_size = 0
                    for content_id, size_bytes in cursor.fetchall():
                        if removed_size >= space_needed:
                            break
                        
                        conn.execute("DELETE FROM cached_content WHERE content_id = ?", (content_id,))
                        removed_size += size_bytes
                        
                        # Remove from memory cache too
                        if content_id in self.memory_cache:
                            del self.memory_cache[content_id]
                
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"Failed to manage cache size: {e}")

    async def _update_access_stats(self, content_id: str) -> None:
        """Update access statistics for content"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    UPDATE cached_content 
                    SET access_count = access_count + 1, last_accessed = ?
                    WHERE content_id = ?
                """, (datetime.now().isoformat(), content_id))
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"Failed to update access stats for {content_id}: {e}")

    async def _remove_expired_content(self, content_id: str) -> None:
        """Remove expired content from cache"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("DELETE FROM cached_content WHERE content_id = ?", (content_id,))
                conn.commit()
            
            # Remove from memory cache
            if content_id in self.memory_cache:
                del self.memory_cache[content_id]
                
        except Exception as e:
            self.logger.error(f"Failed to remove expired content {content_id}: {e}")

    async def _mark_for_sync(self, content_id: str, operation_type: str) -> None:
        """Mark content for synchronization"""
        try:
            operation_id = f"sync_{content_id}_{int(datetime.now().timestamp())}"
            
            with sqlite3.connect(self.db_path) as conn:
                # Get student_id for this content
                cursor = conn.execute("SELECT student_id FROM cached_content WHERE content_id = ?", (content_id,))
                row = cursor.fetchone()
                if not row:
                    return
                
                student_id = row[0]
                
                # Create sync operation
                conn.execute("""
                    INSERT INTO sync_operations 
                    (operation_id, student_id, operation_type, content_id, status, created_at, metadata_json)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    operation_id, student_id, operation_type, content_id, "pending",
                    datetime.now().isoformat(), json.dumps({})
                ))
                
                # Update content sync status
                if operation_type == "upload":
                    sync_status = SyncStatus.PENDING_UPLOAD.value
                else:
                    sync_status = SyncStatus.PENDING_DOWNLOAD.value
                
                conn.execute("""
                    UPDATE cached_content SET sync_status = ? WHERE content_id = ?
                """, (sync_status, content_id))
                
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"Failed to mark {content_id} for sync: {e}")

    async def _attempt_sync_operation(self, student_id: str) -> None:
        """Attempt to sync pending operations"""
        # This is a placeholder for actual sync implementation
        # In a real system, this would connect to the server and sync data
        self.logger.info(f"Sync operations attempted for student {student_id}")

# Global Offline Cache service instance
offline_cache_service = OfflineCacheService()