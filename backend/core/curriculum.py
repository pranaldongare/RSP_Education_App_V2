"""
CBSE Curriculum Structure and Management
Provides structured access to CBSE curriculum data for Grades 1-12
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass

from pydantic import BaseModel


class Subject(str, Enum):
    """CBSE Subjects"""
    MATHEMATICS = "Mathematics"
    SCIENCE = "Science"
    ENGLISH = "English"
    SOCIAL_STUDIES = "Social Studies"
    HINDI = "Hindi"
    SANSKRIT = "Sanskrit"
    COMPUTER_SCIENCE = "Computer Science"
    PHYSICAL_EDUCATION = "Physical Education"
    ART_EDUCATION = "Art Education"


@dataclass
class CurriculumTopic:
    """Individual curriculum topic structure"""
    code: str
    name: str
    chapter: str
    learning_objectives: List[str]
    key_concepts: List[str]
    prerequisites: List[str]
    difficulty_level: str
    estimated_hours: int
    assessment_type: List[str]


@dataclass
class CurriculumChapter:
    """Chapter structure in curriculum"""
    chapter_number: int
    chapter_name: str
    topics: List[CurriculumTopic]
    learning_outcomes: List[str]
    skills_developed: List[str]


@dataclass
class SubjectCurriculum:
    """Complete subject curriculum for a grade"""
    subject: Subject
    grade: int
    chapters: List[CurriculumChapter]
    yearly_learning_outcomes: List[str]
    assessment_pattern: Dict[str, Any]


class CBSECurriculum:
    """
    CBSE Curriculum Manager
    Provides structured access to curriculum data for content generation
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.CBSECurriculum")
        self._curriculum_data = {}
        self._initialize_curriculum()
    
    def _initialize_curriculum(self):
        """Initialize curriculum data structure"""
        try:
            # Mathematics Curriculum (Sample for Grades 1-5)
            self._curriculum_data = {
                Subject.MATHEMATICS: {
                    1: self._get_math_grade_1(),
                    2: self._get_math_grade_2(),
                    3: self._get_math_grade_3(),
                    4: self._get_math_grade_4(),
                    5: self._get_math_grade_5(),
                    # Add more grades as needed
                },
                Subject.SCIENCE: {
                    1: self._get_science_grade_1(),
                    2: self._get_science_grade_2(),
                    3: self._get_science_grade_3(),
                    4: self._get_science_grade_4(),
                    5: self._get_science_grade_5(),
                },
                Subject.ENGLISH: {
                    1: self._get_english_grade_1(),
                    2: self._get_english_grade_2(),
                    3: self._get_english_grade_3(),
                    4: self._get_english_grade_4(),
                    5: self._get_english_grade_5(),
                },
                Subject.SOCIAL_STUDIES: {
                    1: self._get_social_studies_grade_1(),
                    2: self._get_social_studies_grade_2(),
                    3: self._get_social_studies_grade_3(),
                    4: self._get_social_studies_grade_4(),
                    5: self._get_social_studies_grade_5(),
                }
            }
            
            self.logger.info("CBSE Curriculum initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize curriculum: {e}")
            raise

    async def get_subject_curriculum(self, subject: str, grade: int) -> Optional[SubjectCurriculum]:
        """Get complete curriculum for a subject and grade"""
        try:
            subject_enum = Subject(subject)
            curriculum_data = self._curriculum_data.get(subject_enum, {}).get(grade)
            
            if curriculum_data:
                return curriculum_data
                
            self.logger.warning(f"Curriculum not found for {subject} Grade {grade}")
            return None
            
        except Exception as e:
            self.logger.error(f"Error retrieving curriculum: {e}")
            return None

    async def get_topic_details(self, subject: str, grade: int, topic: str) -> Optional[Dict[str, Any]]:
        """Get details for a specific topic"""
        try:
            curriculum = await self.get_subject_curriculum(subject, grade)
            if not curriculum:
                return None
            
            # Search through all chapters for the topic
            for chapter in curriculum.chapters:
                for curriculum_topic in chapter.topics:
                    if curriculum_topic.name.lower() == topic.lower() or topic.lower() in curriculum_topic.name.lower():
                        return {
                            "code": curriculum_topic.code,
                            "name": curriculum_topic.name,
                            "chapter": chapter.chapter_name,
                            "learning_objectives": curriculum_topic.learning_objectives,
                            "key_concepts": curriculum_topic.key_concepts,
                            "prerequisites": curriculum_topic.prerequisites,
                            "difficulty_level": curriculum_topic.difficulty_level,
                            "estimated_hours": curriculum_topic.estimated_hours,
                            "assessment_type": curriculum_topic.assessment_type
                        }
            
            self.logger.warning(f"Topic '{topic}' not found in {subject} Grade {grade}")
            return None
            
        except Exception as e:
            self.logger.error(f"Error retrieving topic details: {e}")
            return None

    async def get_chapter_topics(self, subject: str, grade: int, chapter_number: int) -> List[str]:
        """Get all topics in a specific chapter"""
        try:
            curriculum = await self.get_subject_curriculum(subject, grade)
            if not curriculum:
                return []
            
            for chapter in curriculum.chapters:
                if chapter.chapter_number == chapter_number:
                    return [topic.name for topic in chapter.topics]
            
            return []
            
        except Exception as e:
            self.logger.error(f"Error retrieving chapter topics: {e}")
            return []

    async def get_learning_objectives(self, subject: str, grade: int, topic: str) -> List[str]:
        """Get learning objectives for a specific topic"""
        topic_details = await self.get_topic_details(subject, grade, topic)
        return topic_details.get("learning_objectives", []) if topic_details else []

    async def get_prerequisites(self, subject: str, grade: int, topic: str) -> List[str]:
        """Get prerequisites for a specific topic"""
        topic_details = await self.get_topic_details(subject, grade, topic)
        return topic_details.get("prerequisites", []) if topic_details else []

    def _get_math_grade_1(self) -> SubjectCurriculum:
        """Enhanced Mathematics curriculum for Grade 1 - Complete Coverage"""
        return SubjectCurriculum(
            subject=Subject.MATHEMATICS,
            grade=1,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="Numbers up to 20",
                    topics=[
                        CurriculumTopic(
                            code="M1-1-1",
                            name="Counting Numbers 1-20",
                            chapter="Numbers up to 20",
                            learning_objectives=[
                                "Count objects up to 20",
                                "Recognize and write numbers 1-20",
                                "Understand number sequence",
                                "Match numbers with quantities"
                            ],
                            key_concepts=["Counting", "Number recognition", "Number sequence", "One-to-one correspondence"],
                            prerequisites=["Basic observation skills"],
                            difficulty_level="beginner",
                            estimated_hours=12,
                            assessment_type=["oral", "written", "practical"]
                        ),
                        CurriculumTopic(
                            code="M1-1-2",
                            name="Number Comparison up to 20",
                            chapter="Numbers up to 20",
                            learning_objectives=[
                                "Compare numbers using more/less/equal",
                                "Arrange numbers in ascending/descending order",
                                "Use comparison symbols"
                            ],
                            key_concepts=["Comparison", "Greater than", "Less than", "Equal to", "Ordering"],
                            prerequisites=["Number recognition 1-20"],
                            difficulty_level="beginner",
                            estimated_hours=8,
                            assessment_type=["written", "practical"]
                        ),
                        CurriculumTopic(
                            code="M1-1-3",
                            name="Before, After, and Between",
                            chapter="Numbers up to 20",
                            learning_objectives=[
                                "Identify number before and after a given number",
                                "Find numbers between two given numbers",
                                "Complete number patterns"
                            ],
                            key_concepts=["Before", "After", "Between", "Number line", "Patterns"],
                            prerequisites=["Number sequence 1-20"],
                            difficulty_level="beginner",
                            estimated_hours=6,
                            assessment_type=["written", "practical"]
                        )
                    ],
                    learning_outcomes=["Master numbers 1-20 with comparison and ordering"],
                    skills_developed=["Number sense", "Logical thinking", "Pattern recognition"]
                ),
                CurriculumChapter(
                    chapter_number=2,
                    chapter_name="Addition",
                    topics=[
                        CurriculumTopic(
                            code="M1-2-1",
                            name="Addition up to 10",
                            chapter="Addition",
                            learning_objectives=[
                                "Understand concept of addition as combining",
                                "Add numbers with sum up to 10",
                                "Use addition symbol (+)",
                                "Solve simple addition problems"
                            ],
                            key_concepts=["Addition", "Sum", "Plus", "Combining", "Total"],
                            prerequisites=["Counting 1-10"],
                            difficulty_level="beginner",
                            estimated_hours=10,
                            assessment_type=["written", "practical", "oral"]
                        ),
                        CurriculumTopic(
                            code="M1-2-2",
                            name="Addition up to 20",
                            chapter="Addition",
                            learning_objectives=[
                                "Add numbers with sum up to 20",
                                "Use objects to solve addition problems",
                                "Create addition stories",
                                "Check addition answers"
                            ],
                            key_concepts=["Addition facts", "Story problems", "Verification", "Mental math"],
                            prerequisites=["Addition up to 10"],
                            difficulty_level="beginner",
                            estimated_hours=12,
                            assessment_type=["written", "practical", "storytelling"]
                        )
                    ],
                    learning_outcomes=["Perform addition operations confidently up to 20"],
                    skills_developed=["Mathematical reasoning", "Problem solving", "Mental calculation"]
                ),
                CurriculumChapter(
                    chapter_number=3,
                    chapter_name="Subtraction",
                    topics=[
                        CurriculumTopic(
                            code="M1-3-1",
                            name="Subtraction up to 10",
                            chapter="Subtraction",
                            learning_objectives=[
                                "Understand subtraction as taking away",
                                "Subtract numbers within 10",
                                "Use subtraction symbol (-)",
                                "Relate subtraction to addition"
                            ],
                            key_concepts=["Subtraction", "Take away", "Minus", "Difference", "Inverse operation"],
                            prerequisites=["Addition up to 10"],
                            difficulty_level="beginner",
                            estimated_hours=10,
                            assessment_type=["written", "practical", "oral"]
                        ),
                        CurriculumTopic(
                            code="M1-3-2",
                            name="Subtraction up to 20",
                            chapter="Subtraction",
                            learning_objectives=[
                                "Subtract numbers within 20",
                                "Solve subtraction word problems",
                                "Check subtraction using addition",
                                "Find missing numbers in subtraction"
                            ],
                            key_concepts=["Subtraction facts", "Word problems", "Checking", "Missing numbers"],
                            prerequisites=["Subtraction up to 10", "Addition up to 20"],
                            difficulty_level="beginner",
                            estimated_hours=12,
                            assessment_type=["written", "problem-solving"]
                        )
                    ],
                    learning_outcomes=["Master subtraction operations within 20"],
                    skills_developed=["Logical reasoning", "Problem solving", "Verification skills"]
                ),
                CurriculumChapter(
                    chapter_number=4,
                    chapter_name="Shapes and Patterns",
                    topics=[
                        CurriculumTopic(
                            code="M1-4-1",
                            name="Basic Shapes",
                            chapter="Shapes and Patterns",
                            learning_objectives=[
                                "Identify basic 2D shapes (circle, square, triangle, rectangle)",
                                "Recognize shapes in environment",
                                "Draw basic shapes",
                                "Sort objects by shape"
                            ],
                            key_concepts=["Circle", "Square", "Triangle", "Rectangle", "2D shapes", "Classification"],
                            prerequisites=["Basic observation skills"],
                            difficulty_level="beginner",
                            estimated_hours=8,
                            assessment_type=["practical", "drawing", "identification"]
                        ),
                        CurriculumTopic(
                            code="M1-4-2",
                            name="Patterns",
                            chapter="Shapes and Patterns",
                            learning_objectives=[
                                "Identify simple patterns with objects and numbers",
                                "Continue given patterns",
                                "Create own patterns",
                                "Recognize patterns in daily life"
                            ],
                            key_concepts=["Pattern", "Sequence", "Repetition", "Continuation", "Creation"],
                            prerequisites=["Number sequence", "Shape recognition"],
                            difficulty_level="beginner",
                            estimated_hours=8,
                            assessment_type=["practical", "creative", "identification"]
                        )
                    ],
                    learning_outcomes=["Recognize and work with basic shapes and patterns"],
                    skills_developed=["Visual perception", "Pattern recognition", "Spatial awareness"]
                ),
                CurriculumChapter(
                    chapter_number=5,
                    chapter_name="Time and Money",
                    topics=[
                        CurriculumTopic(
                            code="M1-5-1",
                            name="Time Concepts",
                            chapter="Time and Money",
                            learning_objectives=[
                                "Understand day and night",
                                "Learn days of the week",
                                "Identify morning, afternoon, evening",
                                "Read time on the hour"
                            ],
                            key_concepts=["Day", "Night", "Week", "Morning", "Afternoon", "Evening", "Clock", "Hour"],
                            prerequisites=["Number recognition 1-12"],
                            difficulty_level="beginner",
                            estimated_hours=10,
                            assessment_type=["oral", "practical", "identification"]
                        ),
                        CurriculumTopic(
                            code="M1-5-2",
                            name="Money Recognition",
                            chapter="Time and Money",
                            learning_objectives=[
                                "Identify Indian coins (1, 2, 5, 10 rupees)",
                                "Recognize currency notes",
                                "Understand value of money",
                                "Simple buying and selling concepts"
                            ],
                            key_concepts=["Coins", "Notes", "Rupees", "Value", "Buying", "Selling"],
                            prerequisites=["Number recognition 1-10"],
                            difficulty_level="beginner",
                            estimated_hours=8,
                            assessment_type=["practical", "identification", "role-play"]
                        )
                    ],
                    learning_outcomes=["Basic understanding of time and money concepts"],
                    skills_developed=["Time awareness", "Money sense", "Practical application"]
                )
            ],
            yearly_learning_outcomes=[
                "Count, read, write and compare numbers up to 20",
                "Perform addition and subtraction within 20",
                "Recognize basic shapes and simple patterns",
                "Understand basic concepts of time and money"
            ],
            assessment_pattern={
                "formative": "60%",
                "summative": "40%",
                "practical": "40%",
                "oral": "30%"
            }
        )

    def _get_math_grade_2(self) -> SubjectCurriculum:
        """Enhanced Mathematics curriculum for Grade 2 - Complete Coverage"""
        return SubjectCurriculum(
            subject=Subject.MATHEMATICS,
            grade=2,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="Numbers up to 100",
                    topics=[
                        CurriculumTopic(
                            code="M2-1-1",
                            name="Numbers up to 50",
                            chapter="Numbers up to 100",
                            learning_objectives=[
                                "Count numbers up to 50",
                                "Read and write numbers up to 50",
                                "Understand number sequence",
                                "Skip counting by 2s, 5s, 10s"
                            ],
                            key_concepts=["Counting", "Number names", "Skip counting", "Number line"],
                            prerequisites=["Numbers up to 20"],
                            difficulty_level="beginner",
                            estimated_hours=10,
                            assessment_type=["written", "oral", "practical"]
                        ),
                        CurriculumTopic(
                            code="M2-1-2",
                            name="Place Value - Tens and Ones",
                            chapter="Numbers up to 100",
                            learning_objectives=[
                                "Understand concept of tens and ones",
                                "Represent 2-digit numbers using place value",
                                "Expand numbers into tens and ones",
                                "Compare 2-digit numbers"
                            ],
                            key_concepts=["Place value", "Tens", "Ones", "Expanded form", "Standard form"],
                            prerequisites=["Numbers up to 50"],
                            difficulty_level="intermediate",
                            estimated_hours=12,
                            assessment_type=["written", "practical", "manipulation"]
                        ),
                        CurriculumTopic(
                            code="M2-1-3",
                            name="Numbers up to 100",
                            chapter="Numbers up to 100",
                            learning_objectives=[
                                "Count, read and write numbers up to 100",
                                "Order numbers up to 100",
                                "Find patterns in number charts",
                                "Use number line effectively"
                            ],
                            key_concepts=["Hundred", "Number chart", "Ordering", "Number patterns"],
                            prerequisites=["Place value understanding"],
                            difficulty_level="intermediate",
                            estimated_hours=10,
                            assessment_type=["written", "pattern-recognition"]
                        )
                    ],
                    learning_outcomes=["Master 2-digit number system with place value understanding"],
                    skills_developed=["Number sense", "Place value concepts", "Logical thinking"]
                ),
                CurriculumChapter(
                    chapter_number=2,
                    chapter_name="Addition and Subtraction",
                    topics=[
                        CurriculumTopic(
                            code="M2-2-1",
                            name="Addition without Regrouping",
                            chapter="Addition and Subtraction",
                            learning_objectives=[
                                "Add 2-digit numbers without regrouping",
                                "Use column addition method",
                                "Solve addition word problems",
                                "Estimate sums"
                            ],
                            key_concepts=["Column addition", "No regrouping", "Word problems", "Estimation"],
                            prerequisites=["Place value", "Addition facts"],
                            difficulty_level="intermediate",
                            estimated_hours=12,
                            assessment_type=["written", "problem-solving"]
                        ),
                        CurriculumTopic(
                            code="M2-2-2",
                            name="Addition with Regrouping",
                            chapter="Addition and Subtraction",
                            learning_objectives=[
                                "Add 2-digit numbers with regrouping",
                                "Understand carrying in addition",
                                "Apply regrouping in word problems",
                                "Check addition answers"
                            ],
                            key_concepts=["Regrouping", "Carrying", "Column addition", "Verification"],
                            prerequisites=["Addition without regrouping"],
                            difficulty_level="intermediate",
                            estimated_hours=14,
                            assessment_type=["written", "step-by-step", "problem-solving"]
                        ),
                        CurriculumTopic(
                            code="M2-2-3",
                            name="Subtraction without Regrouping",
                            chapter="Addition and Subtraction",
                            learning_objectives=[
                                "Subtract 2-digit numbers without regrouping",
                                "Use column subtraction method",
                                "Solve subtraction word problems",
                                "Relate addition and subtraction"
                            ],
                            key_concepts=["Column subtraction", "No regrouping", "Inverse operations"],
                            prerequisites=["Place value", "Subtraction facts"],
                            difficulty_level="intermediate",
                            estimated_hours=12,
                            assessment_type=["written", "problem-solving"]
                        ),
                        CurriculumTopic(
                            code="M2-2-4",
                            name="Subtraction with Regrouping",
                            chapter="Addition and Subtraction",
                            learning_objectives=[
                                "Subtract 2-digit numbers with regrouping",
                                "Understand borrowing in subtraction",
                                "Apply regrouping in word problems",
                                "Check subtraction answers"
                            ],
                            key_concepts=["Regrouping", "Borrowing", "Column subtraction", "Verification"],
                            prerequisites=["Subtraction without regrouping"],
                            difficulty_level="advanced",
                            estimated_hours=14,
                            assessment_type=["written", "step-by-step", "problem-solving"]
                        )
                    ],
                    learning_outcomes=["Master addition and subtraction of 2-digit numbers"],
                    skills_developed=["Computational skills", "Problem solving", "Mathematical reasoning"]
                ),
                CurriculumChapter(
                    chapter_number=3,
                    chapter_name="Introduction to Multiplication",
                    topics=[
                        CurriculumTopic(
                            code="M2-3-1",
                            name="Multiplication as Repeated Addition",
                            chapter="Introduction to Multiplication",
                            learning_objectives=[
                                "Understand multiplication as repeated addition",
                                "Use arrays to show multiplication",
                                "Write multiplication sentences",
                                "Solve simple multiplication problems"
                            ],
                            key_concepts=["Repeated addition", "Arrays", "Multiplication sign", "Groups"],
                            prerequisites=["Addition skills", "Skip counting"],
                            difficulty_level="intermediate",
                            estimated_hours=10,
                            assessment_type=["practical", "visual", "written"]
                        ),
                        CurriculumTopic(
                            code="M2-3-2",
                            name="Multiplication Tables 2, 5, 10",
                            chapter="Introduction to Multiplication",
                            learning_objectives=[
                                "Learn and recite tables of 2, 5, and 10",
                                "Apply multiplication tables",
                                "Find patterns in multiplication tables",
                                "Use tables to solve problems"
                            ],
                            key_concepts=["Multiplication tables", "Patterns", "Skip counting", "Facts"],
                            prerequisites=["Multiplication concept"],
                            difficulty_level="intermediate",
                            estimated_hours=12,
                            assessment_type=["oral", "written", "pattern-recognition"]
                        )
                    ],
                    learning_outcomes=["Understand multiplication concept and basic tables"],
                    skills_developed=["Pattern recognition", "Memory skills", "Computational fluency"]
                ),
                CurriculumChapter(
                    chapter_number=4,
                    chapter_name="Measurement",
                    topics=[
                        CurriculumTopic(
                            code="M2-4-1",
                            name="Length Measurement",
                            chapter="Measurement",
                            learning_objectives=[
                                "Measure length using non-standard units",
                                "Introduction to standard units (cm, m)",
                                "Compare lengths of objects",
                                "Estimate lengths"
                            ],
                            key_concepts=["Length", "Centimeter", "Meter", "Measurement", "Estimation"],
                            prerequisites=["Number comparison"],
                            difficulty_level="intermediate",
                            estimated_hours=10,
                            assessment_type=["practical", "hands-on", "measurement"]
                        ),
                        CurriculumTopic(
                            code="M2-4-2",
                            name="Weight and Capacity",
                            chapter="Measurement",
                            learning_objectives=[
                                "Compare weights of objects (heavy/light)",
                                "Introduction to kilogram",
                                "Compare capacity (more/less)",
                                "Introduction to litre"
                            ],
                            key_concepts=["Weight", "Heavy", "Light", "Kilogram", "Capacity", "Litre"],
                            prerequisites=["Comparison concepts"],
                            difficulty_level="intermediate",
                            estimated_hours=10,
                            assessment_type=["practical", "hands-on", "comparison"]
                        )
                    ],
                    learning_outcomes=["Basic understanding of measurement concepts"],
                    skills_developed=["Practical measurement", "Estimation", "Comparison skills"]
                ),
                CurriculumChapter(
                    chapter_number=5,
                    chapter_name="Data Handling and Time",
                    topics=[
                        CurriculumTopic(
                            code="M2-5-1",
                            name="Simple Data Collection",
                            chapter="Data Handling and Time",
                            learning_objectives=[
                                "Collect simple data through surveys",
                                "Organize data in tables",
                                "Create simple pictographs",
                                "Interpret pictographs"
                            ],
                            key_concepts=["Data collection", "Tables", "Pictographs", "Interpretation"],
                            prerequisites=["Counting skills", "Basic addition"],
                            difficulty_level="intermediate",
                            estimated_hours=8,
                            assessment_type=["project", "practical", "creation"]
                        ),
                        CurriculumTopic(
                            code="M2-5-2",
                            name="Time - Hours and Half Hours",
                            chapter="Data Handling and Time",
                            learning_objectives=[
                                "Read time to the hour and half hour",
                                "Understand AM and PM",
                                "Sequence daily activities by time",
                                "Solve simple time problems"
                            ],
                            key_concepts=["Clock", "Hour", "Half hour", "AM", "PM", "Time sequence"],
                            prerequisites=["Numbers 1-12", "Basic time concepts"],
                            difficulty_level="intermediate",
                            estimated_hours=10,
                            assessment_type=["practical", "clock-reading", "problem-solving"]
                        )
                    ],
                    learning_outcomes=["Handle simple data and understand time concepts"],
                    skills_developed=["Data organization", "Time management", "Analytical thinking"]
                )
            ],
            yearly_learning_outcomes=[
                "Master 2-digit numbers with place value understanding",
                "Perform addition and subtraction with regrouping",
                "Understand basic multiplication concepts",
                "Apply measurement and time concepts in daily life"
            ],
            assessment_pattern={
                "formative": "50%",
                "summative": "50%",
                "practical": "40%",
                "problem-solving": "30%"
            }
        )

    def _get_math_grade_3(self) -> SubjectCurriculum:
        """Mathematics curriculum for Grade 3"""
        return SubjectCurriculum(
            subject=Subject.MATHEMATICS,
            grade=3,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="Numbers up to 999",
                    topics=[
                        CurriculumTopic(
                            code="M3-1-1",
                            name="Place Value in 3-digit Numbers",
                            chapter="Numbers up to 999",
                            learning_objectives=[
                                "Understand hundreds, tens, ones",
                                "Read and write 3-digit numbers",
                                "Compare 3-digit numbers"
                            ],
                            key_concepts=["Hundreds", "Place value", "Comparison", "Number names"],
                            prerequisites=["2-digit numbers", "Place value basics"],
                            difficulty_level="intermediate",
                            estimated_hours=15,
                            assessment_type=["written", "practical", "project"]
                        )
                    ],
                    learning_outcomes=["Master 3-digit number system"],
                    skills_developed=["Abstract thinking", "Pattern recognition"]
                )
            ],
            yearly_learning_outcomes=["Number system mastery", "Basic geometry", "Data handling"],
            assessment_pattern={
                "formative": "50%",
                "summative": "50%",
                "practical": "20%"
            }
        )

    def _get_math_grade_4(self) -> SubjectCurriculum:
        """Mathematics curriculum for Grade 4"""
        return SubjectCurriculum(
            subject=Subject.MATHEMATICS,
            grade=4,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="Large Numbers",
                    topics=[
                        CurriculumTopic(
                            code="M4-1-1",
                            name="Numbers up to 10,000",
                            chapter="Large Numbers",
                            learning_objectives=[
                                "Read and write 4-digit numbers",
                                "Understand place value in large numbers",
                                "Compare and order large numbers"
                            ],
                            key_concepts=["Thousands", "Place value", "Number comparison", "Roman numerals"],
                            prerequisites=["3-digit numbers", "Place value concept"],
                            difficulty_level="intermediate",
                            estimated_hours=18,
                            assessment_type=["written", "oral", "project"]
                        ),
                        CurriculumTopic(
                            code="M4-1-2",
                            name="Roman Numerals",
                            chapter="Large Numbers",
                            learning_objectives=[
                                "Read and write Roman numerals up to 100",
                                "Convert between Roman and Arabic numerals",
                                "Understand Roman numeral system"
                            ],
                            key_concepts=["Roman system", "I, V, X, L, C", "Conversion"],
                            prerequisites=["Numbers up to 100"],
                            difficulty_level="intermediate",
                            estimated_hours=12,
                            assessment_type=["written", "practical"]
                        )
                    ],
                    learning_outcomes=["Handle large numbers confidently"],
                    skills_developed=["Analytical thinking", "Number sense"]
                ),
                CurriculumChapter(
                    chapter_number=2,
                    chapter_name="Addition and Subtraction",
                    topics=[
                        CurriculumTopic(
                            code="M4-2-1",
                            name="Addition of Large Numbers",
                            chapter="Addition and Subtraction",
                            learning_objectives=[
                                "Add 4-digit numbers with and without regrouping",
                                "Estimate sums",
                                "Solve word problems involving addition"
                            ],
                            key_concepts=["Addition", "Regrouping", "Estimation", "Word problems"],
                            prerequisites=["Addition basics", "Place value"],
                            difficulty_level="intermediate",
                            estimated_hours=16,
                            assessment_type=["written", "problem-solving"]
                        ),
                        CurriculumTopic(
                            code="M4-2-2",
                            name="Subtraction of Large Numbers",
                            chapter="Addition and Subtraction",
                            learning_objectives=[
                                "Subtract 4-digit numbers with and without borrowing",
                                "Estimate differences",
                                "Solve word problems involving subtraction"
                            ],
                            key_concepts=["Subtraction", "Borrowing", "Estimation", "Word problems"],
                            prerequisites=["Subtraction basics", "Place value"],
                            difficulty_level="intermediate",
                            estimated_hours=16,
                            assessment_type=["written", "problem-solving"]
                        )
                    ],
                    learning_outcomes=["Master addition and subtraction of large numbers"],
                    skills_developed=["Problem solving", "Mathematical reasoning"]
                ),
                CurriculumChapter(
                    chapter_number=3,
                    chapter_name="Multiplication",
                    topics=[
                        CurriculumTopic(
                            code="M4-3-1",
                            name="Multiplication Tables",
                            chapter="Multiplication",
                            learning_objectives=[
                                "Memorize multiplication tables 1-12",
                                "Apply tables in problem solving",
                                "Identify patterns in multiplication"
                            ],
                            key_concepts=["Multiplication tables", "Patterns", "Mental math"],
                            prerequisites=["Basic multiplication concept"],
                            difficulty_level="intermediate",
                            estimated_hours=20,
                            assessment_type=["oral", "written", "speed tests"]
                        ),
                        CurriculumTopic(
                            code="M4-3-2",
                            name="Multiplication of 2-digit and 3-digit Numbers",
                            chapter="Multiplication",
                            learning_objectives=[
                                "Multiply 2-digit by 1-digit numbers",
                                "Multiply 3-digit by 1-digit numbers",
                                "Solve multiplication word problems"
                            ],
                            key_concepts=["Long multiplication", "Regrouping", "Word problems"],
                            prerequisites=["Multiplication tables", "Place value"],
                            difficulty_level="intermediate",
                            estimated_hours=18,
                            assessment_type=["written", "problem-solving"]
                        )
                    ],
                    learning_outcomes=["Master multiplication operations"],
                    skills_developed=["Computational fluency", "Pattern recognition"]
                ),
                CurriculumChapter(
                    chapter_number=4,
                    chapter_name="Division",
                    topics=[
                        CurriculumTopic(
                            code="M4-4-1",
                            name="Division Basics",
                            chapter="Division",
                            learning_objectives=[
                                "Understand division as repeated subtraction",
                                "Divide using multiplication tables",
                                "Find quotient and remainder"
                            ],
                            key_concepts=["Division", "Quotient", "Remainder", "Division facts"],
                            prerequisites=["Multiplication tables", "Subtraction"],
                            difficulty_level="intermediate",
                            estimated_hours=16,
                            assessment_type=["written", "practical"]
                        ),
                        CurriculumTopic(
                            code="M4-4-2",
                            name="Long Division",
                            chapter="Division",
                            learning_objectives=[
                                "Divide 2-digit by 1-digit numbers",
                                "Divide 3-digit by 1-digit numbers",
                                "Solve division word problems"
                            ],
                            key_concepts=["Long division", "Algorithm", "Word problems"],
                            prerequisites=["Division basics", "Multiplication"],
                            difficulty_level="advanced",
                            estimated_hours=18,
                            assessment_type=["written", "problem-solving"]
                        )
                    ],
                    learning_outcomes=["Master division operations"],
                    skills_developed=["Logical thinking", "Problem solving"]
                ),
                CurriculumChapter(
                    chapter_number=5,
                    chapter_name="Fractions",
                    topics=[
                        CurriculumTopic(
                            code="M4-5-1",
                            name="Introduction to Fractions",
                            chapter="Fractions",
                            learning_objectives=[
                                "Understand fractions as parts of whole",
                                "Identify numerator and denominator",
                                "Compare unit fractions"
                            ],
                            key_concepts=["Fractions", "Numerator", "Denominator", "Unit fractions"],
                            prerequisites=["Number sense", "Division concept"],
                            difficulty_level="intermediate",
                            estimated_hours=15,
                            assessment_type=["written", "practical", "visual"]
                        ),
                        CurriculumTopic(
                            code="M4-5-2",
                            name="Equivalent Fractions",
                            chapter="Fractions",
                            learning_objectives=[
                                "Identify equivalent fractions",
                                "Create equivalent fractions",
                                "Compare and order fractions"
                            ],
                            key_concepts=["Equivalent fractions", "Comparison", "Ordering"],
                            prerequisites=["Basic fractions", "Multiplication"],
                            difficulty_level="intermediate",
                            estimated_hours=14,
                            assessment_type=["written", "practical"]
                        )
                    ],
                    learning_outcomes=["Understand fraction concepts"],
                    skills_developed=["Fractional thinking", "Comparison skills"]
                ),
                CurriculumChapter(
                    chapter_number=6,
                    chapter_name="Decimals",
                    topics=[
                        CurriculumTopic(
                            code="M4-6-1",
                            name="Introduction to Decimals",
                            chapter="Decimals",
                            learning_objectives=[
                                "Understand decimal notation",
                                "Read and write decimals to one place",
                                "Relate decimals to fractions"
                            ],
                            key_concepts=["Decimals", "Decimal point", "Tenths", "Place value"],
                            prerequisites=["Fractions", "Place value"],
                            difficulty_level="intermediate",
                            estimated_hours=12,
                            assessment_type=["written", "practical"]
                        )
                    ],
                    learning_outcomes=["Understand decimal notation"],
                    skills_developed=["Decimal number sense"]
                ),
                CurriculumChapter(
                    chapter_number=7,
                    chapter_name="Measurement",
                    topics=[
                        CurriculumTopic(
                            code="M4-7-1",
                            name="Length and Distance",
                            chapter="Measurement",
                            learning_objectives=[
                                "Measure length using standard units",
                                "Convert between units (mm, cm, m, km)",
                                "Solve measurement problems"
                            ],
                            key_concepts=["Length", "Units", "Conversion", "Estimation"],
                            prerequisites=["Number operations", "Basic measurement"],
                            difficulty_level="intermediate",
                            estimated_hours=14,
                            assessment_type=["practical", "written"]
                        ),
                        CurriculumTopic(
                            code="M4-7-2",
                            name="Weight and Capacity",
                            chapter="Measurement",
                            learning_objectives=[
                                "Measure weight using standard units",
                                "Measure capacity using standard units",
                                "Convert between units"
                            ],
                            key_concepts=["Weight", "Capacity", "Units", "Grams", "Kilograms", "Litres"],
                            prerequisites=["Basic measurement", "Number operations"],
                            difficulty_level="intermediate",
                            estimated_hours=14,
                            assessment_type=["practical", "written"]
                        )
                    ],
                    learning_outcomes=["Master measurement concepts"],
                    skills_developed=["Practical measurement skills", "Estimation"]
                ),
                CurriculumChapter(
                    chapter_number=8,
                    chapter_name="Geometry",
                    topics=[
                        CurriculumTopic(
                            code="M4-8-1",
                            name="Lines and Angles",
                            chapter="Geometry",
                            learning_objectives=[
                                "Identify different types of lines",
                                "Understand angles and their types",
                                "Measure angles using protractor"
                            ],
                            key_concepts=["Lines", "Angles", "Parallel", "Perpendicular", "Acute", "Obtuse"],
                            prerequisites=["Basic shapes", "Observation skills"],
                            difficulty_level="intermediate",
                            estimated_hours=16,
                            assessment_type=["practical", "written", "drawing"]
                        ),
                        CurriculumTopic(
                            code="M4-8-2",
                            name="Triangles and Quadrilaterals",
                            chapter="Geometry",
                            learning_objectives=[
                                "Classify triangles by sides and angles",
                                "Identify different quadrilaterals",
                                "Find perimeter of polygons"
                            ],
                            key_concepts=["Triangles", "Quadrilaterals", "Perimeter", "Properties"],
                            prerequisites=["Basic shapes", "Measurement"],
                            difficulty_level="intermediate",
                            estimated_hours=16,
                            assessment_type=["written", "practical", "drawing"]
                        )
                    ],
                    learning_outcomes=["Understand geometric shapes and properties"],
                    skills_developed=["Spatial reasoning", "Geometric thinking"]
                ),
                CurriculumChapter(
                    chapter_number=9,
                    chapter_name="Data Handling",
                    topics=[
                        CurriculumTopic(
                            code="M4-9-1",
                            name="Collection and Organization of Data",
                            chapter="Data Handling",
                            learning_objectives=[
                                "Collect data systematically",
                                "Organize data in tables",
                                "Create simple bar graphs"
                            ],
                            key_concepts=["Data collection", "Tables", "Bar graphs", "Frequency"],
                            prerequisites=["Number operations", "Basic counting"],
                            difficulty_level="intermediate",
                            estimated_hours=12,
                            assessment_type=["project", "practical", "written"]
                        )
                    ],
                    learning_outcomes=["Handle data systematically"],
                    skills_developed=["Data analysis", "Graphical representation"]
                )
            ],
            yearly_learning_outcomes=["Large number operations", "Fractions and decimals", "Geometry", "Data handling"],
            assessment_pattern={
                "formative": "50%",
                "summative": "50%",
                "practical": "25%"
            }
        )

    def _get_math_grade_5(self) -> SubjectCurriculum:
        """Mathematics curriculum for Grade 5"""
        return SubjectCurriculum(
            subject=Subject.MATHEMATICS,
            grade=5,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="The Fish Tale",
                    topics=[
                        CurriculumTopic(
                            code="M5-1-1",
                            name="Large Numbers and Place Value",
                            chapter="The Fish Tale",
                            learning_objectives=[
                                "Read and write numbers up to 1,00,000",
                                "Use place value to compare numbers",
                                "Form largest and smallest numbers"
                            ],
                            key_concepts=["Lakhs", "Place value", "Number formation", "Comparison"],
                            prerequisites=["4-digit numbers", "Place value understanding"],
                            difficulty_level="intermediate",
                            estimated_hours=20,
                            assessment_type=["written", "practical", "project"]
                        )
                    ],
                    learning_outcomes=["Master large number system"],
                    skills_developed=["Logical reasoning", "Problem solving"]
                ),
                CurriculumChapter(
                    chapter_number=2,
                    chapter_name="Shapes and Angles",
                    topics=[
                        CurriculumTopic(
                            code="M5-2-1",
                            name="Basic Geometry Concepts",
                            chapter="Shapes and Angles",
                            learning_objectives=[
                                "Identify different types of angles",
                                "Recognize geometric shapes",
                                "Understand properties of triangles"
                            ],
                            key_concepts=["Angles", "Triangles", "Quadrilaterals", "Parallel lines"],
                            prerequisites=["Basic shapes", "Line concepts"],
                            difficulty_level="intermediate",
                            estimated_hours=16,
                            assessment_type=["written", "practical", "drawing"]
                        )
                    ],
                    learning_outcomes=["Understand basic geometric concepts"],
                    skills_developed=["Spatial thinking", "Visualization"]
                )
            ],
            yearly_learning_outcomes=["Advanced number operations", "Geometry fundamentals", "Data analysis"],
            assessment_pattern={
                "formative": "50%",
                "summative": "50%",
                "practical": "30%"
            }
        )

    def _get_science_grade_3(self) -> SubjectCurriculum:
        """Science curriculum for Grade 3"""
        return SubjectCurriculum(
            subject=Subject.SCIENCE,
            grade=3,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="Our Body",
                    topics=[
                        CurriculumTopic(
                            code="S3-1-1",
                            name="Body Parts and Functions",
                            chapter="Our Body",
                            learning_objectives=[
                                "Identify external body parts",
                                "Understand basic body functions",
                                "Learn about keeping body healthy"
                            ],
                            key_concepts=["Body parts", "Functions", "Health", "Hygiene"],
                            prerequisites=["Basic body awareness"],
                            difficulty_level="beginner",
                            estimated_hours=12,
                            assessment_type=["oral", "practical", "drawing"]
                        )
                    ],
                    learning_outcomes=["Understand human body basics"],
                    skills_developed=["Observation", "Health awareness"]
                )
            ],
            yearly_learning_outcomes=["Basic science concepts", "Environmental awareness", "Health consciousness"],
            assessment_pattern={
                "formative": "60%",
                "summative": "40%",
                "practical": "40%"
            }
        )

    def _get_science_grade_4(self) -> SubjectCurriculum:
        """Science curriculum for Grade 4"""
        return SubjectCurriculum(
            subject=Subject.SCIENCE,
            grade=4,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="Plants and Animals",
                    topics=[
                        CurriculumTopic(
                            code="S4-1-1",
                            name="Plant Life Cycle",
                            chapter="Plants and Animals",
                            learning_objectives=[
                                "Understand plant growth stages",
                                "Identify parts of a plant",
                                "Learn about plant needs"
                            ],
                            key_concepts=["Life cycle", "Plant parts", "Photosynthesis", "Growth"],
                            prerequisites=["Basic plant knowledge"],
                            difficulty_level="intermediate",
                            estimated_hours=14,
                            assessment_type=["written", "practical", "project"]
                        )
                    ],
                    learning_outcomes=["Understand living organisms"],
                    skills_developed=["Scientific observation", "Environmental awareness"]
                )
            ],
            yearly_learning_outcomes=["Life science concepts", "Environmental science", "Scientific method"],
            assessment_pattern={
                "formative": "60%",
                "summative": "40%",
                "practical": "50%"
            }
        )

    def _get_science_grade_5(self) -> SubjectCurriculum:
        """Science curriculum for Grade 5"""
        return SubjectCurriculum(
            subject=Subject.SCIENCE,
            grade=5,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="Super Senses",
                    topics=[
                        CurriculumTopic(
                            code="S5-1-1",
                            name="Human Senses and Animal Senses",
                            chapter="Super Senses",
                            learning_objectives=[
                                "Understand five human senses",
                                "Compare human and animal senses",
                                "Learn about sense organs"
                            ],
                            key_concepts=["Five senses", "Sense organs", "Animal senses", "Adaptation"],
                            prerequisites=["Basic body parts knowledge"],
                            difficulty_level="intermediate",
                            estimated_hours=16,
                            assessment_type=["written", "practical", "observation"]
                        )
                    ],
                    learning_outcomes=["Understand sensory systems"],
                    skills_developed=["Scientific inquiry", "Comparative analysis"]
                )
            ],
            yearly_learning_outcomes=["Advanced life science", "Physical science basics", "Scientific thinking"],
            assessment_pattern={
                "formative": "60%",
                "summative": "40%",
                "practical": "60%"
            }
        )

    def _get_english_grade_1(self) -> SubjectCurriculum:
        """English curriculum for Grade 1"""
        return SubjectCurriculum(
            subject=Subject.ENGLISH,
            grade=1,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="Letters and Sounds",
                    topics=[
                        CurriculumTopic(
                            code="E1-1-1",
                            name="Alphabet Recognition",
                            chapter="Letters and Sounds",
                            learning_objectives=[
                                "Recognize all 26 letters",
                                "Associate letters with sounds",
                                "Write uppercase and lowercase letters"
                            ],
                            key_concepts=["Alphabet", "Phonics", "Letter formation", "Sounds"],
                            prerequisites=["Basic speaking ability"],
                            difficulty_level="beginner",
                            estimated_hours=25,
                            assessment_type=["oral", "written", "recognition"]
                        )
                    ],
                    learning_outcomes=["Master alphabet basics"],
                    skills_developed=["Reading readiness", "Fine motor skills"]
                )
            ],
            yearly_learning_outcomes=["Basic reading", "Simple writing", "Vocabulary building"],
            assessment_pattern={
                "formative": "70%",
                "summative": "30%",
                "oral": "50%"
            }
        )

    def _get_english_grade_2(self) -> SubjectCurriculum:
        """English curriculum for Grade 2"""
        return SubjectCurriculum(
            subject=Subject.ENGLISH,
            grade=2,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="Reading and Comprehension",
                    topics=[
                        CurriculumTopic(
                            code="E2-1-1",
                            name="Simple Story Reading",
                            chapter="Reading and Comprehension",
                            learning_objectives=[
                                "Read simple sentences fluently",
                                "Understand story elements",
                                "Answer basic comprehension questions"
                            ],
                            key_concepts=["Reading fluency", "Comprehension", "Story elements", "Characters"],
                            prerequisites=["Alphabet knowledge", "Basic phonics"],
                            difficulty_level="beginner",
                            estimated_hours=20,
                            assessment_type=["reading", "oral", "written"]
                        )
                    ],
                    learning_outcomes=["Develop reading skills"],
                    skills_developed=["Reading comprehension", "Vocabulary"]
                )
            ],
            yearly_learning_outcomes=["Fluent reading", "Basic writing", "Story understanding"],
            assessment_pattern={
                "formative": "60%",
                "summative": "40%",
                "oral": "40%"
            }
        )

    def _get_english_grade_3(self) -> SubjectCurriculum:
        """English curriculum for Grade 3 - sample structure"""
        return SubjectCurriculum(
            subject=Subject.ENGLISH,
            grade=3,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="Stories and Poems",
                    topics=[
                        CurriculumTopic(
                            code="E3-1-1",
                            name="Story Comprehension",
                            chapter="Stories and Poems",
                            learning_objectives=[
                                "Read stories with understanding",
                                "Identify story themes",
                                "Express opinions about characters"
                            ],
                            key_concepts=["Theme", "Characters", "Plot", "Setting"],
                            prerequisites=["Basic reading skills"],
                            difficulty_level="intermediate",
                            estimated_hours=18,
                            assessment_type=["reading", "writing", "discussion"]
                        )
                    ],
                    learning_outcomes=["Advanced reading comprehension"],
                    skills_developed=["Critical thinking", "Expression"]
                )
            ],
            yearly_learning_outcomes=["Advanced reading", "Creative writing", "Grammar basics"],
            assessment_pattern={
                "formative": "60%",
                "summative": "40%",
                "project": "20%"
            }
        )

    def _get_english_grade_4(self) -> SubjectCurriculum:
        """English curriculum for Grade 4 - sample structure"""
        return SubjectCurriculum(
            subject=Subject.ENGLISH,
            grade=4,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="Literature and Language",
                    topics=[
                        CurriculumTopic(
                            code="E4-1-1",
                            name="Poetry Appreciation",
                            chapter="Literature and Language",
                            learning_objectives=[
                                "Appreciate poetic language",
                                "Understand rhyme and rhythm",
                                "Memorize and recite poems"
                            ],
                            key_concepts=["Poetry", "Rhyme", "Rhythm", "Imagery"],
                            prerequisites=["Reading fluency"],
                            difficulty_level="intermediate",
                            estimated_hours=16,
                            assessment_type=["recitation", "written", "creative"]
                        )
                    ],
                    learning_outcomes=["Develop literary appreciation"],
                    skills_developed=["Aesthetic sense", "Memory", "Expression"]
                )
            ],
            yearly_learning_outcomes=["Literary appreciation", "Advanced grammar", "Creative expression"],
            assessment_pattern={
                "formative": "50%",
                "summative": "50%",
                "creative": "30%"
            }
        )

    def _get_english_grade_5(self) -> SubjectCurriculum:
        """English curriculum for Grade 5 - sample structure"""
        return SubjectCurriculum(
            subject=Subject.ENGLISH,
            grade=5,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="Advanced Reading",
                    topics=[
                        CurriculumTopic(
                            code="E5-1-1",
                            name="Complex Story Analysis",
                            chapter="Advanced Reading",
                            learning_objectives=[
                                "Analyze story structure",
                                "Understand character development",
                                "Make inferences from text"
                            ],
                            key_concepts=["Analysis", "Inference", "Character development", "Theme"],
                            prerequisites=["Good reading comprehension"],
                            difficulty_level="intermediate",
                            estimated_hours=20,
                            assessment_type=["analytical writing", "discussion", "project"]
                        )
                    ],
                    learning_outcomes=["Master reading analysis"],
                    skills_developed=["Critical thinking", "Analytical skills"]
                )
            ],
            yearly_learning_outcomes=["Advanced literacy", "Research skills", "Presentation skills"],
            assessment_pattern={
                "formative": "50%",
                "summative": "50%",
                "project": "40%"
            }
        )

    def _get_social_studies_grade_3(self) -> SubjectCurriculum:
        """Social Studies curriculum for Grade 3"""
        return SubjectCurriculum(
            subject=Subject.SOCIAL_STUDIES,
            grade=3,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="Our Family and Community",
                    topics=[
                        CurriculumTopic(
                            code="SS3-1-1",
                            name="Family Types and Relationships",
                            chapter="Our Family and Community",
                            learning_objectives=[
                                "Understand different family types",
                                "Learn about family relationships",
                                "Appreciate family values"
                            ],
                            key_concepts=["Family", "Relationships", "Community", "Values"],
                            prerequisites=["Basic social awareness"],
                            difficulty_level="beginner",
                            estimated_hours=12,
                            assessment_type=["oral", "project", "drawing"]
                        )
                    ],
                    learning_outcomes=["Understand social structures"],
                    skills_developed=["Social awareness", "Value appreciation"]
                )
            ],
            yearly_learning_outcomes=["Social awareness", "Community understanding", "Cultural appreciation"],
            assessment_pattern={
                "formative": "70%",
                "summative": "30%",
                "project": "50%"
            }
        )

    def _get_social_studies_grade_4(self) -> SubjectCurriculum:
        """Social Studies curriculum for Grade 4"""
        return SubjectCurriculum(
            subject=Subject.SOCIAL_STUDIES,
            grade=4,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="Our Country India",
                    topics=[
                        CurriculumTopic(
                            code="SS4-1-1",
                            name="Geography of India",
                            chapter="Our Country India",
                            learning_objectives=[
                                "Learn about India's location",
                                "Understand physical features",
                                "Identify major states and capitals"
                            ],
                            key_concepts=["Geography", "States", "Physical features", "Location"],
                            prerequisites=["Basic map reading"],
                            difficulty_level="intermediate",
                            estimated_hours=16,
                            assessment_type=["map work", "written", "project"]
                        )
                    ],
                    learning_outcomes=["Understand national geography"],
                    skills_developed=["Map reading", "Geographical awareness"]
                )
            ],
            yearly_learning_outcomes=["National awareness", "Historical understanding", "Cultural diversity"],
            assessment_pattern={
                "formative": "60%",
                "summative": "40%",
                "project": "40%"
            }
        )

    def _get_social_studies_grade_5(self) -> SubjectCurriculum:
        """Social Studies curriculum for Grade 5"""
        return SubjectCurriculum(
            subject=Subject.SOCIAL_STUDIES,
            grade=5,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="Indian History and Culture",
                    topics=[
                        CurriculumTopic(
                            code="SS5-1-1",
                            name="Ancient Indian Civilizations",
                            chapter="Indian History and Culture",
                            learning_objectives=[
                                "Learn about Harappan civilization",
                                "Understand ancient Indian culture",
                                "Appreciate historical heritage"
                            ],
                            key_concepts=["History", "Civilization", "Culture", "Heritage"],
                            prerequisites=["Basic historical awareness"],
                            difficulty_level="intermediate",
                            estimated_hours=18,
                            assessment_type=["written", "project", "timeline"]
                        )
                    ],
                    learning_outcomes=["Understand historical development"],
                    skills_developed=["Historical thinking", "Cultural appreciation"]
                )
            ],
            yearly_learning_outcomes=["Historical awareness", "Cultural understanding", "Research skills"],
            assessment_pattern={
                "formative": "50%",
                "summative": "50%",
                "project": "60%"
            }
        )

    async def search_topics(self, query: str, subject: Optional[str] = None, grade: Optional[int] = None) -> List[Dict]:
        """Search for topics across curriculum"""
        results = []
        
        try:
            # Determine search scope
            subjects_to_search = [Subject(subject)] if subject else list(Subject)
            
            for subj in subjects_to_search:
                subject_data = self._curriculum_data.get(subj, {})
                
                grades_to_search = [grade] if grade else subject_data.keys()
                
                for gr in grades_to_search:
                    curriculum = subject_data.get(gr)
                    if not curriculum:
                        continue
                        
                    for chapter in curriculum.chapters:
                        for topic in chapter.topics:
                            if query.lower() in topic.name.lower() or query.lower() in ' '.join(topic.key_concepts).lower():
                                results.append({
                                    "subject": subj.value,
                                    "grade": gr,
                                    "chapter": chapter.chapter_name,
                                    "topic": topic.name,
                                    "code": topic.code,
                                    "difficulty": topic.difficulty_level,
                                    "concepts": topic.key_concepts
                                })
            
            return results[:10]  # Limit results
            
        except Exception as e:
            self.logger.error(f"Error searching topics: {e}")
            return []

    def _get_science_grade_1(self) -> SubjectCurriculum:
        """Enhanced Science curriculum for Grade 1 - Complete Coverage"""
        return SubjectCurriculum(
            subject=Subject.SCIENCE,
            grade=1,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="Living and Non-Living",
                    topics=[
                        CurriculumTopic(
                            code="S1-1-1",
                            name="Living Things Around Us",
                            chapter="Living and Non-Living",
                            learning_objectives=[
                                "Identify living things in environment",
                                "Understand basic characteristics of living things",
                                "Distinguish between living and non-living things",
                                "Observe growth and movement in living things"
                            ],
                            key_concepts=["Living", "Non-living", "Growth", "Movement", "Breathing", "Eating"],
                            prerequisites=["Basic observation skills"],
                            difficulty_level="beginner",
                            estimated_hours=12,
                            assessment_type=["oral", "practical", "drawing", "identification"]
                        ),
                        CurriculumTopic(
                            code="S1-1-2",
                            name="Non-Living Things Around Us",
                            chapter="Living and Non-Living",
                            learning_objectives=[
                                "Identify non-living things in environment",
                                "Understand properties of non-living things",
                                "Compare living and non-living things",
                                "Classify objects as living or non-living"
                            ],
                            key_concepts=["Non-living", "Properties", "Classification", "Materials"],
                            prerequisites=["Living things identification"],
                            difficulty_level="beginner",
                            estimated_hours=10,
                            assessment_type=["classification", "practical", "oral"]
                        )
                    ],
                    learning_outcomes=["Distinguish between living and non-living things effectively"],
                    skills_developed=["Observation", "Classification", "Comparison"]
                ),
                CurriculumChapter(
                    chapter_number=2,
                    chapter_name="Plants Around Us",
                    topics=[
                        CurriculumTopic(
                            code="S1-2-1",
                            name="Different Types of Plants",
                            chapter="Plants Around Us",
                            learning_objectives=[
                                "Identify different types of plants (trees, shrubs, herbs)",
                                "Observe plant parts (roots, stem, leaves, flowers)",
                                "Recognize plants in the environment",
                                "Understand plants are living things"
                            ],
                            key_concepts=["Trees", "Shrubs", "Herbs", "Plant parts", "Roots", "Stem", "Leaves"],
                            prerequisites=["Living things concept"],
                            difficulty_level="beginner",
                            estimated_hours=12,
                            assessment_type=["identification", "drawing", "practical"]
                        )
                    ],
                    learning_outcomes=["Identify and classify different types of plants"],
                    skills_developed=["Plant identification", "Observation", "Drawing"]
                ),
                CurriculumChapter(
                    chapter_number=3,
                    chapter_name="Animals Around Us",
                    topics=[
                        CurriculumTopic(
                            code="S1-3-1",
                            name="Animals in Our Environment",
                            chapter="Animals Around Us",
                            learning_objectives=[
                                "Identify domestic and wild animals",
                                "Understand animal sounds and movements",
                                "Learn about animal homes",
                                "Recognize baby animals and their parents"
                            ],
                            key_concepts=["Domestic animals", "Wild animals", "Animal sounds", "Animal homes", "Baby animals"],
                            prerequisites=["Living things concept"],
                            difficulty_level="beginner",
                            estimated_hours=12,
                            assessment_type=["identification", "matching", "oral", "drawing"]
                        )
                    ],
                    learning_outcomes=["Recognize and classify animals in environment"],
                    skills_developed=["Animal identification", "Sound recognition", "Observation"]
                ),
                CurriculumChapter(
                    chapter_number=4,
                    chapter_name="My Body",
                    topics=[
                        CurriculumTopic(
                            code="S1-4-1",
                            name="Parts of My Body",
                            chapter="My Body",
                            learning_objectives=[
                                "Identify major body parts",
                                "Understand functions of body parts",
                                "Learn about five sense organs",
                                "Practice good hygiene habits"
                            ],
                            key_concepts=["Body parts", "Head", "Arms", "Legs", "Sense organs", "Eyes", "Ears", "Nose"],
                            prerequisites=["Basic self-awareness"],
                            difficulty_level="beginner",
                            estimated_hours=10,
                            assessment_type=["identification", "practical", "hygiene-demo"]
                        )
                    ],
                    learning_outcomes=["Identify body parts and understand their basic functions"],
                    skills_developed=["Self-awareness", "Health consciousness", "Body coordination"]
                ),
                CurriculumChapter(
                    chapter_number=5,
                    chapter_name="Food and Water",
                    topics=[
                        CurriculumTopic(
                            code="S1-5-1",
                            name="Food We Eat",
                            chapter="Food and Water",
                            learning_objectives=[
                                "Identify different types of food",
                                "Understand healthy and unhealthy food",
                                "Learn about food from plants and animals",
                                "Practice good eating habits"
                            ],
                            key_concepts=["Healthy food", "Unhealthy food", "Plant food", "Animal food", "Nutrition"],
                            prerequisites=["Plants and animals concepts"],
                            difficulty_level="beginner",
                            estimated_hours=10,
                            assessment_type=["identification", "classification", "practical"]
                        ),
                        CurriculumTopic(
                            code="S1-5-2",
                            name="Water and Its Uses",
                            chapter="Food and Water",
                            learning_objectives=[
                                "Understand importance of water",
                                "Learn different uses of water",
                                "Identify sources of water",
                                "Practice water conservation"
                            ],
                            key_concepts=["Water uses", "Water sources", "Clean water", "Water conservation"],
                            prerequisites=["Basic water awareness"],
                            difficulty_level="beginner",
                            estimated_hours=8,
                            assessment_type=["practical", "demonstration", "oral"]
                        )
                    ],
                    learning_outcomes=["Understand importance of food and water for life"],
                    skills_developed=["Health awareness", "Conservation mindset", "Practical life skills"]
                )
            ],
            yearly_learning_outcomes=[
                "Distinguish between living and non-living things",
                "Identify plants and animals in environment",
                "Know basic body parts and their functions", 
                "Understand importance of food and water"
            ],
            assessment_pattern={
                "formative": "60%",
                "summative": "40%",
                "practical": "50%",
                "oral": "30%"
            }
        )

    def _get_science_grade_2(self) -> SubjectCurriculum:
        """Enhanced Science curriculum for Grade 2 - Complete Coverage"""
        return SubjectCurriculum(
            subject=Subject.SCIENCE,
            grade=2,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="Plants and Their Parts",
                    topics=[
                        CurriculumTopic(
                            code="S2-1-1",
                            name="Parts of a Plant",
                            chapter="Plants and Their Parts",
                            learning_objectives=[
                                "Identify and name parts of a plant",
                                "Understand functions of different plant parts",
                                "Observe how plants grow",
                                "Learn about seed germination"
                            ],
                            key_concepts=["Roots", "Stem", "Leaves", "Flowers", "Fruits", "Seeds", "Germination"],
                            prerequisites=["Basic plant identification"],
                            difficulty_level="beginner",
                            estimated_hours=12,
                            assessment_type=["identification", "drawing", "practical", "observation"]
                        ),
                        CurriculumTopic(
                            code="S2-1-2",
                            name="How Plants Grow",
                            chapter="Plants and Their Parts",
                            learning_objectives=[
                                "Understand what plants need to grow",
                                "Observe plant growth from seed",
                                "Learn about plant care",
                                "Understand plants make their own food"
                            ],
                            key_concepts=["Sunlight", "Water", "Air", "Soil", "Growth", "Plant care"],
                            prerequisites=["Plant parts knowledge"],
                            difficulty_level="intermediate",
                            estimated_hours=10,
                            assessment_type=["experiment", "observation", "care-demo"]
                        )
                    ],
                    learning_outcomes=["Understand plant structure and growth requirements"],
                    skills_developed=["Scientific observation", "Plant care", "Understanding life processes"]
                ),
                CurriculumChapter(
                    chapter_number=2,
                    chapter_name="Animals and Their Homes",
                    topics=[
                        CurriculumTopic(
                            code="S2-2-1",
                            name="Animal Families",
                            chapter="Animals and Their Homes",
                            learning_objectives=[
                                "Learn about animal families (male, female, young ones)",
                                "Understand animal behaviors",
                                "Identify animals by their features",
                                "Learn about animal movements"
                            ],
                            key_concepts=["Animal families", "Male", "Female", "Young ones", "Animal behaviors", "Features"],
                            prerequisites=["Basic animal identification"],
                            difficulty_level="beginner",
                            estimated_hours=12,
                            assessment_type=["matching", "identification", "oral"]
                        ),
                        CurriculumTopic(
                            code="S2-2-2",
                            name="Where Animals Live",
                            chapter="Animals and Their Homes",
                            learning_objectives=[
                                "Identify different animal homes",
                                "Understand why animals need homes",
                                "Learn about land and water animals",
                                "Match animals with their homes"
                            ],
                            key_concepts=["Animal homes", "Shelter", "Habitat", "Land animals", "Water animals"],
                            prerequisites=["Animal identification"],
                            difficulty_level="intermediate",
                            estimated_hours=10,
                            assessment_type=["matching", "classification", "practical"]
                        )
                    ],
                    learning_outcomes=["Understand animal families and their living needs"],
                    skills_developed=["Animal behavior understanding", "Habitat awareness", "Classification"]
                ),
                CurriculumChapter(
                    chapter_number=3,
                    chapter_name="Food and Health",
                    topics=[
                        CurriculumTopic(
                            code="S2-3-1",
                            name="Healthy Food Habits",
                            chapter="Food and Health",
                            learning_objectives=[
                                "Learn about balanced diet",
                                "Identify energy-giving and body-building foods",
                                "Understand importance of fruits and vegetables",
                                "Practice healthy eating habits"
                            ],
                            key_concepts=["Balanced diet", "Energy foods", "Body-building foods", "Vitamins", "Healthy habits"],
                            prerequisites=["Basic food knowledge"],
                            difficulty_level="intermediate",
                            estimated_hours=10,
                            assessment_type=["classification", "practical", "habit-tracking"]
                        ),
                        CurriculumTopic(
                            code="S2-3-2",
                            name="Keeping Our Body Clean",
                            chapter="Food and Health",
                            learning_objectives=[
                                "Learn personal hygiene practices",
                                "Understand importance of cleanliness",
                                "Practice daily hygiene routines",
                                "Learn about dental care"
                            ],
                            key_concepts=["Personal hygiene", "Cleanliness", "Bathing", "Dental care", "Hand washing"],
                            prerequisites=["Body parts knowledge"],
                            difficulty_level="beginner",
                            estimated_hours=8,
                            assessment_type=["demonstration", "practical", "routine-practice"]
                        )
                    ],
                    learning_outcomes=["Develop healthy food and hygiene habits"],
                    skills_developed=["Health consciousness", "Self-care", "Healthy lifestyle"]
                ),
                CurriculumChapter(
                    chapter_number=4,
                    chapter_name="Materials Around Us",
                    topics=[
                        CurriculumTopic(
                            code="S2-4-1",
                            name="Different Materials",
                            chapter="Materials Around Us",
                            learning_objectives=[
                                "Identify different materials (wood, metal, plastic, cloth)",
                                "Understand properties of materials",
                                "Learn about uses of different materials",
                                "Classify objects by material type"
                            ],
                            key_concepts=["Wood", "Metal", "Plastic", "Cloth", "Glass", "Material properties"],
                            prerequisites=["Object identification"],
                            difficulty_level="intermediate",
                            estimated_hours=12,
                            assessment_type=["classification", "identification", "property-testing"]
                        )
                    ],
                    learning_outcomes=["Identify and classify materials by properties"],
                    skills_developed=["Material identification", "Property observation", "Classification"]
                ),
                CurriculumChapter(
                    chapter_number=5,
                    chapter_name="Weather and Safety",
                    topics=[
                        CurriculumTopic(
                            code="S2-5-1",
                            name="Weather Changes",
                            chapter="Weather and Safety",
                            learning_objectives=[
                                "Observe different weather conditions",
                                "Understand sunny, rainy, windy weather",
                                "Learn appropriate clothing for weather",
                                "Understand seasons"
                            ],
                            key_concepts=["Weather", "Sunny", "Rainy", "Windy", "Cloudy", "Seasons", "Clothing"],
                            prerequisites=["Basic observation skills"],
                            difficulty_level="beginner",
                            estimated_hours=10,
                            assessment_type=["observation", "matching", "practical"]
                        ),
                        CurriculumTopic(
                            code="S2-5-2",
                            name="Staying Safe",
                            chapter="Weather and Safety",
                            learning_objectives=[
                                "Learn basic safety rules",
                                "Understand traffic safety",
                                "Know emergency contact numbers",
                                "Practice safety at home and school"
                            ],
                            key_concepts=["Safety rules", "Traffic safety", "Emergency", "Home safety", "School safety"],
                            prerequisites=["Basic awareness"],
                            difficulty_level="intermediate",
                            estimated_hours=10,
                            assessment_type=["role-play", "demonstration", "rule-practice"]
                        )
                    ],
                    learning_outcomes=["Understand weather patterns and safety practices"],
                    skills_developed=["Weather awareness", "Safety consciousness", "Emergency preparedness"]
                )
            ],
            yearly_learning_outcomes=[
                "Understand plant structure and growth needs",
                "Learn about animal families and their homes", 
                "Develop healthy food and hygiene habits",
                "Identify materials and their properties",
                "Understand weather changes and safety practices"
            ],
            assessment_pattern={
                "formative": "55%",
                "summative": "45%",
                "practical": "45%", 
                "observation": "25%"
            }
        )

    def _get_social_studies_grade_1(self) -> SubjectCurriculum:
        """Social Studies curriculum for Grade 1"""
        return SubjectCurriculum(
            subject=Subject.SOCIAL_STUDIES,
            grade=1,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="My Family",
                    topics=[
                        CurriculumTopic(
                            code="SS1-1-1",
                            name="Family Members and Relationships",
                            chapter="My Family",
                            learning_objectives=[
                                "Identify family members",
                                "Understand family relationships",
                                "Learn about family love and care"
                            ],
                            key_concepts=["Family", "Relationships", "Love", "Care"],
                            prerequisites=["Basic social awareness"],
                            difficulty_level="beginner",
                            estimated_hours=8,
                            assessment_type=["oral", "drawing", "storytelling"]
                        )
                    ],
                    learning_outcomes=["Understanding family structure"],
                    skills_developed=["Social awareness", "Expression"]
                )
            ],
            yearly_learning_outcomes=["Basic social concepts"],
            assessment_pattern={"formative": "80%", "summative": "20%", "oral": "60%"}
        )

    def _get_social_studies_grade_2(self) -> SubjectCurriculum:
        """Social Studies curriculum for Grade 2"""
        return SubjectCurriculum(
            subject=Subject.SOCIAL_STUDIES,
            grade=2,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="My Community",
                    topics=[
                        CurriculumTopic(
                            code="SS2-1-1",
                            name="People in Our Community",
                            chapter="My Community",
                            learning_objectives=[
                                "Identify community helpers",
                                "Understand their roles",
                                "Appreciate community services"
                            ],
                            key_concepts=["Community", "Helpers", "Services", "Cooperation"],
                            prerequisites=["Family awareness"],
                            difficulty_level="beginner",
                            estimated_hours=10,
                            assessment_type=["oral", "project", "role-play"]
                        )
                    ],
                    learning_outcomes=["Community awareness"],
                    skills_developed=["Social understanding", "Appreciation"]
                )
            ],
            yearly_learning_outcomes=["Community life understanding"],
            assessment_pattern={"formative": "70%", "summative": "30%", "project": "40%"}
        )