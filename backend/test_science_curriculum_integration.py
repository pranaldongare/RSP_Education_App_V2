#!/usr/bin/env python3
"""
Test Science Curriculum Integration for Grades 1-5
Verify that the expanded Science curriculum is properly integrated
"""

import sys
sys.path.append('.')

from core.curriculum import CBSECurriculum, Subject

def test_science_curriculum_integration():
    """Test the integrated Science curriculum for all grades"""
    
    print("TESTING SCIENCE CURRICULUM INTEGRATION")
    print("=" * 50)
    
    try:
        curriculum = CBSECurriculum()
        
        total_science_topics = 0
        total_science_chapters = 0
        
        # Test each grade 1-5
        for grade in range(1, 6):
            print(f"\nGRADE {grade} SCIENCE CURRICULUM:")
            print("-" * 30)
            
            try:
                # Get Science curriculum for this grade
                science_curriculum = curriculum.get_subject_curriculum(Subject.SCIENCE, grade)
                
                if science_curriculum:
                    chapters = science_curriculum.chapters
                    print(f"✅ Grade {grade}: {len(chapters)} chapters")
                    
                    grade_topics = 0
                    for i, chapter in enumerate(chapters, 1):
                        topics_count = len(chapter.topics)
                        grade_topics += topics_count
                        print(f"   Chapter {i}: {chapter.chapter_name} ({topics_count} topics)")
                        
                        # Show first topic as example
                        if chapter.topics:
                            first_topic = chapter.topics[0]
                            print(f"     • {first_topic.name} ({first_topic.code})")
                    
                    total_science_topics += grade_topics
                    total_science_chapters += len(chapters)
                    
                    print(f"   Total Grade {grade} Topics: {grade_topics}")
                    print(f"   Assessment Pattern: {science_curriculum.assessment_pattern}")
                    
                else:
                    print(f"❌ Grade {grade}: No Science curriculum found!")
                    
            except Exception as e:
                print(f"❌ Grade {grade}: Error loading curriculum - {e}")
        
        print(f"\nSCIENCE CURRICULUM SUMMARY:")
        print("=" * 30)
        print(f"Total Science Chapters (Grades 1-5): {total_science_chapters}")
        print(f"Total Science Topics (Grades 1-5): {total_science_topics}")
        
        if total_science_topics >= 30:  # Expecting at least 6 topics per grade
            print("✅ SCIENCE CURRICULUM INTEGRATION SUCCESSFUL!")
            print("✅ All grades have comprehensive Science curriculum")
        else:
            print("⚠️  Science curriculum may need more topics")
            
        # Test content generation with Science
        print(f"\nTESTING SCIENCE CONTENT GENERATION:")
        print("-" * 30)
        
        # Test with Grade 3 Science topic (should have comprehensive curriculum)
        test_topic = "Life Cycle of Plants"
        grade = 3
        
        print(f"Testing content generation for: Grade {grade} - {test_topic}")
        
        # Try to find this topic in the curriculum
        science_curriculum = curriculum.get_subject_curriculum(Subject.SCIENCE, grade)
        found_topic = None
        
        if science_curriculum:
            for chapter in science_curriculum.chapters:
                for topic in chapter.topics:
                    if test_topic.lower() in topic.name.lower():
                        found_topic = topic
                        break
                if found_topic:
                    break
        
        if found_topic:
            print(f"✅ Found topic: {found_topic.name} ({found_topic.code})")
            print(f"   Learning Objectives: {len(found_topic.learning_objectives)}")
            print(f"   Key Concepts: {found_topic.key_concepts}")
            print("✅ Ready for AI content generation!")
        else:
            print("❌ Topic not found in curriculum")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        
    print(f"\nSCIENCE INTEGRATION TEST COMPLETE")

if __name__ == "__main__":
    test_science_curriculum_integration()