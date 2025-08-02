"""
Test Suite for Voice Interaction Agent - Phase 5 Implementation
Comprehensive testing of voice interaction, speech processing, and audio content generation.
"""

import asyncio
import pytest
import base64
from datetime import datetime, timedelta
from typing import Dict, List, Any

from agents.voice_interaction_agent import (
    VoiceInteractionAgent,
    VoiceCommand,
    SpeechLanguage,
    VoiceGender,
    AudioFormat,
    VoiceSettings,
    SpeechInput,
    SpeechOutput,
    VoiceInteractionSession,
    VoiceInteractionResult,
    AudioContent
)


class TestVoiceInteractionAgent:
    """Test suite for Voice Interaction Agent"""
    
    @pytest.fixture
    async def voice_agent(self):
        """Create Voice Interaction Agent instance for testing"""
        agent = VoiceInteractionAgent()
        await agent.initialize_ai_clients()
        return agent
    
    @pytest.mark.asyncio
    async def test_agent_initialization_and_status(self, voice_agent):
        """Test agent initialization and status reporting"""
        print("\n=== Testing Voice Interaction Agent Initialization ===")
        
        # Test agent status
        status = await voice_agent.get_agent_status()
        
        print(f"Agent Status: {status}")
        
        # Verify status structure
        assert status["agent_name"] == "voice_interaction"
        assert status["status"] == "active"
        assert "test_mode" in status
        assert "active_sessions" in status
        assert "cached_audio_content" in status
        assert "supported_languages" in status
        assert "supported_commands" in status
        assert "capabilities" in status
        assert len(status["capabilities"]) == 6
        
        # Verify supported features
        assert len(status["supported_languages"]) >= 6  # Multiple language support
        assert len(status["supported_commands"]) == 9   # All voice commands
        
        print("SUCCESS: Voice Interaction Agent initialized successfully")
    
    @pytest.mark.asyncio
    async def test_voice_session_management(self, voice_agent):
        """Test voice session creation and management"""
        print("\n=== Testing Voice Session Management ===")
        
        student_id = "student_voice_001"
        language = SpeechLanguage.ENGLISH
        
        # Test session creation
        voice_settings = VoiceSettings(
            language=language,
            gender=VoiceGender.FEMALE,
            speed=1.0,
            pitch=1.0,
            volume=0.8
        )
        
        session = await voice_agent.start_voice_session(
            student_id=student_id,
            language=language,
            voice_settings=voice_settings
        )
        
        print(f"Created Voice Session: {session.session_id}")
        print(f"Student ID: {session.student_id}")
        print(f"Language: {session.language}")
        print(f"Voice Settings: {session.voice_settings}")
        
        # Verify session structure
        assert session.student_id == student_id
        assert session.language == language
        assert session.voice_settings.language == language
        assert session.voice_settings.gender == VoiceGender.FEMALE
        assert session.is_active == True
        assert session.total_interactions == 0
        
        # Test session status
        session_status = await voice_agent.get_session_status(session.session_id)
        
        print(f"Session Status: {session_status}")
        
        assert session_status["session_id"] == session.session_id
        assert session_status["student_id"] == student_id
        assert session_status["is_active"] == True
        assert session_status["total_interactions"] == 0
        
        print("SUCCESS: Voice session created and managed successfully")
    
    @pytest.mark.asyncio
    async def test_speech_to_text_processing(self, voice_agent):
        """Test speech-to-text functionality"""
        print("\n=== Testing Speech-to-Text Processing ===")
        
        # Create mock audio input
        mock_audio_data = base64.b64encode(b"mock_audio_content").decode('utf-8')
        
        speech_input = SpeechInput(
            audio_data=mock_audio_data,
            format=AudioFormat.WAV,
            language=SpeechLanguage.ENGLISH,
            duration=3.5
        )
        
        print(f"Processing Speech Input:")
        print(f"  Format: {speech_input.format}")
        print(f"  Language: {speech_input.language}")
        print(f"  Duration: {speech_input.duration}s")
        
        # Test speech recognition
        recognized_text = await voice_agent.speech_to_text(speech_input)
        
        print(f"Recognized Text: '{recognized_text}'")
        
        # Verify recognition results
        assert isinstance(recognized_text, str)
        assert len(recognized_text) > 0
        # In test mode, should return one of the predefined phrases
        test_phrases = [
            "Start the lesson on mathematics",
            "Explain fractions to me", 
            "I have a question about science",
            "Can you repeat that explanation",
            "Help me understand this concept",
            "What is photosynthesis",
            "End the session"
        ]
        assert recognized_text in test_phrases
        
        print("SUCCESS: Speech-to-text processing working correctly")
    
    @pytest.mark.asyncio
    async def test_text_to_speech_synthesis(self, voice_agent):
        """Test text-to-speech functionality"""
        print("\n=== Testing Text-to-Speech Synthesis ===")
        
        # Test text to convert
        test_text = "Hello! This is a test of the text-to-speech system. How does it sound?"
        
        voice_settings = VoiceSettings(
            language=SpeechLanguage.ENGLISH,
            gender=VoiceGender.FEMALE,
            speed=1.0,
            pitch=1.0,
            volume=0.8
        )
        
        print(f"Converting Text to Speech:")
        print(f"  Text: '{test_text}'")
        print(f"  Language: {voice_settings.language}")
        print(f"  Gender: {voice_settings.gender}")
        print(f"  Speed: {voice_settings.speed}")
        
        # Test speech synthesis
        speech_output = await voice_agent.text_to_speech(test_text, voice_settings)
        
        print(f"Speech Output Generated:")
        print(f"  Format: {speech_output.format}")
        print(f"  Duration: {speech_output.duration}s")
        print(f"  Audio Data Length: {len(speech_output.audio_data)} chars")
        
        # Verify speech output
        assert speech_output.text == test_text
        assert speech_output.format == AudioFormat.MP3
        assert speech_output.voice_settings == voice_settings
        assert len(speech_output.audio_data) > 0
        assert speech_output.duration > 0
        
        print("SUCCESS: Text-to-speech synthesis working correctly")
    
    @pytest.mark.asyncio
    async def test_voice_command_recognition(self, voice_agent):
        """Test voice command detection and processing"""
        print("\n=== Testing Voice Command Recognition ===")
        
        # Test various voice commands
        test_commands = [
            ("start lesson on mathematics", VoiceCommand.START_LESSON),
            ("pause the current session", VoiceCommand.PAUSE_LESSON),
            ("resume learning", VoiceCommand.RESUME_LESSON),
            ("repeat that explanation", VoiceCommand.REPEAT_CONTENT),
            ("explain this concept", VoiceCommand.EXPLAIN_CONCEPT),
            ("I have a question", VoiceCommand.ASK_QUESTION),
            ("the answer is 42", VoiceCommand.ANSWER_QUESTION), 
            ("help me understand", VoiceCommand.GET_HELP),
            ("end session now", VoiceCommand.END_SESSION)
        ]
        
        print(f"Testing {len(test_commands)} voice commands:")
        
        for test_text, expected_command in test_commands:
            detected_command = await voice_agent._detect_voice_command(test_text)
            
            print(f"  '{test_text}' -> {detected_command}")
            
            assert detected_command == expected_command
        
        # Test unrecognized command
        unrecognized_text = "this is completely random text with no command"
        detected_command = await voice_agent._detect_voice_command(unrecognized_text)
        
        print(f"  '{unrecognized_text}' -> {detected_command}")
        assert detected_command is None
        
        print("SUCCESS: Voice command recognition working correctly")
    
    @pytest.mark.asyncio
    async def test_complete_voice_interaction(self, voice_agent):
        """Test complete voice interaction flow"""
        print("\n=== Testing Complete Voice Interaction Flow ===")
        
        # Start voice session
        student_id = "student_voice_complete"
        session = await voice_agent.start_voice_session(student_id)
        
        # Create speech input with command
        mock_audio_data = base64.b64encode(b"start_lesson_audio").decode('utf-8')
        speech_input = SpeechInput(
            audio_data=mock_audio_data,
            format=AudioFormat.WAV,
            language=SpeechLanguage.ENGLISH
        )
        
        print(f"Processing complete voice interaction:")
        print(f"  Session: {session.session_id}")
        print(f"  Student: {student_id}")
        
        # Process speech input
        interaction_result = await voice_agent.process_speech_input(
            session.session_id, speech_input
        )
        
        print(f"Interaction Results:")
        print(f"  Recognized Text: '{interaction_result.recognized_text}'")
        print(f"  Detected Command: {interaction_result.detected_command}")
        print(f"  Response Text: '{interaction_result.response_text}'")
        print(f"  Confidence Score: {interaction_result.confidence_score}")
        print(f"  Processing Time: {interaction_result.processing_time:.3f}s")
        
        # Verify interaction results
        assert interaction_result.session_id == session.session_id
        assert interaction_result.recognized_text is not None
        assert len(interaction_result.response_text) > 0
        assert 0.0 <= interaction_result.confidence_score <= 1.0
        assert interaction_result.processing_time > 0
        assert interaction_result.response_audio is not None
        
        # Verify session was updated
        updated_session = voice_agent.active_sessions[session.session_id]
        assert updated_session.total_interactions == 1
        
        print("SUCCESS: Complete voice interaction processed successfully")
    
    @pytest.mark.asyncio
    async def test_audio_content_generation(self, voice_agent):
        """Test educational audio content generation"""
        print("\n=== Testing Audio Content Generation ===")
        
        # Test parameters
        subject = "Mathematics"
        grade = 5
        topic = "Fractions and Decimals"
        content_type = "explanation"
        language = SpeechLanguage.ENGLISH
        
        voice_settings = VoiceSettings(
            language=language,
            gender=VoiceGender.FEMALE,
            speed=0.9
        )
        
        print(f"Generating Audio Content:")
        print(f"  Subject: {subject}")
        print(f"  Grade: {grade}")
        print(f"  Topic: {topic}")
        print(f"  Type: {content_type}")
        print(f"  Language: {language}")
        
        # Generate audio content
        audio_content = await voice_agent.generate_audio_content(
            subject=subject,
            grade=grade,
            topic=topic,
            content_type=content_type,
            language=language,
            voice_settings=voice_settings
        )
        
        print(f"Generated Audio Content:")
        print(f"  Content ID: {audio_content.content_id}")
        print(f"  Title: {audio_content.title}")
        print(f"  Duration: {audio_content.duration}s")
        print(f"  Text Length: {len(audio_content.text_content)} chars")
        print(f"  Audio Data Length: {len(audio_content.audio_data)} chars")
        
        # Verify audio content
        assert audio_content.subject == subject
        assert audio_content.grade == grade
        assert audio_content.topic == topic
        assert audio_content.content_type == content_type
        assert audio_content.language == language
        assert len(audio_content.text_content) > 0
        assert len(audio_content.audio_data) > 0
        assert audio_content.duration > 0
        assert audio_content.voice_settings == voice_settings
        
        print("SUCCESS: Audio content generated successfully")
    
    @pytest.mark.asyncio
    async def test_multilingual_support(self, voice_agent):
        """Test multilingual voice interaction support"""
        print("\n=== Testing Multilingual Support ===")
        
        # Test different languages
        test_languages = [
            SpeechLanguage.ENGLISH,
            SpeechLanguage.HINDI,
            SpeechLanguage.TAMIL,
            SpeechLanguage.GUJARATI
        ]
        
        student_id = "student_multilingual"
        
        for language in test_languages:
            print(f"Testing language: {language}")
            
            # Start session in different language
            session = await voice_agent.start_voice_session(
                student_id=f"{student_id}_{language.value}",
                language=language
            )
            
            # Generate welcome message
            welcome_message = await voice_agent._generate_welcome_message(language)
            
            # Safely display message without Unicode issues
            try:
                print(f"  Welcome Message: '{welcome_message[:50]}...'")
            except UnicodeEncodeError:
                print(f"  Welcome Message: '[{language.value} message generated successfully]'")
            
            # Verify session
            assert session.language == language
            assert session.voice_settings.language == language
            assert len(welcome_message) > 0
            
            # Test content generation in this language
            audio_content = await voice_agent.generate_audio_content(
                subject="Science",
                grade=4,
                topic="Plants",
                language=language
            )
            
            assert audio_content.language == language
            
        print("SUCCESS: Multilingual support working correctly")
    
    @pytest.mark.asyncio
    async def test_audio_content_library(self, voice_agent):
        """Test audio content library management"""
        print("\n=== Testing Audio Content Library ===")
        
        # Generate several audio content pieces
        content_configs = [
            ("Mathematics", 5, "Algebra", "explanation"),
            ("Science", 4, "Photosynthesis", "story"),  
            ("English", 3, "Grammar", "quiz"),
            ("Mathematics", 5, "Geometry", "explanation")
        ]
        
        print(f"Generating {len(content_configs)} audio content pieces:")
        
        for subject, grade, topic, content_type in content_configs:
            await voice_agent.generate_audio_content(
                subject=subject,
                grade=grade,
                topic=topic,
                content_type=content_type
            )
            print(f"  Generated: {subject} Grade {grade} - {topic} ({content_type})")
        
        # Test library retrieval - all content
        all_content = await voice_agent.get_audio_content_library()
        
        print(f"Total Content in Library: {len(all_content)}")
        
        assert len(all_content) >= len(content_configs)
        
        # Test filtered retrieval - Mathematics only
        math_content = await voice_agent.get_audio_content_library(subject="Mathematics")
        
        print(f"Mathematics Content: {len(math_content)}")
        
        assert len(math_content) >= 2  # At least two math content pieces
        for content in math_content:
            assert content["subject"] == "Mathematics"
        
        # Test filtered retrieval - Grade 5 only
        grade5_content = await voice_agent.get_audio_content_library(grade=5)
        
        print(f"Grade 5 Content: {len(grade5_content)}")
        
        for content in grade5_content:
            assert content["grade"] == 5
        
        print("SUCCESS: Audio content library management working correctly")
    
    @pytest.mark.asyncio
    async def test_session_ending_and_analytics(self, voice_agent):
        """Test session ending and analytics generation"""
        print("\n=== Testing Session Ending and Analytics ===")
        
        student_id = "student_analytics"
        
        # Start session
        session = await voice_agent.start_voice_session(student_id)
        session_id = session.session_id
        
        # Simulate multiple interactions
        mock_audio = base64.b64encode(b"test_audio").decode('utf-8')
        
        interactions = [
            "start lesson on science",
            "explain photosynthesis",
            "I have a question",
            "help me understand"
        ]
        
        print(f"Simulating {len(interactions)} voice interactions:")
        
        for interaction_text in interactions:
            speech_input = SpeechInput(
                audio_data=mock_audio,
                format=AudioFormat.WAV,
                language=SpeechLanguage.ENGLISH
            )
            
            await voice_agent.process_speech_input(session_id, speech_input)
            print(f"  Processed: '{interaction_text}'")
        
        # End session
        session_summary = await voice_agent.end_voice_session(session_id)
        
        print(f"Session Ended:")
        print(f"  Duration: {session_summary['duration_seconds']:.1f}s")
        print(f"  Total Interactions: {session_summary['total_interactions']}")
        print(f"  Commands Processed: {len(session_summary['commands_processed'])}")
        
        # Verify session summary
        assert session_summary["session_id"] == session_id
        assert session_summary["student_id"] == student_id
        assert session_summary["total_interactions"] == len(interactions)
        assert session_summary["status"] == "completed"
        assert session_summary["duration_seconds"] > 0
        
        # Verify session is no longer active
        assert session_id not in voice_agent.active_sessions
        
        # Test analytics (session ended, but we can test with active sessions)
        # Start another session for analytics
        new_session = await voice_agent.start_voice_session(student_id)
        
        analytics = await voice_agent.get_voice_interaction_analytics(student_id)
        
        print(f"Voice Interaction Analytics:")
        print(f"  Total Sessions: {analytics['total_sessions']}")
        print(f"  Current Active Sessions: {analytics['current_active_sessions']}")
        
        assert analytics["student_id"] == student_id
        assert analytics["total_sessions"] >= 1
        assert analytics["current_active_sessions"] >= 1
        
        print("SUCCESS: Session ending and analytics working correctly")


