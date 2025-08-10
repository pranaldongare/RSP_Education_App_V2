"""Pytest-based tests for the Content Generator agent."""

import os
import sys

import pytest

# Ensure local imports work when running tests directly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.content_generator import (
    ContentGeneratorAgent,
    ContentRequest,
    ContentType,
    DifficultyLevel,
    QuestionRequest,
    QuestionType,
)


@pytest.mark.asyncio
async def test_curriculum_access() -> None:
    """Verify curriculum search and topic details access."""

    agent = ContentGeneratorAgent()
    curriculum = agent.curriculum

    math_topics = await curriculum.search_topics("place value", "Mathematics", 3)
    assert math_topics, "Expected at least one topic for 'place value'"

    first_topic = math_topics[0]
    assert first_topic["subject"] == "Mathematics"
    assert first_topic["grade"] == 3

    topic_details = await curriculum.get_topic_details(
        "Mathematics", 3, "Place Value in 3-digit Numbers"
    )
    assert topic_details is not None, "Topic details should not be None"
    assert topic_details["code"] == "M3-1-1"
    assert topic_details["chapter"] == "Numbers up to 999"
    assert topic_details["learning_objectives"]
    assert topic_details["prerequisites"]


@pytest.mark.asyncio
async def test_agent_status() -> None:
    """Ensure the agent reports expected status information."""

    agent = ContentGeneratorAgent()
    status = await agent.get_agent_status()

    assert status["name"] == "ContentGeneratorAgent"
    assert status["status"] == "active"
    assert isinstance(status["models_available"], dict)
    assert "openai" in status["models_available"]
    assert "anthropic" in status["models_available"]
    assert status["curriculum_loaded"] is True
    assert set(status["supported_content_types"]) == {
        ct.value for ct in ContentType
    }
    assert set(status["supported_question_types"]) == {
        qt.value for qt in QuestionType
    }


@pytest.mark.asyncio
async def test_content_request_creation() -> None:
    """Validate creation of content and question requests."""

    content_request = ContentRequest(
        subject="Mathematics",
        grade=3,
        topic="Place Value in 3-digit Numbers",
        content_type=ContentType.EXPLANATION,
        difficulty=DifficultyLevel.INTERMEDIATE,
    )

    assert content_request.subject == "Mathematics"
    assert content_request.grade == 3
    assert content_request.content_type == ContentType.EXPLANATION
    assert content_request.difficulty == DifficultyLevel.INTERMEDIATE

    question_request = QuestionRequest(
        subject="Mathematics",
        grade=3,
        topic="Place Value in 3-digit Numbers",
        question_type=QuestionType.MCQ,
        difficulty=DifficultyLevel.INTERMEDIATE,
        num_questions=2,
    )

    assert question_request.subject == "Mathematics"
    assert question_request.grade == 3
    assert question_request.question_type == QuestionType.MCQ
    assert question_request.num_questions == 2

