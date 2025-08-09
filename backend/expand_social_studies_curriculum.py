#!/usr/bin/env python3
"""
Expand Social Studies Curriculum for Grades 1-5
Creates comprehensive CBSE-aligned Social Studies curriculum with all topics
"""

import sys
sys.path.append('.')

from core.curriculum import Subject, CurriculumTopic, CurriculumChapter, SubjectCurriculum

class SocialStudiesExpansion:
    def __init__(self):
        self.subject = Subject.SOCIAL_STUDIES
        
    def get_expanded_social_studies_grade_1(self) -> SubjectCurriculum:
        """Enhanced Social Studies curriculum for Grade 1 - Complete Coverage"""
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
                                "Identify family members and their relationships",
                                "Understand family roles and responsibilities", 
                                "Express love and care for family",
                                "Learn about family traditions"
                            ],
                            key_concepts=["Family", "Relationships", "Roles", "Love", "Care", "Traditions"],
                            prerequisites=["Basic social awareness"],
                            difficulty_level="beginner",
                            estimated_hours=10,
                            assessment_type=["oral", "drawing", "storytelling", "family-tree"]
                        ),
                        CurriculumTopic(
                            code="SS1-1-2",
                            name="Family Celebrations and Festivals",
                            chapter="My Family",
                            learning_objectives=[
                                "Learn about family celebrations and festivals",
                                "Understand the importance of togetherness",
                                "Share experiences of family festivals",
                                "Appreciate cultural diversity in celebrations"
                            ],
                            key_concepts=["Celebrations", "Festivals", "Togetherness", "Cultural diversity", "Traditions"],
                            prerequisites=["Family relationships understanding"],
                            difficulty_level="beginner",
                            estimated_hours=8,
                            assessment_type=["sharing", "drawing", "celebration-description"]
                        )
                    ],
                    learning_outcomes=["Understand family structure and celebrate family bonds"],
                    skills_developed=["Social awareness", "Expression", "Cultural appreciation"]
                ),
                CurriculumChapter(
                    chapter_number=2,
                    chapter_name="My School",
                    topics=[
                        CurriculumTopic(
                            code="SS1-2-1",
                            name="School Community",
                            chapter="My School",
                            learning_objectives=[
                                "Identify different people in school (teachers, friends, staff)",
                                "Understand school rules and their importance",
                                "Learn to cooperate and share with classmates",
                                "Appreciate the role of education"
                            ],
                            key_concepts=["School community", "Teachers", "Friends", "Rules", "Cooperation", "Education"],
                            prerequisites=["Basic social interaction"],
                            difficulty_level="beginner",
                            estimated_hours=12,
                            assessment_type=["identification", "rule-practice", "cooperation-activities"]
                        )
                    ],
                    learning_outcomes=["Understand school environment and social interactions"],
                    skills_developed=["Social skills", "Cooperation", "Rule-following"]
                ),
                CurriculumChapter(
                    chapter_number=3,
                    chapter_name="My Neighborhood",
                    topics=[
                        CurriculumTopic(
                            code="SS1-3-1",
                            name="Places in My Neighborhood",
                            chapter="My Neighborhood",
                            learning_objectives=[
                                "Identify important places in neighborhood (market, hospital, park)",
                                "Understand the purpose of different places",
                                "Learn about community helpers",
                                "Practice giving and following directions"
                            ],
                            key_concepts=["Neighborhood", "Community places", "Community helpers", "Directions", "Safety"],
                            prerequisites=["Basic location awareness"],
                            difficulty_level="beginner", 
                            estimated_hours=12,
                            assessment_type=["place-identification", "helper-matching", "direction-practice"]
                        ),
                        CurriculumTopic(
                            code="SS1-3-2",
                            name="Being a Good Neighbor",
                            chapter="My Neighborhood",
                            learning_objectives=[
                                "Learn about being kind and helpful to neighbors",
                                "Understand community responsibility",
                                "Practice good manners and politeness",
                                "Learn about keeping neighborhood clean"
                            ],
                            key_concepts=["Good neighbor", "Kindness", "Community responsibility", "Manners", "Cleanliness"],
                            prerequisites=["Social interaction skills"],
                            difficulty_level="intermediate",
                            estimated_hours=10,
                            assessment_type=["role-play", "manner-practice", "community-service"]
                        )
                    ],
                    learning_outcomes=["Understand community life and civic responsibility"],
                    skills_developed=["Community awareness", "Civic sense", "Social responsibility"]
                ),
                CurriculumChapter(
                    chapter_number=4,
                    chapter_name="Our Country",
                    topics=[
                        CurriculumTopic(
                            code="SS1-4-1",
                            name="My Country India",
                            chapter="Our Country",
                            learning_objectives=[
                                "Learn basic facts about India",
                                "Recognize Indian flag and its colors",
                                "Understand feeling proud of our country",
                                "Learn about unity in diversity"
                            ],
                            key_concepts=["India", "Indian flag", "Tricolor", "Pride", "Unity in diversity"],
                            prerequisites=["Basic national awareness"],
                            difficulty_level="beginner",
                            estimated_hours=12,
                            assessment_type=["flag-recognition", "patriotic-songs", "country-facts"]
                        )
                    ],
                    learning_outcomes=["Develop basic national identity and patriotism"],
                    skills_developed=["National pride", "Cultural identity", "Patriotism"]
                ),
                CurriculumChapter(
                    chapter_number=5,
                    chapter_name="Festivals and Celebrations",
                    topics=[
                        CurriculumTopic(
                            code="SS1-5-1",
                            name="Festivals of India",
                            chapter="Festivals and Celebrations",
                            learning_objectives=[
                                "Learn about major Indian festivals (Diwali, Holi, Eid, Christmas)",
                                "Understand the joy and significance of festivals",
                                "Appreciate different religious celebrations",
                                "Learn about sharing and caring during festivals"
                            ],
                            key_concepts=["Indian festivals", "Religious diversity", "Celebration", "Sharing", "Joy"],
                            prerequisites=["Cultural awareness"],
                            difficulty_level="intermediate", 
                            estimated_hours=14,
                            assessment_type=["festival-identification", "celebration-activities", "sharing-practices"]
                        )
                    ],
                    learning_outcomes=["Appreciate cultural diversity and festival traditions"],
                    skills_developed=["Cultural appreciation", "Religious tolerance", "Social participation"]
                )
            ],
            yearly_learning_outcomes=[
                "Understand family relationships and responsibilities",
                "Develop school and community awareness",
                "Learn about neighborhood and civic duties",
                "Build national identity and patriotism",
                "Appreciate cultural diversity and festivals"
            ],
            assessment_pattern={
                "formative": "75%",
                "summative": "25%",
                "oral": "50%",
                "practical": "30%",
                "project": "20%"
            }
        )

    def get_expanded_social_studies_grade_2(self) -> SubjectCurriculum:
        """Enhanced Social Studies curriculum for Grade 2 - Complete Coverage"""
        return SubjectCurriculum(
            subject=Subject.SOCIAL_STUDIES,
            grade=2,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="Family and Relationships",
                    topics=[
                        CurriculumTopic(
                            code="SS2-1-1",
                            name="Extended Family and Community",
                            chapter="Family and Relationships",
                            learning_objectives=[
                                "Learn about extended family (grandparents, aunts, uncles)",
                                "Understand different types of families",
                                "Learn about family occupations",
                                "Appreciate family support systems"
                            ],
                            key_concepts=["Extended family", "Family types", "Occupations", "Support systems"],
                            prerequisites=["Basic family understanding"],
                            difficulty_level="intermediate",
                            estimated_hours=12,
                            assessment_type=["family-mapping", "occupation-matching", "support-discussion"]
                        )
                    ],
                    learning_outcomes=["Understand extended family and community connections"],
                    skills_developed=["Family appreciation", "Community understanding", "Social connections"]
                ),
                CurriculumChapter(
                    chapter_number=2,
                    chapter_name="Community Helpers and Services",
                    topics=[
                        CurriculumTopic(
                            code="SS2-2-1",
                            name="People Who Help Us",
                            chapter="Community Helpers and Services",
                            learning_objectives=[
                                "Learn about various community helpers (doctor, teacher, police, firefighter)",
                                "Understand their roles and importance",
                                "Learn how to seek help when needed",
                                "Appreciate service to community"
                            ],
                            key_concepts=["Community helpers", "Service", "Roles", "Importance", "Help-seeking"],
                            prerequisites=["Community awareness"],
                            difficulty_level="intermediate",
                            estimated_hours=14,
                            assessment_type=["helper-identification", "role-play", "service-appreciation"]
                        ),
                        CurriculumTopic(
                            code="SS2-2-2",
                            name="Public Services and Facilities",
                            chapter="Community Helpers and Services",
                            learning_objectives=[
                                "Learn about public services (hospital, post office, library)",
                                "Understand how to use public facilities",
                                "Learn about public transportation",
                                "Appreciate community resources"
                            ],
                            key_concepts=["Public services", "Facilities", "Transportation", "Community resources"],
                            prerequisites=["Helper understanding"],
                            difficulty_level="intermediate",
                            estimated_hours=12,
                            assessment_type=["facility-identification", "usage-practice", "resource-appreciation"]
                        )
                    ],
                    learning_outcomes=["Understand community services and appreciate helpers"],
                    skills_developed=["Service appreciation", "Community engagement", "Resource utilization"]
                ),
                CurriculumChapter(
                    chapter_number=3,
                    chapter_name="Our Local Environment",
                    topics=[
                        CurriculumTopic(
                            code="SS2-3-1",
                            name="Our Town or City",
                            chapter="Our Local Environment", 
                            learning_objectives=[
                                "Learn about local area (town/city/village)",
                                "Identify local landmarks and important places",
                                "Understand urban and rural differences",
                                "Appreciate local heritage and culture"
                            ],
                            key_concepts=["Local area", "Landmarks", "Urban-rural", "Heritage", "Culture"],
                            prerequisites=["Neighborhood knowledge"],
                            difficulty_level="intermediate",
                            estimated_hours=16,
                            assessment_type=["area-mapping", "landmark-identification", "culture-sharing"]
                        ),
                        CurriculumTopic(
                            code="SS2-3-2",
                            name="Caring for Our Environment",
                            chapter="Our Local Environment",
                            learning_objectives=[
                                "Learn about keeping environment clean",
                                "Understand importance of trees and plants",
                                "Practice waste disposal and recycling",
                                "Develop environmental responsibility"
                            ],
                            key_concepts=["Environment care", "Cleanliness", "Trees", "Waste disposal", "Recycling"],
                            prerequisites=["Environmental awareness"],
                            difficulty_level="intermediate",
                            estimated_hours=12,
                            assessment_type=["cleaning-activities", "tree-planting", "recycling-practice"]
                        )
                    ],
                    learning_outcomes=["Understand local environment and develop environmental responsibility"],
                    skills_developed=["Environmental awareness", "Local appreciation", "Civic responsibility"]
                ),
                CurriculumChapter(
                    chapter_number=4,
                    chapter_name="Our State and Country",
                    topics=[
                        CurriculumTopic(
                            code="SS2-4-1",
                            name="Our State",
                            chapter="Our State and Country",
                            learning_objectives=[
                                "Learn basic information about own state",
                                "Identify state capital and major cities",
                                "Learn about state festivals and culture",
                                "Understand state within country concept"
                            ],
                            key_concepts=["State", "Capital", "Cities", "State culture", "State festivals"],
                            prerequisites=["Basic geography concepts"],
                            difficulty_level="intermediate",
                            estimated_hours=14,
                            assessment_type=["state-identification", "capital-learning", "culture-sharing"]
                        ),
                        CurriculumTopic(
                            code="SS2-4-2",
                            name="Symbols of India",
                            chapter="Our State and Country",
                            learning_objectives=[
                                "Learn about national symbols (flag, anthem, emblem)",
                                "Understand their significance",
                                "Practice respectful behavior towards symbols",
                                "Develop national pride"
                            ],
                            key_concepts=["National symbols", "Flag", "Anthem", "Emblem", "Respect", "Pride"],
                            prerequisites=["National awareness"],
                            difficulty_level="intermediate",
                            estimated_hours=12,
                            assessment_type=["symbol-recognition", "anthem-practice", "respect-demonstration"]
                        )
                    ],
                    learning_outcomes=["Understand state identity and national symbols"],
                    skills_developed=["Geographical awareness", "National identity", "Patriotic values"]
                ),
                CurriculumChapter(
                    chapter_number=5,
                    chapter_name="Traditions and Cultures",
                    topics=[
                        CurriculumTopic(
                            code="SS2-5-1",
                            name="Cultural Diversity in India",
                            chapter="Traditions and Cultures",
                            learning_objectives=[
                                "Learn about different cultures in India",
                                "Understand various languages and traditions",
                                "Appreciate cultural festivals and practices",
                                "Promote unity in diversity"
                            ],
                            key_concepts=["Cultural diversity", "Languages", "Traditions", "Festivals", "Unity in diversity"],
                            prerequisites=["Cultural awareness"],
                            difficulty_level="advanced",
                            estimated_hours=16,
                            assessment_type=["culture-presentation", "language-appreciation", "diversity-celebration"]
                        )
                    ],
                    learning_outcomes=["Appreciate cultural diversity and promote unity"],
                    skills_developed=["Cultural appreciation", "Diversity acceptance", "National unity"]
                )
            ],
            yearly_learning_outcomes=[
                "Understand extended family and community connections",
                "Appreciate community helpers and public services",
                "Develop environmental responsibility and local pride", 
                "Build state identity and respect for national symbols",
                "Celebrate cultural diversity and national unity"
            ],
            assessment_pattern={
                "formative": "70%",
                "summative": "30%",
                "oral": "45%",
                "practical": "35%",
                "project": "20%"
            }
        )

    def get_expanded_social_studies_grade_3(self) -> SubjectCurriculum:
        """Enhanced Social Studies curriculum for Grade 3 - Complete Coverage"""
        return SubjectCurriculum(
            subject=Subject.SOCIAL_STUDIES,
            grade=3,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="Our Government and Leadership",
                    topics=[
                        CurriculumTopic(
                            code="SS3-1-1",
                            name="Local Government and Leadership",
                            chapter="Our Government and Leadership",
                            learning_objectives=[
                                "Learn about local government (Panchayat, Municipal Corporation)",
                                "Understand roles of local leaders (Sarpanch, Mayor)",
                                "Learn about community decision making",
                                "Understand citizen participation in democracy"
                            ],
                            key_concepts=["Local government", "Panchayat", "Municipality", "Leadership", "Democracy"],
                            prerequisites=["Community awareness"],
                            difficulty_level="intermediate",
                            estimated_hours=16,
                            assessment_type=["leadership-identification", "role-explanation", "participation-activities"]
                        ),
                        CurriculumTopic(
                            code="SS3-1-2",
                            name="Rights and Responsibilities",
                            chapter="Our Government and Leadership",
                            learning_objectives=[
                                "Learn about basic rights (education, healthcare, safety)",
                                "Understand civic responsibilities",
                                "Practice responsible citizenship",
                                "Learn about helping community"
                            ],
                            key_concepts=["Rights", "Responsibilities", "Citizenship", "Community service", "Civic duty"],
                            prerequisites=["Government understanding"],
                            difficulty_level="intermediate",
                            estimated_hours=14,
                            assessment_type=["rights-discussion", "responsibility-practice", "service-projects"]
                        )
                    ],
                    learning_outcomes=["Understand governance and develop civic responsibility"],
                    skills_developed=["Civic awareness", "Democratic participation", "Social responsibility"]
                ),
                CurriculumChapter(
                    chapter_number=2,
                    chapter_name="Geography and Natural Resources",
                    topics=[
                        CurriculumTopic(
                            code="SS3-2-1",
                            name="Physical Features of India",
                            chapter="Geography and Natural Resources",
                            learning_objectives=[
                                "Learn about mountains, plains, rivers, and deserts of India",
                                "Understand climate and seasons",
                                "Locate major geographical features on map",
                                "Appreciate geographical diversity"
                            ],
                            key_concepts=["Mountains", "Plains", "Rivers", "Deserts", "Climate", "Seasons"],
                            prerequisites=["Basic geography concepts"],
                            difficulty_level="intermediate",
                            estimated_hours=18,
                            assessment_type=["map-work", "feature-identification", "climate-discussion"]
                        ),
                        CurriculumTopic(
                            code="SS3-2-2",
                            name="Natural Resources and Conservation",
                            chapter="Geography and Natural Resources",
                            learning_objectives=[
                                "Learn about natural resources (water, forests, minerals)",
                                "Understand importance of conservation",
                                "Practice resource conservation",
                                "Learn about renewable and non-renewable resources"
                            ],
                            key_concepts=["Natural resources", "Conservation", "Water", "Forests", "Renewable", "Non-renewable"],
                            prerequisites=["Environmental awareness"],
                            difficulty_level="intermediate",
                            estimated_hours=16,
                            assessment_type=["resource-identification", "conservation-projects", "sustainability-practices"]
                        )
                    ],
                    learning_outcomes=["Understand geography and develop conservation mindset"],
                    skills_developed=["Geographical knowledge", "Environmental responsibility", "Map skills"]
                ),
                CurriculumChapter(
                    chapter_number=3,
                    chapter_name="History and Heritage",
                    topics=[
                        CurriculumTopic(
                            code="SS3-3-1",
                            name="Our Past and Heritage",
                            chapter="History and Heritage",
                            learning_objectives=[
                                "Learn about ancient Indian civilization",
                                "Understand historical monuments and their significance",
                                "Appreciate cultural heritage",
                                "Learn about great historical figures"
                            ],
                            key_concepts=["Ancient India", "Monuments", "Heritage", "Historical figures", "Culture"],
                            prerequisites=["Cultural awareness"],
                            difficulty_level="advanced",
                            estimated_hours=16,
                            assessment_type=["heritage-projects", "monument-study", "historical-storytelling"]
                        )
                    ],
                    learning_outcomes=["Develop historical consciousness and heritage appreciation"],
                    skills_developed=["Historical thinking", "Heritage appreciation", "Cultural understanding"]
                ),
                CurriculumChapter(
                    chapter_number=4,
                    chapter_name="Economic Activities",
                    topics=[
                        CurriculumTopic(
                            code="SS3-4-1",
                            name="Occupations and Livelihoods",
                            chapter="Economic Activities",
                            learning_objectives=[
                                "Learn about different occupations (farming, business, services)",
                                "Understand rural and urban livelihoods",
                                "Appreciate dignity of labor",
                                "Learn about economic interdependence"
                            ],
                            key_concepts=["Occupations", "Farming", "Business", "Services", "Rural", "Urban", "Dignity of labor"],
                            prerequisites=["Community helper knowledge"],
                            difficulty_level="intermediate",
                            estimated_hours=14,
                            assessment_type=["occupation-mapping", "livelihood-study", "labor-appreciation"]
                        ),
                        CurriculumTopic(
                            code="SS3-4-2",
                            name="Markets and Trade",
                            chapter="Economic Activities",
                            learning_objectives=[
                                "Learn about local markets and trade",
                                "Understand buying and selling",
                                "Learn about money and its uses",
                                "Understand economic cooperation"
                            ],
                            key_concepts=["Markets", "Trade", "Buying", "Selling", "Money", "Economic cooperation"],
                            prerequisites=["Basic economic awareness"],
                            difficulty_level="intermediate",
                            estimated_hours=12,
                            assessment_type=["market-visits", "trade-simulation", "money-handling"]
                        )
                    ],
                    learning_outcomes=["Understand economic activities and develop economic awareness"],
                    skills_developed=["Economic literacy", "Market understanding", "Financial awareness"]
                ),
                CurriculumChapter(
                    chapter_number=5,
                    chapter_name="Social Issues and Solutions",
                    topics=[
                        CurriculumTopic(
                            code="SS3-5-1",
                            name="Community Problems and Solutions",
                            chapter="Social Issues and Solutions",
                            learning_objectives=[
                                "Identify common community problems",
                                "Understand collective problem solving",
                                "Learn about social cooperation",
                                "Practice community participation"
                            ],
                            key_concepts=["Community problems", "Problem solving", "Cooperation", "Participation", "Solutions"],
                            prerequisites=["Community understanding"],
                            difficulty_level="advanced",
                            estimated_hours=14,
                            assessment_type=["problem-identification", "solution-brainstorming", "community-projects"]
                        )
                    ],
                    learning_outcomes=["Develop problem-solving skills and community engagement"],
                    skills_developed=["Critical thinking", "Problem solving", "Community engagement"]
                )
            ],
            yearly_learning_outcomes=[
                "Understand governance and develop civic responsibility",
                "Learn geography and develop conservation mindset",
                "Appreciate historical heritage and culture",
                "Understand economic activities and develop economic awareness",
                "Develop problem-solving skills and community engagement"
            ],
            assessment_pattern={
                "formative": "65%",
                "summative": "35%",
                "oral": "40%",
                "practical": "35%",
                "project": "25%"
            }
        )

    def get_expanded_social_studies_grade_4(self) -> SubjectCurriculum:
        """Enhanced Social Studies curriculum for Grade 4 - Complete Coverage"""
        return SubjectCurriculum(
            subject=Subject.SOCIAL_STUDIES,
            grade=4,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="Democratic Governance",
                    topics=[
                        CurriculumTopic(
                            code="SS4-1-1",
                            name="State and National Government",
                            chapter="Democratic Governance",
                            learning_objectives=[
                                "Learn about state and national government structure",
                                "Understand roles of Chief Minister and Prime Minister",
                                "Learn about elections and voting",
                                "Understand democratic processes"
                            ],
                            key_concepts=["State government", "National government", "Chief Minister", "Prime Minister", "Elections", "Democracy"],
                            prerequisites=["Local government knowledge"],
                            difficulty_level="advanced",
                            estimated_hours=18,
                            assessment_type=["government-mapping", "election-simulation", "democratic-processes"]
                        ),
                        CurriculumTopic(
                            code="SS4-1-2",
                            name="Constitution and Fundamental Rights",
                            chapter="Democratic Governance",
                            learning_objectives=[
                                "Learn about Indian Constitution basics",
                                "Understand fundamental rights for children",
                                "Learn about equality and justice",
                                "Practice constitutional values"
                            ],
                            key_concepts=["Constitution", "Fundamental rights", "Equality", "Justice", "Constitutional values"],
                            prerequisites=["Rights understanding"],
                            difficulty_level="advanced",
                            estimated_hours=16,
                            assessment_type=["rights-discussion", "equality-activities", "value-practice"]
                        )
                    ],
                    learning_outcomes=["Understand democratic governance and constitutional values"],
                    skills_developed=["Democratic understanding", "Constitutional awareness", "Value-based thinking"]
                ),
                CurriculumChapter(
                    chapter_number=2,
                    chapter_name="Advanced Geography",
                    topics=[
                        CurriculumTopic(
                            code="SS4-2-1",
                            name="States and Union Territories",
                            chapter="Advanced Geography",
                            learning_objectives=[
                                "Learn about different states and union territories of India",
                                "Understand state capitals and major cities",
                                "Learn about regional diversity",
                                "Practice map reading and location skills"
                            ],
                            key_concepts=["States", "Union territories", "Capitals", "Regional diversity", "Map skills"],
                            prerequisites=["Basic geography knowledge"],
                            difficulty_level="intermediate",
                            estimated_hours=20,
                            assessment_type=["map-work", "state-identification", "location-skills"]
                        ),
                        CurriculumTopic(
                            code="SS4-2-2",
                            name="Climate, Agriculture and Industries",
                            chapter="Advanced Geography",
                            learning_objectives=[
                                "Learn about different climatic regions of India",
                                "Understand major crops and agricultural patterns",
                                "Learn about important industries",
                                "Understand human-environment interaction"
                            ],
                            key_concepts=["Climate regions", "Agriculture", "Crops", "Industries", "Human-environment interaction"],
                            prerequisites=["Physical geography knowledge"],
                            difficulty_level="advanced",
                            estimated_hours=18,
                            assessment_type=["climate-mapping", "agriculture-study", "industry-identification"]
                        )
                    ],
                    learning_outcomes=["Master geographical knowledge and understand human-environment relationships"],
                    skills_developed=["Advanced geography", "Analytical thinking", "Spatial understanding"]
                ),
                CurriculumChapter(
                    chapter_number=3,
                    chapter_name="Indian History and Culture",
                    topics=[
                        CurriculumTopic(
                            code="SS4-3-1",
                            name="Medieval India and Mughal Period",
                            chapter="Indian History and Culture",
                            learning_objectives=[
                                "Learn about medieval Indian kingdoms",
                                "Understand Mughal empire and its contributions",
                                "Learn about architectural marvels",
                                "Appreciate cultural synthesis"
                            ],
                            key_concepts=["Medieval India", "Mughal empire", "Architecture", "Cultural synthesis"],
                            prerequisites=["Ancient history knowledge"],
                            difficulty_level="advanced",
                            estimated_hours=18,
                            assessment_type=["historical-timeline", "monument-study", "cultural-analysis"]
                        ),
                        CurriculumTopic(
                            code="SS4-3-2",
                            name="Freedom Struggle and Independence",
                            chapter="Indian History and Culture",
                            learning_objectives=[
                                "Learn about Indian freedom struggle",
                                "Understand role of freedom fighters",
                                "Learn about Mahatma Gandhi and non-violence",
                                "Appreciate sacrifice for independence"
                            ],
                            key_concepts=["Freedom struggle", "Freedom fighters", "Mahatma Gandhi", "Non-violence", "Independence"],
                            prerequisites=["Historical awareness"],
                            difficulty_level="advanced",
                            estimated_hours=16,
                            assessment_type=["freedom-fighter-study", "gandhi-principles", "independence-celebration"]
                        )
                    ],
                    learning_outcomes=["Understand Indian history and develop patriotic values"],
                    skills_developed=["Historical consciousness", "Patriotic values", "Cultural pride"]
                ),
                CurriculumChapter(
                    chapter_number=4,
                    chapter_name="Economic Development",
                    topics=[
                        CurriculumTopic(
                            code="SS4-4-1",
                            name="Economic Growth and Development",
                            chapter="Economic Development",
                            learning_objectives=[
                                "Learn about economic planning and development",
                                "Understand role of government in economy",
                                "Learn about poverty alleviation programs",
                                "Understand economic inequality and solutions"
                            ],
                            key_concepts=["Economic development", "Government role", "Poverty alleviation", "Economic inequality"],
                            prerequisites=["Basic economic understanding"],
                            difficulty_level="advanced",
                            estimated_hours=16,
                            assessment_type=["development-analysis", "program-study", "inequality-discussion"]
                        )
                    ],
                    learning_outcomes=["Understand economic development and social justice"],
                    skills_developed=["Economic analysis", "Social awareness", "Critical thinking"]
                ),
                CurriculumChapter(
                    chapter_number=5,
                    chapter_name="Global Awareness",
                    topics=[
                        CurriculumTopic(
                            code="SS4-5-1",
                            name="India and the World",
                            chapter="Global Awareness",
                            learning_objectives=[
                                "Learn about India's relationships with other countries",
                                "Understand international cooperation",
                                "Learn about United Nations and world peace",
                                "Develop global citizenship awareness"
                            ],
                            key_concepts=["International relations", "Cooperation", "United Nations", "World peace", "Global citizenship"],
                            prerequisites=["National awareness"],
                            difficulty_level="advanced",
                            estimated_hours=14,
                            assessment_type=["country-study", "cooperation-projects", "peace-activities"]
                        )
                    ],
                    learning_outcomes=["Develop global awareness and international understanding"],
                    skills_developed=["Global perspective", "International understanding", "Peace consciousness"]
                )
            ],
            yearly_learning_outcomes=[
                "Understand democratic governance and constitutional values",
                "Master geographical knowledge and human-environment relationships",
                "Learn Indian history and develop patriotic values",
                "Understand economic development and social justice",
                "Develop global awareness and international understanding"
            ],
            assessment_pattern={
                "formative": "60%",
                "summative": "40%",
                "oral": "35%",
                "written": "40%",
                "project": "25%"
            }
        )

    def get_expanded_social_studies_grade_5(self) -> SubjectCurriculum:
        """Enhanced Social Studies curriculum for Grade 5 - Complete Coverage"""
        return SubjectCurriculum(
            subject=Subject.SOCIAL_STUDIES,
            grade=5,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="Advanced Civics and Governance",
                    topics=[
                        CurriculumTopic(
                            code="SS5-1-1",
                            name="Parliamentary Democracy and Federal System",
                            chapter="Advanced Civics and Governance",
                            learning_objectives=[
                                "Learn about Parliament and its functions",
                                "Understand federal system and division of powers",
                                "Learn about separation of powers (executive, legislative, judicial)",
                                "Understand democratic accountability"
                            ],
                            key_concepts=["Parliament", "Federal system", "Separation of powers", "Democratic accountability"],
                            prerequisites=["Government structure knowledge"],
                            difficulty_level="advanced",
                            estimated_hours=20,
                            assessment_type=["parliament-simulation", "federal-mapping", "power-analysis"]
                        ),
                        CurriculumTopic(
                            code="SS5-1-2",
                            name="Social Justice and Human Rights",
                            chapter="Advanced Civics and Governance",
                            learning_objectives=[
                                "Learn about social justice and equality",
                                "Understand human rights and dignity",
                                "Learn about protection of minorities",
                                "Practice inclusive citizenship"
                            ],
                            key_concepts=["Social justice", "Human rights", "Equality", "Minorities", "Inclusive citizenship"],
                            prerequisites=["Rights and justice understanding"],
                            difficulty_level="advanced",
                            estimated_hours=18,
                            assessment_type=["justice-projects", "rights-advocacy", "inclusion-activities"]
                        )
                    ],
                    learning_outcomes=["Master democratic principles and social justice concepts"],
                    skills_developed=["Advanced civic knowledge", "Justice consciousness", "Democratic leadership"]
                ),
                CurriculumChapter(
                    chapter_number=2,
                    chapter_name="Comprehensive Geography",
                    topics=[
                        CurriculumTopic(
                            code="SS5-2-1",
                            name="Physical and Human Geography Integration",
                            chapter="Comprehensive Geography",
                            learning_objectives=[
                                "Understand interaction between physical and human geography",
                                "Learn about population distribution and migration",
                                "Understand urbanization and its impacts",
                                "Analyze geographical patterns and trends"
                            ],
                            key_concepts=["Physical-human geography", "Population", "Migration", "Urbanization", "Geographical patterns"],
                            prerequisites=["Advanced geography knowledge"],
                            difficulty_level="advanced",
                            estimated_hours=20,
                            assessment_type=["geography-integration", "population-analysis", "pattern-recognition"]
                        ),
                        CurriculumTopic(
                            code="SS5-2-2",
                            name="Environmental Geography and Sustainability",
                            chapter="Comprehensive Geography",
                            learning_objectives=[
                                "Learn about environmental challenges and solutions",
                                "Understand sustainable development concepts",
                                "Learn about climate change and its impacts",
                                "Practice environmental stewardship"
                            ],
                            key_concepts=["Environmental challenges", "Sustainable development", "Climate change", "Environmental stewardship"],
                            prerequisites=["Environmental awareness"],
                            difficulty_level="advanced",
                            estimated_hours=18,
                            assessment_type=["environmental-projects", "sustainability-planning", "stewardship-activities"]
                        )
                    ],
                    learning_outcomes=["Understand complex geographical relationships and environmental responsibility"],
                    skills_developed=["Advanced geographical analysis", "Environmental consciousness", "Sustainability thinking"]
                ),
                CurriculumChapter(
                    chapter_number=3,
                    chapter_name="Modern Indian History",
                    topics=[
                        CurriculumTopic(
                            code="SS5-3-1",
                            name="Post-Independence India",
                            chapter="Modern Indian History",
                            learning_objectives=[
                                "Learn about India after independence",
                                "Understand challenges of nation building",
                                "Learn about economic and social progress",
                                "Appreciate modern achievements"
                            ],
                            key_concepts=["Post-independence", "Nation building", "Economic progress", "Social progress", "Modern achievements"],
                            prerequisites=["Independence struggle knowledge"],
                            difficulty_level="advanced",
                            estimated_hours=18,
                            assessment_type=["progress-analysis", "achievement-study", "nation-building-projects"]
                        )
                    ],
                    learning_outcomes=["Understand modern Indian development and achievements"],
                    skills_developed=["Historical analysis", "Progress appreciation", "National pride"]
                ),
                CurriculumChapter(
                    chapter_number=4,
                    chapter_name="Advanced Economics",
                    topics=[
                        CurriculumTopic(
                            code="SS5-4-1",
                            name="Economic Systems and Global Economy",
                            chapter="Advanced Economics",
                            learning_objectives=[
                                "Learn about different economic systems",
                                "Understand India's role in global economy",
                                "Learn about international trade and cooperation",
                                "Understand economic interdependence"
                            ],
                            key_concepts=["Economic systems", "Global economy", "International trade", "Economic interdependence"],
                            prerequisites=["Economic development knowledge"],
                            difficulty_level="advanced",
                            estimated_hours=18,
                            assessment_type=["economic-analysis", "trade-study", "interdependence-mapping"]
                        ),
                        CurriculumTopic(
                            code="SS5-4-2",
                            name="Entrepreneurship and Innovation",
                            chapter="Advanced Economics",
                            learning_objectives=[
                                "Learn about entrepreneurship and business creation",
                                "Understand innovation and technology",
                                "Learn about economic opportunities",
                                "Practice entrepreneurial thinking"
                            ],
                            key_concepts=["Entrepreneurship", "Innovation", "Technology", "Economic opportunities"],
                            prerequisites=["Business understanding"],
                            difficulty_level="advanced",
                            estimated_hours=16,
                            assessment_type=["business-planning", "innovation-projects", "entrepreneurship-activities"]
                        )
                    ],
                    learning_outcomes=["Understand advanced economics and develop entrepreneurial mindset"],
                    skills_developed=["Economic sophistication", "Entrepreneurial thinking", "Innovation mindset"]
                ),
                CurriculumChapter(
                    chapter_number=5,
                    chapter_name="Global Citizenship and Future Challenges",
                    topics=[
                        CurriculumTopic(
                            code="SS5-5-1",
                            name="Global Challenges and Solutions",
                            chapter="Global Citizenship and Future Challenges",
                            learning_objectives=[
                                "Learn about global challenges (poverty, climate change, conflict)",
                                "Understand international cooperation for solutions",
                                "Learn about sustainable development goals",
                                "Develop global problem-solving mindset"
                            ],
                            key_concepts=["Global challenges", "International cooperation", "Sustainable development goals", "Global problem-solving"],
                            prerequisites=["Global awareness"],
                            difficulty_level="advanced",
                            estimated_hours=20,
                            assessment_type=["challenge-analysis", "solution-brainstorming", "global-projects"]
                        )
                    ],
                    learning_outcomes=["Develop global citizenship and future-oriented thinking"],
                    skills_developed=["Global consciousness", "Future thinking", "Problem-solving leadership"]
                )
            ],
            yearly_learning_outcomes=[
                "Master democratic principles and social justice concepts",
                "Understand complex geographical relationships and environmental responsibility",
                "Learn modern Indian history and appreciate achievements",
                "Understand advanced economics and develop entrepreneurial mindset",
                "Develop global citizenship and future-oriented thinking"
            ],
            assessment_pattern={
                "formative": "55%",
                "summative": "45%",
                "oral": "30%",
                "written": "45%",
                "project": "25%"
            }
        )

def main():
    expansion = SocialStudiesExpansion()
    
    print("EXPANDED SOCIAL STUDIES CURRICULUM - GRADES 1-5")
    print("=" * 65)
    
    total_all_topics = 0
    
    # All grades 1-5
    for grade_num in range(1, 6):
        method_name = f"get_expanded_social_studies_grade_{grade_num}"
        curriculum = getattr(expansion, method_name)()
        total_topics = sum(len(ch.topics) for ch in curriculum.chapters)
        total_all_topics += total_topics
        
        print(f"\n# Grade {grade_num} Social Studies - {total_topics} topics across {len(curriculum.chapters)} chapters")
        for chapter in curriculum.chapters:
            print(f"  • Chapter {chapter.chapter_number}: {chapter.chapter_name} ({len(chapter.topics)} topics)")
    
    print(f"\nSTATUS: Social Studies Grades 1-5 COMPLETE EXPANSION")
    print(f"Total Topics: {total_all_topics} comprehensive Social Studies topics")
    print(f"Average per Grade: {total_all_topics/5:.1f} topics")
    print("Covers: Civics, Geography, History, Economics, Global Citizenship")
    print("Ready for AI content generation and curriculum integration")

if __name__ == "__main__":
    main()