"""
Content Generator Agent - Phase 2 Implementation
Generates CBSE curriculum-aligned educational content, questions, and explanations.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field
# AI Model imports - Phase 2 implementation (simplified for testing)
# TODO: Fix LangChain dependency version conflicts
# from langchain_openai import ChatOpenAI
# from langchain_anthropic import ChatAnthropic
# from langchain.schema import HumanMessage, SystemMessage
# from langchain.prompts import PromptTemplate
import openai
from anthropic import Anthropic

from config.settings import settings
from core.curriculum import CBSECurriculum
from core.exceptions import AgentException


class DifficultyLevel(str, Enum):
    """Content difficulty levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate" 
    ADVANCED = "advanced"


class ContentType(str, Enum):
    """Types of content to generate"""
    EXPLANATION = "explanation"
    EXAMPLE = "example"
    EXERCISE = "exercise"
    ASSESSMENT = "assessment"


class QuestionType(str, Enum):
    """Types of questions to generate"""
    MCQ = "multiple_choice"
    SHORT_ANSWER = "short_answer"
    LONG_ANSWER = "long_answer"
    FILL_BLANK = "fill_blank"
    TRUE_FALSE = "true_false"


class ContentRequest(BaseModel):
    """Request model for content generation"""
    subject: str = Field(..., description="Subject name (Math, Science, English, Social Studies)")
    grade: int = Field(..., ge=1, le=12, description="Grade level (1-12)")
    topic: str = Field(..., description="Specific topic within the subject")
    content_type: ContentType = Field(..., description="Type of content to generate")
    difficulty: DifficultyLevel = Field(default=DifficultyLevel.INTERMEDIATE)
    student_context: Optional[Dict[str, Any]] = Field(default=None, description="Student's learning context")
    learning_objectives: Optional[List[str]] = Field(default=None, description="Specific learning objectives")
    
    # Optional fields added by API endpoint for user context
    student_id: Optional[str] = Field(default=None, description="Student ID from authentication")
    student_grade: Optional[str] = Field(default=None, description="Student's current grade")
    preferred_language: Optional[str] = Field(default=None, description="Student's preferred language")
    learning_style: Optional[str] = Field(default=None, description="Student's learning style")


class QuestionRequest(BaseModel):
    """Request model for question generation"""
    subject: str
    grade: int = Field(..., ge=1, le=12)
    topic: str
    question_type: QuestionType
    difficulty: DifficultyLevel = Field(default=DifficultyLevel.INTERMEDIATE)
    num_questions: int = Field(default=1, ge=1, le=10)
    context: Optional[str] = Field(default=None, description="Context or passage for questions")


class GeneratedContent(BaseModel):
    """Generated content response model"""
    content: str
    content_type: ContentType
    subject: str
    grade: int
    topic: str
    difficulty: DifficultyLevel
    learning_objectives: List[str]
    estimated_time: int  # in minutes
    prerequisites: List[str]
    generated_at: datetime
    metadata: Dict[str, Any]


class GeneratedQuestion(BaseModel):
    """Generated question response model"""
    question: str
    question_type: QuestionType
    options: Optional[List[str]] = None  # For MCQ
    correct_answer: str
    explanation: str
    difficulty: DifficultyLevel
    subject: str
    grade: int
    topic: str
    learning_objective: str
    generated_at: datetime


