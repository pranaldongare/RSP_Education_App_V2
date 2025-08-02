"""
Assessment Agent - Phase 3 Implementation
Evaluates student responses, provides detailed feedback, and tracks learning progress.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from enum import Enum
import re

from pydantic import BaseModel, Field
import openai
from anthropic import Anthropic

from config.settings import settings
from core.curriculum import CBSECurriculum
from core.exceptions import AgentException
from agents.content_generator import DifficultyLevel, QuestionType, GeneratedQuestion


class AssessmentType(str, Enum):
    """Types of assessments"""
    FORMATIVE = "formative"  # Ongoing assessment during learning
    SUMMATIVE = "summative"  # Final assessment after learning
    DIAGNOSTIC = "diagnostic"  # Initial assessment to identify gaps
    SELF_ASSESSMENT = "self_assessment"  # Student self-evaluation


class FeedbackLevel(str, Enum):
    """Levels of feedback detail"""
    BASIC = "basic"  # Simple correct/incorrect
    DETAILED = "detailed"  # Explanation of why answer is right/wrong
    COMPREHENSIVE = "comprehensive"  # Detailed explanation + learning suggestions


class ScoreType(str, Enum):
    """Types of scoring methods"""
    BINARY = "binary"  # 0 or 1 (correct/incorrect)
    PARTIAL = "partial"  # Partial credit (0.0 to 1.0)
    RUBRIC = "rubric"  # Multi-criteria scoring
    HOLISTIC = "holistic"  # Overall qualitative assessment


class StudentResponse(BaseModel):
    """Student's response to a question"""
    question_id: str = Field(..., description="Unique identifier for the question")
    student_answer: str = Field(..., description="Student's submitted answer")
    question_text: str = Field(..., description="Original question text")
    correct_answer: str = Field(..., description="Expected correct answer")
    question_type: QuestionType = Field(..., description="Type of question")
    options: Optional[List[str]] = Field(default=None, description="Options for MCQ")
    context: Optional[str] = Field(default=None, description="Additional context")
    time_taken: Optional[int] = Field(default=None, description="Time taken in seconds")
    attempt_number: int = Field(default=1, description="Which attempt this is")


class AssessmentRequest(BaseModel):
    """Request for assessing student responses"""
    student_id: str = Field(..., description="Unique student identifier")
    responses: List[StudentResponse] = Field(..., description="List of student responses")
    assessment_type: AssessmentType = Field(..., description="Type of assessment")
    feedback_level: FeedbackLevel = Field(default=FeedbackLevel.DETAILED)
    score_type: ScoreType = Field(default=ScoreType.PARTIAL)
    subject: str = Field(..., description="Subject being assessed")
    grade: int = Field(..., ge=1, le=12, description="Student's grade level")
    topic: str = Field(..., description="Topic being assessed")


class FeedbackItem(BaseModel):
    """Individual feedback item for a response"""
    question_id: str
    is_correct: bool
    score: float = Field(..., ge=0.0, le=1.0, description="Score between 0.0 and 1.0")
    feedback_text: str
    explanation: str
    improvement_suggestions: List[str]
    concepts_demonstrated: List[str]
    concepts_to_review: List[str]
    difficulty_assessment: DifficultyLevel


class PerformanceMetrics(BaseModel):
    """Overall performance metrics for the assessment"""
    total_questions: int
    correct_answers: int
    partial_credit_answers: int
    incorrect_answers: int
    overall_score: float = Field(..., ge=0.0, le=1.0)
    completion_time: Optional[int] = Field(default=None, description="Total time in seconds")
    subject_mastery_level: DifficultyLevel
    strengths: List[str]
    areas_for_improvement: List[str]
    recommended_next_topics: List[str]


class AssessmentResult(BaseModel):
    """Complete assessment result"""
    student_id: str
    assessment_id: str
    assessment_type: AssessmentType
    subject: str
    grade: int
    topic: str
    feedback_items: List[FeedbackItem]
    performance_metrics: PerformanceMetrics
    overall_feedback: str
    learning_path_adjustments: List[str]
    confidence_indicators: Dict[str, float]
    assessed_at: datetime
    assessor_notes: Optional[str] = None


class LearningProgress(BaseModel):
    """Learning progress tracking"""
    concept: str
    mastery_level: float = Field(..., ge=0.0, le=1.0)
    attempts_count: int
    improvement_rate: float
    last_assessment_score: float
    recommended_practice_time: int  # in minutes


