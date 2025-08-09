"""
Advanced Gamification Service - RSP Education Agent V2 Phase 2.3
Quest-based learning, virtual rewards system, and social competitions with AI-enhanced progression
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

logger = logging.getLogger(__name__)

class QuestType(Enum):
    LEARNING_ADVENTURE = "learning_adventure"
    SKILL_CHALLENGE = "skill_challenge"
    EXPLORATION_QUEST = "exploration_quest"
    COLLABORATIVE_MISSION = "collaborative_mission"
    DAILY_QUEST = "daily_quest"
    WEEKLY_CHALLENGE = "weekly_challenge"

class QuestStatus(Enum):
    AVAILABLE = "available"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    LOCKED = "locked"
    EXPIRED = "expired"

class QuestDifficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"

class RewardType(Enum):
    BADGE = "badge"
    TROPHY = "trophy"
    COLLECTIBLE_ITEM = "collectible_item"
    VIRTUAL_CURRENCY = "virtual_currency"
    AVATAR_CUSTOMIZATION = "avatar_customization"
    SPECIAL_ABILITY = "special_ability"

class CompetitionType(Enum):
    INDIVIDUAL_LEADERBOARD = "individual_leaderboard"
    CLASS_COMPETITION = "class_competition"
    SCHOOL_TOURNAMENT = "school_tournament"
    SUBJECT_MASTERY = "subject_mastery"
    LEARNING_STREAK = "learning_streak"

@dataclass
class Quest:
    """Quest with storyline, objectives, and rewards"""
    quest_id: str
    quest_name: str
    quest_type: str  # QuestType
    difficulty: str  # QuestDifficulty
    subject: str
    grade_range: List[int]
    storyline: str
    description: str
    objectives: List[Dict]  # [{"objective": str, "completed": bool, "progress": int, "target": int}]
    prerequisites: List[str]  # quest_ids that must be completed first
    rewards: List[Dict]  # [{"type": RewardType, "item": str, "quantity": int, "rarity": str}]
    experience_points: int
    estimated_duration_minutes: int
    character_context: Dict  # storyline character and setting information
    status: str  # QuestStatus
    progress_percentage: float
    started_at: Optional[str]
    completed_at: Optional[str]
    expires_at: Optional[str]
    ai_hints: List[str]
    adaptive_difficulty: bool

@dataclass
class VirtualReward:
    """Virtual reward item with rarity and special properties"""
    reward_id: str
    reward_name: str
    reward_type: str  # RewardType
    rarity: str  # common, uncommon, rare, epic, legendary
    description: str
    visual_representation: str  # emoji or icon identifier
    special_properties: List[str]
    unlock_requirements: Dict
    student_id: str
    earned_at: str
    quest_source: Optional[str]
    competition_source: Optional[str]
    display_order: int
    equipped: bool

@dataclass
class LearningStreak:
    """Learning streak tracking with multipliers and bonuses"""
    streak_id: str
    student_id: str
    current_streak: int
    longest_streak: int
    streak_type: str  # daily, weekly, subject_specific
    subject: Optional[str]
    started_date: str
    last_activity_date: str
    streak_multiplier: float
    bonus_rewards: List[str]
    milestone_rewards: Dict  # {streak_length: reward_info}
    is_active: bool

@dataclass
class Competition:
    """Social learning competition with rankings and prizes"""
    competition_id: str
    competition_name: str
    competition_type: str  # CompetitionType
    description: str
    subject: Optional[str]
    grade_range: List[int]
    participants: List[str]  # student_ids
    start_date: str
    end_date: str
    ranking_criteria: str  # points, accuracy, speed, completion_rate
    current_rankings: List[Dict]  # [{"student_id": str, "score": int, "rank": int}]
    prizes: List[Dict]  # [{"rank_range": [int, int], "reward": Dict}]
    is_active: bool
    registration_deadline: str
    min_participants: int
    max_participants: int

@dataclass
class CharacterProgression:
    """Student's character/avatar progression and customization"""
    character_id: str
    student_id: str
    character_name: str
    character_type: str  # explorer, scholar, warrior, sage, artist
    level: int
    experience_points: int
    next_level_xp: int
    appearance: Dict  # customization options
    abilities: List[Dict]  # special learning abilities unlocked
    achievements: List[str]
    personality_traits: List[str]
    favorite_subjects: List[str]
    learning_style_bonuses: Dict
    companion_relationship: str  # with AI companion
    last_adventure: str
    created_at: str
    updated_at: str

