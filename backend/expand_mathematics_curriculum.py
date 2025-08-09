#!/usr/bin/env python3
"""
Expand Mathematics Curriculum for Grades 1-5
Creates comprehensive CBSE-aligned mathematics curriculum with all topics
"""

import sys
sys.path.append('.')

from core.curriculum import Subject, CurriculumTopic, CurriculumChapter, SubjectCurriculum
from dataclasses import dataclass, replace

class MathematicsExpansion:
    def __init__(self):
        self.subject = Subject.MATHEMATICS
        
    def get_expanded_math_grade_1(self) -> SubjectCurriculum:
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
    
    def get_expanded_math_grade_2(self) -> SubjectCurriculum:
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

    def get_expanded_math_grade_3(self) -> SubjectCurriculum:
        """Enhanced Mathematics curriculum for Grade 3 - Complete Coverage"""
        return SubjectCurriculum(
            subject=Subject.MATHEMATICS,
            grade=3,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="Numbers up to 1000",
                    topics=[
                        CurriculumTopic(
                            code="M3-1-1",
                            name="Place Value - Hundreds, Tens, Ones",
                            chapter="Numbers up to 1000",
                            learning_objectives=[
                                "Understand 3-digit place value system",
                                "Represent numbers in expanded form",
                                "Compare and order 3-digit numbers",
                                "Round numbers to nearest 10 and 100"
                            ],
                            key_concepts=["Place value", "Hundreds", "Expanded form", "Standard form", "Rounding"],
                            prerequisites=["2-digit place value"],
                            difficulty_level="intermediate",
                            estimated_hours=14,
                            assessment_type=["written", "practical", "manipulation"]
                        ),
                        CurriculumTopic(
                            code="M3-1-2",
                            name="Number Patterns and Skip Counting",
                            chapter="Numbers up to 1000",
                            learning_objectives=[
                                "Skip count by 2s, 3s, 5s, 10s up to 1000",
                                "Identify and extend number patterns",
                                "Create number patterns",
                                "Find missing numbers in patterns"
                            ],
                            key_concepts=["Skip counting", "Number patterns", "Sequences", "Pattern rules"],
                            prerequisites=["Numbers up to 100"],
                            difficulty_level="intermediate",
                            estimated_hours=10,
                            assessment_type=["pattern-recognition", "written"]
                        )
                    ],
                    learning_outcomes=["Master 3-digit number system with advanced place value concepts"],
                    skills_developed=["Number sense", "Pattern recognition", "Mathematical reasoning"]
                ),
                CurriculumChapter(
                    chapter_number=2,
                    chapter_name="Addition and Subtraction",
                    topics=[
                        CurriculumTopic(
                            code="M3-2-1",
                            name="3-digit Addition",
                            chapter="Addition and Subtraction",
                            learning_objectives=[
                                "Add 3-digit numbers with and without regrouping",
                                "Solve multi-step addition problems",
                                "Estimate and verify addition results",
                                "Apply addition in real-world contexts"
                            ],
                            key_concepts=["3-digit addition", "Multiple regrouping", "Estimation", "Word problems"],
                            prerequisites=["2-digit addition with regrouping"],
                            difficulty_level="intermediate",
                            estimated_hours=15,
                            assessment_type=["written", "problem-solving", "estimation"]
                        ),
                        CurriculumTopic(
                            code="M3-2-2",
                            name="3-digit Subtraction",
                            chapter="Addition and Subtraction",
                            learning_objectives=[
                                "Subtract 3-digit numbers with regrouping",
                                "Solve multi-step subtraction problems",
                                "Check subtraction using addition",
                                "Apply subtraction in practical situations"
                            ],
                            key_concepts=["3-digit subtraction", "Multiple borrowing", "Verification", "Applications"],
                            prerequisites=["2-digit subtraction with regrouping"],
                            difficulty_level="intermediate",
                            estimated_hours=15,
                            assessment_type=["written", "problem-solving", "verification"]
                        )
                    ],
                    learning_outcomes=["Master 3-digit arithmetic operations with confidence"],
                    skills_developed=["Computational fluency", "Problem solving", "Estimation skills"]
                ),
                CurriculumChapter(
                    chapter_number=3,
                    chapter_name="Multiplication",
                    topics=[
                        CurriculumTopic(
                            code="M3-3-1",
                            name="Multiplication Tables and Facts",
                            chapter="Multiplication",
                            learning_objectives=[
                                "Master multiplication tables 1-12",
                                "Understand multiplication properties",
                                "Use multiplication facts for mental math",
                                "Apply multiplication in problem solving"
                            ],
                            key_concepts=["Multiplication tables", "Commutative property", "Mental math", "Fact families"],
                            prerequisites=["Multiplication concept", "Basic tables 2, 5, 10"],
                            difficulty_level="intermediate",
                            estimated_hours=20,
                            assessment_type=["oral", "written", "speed-tests"]
                        ),
                        CurriculumTopic(
                            code="M3-3-2",
                            name="Multi-digit Multiplication",
                            chapter="Multiplication",
                            learning_objectives=[
                                "Multiply 2-digit by 1-digit numbers",
                                "Use partial products method",
                                "Solve multiplication word problems",
                                "Estimate products"
                            ],
                            key_concepts=["Multi-digit multiplication", "Partial products", "Regrouping", "Estimation"],
                            prerequisites=["Multiplication facts"],
                            difficulty_level="advanced",
                            estimated_hours=18,
                            assessment_type=["written", "problem-solving", "step-by-step"]
                        )
                    ],
                    learning_outcomes=["Develop multiplication fluency and problem-solving skills"],
                    skills_developed=["Computational skills", "Memory", "Strategic thinking"]
                ),
                CurriculumChapter(
                    chapter_number=4,
                    chapter_name="Division",
                    topics=[
                        CurriculumTopic(
                            code="M3-4-1",
                            name="Introduction to Division",
                            chapter="Division",
                            learning_objectives=[
                                "Understand division as sharing and grouping",
                                "Relate division to multiplication",
                                "Perform simple division with no remainders",
                                "Use division symbol and vocabulary"
                            ],
                            key_concepts=["Division", "Sharing", "Grouping", "Inverse operation", "Quotient"],
                            prerequisites=["Multiplication facts"],
                            difficulty_level="intermediate",
                            estimated_hours=12,
                            assessment_type=["practical", "written", "concept-mapping"]
                        ),
                        CurriculumTopic(
                            code="M3-4-2",
                            name="Division with Remainders",
                            chapter="Division",
                            learning_objectives=[
                                "Divide numbers with remainders",
                                "Interpret remainders in context",
                                "Check division using multiplication",
                                "Solve division word problems"
                            ],
                            key_concepts=["Remainders", "Division algorithm", "Checking", "Contextual interpretation"],
                            prerequisites=["Basic division concepts"],
                            difficulty_level="advanced",
                            estimated_hours=14,
                            assessment_type=["written", "problem-solving", "interpretation"]
                        )
                    ],
                    learning_outcomes=["Understand and apply division concepts effectively"],
                    skills_developed=["Logical reasoning", "Problem solving", "Number relationships"]
                ),
                CurriculumChapter(
                    chapter_number=5,
                    chapter_name="Fractions and Geometry",
                    topics=[
                        CurriculumTopic(
                            code="M3-5-1",
                            name="Introduction to Fractions",
                            chapter="Fractions and Geometry",
                            learning_objectives=[
                                "Understand fractions as parts of a whole",
                                "Identify and write simple fractions",
                                "Compare unit fractions",
                                "Recognize fractions in daily life"
                            ],
                            key_concepts=["Fractions", "Numerator", "Denominator", "Parts of whole", "Unit fractions"],
                            prerequisites=["Division concepts"],
                            difficulty_level="intermediate",
                            estimated_hours=12,
                            assessment_type=["visual", "practical", "identification"]
                        ),
                        CurriculumTopic(
                            code="M3-5-2",
                            name="2D and 3D Shapes",
                            chapter="Fractions and Geometry",
                            learning_objectives=[
                                "Classify 2D and 3D shapes",
                                "Identify properties of shapes",
                                "Find perimeter of simple shapes",
                                "Recognize shapes in environment"
                            ],
                            key_concepts=["2D shapes", "3D shapes", "Properties", "Perimeter", "Classification"],
                            prerequisites=["Basic shape recognition"],
                            difficulty_level="intermediate",
                            estimated_hours=10,
                            assessment_type=["identification", "measurement", "classification"]
                        )
                    ],
                    learning_outcomes=["Basic understanding of fractions and geometric concepts"],
                    skills_developed=["Spatial reasoning", "Visual perception", "Measurement skills"]
                )
            ],
            yearly_learning_outcomes=[
                "Master 3-digit number system and operations",
                "Develop multiplication and division fluency",
                "Understand basic fraction and geometry concepts",
                "Apply mathematical skills to solve real-world problems"
            ],
            assessment_pattern={
                "formative": "50%",
                "summative": "50%",
                "practical": "40%",
                "problem-solving": "35%"
            }
        )

    def get_expanded_math_grade_4(self) -> SubjectCurriculum:
        """Enhanced Mathematics curriculum for Grade 4 - Complete Coverage"""
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
                                "Read, write and represent numbers up to 10,000",
                                "Understand 4-digit place value system",
                                "Compare and order large numbers",
                                "Round numbers to nearest 10, 100, 1000"
                            ],
                            key_concepts=["4-digit numbers", "Place value", "Comparison", "Rounding", "Number names"],
                            prerequisites=["3-digit place value"],
                            difficulty_level="intermediate",
                            estimated_hours=12,
                            assessment_type=["written", "practical", "comparison"]
                        ),
                        CurriculumTopic(
                            code="M4-1-2",
                            name="Number Patterns and Sequences",
                            chapter="Large Numbers",
                            learning_objectives=[
                                "Identify arithmetic and geometric patterns",
                                "Extend and create complex patterns",
                                "Find rules for number sequences",
                                "Apply patterns to solve problems"
                            ],
                            key_concepts=["Arithmetic sequences", "Geometric patterns", "Pattern rules", "Problem solving"],
                            prerequisites=["Basic number patterns"],
                            difficulty_level="intermediate",
                            estimated_hours=10,
                            assessment_type=["pattern-recognition", "rule-finding", "creative"]
                        )
                    ],
                    learning_outcomes=["Master large number concepts and pattern recognition"],
                    skills_developed=["Number sense", "Pattern recognition", "Logical thinking"]
                ),
                CurriculumChapter(
                    chapter_number=2,
                    chapter_name="Four Operations",
                    topics=[
                        CurriculumTopic(
                            code="M4-2-1",
                            name="Advanced Addition and Subtraction",
                            chapter="Four Operations",
                            learning_objectives=[
                                "Add and subtract 4-digit numbers",
                                "Solve multi-step word problems",
                                "Use estimation to check reasonableness",
                                "Apply operations in real contexts"
                            ],
                            key_concepts=["4-digit operations", "Multi-step problems", "Estimation", "Real-world applications"],
                            prerequisites=["3-digit arithmetic"],
                            difficulty_level="intermediate",
                            estimated_hours=15,
                            assessment_type=["written", "problem-solving", "estimation"]
                        ),
                        CurriculumTopic(
                            code="M4-2-2",
                            name="Advanced Multiplication",
                            chapter="Four Operations",
                            learning_objectives=[
                                "Multiply multi-digit numbers",
                                "Use different multiplication strategies",
                                "Solve complex word problems",
                                "Understand factors and multiples"
                            ],
                            key_concepts=["Multi-digit multiplication", "Strategies", "Factors", "Multiples", "Prime numbers"],
                            prerequisites=["Basic multiplication facts"],
                            difficulty_level="advanced",
                            estimated_hours=18,
                            assessment_type=["written", "strategic", "problem-solving"]
                        ),
                        CurriculumTopic(
                            code="M4-2-3",
                            name="Advanced Division",
                            chapter="Four Operations",
                            learning_objectives=[
                                "Divide larger numbers",
                                "Use long division method",
                                "Interpret remainders appropriately",
                                "Solve division word problems"
                            ],
                            key_concepts=["Long division", "Divisibility", "Remainder interpretation", "Problem solving"],
                            prerequisites=["Basic division with remainders"],
                            difficulty_level="advanced",
                            estimated_hours=16,
                            assessment_type=["written", "procedural", "problem-solving"]
                        )
                    ],
                    learning_outcomes=["Master all four arithmetic operations with large numbers"],
                    skills_developed=["Computational fluency", "Strategic thinking", "Problem solving"]
                ),
                CurriculumChapter(
                    chapter_number=3,
                    chapter_name="Fractions and Decimals",
                    topics=[
                        CurriculumTopic(
                            code="M4-3-1",
                            name="Fraction Operations",
                            chapter="Fractions and Decimals",
                            learning_objectives=[
                                "Add and subtract like fractions",
                                "Compare fractions with different denominators",
                                "Convert between mixed numbers and improper fractions",
                                "Solve fraction word problems"
                            ],
                            key_concepts=["Like fractions", "Mixed numbers", "Improper fractions", "Comparison"],
                            prerequisites=["Basic fraction understanding"],
                            difficulty_level="intermediate",
                            estimated_hours=14,
                            assessment_type=["written", "problem-solving", "conversion"]
                        ),
                        CurriculumTopic(
                            code="M4-3-2",
                            name="Introduction to Decimals",
                            chapter="Fractions and Decimals",
                            learning_objectives=[
                                "Understand decimal place value",
                                "Read and write decimal numbers",
                                "Compare and order decimals",
                                "Relate decimals to fractions"
                            ],
                            key_concepts=["Decimal place value", "Tenths", "Hundredths", "Decimal comparison"],
                            prerequisites=["Place value understanding", "Fractions"],
                            difficulty_level="intermediate",
                            estimated_hours=12,
                            assessment_type=["written", "comparison", "conversion"]
                        )
                    ],
                    learning_outcomes=["Develop understanding of fractions and decimal number system"],
                    skills_developed=["Number relationships", "Precision", "Comparative reasoning"]
                ),
                CurriculumChapter(
                    chapter_number=4,
                    chapter_name="Measurement and Geometry",
                    topics=[
                        CurriculumTopic(
                            code="M4-4-1",
                            name="Units of Measurement",
                            chapter="Measurement and Geometry",
                            learning_objectives=[
                                "Use standard units for length, weight, capacity",
                                "Convert between related units",
                                "Solve measurement word problems",
                                "Estimate and measure accurately"
                            ],
                            key_concepts=["Standard units", "Conversion", "Estimation", "Precision", "Measurement tools"],
                            prerequisites=["Basic measurement concepts"],
                            difficulty_level="intermediate",
                            estimated_hours=12,
                            assessment_type=["practical", "problem-solving", "estimation"]
                        ),
                        CurriculumTopic(
                            code="M4-4-2",
                            name="Area and Perimeter",
                            chapter="Measurement and Geometry",
                            learning_objectives=[
                                "Find perimeter of polygons",
                                "Calculate area of rectangles and squares",
                                "Distinguish between area and perimeter",
                                "Solve real-world area and perimeter problems"
                            ],
                            key_concepts=["Area", "Perimeter", "Square units", "Rectangles", "Problem solving"],
                            prerequisites=["Basic geometry", "Multiplication"],
                            difficulty_level="advanced",
                            estimated_hours=14,
                            assessment_type=["calculation", "problem-solving", "application"]
                        )
                    ],
                    learning_outcomes=["Apply measurement concepts and calculate area/perimeter"],
                    skills_developed=["Measurement skills", "Spatial reasoning", "Real-world applications"]
                ),
                CurriculumChapter(
                    chapter_number=5,
                    chapter_name="Data Handling and Time",
                    topics=[
                        CurriculumTopic(
                            code="M4-5-1",
                            name="Data Collection and Representation",
                            chapter="Data Handling and Time",
                            learning_objectives=[
                                "Collect and organize data systematically",
                                "Create bar graphs and pictographs",
                                "Interpret data from charts and graphs",
                                "Draw conclusions from data"
                            ],
                            key_concepts=["Data collection", "Bar graphs", "Pictographs", "Interpretation", "Analysis"],
                            prerequisites=["Basic counting", "Simple data concepts"],
                            difficulty_level="intermediate",
                            estimated_hours=12,
                            assessment_type=["project", "interpretation", "creation"]
                        ),
                        CurriculumTopic(
                            code="M4-5-2",
                            name="Time and Calendar",
                            chapter="Data Handling and Time",
                            learning_objectives=[
                                "Read time to the minute",
                                "Calculate elapsed time",
                                "Use calendar for planning",
                                "Solve time-related problems"
                            ],
                            key_concepts=["Time reading", "Elapsed time", "Calendar", "24-hour time", "Problem solving"],
                            prerequisites=["Basic time concepts"],
                            difficulty_level="intermediate",
                            estimated_hours=10,
                            assessment_type=["practical", "calculation", "problem-solving"]
                        )
                    ],
                    learning_outcomes=["Handle data effectively and solve time-related problems"],
                    skills_developed=["Data analysis", "Time management", "Logical thinking"]
                )
            ],
            yearly_learning_outcomes=[
                "Master large number operations and place value concepts",
                "Perform all four operations with multi-digit numbers",
                "Understand fractions, decimals, and their relationships", 
                "Apply measurement, geometry, and data handling skills"
            ],
            assessment_pattern={
                "formative": "45%",
                "summative": "55%",
                "practical": "40%",
                "problem-solving": "40%"
            }
        )

    def get_expanded_math_grade_5(self) -> SubjectCurriculum:
        """Enhanced Mathematics curriculum for Grade 5 - Complete Coverage"""
        return SubjectCurriculum(
            subject=Subject.MATHEMATICS,
            grade=5,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="Large Numbers and Place Value",
                    topics=[
                        CurriculumTopic(
                            code="M5-1-1",
                            name="Numbers up to 1,00,000",
                            chapter="Large Numbers and Place Value",
                            learning_objectives=[
                                "Read, write numbers up to one lakh",
                                "Understand Indian and International place value systems",
                                "Compare and order very large numbers",
                                "Use place value for mental calculations"
                            ],
                            key_concepts=["Lakh", "Indian system", "International system", "Place value", "Mental math"],
                            prerequisites=["4-digit place value"],
                            difficulty_level="intermediate",
                            estimated_hours=12,
                            assessment_type=["written", "comparison", "mental-math"]
                        ),
                        CurriculumTopic(
                            code="M5-1-2",
                            name="Estimation and Approximation",
                            chapter="Large Numbers and Place Value",
                            learning_objectives=[
                                "Estimate results of calculations",
                                "Round numbers to convenient values",
                                "Use estimation for checking answers",
                                "Apply estimation in real-world contexts"
                            ],
                            key_concepts=["Estimation", "Rounding", "Approximation", "Reasonableness", "Checking"],
                            prerequisites=["Large number operations"],
                            difficulty_level="intermediate",
                            estimated_hours=10,
                            assessment_type=["estimation", "verification", "application"]
                        )
                    ],
                    learning_outcomes=["Master very large numbers and estimation skills"],
                    skills_developed=["Number sense", "Estimation skills", "Mental mathematics"]
                ),
                CurriculumChapter(
                    chapter_number=2,
                    chapter_name="Decimals",
                    topics=[
                        CurriculumTopic(
                            code="M5-2-1",
                            name="Decimal Operations",
                            chapter="Decimals",
                            learning_objectives=[
                                "Add and subtract decimal numbers",
                                "Multiply decimals by whole numbers",
                                "Divide decimals by whole numbers",
                                "Solve decimal word problems"
                            ],
                            key_concepts=["Decimal operations", "Decimal point alignment", "Decimal multiplication", "Division"],
                            prerequisites=["Basic decimals", "Place value"],
                            difficulty_level="advanced",
                            estimated_hours=16,
                            assessment_type=["written", "problem-solving", "procedural"]
                        ),
                        CurriculumTopic(
                            code="M5-2-2",
                            name="Decimals and Money",
                            chapter="Decimals",
                            learning_objectives=[
                                "Work with money in decimal form",
                                "Calculate bills and change",
                                "Solve money problems involving decimals",
                                "Understand profit and loss basics"
                            ],
                            key_concepts=["Money", "Bills", "Change", "Profit", "Loss", "Real applications"],
                            prerequisites=["Decimal operations"],
                            difficulty_level="intermediate",
                            estimated_hours=12,
                            assessment_type=["practical", "real-world", "calculation"]
                        )
                    ],
                    learning_outcomes=["Master decimal operations and money applications"],
                    skills_developed=["Precision", "Real-world applications", "Financial literacy"]
                ),
                CurriculumChapter(
                    chapter_number=3,
                    chapter_name="Fractions",
                    topics=[
                        CurriculumTopic(
                            code="M5-3-1",
                            name="Fraction Operations",
                            chapter="Fractions",
                            learning_objectives=[
                                "Add and subtract unlike fractions",
                                "Multiply fractions by whole numbers",
                                "Convert between fractions and decimals",
                                "Solve complex fraction problems"
                            ],
                            key_concepts=["Unlike fractions", "Common denominators", "Fraction multiplication", "Conversion"],
                            prerequisites=["Basic fractions", "Decimals"],
                            difficulty_level="advanced",
                            estimated_hours=18,
                            assessment_type=["written", "problem-solving", "conversion"]
                        ),
                        CurriculumTopic(
                            code="M5-3-2",
                            name="Percentage Introduction",
                            chapter="Fractions",
                            learning_objectives=[
                                "Understand percentage as parts per hundred",
                                "Convert between fractions, decimals, and percentages",
                                "Calculate simple percentages",
                                "Apply percentages in real situations"
                            ],
                            key_concepts=["Percentage", "Parts per hundred", "Conversion", "Calculation", "Applications"],
                            prerequisites=["Fractions", "Decimals"],
                            difficulty_level="advanced",
                            estimated_hours=14,
                            assessment_type=["conversion", "calculation", "application"]
                        )
                    ],
                    learning_outcomes=["Advanced fraction operations and percentage concepts"],
                    skills_developed=["Mathematical relationships", "Proportional reasoning", "Problem solving"]
                ),
                CurriculumChapter(
                    chapter_number=4,
                    chapter_name="Geometry and Measurement",
                    topics=[
                        CurriculumTopic(
                            code="M5-4-1",
                            name="Advanced Geometry",
                            chapter="Geometry and Measurement",
                            learning_objectives=[
                                "Classify triangles by sides and angles",
                                "Identify properties of quadrilaterals",
                                "Understand symmetry and patterns",
                                "Draw geometric figures accurately"
                            ],
                            key_concepts=["Triangle classification", "Quadrilaterals", "Symmetry", "Geometric drawing"],
                            prerequisites=["Basic geometry", "Shapes"],
                            difficulty_level="intermediate",
                            estimated_hours=14,
                            assessment_type=["classification", "drawing", "identification"]
                        ),
                        CurriculumTopic(
                            code="M5-4-2",
                            name="Area and Volume",
                            chapter="Geometry and Measurement",
                            learning_objectives=[
                                "Calculate area of triangles and parallelograms",
                                "Find surface area of simple solids",
                                "Calculate volume of cubes and cuboids",
                                "Solve measurement problems"
                            ],
                            key_concepts=["Triangle area", "Parallelogram area", "Surface area", "Volume", "Cubic units"],
                            prerequisites=["Area and perimeter", "3D shapes"],
                            difficulty_level="advanced",
                            estimated_hours=16,
                            assessment_type=["calculation", "formula-application", "problem-solving"]
                        )
                    ],
                    learning_outcomes=["Advanced geometric concepts and measurement skills"],
                    skills_developed=["Spatial reasoning", "Formula application", "Measurement precision"]
                ),
                CurriculumChapter(
                    chapter_number=5,
                    chapter_name="Data Handling and Probability",
                    topics=[
                        CurriculumTopic(
                            code="M5-5-1",
                            name="Advanced Data Handling",
                            chapter="Data Handling and Probability",
                            learning_objectives=[
                                "Create and interpret line graphs",
                                "Calculate mean, median, and mode",
                                "Analyze data trends and patterns",
                                "Make predictions based on data"
                            ],
                            key_concepts=["Line graphs", "Mean", "Median", "Mode", "Data analysis", "Trends"],
                            prerequisites=["Basic data handling"],
                            difficulty_level="advanced",
                            estimated_hours=14,
                            assessment_type=["creation", "interpretation", "analysis"]
                        ),
                        CurriculumTopic(
                            code="M5-5-2",
                            name="Introduction to Probability",
                            chapter="Data Handling and Probability",
                            learning_objectives=[
                                "Understand concepts of chance and probability",
                                "Identify certain, impossible, and possible events",
                                "Calculate simple probabilities",
                                "Apply probability to games and real situations"
                            ],
                            key_concepts=["Probability", "Chance", "Certain events", "Impossible events", "Likelihood"],
                            prerequisites=["Fractions", "Data concepts"],
                            difficulty_level="intermediate",
                            estimated_hours=12,
                            assessment_type=["conceptual", "calculation", "application"]
                        )
                    ],
                    learning_outcomes=["Analyze data effectively and understand basic probability"],
                    skills_developed=["Statistical thinking", "Data analysis", "Logical reasoning"]
                )
            ],
            yearly_learning_outcomes=[
                "Master large number systems and decimal operations",
                "Perform advanced fraction operations and understand percentages",
                "Apply geometric concepts and measurement formulas",
                "Analyze data and understand basic probability concepts"
            ],
            assessment_pattern={
                "formative": "40%",
                "summative": "60%",
                "practical": "35%",
                "problem-solving": "45%"
            }
        )

    def generate_curriculum_code(self):
        """Generate Python code for expanded mathematics curriculum"""
        print("EXPANDED MATHEMATICS CURRICULUM - GRADES 1-5")
        print("=" * 60)
        
        print("\n# Grade 1 Mathematics - 11 topics across 5 chapters")
        grade1 = self.get_expanded_math_grade_1()
        total_topics_g1 = sum(len(chapter.topics) for chapter in grade1.chapters)
        print(f"# Total topics: {total_topics_g1}")
        print(f"# Total chapters: {len(grade1.chapters)}")
        
        print("\n# Grade 2 Mathematics - 13 topics across 5 chapters") 
        grade2 = self.get_expanded_math_grade_2()
        total_topics_g2 = sum(len(chapter.topics) for chapter in grade2.chapters)
        print(f"# Total topics: {total_topics_g2}")
        print(f"# Total chapters: {len(grade2.chapters)}")
        
        print("\n# Grade 3 Mathematics - 10 topics across 5 chapters")
        grade3 = self.get_expanded_math_grade_3()
        total_topics_g3 = sum(len(chapter.topics) for chapter in grade3.chapters)
        print(f"# Total topics: {total_topics_g3}")
        print(f"# Total chapters: {len(grade3.chapters)}")
        
        print("\n# Grade 4 Mathematics - 12 topics across 5 chapters")
        grade4 = self.get_expanded_math_grade_4()
        total_topics_g4 = sum(len(chapter.topics) for chapter in grade4.chapters)
        print(f"# Total topics: {total_topics_g4}")
        print(f"# Total chapters: {len(grade4.chapters)}")
        
        print("\n# Grade 5 Mathematics - 10 topics across 5 chapters")
        grade5 = self.get_expanded_math_grade_5()
        total_topics_g5 = sum(len(chapter.topics) for chapter in grade5.chapters)
        print(f"# Total topics: {total_topics_g5}")
        print(f"# Total chapters: {len(grade5.chapters)}")
        
        total_topics_all = total_topics_g1 + total_topics_g2 + total_topics_g3 + total_topics_g4 + total_topics_g5
        
        print(f"\nSTATUS: Mathematics Grades 1-5 COMPLETE EXPANSION")
        print(f"Grade 1: {total_topics_g1} topics (was 3) - {(total_topics_g1-3)/3*100:.0f}% increase")
        print(f"Grade 2: {total_topics_g2} topics (was 1) - {(total_topics_g2-1)/1*100:.0f}% increase")
        print(f"Grade 3: {total_topics_g3} topics (was 1) - {(total_topics_g3-1)/1*100:.0f}% increase")
        print(f"Grade 4: {total_topics_g4} topics (maintained comprehensive coverage)")
        print(f"Grade 5: {total_topics_g5} topics (was 3) - {(total_topics_g5-3)/3*100:.0f}% increase")
        print(f"TOTAL: {total_topics_all} mathematics topics across 25 chapters")
        print(f"Next: Apply to curriculum.py and test content generation")

def main():
    expander = MathematicsExpansion()
    expander.generate_curriculum_code()

if __name__ == "__main__":
    main()