class AssessmentAgent:
    """
    Assessment Agent for evaluating student responses and providing feedback
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.AssessmentAgent")
        self.curriculum = CBSECurriculum()
        self.openai_model = None
        self.anthropic_model = None
        self._initialize_models()
        
        # Assessment scoring weights
        self.scoring_weights = {
            QuestionType.MCQ: {"exact_match": 1.0, "partial": 0.0},
            QuestionType.TRUE_FALSE: {"exact_match": 1.0, "partial": 0.0},
            QuestionType.FILL_BLANK: {"exact_match": 1.0, "partial": 0.5},
            QuestionType.SHORT_ANSWER: {"exact_match": 1.0, "partial": 0.7, "conceptual": 0.5},
            QuestionType.LONG_ANSWER: {"exact_match": 1.0, "partial": 0.8, "conceptual": 0.6}
        }
        
    def _initialize_models(self):
        """Initialize AI models for assessment"""
        try:
            if hasattr(settings, 'openai_api_key') and settings.openai_api_key:
                openai.api_key = settings.openai_api_key
                self.openai_model = "gpt-4-turbo-preview"
                
            if hasattr(settings, 'anthropic_api_key') and settings.anthropic_api_key:
                self.anthropic_model = Anthropic(api_key=settings.anthropic_api_key)
                
            self.logger.info("Assessment AI models initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize AI models: {e}")
            self.logger.warning("Continuing without AI models for testing purposes")

    async def assess_responses(self, request: AssessmentRequest) -> AssessmentResult:
        """
        Main method to assess student responses and generate comprehensive feedback
        """
        try:
            self.logger.info(f"Assessing {len(request.responses)} responses for student {request.student_id}")
            
            # Validate curriculum alignment
            curriculum_data = await self.curriculum.get_topic_details(
                subject=request.subject,
                grade=request.grade,
                topic=request.topic
            )
            
            if not curriculum_data:
                raise AgentException(f"Topic '{request.topic}' not found in CBSE curriculum")
            
            # Assess each response
            feedback_items = []
            for response in request.responses:
                feedback_item = await self._assess_single_response(
                    response, request.feedback_level, request.score_type, curriculum_data
                )
                feedback_items.append(feedback_item)
            
            # Calculate performance metrics
            performance_metrics = self._calculate_performance_metrics(
                feedback_items, request, curriculum_data
            )
            
            # Generate overall feedback and recommendations
            overall_feedback = await self._generate_overall_feedback(
                feedback_items, performance_metrics, request
            )
            
            # Create assessment result
            assessment_result = AssessmentResult(
                student_id=request.student_id,
                assessment_id=f"assessment_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{request.student_id}",
                assessment_type=request.assessment_type,
                subject=request.subject,
                grade=request.grade,
                topic=request.topic,
                feedback_items=feedback_items,
                performance_metrics=performance_metrics,
                overall_feedback=overall_feedback,
                learning_path_adjustments=self._generate_learning_adjustments(
                    performance_metrics, curriculum_data
                ),
                confidence_indicators=self._calculate_confidence_indicators(feedback_items),
                assessed_at=datetime.utcnow()
            )
            
            self.logger.info(f"Assessment completed for student {request.student_id}")
            return assessment_result
            
        except Exception as e:
            self.logger.error(f"Assessment failed: {e}")
            raise AgentException(f"Assessment failed: {e}")

    async def _assess_single_response(
        self, 
        response: StudentResponse, 
        feedback_level: FeedbackLevel,
        score_type: ScoreType,
        curriculum_data: Dict[str, Any]
    ) -> FeedbackItem:
        """Assess a single student response"""
        
        # Calculate score based on answer correctness
        score, is_correct = self._calculate_answer_score(response, score_type)
        
        # Generate feedback based on level requested
        feedback_text = await self._generate_feedback_text(
            response, score, feedback_level, curriculum_data
        )
        
        # Generate detailed explanation
        explanation = await self._generate_explanation(response, curriculum_data)
        
        # Identify concepts demonstrated and areas to review
        concepts_demonstrated = self._identify_demonstrated_concepts(response, is_correct)
        concepts_to_review = self._identify_review_concepts(response, is_correct)
        
        # Generate improvement suggestions
        improvement_suggestions = self._generate_improvement_suggestions(
            response, score, concepts_to_review
        )
        
        # Assess difficulty level understanding
        difficulty_assessment = self._assess_difficulty_understanding(response, score)
        
        return FeedbackItem(
            question_id=response.question_id,
            is_correct=is_correct,
            score=score,
            feedback_text=feedback_text,
            explanation=explanation,
            improvement_suggestions=improvement_suggestions,
            concepts_demonstrated=concepts_demonstrated,
            concepts_to_review=concepts_to_review,
            difficulty_assessment=difficulty_assessment
        )

    def _calculate_answer_score(self, response: StudentResponse, score_type: ScoreType) -> tuple[float, bool]:
        """Calculate score for a student's answer"""
        
        student_answer = response.student_answer.strip().lower()
        correct_answer = response.correct_answer.strip().lower()
        
        if score_type == ScoreType.BINARY:
            # Simple exact match for binary scoring
            is_correct = student_answer == correct_answer
            return (1.0 if is_correct else 0.0, is_correct)
        
        elif score_type == ScoreType.PARTIAL:
            # Partial credit based on question type
            return self._calculate_partial_score(response)
            
        elif score_type == ScoreType.RUBRIC:
            # Multi-criteria scoring (simplified for now)
            return self._calculate_rubric_score(response)
            
        else:  # HOLISTIC
            # Holistic assessment (simplified for now)
            return self._calculate_holistic_score(response)

    def _calculate_partial_score(self, response: StudentResponse) -> tuple[float, bool]:
        """Calculate partial score based on answer quality"""
        
        student_answer = response.student_answer.strip().lower()
        correct_answer = response.correct_answer.strip().lower()
        
        # Exact match gets full score
        if student_answer == correct_answer:
            return (1.0, True)
        
        # Question type specific scoring
        if response.question_type == QuestionType.MCQ:
            # MCQ is typically binary
            return (0.0, False)
            
        elif response.question_type == QuestionType.TRUE_FALSE:
            # True/False is binary
            return (0.0, False)
            
        elif response.question_type == QuestionType.FILL_BLANK:
            # Check for partial matches in fill blanks
            score = self._calculate_fill_blank_score(student_answer, correct_answer)
            return (score, score >= 0.5)
            
        elif response.question_type in [QuestionType.SHORT_ANSWER, QuestionType.LONG_ANSWER]:
            # Semantic similarity for text answers
            score = self._calculate_text_similarity_score(student_answer, correct_answer)
            return (score, score >= 0.6)
        
        return (0.0, False)

    def _calculate_fill_blank_score(self, student_answer: str, correct_answer: str) -> float:
        """Calculate score for fill-in-the-blank questions"""
        
        # Split answers into words and compare
        student_words = set(student_answer.split())
        correct_words = set(correct_answer.split())
        
        if not correct_words:
            return 1.0 if not student_words else 0.0
        
        # Calculate Jaccard similarity
        intersection = len(student_words.intersection(correct_words))
        union = len(student_words.union(correct_words))
        
        return intersection / union if union > 0 else 0.0

    def _calculate_text_similarity_score(self, student_answer: str, correct_answer: str) -> float:
        """Calculate similarity score for text-based answers"""
        
        # Simple keyword-based similarity (in production, use more sophisticated NLP)
        student_keywords = self._extract_keywords(student_answer)
        correct_keywords = self._extract_keywords(correct_answer)
        
        if not correct_keywords:
            return 1.0 if not student_keywords else 0.0
        
        # Calculate keyword overlap
        common_keywords = len(student_keywords.intersection(correct_keywords))
        total_keywords = len(correct_keywords)
        
        keyword_score = common_keywords / total_keywords
        
        # If no keywords match, return 0.0 (completely incorrect)
        if keyword_score == 0.0:
            return 0.0
        
        # Adjust based on answer length appropriateness
        length_score = min(len(student_answer) / max(len(correct_answer), 1), 2.0)
        if length_score > 1.5:
            length_score = 1.0 - (length_score - 1.5)  # Penalize overly long answers
        
        return min((keyword_score * 0.8) + (length_score * 0.2), 1.0)

    def _extract_keywords(self, text: str) -> set:
        """Extract keywords from text (simplified implementation)"""
        
        # Remove common stop words and extract meaningful words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'
        }
        
        words = re.findall(r'\b\w+\b', text.lower())
        keywords = {word for word in words if len(word) > 2 and word not in stop_words}
        
        return keywords

    def _calculate_rubric_score(self, response: StudentResponse) -> tuple[float, bool]:
        """Calculate score using rubric-based assessment"""
        # Simplified rubric scoring - in production, this would be more sophisticated
        base_score, is_correct = self._calculate_partial_score(response)
        
        # Adjust based on response quality factors
        quality_factors = {
            'completeness': self._assess_completeness(response),
            'clarity': self._assess_clarity(response),
            'accuracy': base_score
        }
        
        weighted_score = (
            quality_factors['completeness'] * 0.3 +
            quality_factors['clarity'] * 0.2 +
            quality_factors['accuracy'] * 0.5
        )
        
        return (weighted_score, weighted_score >= 0.6)

    def _calculate_holistic_score(self, response: StudentResponse) -> tuple[float, bool]:
        """Calculate holistic score considering overall response quality"""
        # Start with partial score
        base_score, _ = self._calculate_partial_score(response)
        
        # Adjust based on overall understanding demonstration
        understanding_factors = [
            self._assess_conceptual_understanding(response),
            self._assess_problem_solving_approach(response),
            self._assess_communication_clarity(response)
        ]
        
        holistic_score = (base_score * 0.6) + (sum(understanding_factors) / len(understanding_factors) * 0.4)
        
        return (min(holistic_score, 1.0), holistic_score >= 0.6)

    def _assess_completeness(self, response: StudentResponse) -> float:
        """Assess completeness of the response"""
        if len(response.student_answer.strip()) == 0:
            return 0.0
        
        # Simple heuristic based on answer length relative to expected
        min_expected_length = max(len(response.correct_answer) * 0.5, 10)
        actual_length = len(response.student_answer)
        
        if actual_length >= min_expected_length:
            return 1.0
        else:
            return actual_length / min_expected_length

    def _assess_clarity(self, response: StudentResponse) -> float:
        """Assess clarity of the response"""
        answer = response.student_answer.strip()
        
        if not answer:
            return 0.0
        
        # Simple clarity metrics
        sentence_count = len([s for s in answer.split('.') if s.strip()])
        word_count = len(answer.split())
        
        if word_count == 0:
            return 0.0
        
        # Prefer concise but complete answers
        avg_sentence_length = word_count / max(sentence_count, 1)
        
        clarity_score = 1.0
        if avg_sentence_length > 25:  # Very long sentences might be unclear
            clarity_score *= 0.8
        if sentence_count > 5 and response.question_type == QuestionType.SHORT_ANSWER:
            clarity_score *= 0.9  # Short answers should be concise
        
        return min(clarity_score, 1.0)

    def _assess_conceptual_understanding(self, response: StudentResponse) -> float:
        """Assess conceptual understanding from the response"""
        # Simplified assessment - in production, use more sophisticated analysis
        
        answer = response.student_answer.lower()
        correct = response.correct_answer.lower()
        
        # Look for key conceptual terms
        conceptual_terms = self._extract_keywords(correct)
        student_terms = self._extract_keywords(answer)
        
        if not conceptual_terms:
            return 0.5
        
        concept_overlap = len(student_terms.intersection(conceptual_terms))
        return min(concept_overlap / len(conceptual_terms), 1.0)

    def _assess_problem_solving_approach(self, response: StudentResponse) -> float:
        """Assess problem-solving approach in the response"""
        # Look for indicators of systematic thinking
        
        answer = response.student_answer.lower()
        
        problem_solving_indicators = [
            'first', 'then', 'next', 'finally', 'because', 'therefore', 
            'step', 'method', 'approach', 'solve', 'calculate'
        ]
        
        found_indicators = sum(1 for indicator in problem_solving_indicators if indicator in answer)
        
        return min(found_indicators / 3, 1.0)  # Normalize to 0-1

    def _assess_communication_clarity(self, response: StudentResponse) -> float:
        """Assess how clearly the student communicated their answer"""
        return self._assess_clarity(response)  # Use existing clarity assessment

    async def _generate_feedback_text(
        self, 
        response: StudentResponse,
        score: float,
        feedback_level: FeedbackLevel,
        curriculum_data: Dict[str, Any]
    ) -> str:
        """Generate feedback text based on the response and feedback level"""
        
        if feedback_level == FeedbackLevel.BASIC:
            return "Correct!" if score >= 0.6 else "Incorrect. Please review and try again."
        
        elif feedback_level == FeedbackLevel.DETAILED:
            return await self._generate_detailed_feedback(response, score, curriculum_data)
        
        else:  # COMPREHENSIVE
            return await self._generate_comprehensive_feedback(response, score, curriculum_data)

    async def _generate_detailed_feedback(
        self, 
        response: StudentResponse, 
        score: float,
        curriculum_data: Dict[str, Any]
    ) -> str:
        """Generate detailed feedback (test mode implementation)"""
        
        if score >= 0.8:
            feedback = f"Excellent work! Your answer demonstrates a strong understanding of {response.question_text}. "
        elif score >= 0.6:
            feedback = f"Good attempt! You show understanding of the key concepts, but there are some areas for improvement. "
        elif score >= 0.3:
            feedback = f"Partial understanding shown. Your answer has some correct elements but needs refinement. "
        else:
            feedback = f"This answer needs significant improvement. Let's review the key concepts together. "
        
        # Add specific guidance
        if response.question_type == QuestionType.MCQ:
            if score < 1.0:
                feedback += "Review the question carefully and consider each option before selecting."
        elif response.question_type in [QuestionType.SHORT_ANSWER, QuestionType.LONG_ANSWER]:
            if score < 0.8:
                feedback += "Try to include more specific details and use appropriate terminology."
        
        feedback += f" The correct answer is: {response.correct_answer}"
        
        return feedback

    async def _generate_comprehensive_feedback(
        self, 
        response: StudentResponse, 
        score: float,
        curriculum_data: Dict[str, Any]
    ) -> str:
        """Generate comprehensive feedback with learning suggestions"""
        
        detailed_feedback = await self._generate_detailed_feedback(response, score, curriculum_data)
        
        # Add learning suggestions
        learning_suggestions = f"\n\nLearning Suggestions:\n"
        
        if score < 0.5:
            learning_suggestions += f"- Review the key concepts in {curriculum_data.get('chapter', 'this topic')}\n"
            learning_suggestions += f"- Practice similar problems to strengthen understanding\n"
            learning_suggestions += f"- Ask for help if you're confused about any part\n"
        elif score < 0.8:
            learning_suggestions += f"- You're on the right track! Focus on being more precise\n"
            learning_suggestions += f"- Review specific terminology and definitions\n"
            learning_suggestions += f"- Practice explaining your reasoning step-by-step\n"
        else:
            learning_suggestions += f"- Excellent understanding! Try more challenging problems\n"
            learning_suggestions += f"- Help explain concepts to classmates\n"
            learning_suggestions += f"- Explore real-world applications of this topic\n"
        
        return detailed_feedback + learning_suggestions

    async def _generate_explanation(
        self, 
        response: StudentResponse,
        curriculum_data: Dict[str, Any]
    ) -> str:
        """Generate explanation for the correct answer"""
        
        explanation = f"Explanation for: {response.question_text}\n\n"
        explanation += f"The correct answer is '{response.correct_answer}' because:\n"
        
        # Add context-specific explanation based on question type
        if response.question_type == QuestionType.MCQ:
            explanation += f"This option correctly addresses all aspects of the question. "
            if response.options:
                explanation += f"The other options are incorrect because they either contain factual errors or don't fully answer the question."
        
        elif response.question_type in [QuestionType.SHORT_ANSWER, QuestionType.LONG_ANSWER]:
            explanation += f"This answer demonstrates understanding of the key concepts and provides appropriate examples or reasoning."
        
        elif response.question_type == QuestionType.FILL_BLANK:
            explanation += f"This term/phrase correctly completes the sentence and aligns with the concepts being tested."
        
        elif response.question_type == QuestionType.TRUE_FALSE:
            explanation += f"This statement is {response.correct_answer} based on the principles covered in {curriculum_data.get('chapter', 'this topic')}."
        
        explanation += f"\n\nThis concept is important because it helps you understand {curriculum_data.get('name', 'the topic')} and builds toward more advanced topics."
        
        return explanation

    def _identify_demonstrated_concepts(self, response: StudentResponse, is_correct: bool) -> List[str]:
        """Identify concepts the student demonstrated understanding of"""
        
        concepts = []
        
        if is_correct:
            # Basic concept understanding
            concepts.append(f"Basic understanding of {response.question_text}")
            
            # Question-type specific concepts
            if response.question_type == QuestionType.MCQ:
                concepts.append("Multiple choice reasoning")
            elif response.question_type in [QuestionType.SHORT_ANSWER, QuestionType.LONG_ANSWER]:
                concepts.append("Written communication of ideas")
                if len(response.student_answer) > 50:
                    concepts.append("Detailed explanation ability")
        
        # Partial understanding concepts
        if not is_correct and len(response.student_answer.strip()) > 0:
            concepts.append("Attempted problem solving")
            concepts.append("Basic engagement with the material")
        
        return concepts

    def _identify_review_concepts(self, response: StudentResponse, is_correct: bool) -> List[str]:
        """Identify concepts that need review"""
        
        concepts_to_review = []
        
        if not is_correct:
            # Basic concepts that need review
            concepts_to_review.append(f"Core concepts in {response.question_text}")
            
            # Question-type specific review areas
            if response.question_type == QuestionType.MCQ:
                concepts_to_review.append("Careful reading and option analysis")
            elif response.question_type in [QuestionType.SHORT_ANSWER, QuestionType.LONG_ANSWER]:
                concepts_to_review.append("Structured answer writing")
                concepts_to_review.append("Use of appropriate terminology")
            elif response.question_type == QuestionType.FILL_BLANK:
                concepts_to_review.append("Key vocabulary and definitions")
        
        return concepts_to_review

    def _generate_improvement_suggestions(
        self, 
        response: StudentResponse, 
        score: float,
        concepts_to_review: List[str]
    ) -> List[str]:
        """Generate specific improvement suggestions"""
        
        suggestions = []
        
        if score < 0.3:
            suggestions.extend([
                "Review the fundamental concepts before attempting similar questions",
                "Ask for help from a teacher or tutor to clarify confusing points",
                "Practice basic problems to build confidence"
            ])
        elif score < 0.6:
            suggestions.extend([
                "Take more time to read questions carefully",
                "Practice explaining your reasoning step-by-step",
                "Review specific terminology and definitions"
            ])
        elif score < 0.9:
            suggestions.extend([
                "Focus on precision and completeness in your answers",
                "Double-check your work before submitting",
                "Practice more challenging problems to deepen understanding"
            ])
        
        # Question-type specific suggestions
        if response.question_type == QuestionType.MCQ and score < 0.5:
            suggestions.append("Eliminate obviously incorrect options before choosing")
        elif response.question_type in [QuestionType.SHORT_ANSWER, QuestionType.LONG_ANSWER]:
            if len(response.student_answer) < 20:
                suggestions.append("Provide more detailed explanations in your answers")
        
        return suggestions

    def _assess_difficulty_understanding(self, response: StudentResponse, score: float) -> DifficultyLevel:
        """Assess what difficulty level the student can handle"""
        
        if score >= 0.8:
            return DifficultyLevel.ADVANCED
        elif score >= 0.6:
            return DifficultyLevel.INTERMEDIATE
        else:
            return DifficultyLevel.BEGINNER

    def _calculate_performance_metrics(
        self, 
        feedback_items: List[FeedbackItem],
        request: AssessmentRequest,
        curriculum_data: Dict[str, Any]
    ) -> PerformanceMetrics:
        """Calculate overall performance metrics"""
        
        total_questions = len(feedback_items)
        if total_questions == 0:
            raise AgentException("No questions to assess")
        
        correct_answers = sum(1 for item in feedback_items if item.is_correct)
        partial_credit_answers = sum(1 for item in feedback_items if 0.3 <= item.score < 1.0 and not item.is_correct)
        incorrect_answers = total_questions - correct_answers - partial_credit_answers
        
        overall_score = sum(item.score for item in feedback_items) / total_questions
        
        # Calculate completion time if provided
        completion_time = None
        if any(response.time_taken for response in request.responses):
            completion_time = sum(response.time_taken or 0 for response in request.responses)
        
        # Assess subject mastery level
        if overall_score >= 0.8:
            subject_mastery_level = DifficultyLevel.ADVANCED
        elif overall_score >= 0.6:
            subject_mastery_level = DifficultyLevel.INTERMEDIATE
        else:
            subject_mastery_level = DifficultyLevel.BEGINNER
        
        # Identify strengths and areas for improvement
        strengths = self._identify_strengths(feedback_items, overall_score)
        areas_for_improvement = self._identify_improvement_areas(feedback_items, overall_score)
        recommended_next_topics = self._recommend_next_topics(
            overall_score, request.subject, request.grade, curriculum_data
        )
        
        return PerformanceMetrics(
            total_questions=total_questions,
            correct_answers=correct_answers,
            partial_credit_answers=partial_credit_answers,
            incorrect_answers=incorrect_answers,
            overall_score=overall_score,
            completion_time=completion_time,
            subject_mastery_level=subject_mastery_level,
            strengths=strengths,
            areas_for_improvement=areas_for_improvement,
            recommended_next_topics=recommended_next_topics
        )

    def _identify_strengths(self, feedback_items: List[FeedbackItem], overall_score: float) -> List[str]:
        """Identify student's strengths based on performance"""
        
        strengths = []
        
        if overall_score >= 0.8:
            strengths.append("Strong overall understanding of the topic")
        
        # Analyze by question types
        question_type_scores = {}
        for item in feedback_items:
            # We need to track question types - for now, use a placeholder
            # In real implementation, this would come from the response data
            strengths.append("Consistent performance across different question types")
        
        # Analyze concepts demonstrated
        all_concepts = []
        for item in feedback_items:
            all_concepts.extend(item.concepts_demonstrated)
        
        if len(all_concepts) > len(feedback_items):
            strengths.append("Good conceptual understanding")
        
        if not strengths:
            strengths.append("Shows effort and engagement with the material")
        
        return strengths

    def _identify_improvement_areas(self, feedback_items: List[FeedbackItem], overall_score: float) -> List[str]:
        """Identify areas that need improvement"""
        
        areas = []
        
        if overall_score < 0.5:
            areas.append("Fundamental concept understanding needs strengthening")
        elif overall_score < 0.7:
            areas.append("Focus on accuracy and attention to detail")
        
        # Collect all concepts to review
        all_review_concepts = []
        for item in feedback_items:
            all_review_concepts.extend(item.concepts_to_review)
        
        # Find most common review areas
        concept_counts = {}
        for concept in all_review_concepts:
            concept_counts[concept] = concept_counts.get(concept, 0) + 1
        
        # Add most common issues
        for concept, count in sorted(concept_counts.items(), key=lambda x: x[1], reverse=True)[:3]:
            if count > 1:  # Only include if it's a pattern
                areas.append(concept)
        
        return areas

    def _recommend_next_topics(
        self, 
        overall_score: float,
        subject: str,
        grade: int,
        curriculum_data: Dict[str, Any]
    ) -> List[str]:
        """Recommend next topics based on performance"""
        
        recommendations = []
        
        if overall_score >= 0.8:
            recommendations.extend([
                "Advanced topics in the same subject area",
                "Real-world application problems",
                "Cross-curricular connections"
            ])
        elif overall_score >= 0.6:
            recommendations.extend([
                "More practice problems at the same level",
                "Review and strengthen weaker areas",
                "Gradually introduce more challenging concepts"
            ])
        else:
            recommendations.extend([
                "Review fundamental concepts",
                "Additional practice with guided support",
                "One-on-one tutoring if available"
            ])
        
        return recommendations

    async def _generate_overall_feedback(
        self,
        feedback_items: List[FeedbackItem],
        performance_metrics: PerformanceMetrics,
        request: AssessmentRequest
    ) -> str:
        """Generate overall feedback for the assessment"""
        
        overall_feedback = f"Assessment Summary for {request.subject} - {request.topic}\n\n"
        
        # Performance summary
        overall_feedback += f"You answered {performance_metrics.correct_answers} out of {performance_metrics.total_questions} questions correctly "
        overall_feedback += f"({performance_metrics.overall_score:.1%} overall score).\n\n"
        
        # Personalized message based on performance
        if performance_metrics.overall_score >= 0.8:
            overall_feedback += "Excellent work! You demonstrate a strong understanding of this topic. "
        elif performance_metrics.overall_score >= 0.6:
            overall_feedback += "Good progress! You show solid understanding with room for improvement. "
        else:
            overall_feedback += "Keep working! This topic needs more attention and practice. "
        
        # Strengths
        if performance_metrics.strengths:
            overall_feedback += f"\n\nYour strengths include:\n"
            for strength in performance_metrics.strengths:
                overall_feedback += f"• {strength}\n"
        
        # Areas for improvement
        if performance_metrics.areas_for_improvement:
            overall_feedback += f"\nAreas to focus on:\n"
            for area in performance_metrics.areas_for_improvement:
                overall_feedback += f"• {area}\n"
        
        # Next steps
        overall_feedback += f"\nRecommended next steps:\n"
        for recommendation in performance_metrics.recommended_next_topics:
            overall_feedback += f"• {recommendation}\n"
        
        return overall_feedback

    def _generate_learning_adjustments(
        self,
        performance_metrics: PerformanceMetrics,
        curriculum_data: Dict[str, Any]
    ) -> List[str]:
        """Generate learning path adjustments based on assessment"""
        
        adjustments = []
        
        if performance_metrics.overall_score >= 0.8:
            adjustments.extend([
                "Increase difficulty level for future content",
                "Introduce advanced concepts earlier",
                "Provide enrichment activities"
            ])
        elif performance_metrics.overall_score >= 0.6:
            adjustments.extend([
                "Continue at current difficulty level",
                "Provide additional practice in weak areas",
                "Reinforce concepts before moving forward"
            ])
        else:
            adjustments.extend([
                "Reduce difficulty level temporarily",
                "Provide more foundational support",
                "Increase practice time and repetition",
                "Consider additional tutoring support"
            ])
        
        return adjustments

    def _calculate_confidence_indicators(self, feedback_items: List[FeedbackItem]) -> Dict[str, float]:
        """Calculate confidence indicators for different aspects"""
        
        indicators = {
            "overall_confidence": sum(item.score for item in feedback_items) / len(feedback_items) if feedback_items else 0.0,
            "concept_mastery": len([item for item in feedback_items if item.score >= 0.8]) / len(feedback_items) if feedback_items else 0.0,
            "consistency": 1.0 - (max([item.score for item in feedback_items]) - min([item.score for item in feedback_items])) if feedback_items else 0.0,
        }
        
        # Add question-type specific confidence if we have varied question types
        # This would be enhanced with actual question type tracking
        indicators["multiple_choice_confidence"] = indicators["overall_confidence"]
        indicators["written_response_confidence"] = indicators["overall_confidence"]
        
        return indicators

    async def track_learning_progress(
        self, 
        student_id: str,
        assessment_results: List[AssessmentResult]
    ) -> List[LearningProgress]:
        """Track learning progress over multiple assessments"""
        
        if not assessment_results:
            return []
        
        # Group by concepts and track progress
        concept_progress = {}
        
        for result in assessment_results:
            for feedback_item in result.feedback_items:
                for concept in feedback_item.concepts_demonstrated:
                    if concept not in concept_progress:
                        concept_progress[concept] = {
                            'scores': [],
                            'attempts': 0,
                            'last_score': 0.0
                        }
                    
                    concept_progress[concept]['scores'].append(feedback_item.score)
                    concept_progress[concept]['attempts'] += 1
                    concept_progress[concept]['last_score'] = feedback_item.score
        
        # Create progress tracking objects
        progress_list = []
        for concept, data in concept_progress.items():
            scores = data['scores']
            
            # Calculate improvement rate
            if len(scores) > 1:
                improvement_rate = (scores[-1] - scores[0]) / len(scores)
            else:
                improvement_rate = 0.0
            
            # Calculate mastery level (average of recent scores)
            recent_scores = scores[-3:] if len(scores) >= 3 else scores
            mastery_level = sum(recent_scores) / len(recent_scores)
            
            # Recommend practice time based on mastery level
            if mastery_level >= 0.8:
                practice_time = 5  # Minimal practice needed
            elif mastery_level >= 0.6:
                practice_time = 15  # Moderate practice
            else:
                practice_time = 30  # Significant practice needed
            
            progress = LearningProgress(
                concept=concept,
                mastery_level=mastery_level,
                attempts_count=data['attempts'],
                improvement_rate=improvement_rate,
                last_assessment_score=data['last_score'],
                recommended_practice_time=practice_time
            )
            
            progress_list.append(progress)
        
        return progress_list

    async def get_agent_status(self) -> Dict[str, Any]:
        """Get agent status and health"""
        return {
            "name": "AssessmentAgent",
            "status": "active",
            "models_available": {
                "openai": self.openai_model is not None,
                "anthropic": self.anthropic_model is not None
            },
            "supported_assessment_types": [at.value for at in AssessmentType],
            "supported_feedback_levels": [fl.value for fl in FeedbackLevel],
            "supported_score_types": [st.value for st in ScoreType],
            "curriculum_loaded": self.curriculum is not None,
            "scoring_weights_configured": len(self.scoring_weights) > 0
        }