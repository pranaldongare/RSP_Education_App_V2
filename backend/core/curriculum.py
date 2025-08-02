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
        """Mathematics curriculum for Grade 1"""
        return SubjectCurriculum(
            subject=Subject.MATHEMATICS,
            grade=1,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="Numbers up to 9",
                    topics=[
                        CurriculumTopic(
                            code="M1-1-1",
                            name="Counting Numbers 1-9",
                            chapter="Numbers up to 9",
                            learning_objectives=[
                                "Recognize and write numbers 1-9",
                                "Count objects up to 9",
                                "Understand number sequence"
                            ],
                            key_concepts=["Counting", "Number recognition", "Number writing"],
                            prerequisites=["Basic object identification"],
                            difficulty_level="beginner",
                            estimated_hours=8,
                            assessment_type=["oral", "written", "practical"]
                        ),
                        CurriculumTopic(
                            code="M1-1-2", 
                            name="Number Comparison",
                            chapter="Numbers up to 9",
                            learning_objectives=[
                                "Compare numbers using more/less",
                                "Arrange numbers in order"
                            ],
                            key_concepts=["Comparison", "Ordering", "Greater than", "Less than"],
                            prerequisites=["Number recognition 1-9"],
                            difficulty_level="beginner",
                            estimated_hours=6,
                            assessment_type=["oral", "written"]
                        )
                    ],
                    learning_outcomes=["Students can count, recognize and write numbers 1-9"],
                    skills_developed=["Number sense", "Observation", "Fine motor skills"]
                ),
                CurriculumChapter(
                    chapter_number=2,
                    chapter_name="Addition",
                    topics=[
                        CurriculumTopic(
                            code="M1-2-1",
                            name="Addition up to 9",
                            chapter="Addition", 
                            learning_objectives=[
                                "Understand concept of addition",
                                "Add numbers with sum up to 9",
                                "Solve simple word problems"
                            ],
                            key_concepts=["Addition", "Sum", "Combining", "Plus sign"],
                            prerequisites=["Counting 1-9", "Number recognition"],
                            difficulty_level="beginner",
                            estimated_hours=10,
                            assessment_type=["written", "practical", "oral"]
                        )
                    ],
                    learning_outcomes=["Students can perform simple addition"],
                    skills_developed=["Mathematical reasoning", "Problem solving"]
                )
            ],
            yearly_learning_outcomes=[
                "Count and recognize numbers up to 99",
                "Perform basic addition and subtraction",
                "Identify basic shapes and patterns",
                "Understand concepts of time and measurement"
            ],
            assessment_pattern={
                "formative": "40%",
                "summative": "60%",
                "practical": "Integrated",
                "portfolio": "Encouraged"
            }
        )

    def _get_math_grade_2(self) -> SubjectCurriculum:
        """Mathematics curriculum for Grade 2"""
        return SubjectCurriculum(
            subject=Subject.MATHEMATICS,
            grade=2,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="Numbers up to 99",
                    topics=[
                        CurriculumTopic(
                            code="M2-1-1",
                            name="Place Value",
                            chapter="Numbers up to 99",
                            learning_objectives=[
                                "Understand tens and ones",
                                "Read and write 2-digit numbers",
                                "Represent numbers using place value"
                            ],
                            key_concepts=["Place value", "Tens", "Ones", "Two-digit numbers"],
                            prerequisites=["Numbers 1-20", "Counting"],
                            difficulty_level="beginner",
                            estimated_hours=12,
                            assessment_type=["written", "practical"]
                        )
                    ],
                    learning_outcomes=["Understand place value concept"],
                    skills_developed=["Logical thinking", "Number sense"]
                )
            ],
            yearly_learning_outcomes=["Work with numbers up to 999", "Basic operations", "Measurement concepts"],
            assessment_pattern={
                "formative": "40%",
                "summative": "60%",
                "practical": "Integrated"
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
        """Science curriculum for Grade 1"""
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
                                "Identify living things",
                                "Understand basic needs of living things",
                                "Distinguish between living and non-living"
                            ],
                            key_concepts=["Living", "Non-living", "Growth", "Movement"],
                            prerequisites=["Basic observation skills"],
                            difficulty_level="beginner",
                            estimated_hours=10,
                            assessment_type=["oral", "practical", "drawing"]
                        )
                    ],
                    learning_outcomes=["Understand basic life concepts"],
                    skills_developed=["Observation", "Classification"]
                )
            ],
            yearly_learning_outcomes=["Basic life science awareness"],
            assessment_pattern={"formative": "70%", "summative": "30%", "practical": "50%"}
        )

    def _get_science_grade_2(self) -> SubjectCurriculum:
        """Science curriculum for Grade 2"""
        return SubjectCurriculum(
            subject=Subject.SCIENCE,
            grade=2,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="Plants Around Us",
                    topics=[
                        CurriculumTopic(
                            code="S2-1-1",
                            name="Different Types of Plants",
                            chapter="Plants Around Us",
                            learning_objectives=[
                                "Identify different plants",
                                "Understand plant parts",
                                "Learn about plant uses"
                            ],
                            key_concepts=["Plants", "Leaves", "Flowers", "Fruits"],
                            prerequisites=["Basic observation"],
                            difficulty_level="beginner",
                            estimated_hours=12,
                            assessment_type=["oral", "practical", "project"]
                        )
                    ],
                    learning_outcomes=["Basic plant knowledge"],
                    skills_developed=["Observation", "Classification"]
                )
            ],
            yearly_learning_outcomes=["Plant life understanding"],
            assessment_pattern={"formative": "60%", "summative": "40%", "practical": "40%"}
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