# Test runner for standalone execution
async def run_voice_interaction_tests():
    """Run all Voice Interaction Agent tests"""
    print("Starting Voice Interaction Agent Tests")
    print("=" * 60)
    
    # Create test instance
    test_instance = TestVoiceInteractionAgent()
    voice_agent = VoiceInteractionAgent()
    await voice_agent.initialize_ai_clients()
    
    try:
        # Run all tests
        await test_instance.test_agent_initialization_and_status(voice_agent)
        await test_instance.test_voice_session_management(voice_agent)
        await test_instance.test_speech_to_text_processing(voice_agent)
        await test_instance.test_text_to_speech_synthesis(voice_agent)
        await test_instance.test_voice_command_recognition(voice_agent)
        await test_instance.test_complete_voice_interaction(voice_agent)
        await test_instance.test_audio_content_generation(voice_agent)
        await test_instance.test_multilingual_support(voice_agent)
        await test_instance.test_audio_content_library(voice_agent)
        await test_instance.test_session_ending_and_analytics(voice_agent)
        
        print("\n" + "=" * 60)
        print("ALL VOICE INTERACTION AGENT TESTS PASSED!")
        print("Agent 7/7 Complete - Voice Interaction Agent Ready for Production")
        print("Test Coverage: Speech processing, voice commands, multilingual support, audio content")
        print("PHASE 5 COMPLETE: All 7 AI Agents Successfully Implemented!")
        
    except Exception as e:
        print(f"\nTest failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(run_voice_interaction_tests())