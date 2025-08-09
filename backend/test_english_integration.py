#!/usr/bin/env python3
"""
Test English curriculum expansion integration
Quick test to verify English expansion works
"""

import sys
sys.path.append('.')

from expand_english_curriculum import EnglishExpansion

def test_english_expansion():
    """Test the English curriculum expansion"""
    
    expansion = EnglishExpansion()
    
    print("TESTING ENGLISH CURRICULUM EXPANSION")
    print("=" * 50)
    
    total_topics = 0
    
    for grade in range(1, 6):
        try:
            method_name = f"get_expanded_english_grade_{grade}"
            curriculum = getattr(expansion, method_name)()
            
            topics = sum(len(ch.topics) for ch in curriculum.chapters)
            total_topics += topics
            
            print(f"✅ Grade {grade} English: {len(curriculum.chapters)} chapters, {topics} topics")
            
            # Show sample topic for verification
            if curriculum.chapters and curriculum.chapters[0].topics:
                sample_topic = curriculum.chapters[0].topics[0]
                print(f"   Sample: {sample_topic.name} ({sample_topic.code})")
                print(f"   Learning Objectives: {len(sample_topic.learning_objectives)}")
            
        except Exception as e:
            print(f"❌ Grade {grade} English: ERROR - {e}")
    
    print(f"\nENGLISH EXPANSION SUMMARY:")
    print(f"✅ Total English Topics: {total_topics}")
    print(f"✅ Average per Grade: {total_topics/5}")
    print(f"✅ Expansion Factor: {total_topics/5:.0f}x increase (from 1 topic per grade)")
    
    if total_topics == 40:
        print("🎉 ENGLISH CURRICULUM EXPANSION SUCCESSFUL!")
        print("📚 Ready for AI content generation")
    else:
        print("⚠️ Expected 40 topics, got", total_topics)
    
    print("\nNext Steps:")
    print("1. Integrate English expansion into curriculum.py")  
    print("2. Test content generation with new English topics")
    print("3. Continue with Social Studies expansion")

if __name__ == "__main__":
    test_english_expansion()