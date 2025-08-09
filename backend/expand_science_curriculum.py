#!/usr/bin/env python3
"""
Expand Science Curriculum for Grades 1-5
Creates comprehensive CBSE-aligned Science curriculum with all topics
"""

import sys
sys.path.append('.')

from core.curriculum import Subject, CurriculumTopic, CurriculumChapter, SubjectCurriculum

class ScienceExpansion:
    def __init__(self):
        self.subject = Subject.SCIENCE
        
    def get_expanded_science_grade_1(self) -> SubjectCurriculum:
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

    def get_expanded_science_grade_2(self) -> SubjectCurriculum:
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

    def get_expanded_science_grade_3(self) -> SubjectCurriculum:
        """Enhanced Science curriculum for Grade 3 - Complete Coverage"""
        return SubjectCurriculum(
            subject=Subject.SCIENCE,
            grade=3,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="Plant Life",
                    topics=[
                        CurriculumTopic(
                            code="S3-1-1",
                            name="Life Cycle of Plants",
                            chapter="Plant Life",
                            learning_objectives=[
                                "Understand plant life cycle from seed to plant",
                                "Observe different stages of plant growth",
                                "Learn about pollination and seed formation",
                                "Understand reproduction in plants"
                            ],
                            key_concepts=["Life cycle", "Germination", "Seedling", "Pollination", "Reproduction"],
                            prerequisites=["Plant parts and growth"],
                            difficulty_level="intermediate",
                            estimated_hours=14,
                            assessment_type=["observation", "experiment", "drawing", "sequencing"]
                        ),
                        CurriculumTopic(
                            code="S3-1-2",
                            name="Plants and Their Environment",
                            chapter="Plant Life",
                            learning_objectives=[
                                "Understand how plants adapt to environment",
                                "Learn about different plant habitats",
                                "Observe how plants respond to light and water",
                                "Understand plant survival strategies"
                            ],
                            key_concepts=["Adaptation", "Habitat", "Plant responses", "Survival", "Environment"],
                            prerequisites=["Plant growth knowledge"],
                            difficulty_level="intermediate",
                            estimated_hours=12,
                            assessment_type=["observation", "experiment", "comparison"]
                        )
                    ],
                    learning_outcomes=["Understand plant life cycles and environmental adaptations"],
                    skills_developed=["Life cycle understanding", "Environmental awareness", "Scientific observation"]
                ),
                CurriculumChapter(
                    chapter_number=2,
                    chapter_name="Animal Life",
                    topics=[
                        CurriculumTopic(
                            code="S3-2-1",
                            name="Life Cycle of Animals",
                            chapter="Animal Life",
                            learning_objectives=[
                                "Understand animal life cycles",
                                "Learn about metamorphosis in insects",
                                "Observe growth in animals",
                                "Compare life cycles of different animals"
                            ],
                            key_concepts=["Animal life cycle", "Metamorphosis", "Larva", "Pupa", "Adult"],
                            prerequisites=["Animal families knowledge"],
                            difficulty_level="intermediate",
                            estimated_hours=14,
                            assessment_type=["observation", "comparison", "sequencing"]
                        ),
                        CurriculumTopic(
                            code="S3-2-2",
                            name="Animal Movement and Feeding",
                            chapter="Animal Life",
                            learning_objectives=[
                                "Learn about different ways animals move",
                                "Understand animal feeding habits",
                                "Classify animals as herbivores, carnivores, omnivores",
                                "Relate animal body parts to their functions"
                            ],
                            key_concepts=["Animal movement", "Feeding habits", "Herbivores", "Carnivores", "Omnivores"],
                            prerequisites=["Animal behavior knowledge"],
                            difficulty_level="intermediate",
                            estimated_hours=12,
                            assessment_type=["classification", "observation", "matching"]
                        )
                    ],
                    learning_outcomes=["Understand animal life processes and behaviors"],
                    skills_developed=["Life process understanding", "Animal behavior analysis", "Classification skills"]
                ),
                CurriculumChapter(
                    chapter_number=3,
                    chapter_name="Human Body and Senses",
                    topics=[
                        CurriculumTopic(
                            code="S3-3-1",
                            name="Our Sense Organs",
                            chapter="Human Body and Senses",
                            learning_objectives=[
                                "Learn detailed functions of five sense organs",
                                "Understand how we see, hear, smell, taste, and touch",
                                "Learn to protect our sense organs",
                                "Understand sensory disabilities and care"
                            ],
                            key_concepts=["Five senses", "Eyes", "Ears", "Nose", "Tongue", "Skin", "Sensory protection"],
                            prerequisites=["Basic body parts knowledge"],
                            difficulty_level="intermediate",
                            estimated_hours=12,
                            assessment_type=["practical", "testing", "demonstration"]
                        ),
                        CurriculumTopic(
                            code="S3-3-2",
                            name="Staying Healthy",
                            chapter="Human Body and Senses",
                            learning_objectives=[
                                "Understand importance of exercise",
                                "Learn about rest and sleep",
                                "Understand disease prevention",
                                "Learn first aid basics"
                            ],
                            key_concepts=["Exercise", "Rest", "Sleep", "Disease prevention", "First aid", "Health"],
                            prerequisites=["Personal hygiene knowledge"],
                            difficulty_level="intermediate",
                            estimated_hours=10,
                            assessment_type=["demonstration", "practical", "health-tracking"]
                        )
                    ],
                    learning_outcomes=["Understand human senses and health maintenance"],
                    skills_developed=["Sensory awareness", "Health consciousness", "Self-care skills"]
                ),
                CurriculumChapter(
                    chapter_number=4,
                    chapter_name="Food and Nutrition",
                    topics=[
                        CurriculumTopic(
                            code="S3-4-1",
                            name="Food Groups and Nutrition",
                            chapter="Food and Nutrition",
                            learning_objectives=[
                                "Learn about different food groups",
                                "Understand balanced nutrition",
                                "Learn about vitamins and minerals",
                                "Plan healthy meals"
                            ],
                            key_concepts=["Food groups", "Carbohydrates", "Proteins", "Fats", "Vitamins", "Minerals"],
                            prerequisites=["Healthy food knowledge"],
                            difficulty_level="intermediate",
                            estimated_hours=12,
                            assessment_type=["classification", "meal-planning", "practical"]
                        )
                    ],
                    learning_outcomes=["Understand nutrition and plan balanced meals"],
                    skills_developed=["Nutritional awareness", "Meal planning", "Health management"]
                ),
                CurriculumChapter(
                    chapter_number=5,
                    chapter_name="Water and Air",
                    topics=[
                        CurriculumTopic(
                            code="S3-5-1",
                            name="Sources and Uses of Water",
                            chapter="Water and Air",
                            learning_objectives=[
                                "Learn about different sources of water",
                                "Understand water purification",
                                "Learn about water conservation",
                                "Understand water cycle basics"
                            ],
                            key_concepts=["Water sources", "Water purification", "Water conservation", "Water cycle"],
                            prerequisites=["Basic water knowledge"],
                            difficulty_level="intermediate",
                            estimated_hours=12,
                            assessment_type=["demonstration", "conservation-project", "experiment"]
                        ),
                        CurriculumTopic(
                            code="S3-5-2",
                            name="Air Around Us",
                            chapter="Water and Air",
                            learning_objectives=[
                                "Understand properties of air",
                                "Learn that air is everywhere",
                                "Understand air pollution and cleanliness",
                                "Learn importance of clean air"
                            ],
                            key_concepts=["Air properties", "Air pollution", "Clean air", "Breathing", "Wind"],
                            prerequisites=["Basic environmental awareness"],
                            difficulty_level="intermediate",
                            estimated_hours=10,
                            assessment_type=["experiment", "demonstration", "observation"]
                        )
                    ],
                    learning_outcomes=["Understand importance of water and air for life"],
                    skills_developed=["Environmental awareness", "Conservation mindset", "Scientific understanding"]
                )
            ],
            yearly_learning_outcomes=[
                "Understand plant and animal life cycles",
                "Learn about human senses and health maintenance",
                "Understand nutrition and balanced diet",
                "Appreciate importance of water and air for life"
            ],
            assessment_pattern={
                "formative": "50%",
                "summative": "50%",
                "practical": "40%",
                "observation": "30%"
            }
        )

    def get_expanded_science_grade_4(self) -> SubjectCurriculum:
        """Enhanced Science curriculum for Grade 4 - Complete Coverage"""
        return SubjectCurriculum(
            subject=Subject.SCIENCE,
            grade=4,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="Plants",
                    topics=[
                        CurriculumTopic(
                            code="S4-1-1",
                            name="Plant Structure and Functions",
                            chapter="Plants",
                            learning_objectives=[
                                "Understand detailed functions of plant parts",
                                "Learn about photosynthesis in simple terms",
                                "Understand transportation in plants",
                                "Learn about plant reproduction methods"
                            ],
                            key_concepts=["Photosynthesis", "Transportation", "Plant reproduction", "Root functions", "Leaf functions"],
                            prerequisites=["Plant life cycle knowledge"],
                            difficulty_level="intermediate",
                            estimated_hours=14,
                            assessment_type=["experiment", "observation", "drawing", "explanation"]
                        ),
                        CurriculumTopic(
                            code="S4-1-2",
                            name="Plant Adaptations",
                            chapter="Plants",
                            learning_objectives=[
                                "Learn how plants adapt to different environments",
                                "Understand desert, water, and mountain plants",
                                "Learn about plant survival strategies",
                                "Understand seasonal changes in plants"
                            ],
                            key_concepts=["Plant adaptations", "Desert plants", "Water plants", "Mountain plants", "Seasonal changes"],
                            prerequisites=["Plant-environment relationship"],
                            difficulty_level="advanced",
                            estimated_hours=12,
                            assessment_type=["comparison", "observation", "case-study"]
                        )
                    ],
                    learning_outcomes=["Understand plant functions and environmental adaptations"],
                    skills_developed=["Scientific thinking", "Adaptation understanding", "Environmental awareness"]
                ),
                CurriculumChapter(
                    chapter_number=2,
                    chapter_name="Animals",
                    topics=[
                        CurriculumTopic(
                            code="S4-2-1",
                            name="Animal Adaptations",
                            chapter="Animals",
                            learning_objectives=[
                                "Learn how animals adapt to their environment",
                                "Understand body parts that help animals survive",
                                "Learn about camouflage and protection",
                                "Understand migration and hibernation"
                            ],
                            key_concepts=["Animal adaptations", "Camouflage", "Protection", "Migration", "Hibernation"],
                            prerequisites=["Animal behavior knowledge"],
                            difficulty_level="intermediate",
                            estimated_hours=14,
                            assessment_type=["observation", "comparison", "case-study"]
                        ),
                        CurriculumTopic(
                            code="S4-2-2",
                            name="Animal Classification",
                            chapter="Animals",
                            learning_objectives=[
                                "Classify animals into different groups",
                                "Learn about vertebrates and invertebrates",
                                "Understand warm-blooded and cold-blooded animals",
                                "Learn about animal characteristics"
                            ],
                            key_concepts=["Animal classification", "Vertebrates", "Invertebrates", "Warm-blooded", "Cold-blooded"],
                            prerequisites=["Animal identification"],
                            difficulty_level="advanced",
                            estimated_hours=12,
                            assessment_type=["classification", "identification", "grouping"]
                        )
                    ],
                    learning_outcomes=["Understand animal adaptations and classification systems"],
                    skills_developed=["Classification skills", "Adaptation analysis", "Scientific categorization"]
                ),
                CurriculumChapter(
                    chapter_number=3,
                    chapter_name="Food",
                    topics=[
                        CurriculumTopic(
                            code="S4-3-1",
                            name="Food Chains and Webs",
                            chapter="Food",
                            learning_objectives=[
                                "Understand the concept of food chains",
                                "Learn about producers and consumers",
                                "Understand food webs in ecosystems",
                                "Learn about decomposers"
                            ],
                            key_concepts=["Food chains", "Food webs", "Producers", "Consumers", "Decomposers", "Ecosystem"],
                            prerequisites=["Animal feeding habits"],
                            difficulty_level="advanced",
                            estimated_hours=14,
                            assessment_type=["diagram-drawing", "chain-construction", "ecosystem-analysis"]
                        ),
                        CurriculumTopic(
                            code="S4-3-2",
                            name="Food Preservation",
                            chapter="Food",
                            learning_objectives=[
                                "Learn different methods of food preservation",
                                "Understand why food spoils",
                                "Learn about traditional and modern preservation",
                                "Understand food safety practices"
                            ],
                            key_concepts=["Food preservation", "Food spoilage", "Traditional methods", "Modern methods", "Food safety"],
                            prerequisites=["Food groups knowledge"],
                            difficulty_level="intermediate",
                            estimated_hours=10,
                            assessment_type=["experiment", "demonstration", "comparison"]
                        )
                    ],
                    learning_outcomes=["Understand ecological food relationships and preservation methods"],
                    skills_developed=["Ecological thinking", "Food science understanding", "Safety awareness"]
                ),
                CurriculumChapter(
                    chapter_number=4,
                    chapter_name="Housing",
                    topics=[
                        CurriculumTopic(
                            code="S4-4-1",
                            name="Types of Houses",
                            chapter="Housing",
                            learning_objectives=[
                                "Learn about different types of houses",
                                "Understand how climate affects house design",
                                "Learn about building materials",
                                "Understand the need for shelter"
                            ],
                            key_concepts=["House types", "Climate effects", "Building materials", "Shelter needs", "Architecture"],
                            prerequisites=["Material properties knowledge"],
                            difficulty_level="intermediate",
                            estimated_hours=12,
                            assessment_type=["identification", "comparison", "design-activity"]
                        )
                    ],
                    learning_outcomes=["Understand housing needs and architectural adaptations"],
                    skills_developed=["Architectural awareness", "Climate understanding", "Design thinking"]
                ),
                CurriculumChapter(
                    chapter_number=5,
                    chapter_name="Water and Travel",
                    topics=[
                        CurriculumTopic(
                            code="S4-5-1",
                            name="Water Cycle and Conservation",
                            chapter="Water and Travel",
                            learning_objectives=[
                                "Understand the complete water cycle",
                                "Learn about evaporation, condensation, precipitation",
                                "Understand groundwater and surface water",
                                "Learn advanced water conservation methods"
                            ],
                            key_concepts=["Water cycle", "Evaporation", "Condensation", "Precipitation", "Groundwater", "Conservation"],
                            prerequisites=["Basic water cycle knowledge"],
                            difficulty_level="advanced",
                            estimated_hours=14,
                            assessment_type=["diagram-drawing", "experiment", "conservation-project"]
                        ),
                        CurriculumTopic(
                            code="S4-5-2",
                            name="Means of Transportation",
                            chapter="Water and Travel",
                            learning_objectives=[
                                "Learn about different modes of transport",
                                "Understand land, water, and air transport",
                                "Learn about evolution of transport",
                                "Understand environmental impact of transport"
                            ],
                            key_concepts=["Transportation modes", "Land transport", "Water transport", "Air transport", "Environmental impact"],
                            prerequisites=["Basic transport awareness"],
                            difficulty_level="intermediate",
                            estimated_hours=12,
                            assessment_type=["classification", "timeline-creation", "environmental-analysis"]
                        )
                    ],
                    learning_outcomes=["Understand water cycle and transportation systems"],
                    skills_developed=["Environmental science", "Transportation awareness", "Conservation thinking"]
                )
            ],
            yearly_learning_outcomes=[
                "Understand plant and animal adaptations to environment",
                "Learn about food chains and ecological relationships",
                "Understand housing needs and building materials",
                "Learn about water cycle and transportation systems"
            ],
            assessment_pattern={
                "formative": "45%",
                "summative": "55%", 
                "practical": "40%",
                "project": "25%"
            }
        )

    def get_expanded_science_grade_5(self) -> SubjectCurriculum:
        """Enhanced Science curriculum for Grade 5 - Complete Coverage"""
        return SubjectCurriculum(
            subject=Subject.SCIENCE,
            grade=5,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="Plant and Animal Life",
                    topics=[
                        CurriculumTopic(
                            code="S5-1-1",
                            name="Plant and Animal Interdependence",
                            chapter="Plant and Animal Life",
                            learning_objectives=[
                                "Understand how plants and animals depend on each other",
                                "Learn about symbiotic relationships",
                                "Understand ecosystem balance",
                                "Learn about biodiversity importance"
                            ],
                            key_concepts=["Interdependence", "Symbiosis", "Ecosystem balance", "Biodiversity", "Mutualism"],
                            prerequisites=["Food chains and animal/plant adaptations"],
                            difficulty_level="advanced",
                            estimated_hours=16,
                            assessment_type=["ecosystem-project", "relationship-mapping", "case-study"]
                        ),
                        CurriculumTopic(
                            code="S5-1-2",
                            name="Life Processes",
                            chapter="Plant and Animal Life",
                            learning_objectives=[
                                "Understand basic life processes in detail",
                                "Learn about respiration in plants and animals",
                                "Understand excretion and waste removal",
                                "Learn about growth and reproduction"
                            ],
                            key_concepts=["Life processes", "Respiration", "Excretion", "Growth", "Reproduction"],
                            prerequisites=["Plant and animal functions"],
                            difficulty_level="advanced",
                            estimated_hours=14,
                            assessment_type=["experiment", "observation", "comparison"]
                        )
                    ],
                    learning_outcomes=["Understand complex relationships and processes in living organisms"],
                    skills_developed=["Systems thinking", "Ecological awareness", "Scientific analysis"]
                ),
                CurriculumChapter(
                    chapter_number=2,
                    chapter_name="Human Body Systems",
                    topics=[
                        CurriculumTopic(
                            code="S5-2-1",
                            name="Skeletal and Muscular Systems",
                            chapter="Human Body Systems",
                            learning_objectives=[
                                "Learn about bones and their functions",
                                "Understand how muscles work",
                                "Learn about joints and movement",
                                "Understand bone and muscle care"
                            ],
                            key_concepts=["Skeletal system", "Muscular system", "Bones", "Muscles", "Joints", "Movement"],
                            prerequisites=["Basic body parts knowledge"],
                            difficulty_level="intermediate",
                            estimated_hours=14,
                            assessment_type=["identification", "movement-demo", "health-practices"]
                        ),
                        CurriculumTopic(
                            code="S5-2-2",
                            name="Digestive and Circulatory Systems",
                            chapter="Human Body Systems",
                            learning_objectives=[
                                "Understand how food is digested",
                                "Learn about the digestive system organs",
                                "Understand blood circulation basics",
                                "Learn about heart and blood vessels"
                            ],
                            key_concepts=["Digestive system", "Circulatory system", "Digestion", "Heart", "Blood circulation"],
                            prerequisites=["Food and nutrition knowledge"],
                            difficulty_level="advanced",
                            estimated_hours=16,
                            assessment_type=["diagram-labeling", "process-explanation", "health-tracking"]
                        )
                    ],
                    learning_outcomes=["Understand major human body systems and their functions"],
                    skills_developed=["Body system understanding", "Health awareness", "Scientific terminology"]
                ),
                CurriculumChapter(
                    chapter_number=3,
                    chapter_name="Food and Health",
                    topics=[
                        CurriculumTopic(
                            code="S5-3-1",
                            name="Balanced Diet and Nutrition",
                            chapter="Food and Health",
                            learning_objectives=[
                                "Understand detailed nutritional requirements",
                                "Learn about malnutrition and obesity",
                                "Plan nutritious meals for different age groups",
                                "Understand food allergies and intolerances"
                            ],
                            key_concepts=["Nutritional requirements", "Malnutrition", "Obesity", "Food allergies", "Meal planning"],
                            prerequisites=["Food groups and nutrition"],
                            difficulty_level="advanced",
                            estimated_hours=14,
                            assessment_type=["meal-planning", "nutritional-analysis", "health-assessment"]
                        )
                    ],
                    learning_outcomes=["Plan balanced diets and understand nutritional health"],
                    skills_developed=["Nutritional planning", "Health management", "Critical thinking"]
                ),
                CurriculumChapter(
                    chapter_number=4,
                    chapter_name="Materials and Their Properties",
                    topics=[
                        CurriculumTopic(
                            code="S5-4-1",
                            name="States of Matter",
                            chapter="Materials and Their Properties",
                            learning_objectives=[
                                "Understand solids, liquids, and gases",
                                "Learn about changes of state",
                                "Understand melting, boiling, freezing",
                                "Learn about expansion and contraction"
                            ],
                            key_concepts=["States of matter", "Solids", "Liquids", "Gases", "Melting", "Boiling", "Expansion"],
                            prerequisites=["Material properties knowledge"],
                            difficulty_level="intermediate",
                            estimated_hours=14,
                            assessment_type=["experiment", "observation", "state-change-demo"]
                        ),
                        CurriculumTopic(
                            code="S5-4-2",
                            name="Solutions and Mixtures",
                            chapter="Materials and Their Properties",
                            learning_objectives=[
                                "Understand solutions and mixtures",
                                "Learn about soluble and insoluble substances",
                                "Learn separation methods",
                                "Understand concentration and dilution"
                            ],
                            key_concepts=["Solutions", "Mixtures", "Soluble", "Insoluble", "Separation methods", "Concentration"],
                            prerequisites=["Material identification"],
                            difficulty_level="advanced",
                            estimated_hours=12,
                            assessment_type=["experiment", "separation-demo", "solution-making"]
                        )
                    ],
                    learning_outcomes=["Understand matter states and material interactions"],
                    skills_developed=["Scientific experimentation", "Observation skills", "Material science understanding"]
                ),
                CurriculumChapter(
                    chapter_number=5,
                    chapter_name="Water, Air and Weather",
                    topics=[
                        CurriculumTopic(
                            code="S5-5-1",
                            name="Air Pressure and Wind",
                            chapter="Water, Air and Weather",
                            learning_objectives=[
                                "Understand air has weight and exerts pressure",
                                "Learn how wind is formed",
                                "Understand weather patterns",
                                "Learn about air pollution effects"
                            ],
                            key_concepts=["Air pressure", "Wind formation", "Weather patterns", "Air pollution", "Atmospheric conditions"],
                            prerequisites=["Air properties knowledge"],
                            difficulty_level="advanced",
                            estimated_hours=14,
                            assessment_type=["experiment", "weather-observation", "pollution-study"]
                        ),
                        CurriculumTopic(
                            code="S5-5-2",
                            name="Natural Disasters and Safety",
                            chapter="Water, Air and Weather",
                            learning_objectives=[
                                "Learn about natural disasters (floods, earthquakes, storms)",
                                "Understand disaster preparedness",
                                "Learn safety measures for different disasters",
                                "Understand early warning systems"
                            ],
                            key_concepts=["Natural disasters", "Floods", "Earthquakes", "Storms", "Disaster preparedness", "Safety measures"],
                            prerequisites=["Weather and safety knowledge"],
                            difficulty_level="intermediate",
                            estimated_hours=12,
                            assessment_type=["safety-planning", "disaster-simulation", "preparedness-checklist"]
                        )
                    ],
                    learning_outcomes=["Understand atmospheric phenomena and natural disaster safety"],
                    skills_developed=["Weather understanding", "Safety preparedness", "Environmental awareness"]
                )
            ],
            yearly_learning_outcomes=[
                "Understand complex plant-animal relationships and life processes",
                "Learn about major human body systems and their functions",
                "Understand advanced nutrition and health management",
                "Learn about matter states and atmospheric phenomena",
                "Develop disaster preparedness and safety awareness"
            ],
            assessment_pattern={
                "formative": "40%",
                "summative": "60%",
                "practical": "35%",
                "project": "30%"
            }
        )

    def generate_curriculum_code(self):
        """Generate Python code for expanded science curriculum"""
        print("EXPANDED SCIENCE CURRICULUM - GRADES 1-5")
        print("=" * 60)
        
        print("\n# Grade 1 Science - 7 topics across 5 chapters")
        grade1 = self.get_expanded_science_grade_1()
        total_topics_g1 = sum(len(chapter.topics) for chapter in grade1.chapters)
        print(f"# Total topics: {total_topics_g1}")
        print(f"# Total chapters: {len(grade1.chapters)}")
        
        print("\n# Grade 2 Science - 9 topics across 5 chapters") 
        grade2 = self.get_expanded_science_grade_2()
        total_topics_g2 = sum(len(chapter.topics) for chapter in grade2.chapters)
        print(f"# Total topics: {total_topics_g2}")
        print(f"# Total chapters: {len(grade2.chapters)}")
        
        print("\n# Grade 3 Science - 9 topics across 5 chapters")
        grade3 = self.get_expanded_science_grade_3()
        total_topics_g3 = sum(len(chapter.topics) for chapter in grade3.chapters)
        print(f"# Total topics: {total_topics_g3}")
        print(f"# Total chapters: {len(grade3.chapters)}")
        
        print("\n# Grade 4 Science - 9 topics across 5 chapters")
        grade4 = self.get_expanded_science_grade_4()
        total_topics_g4 = sum(len(chapter.topics) for chapter in grade4.chapters)
        print(f"# Total topics: {total_topics_g4}")
        print(f"# Total chapters: {len(grade4.chapters)}")
        
        print("\n# Grade 5 Science - 9 topics across 5 chapters")
        grade5 = self.get_expanded_science_grade_5()
        total_topics_g5 = sum(len(chapter.topics) for chapter in grade5.chapters)
        print(f"# Total topics: {total_topics_g5}")
        print(f"# Total chapters: {len(grade5.chapters)}")
        
        total_topics_all = total_topics_g1 + total_topics_g2 + total_topics_g3 + total_topics_g4 + total_topics_g5
        
        print(f"\nSTATUS: Science Grades 1-5 COMPLETE EXPANSION")
        print(f"Grade 1: {total_topics_g1} topics (was 1) - {(total_topics_g1-1)/1*100:.0f}% increase")
        print(f"Grade 2: {total_topics_g2} topics (was 1) - {(total_topics_g2-1)/1*100:.0f}% increase")
        print(f"Grade 3: {total_topics_g3} topics (was 1) - {(total_topics_g3-1)/1*100:.0f}% increase")
        print(f"Grade 4: {total_topics_g4} topics (was 1) - {(total_topics_g4-1)/1*100:.0f}% increase")
        print(f"Grade 5: {total_topics_g5} topics (was 1) - {(total_topics_g5-1)/1*100:.0f}% increase")
        print(f"TOTAL: {total_topics_all} science topics across 25 chapters")
        print(f"Next: Apply to curriculum.py and test content generation")

def main():
    expander = ScienceExpansion()
    expander.generate_curriculum_code()

if __name__ == "__main__":
    main()