"""
Content Generation API Endpoints
Provides REST API for content generation services
"""

import logging
from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse

from agents.content_generator import (
    ContentRequest, QuestionRequest, GeneratedContent, 
    GeneratedQuestion, DifficultyLevel, ContentType, QuestionType
)
from agents.coordinator import AgentCoordinator
from core.dependencies import get_agent_coordinator
from core.exceptions import AgentException


router = APIRouter(prefix="/content", tags=["Content Generation"])
logger = logging.getLogger(__name__)


@router.post("/generate", response_model=GeneratedContent)
async def generate_content(
    request: ContentRequest,
    coordinator: AgentCoordinator = Depends(get_agent_coordinator)
):
    """
    Generate educational content based on CBSE curriculum
    """
    try:
        logger.info(f"Content generation request: {request.subject} Grade {request.grade} - {request.topic}")
        
        content_generator = coordinator.get_agent('content_generator')
        if not content_generator:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Content Generator agent not available"
            )
        
        generated_content = await content_generator.generate_content(request)
        
        logger.info(f"Content generated successfully for {request.topic}")
        return generated_content
        
    except AgentException as e:
        logger.error(f"Agent error in content generation: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error in content generation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during content generation"
        )


@router.post("/generate/questions", response_model=List[GeneratedQuestion])
async def generate_questions(
    request: QuestionRequest,
    coordinator: AgentCoordinator = Depends(get_agent_coordinator)
):
    """
    Generate questions based on CBSE curriculum topics
    """
    try:
        logger.info(f"Question generation request: {request.num_questions} {request.question_type} questions for {request.subject} Grade {request.grade}")
        
        content_generator = coordinator.get_agent('content_generator')
        if not content_generator:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Content Generator agent not available"
            )
        
        generated_questions = await content_generator.generate_questions(request)
        
        logger.info(f"Generated {len(generated_questions)} questions successfully")
        return generated_questions
        
    except AgentException as e:
        logger.error(f"Agent error in question generation: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error in question generation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during question generation"
        )


@router.post("/generate/explanation")
async def generate_explanation(
    topic: str,
    subject: str,
    grade: int,
    concept: str,
    difficulty: DifficultyLevel = DifficultyLevel.INTERMEDIATE,
    coordinator: AgentCoordinator = Depends(get_agent_coordinator)
):
    """
    Generate detailed explanation for a specific concept
    """
    try:
        logger.info(f"Explanation generation request: {concept} in {topic}")
        
        content_generator = coordinator.get_agent('content_generator')
        if not content_generator:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Content Generator agent not available"
            )
        
        explanation = await content_generator.generate_explanation(
            topic=topic,
            subject=subject,
            grade=grade,
            concept=concept,
            difficulty=difficulty
        )
        
        logger.info("Explanation generated successfully")
        return {
            "topic": topic,
            "subject": subject,
            "grade": grade,
            "concept": concept,
            "difficulty": difficulty.value,
            "explanation": explanation,
            "generated_at": "2025-01-21T00:00:00Z"  # This would be actual timestamp
        }
        
    except AgentException as e:
        logger.error(f"Agent error in explanation generation: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error in explanation generation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during explanation generation"
        )


@router.get("/types")
async def get_content_types():
    """
    Get available content types and question types
    """
    return {
        "content_types": [ct.value for ct in ContentType],
        "question_types": [qt.value for qt in QuestionType],
        "difficulty_levels": [dl.value for dl in DifficultyLevel]
    }


@router.get("/curriculum/topics/{subject}/{grade}")
async def get_curriculum_topics(
    subject: str,
    grade: int,
    coordinator: AgentCoordinator = Depends(get_agent_coordinator)
):
    """
    Get available curriculum topics for a subject and grade
    """
    try:
        content_generator = coordinator.get_agent('content_generator')
        if not content_generator:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Content Generator agent not available"
            )
        
        # Get curriculum topics through the agent's curriculum instance
        curriculum = content_generator.curriculum
        subject_curriculum = await curriculum.get_subject_curriculum(subject, grade)
        
        if not subject_curriculum:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Curriculum not found for {subject} Grade {grade}"
            )
        
        topics = []
        for chapter in subject_curriculum.chapters:
            for topic in chapter.topics:
                topics.append({
                    "code": topic.code,
                    "name": topic.name,
                    "chapter": chapter.chapter_name,
                    "chapter_number": chapter.chapter_number,
                    "difficulty": topic.difficulty_level,
                    "estimated_hours": topic.estimated_hours,
                    "key_concepts": topic.key_concepts
                })
        
        return {
            "subject": subject,
            "grade": grade,
            "total_topics": len(topics),
            "topics": topics
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving curriculum topics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving curriculum topics"
        )


@router.get("/curriculum/search")
async def search_curriculum(
    query: str,
    subject: str = None,
    grade: int = None,
    coordinator: AgentCoordinator = Depends(get_agent_coordinator)
):
    """
    Search for topics across curriculum
    """
    try:
        content_generator = coordinator.get_agent('content_generator')
        if not content_generator:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Content Generator agent not available"
            )
        
        curriculum = content_generator.curriculum
        results = await curriculum.search_topics(query, subject, grade)
        
        return {
            "query": query,
            "filters": {
                "subject": subject,
                "grade": grade
            },
            "total_results": len(results),
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Error searching curriculum: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while searching curriculum"
        )