class ContentGeneratorAgent:
    """
    Content Generator Agent for CBSE curriculum-aligned educational content
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.ContentGeneratorAgent")
        self.curriculum = CBSECurriculum()
        self.openai_client = None
        self.openai_model = None
        self.anthropic_model = None
        self._initialize_models()
        
    def _initialize_models(self):
        """Initialize AI models"""
        try:
            # Initialize OpenAI client if valid API key is available
            if (hasattr(settings, 'openai_api_key') and settings.openai_api_key and 
                settings.openai_api_key != "test-key" and settings.openai_api_key.startswith("sk-")):
                from openai import OpenAI
                self.openai_client = OpenAI(api_key=settings.openai_api_key)
                self.openai_model = settings.openai_model  # Use model from settings
                self.logger.info("OpenAI model initialized")
                
            # Initialize Anthropic client if valid API key is available  
            if (hasattr(settings, 'anthropic_api_key') and settings.anthropic_api_key and 
                settings.anthropic_api_key not in ["test-key", "sk-ant-api03-placeholder-replace-with-real-key"] and
                settings.anthropic_api_key.startswith("sk-ant-")):
                self.anthropic_model = Anthropic(api_key=settings.anthropic_api_key)
                self.logger.info("Anthropic model initialized")
                
            self.logger.info("AI models initialization completed")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize AI models: {e}")
            # Don't raise exception for now, allow testing without API keys
            self.logger.warning("Continuing without AI models for testing purposes")

    async def generate_content(self, request: ContentRequest) -> GeneratedContent:
        """
        Generate educational content based on request parameters
        """
        try:
            self.logger.info(f"Generating {request.content_type} content for {request.subject} Grade {request.grade}")
            
            # Try to get curriculum alignment (flexible approach)
            curriculum_data = await self.curriculum.get_topic_details(
                subject=request.subject,
                grade=request.grade,
                topic=request.topic
            )
            
            # If exact topic not found, create a flexible curriculum context
            if not curriculum_data:
                self.logger.info(f"Topic '{request.topic}' not in exact curriculum, using flexible AI generation")
                curriculum_data = {
                    "code": f"FLEX-{request.grade}-{request.subject[:3].upper()}",
                    "name": request.topic,
                    "chapter": f"Grade {request.grade} {request.subject}",
                    "learning_objectives": [f"Understand {request.topic} concepts", f"Apply {request.topic} skills"],
                    "key_concepts": [request.topic, "Problem solving", "Application"],
                    "prerequisites": [f"Basic {request.subject} knowledge"],
                    "difficulty_level": request.difficulty.value,
                    "estimated_hours": 8 + request.grade * 2,
                    "assessment_type": ["written", "practical"]
                }
            
            # Generate content using AI model
            content = await self._generate_content_with_ai(request, curriculum_data)
            
            # Create response
            generated_content = GeneratedContent(
                content=content["text"],
                content_type=request.content_type,
                subject=request.subject,
                grade=request.grade,
                topic=request.topic,
                difficulty=request.difficulty,
                learning_objectives=content["learning_objectives"],
                estimated_time=content["estimated_time"],
                prerequisites=content["prerequisites"],
                generated_at=datetime.utcnow(),
                metadata={
                    "curriculum_code": curriculum_data.get("code"),
                    "curriculum_chapter": curriculum_data.get("chapter"),
                    "ai_model_used": content.get("model_used", "unknown")
                }
            )
            
            self.logger.info(f"Content generated successfully for {request.topic}")
            return generated_content
            
        except Exception as e:
            self.logger.error(f"Content generation failed: {e}")
            raise AgentException(f"Content generation failed: {e}")

    async def generate_questions(self, request: QuestionRequest) -> List[GeneratedQuestion]:
        """
        Generate questions based on request parameters
        """
        try:
            self.logger.info(f"Generating {request.num_questions} {request.question_type} questions for {request.subject} Grade {request.grade}")
            
            # Try to get curriculum alignment (flexible approach)
            curriculum_data = await self.curriculum.get_topic_details(
                subject=request.subject,
                grade=request.grade,
                topic=request.topic
            )
            
            # If exact topic not found, create a flexible curriculum context
            if not curriculum_data:
                self.logger.info(f"Topic '{request.topic}' not in exact curriculum, using flexible AI generation")
                curriculum_data = {
                    "code": f"FLEX-{request.grade}-{request.subject[:3].upper()}",
                    "name": request.topic,
                    "chapter": f"Grade {request.grade} {request.subject}",
                    "learning_objectives": [f"Understand {request.topic} concepts", f"Apply {request.topic} skills"],
                    "key_concepts": [request.topic, "Problem solving", "Application"],
                    "prerequisites": [f"Basic {request.subject} knowledge"],
                    "difficulty_level": request.difficulty.value,
                    "estimated_hours": 8 + request.grade * 2,
                    "assessment_type": ["written", "practical"]
                }
            
            # Generate questions using AI model
            questions_data = await self._generate_questions_with_ai(request, curriculum_data)
            
            # Create response objects
            generated_questions = []
            for q_data in questions_data:
                question = GeneratedQuestion(
                    question=q_data["question"],
                    question_type=request.question_type,
                    options=q_data.get("options"),
                    correct_answer=q_data["correct_answer"],
                    explanation=q_data["explanation"],
                    difficulty=request.difficulty,
                    subject=request.subject,
                    grade=request.grade,
                    topic=request.topic,
                    learning_objective=q_data["learning_objective"],
                    generated_at=datetime.utcnow()
                )
                generated_questions.append(question)
            
            self.logger.info(f"Generated {len(generated_questions)} questions successfully")
            return generated_questions
            
        except Exception as e:
            self.logger.error(f"Question generation failed: {e}")
            raise AgentException(f"Question generation failed: {e}")

    async def generate_explanation(self, topic: str, subject: str, grade: int, 
                                 concept: str, difficulty: DifficultyLevel = DifficultyLevel.INTERMEDIATE) -> str:
        """
        Generate detailed explanation for a specific concept
        """
        try:
            self.logger.info(f"Generating explanation for concept: {concept}")
            
            # Create explanation prompt
            prompt = self._create_explanation_prompt(topic, subject, grade, concept, difficulty)
            
            # For now, return a mock explanation for testing
            explanation = f"""
