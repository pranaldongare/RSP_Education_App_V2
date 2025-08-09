#!/usr/bin/env python3
"""
Integrate Expanded Science Curriculum into main curriculum.py
Replaces the basic Science methods with comprehensive versions
"""

import sys
sys.path.append('.')

from expand_science_curriculum import ScienceExpansion

def integrate_science_curriculum():
    """
    Generate the complete Science curriculum methods to replace in curriculum.py
    """
    expansion = ScienceExpansion()
    
    print("INTEGRATING EXPANDED SCIENCE CURRICULUM")
    print("=" * 50)
    
    # Generate all Science grade methods
    grades = [1, 2, 3, 4, 5]
    
    for grade in grades:
        method_name = f"get_expanded_science_grade_{grade}"
        if hasattr(expansion, method_name):
            curriculum = getattr(expansion, method_name)()
            
            print(f"\nGrade {grade} Science:")
            print(f"- Chapters: {len(curriculum.chapters)}")
            total_topics = sum(len(chapter.topics) for chapter in curriculum.chapters)
            print(f"- Topics: {total_topics}")
            
            # Print chapter structure
            for chapter in curriculum.chapters:
                print(f"  • Chapter {chapter.chapter_number}: {chapter.chapter_name} ({len(chapter.topics)} topics)")
    
    print(f"\nSTATUS: Ready to replace _get_science_grade_X methods in curriculum.py")
    print("Next: Manual integration required - replace the 5 science methods")

if __name__ == "__main__":
    integrate_science_curriculum()