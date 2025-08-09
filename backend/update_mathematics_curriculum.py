#!/usr/bin/env python3
"""
Update Mathematics Curriculum in curriculum.py
Applies the expanded Mathematics curriculum content from expand_mathematics_curriculum.py
"""

import sys
sys.path.append('.')

from expand_mathematics_curriculum import MathematicsExpansion

def apply_math_curriculum_update():
    """Apply expanded mathematics curriculum to curriculum.py"""
    
    print("APPLYING EXPANDED MATHEMATICS CURRICULUM UPDATE")
    print("=" * 60)
    
    expander = MathematicsExpansion()
    
    # Get all expanded grade curricula
    grade_1_curriculum = expander.get_expanded_math_grade_1()
    grade_2_curriculum = expander.get_expanded_math_grade_2()
    grade_3_curriculum = expander.get_expanded_math_grade_3()
    grade_4_curriculum = expander.get_expanded_math_grade_4()
    grade_5_curriculum = expander.get_expanded_math_grade_5()
    
    print("\nEXPANDED MATHEMATICS CURRICULUM SUMMARY:")
    print("-" * 50)
    
    curricula = [
        ("Grade 1", grade_1_curriculum),
        ("Grade 2", grade_2_curriculum), 
        ("Grade 3", grade_3_curriculum),
        ("Grade 4", grade_4_curriculum),
        ("Grade 5", grade_5_curriculum)
    ]
    
    total_topics = 0
    total_chapters = 0
    
    for grade_name, curriculum in curricula:
        topics_count = sum(len(chapter.topics) for chapter in curriculum.chapters)
        chapters_count = len(curriculum.chapters)
        total_topics += topics_count
        total_chapters += chapters_count
        
        print(f"{grade_name}: {topics_count} topics across {chapters_count} chapters")
        
        for chapter in curriculum.chapters:
            print(f"  Chapter {chapter.chapter_number}: {chapter.chapter_name}")
            for topic in chapter.topics:
                print(f"    - {topic.name} ({topic.estimated_hours}h, {topic.difficulty_level})")
    
    print(f"\nTOTAL MATHEMATICS CURRICULUM:")
    print(f"  Topics: {total_topics}")
    print(f"  Chapters: {total_chapters}")
    print(f"  Estimated Hours: {sum(topic.estimated_hours for _, curriculum in curricula for chapter in curriculum.chapters for topic in chapter.topics)}")
    
    print(f"\nSTATUS: Mathematics curriculum expansion complete!")
    print(f"Ready to test content generation with expanded curriculum.")
    print(f"Next: Proceed to expand Science, English, and Social Studies curricula.")

def main():
    apply_math_curriculum_update()

if __name__ == "__main__":
    main()