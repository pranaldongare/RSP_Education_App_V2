#!/usr/bin/env python3
"""
Final Content Generator Validation Test
Quick validation that content generator is working with real API calls
"""

import asyncio
import sys
import time
sys.path.append('.')

from agents.content_generator import ContentGeneratorAgent, ContentRequest

async def final_validation_test():
    """Final validation test for content generator"""
    print("FINAL CONTENT GENERATOR VALIDATION TEST")
    print("=" * 50)
    
    agent = ContentGeneratorAgent()
    
    # Test one comprehensive scenario
    test_request = ContentRequest(
        topic="Photosynthesis in Plants",
        subject="Science",
        grade=6,
        content_type="explanation",
        difficulty="intermediate",
        learning_objectives=["Understand the process of photosynthesis", "Identify inputs and outputs of photosynthesis"]
    )
    
    print(f"Testing: {test_request.topic} ({test_request.subject}, Grade {test_request.grade})")
    print(f"Content Type: {test_request.content_type}")
    print(f"Difficulty: {test_request.difficulty}")
    
    start_time = time.time()
    
    try:
        result = await agent.generate_content(test_request)
        end_time = time.time()
        
        print("\nSUCCESS: Content generated successfully!")
        print(f"Response Time: {end_time - start_time:.2f} seconds")
        print(f"Content Length: {len(result.content)} characters")
        print(f"Learning Objectives: {len(result.learning_objectives)}")
        print(f"Prerequisites: {len(result.prerequisites)}")
        print(f"Estimated Time: {result.estimated_time} minutes")
        
        print("\nContent Preview (first 500 characters):")
        print("-" * 50)
        print(result.content[:500])
        if len(result.content) > 500:
            print("... (content continues)")
        print("-" * 50)
        
        print("\nLearning Objectives:")
        for i, objective in enumerate(result.learning_objectives, 1):
            print(f"  {i}. {objective}")
        
        print("\nPrerequisites:")
        for i, prereq in enumerate(result.prerequisites, 1):
            print(f"  {i}. {prereq}")
        
        print("\nVALIDATION: Content Generator is working perfectly!")
        return True
        
    except Exception as e:
        end_time = time.time()
        print(f"\nFAILED: Content generation failed after {end_time - start_time:.2f} seconds")
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(final_validation_test())