@dataclass
class SocialLeaderboard:
    """Social leaderboard for various competition types"""
    leaderboard_id: str
    leaderboard_name: str
    leaderboard_type: str  # CompetitionType
    scope: str  # global, school, class, grade
    subject: Optional[str]
    time_period: str  # daily, weekly, monthly, all_time
    rankings: List[Dict]  # [{"student_id": str, "student_name": str, "score": int, "rank": int, "change": int}]
    last_updated: str
    update_frequency: str
    featured_achievement: Optional[str]
    bonus_multipliers: Dict

class AdvancedGamificationService:
    """Advanced Gamification Service with quest-based learning and social competitions"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.AdvancedGamificationService")
        
        # In-memory storage for advanced gamification (in production, use proper database)
        self.quests: Dict[str, Quest] = {}
        self.student_quests: Dict[str, List[str]] = {}  # student_id -> [quest_ids]
        self.virtual_rewards: Dict[str, VirtualReward] = {}
        self.student_rewards: Dict[str, List[str]] = {}  # student_id -> [reward_ids]
        self.learning_streaks: Dict[str, LearningStreak] = {}
        self.competitions: Dict[str, Competition] = {}
        self.character_progressions: Dict[str, CharacterProgression] = {}
        self.leaderboards: Dict[str, SocialLeaderboard] = {}
        
        # Initialize default quests and rewards
        self._initialize_default_content()

    async def create_quest(
        self, 
        quest_name: str, 
        quest_type: str, 
        difficulty: str,
        subject: str,
        grade_range: List[int],
        storyline: str,
        objectives: List[Dict],
        rewards: List[Dict],
        estimated_duration: int = 30
    ) -> Quest:
        """Create a new quest with AI-enhanced storyline and objectives"""
        try:
            quest_id = str(uuid.uuid4())
            
            # AI-enhanced quest creation
            character_context = await self._generate_quest_context(subject, grade_range[0], storyline)
            ai_hints = await self._generate_quest_hints(objectives, difficulty)
            
            quest = Quest(
                quest_id=quest_id,
                quest_name=quest_name,
                quest_type=quest_type,
                difficulty=difficulty,
                subject=subject,
                grade_range=grade_range,
                storyline=storyline,
                description=f"Embark on {quest_name} - {storyline}",
                objectives=objectives,
                prerequisites=[],
                rewards=rewards,
                experience_points=self._calculate_quest_xp(difficulty, len(objectives)),
                estimated_duration_minutes=estimated_duration,
                character_context=character_context,
                status=QuestStatus.AVAILABLE.value,
                progress_percentage=0.0,
                started_at=None,
                completed_at=None,
                expires_at=None,
                ai_hints=ai_hints,
                adaptive_difficulty=True
            )
            
            self.quests[quest_id] = quest
            self.logger.info(f"Created quest {quest_id}: {quest_name}")
            return quest
            
        except Exception as e:
            self.logger.error(f"Failed to create quest: {e}")
            raise AgentException(f"Quest creation failed: {e}")

    async def start_quest(self, student_id: str, quest_id: str) -> bool:
        """Start a quest for a student with AI companion integration"""
        try:
            if quest_id not in self.quests:
                return False
            
            quest = self.quests[quest_id]
            
            # Check prerequisites
            if not await self._check_quest_prerequisites(student_id, quest.prerequisites):
                return False
            
            # Update quest status
            quest.status = QuestStatus.IN_PROGRESS.value
            quest.started_at = datetime.now().isoformat()
            
            # Add to student's active quests
            if student_id not in self.student_quests:
                self.student_quests[student_id] = []
            self.student_quests[student_id].append(quest_id)
            
            # AI companion interaction
            await ai_companion_agent.update_companion_from_agent_interaction(
                student_id=student_id,
                agent_name="advanced_gamification",
                interaction_data={
                    "quest_started": quest.quest_name,
                    "quest_type": quest.quest_type,
                    "difficulty": quest.difficulty,
                    "subject": quest.subject,
                    "storyline": quest.storyline[:100] + "..."
                }
            )
            
            self.logger.info(f"Student {student_id} started quest {quest_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start quest: {e}")
            return False

    async def update_quest_progress(self, student_id: str, quest_id: str, objective_index: int, progress_amount: int = 1) -> Dict:
        """Update quest objective progress with AI-powered feedback"""
        try:
            if quest_id not in self.quests:
                return {"success": False, "error": "Quest not found"}
            
            quest = self.quests[quest_id]
            
            if objective_index >= len(quest.objectives):
                return {"success": False, "error": "Invalid objective index"}
            
            # Update objective progress
            objective = quest.objectives[objective_index]
            objective["progress"] = min(objective["progress"] + progress_amount, objective["target"])
            objective["completed"] = objective["progress"] >= objective["target"]
            
            # Calculate overall quest progress
            completed_objectives = sum(1 for obj in quest.objectives if obj["completed"])
            quest.progress_percentage = (completed_objectives / len(quest.objectives)) * 100
            
            # Check if quest is completed
            if quest.progress_percentage >= 100:
                return await self._complete_quest(student_id, quest_id)
            
            # Generate AI encouragement
            encouragement = await self._generate_progress_encouragement(student_id, quest, objective_index)
            
            return {
                "success": True,
                "progress_percentage": quest.progress_percentage,
                "objective_completed": objective["completed"],
                "quest_completed": False,
                "encouragement": encouragement,
                "next_hint": quest.ai_hints[min(objective_index + 1, len(quest.ai_hints) - 1)] if quest.ai_hints else None
            }
            
        except Exception as e:
            self.logger.error(f"Failed to update quest progress: {e}")
            return {"success": False, "error": str(e)}

    async def award_virtual_reward(self, student_id: str, reward_type: str, reward_name: str, source_quest: str = None) -> VirtualReward:
        """Award virtual reward to student with rarity and special properties"""
        try:
            reward_id = str(uuid.uuid4())
            
            # Determine rarity based on achievement
            rarity = self._determine_reward_rarity(reward_type, source_quest)
            
            reward = VirtualReward(
                reward_id=reward_id,
                reward_name=reward_name,
                reward_type=reward_type,
                rarity=rarity,
                description=self._generate_reward_description(reward_name, reward_type),
                visual_representation=self._get_reward_visual(reward_type),
                special_properties=self._get_special_properties(reward_type, rarity),
                unlock_requirements={},
                student_id=student_id,
                earned_at=datetime.now().isoformat(),
                quest_source=source_quest,
                competition_source=None,
                display_order=len(self.student_rewards.get(student_id, [])),
                equipped=False
            )
            
            self.virtual_rewards[reward_id] = reward
            
            if student_id not in self.student_rewards:
                self.student_rewards[student_id] = []
            self.student_rewards[student_id].append(reward_id)
            
            self.logger.info(f"Awarded {reward_name} ({rarity}) to student {student_id}")
            return reward
            
        except Exception as e:
            self.logger.error(f"Failed to award virtual reward: {e}")
            raise AgentException(f"Reward awarding failed: {e}")

    async def create_competition(
        self,
        competition_name: str,
        competition_type: str,
        subject: str,
        grade_range: List[int],
        duration_days: int = 7
    ) -> Competition:
        """Create social learning competition with rankings and prizes"""
        try:
            competition_id = str(uuid.uuid4())
            start_date = datetime.now()
            end_date = start_date + timedelta(days=duration_days)
            
            competition = Competition(
                competition_id=competition_id,
                competition_name=competition_name,
                competition_type=competition_type,
                description=f"Compete in {competition_name} and showcase your {subject} skills!",
                subject=subject,
                grade_range=grade_range,
                participants=[],
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat(),
                ranking_criteria="points",
                current_rankings=[],
                prizes=self._generate_competition_prizes(),
                is_active=True,
                registration_deadline=(start_date + timedelta(days=1)).isoformat(),
                min_participants=5,
                max_participants=100
            )
            
            self.competitions[competition_id] = competition
            self.logger.info(f"Created competition {competition_id}: {competition_name}")
            return competition
            
        except Exception as e:
            self.logger.error(f"Failed to create competition: {e}")
            raise AgentException(f"Competition creation failed: {e}")

    async def get_student_character_progression(self, student_id: str) -> CharacterProgression:
        """Get or create student's character progression"""
        try:
            if student_id not in self.character_progressions:
                # Create new character progression
                character = await self._create_character_progression(student_id)
                self.character_progressions[student_id] = character
            
            return self.character_progressions[student_id]
            
        except Exception as e:
            self.logger.error(f"Failed to get character progression: {e}")
            raise AgentException(f"Character progression retrieval failed: {e}")

    async def get_available_quests(self, student_id: str) -> List[Quest]:
        """Get available quests for student based on level and prerequisites"""
        try:
            character = await self.get_student_character_progression(student_id)
            available_quests = []
            
            for quest in self.quests.values():
                if quest.status == QuestStatus.AVAILABLE.value:
                    # Check grade level
                    if character.level >= quest.grade_range[0] and character.level <= quest.grade_range[1]:
                        # Check prerequisites
                        if await self._check_quest_prerequisites(student_id, quest.prerequisites):
                            available_quests.append(quest)
            
            # Sort by difficulty and relevance
            available_quests.sort(key=lambda q: (q.difficulty, q.experience_points))
            
            return available_quests[:10]  # Return top 10
            
        except Exception as e:
            self.logger.error(f"Failed to get available quests: {e}")
            return []

    async def get_student_leaderboard_position(self, student_id: str, leaderboard_type: str) -> Dict:
        """Get student's position on various leaderboards"""
        try:
            leaderboard_positions = {}
            
            for leaderboard in self.leaderboards.values():
                if leaderboard.leaderboard_type == leaderboard_type:
                    for ranking in leaderboard.rankings:
                        if ranking["student_id"] == student_id:
                            leaderboard_positions[leaderboard.leaderboard_id] = {
                                "name": leaderboard.leaderboard_name,
                                "rank": ranking["rank"],
                                "score": ranking["score"],
                                "total_participants": len(leaderboard.rankings),
                                "percentile": round((1 - (ranking["rank"] - 1) / len(leaderboard.rankings)) * 100, 1)
                            }
            
            return {
                "student_id": student_id,
                "leaderboard_positions": leaderboard_positions,
                "overall_rank_average": statistics.mean([pos["rank"] for pos in leaderboard_positions.values()]) if leaderboard_positions else 0
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get leaderboard position: {e}")
            return {"student_id": student_id, "leaderboard_positions": {}, "overall_rank_average": 0}

    # Private helper methods
    
    async def _complete_quest(self, student_id: str, quest_id: str) -> Dict:
        """Complete quest and award rewards"""
        quest = self.quests[quest_id]
        quest.status = QuestStatus.COMPLETED.value
        quest.completed_at = datetime.now().isoformat()
        quest.progress_percentage = 100.0
        
        # Award XP and rewards
        character = await self.get_student_character_progression(student_id)
        character.experience_points += quest.experience_points
        
        # Level up check
        level_up = await self._check_level_up(character)
        
        # Award quest rewards
        awarded_rewards = []
        for reward_info in quest.rewards:
            reward = await self.award_virtual_reward(
                student_id=student_id,
                reward_type=reward_info["type"],
                reward_name=reward_info["item"],
                source_quest=quest_id
            )
            awarded_rewards.append(reward)
        
        return {
            "success": True,
            "quest_completed": True,
            "xp_gained": quest.experience_points,
            "level_up": level_up,
            "rewards_earned": len(awarded_rewards),
            "completion_message": f"🎉 Quest Complete! You've finished {quest.quest_name} and gained {quest.experience_points} XP!"
        }

    async def _generate_quest_context(self, subject: str, grade: int, storyline: str) -> Dict:
        """Generate quest context with AI companion integration"""
        contexts = {
            "Math": {
                "character": "Professor Numbers",
                "setting": "The Mathematical Kingdom",
                "theme": "numerical adventures and problem-solving quests"
            },
            "Science": {
                "character": "Dr. Discovery",
                "setting": "The Laboratory of Wonders",
                "theme": "scientific exploration and experimentation"
            },
            "English": {
                "character": "Storyteller Sam",
                "setting": "The Library of Tales",
                "theme": "literary adventures and word mastery"
            }
        }
        
        return contexts.get(subject, {
            "character": "Learning Guide",
            "setting": "The Knowledge Realm",
            "theme": "educational adventure and skill building"
        })

    async def _generate_quest_hints(self, objectives: List[Dict], difficulty: str) -> List[str]:
        """Generate AI-powered hints for quest objectives"""
        hints = []
        for i, objective in enumerate(objectives):
            if difficulty == "easy":
                hints.append(f"💡 Try breaking down '{objective['objective']}' into smaller steps!")
            elif difficulty == "medium":
                hints.append(f"🎯 Focus on the key concepts in '{objective['objective']}' - you've got this!")
            else:
                hints.append(f"🧠 Challenge yourself with '{objective['objective']}' - think creatively!")
        
        return hints

    def _calculate_quest_xp(self, difficulty: str, num_objectives: int) -> int:
        """Calculate experience points for quest completion"""
        base_xp = {"easy": 50, "medium": 100, "hard": 200, "expert": 350}
        return base_xp.get(difficulty, 100) + (num_objectives * 25)

    async def _check_quest_prerequisites(self, student_id: str, prerequisites: List[str]) -> bool:
        """Check if student has completed prerequisite quests"""
        if not prerequisites:
            return True
        
        student_completed_quests = []
        for quest_id in self.student_quests.get(student_id, []):
            if quest_id in self.quests and self.quests[quest_id].status == QuestStatus.COMPLETED.value:
                student_completed_quests.append(quest_id)
        
        return all(prereq in student_completed_quests for prereq in prerequisites)

    async def _create_character_progression(self, student_id: str) -> CharacterProgression:
        """Create initial character progression for student"""
        character_types = ["explorer", "scholar", "warrior", "sage", "artist"]
        
        return CharacterProgression(
            character_id=str(uuid.uuid4()),
            student_id=student_id,
            character_name="Learning Hero",
            character_type=random.choice(character_types),
            level=1,
            experience_points=0,
            next_level_xp=100,
            appearance={"color": "blue", "accessory": "cape", "expression": "determined"},
            abilities=[],
            achievements=[],
            personality_traits=["curious", "determined"],
            favorite_subjects=[],
            learning_style_bonuses={},
            companion_relationship="friendly",
            last_adventure="Getting Started",
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )

    async def _check_level_up(self, character: CharacterProgression) -> bool:
        """Check and handle character level up"""
        if character.experience_points >= character.next_level_xp:
            character.level += 1
            character.next_level_xp = character.level * 100 + 50
            character.updated_at = datetime.now().isoformat()
            return True
        return False

    def _determine_reward_rarity(self, reward_type: str, source_quest: str) -> str:
        """Determine reward rarity based on context"""
        rarity_weights = {"common": 0.5, "uncommon": 0.25, "rare": 0.15, "epic": 0.08, "legendary": 0.02}
        return random.choices(list(rarity_weights.keys()), weights=list(rarity_weights.values()))[0]

    def _generate_reward_description(self, reward_name: str, reward_type: str) -> str:
        """Generate description for virtual reward"""
        descriptions = {
            "badge": f"A prestigious {reward_name} badge that showcases your learning achievement!",
            "trophy": f"A magnificent {reward_name} trophy representing your dedication and success!",
            "collectible_item": f"A rare {reward_name} collectible that adds to your learning collection!",
            "avatar_customization": f"An exclusive {reward_name} customization for your learning avatar!"
        }
        return descriptions.get(reward_type, f"An amazing {reward_name} reward for your hard work!")

    def _get_reward_visual(self, reward_type: str) -> str:
        """Get emoji/visual representation for reward type"""
        visuals = {
            "badge": "🏆",
            "trophy": "🥇",
            "collectible_item": "💎",
            "virtual_currency": "🪙",
            "avatar_customization": "🎨",
            "special_ability": "✨"
        }
        return visuals.get(reward_type, "🎁")

    def _get_special_properties(self, reward_type: str, rarity: str) -> List[str]:
        """Get special properties based on reward type and rarity"""
        if rarity == "legendary":
            return ["Double XP for 24 hours", "Exclusive avatar animation", "Special quest unlock"]
        elif rarity == "epic":
            return ["50% XP bonus", "Unique visual effect", "Advanced customization"]
        elif rarity == "rare":
            return ["25% XP bonus", "Special visual trait"]
        return []

    def _generate_competition_prizes(self) -> List[Dict]:
        """Generate prizes for competition rankings"""
        return [
            {"rank_range": [1, 1], "reward": {"type": "trophy", "item": "Champion's Trophy", "rarity": "legendary"}},
            {"rank_range": [2, 3], "reward": {"type": "badge", "item": "Excellence Badge", "rarity": "epic"}},
            {"rank_range": [4, 10], "reward": {"type": "collectible_item", "item": "Achievement Gem", "rarity": "rare"}},
            {"rank_range": [11, 25], "reward": {"type": "virtual_currency", "item": "Learning Coins", "quantity": 100}}
        ]

    async def _generate_progress_encouragement(self, student_id: str, quest: Quest, objective_index: int) -> str:
        """Generate AI-powered encouragement message"""
        encouragements = [
            f"🌟 Great progress on {quest.quest_name}! You're {quest.progress_percentage:.0f}% complete!",
            f"🎯 Excellent work! Keep going - you're mastering {quest.subject} step by step!",
            f"💪 You're doing amazing! {quest.character_context.get('character', 'Your guide')} is proud of your dedication!",
            f"🚀 Fantastic job! You're well on your way to completing this {quest.difficulty} challenge!"
        ]
        return random.choice(encouragements)

    def _initialize_default_content(self):
        """Initialize default quests, rewards, and competitions"""
        # This would be expanded with pre-built quest content
        pass

# Global Advanced Gamification service instance
advanced_gamification_service = AdvancedGamificationService()