# {concept} - Grade {grade} {subject}

## Introduction
{concept} is an important concept in {subject} for Grade {grade} students.

## Key Points
- This concept helps students understand fundamental principles
- It builds on previous knowledge and prepares for advanced topics
- Real-world applications make learning engaging

## Example
[Example content would be generated by AI model]

## Practice
Students can practice this concept through various exercises and activities.

**Note**: This is a test explanation. Full AI-powered content generation will be available when API keys are configured.
"""
            
            self.logger.info("Explanation generated successfully (test mode)")
            return explanation
            
        except Exception as e:
            self.logger.error(f"Explanation generation failed: {e}")
            raise AgentException(f"Explanation generation failed: {e}")

    async def _generate_content_with_ai(self, request: ContentRequest, curriculum_data: Dict) -> Dict[str, Any]:
        """Generate content using AI model"""
        
        # Check if we have available AI models
        if not self.openai_model and not self.anthropic_model:
            self.logger.info(f"Generating {request.content_type} content in test mode (no API keys)")
            return await self._generate_test_content(request, curriculum_data)
        
        # Try to generate with real AI model
        try:
            self.logger.info(f"Checking AI models: anthropic={self.anthropic_model is not None}, openai={self.openai_model is not None}")
            self.logger.info(f"Anthropic key available: {hasattr(settings, 'anthropic_api_key') and bool(settings.anthropic_api_key)}")
            
            if (self.anthropic_model and hasattr(settings, 'anthropic_api_key') and 
                settings.anthropic_api_key and 
                settings.anthropic_api_key not in ["test-key", "sk-ant-api03-placeholder-replace-with-real-key"] and
                settings.anthropic_api_key.startswith("sk-ant-")):
                self.logger.info("Using Anthropic API for content generation")
                return await self._generate_with_anthropic(request, curriculum_data)
            elif (self.openai_client and hasattr(settings, 'openai_api_key') and 
                  settings.openai_api_key and 
                  settings.openai_api_key != "test-key" and
                  settings.openai_api_key.startswith("sk-")):
                self.logger.info("Using OpenAI API for content generation")
                return await self._generate_with_openai(request, curriculum_data)
            else:
                self.logger.info(f"API keys not configured properly, using test mode")
                return await self._generate_test_content(request, curriculum_data)
                
        except Exception as e:
            self.logger.error(f"AI generation failed, falling back to test mode: {e}")
            return await self._generate_test_content(request, curriculum_data)

    async def _generate_test_content(self, request: ContentRequest, curriculum_data: Dict) -> Dict[str, Any]:
        """Generate test content when AI models are not available"""
        self.logger.info(f"Generating {request.content_type} content in test mode")
        
        # Create test content based on request
        test_content = f"""
