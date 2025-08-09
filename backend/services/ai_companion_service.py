"""
AI Companion Agent - RSP Education Agent V2 Phase 1 (8th Agent)
Intelligent companion agent with personality, memory, and emotional intelligence
Shared memory architecture for consistent experience across all 7 agents
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import random

from sqlalchemy.orm import Session
from database.models import Student
from core.exceptions import AgentException

logger = logging.getLogger(__name__)

class MoodType(Enum):
    HAPPY = "happy"
    ENCOURAGING = "encouraging"
    CONCERNED = "concerned"
    EXCITED = "excited"
    PROUD = "proud"
    PLAYFUL = "playful"
    WISE = "wise"
    CELEBRATORY = "celebratory"

class PersonalityTrait(Enum):
    ENCOURAGING = "encouraging"
    PLAYFUL = "playful"
    WISE = "wise"
    FUNNY = "funny"
    PATIENT = "patient"
    ENERGETIC = "energetic"

@dataclass
class CompanionProfile:
    """AI Companion profile with personality and memory"""
    student_id: str
    companion_name: str = "Buddy Bear"
    personality_traits: List[str] = None
    current_mood: str = MoodType.HAPPY.value
    interaction_count: int = 0
    last_interaction: Optional[str] = None
    memory_bank: Dict = None
    preferences: Dict = None
    
    def __post_init__(self):
        if self.personality_traits is None:
            self.personality_traits = [PersonalityTrait.ENCOURAGING.value, PersonalityTrait.PLAYFUL.value]
        if self.memory_bank is None:
            self.memory_bank = {
                "favorite_subjects": [],
                "struggle_areas": [],
                "achievements": [],
                "learning_patterns": {},
                "emotional_history": []
            }
        if self.preferences is None:
            self.preferences = {
                "celebration_style": "moderate",
                "encouragement_frequency": "balanced",
                "response_length": "medium"
            }

@dataclass
class MoodState:
    """Current emotional state of the AI companion"""
    current_mood: str
    confidence_level: float
    suggested_interaction_style: str
    encouragement_level: int
    factors: List[str]

@dataclass
class CompanionResponse:
    """Personalized response from AI companion"""
    message: str
    emoji: str
    tone: str
    follow_up_suggestions: List[str]
    celebration_level: int
    mood_update: Optional[str] = None
    
@dataclass
class InteractionAnalysis:
    """Analysis of student interaction for mood detection"""
    sentiment_score: float
    performance_trend: str
    frustration_indicators: List[str]
    success_indicators: List[str]
    engagement_level: float

class AICompanionAgent:
    """AI Companion Agent (8th Agent) with personality, memory, and emotional intelligence
    
    Provides shared memory and personality context for all other agents to ensure
    consistent companion experience across the entire platform.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.AICompanionAgent")
        self.companion_profiles: Dict[str, CompanionProfile] = {}
        
        # Response templates by mood and personality
        self.response_templates = {
            MoodType.HAPPY.value: {
                PersonalityTrait.ENCOURAGING.value: [
                    "Hey there, superstar! {emoji} I'm so happy to see you back! {context}",
                    "Welcome back, champion! {emoji} Ready for another amazing learning adventure? {context}",
                    "Hi buddy! {emoji} I've been waiting to learn with you today! {context}"
                ],
                PersonalityTrait.PLAYFUL.value: [
                    "Woohoo! {emoji} My favorite learning buddy is here! {context}",
                    "Hey hey hey! {emoji} Ready to have some learning fun? {context}",
                    "Yippee! {emoji} Let's make today's learning super awesome! {context}"
                ],
                PersonalityTrait.WISE.value: [
                    "Greetings, young learner! {emoji} Wisdom awaits us today. {context}",
                    "Hello there! {emoji} Another day, another opportunity to grow our minds. {context}",
                    "Welcome back! {emoji} Knowledge is calling, shall we answer? {context}"
                ]
            },
            MoodType.ENCOURAGING.value: {
                PersonalityTrait.ENCOURAGING.value: [
                    "You're doing great! {emoji} I believe in you completely! {context}",
                    "Keep going, superstar! {emoji} Every step forward is progress! {context}",
                    "I'm so proud of your effort! {emoji} You're getting stronger every day! {context}"
                ],
                PersonalityTrait.PLAYFUL.value: [
                    "Don't worry, we've got this! {emoji} Let's turn this challenge into a game! {context}",
                    "Oops, no biggie! {emoji} Even superheroes need practice! {context}",
                    "Hey, mistakes are just learning in disguise! {emoji} {context}"
                ]
            },
            MoodType.EXCITED.value: {
                PersonalityTrait.ENERGETIC.value: [
                    "WOW! {emoji} You're absolutely crushing it today! {context}",
                    "AMAZING! {emoji} I can't contain my excitement for your progress! {context}",
                    "FANTASTIC! {emoji} You're on fire today! {context}"
                ],
                PersonalityTrait.PLAYFUL.value: [
                    "Holy moly! {emoji} You're like a learning superhero! {context}",
                    "Incredible! {emoji} My mind is blown by your awesomeness! {context}",
                    "Outstanding! {emoji} You're making my bear heart so happy! {context}"
                ]
            },
            MoodType.PROUD.value: {
                PersonalityTrait.ENCOURAGING.value: [
                    "I'm bursting with pride! {emoji} Look how far you've come! {context}",
                    "You should be so proud of yourself! {emoji} I certainly am! {context}",
                    "What an achievement! {emoji} You've worked so hard for this! {context}"
                ]
            },
            MoodType.CONCERNED.value: {
                PersonalityTrait.PATIENT.value: [
                    "Hey, it's okay to take your time. {emoji} I'm here to help! {context}",
                    "No worries at all! {emoji} Let's figure this out together. {context}",
                    "Sometimes learning is tough, but you're tougher! {emoji} {context}"
                ],
                PersonalityTrait.WISE.value: [
                    "Remember, every expert was once a beginner. {emoji} {context}",
                    "Challenges are just opportunities in disguise. {emoji} {context}",
                    "The path to wisdom has many steps, and you're walking it beautifully. {emoji} {context}"
                ]
            }
        }
        
        # Emoji sets for different moods
        self.mood_emojis = {
            MoodType.HAPPY.value: ["😊", "😄", "🐻", "🌟", "✨"],
            MoodType.ENCOURAGING.value: ["💪", "🌟", "👍", "🎯", "💖"],
            MoodType.EXCITED.value: ["🎉", "🚀", "⭐", "🔥", "🎊"],
            MoodType.PROUD.value: ["🏆", "👏", "🌟", "💎", "🎖️"],
            MoodType.CONCERNED.value: ["🤗", "💭", "🌈", "🍀", "💝"],
            MoodType.PLAYFUL.value: ["🎮", "🎪", "🎭", "🎨", "🎲"],
            MoodType.WISE.value: ["🦉", "📚", "🧠", "💡", "🔍"],
            MoodType.CELEBRATORY.value: ["🎉", "🎊", "🥳", "🎆", "🎈"]
        }

    async def initialize_companion(self, student_id: str, db: Session) -> CompanionProfile:
        """Initialize AI companion for a student"""
        try:
            # Check if companion already exists
            if student_id in self.companion_profiles:
                return self.companion_profiles[student_id]
            
            # Get student info for personalization
            student = db.query(Student).filter(Student.student_id == student_id).first()
            if not student:
                raise AgentException(f"Student not found: {student_id}")
            
            # Create personalized companion profile
            companion = CompanionProfile(
                student_id=student_id,
                companion_name="Buddy Bear",
                personality_traits=self._determine_personality_traits(student),
                memory_bank={
                    "favorite_subjects": [],
                    "struggle_areas": [],
                    "achievements": [],
                    "learning_patterns": {},
                    "emotional_history": [],
                    "student_name": student.name,
                    "grade": student.grade
                }
            )
            
            self.companion_profiles[student_id] = companion
            self.logger.info(f"Initialized AI companion for student: {student_id}")
            
            return companion
            
        except Exception as e:
            self.logger.error(f"Failed to initialize companion for {student_id}: {e}")
            raise AgentException(f"Companion initialization failed: {e}")

    def _determine_personality_traits(self, student: Student) -> List[str]:
        """Determine personality traits based on student profile"""
        traits = [PersonalityTrait.ENCOURAGING.value]  # Always encouraging
        
        # Add traits based on grade level
        grade_num = int(student.grade) if student.grade.isdigit() else 5
        
        if grade_num <= 5:
            traits.extend([PersonalityTrait.PLAYFUL.value, PersonalityTrait.PATIENT.value])
        elif grade_num <= 8:
            traits.extend([PersonalityTrait.ENERGETIC.value, PersonalityTrait.FUNNY.value])
        else:
            traits.extend([PersonalityTrait.WISE.value, PersonalityTrait.ENCOURAGING.value])
        
        return traits

    async def analyze_interaction(self, student_id: str, interaction_data: Dict) -> InteractionAnalysis:
        """Analyze student interaction for emotional state detection"""
        try:
            # Extract interaction metrics
            performance_score = interaction_data.get('performance_score', 0.5)
            time_spent = interaction_data.get('time_spent_minutes', 5)
            attempts = interaction_data.get('attempts', 1)
            completed = interaction_data.get('completed', True)
            
            # Sentiment analysis based on performance and behavior
            sentiment_score = self._calculate_sentiment_score(
                performance_score, time_spent, attempts, completed
            )
            
            # Determine performance trend
            performance_trend = self._analyze_performance_trend(performance_score, attempts)
            
            # Identify frustration indicators
            frustration_indicators = []
            if attempts > 3:
                frustration_indicators.append("multiple_attempts")
            if time_spent > 15:
                frustration_indicators.append("extended_time")
            if not completed:
                frustration_indicators.append("incomplete_session")
            if performance_score < 0.4:
                frustration_indicators.append("low_performance")
            
            # Identify success indicators
            success_indicators = []
            if performance_score > 0.8:
                success_indicators.append("high_performance")
            if attempts == 1:
                success_indicators.append("first_try_success")
            if time_spent < 5:
                success_indicators.append("quick_completion")
            if completed and performance_score > 0.6:
                success_indicators.append("successful_completion")
            
            # Calculate engagement level
            engagement_level = min(1.0, (performance_score + (1 - min(attempts/5, 1))) / 2)
            
            return InteractionAnalysis(
                sentiment_score=sentiment_score,
                performance_trend=performance_trend,
                frustration_indicators=frustration_indicators,
                success_indicators=success_indicators,
                engagement_level=engagement_level
            )
            
        except Exception as e:
            self.logger.error(f"Failed to analyze interaction for {student_id}: {e}")
            # Return neutral analysis on error
            return InteractionAnalysis(
                sentiment_score=0.5,
                performance_trend="stable",
                frustration_indicators=[],
                success_indicators=[],
                engagement_level=0.5
            )

    def _calculate_sentiment_score(self, performance: float, time: int, attempts: int, completed: bool) -> float:
        """Calculate sentiment score based on interaction metrics"""
        base_score = performance
        
        # Adjust for time efficiency
        if time < 3:
            base_score += 0.1  # Quick completion bonus
        elif time > 10:
            base_score -= 0.1  # Extended time penalty
        
        # Adjust for attempts
        if attempts == 1:
            base_score += 0.2  # First try bonus
        elif attempts > 3:
            base_score -= 0.15  # Multiple attempts penalty
        
        # Adjust for completion
        if not completed:
            base_score -= 0.3  # Incomplete penalty
        
        return max(0.0, min(1.0, base_score))

    def _analyze_performance_trend(self, performance: float, attempts: int) -> str:
        """Analyze performance trend"""
        if performance > 0.8 and attempts <= 2:
            return "improving"
        elif performance < 0.4 or attempts > 4:
            return "struggling"
        else:
            return "stable"

    async def update_mood(self, student_id: str, interaction_analysis: InteractionAnalysis) -> MoodState:
        """Update companion mood based on interaction analysis"""
        try:
            companion = self.companion_profiles.get(student_id)
            if not companion:
                raise AgentException(f"Companion not found for student: {student_id}")
            
            # Determine new mood based on analysis
            new_mood = self._determine_mood_from_analysis(interaction_analysis, companion.current_mood)
            
            # Update companion profile
            companion.current_mood = new_mood
            companion.interaction_count += 1
            companion.last_interaction = datetime.now().isoformat()
            
            # Add to emotional history
            companion.memory_bank["emotional_history"].append({
                "timestamp": datetime.now().isoformat(),
                "mood": new_mood,
                "sentiment_score": interaction_analysis.sentiment_score,
                "performance_trend": interaction_analysis.performance_trend
            })
            
            # Keep only last 50 emotional history entries
            if len(companion.memory_bank["emotional_history"]) > 50:
                companion.memory_bank["emotional_history"] = companion.memory_bank["emotional_history"][-50:]
            
            # Determine interaction style and encouragement level
            interaction_style = self._get_interaction_style(new_mood, companion.personality_traits)
            encouragement_level = self._calculate_encouragement_level(interaction_analysis)
            
            mood_state = MoodState(
                current_mood=new_mood,
                confidence_level=interaction_analysis.sentiment_score,
                suggested_interaction_style=interaction_style,
                encouragement_level=encouragement_level,
                factors=interaction_analysis.frustration_indicators + interaction_analysis.success_indicators
            )
            
            self.logger.info(f"Updated mood for {student_id}: {new_mood}")
            return mood_state
            
        except Exception as e:
            self.logger.error(f"Failed to update mood for {student_id}: {e}")
            raise AgentException(f"Mood update failed: {e}")

    def _determine_mood_from_analysis(self, analysis: InteractionAnalysis, current_mood: str) -> str:
        """Determine new mood based on interaction analysis"""
        # High performance and success indicators
        if analysis.sentiment_score > 0.8 and len(analysis.success_indicators) >= 2:
            return MoodType.EXCITED.value
        
        # Good performance
        elif analysis.sentiment_score > 0.7:
            return MoodType.PROUD.value if "high_performance" in analysis.success_indicators else MoodType.HAPPY.value
        
        # Struggling indicators
        elif len(analysis.frustration_indicators) >= 2 or analysis.sentiment_score < 0.4:
            return MoodType.CONCERNED.value
        
        # Moderate performance, provide encouragement
        elif analysis.sentiment_score < 0.6:
            return MoodType.ENCOURAGING.value
        
        # Default to happy
        else:
            return MoodType.HAPPY.value

    def _get_interaction_style(self, mood: str, personality_traits: List[str]) -> str:
        """Get appropriate interaction style based on mood and personality"""
        style_map = {
            MoodType.HAPPY.value: "friendly_casual",
            MoodType.ENCOURAGING.value: "supportive_motivational",
            MoodType.EXCITED.value: "enthusiastic_celebratory",
            MoodType.PROUD.value: "warm_congratulatory",
            MoodType.CONCERNED.value: "gentle_supportive",
            MoodType.PLAYFUL.value: "fun_interactive",
            MoodType.WISE.value: "thoughtful_guiding"
        }
        
        return style_map.get(mood, "friendly_casual")

    def _calculate_encouragement_level(self, analysis: InteractionAnalysis) -> int:
        """Calculate encouragement level (1-10) based on analysis"""
        if len(analysis.frustration_indicators) >= 3:
            return 9  # High encouragement needed
        elif len(analysis.frustration_indicators) >= 1:
            return 6  # Moderate encouragement
        elif len(analysis.success_indicators) >= 2:
            return 3  # Light encouragement, focus on celebration
        else:
            return 5  # Balanced encouragement

    async def generate_response(self, student_id: str, context: str, mood_state: MoodState) -> CompanionResponse:
        """Generate personalized response from AI companion"""
        try:
            companion = self.companion_profiles.get(student_id)
            if not companion:
                raise AgentException(f"Companion not found for student: {student_id}")
            
            # Select appropriate response template
            templates = self._get_response_templates(mood_state.current_mood, companion.personality_traits)
            template = random.choice(templates)
            
            # Get appropriate emoji
            emoji = random.choice(self.mood_emojis.get(mood_state.current_mood, ["🐻"]))
            
            # Format message with context
            message = template.format(
                emoji=emoji,
                context=self._format_context(context, companion),
                name=companion.memory_bank.get("student_name", "champion")
            )
            
            # Generate follow-up suggestions based on mood and context
            follow_up_suggestions = self._generate_follow_up_suggestions(mood_state, context, companion)
            
            # Determine celebration level
            celebration_level = self._calculate_celebration_level(mood_state)
            
            response = CompanionResponse(
                message=message,
                emoji=emoji,
                tone=mood_state.suggested_interaction_style,
                follow_up_suggestions=follow_up_suggestions,
                celebration_level=celebration_level,
                mood_update=mood_state.current_mood
            )
            
            self.logger.info(f"Generated response for {student_id} in {mood_state.current_mood} mood")
            return response
            
        except Exception as e:
            self.logger.error(f"Failed to generate response for {student_id}: {e}")
            # Return default encouraging response
            return CompanionResponse(
                message="You're doing great! Keep up the amazing work! 🐻",
                emoji="🐻",
                tone="friendly_casual",
                follow_up_suggestions=["Keep learning!", "Try another question!", "You've got this!"],
                celebration_level=5
            )

    def _get_response_templates(self, mood: str, personality_traits: List[str]) -> List[str]:
        """Get response templates for given mood and personality"""
        mood_templates = self.response_templates.get(mood, {})
        
        # Find the best matching personality trait
        for trait in personality_traits:
            if trait in mood_templates:
                return mood_templates[trait]
        
        # Fallback to first available template
        if mood_templates:
            return list(mood_templates.values())[0]
        
        # Ultimate fallback
        return ["Hey there! {emoji} You're doing great! {context}"]

    def _format_context(self, context: str, companion: CompanionProfile) -> str:
        """Format context message with personalization"""
        if not context:
            return "Let's keep learning together!"
        
        # Add personal touches based on memory
        student_name = companion.memory_bank.get("student_name", "")
        if student_name and student_name.lower() not in context.lower():
            context = f"{student_name}, {context}"
        
        return context

    def _generate_follow_up_suggestions(self, mood_state: MoodState, context: str, companion: CompanionProfile) -> List[str]:
        """Generate contextual follow-up suggestions"""
        suggestions = []
        
        if mood_state.current_mood == MoodType.EXCITED.value:
            suggestions = [
                "Let's tackle the next challenge!",
                "Want to try something even more exciting?",
                "You're on a roll - keep going!"
            ]
        elif mood_state.current_mood == MoodType.CONCERNED.value:
            suggestions = [
                "Would you like a hint?",
                "Let's break this down step by step",
                "Take your time, I'm here to help"
            ]
        elif mood_state.current_mood == MoodType.PROUD.value:
            suggestions = [
                "Share your success with friends!",
                "Ready for the next adventure?",
                "You've earned a celebration!"
            ]
        else:
            suggestions = [
                "What would you like to learn next?",
                "Ready for another question?",
                "Let's keep the momentum going!"
            ]
        
        return suggestions[:3]  # Return max 3 suggestions

    def _calculate_celebration_level(self, mood_state: MoodState) -> int:
        """Calculate celebration level (1-10) based on mood state"""
        celebration_map = {
            MoodType.EXCITED.value: 9,
            MoodType.PROUD.value: 8,
            MoodType.HAPPY.value: 6,
            MoodType.PLAYFUL.value: 7,
            MoodType.ENCOURAGING.value: 4,
            MoodType.CONCERNED.value: 2,
            MoodType.WISE.value: 5
        }
        
        base_level = celebration_map.get(mood_state.current_mood, 5)
        
        # Adjust based on encouragement level
        if mood_state.encouragement_level > 7:
            base_level = max(1, base_level - 2)  # Lower celebration when high encouragement needed
        elif mood_state.encouragement_level < 4:
            base_level = min(10, base_level + 2)  # Higher celebration when doing well
        
        return base_level

    async def track_interaction(self, student_id: str, interaction: Dict) -> None:
        """Track interaction in companion memory"""
        try:
            companion = self.companion_profiles.get(student_id)
            if not companion:
                return
            
            # Update learning patterns
            subject = interaction.get('subject', 'general')
            performance = interaction.get('performance_score', 0.5)
            
            # Update subject preferences
            if subject not in companion.memory_bank["learning_patterns"]:
                companion.memory_bank["learning_patterns"][subject] = {
                    "total_interactions": 0,
                    "average_performance": 0.0,
                    "last_interaction": None
                }
            
            pattern = companion.memory_bank["learning_patterns"][subject]
            pattern["total_interactions"] += 1
            pattern["average_performance"] = (
                (pattern["average_performance"] * (pattern["total_interactions"] - 1) + performance) 
                / pattern["total_interactions"]
            )
            pattern["last_interaction"] = datetime.now().isoformat()
            
            # Update favorite subjects and struggle areas
            if performance > 0.8:
                if subject not in companion.memory_bank["favorite_subjects"]:
                    companion.memory_bank["favorite_subjects"].append(subject)
            elif performance < 0.4:
                if subject not in companion.memory_bank["struggle_areas"]:
                    companion.memory_bank["struggle_areas"].append(subject)
            
            # Track achievements
            if 'achievement' in interaction:
                companion.memory_bank["achievements"].append({
                    "achievement": interaction['achievement'],
                    "timestamp": datetime.now().isoformat(),
                    "subject": subject
                })
            
            self.logger.info(f"Tracked interaction for {student_id} in {subject}")
            
        except Exception as e:
            self.logger.error(f"Failed to track interaction for {student_id}: {e}")

    async def get_companion_status(self, student_id: str) -> Dict:
        """Get current companion status and statistics"""
        try:
            companion = self.companion_profiles.get(student_id)
            if not companion:
                return {"error": "Companion not found"}
            
            # Calculate statistics
            total_interactions = companion.interaction_count
            favorite_subjects = companion.memory_bank.get("favorite_subjects", [])
            struggle_areas = companion.memory_bank.get("struggle_areas", [])
            recent_achievements = companion.memory_bank.get("achievements", [])[-5:]  # Last 5 achievements
            
            # Calculate mood stability
            recent_moods = [entry["mood"] for entry in companion.memory_bank.get("emotional_history", [])[-10:]]
            mood_stability = len(set(recent_moods)) if recent_moods else 0
            
            return {
                "companion_name": companion.companion_name,
                "current_mood": companion.current_mood,
                "personality_traits": companion.personality_traits,
                "total_interactions": total_interactions,
                "favorite_subjects": favorite_subjects,
                "struggle_areas": struggle_areas,
                "recent_achievements": recent_achievements,
                "mood_stability": mood_stability,
                "last_interaction": companion.last_interaction,
                "companion_level": min(10, total_interactions // 10 + 1)  # Companion grows with interactions
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get companion status for {student_id}: {e}")
            return {"error": f"Failed to get status: {e}"}

    # === SHARED MEMORY METHODS FOR OTHER AGENTS ===
    
    def get_companion_context_for_agent(self, student_id: str, agent_name: str) -> Dict:
        """Get companion context that other agents can use for personalized responses"""
        try:
            companion = self.companion_profiles.get(student_id)
            if not companion:
                return {
                    "companion_available": False,
                    "default_personality": ["encouraging", "friendly"],
                    "interaction_count": 0
                }
            
            context = {
                "companion_available": True,
                "companion_name": companion.companion_name,
                "current_mood": companion.current_mood,
                "personality_traits": companion.personality_traits,
                "interaction_count": companion.interaction_count,
                "student_name": companion.memory_bank.get("student_name", "champion"),
                "favorite_subjects": companion.memory_bank.get("favorite_subjects", []),
                "struggle_areas": companion.memory_bank.get("struggle_areas", []),
                "recent_achievements": companion.memory_bank.get("achievements", [])[-3:],  # Last 3 achievements
                "engagement_level": self._calculate_current_engagement_level(companion),
                "encouragement_needed": len(companion.memory_bank.get("struggle_areas", [])) > 0,
                "celebration_worthy": len(companion.memory_bank.get("achievements", [])) > 0
            }
            
            # Add agent-specific context
            context["agent_integration"] = {
                "suggested_tone": self._get_tone_for_agent(companion.current_mood, agent_name),
                "personalization_tips": self._get_personalization_tips(companion, agent_name),
                "response_style": self._get_response_style_for_agent(companion.personality_traits, agent_name)
            }
            
            return context
            
        except Exception as e:
            self.logger.error(f"Failed to get companion context for {agent_name}: {e}")
            return {"companion_available": False, "error": str(e)}
    
    def update_companion_from_agent_interaction(self, student_id: str, agent_name: str, interaction_data: Dict) -> None:
        """Update companion state based on interaction from any agent"""
        try:
            companion = self.companion_profiles.get(student_id)
            if not companion:
                self.logger.warning(f"No companion found for {student_id}, skipping update from {agent_name}")
                return
            
            # Track which agent was used
            if "agent_interactions" not in companion.memory_bank:
                companion.memory_bank["agent_interactions"] = {}
            
            if agent_name not in companion.memory_bank["agent_interactions"]:
                companion.memory_bank["agent_interactions"][agent_name] = {
                    "count": 0,
                    "last_used": None,
                    "performance_history": []
                }
            
            agent_data = companion.memory_bank["agent_interactions"][agent_name]
            agent_data["count"] += 1
            agent_data["last_used"] = datetime.now().isoformat()
            
            # Update performance history
            if "performance_score" in interaction_data:
                agent_data["performance_history"].append({
                    "score": interaction_data["performance_score"],
                    "timestamp": datetime.now().isoformat()
                })
                # Keep only last 10 scores
                agent_data["performance_history"] = agent_data["performance_history"][-10:]
            
            # Update overall companion stats
            companion.interaction_count += 1
            companion.last_interaction = datetime.now().isoformat()
            
            # Update subject-specific data if provided
            if "subject" in interaction_data:
                subject = interaction_data["subject"]
                performance = interaction_data.get("performance_score", 0.5)
                
                # Update favorite subjects
                if performance > 0.8 and subject not in companion.memory_bank.get("favorite_subjects", []):
                    companion.memory_bank.setdefault("favorite_subjects", []).append(subject)
                
                # Update struggle areas
                elif performance < 0.4 and subject not in companion.memory_bank.get("struggle_areas", []):
                    companion.memory_bank.setdefault("struggle_areas", []).append(subject)
            
            # Add achievements if provided
            if "achievement" in interaction_data:
                companion.memory_bank.setdefault("achievements", []).append({
                    "achievement": interaction_data["achievement"],
                    "agent": agent_name,
                    "timestamp": datetime.now().isoformat()
                })
            
            self.logger.info(f"Updated companion for {student_id} based on {agent_name} interaction")
            
        except Exception as e:
            self.logger.error(f"Failed to update companion from {agent_name} interaction: {e}")
    
    def get_personalized_response_for_agent(self, student_id: str, agent_name: str, base_response: str, context: Dict = None) -> str:
        """Enhance any agent's response with companion personality"""
        try:
            companion = self.companion_profiles.get(student_id)
            if not companion:
                return base_response  # Return original response if no companion
            
            # Get appropriate emoji for current mood
            emoji = random.choice(self.mood_emojis.get(companion.current_mood, ["🐻"]))
            
            # Add personality touches based on companion traits
            personality_additions = []
            
            if PersonalityTrait.ENCOURAGING.value in companion.personality_traits:
                if "great" in base_response.lower() or "good" in base_response.lower():
                    personality_additions.append("You're doing amazing!")
                elif "try" in base_response.lower():
                    personality_additions.append("I believe in you!")
            
            if PersonalityTrait.PLAYFUL.value in companion.personality_traits:
                personality_additions.append(random.choice([
                    "Let's keep the fun going!", 
                    "Learning is an adventure!", 
                    "Ready for more excitement?"
                ]))
            
            # Construct enhanced response
            enhanced_response = f"{emoji} {base_response}"
            
            if personality_additions:
                enhanced_response += f" {random.choice(personality_additions)}"
            
            # Add student name if appropriate
            student_name = companion.memory_bank.get("student_name", "")
            if student_name and student_name.lower() not in enhanced_response.lower():
                enhanced_response = enhanced_response.replace("You", f"{student_name}")
            
            return enhanced_response
            
        except Exception as e:
            self.logger.error(f"Failed to enhance response for {agent_name}: {e}")
            return base_response  # Return original on error
    
    def _calculate_current_engagement_level(self, companion: CompanionProfile) -> float:
        """Calculate current engagement level based on recent interactions"""
        recent_history = companion.memory_bank.get("emotional_history", [])[-5:]  # Last 5 interactions
        if not recent_history:
            return 0.5
        
        sentiment_scores = [entry.get("sentiment_score", 0.5) for entry in recent_history]
        return sum(sentiment_scores) / len(sentiment_scores)
    
    def _get_tone_for_agent(self, mood: str, agent_name: str) -> str:
        """Get appropriate tone for specific agent based on companion mood"""
        tone_map = {
            "content_generator": {
                MoodType.HAPPY.value: "creative_encouraging",
                MoodType.EXCITED.value: "enthusiastic_imaginative",
                MoodType.CONCERNED.value: "gentle_supportive",
                MoodType.ENCOURAGING.value: "motivational_inspiring"
            },
            "assessment": {
                MoodType.HAPPY.value: "confident_positive",
                MoodType.EXCITED.value: "celebratory_proud",
                MoodType.CONCERNED.value: "patient_understanding",
                MoodType.ENCOURAGING.value: "supportive_motivating"
            },
            "voice_interaction": {
                MoodType.HAPPY.value: "cheerful_warm",
                MoodType.EXCITED.value: "energetic_enthusiastic",
                MoodType.PLAYFUL.value: "fun_interactive",
                MoodType.WISE.value: "calm_thoughtful"
            }
        }
        
        agent_tones = tone_map.get(agent_name, {})
        return agent_tones.get(mood, "friendly_supportive")
    
    def _get_personalization_tips(self, companion: CompanionProfile, agent_name: str) -> List[str]:
        """Get personalization tips for specific agent"""
        tips = []
        
        # Based on favorite subjects
        favorites = companion.memory_bank.get("favorite_subjects", [])
        if favorites and agent_name in ["content_generator", "assessment"]:
            tips.append(f"Student loves {', '.join(favorites)} - incorporate these interests")
        
        # Based on struggle areas
        struggles = companion.memory_bank.get("struggle_areas", [])
        if struggles:
            tips.append(f"Be extra encouraging with {', '.join(struggles)} - student finds these challenging")
        
        # Based on interaction count
        if companion.interaction_count < 5:
            tips.append("New student - be extra welcoming and explain features")
        elif companion.interaction_count > 50:
            tips.append("Experienced student - can handle advanced features and challenges")
        
        return tips
    
    def _get_response_style_for_agent(self, personality_traits: List[str], agent_name: str) -> str:
        """Get response style recommendation for specific agent"""
        if PersonalityTrait.PLAYFUL.value in personality_traits:
            return "use_emojis_and_fun_language"
        elif PersonalityTrait.WISE.value in personality_traits:
            return "thoughtful_and_educational"
        elif PersonalityTrait.ENERGETIC.value in personality_traits:
            return "enthusiastic_and_dynamic"
        else:
            return "warm_and_encouraging"

# Global AI Companion Agent instance (8th Agent)
ai_companion_agent = AICompanionAgent()