"""
Adaptive Learning Agent - Phase 3 Implementation
Personalizes learning experiences by adjusting difficulty, detecting learning styles, and optimizing learning paths.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime, timedelta
from enum import Enum
import statistics
from dataclasses import dataclass

from pydantic import BaseModel, Field
import openai
from anthropic import Anthropic

from config.settings import settings
from core.curriculum import CBSECurriculum
from core.exceptions import AgentException
from agents.content_generator import DifficultyLevel, QuestionType
from agents.assessment_agent import AssessmentResult, PerformanceMetrics, FeedbackItem


class LearningStyle(str, Enum):
    """Learning style preferences"""
    VISUAL = "visual"           # Learn through images, diagrams, charts
    AUDITORY = "auditory"       # Learn through listening and discussion
    KINESTHETIC = "kinesthetic" # Learn through hands-on activities
    READING = "reading"         # Learn through reading and writing
    MULTIMODAL = "multimodal"   # Combination of multiple styles


class LearningPace(str, Enum):
    """Learning pace preferences"""
    SLOW = "slow"           # Needs more time and practice
    MODERATE = "moderate"   # Average learning pace
    FAST = "fast"          # Quick learner, needs challenges


class DifficultyAdjustmentStrategy(str, Enum):
    """Strategies for adjusting difficulty"""
    CONSERVATIVE = "conservative"  # Small incremental changes
    MODERATE = "moderate"          # Balanced adjustments
    AGGRESSIVE = "aggressive"      # Large changes based on performance


class LearningStyleIndicator(BaseModel):
    """Indicators for detecting learning styles"""
    style: LearningStyle
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in this style detection")
    evidence: List[str] = Field(default_factory=list, description="Evidence supporting this style")


class LearningProfile(BaseModel):
    """Comprehensive learning profile for a student"""
    student_id: str
    preferred_learning_styles: List[LearningStyleIndicator]
    learning_pace: LearningPace
    current_difficulty_level: Dict[str, DifficultyLevel]  # Per subject
    mastery_thresholds: Dict[str, float] = Field(default_factory=lambda: {
        "beginner": 0.6, "intermediate": 0.7, "advanced": 0.8
    })
    attention_span_minutes: int = Field(default=20, description="Estimated attention span")
    preferred_question_types: List[QuestionType] = Field(default_factory=list)
    weak_concepts: Dict[str, List[str]] = Field(default_factory=dict)  # Per subject
    strong_concepts: Dict[str, List[str]] = Field(default_factory=dict)  # Per subject
    last_updated: datetime = Field(default_factory=datetime.utcnow)


class AdaptationRequest(BaseModel):
    """Request for adaptive learning adjustments"""
    student_id: str
    assessment_results: List[AssessmentResult]
    current_profile: Optional[LearningProfile] = None
    learning_goals: List[str] = Field(default_factory=list)
    time_constraints: Optional[int] = Field(default=None, description="Available time in minutes")
    preferred_subjects: List[str] = Field(default_factory=list)


class ContentRecommendation(BaseModel):
    """Recommendation for learning content"""
    content_type: str  # "explanation", "practice", "assessment", "review"
    subject: str
    topic: str
    difficulty_level: DifficultyLevel
    estimated_time_minutes: int
    learning_objectives: List[str]
    recommended_question_types: List[QuestionType]
    priority: int = Field(..., ge=1, le=5, description="Priority level (1=highest)")
    reasoning: str = Field(..., description="Why this content is recommended")


class DifficultyAdjustment(BaseModel):
    """Difficulty level adjustment recommendation"""
    subject: str
    current_level: DifficultyLevel
    recommended_level: DifficultyLevel
    confidence: float = Field(..., ge=0.0, le=1.0)
    reasoning: str
    adjustment_factors: Dict[str, float] = Field(default_factory=dict)


class LearningPathRecommendation(BaseModel):
    """Complete learning path recommendation"""
    student_id: str
    recommended_content: List[ContentRecommendation]
    difficulty_adjustments: List[DifficultyAdjustment]
    updated_profile: LearningProfile
    next_assessment_timing: int = Field(..., description="Recommended time until next assessment in hours")
    focus_areas: List[str] = Field(default_factory=list)
    estimated_total_time: int = Field(..., description="Total estimated time in minutes")
    success_probability: float = Field(..., ge=0.0, le=1.0, description="Estimated success probability")


class AdaptiveLearningAgent:
    """
    Adaptive Learning Agent for personalizing educational experiences
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.AdaptiveLearningAgent")
        self.curriculum = CBSECurriculum()
        self.openai_model = None
        self.anthropic_model = None
        self._initialize_models()
        
        # Learning style detection patterns
        self.style_indicators = {
            LearningStyle.VISUAL: [
                "prefers diagrams", "uses charts", "draws while learning", "visual memory",
                "better with images", "spatial thinking"
            ],
            LearningStyle.AUDITORY: [
                "listens well", "discusses concepts", "verbal explanations", "sound patterns",
                "talks through problems", "music/rhythm helps"
            ],
            LearningStyle.KINESTHETIC: [
                "hands-on activities", "movement helps", "builds models", "physical practice",
                "learns by doing", "needs breaks"
            ],
            LearningStyle.READING: [
                "reads instructions", "takes notes", "text-based learning", "written summaries",
                "prefers reading", "written communication"
            ]
        }
        
        # Difficulty adjustment weights
        self.difficulty_weights = {
            "accuracy": 0.4,      # Recent accuracy scores
            "consistency": 0.2,    # Score consistency
            "time_efficiency": 0.2, # Time taken vs expected
            "improvement_trend": 0.2  # Learning progress trend
        }

    def _initialize_models(self):
        """Initialize AI models for adaptive learning"""
        try:
            if hasattr(settings, 'openai_api_key') and settings.openai_api_key:
                openai.api_key = settings.openai_api_key
                self.openai_model = "gpt-4-turbo-preview"
                
            if hasattr(settings, 'anthropic_api_key') and settings.anthropic_api_key:
                self.anthropic_model = Anthropic(api_key=settings.anthropic_api_key)
                
            self.logger.info("Adaptive Learning AI models initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize AI models: {e}")
            self.logger.warning("Continuing without AI models for testing purposes")

    async def adapt_learning_path(self, request: AdaptationRequest) -> LearningPathRecommendation:
        """
        Main method to adapt learning path based on student performance and profile
        """
        try:
            self.logger.info(f"Adapting learning path for student {request.student_id}")
            
            # Analyze assessment results
            performance_analysis = await self._analyze_performance_patterns(request.assessment_results)
            
            # Detect or update learning style
            learning_styles = await self._detect_learning_styles(
                request.assessment_results, request.current_profile
            )
            
            # Update learning profile
            updated_profile = await self._update_learning_profile(
                request.student_id, request.current_profile, performance_analysis, learning_styles
            )
            
            # Calculate difficulty adjustments
            difficulty_adjustments = await self._calculate_difficulty_adjustments(
                performance_analysis, updated_profile
            )
            
            # Generate content recommendations
            content_recommendations = await self._generate_content_recommendations(
                updated_profile, difficulty_adjustments, request.learning_goals, request.time_constraints
            )
            
            # Calculate next assessment timing
            next_assessment_timing = self._calculate_next_assessment_timing(
                performance_analysis, updated_profile
            )
            
            # Estimate success probability
            success_probability = self._estimate_success_probability(
                performance_analysis, difficulty_adjustments, updated_profile
            )
            
            recommendation = LearningPathRecommendation(
                student_id=request.student_id,
                recommended_content=content_recommendations,
                difficulty_adjustments=difficulty_adjustments,
                updated_profile=updated_profile,
                next_assessment_timing=next_assessment_timing,
                focus_areas=self._identify_focus_areas(performance_analysis, updated_profile),
                estimated_total_time=sum(rec.estimated_time_minutes for rec in content_recommendations),
                success_probability=success_probability
            )
            
            self.logger.info(f"Learning path adaptation completed for student {request.student_id}")
            return recommendation
            
        except Exception as e:
            self.logger.error(f"Learning path adaptation failed: {e}")
            raise AgentException(f"Learning path adaptation failed: {e}")

    async def _analyze_performance_patterns(self, assessment_results: List[AssessmentResult]) -> Dict[str, Any]:
        """Analyze patterns in student performance"""
        
        if not assessment_results:
            return {"error": "No assessment results to analyze"}
        
        # Sort by date
        sorted_results = sorted(assessment_results, key=lambda x: x.assessed_at)
        
        analysis = {
            "total_assessments": len(assessment_results),
            "subjects_assessed": list(set(result.subject for result in assessment_results)),
            "overall_trend": self._calculate_trend([result.performance_metrics.overall_score for result in sorted_results]),
            "consistency": self._calculate_consistency([result.performance_metrics.overall_score for result in sorted_results]),
            "subject_performance": {},
            "question_type_performance": {},
            "time_efficiency": self._analyze_time_efficiency(assessment_results),
            "common_mistakes": self._identify_common_mistakes(assessment_results),
            "strengths": self._identify_performance_strengths(assessment_results),
            "recent_performance": self._analyze_recent_performance(sorted_results[-3:] if len(sorted_results) >= 3 else sorted_results)
        }
        
        # Analyze by subject
        for subject in analysis["subjects_assessed"]:
            subject_results = [r for r in assessment_results if r.subject == subject]
            analysis["subject_performance"][subject] = {
                "average_score": statistics.mean(r.performance_metrics.overall_score for r in subject_results),
                "trend": self._calculate_trend([r.performance_metrics.overall_score for r in sorted(subject_results, key=lambda x: x.assessed_at)]),
                "mastery_level": self._determine_mastery_level(subject_results),
                "weak_topics": self._identify_weak_topics(subject_results),
                "strong_topics": self._identify_strong_topics(subject_results)
            }
        
        # Analyze by question type
        all_feedback_items = []
        for result in assessment_results:
            all_feedback_items.extend(result.feedback_items)
        
        # Group by question type (would need to track this in feedback items)
        # For now, use a simplified approach
        analysis["question_type_performance"] = {
            "overall_accuracy": statistics.mean(item.score for item in all_feedback_items) if all_feedback_items else 0.0,
            "total_questions": len(all_feedback_items)
        }
        
        return analysis

    def _calculate_trend(self, scores: List[float]) -> Dict[str, Any]:
        """Calculate performance trend"""
        if len(scores) < 2:
            return {"direction": "insufficient_data", "slope": 0.0, "confidence": 0.0}
        
        # Simple linear trend calculation
        x = list(range(len(scores)))
        n = len(scores)
        
        sum_x = sum(x)
        sum_y = sum(scores)
        sum_xy = sum(x[i] * scores[i] for i in range(n))
        sum_x2 = sum(xi * xi for xi in x)
        
        if n * sum_x2 - sum_x * sum_x == 0:
            slope = 0
        else:
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        
        direction = "improving" if slope > 0.02 else "declining" if slope < -0.02 else "stable"
        confidence = min(abs(slope) * 10, 1.0)  # Simplified confidence measure
        
        return {
            "direction": direction,
            "slope": slope,
            "confidence": confidence
        }

    def _calculate_consistency(self, scores: List[float]) -> Dict[str, Any]:
        """Calculate performance consistency"""
        if len(scores) < 2:
            return {"consistency_score": 1.0, "variability": 0.0}
        
        mean_score = statistics.mean(scores)
        variance = statistics.variance(scores)
        std_dev = statistics.stdev(scores)
        
        # Consistency score: higher is more consistent
        consistency_score = max(0.0, 1.0 - (std_dev / max(mean_score, 0.1)))
        
        return {
            "consistency_score": consistency_score,
            "variability": variance,
            "standard_deviation": std_dev,
            "mean_score": mean_score
        }

    def _analyze_time_efficiency(self, assessment_results: List[AssessmentResult]) -> Dict[str, Any]:
        """Analyze time efficiency patterns"""
        
        completion_times = []
        for result in assessment_results:
            if result.performance_metrics.completion_time:
                # Time per question
                time_per_question = result.performance_metrics.completion_time / result.performance_metrics.total_questions
                completion_times.append(time_per_question)
        
        if not completion_times:
            return {"average_time_per_question": 0, "time_consistency": 0.5}
        
        return {
            "average_time_per_question": statistics.mean(completion_times),
            "time_consistency": self._calculate_consistency(completion_times)["consistency_score"],
            "fastest_time": min(completion_times),
            "slowest_time": max(completion_times)
        }

    def _identify_common_mistakes(self, assessment_results: List[AssessmentResult]) -> List[str]:
        """Identify patterns in common mistakes"""
        
        mistake_patterns = []
        all_feedback_items = []
        
        for result in assessment_results:
            all_feedback_items.extend(result.feedback_items)
        
        # Analyze incorrect responses
        incorrect_items = [item for item in all_feedback_items if not item.is_correct]
        
        if len(incorrect_items) > len(all_feedback_items) * 0.3:  # More than 30% incorrect
            mistake_patterns.append("Frequent calculation errors")
        
        # Check for concept review patterns
        all_review_concepts = []
        for item in incorrect_items:
            all_review_concepts.extend(item.concepts_to_review)
        
        # Find most common review concepts
        concept_counts = {}
        for concept in all_review_concepts:
            concept_counts[concept] = concept_counts.get(concept, 0) + 1
        
        # Add frequent mistake patterns
        for concept, count in sorted(concept_counts.items(), key=lambda x: x[1], reverse=True)[:3]:
            if count > 1:
                mistake_patterns.append(f"Struggles with {concept}")
        
        return mistake_patterns

    def _identify_performance_strengths(self, assessment_results: List[AssessmentResult]) -> List[str]:
        """Identify student's performance strengths"""
        
        strengths = []
        all_feedback_items = []
        
        for result in assessment_results:
            all_feedback_items.extend(result.feedback_items)
        
        # Analyze correct responses
        correct_items = [item for item in all_feedback_items if item.is_correct]
        
        if len(correct_items) > len(all_feedback_items) * 0.7:  # More than 70% correct
            strengths.append("Consistently accurate responses")
        
        # Check for demonstrated concepts
        all_demonstrated_concepts = []
        for item in correct_items:
            all_demonstrated_concepts.extend(item.concepts_demonstrated)
        
        # Find most common demonstrated concepts
        concept_counts = {}
        for concept in all_demonstrated_concepts:
            concept_counts[concept] = concept_counts.get(concept, 0) + 1
        
        # Add strength patterns
        for concept, count in sorted(concept_counts.items(), key=lambda x: x[1], reverse=True)[:3]:
            if count > 2:
                strengths.append(f"Strong understanding of {concept}")
        
        return strengths

    def _analyze_recent_performance(self, recent_results: List[AssessmentResult]) -> Dict[str, Any]:
        """Analyze recent performance trends"""
        
        if not recent_results:
            return {"trend": "no_data", "average_score": 0.0}
        
        recent_scores = [result.performance_metrics.overall_score for result in recent_results]
        
        return {
            "trend": self._calculate_trend(recent_scores)["direction"],
            "average_score": statistics.mean(recent_scores),
            "best_recent_score": max(recent_scores),
            "most_recent_score": recent_scores[-1] if recent_scores else 0.0,
            "subjects_covered": list(set(result.subject for result in recent_results))
        }

    def _determine_mastery_level(self, subject_results: List[AssessmentResult]) -> DifficultyLevel:
        """Determine mastery level for a subject"""
        
        if not subject_results:
            return DifficultyLevel.BEGINNER
        
        avg_score = statistics.mean(result.performance_metrics.overall_score for result in subject_results)
        
        if avg_score >= 0.8:
            return DifficultyLevel.ADVANCED
        elif avg_score >= 0.6:
            return DifficultyLevel.INTERMEDIATE
        else:
            return DifficultyLevel.BEGINNER

    def _identify_weak_topics(self, subject_results: List[AssessmentResult]) -> List[str]:
        """Identify weak topics in a subject"""
        
        weak_topics = []
        topic_performance = {}
        
        for result in subject_results:
            topic = result.topic
            score = result.performance_metrics.overall_score
            
            if topic not in topic_performance:
                topic_performance[topic] = []
            topic_performance[topic].append(score)
        
        # Identify topics with consistently low scores
        for topic, scores in topic_performance.items():
            avg_score = statistics.mean(scores)
            if avg_score < 0.6:  # Below 60% average
                weak_topics.append(topic)
        
        return weak_topics

    def _identify_strong_topics(self, subject_results: List[AssessmentResult]) -> List[str]:
        """Identify strong topics in a subject"""
        
        strong_topics = []
        topic_performance = {}
        
        for result in subject_results:
            topic = result.topic
            score = result.performance_metrics.overall_score
            
            if topic not in topic_performance:
                topic_performance[topic] = []
            topic_performance[topic].append(score)
        
        # Identify topics with consistently high scores
        for topic, scores in topic_performance.items():
            avg_score = statistics.mean(scores)
            if avg_score >= 0.8:  # Above 80% average
                strong_topics.append(topic)
        
        return strong_topics

    async def _detect_learning_styles(
        self, 
        assessment_results: List[AssessmentResult],
        current_profile: Optional[LearningProfile]
    ) -> List[LearningStyleIndicator]:
        """Detect student's learning styles from performance patterns"""
        
        style_scores = {style: 0.0 for style in LearningStyle}
        style_evidence = {style: [] for style in LearningStyle}
        
        # Analyze performance patterns for style indicators
        for result in assessment_results:
            # Check response patterns that might indicate learning styles
            for feedback_item in result.feedback_items:
                
                # Visual learners might perform better on certain types of questions
                if feedback_item.is_correct and feedback_item.score >= 0.8:
                    # This is a simplified heuristic - in production, use more sophisticated analysis
                    style_scores[LearningStyle.VISUAL] += 0.1
                    style_evidence[LearningStyle.VISUAL].append("High performance on structured questions")
                
                # Reading/writing learners might show specific patterns
                if len(feedback_item.feedback_text) > 100 and feedback_item.is_correct:
                    style_scores[LearningStyle.READING] += 0.1
                    style_evidence[LearningStyle.READING].append("Good performance on text-based questions")
        
        # Convert to indicators with confidence scores
        indicators = []
        total_assessments = len(assessment_results)
        
        for style, score in style_scores.items():
            if total_assessments > 0:
                confidence = min(score / total_assessments, 1.0)
                if confidence > 0.1:  # Only include styles with some evidence
                    indicators.append(LearningStyleIndicator(
                        style=style,
                        confidence=confidence,
                        evidence=style_evidence[style][:3]  # Top 3 pieces of evidence
                    ))
        
        # If no clear style detected, default to multimodal
        if not indicators:
            indicators.append(LearningStyleIndicator(
                style=LearningStyle.MULTIMODAL,
                confidence=0.5,
                evidence=["Balanced performance across different question types"]
            ))
        
        # Sort by confidence
        indicators.sort(key=lambda x: x.confidence, reverse=True)
        
        return indicators[:3]  # Return top 3 detected styles

    async def _update_learning_profile(
        self,
        student_id: str,
        current_profile: Optional[LearningProfile],
        performance_analysis: Dict[str, Any],
        learning_styles: List[LearningStyleIndicator]
    ) -> LearningProfile:
        """Update or create student's learning profile"""
        
        if current_profile:
            # Update existing profile
            updated_profile = current_profile.model_copy()
        else:
            # Create new profile
            updated_profile = LearningProfile(
                student_id=student_id,
                preferred_learning_styles=[],
                learning_pace=LearningPace.MODERATE,
                current_difficulty_level={}
            )
        
        # Update learning styles
        updated_profile.preferred_learning_styles = learning_styles
        
        # Update learning pace based on performance trends
        recent_perf = performance_analysis.get("recent_performance", {})
        if recent_perf.get("trend") == "improving":
            updated_profile.learning_pace = LearningPace.FAST
        elif recent_perf.get("trend") == "declining":
            updated_profile.learning_pace = LearningPace.SLOW
        else:
            updated_profile.learning_pace = LearningPace.MODERATE
        
        # Update difficulty levels per subject
        for subject, perf in performance_analysis.get("subject_performance", {}).items():
            updated_profile.current_difficulty_level[subject] = perf.get("mastery_level", DifficultyLevel.BEGINNER)
            updated_profile.weak_concepts[subject] = perf.get("weak_topics", [])
            updated_profile.strong_concepts[subject] = perf.get("strong_topics", [])
        
        # Update attention span based on time efficiency
        time_analysis = performance_analysis.get("time_efficiency", {})
        avg_time = time_analysis.get("average_time_per_question", 30)  # seconds
        
        # Estimate attention span (rough heuristic)
        if avg_time > 120:  # More than 2 minutes per question
            updated_profile.attention_span_minutes = 15
        elif avg_time < 30:  # Less than 30 seconds per question
            updated_profile.attention_span_minutes = 30
        else:
            updated_profile.attention_span_minutes = 20
        
        updated_profile.last_updated = datetime.utcnow()
        
        return updated_profile

    async def _calculate_difficulty_adjustments(
        self,
        performance_analysis: Dict[str, Any],
        profile: LearningProfile
    ) -> List[DifficultyAdjustment]:
        """Calculate recommended difficulty adjustments"""
        
        adjustments = []
        
        for subject, perf in performance_analysis.get("subject_performance", {}).items():
            current_level = profile.current_difficulty_level.get(subject, DifficultyLevel.BEGINNER)
            avg_score = perf.get("average_score", 0.0)
            trend = perf.get("trend", {}).get("direction", "stable")
            
            # Determine recommended level
            recommended_level = current_level
            confidence = 0.5
            reasoning = "Maintaining current difficulty level"
            adjustment_factors = {
                "accuracy": avg_score,
                "trend": 1.0 if trend == "improving" else -1.0 if trend == "declining" else 0.0,
                "consistency": performance_analysis.get("consistency", {}).get("consistency_score", 0.5)
            }
            
            # Calculate weighted adjustment score
            weighted_score = (
                adjustment_factors["accuracy"] * self.difficulty_weights["accuracy"] +
                (adjustment_factors["trend"] + 1) / 2 * self.difficulty_weights["improvement_trend"] +
                adjustment_factors["consistency"] * self.difficulty_weights["consistency"]
            )
            
            # Determine adjustment
            if weighted_score > 0.8 and current_level != DifficultyLevel.ADVANCED:
                # Increase difficulty
                if current_level == DifficultyLevel.BEGINNER:
                    recommended_level = DifficultyLevel.INTERMEDIATE
                elif current_level == DifficultyLevel.INTERMEDIATE:
                    recommended_level = DifficultyLevel.ADVANCED
                confidence = min(weighted_score, 0.9)
                reasoning = f"Strong performance (score: {avg_score:.2f}) suggests readiness for increased difficulty"
                
            elif weighted_score < 0.4 and current_level != DifficultyLevel.BEGINNER:
                # Decrease difficulty
                if current_level == DifficultyLevel.ADVANCED:
                    recommended_level = DifficultyLevel.INTERMEDIATE
                elif current_level == DifficultyLevel.INTERMEDIATE:
                    recommended_level = DifficultyLevel.BEGINNER
                confidence = min(1.0 - weighted_score, 0.9)
                reasoning = f"Struggling performance (score: {avg_score:.2f}) suggests need for easier content"
            
            adjustment = DifficultyAdjustment(
                subject=subject,
                current_level=current_level,
                recommended_level=recommended_level,
                confidence=confidence,
                reasoning=reasoning,
                adjustment_factors=adjustment_factors
            )
            
            adjustments.append(adjustment)
        
        return adjustments

    async def _generate_content_recommendations(
        self,
        profile: LearningProfile,
        difficulty_adjustments: List[DifficultyAdjustment],
        learning_goals: List[str],
        time_constraints: Optional[int]
    ) -> List[ContentRecommendation]:
        """Generate personalized content recommendations"""
        
        recommendations = []
        available_time = time_constraints or 60  # Default 60 minutes
        
        # Prioritize subjects based on difficulty adjustments and weak concepts
        subject_priorities = {}
        
        for adjustment in difficulty_adjustments:
            subject = adjustment.subject
            
            # Higher priority for subjects that need attention
            if adjustment.recommended_level < adjustment.current_level:
                priority = 1  # Highest priority for struggling subjects
            elif len(profile.weak_concepts.get(subject, [])) > 0:
                priority = 2  # High priority for subjects with weak concepts
            else:
                priority = 3  # Normal priority
            
            subject_priorities[subject] = priority
        
        # Generate recommendations for each subject
        for subject, priority in sorted(subject_priorities.items(), key=lambda x: x[1]):
            
            # Find the appropriate difficulty adjustment
            adjustment = next((adj for adj in difficulty_adjustments if adj.subject == subject), None)
            if not adjustment:
                continue
            
            difficulty = adjustment.recommended_level
            weak_topics = profile.weak_concepts.get(subject, [])
            
            # Recommend review content for weak topics
            if weak_topics:
                for topic in weak_topics[:2]:  # Focus on top 2 weak topics
                    recommendations.append(ContentRecommendation(
                        content_type="review",
                        subject=subject,
                        topic=topic,
                        difficulty_level=DifficultyLevel.BEGINNER,  # Start with easier review
                        estimated_time_minutes=15,
                        learning_objectives=[f"Review and strengthen understanding of {topic}"],
                        recommended_question_types=self._get_preferred_question_types(profile),
                        priority=priority,
                        reasoning=f"Student needs to review {topic} based on recent performance"
                    ))
            
            # Recommend practice content at appropriate difficulty
            recommendations.append(ContentRecommendation(
                content_type="practice",
                subject=subject,
                topic=f"Practice exercises",  # Would be more specific in production
                difficulty_level=difficulty,
                estimated_time_minutes=20,
                learning_objectives=[f"Practice {subject} skills at {difficulty.value} level"],
                recommended_question_types=self._get_preferred_question_types(profile),
                priority=priority,
                reasoning=f"Practice at {difficulty.value} level to build confidence and skills"
            ))
            
            # Stop if we've allocated enough time
            total_time = sum(rec.estimated_time_minutes for rec in recommendations)
            if total_time >= available_time * 0.8:  # Use 80% of available time
                break
        
        # Sort by priority and limit by time
        recommendations.sort(key=lambda x: (x.priority, -x.estimated_time_minutes))
        
        # Ensure we don't exceed time constraints
        final_recommendations = []
        total_time = 0
        
        for rec in recommendations:
            if total_time + rec.estimated_time_minutes <= available_time:
                final_recommendations.append(rec)
                total_time += rec.estimated_time_minutes
            else:
                # Try to fit a shorter version
                remaining_time = available_time - total_time
                if remaining_time >= 10:  # At least 10 minutes
                    rec.estimated_time_minutes = remaining_time
                    final_recommendations.append(rec)
                break
        
        return final_recommendations

    def _get_preferred_question_types(self, profile: LearningProfile) -> List[QuestionType]:
        """Get preferred question types based on learning style"""
        
        preferred_types = []
        
        # Map learning styles to question type preferences
        for style_indicator in profile.preferred_learning_styles:
            if style_indicator.style == LearningStyle.VISUAL:
                preferred_types.extend([QuestionType.MCQ, QuestionType.TRUE_FALSE])
            elif style_indicator.style == LearningStyle.READING:
                preferred_types.extend([QuestionType.SHORT_ANSWER, QuestionType.LONG_ANSWER])
            elif style_indicator.style == LearningStyle.KINESTHETIC:
                preferred_types.extend([QuestionType.FILL_BLANK, QuestionType.SHORT_ANSWER])
            else:  # AUDITORY or MULTIMODAL
                preferred_types.extend([QuestionType.MCQ, QuestionType.SHORT_ANSWER])
        
        # Remove duplicates and return
        return list(set(preferred_types)) if preferred_types else [QuestionType.MCQ, QuestionType.SHORT_ANSWER]

    def _calculate_next_assessment_timing(
        self,
        performance_analysis: Dict[str, Any],
        profile: LearningProfile
    ) -> int:
        """Calculate when the next assessment should occur (in hours)"""
        
        recent_perf = performance_analysis.get("recent_performance", {})
        trend = recent_perf.get("trend", "stable")
        avg_score = recent_perf.get("average_score", 0.5)
        
        base_hours = 24  # Default 24 hours
        
        # Adjust based on performance trend
        if trend == "improving":
            base_hours = 18  # Assess sooner for improving students
        elif trend == "declining":
            base_hours = 12  # Assess sooner for struggling students
        
        # Adjust based on current performance level
        if avg_score < 0.4:
            base_hours = 8   # More frequent assessment for low performers
        elif avg_score > 0.8:
            base_hours = 48  # Less frequent for high performers
        
        # Adjust based on learning pace
        if profile.learning_pace == LearningPace.FAST:
            base_hours = int(base_hours * 0.8)  # 20% sooner
        elif profile.learning_pace == LearningPace.SLOW:
            base_hours = int(base_hours * 1.3)  # 30% later
        
        return max(4, min(base_hours, 72))  # Between 4 hours and 3 days

    def _identify_focus_areas(
        self,
        performance_analysis: Dict[str, Any],
        profile: LearningProfile
    ) -> List[str]:
        """Identify key focus areas for the student"""
        
        focus_areas = []
        
        # Add subjects with weak performance
        for subject, perf in performance_analysis.get("subject_performance", {}).items():
            if perf.get("average_score", 0) < 0.6:
                focus_areas.append(f"Strengthen {subject} fundamentals")
        
        # Add common mistake patterns
        for mistake in performance_analysis.get("common_mistakes", []):
            focus_areas.append(f"Address: {mistake}")
        
        # Add learning pace adjustments
        if profile.learning_pace == LearningPace.SLOW:
            focus_areas.append("Allow extra time for concept mastery")
        elif profile.learning_pace == LearningPace.FAST:
            focus_areas.append("Provide challenging extension activities")
        
        # Add learning style recommendations
        primary_style = profile.preferred_learning_styles[0] if profile.preferred_learning_styles else None
        if primary_style:
            focus_areas.append(f"Incorporate {primary_style.style.value} learning approaches")
        
        return focus_areas[:5]  # Limit to top 5 focus areas

    def _estimate_success_probability(
        self,
        performance_analysis: Dict[str, Any],
        difficulty_adjustments: List[DifficultyAdjustment],
        profile: LearningProfile
    ) -> float:
        """Estimate probability of success with the recommended learning path"""
        
        base_probability = 0.7  # Base 70% success probability
        
        # Adjust based on recent performance trend
        trend = performance_analysis.get("recent_performance", {}).get("trend", "stable")
        if trend == "improving":
            base_probability += 0.15
        elif trend == "declining":
            base_probability -= 0.15
        
        # Adjust based on consistency
        consistency = performance_analysis.get("consistency", {}).get("consistency_score", 0.5)
        base_probability += (consistency - 0.5) * 0.2
        
        # Adjust based on difficulty adjustments
        for adjustment in difficulty_adjustments:
            if adjustment.recommended_level < adjustment.current_level:
                # Reducing difficulty increases success probability
                base_probability += 0.1 * adjustment.confidence
            elif adjustment.recommended_level > adjustment.current_level:
                # Increasing difficulty decreases success probability slightly
                base_probability -= 0.05 * adjustment.confidence
        
        # Adjust based on learning style alignment
        if profile.preferred_learning_styles:
            # Higher confidence in learning style detection increases success probability
            max_style_confidence = max(style.confidence for style in profile.preferred_learning_styles)
            base_probability += max_style_confidence * 0.1
        
        return max(0.1, min(base_probability, 0.95))  # Between 10% and 95%

    async def get_agent_status(self) -> Dict[str, Any]:
        """Get agent status and health"""
        return {
            "name": "AdaptiveLearningAgent",
            "status": "active",
            "models_available": {
                "openai": self.openai_model is not None,
                "anthropic": self.anthropic_model is not None
            },
            "supported_learning_styles": [style.value for style in LearningStyle],
            "supported_learning_paces": [pace.value for pace in LearningPace],
            "supported_difficulty_levels": [level.value for level in DifficultyLevel],
            "curriculum_loaded": self.curriculum is not None,
            "difficulty_weights_configured": len(self.difficulty_weights) > 0,
            "style_indicators_loaded": len(self.style_indicators) > 0
        }