# {request.topic} - Grade {request.grade} {request.subject}

## Learning Content ({request.content_type.value.title()})

This is test content for **{request.topic}** in Grade {request.grade} {request.subject}.

### Key Concepts:
- Concept 1: Understanding the basics
- Concept 2: Applying knowledge 
- Concept 3: Problem-solving approaches

### Examples:
Example problems and solutions would be generated here based on CBSE curriculum requirements.

### Practice Activities:
Interactive exercises and activities to reinforce learning.

**Difficulty Level**: {request.difficulty.value}
**Curriculum Alignment**: CBSE Grade {request.grade} {request.subject}

*Note: This is test content. Full AI-powered generation will be available with proper API configuration.*
"""
        
        return {
            "text": test_content,
            "learning_objectives": request.learning_objectives or [
                f"Understand {request.topic} concepts",
                f"Apply {request.topic} principles", 
                f"Solve problems related to {request.topic}"
            ],
            "estimated_time": 15 + (request.grade * 2),  # Rough estimate
            "prerequisites": curriculum_data.get("prerequisites", [f"Basic {request.subject} knowledge"]),
            "model_used": "TestMode"
        }

    async def _generate_questions_with_ai(self, request: QuestionRequest, curriculum_data: Dict) -> List[Dict]:
        """Generate questions using AI model"""
        
        # Check if we have available AI models
        if not self.openai_model and not self.anthropic_model:
            self.logger.info(f"Generating {request.num_questions} questions in test mode (no API keys)")
            return await self._generate_test_questions(request, curriculum_data)
        
        # Try to generate with real AI model
        try:
            self.logger.info(f"Checking AI models for question generation: anthropic={self.anthropic_model is not None}, openai={self.openai_model is not None}")
            
            if (self.anthropic_model and hasattr(settings, 'anthropic_api_key') and 
                settings.anthropic_api_key and 
                settings.anthropic_api_key not in ["test-key", "sk-ant-api03-placeholder-replace-with-real-key"] and
                settings.anthropic_api_key.startswith("sk-ant-")):
                self.logger.info("Using Anthropic API for question generation")
                return await self._generate_questions_with_anthropic(request, curriculum_data)
            elif (self.openai_client and hasattr(settings, 'openai_api_key') and 
                  settings.openai_api_key and 
                  settings.openai_api_key != "test-key" and
                  settings.openai_api_key.startswith("sk-")):
                self.logger.info("Using OpenAI API for question generation")
                return await self._generate_questions_with_openai(request, curriculum_data)
            else:
                self.logger.info(f"API keys not configured properly, using test mode")
                return await self._generate_test_questions(request, curriculum_data)
                
        except Exception as e:
            self.logger.error(f"AI question generation failed, falling back to test mode: {e}")
            return await self._generate_test_questions(request, curriculum_data)

    async def _generate_test_questions(self, request: QuestionRequest, curriculum_data: Dict) -> List[GeneratedQuestion]:
        """Generate test questions when AI models are not available"""
        
        self.logger.info(f"Generating {request.num_questions} questions in test mode")
        
        # Generate test questions based on request
        questions = []
        
        for i in range(request.num_questions):
            # Add options for MCQ
            options = None
            if request.question_type == QuestionType.MCQ:
                options = [
                    f"Test Answer {i+1}",  # Correct answer
                    f"Incorrect Option A for Q{i+1}", 
                    f"Incorrect Option B for Q{i+1}",
                    f"Incorrect Option C for Q{i+1}"
                ]
            
            question = GeneratedQuestion(
                question=f"Test Question {i+1} for {request.topic} (Grade {request.grade} {request.subject})",
                question_type=request.question_type,
                options=options,
                correct_answer=f"Test Answer {i+1}",
                explanation=f"This is a test explanation for Question {i+1} about {request.topic}. The answer demonstrates understanding of key concepts in {request.subject}.",
                difficulty=request.difficulty,
                subject=request.subject,
                grade=request.grade,
                topic=request.topic,
                learning_objective=f"Understand and apply {request.topic} concepts",
                estimated_time=5,
                generated_at=datetime.utcnow(),
                metadata={"test_mode": True, "question_index": i+1}
            )
            
            questions.append(question)
        
        return questions

    async def _generate_questions_with_openai(self, request: QuestionRequest, curriculum_data: Dict) -> List[GeneratedQuestion]:
        """Generate questions using OpenAI API"""
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=settings.openai_api_key)
            
            prompt = self._create_question_prompt(request, curriculum_data)
            system_prompt = self._get_question_system_prompt(request.question_type)
            
            response = await client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            response_text = response.choices[0].message.content
            questions = self._parse_questions_response(response_text, request)
            
            self.logger.info(f"OpenAI question generation successful for {request.topic}")
            return questions
            
        except Exception as e:
            self.logger.error(f"OpenAI question generation failed: {e}")
            raise

    async def _generate_questions_with_anthropic(self, request: QuestionRequest, curriculum_data: Dict) -> List[GeneratedQuestion]:
        """Generate questions using Anthropic API"""
        try:
            client = Anthropic(api_key=settings.anthropic_api_key)
            
            prompt = self._create_question_prompt(request, curriculum_data)
            system_prompt = self._get_question_system_prompt(request.question_type)
            
            response = client.messages.create(
                model=settings.anthropic_model,
                max_tokens=2000,
                temperature=0.7,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            response_text = response.content[0].text
            questions = self._parse_questions_response(response_text, request)
            
            self.logger.info(f"Anthropic question generation successful for {request.topic}")
            return questions
            
        except Exception as e:
            self.logger.error(f"Anthropic question generation failed: {e}")
            raise

    async def _generate_with_openai(self, request: ContentRequest, curriculum_data: Dict) -> Dict[str, Any]:
        """Generate content using OpenAI API"""
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=settings.openai_api_key)
            
            prompt = self._create_content_prompt(request, curriculum_data)
            system_prompt = self._get_content_system_prompt(request.content_type)
            
            response = await client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            content_text = response.choices[0].message.content
            parsed_response = self._parse_content_response(content_text, request)
            parsed_response["model_used"] = "OpenAI " + settings.openai_model
            
            self.logger.info(f"OpenAI content generation successful for {request.topic}")
            return parsed_response
            
        except Exception as e:
            self.logger.error(f"OpenAI generation failed: {e}")
            raise

    async def _generate_with_anthropic(self, request: ContentRequest, curriculum_data: Dict) -> Dict[str, Any]:
        """Generate content using Anthropic API"""
        try:
            # Use synchronous client for now as async requires different setup
            client = Anthropic(api_key=settings.anthropic_api_key)
            
            prompt = self._create_content_prompt(request, curriculum_data)
            system_prompt = self._get_content_system_prompt(request.content_type)
            
            # Use synchronous call
            response = client.messages.create(
                model=settings.anthropic_model,
                max_tokens=1500,
                temperature=0.7,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            content_text = response.content[0].text
            parsed_response = self._parse_content_response(content_text, request)
            parsed_response["model_used"] = "Anthropic " + settings.anthropic_model
            
            self.logger.info(f"Anthropic content generation successful for {request.topic}")
            return parsed_response
            
        except Exception as e:
            self.logger.error(f"Anthropic generation failed: {e}")
            raise

    def _create_content_prompt(self, request: ContentRequest, curriculum_data: Dict) -> str:
        """Create prompt for content generation - Simplified version"""
        
        template = f"""
