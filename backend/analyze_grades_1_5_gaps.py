#!/usr/bin/env python3
"""
Analyze Grades 1-5 Curriculum Gaps
Detailed analysis of missing content in primary grades to guide expansion
"""

import asyncio
import sys
sys.path.append('.')

from core.curriculum import CBSECurriculum, Subject

class Grades15GapAnalyzer:
    def __init__(self):
        self.curriculum = CBSECurriculum()
        self.target_grades = [1, 2, 3, 4, 5]
        self.target_subjects = [Subject.MATHEMATICS, Subject.SCIENCE, Subject.ENGLISH, Subject.SOCIAL_STUDIES]
        self.missing_subjects = [Subject.HINDI, Subject.COMPUTER_SCIENCE, Subject.PHYSICAL_EDUCATION, Subject.ART_EDUCATION]
        
    async def analyze_current_coverage(self):
        """Analyze current coverage for Grades 1-5"""
        print("GRADES 1-5 CURRICULUM GAP ANALYSIS")
        print("=" * 50)
        
        coverage_data = {}
        
        for subject in self.target_subjects:
            subject_name = subject.value
            coverage_data[subject_name] = {}
            
            print(f"\n{subject_name} COVERAGE:")
            print("-" * 30)
            
            for grade in self.target_grades:
                curriculum = await self.curriculum.get_subject_curriculum(subject_name, grade)
                
                if curriculum:
                    total_chapters = len(curriculum.chapters)
                    total_topics = sum(len(chapter.topics) for chapter in curriculum.chapters)
                    
                    coverage_data[subject_name][grade] = {
                        'available': True,
                        'chapters': total_chapters,
                        'topics': total_topics,
                        'chapter_details': []
                    }
                    
                    print(f"  Grade {grade}: {total_topics} topics across {total_chapters} chapters")
                    
                    for chapter in curriculum.chapters:
                        chapter_info = {
                            'name': chapter.chapter_name,
                            'topics': [topic.name for topic in chapter.topics]
                        }
                        coverage_data[subject_name][grade]['chapter_details'].append(chapter_info)
                        
                        print(f"    Chapter: {chapter.chapter_name}")
                        for topic in chapter.topics:
                            print(f"      - {topic.name}")
                else:
                    coverage_data[subject_name][grade] = {'available': False}
                    print(f"  Grade {grade}: NO CURRICULUM DATA")
        
        await self.identify_specific_gaps(coverage_data)
        await self.recommend_expansion_priorities()
    
    async def identify_specific_gaps(self, coverage_data):
        """Identify specific gaps in current curriculum"""
        print(f"\nSPECIFIC GAPS IDENTIFIED:")
        print("-" * 30)
        
        # Mathematics gaps
        math_expected_topics = {
            1: ['Counting 1-20', 'Addition up to 20', 'Subtraction up to 20', 'Shapes', 'Patterns', 'Time', 'Money'],
            2: ['Numbers up to 100', 'Addition with regrouping', 'Subtraction with regrouping', 'Multiplication tables', 'Measurement', 'Data handling'],
            3: ['Numbers up to 1000', 'Multiplication', 'Division', 'Fractions', 'Time and calendar', 'Geometry'],
            4: ['Large numbers', 'All operations', 'Fractions', 'Decimals', 'Measurement', 'Geometry', 'Data handling'],
            5: ['Large numbers', 'Decimals', 'Fractions operations', 'Percentage', 'Geometry', 'Area and perimeter', 'Data interpretation']
        }
        
        print("Mathematics Gaps:")
        for grade, expected in math_expected_topics.items():
            current = coverage_data.get('Mathematics', {}).get(grade, {})
            if current.get('available'):
                current_topics = []
                for chapter in current.get('chapter_details', []):
                    current_topics.extend(chapter['topics'])
                
                missing_topics = []
                for expected_topic in expected:
                    found = any(expected_topic.lower() in topic.lower() for topic in current_topics)
                    if not found:
                        missing_topics.append(expected_topic)
                
                if missing_topics:
                    print(f"  Grade {grade}: Missing {missing_topics}")
                else:
                    print(f"  Grade {grade}: Well covered")
            else:
                print(f"  Grade {grade}: COMPLETELY MISSING")
        
        # Science gaps
        science_expected_topics = {
            1: ['Living and non-living', 'Plants around us', 'Animals around us', 'My body', 'Food', 'Water'],
            2: ['Plants', 'Animals', 'Food and health', 'Materials', 'Weather', 'Safety'],
            3: ['Plant life', 'Animal life', 'My body', 'Food and nutrition', 'Water', 'Shelter', 'Transport'],
            4: ['Plants', 'Animals', 'Food', 'Housing', 'Water', 'Travel and transport', 'Things we make'],
            5: ['Plant and animal life', 'Human body', 'Food and health', 'Materials', 'Water', 'Shelter', 'Travel']
        }
        
        print(f"\nScience Gaps:")
        for grade, expected in science_expected_topics.items():
            current = coverage_data.get('Science', {}).get(grade, {})
            if current.get('available'):
                print(f"  Grade {grade}: Only {current.get('topics', 0)} topics (Expected ~{len(expected)})")
            else:
                print(f"  Grade {grade}: COMPLETELY MISSING")
        
        # English gaps  
        english_expected_topics = {
            1: ['Alphabets', 'Phonics', 'Simple words', 'Reading', 'Writing', 'Speaking', 'Listening'],
            2: ['Reading skills', 'Writing skills', 'Grammar basics', 'Vocabulary', 'Stories', 'Poems'],
            3: ['Reading comprehension', 'Creative writing', 'Grammar', 'Vocabulary building', 'Literature'],
            4: ['Advanced reading', 'Essay writing', 'Grammar rules', 'Literature appreciation', 'Public speaking'],
            5: ['Critical reading', 'Creative expression', 'Advanced grammar', 'Research skills', 'Presentation']
        }
        
        print(f"\nEnglish Gaps:")
        for grade, expected in english_expected_topics.items():
            current = coverage_data.get('English', {}).get(grade, {})
            if current.get('available'):
                print(f"  Grade {grade}: Only {current.get('topics', 0)} topics (Expected ~{len(expected)})")
            else:
                print(f"  Grade {grade}: COMPLETELY MISSING")
        
        # Social Studies gaps
        social_expected_topics = {
            1: ['Myself', 'My family', 'My home', 'My school', 'My neighborhood'],
            2: ['Family and friends', 'Community helpers', 'Our neighborhood', 'Festivals', 'Transport'],
            3: ['Our community', 'Our environment', 'Our country', 'Good habits', 'Safety rules'],
            4: ['Our state', 'Our country India', 'Maps and directions', 'Our past', 'Government'],
            5: ['India our country', 'Our earth', 'Our past and present', 'Our government', 'Our culture']
        }
        
        print(f"\nSocial Studies Gaps:")
        for grade, expected in social_expected_topics.items():
            current = coverage_data.get('Social Studies', {}).get(grade, {})
            if current.get('available'):
                print(f"  Grade {grade}: Only {current.get('topics', 0)} topics (Expected ~{len(expected)})")
            else:
                print(f"  Grade {grade}: COMPLETELY MISSING")
        
        # Missing subjects
        print(f"\nCOMPLETELY MISSING SUBJECTS:")
        for subject in self.missing_subjects:
            print(f"  {subject.value}: 0 topics across all grades 1-5")
    
    async def recommend_expansion_priorities(self):
        """Recommend expansion priorities"""
        print(f"\nEXPANSION PRIORITIES FOR GRADES 1-5:")
        print("-" * 40)
        
        print("PHASE 1: EXPAND EXISTING SUBJECTS (4-6 weeks)")
        print("  Priority: CRITICAL - Complete foundation")
        print("")
        print("  Mathematics Expansion:")
        print("    - Grade 1: Add 4 more topics (shapes, patterns, time, money)")
        print("    - Grade 2: Add 5 more topics (complete place value, operations)")
        print("    - Grade 3: Add 4 more topics (multiplication, division, time)")
        print("    - Grade 4: Keep current comprehensive coverage") 
        print("    - Grade 5: Add 3 more topics (percentage, area, advanced geometry)")
        print("")
        print("  Science Expansion:")
        print("    - All Grades: Expand from 1 topic to 6-8 topics per grade")
        print("    - Focus: Living world, materials, forces, earth science")
        print("    - Include: Practical activities, observations, experiments")
        print("")
        print("  English Expansion:")
        print("    - All Grades: Expand from 1 topic to 6-7 topics per grade")
        print("    - Focus: Reading, writing, speaking, listening, grammar")
        print("    - Include: Literature, creative expression, communication")
        print("")
        print("  Social Studies Expansion:")
        print("    - All Grades: Expand from 1 topic to 5-6 topics per grade")
        print("    - Focus: Social awareness, geography, history, civics")
        print("    - Include: Cultural awareness, national identity")
        
        print(f"\nPHASE 2: ADD MISSING SUBJECTS (6-8 weeks)")
        print("  Priority: HIGH - Holistic education")
        print("")
        print("  Hindi (All Grades 1-5):")
        print("    - Devanagari script, vocabulary, grammar")
        print("    - Reading, writing, literature, cultural stories")
        print("    - 6-8 topics per grade")
        print("")
        print("  Computer Science (Grades 3-5):")
        print("    - Basic computer awareness, typing, drawing")
        print("    - Introduction to coding concepts")
        print("    - 4-5 topics per grade")
        print("")
        print("  Physical Education (All Grades 1-5):")
        print("    - Health and hygiene, basic exercises")
        print("    - Games, sports, fitness activities")
        print("    - 4-5 topics per grade")
        print("")
        print("  Art Education (All Grades 1-5):")
        print("    - Drawing, coloring, crafts, music")
        print("    - Creative expression, cultural arts")
        print("    - 4-5 topics per grade")
        
        print(f"\nESTIMATED DELIVERABLES:")
        print("  Phase 1: ~80 new topics for existing subjects")
        print("  Phase 2: ~90 new topics for missing subjects") 
        print("  Total: ~170 new topics for complete Grades 1-5 coverage")
        print("  Expected outcome: 8-10 topics per subject per grade")

async def main():
    analyzer = Grades15GapAnalyzer()
    await analyzer.analyze_current_coverage()

if __name__ == "__main__":
    asyncio.run(main())