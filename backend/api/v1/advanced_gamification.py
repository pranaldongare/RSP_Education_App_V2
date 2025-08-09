"""
Advanced Gamification API - RSP Education Agent V2 Phase 2.3
REST API endpoints for quest-based learning, virtual rewards, and social competitions
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from pydantic import BaseModel
import logging

from database.database import get_db
from api.v1.auth import get_current_user
from database.models import Student
from services.advanced_gamification_service import advanced_gamification_service
from core.exceptions import AgentException

logger = logging.getLogger(__name__)

# Pydantic models for API requests/responses
class CreateQuestRequest(BaseModel):
    """Request model for creating a quest"""
    quest_name: str
    quest_type: str
    difficulty: str
    subject: str
    grade_range: List[int]
    storyline: str
    objectives: List[Dict]
    rewards: List[Dict]
    estimated_duration: int = 30

class StartQuestRequest(BaseModel):
    """Request model for starting a quest"""
    quest_id: str

class UpdateQuestProgressRequest(BaseModel):
    """Request model for updating quest progress"""
    quest_id: str
    objective_index: int
    progress_amount: int = 1

class CreateCompetitionRequest(BaseModel):
    """Request model for creating a competition"""
    competition_name: str
    competition_type: str
    subject: str
    grade_range: List[int]
    duration_days: int = 7

class JoinCompetitionRequest(BaseModel):
    """Request model for joining a competition"""
    competition_id: str

# Create API router
router = APIRouter(prefix="/advanced-gamification", tags=["Advanced Gamification"])

@router.post("/quests/create")
async def create_quest(
    request: CreateQuestRequest,
    current_user: Student = Depends(get_current_user)
):
    """Create a new quest with storyline and objectives"""
    try:
        quest = await advanced_gamification_service.create_quest(
            quest_name=request.quest_name,
            quest_type=request.quest_type,
            difficulty=request.difficulty,
            subject=request.subject,
            grade_range=request.grade_range,
            storyline=request.storyline,
            objectives=request.objectives,
            rewards=request.rewards,
            estimated_duration=request.estimated_duration
        )
        
        return {
            "success": True,
            "message": f"🎮 Quest '{request.quest_name}' created successfully for {current_user.name}!",
            "data": {
                "quest_id": quest.quest_id,
                "quest_name": quest.quest_name,
                "quest_type": quest.quest_type,
                "difficulty": quest.difficulty,
                "subject": quest.subject,
                "storyline": quest.storyline,
                "objectives": quest.objectives,
                "experience_points": quest.experience_points,
                "estimated_duration": quest.estimated_duration_minutes,
                "character_context": quest.character_context,
                "ai_hints": quest.ai_hints[:3]  # First 3 hints only
            },
            "quest_features": {
                "ai_enhanced_storyline": "Immersive narrative with character interactions",
                "adaptive_difficulty": "Quest adjusts based on your performance",
                "personalized_hints": "AI provides contextual guidance throughout",
                "character_progression": "Gain XP and unlock new abilities",
                "virtual_rewards": "Earn badges, trophies, and collectible items"
            },
            "getting_started": [
                f"Begin your adventure in {quest.character_context.get('setting', 'the learning realm')}",
                f"Meet {quest.character_context.get('character', 'your guide')} who will help you",
                "Complete objectives step by step to progress through the story",
                "Use AI hints when you need guidance or encouragement"
            ]
        }
        
    except AgentException as e:
        logger.error(f"Error creating quest: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error creating quest: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during quest creation"
        )

@router.get("/quests/available")
async def get_available_quests(
    subject: Optional[str] = Query(None, description="Filter by subject"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty"),
    current_user: Student = Depends(get_current_user)
):
    """Get available quests for the current student"""
    try:
        available_quests = await advanced_gamification_service.get_available_quests(current_user.student_id)
        
        # Apply filters
        if subject:
            available_quests = [q for q in available_quests if q.subject.lower() == subject.lower()]
        if difficulty:
            available_quests = [q for q in available_quests if q.difficulty.lower() == difficulty.lower()]
        
        quests_data = []
        for quest in available_quests:
            quests_data.append({
                "quest_id": quest.quest_id,
                "quest_name": quest.quest_name,
                "quest_type": quest.quest_type,
                "difficulty": quest.difficulty,
                "subject": quest.subject,
                "storyline": quest.storyline,
                "objectives_count": len(quest.objectives),
                "experience_points": quest.experience_points,
                "estimated_duration": quest.estimated_duration_minutes,
                "rewards_preview": quest.rewards[:2],  # Show first 2 rewards
                "character_context": quest.character_context,
                "difficulty_stars": "⭐" * ({"easy": 1, "medium": 2, "hard": 3, "expert": 4}.get(quest.difficulty, 2))
            })
        
        return {
            "success": True,
            "message": f"🎯 Found {len(quests_data)} available quests for {current_user.name}!",
            "data": quests_data,
            "quest_summary": {
                "total_available": len(quests_data),
                "subjects_available": list(set(q["subject"] for q in quests_data)),
                "difficulty_levels": list(set(q["difficulty"] for q in quests_data)),
                "total_xp_potential": sum(q["experience_points"] for q in quests_data),
                "estimated_total_time": sum(q["estimated_duration"] for q in quests_data)
            },
            "recommendation": {
                "suggested_quest": quests_data[0] if quests_data else None,
                "reason": "Perfect match for your current level and interests!" if quests_data else "No quests available at your level"
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting available quests: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during quest retrieval"
        )

@router.post("/quests/start")
async def start_quest(
    request: StartQuestRequest,
    current_user: Student = Depends(get_current_user)
):
    """Start a quest for the current student"""
    try:
        success = await advanced_gamification_service.start_quest(
            student_id=current_user.student_id,
            quest_id=request.quest_id
        )
        
        if success:
            # Get quest details for response
            quest = advanced_gamification_service.quests.get(request.quest_id)
            
            return {
                "success": True,
                "message": f"🚀 Quest '{quest.quest_name}' started successfully! Your adventure begins now, {current_user.name}!",
                "data": {
                    "quest_id": quest.quest_id,
                    "quest_name": quest.quest_name,
                    "storyline": quest.storyline,
                    "first_objective": quest.objectives[0] if quest.objectives else None,
                    "first_hint": quest.ai_hints[0] if quest.ai_hints else None,
                    "character_context": quest.character_context
                },
                "adventure_begins": {
                    "welcome_message": f"Welcome to {quest.character_context.get('setting', 'the adventure')}!",
                    "guide_introduction": f"{quest.character_context.get('character', 'Your guide')} is ready to help you succeed!",
                    "quest_theme": quest.character_context.get('theme', 'an exciting learning journey'),
                    "objectives_total": len(quest.objectives),
                    "xp_reward": quest.experience_points
                },
                "next_steps": [
                    "Review your first objective and plan your approach",
                    "Use the AI hints whenever you need guidance",
                    "Track your progress as you complete each step",
                    "Celebrate your achievements along the way!"
                ]
            }
        else:
            return {
                "success": False,
                "message": "Unable to start quest - check prerequisites or quest availability",
                "error": "Quest start failed"
            }
        
    except Exception as e:
        logger.error(f"Error starting quest: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during quest start"
        )

@router.post("/quests/progress")
async def update_quest_progress(
    request: UpdateQuestProgressRequest,
    current_user: Student = Depends(get_current_user)
):
    """Update progress on a quest objective"""
    try:
        result = await advanced_gamification_service.update_quest_progress(
            student_id=current_user.student_id,
            quest_id=request.quest_id,
            objective_index=request.objective_index,
            progress_amount=request.progress_amount
        )
        
        if result["success"]:
            return {
                "success": True,
                "message": result.get("encouragement", "Great progress!"),
                "data": {
                    "quest_id": request.quest_id,
                    "progress_percentage": result["progress_percentage"],
                    "objective_completed": result["objective_completed"],
                    "quest_completed": result["quest_completed"]
                },
                "progress_feedback": {
                    "encouragement": result.get("encouragement", "Keep up the excellent work!"),
                    "next_hint": result.get("next_hint"),
                    "completion_status": "🎉 Quest Complete!" if result["quest_completed"] else f"📊 {result['progress_percentage']:.0f}% Complete",
                    "xp_gained": result.get("xp_gained", 0) if result["quest_completed"] else 0,
                    "rewards_earned": result.get("rewards_earned", 0) if result["quest_completed"] else 0
                }
            }
        else:
            return result
        
    except Exception as e:
        logger.error(f"Error updating quest progress: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during quest progress update"
        )

@router.get("/character/progression")
async def get_character_progression(
    current_user: Student = Depends(get_current_user)
):
    """Get current student's character progression"""
    try:
        character = await advanced_gamification_service.get_student_character_progression(current_user.student_id)
        
        return {
            "success": True,
            "message": f"📈 Character progression for {current_user.name}'s learning hero!",
            "data": {
                "character_id": character.character_id,
                "character_name": character.character_name,
                "character_type": character.character_type,
                "level": character.level,
                "experience_points": character.experience_points,
                "next_level_xp": character.next_level_xp,
                "xp_progress": (character.experience_points / character.next_level_xp) * 100,
                "appearance": character.appearance,
                "abilities": character.abilities,
                "achievements": character.achievements,
                "personality_traits": character.personality_traits,
                "favorite_subjects": character.favorite_subjects,
                "companion_relationship": character.companion_relationship,
                "last_adventure": character.last_adventure
            },
            "progression_stats": {
                "level_display": f"Level {character.level} {character.character_type.title()}",
                "xp_display": f"{character.experience_points}/{character.next_level_xp} XP",
                "xp_to_next_level": character.next_level_xp - character.experience_points,
                "abilities_unlocked": len(character.abilities),
                "achievements_earned": len(character.achievements),
                "adventure_count": len(character.achievements) + 1
            },
            "character_description": {
                "archetype": character.character_type,
                "personality": ", ".join(character.personality_traits),
                "specialties": character.favorite_subjects or ["Exploring new subjects"],
                "current_status": f"Ready for the next adventure in {character.last_adventure}!"
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting character progression: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during character progression retrieval"
        )

@router.get("/rewards/collection")
async def get_student_rewards(
    current_user: Student = Depends(get_current_user)
):
    """Get student's virtual reward collection"""
    try:
        student_reward_ids = advanced_gamification_service.student_rewards.get(current_user.student_id, [])
        rewards_collection = []
        
        for reward_id in student_reward_ids:
            reward = advanced_gamification_service.virtual_rewards.get(reward_id)
            if reward:
                rewards_collection.append({
                    "reward_id": reward.reward_id,
                    "reward_name": reward.reward_name,
                    "reward_type": reward.reward_type,
                    "rarity": reward.rarity,
                    "description": reward.description,
                    "visual_representation": reward.visual_representation,
                    "special_properties": reward.special_properties,
                    "earned_at": reward.earned_at,
                    "quest_source": reward.quest_source,
                    "equipped": reward.equipped,
                    "rarity_display": f"{reward.rarity.title()} {reward.reward_type.title()}"
                })
        
        # Sort by rarity and earned date
        rarity_order = {"legendary": 5, "epic": 4, "rare": 3, "uncommon": 2, "common": 1}
        rewards_collection.sort(key=lambda r: (rarity_order.get(r["rarity"], 0), r["earned_at"]), reverse=True)
        
        return {
            "success": True,
            "message": f"🏆 {current_user.name}'s Amazing Reward Collection!",
            "data": rewards_collection,
            "collection_stats": {
                "total_rewards": len(rewards_collection),
                "rarity_breakdown": {
                    rarity: len([r for r in rewards_collection if r["rarity"] == rarity])
                    for rarity in ["legendary", "epic", "rare", "uncommon", "common"]
                },
                "type_breakdown": {
                    reward_type: len([r for r in rewards_collection if r["reward_type"] == reward_type])
                    for reward_type in set(r["reward_type"] for r in rewards_collection)
                },
                "equipped_items": len([r for r in rewards_collection if r["equipped"]]),
                "collection_value": len(rewards_collection) * 10  # Simple value calculation
            },
            "achievements": {
                "collector_level": min(len(rewards_collection) // 10 + 1, 10),
                "rare_items": len([r for r in rewards_collection if r["rarity"] in ["rare", "epic", "legendary"]]),
                "completion_percentage": min((len(rewards_collection) / 50) * 100, 100)  # Assume 50 total possible
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting student rewards: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during rewards retrieval"
        )

@router.post("/competitions/create")
async def create_competition(
    request: CreateCompetitionRequest,
    current_user: Student = Depends(get_current_user)
):
    """Create a new learning competition"""
    try:
        competition = await advanced_gamification_service.create_competition(
            competition_name=request.competition_name,
            competition_type=request.competition_type,
            subject=request.subject,
            grade_range=request.grade_range,
            duration_days=request.duration_days
        )
        
        return {
            "success": True,
            "message": f"🏁 Competition '{request.competition_name}' created successfully by {current_user.name}!",
            "data": {
                "competition_id": competition.competition_id,
                "competition_name": competition.competition_name,
                "competition_type": competition.competition_type,
                "subject": competition.subject,
                "grade_range": competition.grade_range,
                "start_date": competition.start_date,
                "end_date": competition.end_date,
                "registration_deadline": competition.registration_deadline,
                "max_participants": competition.max_participants,
                "prizes": competition.prizes
            },
            "competition_features": {
                "social_learning": "Compete with peers in friendly learning challenges",
                "ranking_system": "Real-time leaderboards and performance tracking",
                "rewards_system": "Exclusive prizes and recognition for top performers",
                "fair_competition": "Grade-appropriate matching and balanced challenges"
            },
            "how_to_participate": [
                "Register before the deadline to secure your spot",
                "Complete learning activities to earn competition points",
                "Track your progress on the real-time leaderboard",
                "Aim for top rankings to earn exclusive rewards!"
            ]
        }
        
    except AgentException as e:
        logger.error(f"Error creating competition: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error creating competition: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during competition creation"
        )

@router.get("/competitions/active")
async def get_active_competitions(
    current_user: Student = Depends(get_current_user)
):
    """Get active competitions that the student can join"""
    try:
        active_competitions = []
        
        for competition in advanced_gamification_service.competitions.values():
            if competition.is_active and len(competition.participants) < competition.max_participants:
                active_competitions.append({
                    "competition_id": competition.competition_id,
                    "competition_name": competition.competition_name,
                    "competition_type": competition.competition_type,
                    "subject": competition.subject,
                    "description": competition.description,
                    "participants": len(competition.participants),
                    "max_participants": competition.max_participants,
                    "start_date": competition.start_date,
                    "end_date": competition.end_date,
                    "registration_deadline": competition.registration_deadline,
                    "prizes_preview": competition.prizes[:3],  # Show top 3 prizes
                    "already_joined": current_user.student_id in competition.participants,
                    "grade_eligible": current_user.grade in range(competition.grade_range[0], competition.grade_range[1] + 1)
                })
        
        return {
            "success": True,
            "message": f"🎮 {len(active_competitions)} active competitions available for {current_user.name}!",
            "data": active_competitions,
            "competition_summary": {
                "total_active": len(active_competitions),
                "eligible_competitions": len([c for c in active_competitions if c["grade_eligible"]]),
                "already_participating": len([c for c in active_competitions if c["already_joined"]]),
                "subjects_available": list(set(c["subject"] for c in active_competitions)),
                "competition_types": list(set(c["competition_type"] for c in active_competitions))
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting active competitions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during competitions retrieval"
        )

@router.post("/competitions/join")
async def join_competition(
    request: JoinCompetitionRequest,
    current_user: Student = Depends(get_current_user)
):
    """Join an active competition"""
    try:
        competition = advanced_gamification_service.competitions.get(request.competition_id)
        
        if not competition:
            return {
                "success": False,
                "message": "Competition not found",
                "error": "COMPETITION_NOT_FOUND"
            }
        
        if not competition.is_active:
            return {
                "success": False,
                "message": "Competition is not currently active",
                "error": "COMPETITION_INACTIVE"
            }
        
        if current_user.student_id in competition.participants:
            return {
                "success": False,
                "message": "You are already participating in this competition",
                "error": "ALREADY_JOINED"
            }
        
        if len(competition.participants) >= competition.max_participants:
            return {
                "success": False,
                "message": "Competition is full",
                "error": "COMPETITION_FULL"
            }
        
        if current_user.grade not in range(competition.grade_range[0], competition.grade_range[1] + 1):
            return {
                "success": False,
                "message": "You are not eligible for this competition based on your grade",
                "error": "GRADE_NOT_ELIGIBLE"
            }
        
        # Add student to competition
        competition.participants.append(current_user.student_id)
        
        return {
            "success": True,
            "message": f"🎉 Successfully joined '{competition.competition_name}'! Welcome to the competition, {current_user.name}!",
            "data": {
                "competition_id": competition.competition_id,
                "competition_name": competition.competition_name,
                "participants_count": len(competition.participants),
                "your_position": "Registered",
                "competition_status": "Active"
            },
            "next_steps": [
                "Complete learning activities to earn competition points",
                "Check your progress on the leaderboard regularly",
                "Aim for top rankings to win exclusive prizes",
                "Engage with the learning content to boost your score"
            ]
        }
        
    except Exception as e:
        logger.error(f"Error joining competition: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during competition join"
        )

@router.get("/leaderboards/{leaderboard_type}")
async def get_leaderboard(
    leaderboard_type: str,
    current_user: Student = Depends(get_current_user)
):
    """Get leaderboard for specific competition type"""
    try:
        leaderboard_position = await advanced_gamification_service.get_student_leaderboard_position(
            current_user.student_id, 
            leaderboard_type
        )
        
        return {
            "success": True,
            "message": f"📊 Leaderboard standings for {leaderboard_type.title()} competitions!",
            "data": leaderboard_position,
            "leaderboard_info": {
                "competition_type": leaderboard_type,
                "your_best_rank": min([pos["rank"] for pos in leaderboard_position["leaderboard_positions"].values()]) if leaderboard_position["leaderboard_positions"] else None,
                "total_leaderboards": len(leaderboard_position["leaderboard_positions"]),
                "overall_performance": "excellent" if leaderboard_position["overall_rank_average"] <= 10 else "good" if leaderboard_position["overall_rank_average"] <= 25 else "improving"
            },
            "motivation": {
                "keep_climbing": "Every learning session brings you closer to the top!",
                "your_progress": "You're making amazing strides in your learning journey!",
                "next_goal": "Aim for your next rank milestone - you've got this!"
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting leaderboard: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during leaderboard retrieval"
        )

@router.get("/dashboard-summary")
async def get_gamification_dashboard(
    current_user: Student = Depends(get_current_user)
):
    """Get comprehensive advanced gamification dashboard"""
    try:
        # Get character progression
        character = await advanced_gamification_service.get_student_character_progression(current_user.student_id)
        
        # Get active quests
        student_quest_ids = advanced_gamification_service.student_quests.get(current_user.student_id, [])
        active_quests = []
        completed_quests = []
        
        for quest_id in student_quest_ids:
            quest = advanced_gamification_service.quests.get(quest_id)
            if quest:
                if quest.status == "in_progress":
                    active_quests.append(quest)
                elif quest.status == "completed":
                    completed_quests.append(quest)
        
        # Get rewards count
        rewards_count = len(advanced_gamification_service.student_rewards.get(current_user.student_id, []))
        
        return {
            "success": True,
            "message": f"🎮 Advanced Gamification Dashboard for {current_user.name}!",
            "data": {
                "character_overview": {
                    "name": character.character_name,
                    "type": character.character_type,
                    "level": character.level,
                    "experience_points": character.experience_points,
                    "next_level_xp": character.next_level_xp,
                    "level_progress": (character.experience_points / character.next_level_xp) * 100
                },
                "quest_summary": {
                    "active_quests": len(active_quests),
                    "completed_quests": len(completed_quests),
                    "total_quests_attempted": len(student_quest_ids),
                    "completion_rate": (len(completed_quests) / len(student_quest_ids) * 100) if student_quest_ids else 0
                },
                "rewards_summary": {
                    "total_rewards": rewards_count,
                    "collection_progress": min((rewards_count / 50) * 100, 100),  # Assume 50 total rewards
                    "achievements_unlocked": len(character.achievements),
                    "abilities_learned": len(character.abilities)
                },
                "recent_activities": [
                    {"activity": f"Started quest: {quest.quest_name}", "timestamp": quest.started_at}
                    for quest in active_quests[-3:]
                ],
                "recommended_actions": [
                    "Continue your active quests to gain more XP",
                    "Explore new quests in your favorite subjects",
                    "Join competitions to earn exclusive rewards",
                    "Level up your character with learning achievements"
                ]
            },
            "gamification_features": {
                "quest_based_learning": "Immersive storylines with educational objectives",
                "character_progression": "Level up your avatar through learning achievements",
                "virtual_rewards": "Collect badges, trophies, and rare items",
                "social_competitions": "Compete with peers in learning challenges",
                "ai_enhancement": "Personalized hints and adaptive difficulty"
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting gamification dashboard: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during dashboard generation"
        )