Generate {request.content_type.value} content for CBSE curriculum:

Subject: {request.subject}
Grade: {request.grade} 
Topic: {request.topic}
Difficulty Level: {request.difficulty.value}

Curriculum Information:
{str(curriculum_data)}

Learning Objectives:
{str(request.learning_objectives or "Standard CBSE objectives")}

Requirements:
1. Align with CBSE curriculum standards
2. Age-appropriate language and examples
3. Include real-world applications where relevant
4. Structure content logically with clear sections
5. Provide estimated time for completion
6. List prerequisites

Please provide the content in this JSON format:
{{
  "text": "Main content here...",
  "learning_objectives": ["objective 1", "objective 2"],
  "estimated_time": 15,
  "prerequisites": ["prerequisite 1", "prerequisite 2"]
}}
"""
        
        return template

    def _create_question_prompt(self, request: QuestionRequest, curriculum_data: Dict) -> str:
        """Create prompt for question generation - Simplified version"""
        
        template = f"""
Generate {request.num_questions} {request.question_type.value} question(s) for CBSE curriculum:

Subject: {request.subject}
Grade: {request.grade}
Topic: {request.topic}
Difficulty Level: {request.difficulty.value}
Context: {request.context or "No specific context provided"}

Curriculum Information:
{str(curriculum_data)}

