#!/usr/bin/env python3
"""
Comprehensive CBSE Curriculum Validation Test
Validates Grade-Subject-Topic combinations for completeness and CBSE alignment
"""

import asyncio
import sys
import json
from typing import Dict, List, Set, Tuple
sys.path.append('.')

from core.curriculum import CBSECurriculum, Subject
from agents.content_generator import ContentGeneratorAgent, ContentRequest

class CurriculumValidator:
    def __init__(self):
        self.curriculum = CBSECurriculum()
        self.content_agent = ContentGeneratorAgent()
        self.validation_results = {}
        
    async def run_comprehensive_validation(self):
        """Run comprehensive curriculum validation"""
        print("COMPREHENSIVE CBSE CURRICULUM VALIDATION")
        print("=" * 60)
        
        await self.validate_grade_coverage()
        await self.validate_subject_coverage() 
        await self.validate_topic_completeness()
        await self.validate_progression_logic()
        await self.validate_content_generation_compatibility()
        await self.generate_validation_report()
    
    async def validate_grade_coverage(self):
        """Validate grade level coverage"""
        print("\n1. VALIDATING GRADE COVERAGE")
        print("-" * 40)
        
        expected_grades = set(range(1, 13))  # Grades 1-12 for CBSE
        available_grades = set()
        
        subjects_to_check = [Subject.MATHEMATICS, Subject.SCIENCE, Subject.ENGLISH, Subject.SOCIAL_STUDIES]
        
        grade_coverage = {}
        
        for subject in subjects_to_check:
            subject_data = self.curriculum._curriculum_data.get(subject, {})
            subject_grades = set(subject_data.keys())
            available_grades.update(subject_grades)
            grade_coverage[subject.value] = {
                'available_grades': sorted(list(subject_grades)),
                'missing_grades': sorted(list(expected_grades - subject_grades)),
                'coverage_percentage': (len(subject_grades) / len(expected_grades)) * 100
            }
            
            print(f"{subject.value}:")
            print(f"  Available Grades: {sorted(list(subject_grades))}")
            print(f"  Missing Grades: {sorted(list(expected_grades - subject_grades))}")
            print(f"  Coverage: {len(subject_grades)}/12 ({(len(subject_grades)/12)*100:.1f}%)")
        
        overall_missing = expected_grades - available_grades
        
        self.validation_results['grade_coverage'] = {
            'expected_grades': sorted(list(expected_grades)),
            'available_grades': sorted(list(available_grades)),
            'missing_grades': sorted(list(overall_missing)),
            'subject_breakdown': grade_coverage,
            'overall_coverage': (len(available_grades) / len(expected_grades)) * 100
        }
        
        print(f"\nOVERALL GRADE COVERAGE:")
        print(f"  Expected: {sorted(list(expected_grades))}")
        print(f"  Available: {sorted(list(available_grades))}")
        print(f"  Missing: {sorted(list(overall_missing))}")
        print(f"  Coverage: {len(available_grades)}/12 ({(len(available_grades)/12)*100:.1f}%)")
        
        status = "COMPLETE" if len(overall_missing) == 0 else "INCOMPLETE"
        print(f"  Status: {status}")
    
    async def validate_subject_coverage(self):
        """Validate subject coverage across grades"""
        print("\n2. VALIDATING SUBJECT COVERAGE")
        print("-" * 40)
        
        expected_subjects = [
            Subject.MATHEMATICS, Subject.SCIENCE, Subject.ENGLISH, Subject.SOCIAL_STUDIES,
            Subject.HINDI, Subject.SANSKRIT, Subject.COMPUTER_SCIENCE, 
            Subject.PHYSICAL_EDUCATION, Subject.ART_EDUCATION
        ]
        
        available_subjects = list(self.curriculum._curriculum_data.keys())
        missing_subjects = [s for s in expected_subjects if s not in available_subjects]
        
        subject_analysis = {}
        
        for subject in available_subjects:
            grades_available = list(self.curriculum._curriculum_data[subject].keys())
            total_topics = 0
            total_chapters = 0
            
            for grade, curriculum in self.curriculum._curriculum_data[subject].items():
                total_chapters += len(curriculum.chapters)
                for chapter in curriculum.chapters:
                    total_topics += len(chapter.topics)
            
            subject_analysis[subject.value] = {
                'grades_covered': sorted(grades_available),
                'total_chapters': total_chapters,
                'total_topics': total_topics,
                'avg_topics_per_grade': total_topics / len(grades_available) if grades_available else 0
            }
            
            print(f"{subject.value}:")
            print(f"  Grades: {sorted(grades_available)} ({len(grades_available)}/12)")
            print(f"  Total Chapters: {total_chapters}")
            print(f"  Total Topics: {total_topics}")
            print(f"  Avg Topics/Grade: {total_topics/len(grades_available):.1f}")
        
        self.validation_results['subject_coverage'] = {
            'expected_subjects': [s.value for s in expected_subjects],
            'available_subjects': [s.value for s in available_subjects],
            'missing_subjects': [s.value for s in missing_subjects],
            'subject_analysis': subject_analysis,
            'coverage_percentage': (len(available_subjects) / len(expected_subjects)) * 100
        }
        
        print(f"\nSUBJECT COVERAGE SUMMARY:")
        print(f"  Expected: {len(expected_subjects)} subjects")
        print(f"  Available: {len(available_subjects)} subjects")
        print(f"  Missing: {[s.value for s in missing_subjects]}")
        print(f"  Coverage: {(len(available_subjects)/len(expected_subjects))*100:.1f}%")
    
    async def validate_topic_completeness(self):
        """Validate topic completeness and age-appropriateness"""
        print("\n3. VALIDATING TOPIC COMPLETENESS")
        print("-" * 40)
        
        topic_analysis = {}
        
        for subject, grades_data in self.curriculum._curriculum_data.items():
            subject_name = subject.value
            topic_analysis[subject_name] = {}
            
            for grade, curriculum in grades_data.items():
                topics_data = []
                
                for chapter in curriculum.chapters:
                    for topic in chapter.topics:
                        topics_data.append({
                            'code': topic.code,
                            'name': topic.name,
                            'chapter': chapter.chapter_name,
                            'difficulty': topic.difficulty_level,
                            'estimated_hours': topic.estimated_hours,
                            'objectives_count': len(topic.learning_objectives),
                            'concepts_count': len(topic.key_concepts),
                            'prerequisites_count': len(topic.prerequisites)
                        })
                
                topic_analysis[subject_name][grade] = {
                    'total_topics': len(topics_data),
                    'total_chapters': len(curriculum.chapters),
                    'topics': topics_data,
                    'difficulty_distribution': self._analyze_difficulty_distribution(topics_data),
                    'avg_hours_per_topic': sum(t['estimated_hours'] for t in topics_data) / len(topics_data) if topics_data else 0
                }
                
                print(f"{subject_name} Grade {grade}:")
                print(f"  Topics: {len(topics_data)} across {len(curriculum.chapters)} chapters")
                print(f"  Difficulty: {topic_analysis[subject_name][grade]['difficulty_distribution']}")
                print(f"  Avg Hours/Topic: {topic_analysis[subject_name][grade]['avg_hours_per_topic']:.1f}")
        
        self.validation_results['topic_completeness'] = topic_analysis
    
    async def validate_progression_logic(self):
        """Validate logical progression of topics across grades"""
        print("\n4. VALIDATING PROGRESSION LOGIC")
        print("-" * 40)
        
        progression_analysis = {}
        
        # Check Mathematics progression
        math_progression = await self._check_math_progression()
        progression_analysis['Mathematics'] = math_progression
        print("Mathematics Progression:")
        for issue in math_progression.get('issues', []):
            print(f"  - {issue}")
        if not math_progression.get('issues'):
            print("  - Progression looks logical")
        
        # Check Science progression
        science_progression = await self._check_science_progression()
        progression_analysis['Science'] = science_progression
        print("\nScience Progression:")
        for issue in science_progression.get('issues', []):
            print(f"  - {issue}")
        if not science_progression.get('issues'):
            print("  - Progression looks logical")
        
        # Check English progression
        english_progression = await self._check_english_progression()
        progression_analysis['English'] = english_progression
        print("\nEnglish Progression:")
        for issue in english_progression.get('issues', []):
            print(f"  - {issue}")
        if not english_progression.get('issues'):
            print("  - Progression looks logical")
        
        self.validation_results['progression_logic'] = progression_analysis
    
    async def validate_content_generation_compatibility(self):
        """Test content generation with various Grade-Subject-Topic combinations"""
        print("\n5. VALIDATING CONTENT GENERATION COMPATIBILITY")
        print("-" * 40)
        
        test_combinations = []
        generation_results = {}
        
        # Sample test cases from available curriculum
        for subject, grades_data in self.curriculum._curriculum_data.items():
            for grade, curriculum in grades_data.items():
                if curriculum.chapters:
                    chapter = curriculum.chapters[0]
                    if chapter.topics:
                        topic = chapter.topics[0]
                        test_combinations.append({
                            'subject': subject.value,
                            'grade': grade,
                            'topic': topic.name,
                            'expected_difficulty': topic.difficulty_level
                        })
        
        # Limit to representative samples
        test_combinations = test_combinations[:10]
        
        successful_generations = 0
        
        for combo in test_combinations:
            try:
                request = ContentRequest(
                    subject=combo['subject'],
                    grade=combo['grade'],
                    topic=combo['topic'],
                    content_type='explanation',
                    difficulty=combo['expected_difficulty']
                )
                
                result = await self.content_agent.generate_content(request)
                
                generation_results[f"{combo['subject']}-{combo['grade']}-{combo['topic'][:20]}"] = {
                    'success': True,
                    'content_length': len(result.content),
                    'objectives_count': len(result.learning_objectives),
                    'estimated_time': result.estimated_time
                }
                successful_generations += 1
                print(f"  SUCCESS: {combo['subject']} Grade {combo['grade']} - {combo['topic'][:30]}...")
                
            except Exception as e:
                generation_results[f"{combo['subject']}-{combo['grade']}-{combo['topic'][:20]}"] = {
                    'success': False,
                    'error': str(e)
                }
                print(f"  FAILED: {combo['subject']} Grade {combo['grade']} - {combo['topic'][:30]}... ({str(e)[:50]})")
        
        compatibility_rate = (successful_generations / len(test_combinations)) * 100
        
        self.validation_results['content_generation_compatibility'] = {
            'total_tests': len(test_combinations),
            'successful_generations': successful_generations,
            'compatibility_rate': compatibility_rate,
            'detailed_results': generation_results
        }
        
        print(f"\nCONTENT GENERATION COMPATIBILITY:")
        print(f"  Total Tests: {len(test_combinations)}")
        print(f"  Successful: {successful_generations}")
        print(f"  Compatibility Rate: {compatibility_rate:.1f}%")
    
    async def generate_validation_report(self):
        """Generate comprehensive validation report"""
        print("\n6. COMPREHENSIVE VALIDATION REPORT")
        print("=" * 60)
        
        # Overall Status Assessment
        grade_coverage = self.validation_results['grade_coverage']['overall_coverage']
        subject_coverage = self.validation_results['subject_coverage']['coverage_percentage']
        compatibility_rate = self.validation_results['content_generation_compatibility']['compatibility_rate']
        
        overall_score = (grade_coverage + subject_coverage + compatibility_rate) / 3
        
        print(f"OVERALL CURRICULUM VALIDATION SCORE: {overall_score:.1f}%")
        print(f"")
        
        # Detailed Assessment
        print("DETAILED ASSESSMENT:")
        print(f"  Grade Coverage: {grade_coverage:.1f}% - {'GOOD' if grade_coverage > 80 else 'NEEDS IMPROVEMENT'}")
        print(f"  Subject Coverage: {subject_coverage:.1f}% - {'GOOD' if subject_coverage > 70 else 'NEEDS IMPROVEMENT'}")
        print(f"  Content Generation: {compatibility_rate:.1f}% - {'EXCELLENT' if compatibility_rate > 90 else 'GOOD' if compatibility_rate > 80 else 'NEEDS IMPROVEMENT'}")
        
        # Critical Issues
        missing_grades = self.validation_results['grade_coverage']['missing_grades']
        missing_subjects = self.validation_results['subject_coverage']['missing_subjects']
        
        print(f"\nCRITICAL ISSUES:")
        if missing_grades:
            print(f"  - Missing Grade Levels: {missing_grades}")
        if missing_subjects:
            print(f"  - Missing Subjects: {missing_subjects}")
        if not missing_grades and not missing_subjects:
            print(f"  - No critical structural issues found")
        
        # Recommendations
        print(f"\nRECOMMENDATIONS:")
        
        if grade_coverage < 100:
            missing_count = len(missing_grades)
            print(f"  1. HIGH PRIORITY: Add curriculum data for {missing_count} missing grades")
        
        if subject_coverage < 100:
            print(f"  2. MEDIUM PRIORITY: Add {len(missing_subjects)} missing subjects")
        
        if compatibility_rate < 100:
            failed_count = self.validation_results['content_generation_compatibility']['total_tests'] - self.validation_results['content_generation_compatibility']['successful_generations']
            print(f"  3. LOW PRIORITY: Fix {failed_count} content generation compatibility issues")
        
        # Summary
        if overall_score >= 90:
            status = "EXCELLENT - Ready for production"
        elif overall_score >= 80:
            status = "GOOD - Minor improvements needed"
        elif overall_score >= 70:
            status = "FAIR - Moderate improvements required"
        else:
            status = "POOR - Major improvements required"
        
        print(f"\nFINAL STATUS: {status}")
        print("=" * 60)
    
    def _analyze_difficulty_distribution(self, topics: List[Dict]) -> Dict:
        """Analyze difficulty distribution of topics"""
        if not topics:
            return {}
        
        difficulty_counts = {}
        for topic in topics:
            difficulty = topic.get('difficulty', 'unknown')
            difficulty_counts[difficulty] = difficulty_counts.get(difficulty, 0) + 1
        
        return difficulty_counts
    
    async def _check_math_progression(self) -> Dict:
        """Check mathematics progression logic"""
        issues = []
        math_data = self.curriculum._curriculum_data.get(Subject.MATHEMATICS, {})
        
        # Check if basic concepts come before advanced ones
        grades_available = sorted(math_data.keys())
        
        # Expected progression patterns
        expected_progression = {
            1: ['counting', 'addition'],
            2: ['place value', 'subtraction'],
            3: ['multiplication', '3-digit'],
            4: ['division', 'fractions', 'decimals'],
            5: ['large numbers', 'geometry']
        }
        
        for grade, expected_topics in expected_progression.items():
            if grade in math_data:
                curriculum = math_data[grade]
                all_topics = []
                for chapter in curriculum.chapters:
                    for topic in chapter.topics:
                        all_topics.append(topic.name.lower())
                
                for expected in expected_topics:
                    found = any(expected in topic for topic in all_topics)
                    if not found:
                        issues.append(f"Grade {grade} missing expected topic area: {expected}")
        
        return {'issues': issues, 'grades_checked': grades_available}
    
    async def _check_science_progression(self) -> Dict:
        """Check science progression logic"""
        issues = []
        science_data = self.curriculum._curriculum_data.get(Subject.SCIENCE, {})
        grades_available = sorted(science_data.keys())
        
        # Expected progression patterns
        expected_progression = {
            1: ['living', 'non-living'],
            2: ['plants', 'animals'],
            3: ['body', 'senses'],
            4: ['life cycle', 'environment'],
            5: ['senses', 'adaptation']
        }
        
        for grade, expected_topics in expected_progression.items():
            if grade in science_data:
                curriculum = science_data[grade]
                all_topics = []
                for chapter in curriculum.chapters:
                    for topic in chapter.topics:
                        all_topics.append(topic.name.lower())
                
                for expected in expected_topics:
                    found = any(expected in topic for topic in all_topics)
                    if not found:
                        issues.append(f"Grade {grade} missing expected science topic: {expected}")
        
        return {'issues': issues, 'grades_checked': grades_available}
    
    async def _check_english_progression(self) -> Dict:
        """Check English progression logic"""
        issues = []
        english_data = self.curriculum._curriculum_data.get(Subject.ENGLISH, {})
        grades_available = sorted(english_data.keys())
        
        # Expected progression patterns
        expected_progression = {
            1: ['alphabet', 'phonics'],
            2: ['reading', 'sentences'],
            3: ['comprehension', 'stories'],
            4: ['poetry', 'grammar'],
            5: ['analysis', 'writing']
        }
        
        for grade, expected_topics in expected_progression.items():
            if grade in english_data:
                curriculum = english_data[grade]
                all_topics = []
                for chapter in curriculum.chapters:
                    for topic in chapter.topics:
                        all_topics.append(topic.name.lower())
                
                for expected in expected_topics:
                    found = any(expected in topic for topic in all_topics)
                    if not found:
                        issues.append(f"Grade {grade} missing expected English topic: {expected}")
        
        return {'issues': issues, 'grades_checked': grades_available}

async def main():
    """Main validation execution"""
    validator = CurriculumValidator()
    await validator.run_comprehensive_validation()

if __name__ == "__main__":
    asyncio.run(main())