Requirements:
1. Questions must align with CBSE curriculum standards
2. Age-appropriate language and difficulty
3. Include detailed explanations for answers
4. For MCQs, provide 4 options with clear distractors
5. Map each question to a specific learning objective

Please provide response in this JSON format:
[
  {{
    "question": "Question text here...",
    "options": ["A", "B", "C", "D"], // Only for MCQ
    "correct_answer": "Correct answer here",
    "explanation": "Detailed explanation here...",
    "learning_objective": "Specific objective being tested"
  }}
]
"""
        
        return template

    def _create_explanation_prompt(self, topic: str, subject: str, grade: int, 
                                  concept: str, difficulty: DifficultyLevel) -> str:
        """Create prompt for concept explanation"""
        
        return f"""
Explain the concept "{concept}" from the topic "{topic}" in {subject} for Grade {grade} students.

Difficulty Level: {difficulty.value}

Please provide a clear, engaging explanation that:
1. Uses age-appropriate language for Grade {grade} students
2. Includes relevant examples and analogies
3. Connects to real-world applications
4. Breaks down complex ideas into simpler parts
5. Follows CBSE curriculum guidelines

Structure the explanation with:
- Introduction to the concept
- Step-by-step breakdown
- Examples with solutions
- Key takeaways
- Common misconceptions to avoid
"""

    def _get_content_system_prompt(self, content_type: ContentType) -> str:
        """Get system prompt for content generation"""
        
        base_prompts = {
            ContentType.EXPLANATION: "You are an expert CBSE curriculum tutor who creates clear, comprehensive explanations that help students understand complex concepts through examples and step-by-step breakdowns.",
            ContentType.EXAMPLE: "You are a skilled educator who creates relevant, practical examples that demonstrate theoretical concepts in real-world contexts, making learning engaging for CBSE students.",
            ContentType.EXERCISE: "You are an experienced teacher who designs practice exercises that reinforce learning objectives and help students apply concepts they've learned.",
            ContentType.ASSESSMENT: "You are a curriculum specialist who creates fair, comprehensive assessments that accurately measure student understanding according to CBSE standards."
        }
        
        base_prompt = base_prompts.get(content_type, "You are an expert CBSE curriculum tutor.")
        
        # Add JSON formatting instruction
        json_instruction = """

CRITICAL: You must respond ONLY with valid JSON in this exact format (no additional text):
{
  "text": "Your educational content here...",
  "learning_objectives": ["objective 1", "objective 2", "objective 3"],
  "estimated_time": 15,
  "prerequisites": ["prerequisite 1", "prerequisite 2"]
}"""
        
        return base_prompt + json_instruction

    def _get_question_system_prompt(self, question_type: QuestionType) -> str:
        """Get system prompt for question generation"""
        
        prompts = {
            QuestionType.MCQ: "You are an expert at creating multiple-choice questions with clear, plausible distractors that test conceptual understanding rather than mere recall.",
            QuestionType.SHORT_ANSWER: "You are skilled at designing short-answer questions that require students to demonstrate understanding through concise, focused responses.",
            QuestionType.LONG_ANSWER: "You are an expert at creating comprehensive questions that allow students to demonstrate deep understanding and analytical thinking.",
            QuestionType.FILL_BLANK: "You are experienced in designing fill-in-the-blank questions that test specific knowledge while maintaining sentence flow and context.",
            QuestionType.TRUE_FALSE: "You are skilled at creating true/false questions that test genuine understanding rather than trivial facts."
        }
        
        return prompts.get(question_type, "You are an expert question writer for educational assessments.")

    def _parse_content_response(self, response: str, request: ContentRequest) -> Dict[str, Any]:
        """Parse AI response for content generation with improved error handling"""
        try:
            import json
            import re
            
            # Clean the response by removing control characters and fixing common issues
            cleaned_response = response.strip()
            
            # Remove control characters that break JSON parsing
            cleaned_response = re.sub(r'[\x00-\x1F\x7F]', ' ', cleaned_response)
            
            # Try to parse as JSON first
            if cleaned_response.startswith('{'):
                parsed = json.loads(cleaned_response)
                
                # Validate and ensure all required fields exist
                if isinstance(parsed, dict):
                    # Ensure required fields
                    if 'text' not in parsed:
                        parsed['text'] = cleaned_response
                    if 'learning_objectives' not in parsed:
                        parsed['learning_objectives'] = request.learning_objectives or [f"Understand {request.topic} concepts"]
                    if 'estimated_time' not in parsed:
                        parsed['estimated_time'] = 15
                    if 'prerequisites' not in parsed:
                        parsed['prerequisites'] = [f"Basic {request.subject} knowledge"]
                    
                    return parsed
            
            # If not JSON or parsing failed, create structure from text
            return {
                "text": cleaned_response,
                "learning_objectives": request.learning_objectives or [f"Understand {request.topic} concepts"],
                "estimated_time": 15,
                "prerequisites": [f"Basic {request.subject} knowledge"]
            }
            
        except Exception as e:
            self.logger.warning(f"Failed to parse structured response, using fallback: {e}")
            # Last resort fallback
            return {
                "text": response,  # Use original response as fallback
                "learning_objectives": [f"Understand {request.topic} concepts"],
                "estimated_time": 15,
                "prerequisites": [f"Basic {request.subject} knowledge"]
            }

    def _parse_questions_response(self, response: str, request: QuestionRequest) -> List[Dict]:
        """Parse AI response for question generation"""
        try:
            import json
            # Try to parse as JSON array
            if response.strip().startswith('['):
                return json.loads(response)
            
            # Fallback: create single question structure
            return [{
                "question": response,
                "options": None,
                "correct_answer": "Answer not provided",
                "explanation": "Explanation not provided",
                "learning_objective": f"Understand {request.topic} concepts"
            }]
            
        except Exception as e:
            self.logger.warning(f"Failed to parse questions response, using fallback: {e}")
            return [{
                "question": response,
                "options": None,
                "correct_answer": "Answer not provided", 
                "explanation": "Explanation not provided",
                "learning_objective": f"Understand {request.topic} concepts"
            }]

    async def get_agent_status(self) -> Dict[str, Any]:
        """Get agent status and health"""
        return {
            "name": "ContentGeneratorAgent",
            "status": "active",
            "models_available": {
                "openai": self.openai_model is not None,
                "anthropic": self.anthropic_model is not None
            },
            "supported_content_types": [ct.value for ct in ContentType],
            "supported_question_types": [qt.value for qt in QuestionType],
            "curriculum_loaded": self.curriculum is not None
        }