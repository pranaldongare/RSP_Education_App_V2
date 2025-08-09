#!/usr/bin/env python3
"""
Expand English Curriculum for Grades 1-5
Creates comprehensive CBSE-aligned English curriculum with all topics
"""

import sys
sys.path.append('.')

from core.curriculum import Subject, CurriculumTopic, CurriculumChapter, SubjectCurriculum

class EnglishExpansion:
    def __init__(self):
        self.subject = Subject.ENGLISH
        
    def get_expanded_english_grade_1(self) -> SubjectCurriculum:
        """Enhanced English curriculum for Grade 1 - Complete Coverage"""
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
                            name="Capital and Small Letters",
                            chapter="Letters and Sounds",
                            learning_objectives=[
                                "Identify and write capital letters A-Z",
                                "Identify and write small letters a-z",
                                "Match capital and small letters",
                                "Understand letter formation"
                            ],
                            key_concepts=["Capital letters", "Small letters", "Letter recognition", "Writing"],
                            prerequisites=["Basic motor skills"],
                            difficulty_level="beginner",
                            estimated_hours=15,
                            assessment_type=["writing", "identification", "matching"]
                        ),
                        CurriculumTopic(
                            code="E1-1-2",
                            name="Letter Sounds (Phonics)",
                            chapter="Letters and Sounds",
                            learning_objectives=[
                                "Learn sounds of each letter",
                                "Connect letters with their sounds",
                                "Blend simple sounds to make words",
                                "Identify beginning sounds in words"
                            ],
                            key_concepts=["Phonics", "Letter sounds", "Beginning sounds", "Sound blending"],
                            prerequisites=["Letter recognition"],
                            difficulty_level="beginner",
                            estimated_hours=18,
                            assessment_type=["oral", "sound-identification", "blending"]
                        )
                    ],
                    learning_outcomes=["Master basic letter recognition and sounds"],
                    skills_developed=["Letter writing", "Phonetic awareness", "Sound recognition"]
                ),
                CurriculumChapter(
                    chapter_number=2,
                    chapter_name="Simple Words",
                    topics=[
                        CurriculumTopic(
                            code="E1-2-1",
                            name="Three Letter Words",
                            chapter="Simple Words",
                            learning_objectives=[
                                "Read simple three-letter words (cat, bat, mat)",
                                "Write three-letter words correctly",
                                "Understand word meaning through pictures",
                                "Form words using letter sounds"
                            ],
                            key_concepts=["Three-letter words", "CVC words", "Word formation", "Reading"],
                            prerequisites=["Letter sounds knowledge"],
                            difficulty_level="beginner",
                            estimated_hours=12,
                            assessment_type=["reading", "writing", "word-formation"]
                        ),
                        CurriculumTopic(
                            code="E1-2-2",
                            name="Sight Words",
                            chapter="Simple Words",
                            learning_objectives=[
                                "Recognize common sight words (the, and, is, my)",
                                "Read sight words quickly without sounding out",
                                "Use sight words in simple sentences",
                                "Build sight word vocabulary"
                            ],
                            key_concepts=["Sight words", "Word recognition", "Vocabulary", "Reading fluency"],
                            prerequisites=["Basic reading skills"],
                            difficulty_level="beginner",
                            estimated_hours=10,
                            assessment_type=["recognition", "reading", "sentence-use"]
                        )
                    ],
                    learning_outcomes=["Read and write simple words independently"],
                    skills_developed=["Word recognition", "Vocabulary building", "Reading confidence"]
                ),
                CurriculumChapter(
                    chapter_number=3,
                    chapter_name="Simple Sentences",
                    topics=[
                        CurriculumTopic(
                            code="E1-3-1",
                            name="Making Sentences",
                            chapter="Simple Sentences",
                            learning_objectives=[
                                "Form simple sentences using known words",
                                "Use capital letter at beginning of sentence",
                                "Use full stop at end of sentence",
                                "Read simple sentences aloud"
                            ],
                            key_concepts=["Simple sentences", "Capital letters", "Full stop", "Sentence structure"],
                            prerequisites=["Word reading ability"],
                            difficulty_level="intermediate",
                            estimated_hours=14,
                            assessment_type=["sentence-formation", "reading", "punctuation"]
                        )
                    ],
                    learning_outcomes=["Create and read simple sentences correctly"],
                    skills_developed=["Sentence construction", "Punctuation", "Reading comprehension"]
                ),
                CurriculumChapter(
                    chapter_number=4,
                    chapter_name="Listening and Speaking",
                    topics=[
                        CurriculumTopic(
                            code="E1-4-1",
                            name="Rhymes and Songs",
                            chapter="Listening and Speaking",
                            learning_objectives=[
                                "Recite nursery rhymes with proper rhythm",
                                "Sing simple songs in English",
                                "Identify rhyming words",
                                "Enjoy language through music and rhythm"
                            ],
                            key_concepts=["Nursery rhymes", "Songs", "Rhyming words", "Rhythm"],
                            prerequisites=["Basic listening skills"],
                            difficulty_level="beginner",
                            estimated_hours=10,
                            assessment_type=["recitation", "singing", "rhyme-identification"]
                        ),
                        CurriculumTopic(
                            code="E1-4-2",
                            name="Simple Conversations",
                            chapter="Listening and Speaking",
                            learning_objectives=[
                                "Introduce themselves in English",
                                "Use polite words (please, thank you, sorry)",
                                "Ask and answer simple questions",
                                "Express basic needs in English"
                            ],
                            key_concepts=["Self-introduction", "Polite words", "Questions", "Basic communication"],
                            prerequisites=["Basic vocabulary"],
                            difficulty_level="beginner",
                            estimated_hours=12,
                            assessment_type=["conversation", "oral", "role-play"]
                        )
                    ],
                    learning_outcomes=["Develop basic listening and speaking skills"],
                    skills_developed=["Oral communication", "Listening skills", "Social interaction"]
                ),
                CurriculumChapter(
                    chapter_number=5,
                    chapter_name="Fun with Stories",
                    topics=[
                        CurriculumTopic(
                            code="E1-5-1",
                            name="Picture Stories",
                            chapter="Fun with Stories",
                            learning_objectives=[
                                "Look at pictures and tell simple stories",
                                "Understand story sequence",
                                "Listen to stories with attention",
                                "Answer questions about stories"
                            ],
                            key_concepts=["Picture stories", "Story sequence", "Comprehension", "Storytelling"],
                            prerequisites=["Basic vocabulary and listening"],
                            difficulty_level="intermediate",
                            estimated_hours=10,
                            assessment_type=["storytelling", "comprehension", "sequencing"]
                        )
                    ],
                    learning_outcomes=["Enjoy stories and develop comprehension skills"],
                    skills_developed=["Story comprehension", "Sequential thinking", "Imagination"]
                )
            ],
            yearly_learning_outcomes=[
                "Master basic letter recognition and phonics",
                "Read and write simple words and sentences",
                "Develop basic conversation skills in English",
                "Enjoy English through stories, rhymes, and songs"
            ],
            assessment_pattern={
                "formative": "70%",
                "summative": "30%",
                "oral": "40%",
                "written": "35%",
                "practical": "25%"
            }
        )

    def get_expanded_english_grade_2(self) -> SubjectCurriculum:
        """Enhanced English curriculum for Grade 2 - Complete Coverage"""
        return SubjectCurriculum(
            subject=Subject.ENGLISH,
            grade=2,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="Reading Skills",
                    topics=[
                        CurriculumTopic(
                            code="E2-1-1",
                            name="Reading Comprehension",
                            chapter="Reading Skills",
                            learning_objectives=[
                                "Read simple paragraphs fluently",
                                "Understand main ideas in text",
                                "Answer questions about reading passages",
                                "Identify characters and settings in stories"
                            ],
                            key_concepts=["Reading fluency", "Comprehension", "Main ideas", "Characters", "Settings"],
                            prerequisites=["Basic reading ability"],
                            difficulty_level="intermediate",
                            estimated_hours=16,
                            assessment_type=["reading", "comprehension", "Q&A"]
                        ),
                        CurriculumTopic(
                            code="E2-1-2",
                            name="Vocabulary Building",
                            chapter="Reading Skills",
                            learning_objectives=[
                                "Learn new words through context",
                                "Use dictionary skills (picture dictionary)",
                                "Understand word meanings",
                                "Build sight word vocabulary"
                            ],
                            key_concepts=["New vocabulary", "Context clues", "Dictionary", "Word meanings"],
                            prerequisites=["Basic word recognition"],
                            difficulty_level="intermediate",
                            estimated_hours=12,
                            assessment_type=["vocabulary-tests", "dictionary-use", "meaning-matching"]
                        )
                    ],
                    learning_outcomes=["Read with understanding and expand vocabulary"],
                    skills_developed=["Reading fluency", "Vocabulary expansion", "Comprehension skills"]
                ),
                CurriculumChapter(
                    chapter_number=2,
                    chapter_name="Writing Skills",
                    topics=[
                        CurriculumTopic(
                            code="E2-2-1",
                            name="Sentence Writing",
                            chapter="Writing Skills",
                            learning_objectives=[
                                "Write complete sentences with proper punctuation",
                                "Use describing words (adjectives)",
                                "Write about personal experiences",
                                "Arrange words to make meaningful sentences"
                            ],
                            key_concepts=["Complete sentences", "Adjectives", "Personal writing", "Word order"],
                            prerequisites=["Basic sentence knowledge"],
                            difficulty_level="intermediate",
                            estimated_hours=14,
                            assessment_type=["sentence-writing", "descriptive-writing", "personal-narrative"]
                        ),
                        CurriculumTopic(
                            code="E2-2-2",
                            name="Creative Writing",
                            chapter="Writing Skills",
                            learning_objectives=[
                                "Write short stories with beginning, middle, end",
                                "Create characters for stories",
                                "Use imagination in writing",
                                "Write simple poems"
                            ],
                            key_concepts=["Story structure", "Character creation", "Imagination", "Poetry"],
                            prerequisites=["Sentence writing skills"],
                            difficulty_level="intermediate",
                            estimated_hours=12,
                            assessment_type=["story-writing", "character-creation", "poetry"]
                        )
                    ],
                    learning_outcomes=["Write clear sentences and creative pieces"],
                    skills_developed=["Writing fluency", "Creativity", "Story structure"]
                ),
                CurriculumChapter(
                    chapter_number=3,
                    chapter_name="Grammar Basics",
                    topics=[
                        CurriculumTopic(
                            code="E2-3-1",
                            name="Parts of Speech",
                            chapter="Grammar Basics",
                            learning_objectives=[
                                "Identify naming words (nouns)",
                                "Identify action words (verbs)",
                                "Use describing words (adjectives) correctly",
                                "Understand word types in sentences"
                            ],
                            key_concepts=["Nouns", "Verbs", "Adjectives", "Parts of speech"],
                            prerequisites=["Basic sentence knowledge"],
                            difficulty_level="intermediate",
                            estimated_hours=14,
                            assessment_type=["identification", "classification", "sentence-construction"]
                        )
                    ],
                    learning_outcomes=["Understand basic parts of speech"],
                    skills_developed=["Grammar awareness", "Language structure", "Analytical skills"]
                ),
                CurriculumChapter(
                    chapter_number=4,
                    chapter_name="Speaking and Listening",
                    topics=[
                        CurriculumTopic(
                            code="E2-4-1",
                            name="Presentations and Discussions",
                            chapter="Speaking and Listening",
                            learning_objectives=[
                                "Give short presentations on familiar topics",
                                "Participate in class discussions",
                                "Listen actively to others",
                                "Ask relevant questions"
                            ],
                            key_concepts=["Presentations", "Discussions", "Active listening", "Questioning"],
                            prerequisites=["Basic conversation skills"],
                            difficulty_level="intermediate",
                            estimated_hours=12,
                            assessment_type=["presentations", "discussion-participation", "listening-tasks"]
                        ),
                        CurriculumTopic(
                            code="E2-4-2",
                            name="Drama and Role Play",
                            chapter="Speaking and Listening",
                            learning_objectives=[
                                "Act out simple stories and scenes",
                                "Use voice and gestures effectively",
                                "Work cooperatively in groups",
                                "Express emotions through drama"
                            ],
                            key_concepts=["Drama", "Role play", "Voice modulation", "Group work"],
                            prerequisites=["Basic speaking confidence"],
                            difficulty_level="intermediate",
                            estimated_hours=10,
                            assessment_type=["drama-performance", "role-play", "group-work"]
                        )
                    ],
                    learning_outcomes=["Develop confident speaking and active listening"],
                    skills_developed=["Public speaking", "Dramatic expression", "Collaborative skills"]
                ),
                CurriculumChapter(
                    chapter_number=5,
                    chapter_name="Literature and Fun",
                    topics=[
                        CurriculumTopic(
                            code="E2-5-1",
                            name="Stories and Poems",
                            chapter="Literature and Fun",
                            learning_objectives=[
                                "Read and enjoy age-appropriate stories",
                                "Memorize and recite simple poems",
                                "Identify moral lessons in stories",
                                "Connect stories to personal experiences"
                            ],
                            key_concepts=["Story appreciation", "Poetry", "Moral lessons", "Personal connections"],
                            prerequisites=["Reading comprehension"],
                            difficulty_level="intermediate",
                            estimated_hours=12,
                            assessment_type=["story-analysis", "poetry-recitation", "moral-discussion"]
                        )
                    ],
                    learning_outcomes=["Appreciate literature and develop moral understanding"],
                    skills_developed=["Literary appreciation", "Moral reasoning", "Cultural awareness"]
                )
            ],
            yearly_learning_outcomes=[
                "Read fluently with comprehension",
                "Write clear sentences and creative pieces",
                "Understand basic grammar concepts", 
                "Communicate confidently in English",
                "Appreciate stories and poems"
            ],
            assessment_pattern={
                "formative": "65%",
                "summative": "35%",
                "oral": "35%",
                "written": "40%",
                "practical": "25%"
            }
        )

    def get_expanded_english_grade_3(self) -> SubjectCurriculum:
        """Enhanced English curriculum for Grade 3 - Complete Coverage"""
        return SubjectCurriculum(
            subject=Subject.ENGLISH,
            grade=3,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="Advanced Reading",
                    topics=[
                        CurriculumTopic(
                            code="E3-1-1",
                            name="Reading Fluency and Expression",
                            chapter="Advanced Reading",
                            learning_objectives=[
                                "Read aloud with proper expression and pace",
                                "Use punctuation cues for expression",
                                "Understand dialogue in stories",
                                "Practice silent reading for comprehension"
                            ],
                            key_concepts=["Reading fluency", "Expression", "Dialogue", "Silent reading"],
                            prerequisites=["Basic reading skills"],
                            difficulty_level="intermediate",
                            estimated_hours=15,
                            assessment_type=["oral-reading", "expression", "comprehension"]
                        ),
                        CurriculumTopic(
                            code="E3-1-2",
                            name="Text Analysis and Inference",
                            chapter="Advanced Reading",
                            learning_objectives=[
                                "Make inferences from text clues",
                                "Identify cause and effect relationships",
                                "Compare and contrast characters",
                                "Predict story outcomes"
                            ],
                            key_concepts=["Inference", "Cause and effect", "Character comparison", "Prediction"],
                            prerequisites=["Reading comprehension"],
                            difficulty_level="advanced",
                            estimated_hours=14,
                            assessment_type=["analysis", "inference-tasks", "prediction"]
                        )
                    ],
                    learning_outcomes=["Read with fluency and analyze text deeply"],
                    skills_developed=["Advanced comprehension", "Analytical thinking", "Expression"]
                ),
                CurriculumChapter(
                    chapter_number=2,
                    chapter_name="Advanced Writing",
                    topics=[
                        CurriculumTopic(
                            code="E3-2-1",
                            name="Paragraph Writing",
                            chapter="Advanced Writing",
                            learning_objectives=[
                                "Write well-organized paragraphs with topic sentences",
                                "Use supporting details effectively",
                                "Practice different paragraph types (descriptive, narrative)",
                                "Edit and revise written work"
                            ],
                            key_concepts=["Paragraph structure", "Topic sentences", "Supporting details", "Revision"],
                            prerequisites=["Sentence writing skills"],
                            difficulty_level="advanced",
                            estimated_hours=16,
                            assessment_type=["paragraph-writing", "structure-analysis", "revision"]
                        ),
                        CurriculumTopic(
                            code="E3-2-2",
                            name="Creative and Informational Writing",
                            chapter="Advanced Writing",
                            learning_objectives=[
                                "Write creative stories with detailed descriptions",
                                "Write informational pieces about topics of interest",
                                "Use variety in sentence structure",
                                "Develop personal writing voice"
                            ],
                            key_concepts=["Creative writing", "Informational writing", "Sentence variety", "Writing voice"],
                            prerequisites=["Basic writing fluency"],
                            difficulty_level="advanced",
                            estimated_hours=14,
                            assessment_type=["creative-writing", "informational-writing", "voice-development"]
                        )
                    ],
                    learning_outcomes=["Write organized paragraphs and develop personal style"],
                    skills_developed=["Organization", "Creativity", "Information presentation"]
                ),
                CurriculumChapter(
                    chapter_number=3,
                    chapter_name="Grammar and Language",
                    topics=[
                        CurriculumTopic(
                            code="E3-3-1",
                            name="Advanced Grammar",
                            chapter="Grammar and Language",
                            learning_objectives=[
                                "Understand subject and predicate in sentences",
                                "Use different types of sentences (statements, questions, exclamations)",
                                "Learn about singular and plural nouns",
                                "Use verb tenses correctly (past, present, future)"
                            ],
                            key_concepts=["Subject-predicate", "Sentence types", "Singular-plural", "Verb tenses"],
                            prerequisites=["Basic parts of speech"],
                            difficulty_level="intermediate",
                            estimated_hours=16,
                            assessment_type=["grammar-exercises", "sentence-analysis", "tense-usage"]
                        ),
                        CurriculumTopic(
                            code="E3-3-2",
                            name="Spelling and Word Study",
                            chapter="Grammar and Language",
                            learning_objectives=[
                                "Learn spelling patterns and rules",
                                "Use prefixes and suffixes",
                                "Understand compound words",
                                "Practice dictionary skills"
                            ],
                            key_concepts=["Spelling patterns", "Prefixes", "Suffixes", "Compound words"],
                            prerequisites=["Basic vocabulary"],
                            difficulty_level="intermediate",
                            estimated_hours=12,
                            assessment_type=["spelling-tests", "word-building", "dictionary-use"]
                        )
                    ],
                    learning_outcomes=["Master grammar rules and spelling patterns"],
                    skills_developed=["Language mechanics", "Word analysis", "Dictionary skills"]
                ),
                CurriculumChapter(
                    chapter_number=4,
                    chapter_name="Communication Skills",
                    topics=[
                        CurriculumTopic(
                            code="E3-4-1",
                            name="Oral Presentations and Debates",
                            chapter="Communication Skills",
                            learning_objectives=[
                                "Prepare and deliver structured presentations",
                                "Participate in simple debates and discussions",
                                "Use visual aids effectively",
                                "Practice persuasive speaking"
                            ],
                            key_concepts=["Structured presentations", "Debates", "Visual aids", "Persuasion"],
                            prerequisites=["Basic speaking skills"],
                            difficulty_level="advanced",
                            estimated_hours=14,
                            assessment_type=["presentations", "debates", "persuasive-speaking"]
                        )
                    ],
                    learning_outcomes=["Communicate ideas effectively through speaking"],
                    skills_developed=["Public speaking", "Persuasion", "Visual presentation"]
                ),
                CurriculumChapter(
                    chapter_number=5,
                    chapter_name="Literature Appreciation",
                    topics=[
                        CurriculumTopic(
                            code="E3-5-1",
                            name="Poetry and Drama",
                            chapter="Literature Appreciation",
                            learning_objectives=[
                                "Analyze simple poems for meaning and emotion",
                                "Understand rhythm and rhyme in poetry",
                                "Read and perform simple plays",
                                "Appreciate different forms of literature"
                            ],
                            key_concepts=["Poetry analysis", "Rhythm and rhyme", "Drama performance", "Literary forms"],
                            prerequisites=["Reading fluency"],
                            difficulty_level="advanced",
                            estimated_hours=12,
                            assessment_type=["poetry-analysis", "recitation", "drama-performance"]
                        )
                    ],
                    learning_outcomes=["Appreciate and analyze different literary forms"],
                    skills_developed=["Literary analysis", "Performance", "Cultural appreciation"]
                )
            ],
            yearly_learning_outcomes=[
                "Read with advanced comprehension and analysis",
                "Write organized paragraphs and creative pieces",
                "Master grammar rules and spelling patterns",
                "Communicate effectively through speaking and presentation",
                "Appreciate poetry, drama, and literature"
            ],
            assessment_pattern={
                "formative": "60%",
                "summative": "40%",
                "oral": "30%",
                "written": "45%",
                "practical": "25%"
            }
        )

    def get_expanded_english_grade_4(self) -> SubjectCurriculum:
        """Enhanced English curriculum for Grade 4 - Complete Coverage"""
        return SubjectCurriculum(
            subject=Subject.ENGLISH,
            grade=4,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="Reading Comprehension",
                    topics=[
                        CurriculumTopic(
                            code="E4-1-1",
                            name="Critical Reading Skills",
                            chapter="Reading Comprehension",
                            learning_objectives=[
                                "Identify main ideas and supporting details",
                                "Distinguish between fact and opinion",
                                "Make connections between texts and personal experience",
                                "Summarize passages effectively"
                            ],
                            key_concepts=["Main ideas", "Supporting details", "Fact vs opinion", "Text connections", "Summarizing"],
                            prerequisites=["Advanced reading fluency"],
                            difficulty_level="advanced",
                            estimated_hours=16,
                            assessment_type=["comprehension-tests", "summary-writing", "critical-analysis"]
                        ),
                        CurriculumTopic(
                            code="E4-1-2",
                            name="Reading Different Text Types",
                            chapter="Reading Comprehension",
                            learning_objectives=[
                                "Read and understand fiction and non-fiction texts",
                                "Identify text features (headings, captions, diagrams)",
                                "Use context clues to understand unknown words",
                                "Compare information from multiple sources"
                            ],
                            key_concepts=["Fiction", "Non-fiction", "Text features", "Context clues", "Source comparison"],
                            prerequisites=["Text analysis skills"],
                            difficulty_level="advanced",
                            estimated_hours=14,
                            assessment_type=["text-type-analysis", "feature-identification", "source-comparison"]
                        )
                    ],
                    learning_outcomes=["Read critically and understand diverse text types"],
                    skills_developed=["Critical thinking", "Text analysis", "Information synthesis"]
                ),
                CurriculumChapter(
                    chapter_number=2,
                    chapter_name="Advanced Writing",
                    topics=[
                        CurriculumTopic(
                            code="E4-2-1",
                            name="Essay Writing",
                            chapter="Advanced Writing",
                            learning_objectives=[
                                "Write structured essays with introduction, body, conclusion",
                                "Develop and support arguments with evidence",
                                "Use transition words effectively",
                                "Practice different essay types (narrative, descriptive, expository)"
                            ],
                            key_concepts=["Essay structure", "Arguments", "Evidence", "Transitions", "Essay types"],
                            prerequisites=["Paragraph writing skills"],
                            difficulty_level="advanced",
                            estimated_hours=18,
                            assessment_type=["essay-writing", "argument-development", "structure-analysis"]
                        ),
                        CurriculumTopic(
                            code="E4-2-2",
                            name="Research and Report Writing",
                            chapter="Advanced Writing",
                            learning_objectives=[
                                "Conduct simple research on topics of interest",
                                "Take notes from multiple sources",
                                "Write informational reports",
                                "Cite sources appropriately for grade level"
                            ],
                            key_concepts=["Research skills", "Note-taking", "Report writing", "Source citation"],
                            prerequisites=["Informational writing"],
                            difficulty_level="advanced",
                            estimated_hours=16,
                            assessment_type=["research-projects", "report-writing", "source-citation"]
                        )
                    ],
                    learning_outcomes=["Write structured essays and research-based reports"],
                    skills_developed=["Research skills", "Academic writing", "Information organization"]
                ),
                CurriculumChapter(
                    chapter_number=3,
                    chapter_name="Language Mechanics",
                    topics=[
                        CurriculumTopic(
                            code="E4-3-1",
                            name="Advanced Grammar and Usage",
                            chapter="Language Mechanics",
                            learning_objectives=[
                                "Use complex sentence structures",
                                "Understand and use dependent and independent clauses",
                                "Master punctuation rules (commas, quotation marks)",
                                "Use pronoun-antecedent agreement"
                            ],
                            key_concepts=["Complex sentences", "Clauses", "Punctuation", "Pronoun agreement"],
                            prerequisites=["Basic grammar mastery"],
                            difficulty_level="advanced",
                            estimated_hours=16,
                            assessment_type=["grammar-exercises", "sentence-combining", "punctuation-practice"]
                        )
                    ],
                    learning_outcomes=["Master complex grammar and punctuation rules"],
                    skills_developed=["Language precision", "Sentence sophistication", "Editing skills"]
                ),
                CurriculumChapter(
                    chapter_number=4,
                    chapter_name="Speaking and Presentation",
                    topics=[
                        CurriculumTopic(
                            code="E4-4-1",
                            name="Formal Speaking and Debate",
                            chapter="Speaking and Presentation",
                            learning_objectives=[
                                "Deliver formal speeches with clear organization",
                                "Participate in structured debates",
                                "Use evidence to support arguments in speaking",
                                "Demonstrate active listening and respectful response"
                            ],
                            key_concepts=["Formal speaking", "Debate techniques", "Evidence use", "Active listening"],
                            prerequisites=["Basic presentation skills"],
                            difficulty_level="advanced",
                            estimated_hours=14,
                            assessment_type=["formal-speeches", "debate-participation", "listening-assessment"]
                        ),
                        CurriculumTopic(
                            code="E4-4-2",
                            name="Media and Technology Integration",
                            chapter="Speaking and Presentation",
                            learning_objectives=[
                                "Create multimedia presentations",
                                "Use technology tools for communication",
                                "Evaluate media messages critically",
                                "Present information using digital tools"
                            ],
                            key_concepts=["Multimedia presentations", "Technology tools", "Media literacy", "Digital communication"],
                            prerequisites=["Basic technology skills"],
                            difficulty_level="advanced",
                            estimated_hours=12,
                            assessment_type=["multimedia-projects", "technology-use", "media-analysis"]
                        )
                    ],
                    learning_outcomes=["Communicate effectively using traditional and digital media"],
                    skills_developed=["Media literacy", "Digital communication", "Technology integration"]
                ),
                CurriculumChapter(
                    chapter_number=5,
                    chapter_name="Literary Analysis",
                    topics=[
                        CurriculumTopic(
                            code="E4-5-1",
                            name="Genre Study and Literary Elements",
                            chapter="Literary Analysis",
                            learning_objectives=[
                                "Identify and analyze literary elements (plot, character, setting, theme)",
                                "Compare different genres of literature",
                                "Understand author's purpose and perspective",
                                "Make text-to-text, text-to-self, and text-to-world connections"
                            ],
                            key_concepts=["Literary elements", "Genres", "Author's purpose", "Text connections"],
                            prerequisites=["Literature appreciation"],
                            difficulty_level="advanced",
                            estimated_hours=14,
                            assessment_type=["literary-analysis", "genre-comparison", "connection-making"]
                        )
                    ],
                    learning_outcomes=["Analyze literature using critical thinking skills"],
                    skills_developed=["Literary analysis", "Critical thinking", "Cultural understanding"]
                )
            ],
            yearly_learning_outcomes=[
                "Read critically and analyze diverse text types",
                "Write structured essays and research-based reports",
                "Master complex grammar and language mechanics",
                "Communicate effectively through formal speaking and digital media",
                "Analyze literature using critical thinking skills"
            ],
            assessment_pattern={
                "formative": "55%",
                "summative": "45%",
                "oral": "25%",
                "written": "50%",
                "practical": "25%"
            }
        )

    def get_expanded_english_grade_5(self) -> SubjectCurriculum:
        """Enhanced English curriculum for Grade 5 - Complete Coverage"""
        return SubjectCurriculum(
            subject=Subject.ENGLISH,
            grade=5,
            chapters=[
                CurriculumChapter(
                    chapter_number=1,
                    chapter_name="Advanced Reading and Analysis",
                    topics=[
                        CurriculumTopic(
                            code="E5-1-1",
                            name="Literary Analysis and Interpretation",
                            chapter="Advanced Reading and Analysis",
                            learning_objectives=[
                                "Analyze themes and messages in complex texts",
                                "Interpret figurative language (metaphors, similes)",
                                "Evaluate author's craft and writing techniques",
                                "Make sophisticated inferences and connections"
                            ],
                            key_concepts=["Theme analysis", "Figurative language", "Author's craft", "Sophisticated inference"],
                            prerequisites=["Critical reading skills"],
                            difficulty_level="advanced",
                            estimated_hours=18,
                            assessment_type=["literary-analysis", "interpretation-essays", "craft-evaluation"]
                        ),
                        CurriculumTopic(
                            code="E5-1-2",
                            name="Research and Information Literacy",
                            chapter="Advanced Reading and Analysis",
                            learning_objectives=[
                                "Evaluate credibility and reliability of sources",
                                "Synthesize information from multiple sources",
                                "Understand bias and perspective in texts",
                                "Use advanced research strategies"
                            ],
                            key_concepts=["Source credibility", "Information synthesis", "Bias analysis", "Research strategies"],
                            prerequisites=["Basic research skills"],
                            difficulty_level="advanced",
                            estimated_hours=16,
                            assessment_type=["source-evaluation", "synthesis-projects", "bias-analysis"]
                        )
                    ],
                    learning_outcomes=["Analyze complex texts and conduct sophisticated research"],
                    skills_developed=["Advanced analysis", "Research expertise", "Critical evaluation"]
                ),
                CurriculumChapter(
                    chapter_number=2,
                    chapter_name="Sophisticated Writing",
                    topics=[
                        CurriculumTopic(
                            code="E5-2-1",
                            name="Argumentative and Persuasive Writing",
                            chapter="Sophisticated Writing",
                            learning_objectives=[
                                "Write persuasive essays with strong arguments",
                                "Use rhetorical techniques effectively",
                                "Address counterarguments",
                                "Support claims with credible evidence"
                            ],
                            key_concepts=["Argumentative writing", "Rhetorical techniques", "Counterarguments", "Evidence support"],
                            prerequisites=["Essay writing skills"],
                            difficulty_level="advanced",
                            estimated_hours=20,
                            assessment_type=["argumentative-essays", "persuasive-writing", "evidence-evaluation"]
                        ),
                        CurriculumTopic(
                            code="E5-2-2",
                            name="Creative and Professional Writing",
                            chapter="Sophisticated Writing",
                            learning_objectives=[
                                "Write in various professional formats (letters, emails, reports)",
                                "Create original literary pieces (stories, poems, plays)",
                                "Adapt writing style for different audiences",
                                "Edit and revise work for publication quality"
                            ],
                            key_concepts=["Professional formats", "Original creation", "Audience adaptation", "Publication quality"],
                            prerequisites=["Advanced writing skills"],
                            difficulty_level="advanced",
                            estimated_hours=18,
                            assessment_type=["professional-writing", "creative-pieces", "audience-adaptation"]
                        )
                    ],
                    learning_outcomes=["Write sophisticated arguments and adapt style for various purposes"],
                    skills_developed=["Advanced writing", "Style adaptation", "Professional communication"]
                ),
                CurriculumChapter(
                    chapter_number=3,
                    chapter_name="Language Mastery",
                    topics=[
                        CurriculumTopic(
                            code="E5-3-1",
                            name="Advanced Language Conventions",
                            chapter="Language Mastery",
                            learning_objectives=[
                                "Master advanced punctuation and capitalization",
                                "Use varied sentence structures for effect",
                                "Understand etymology and word origins",
                                "Apply advanced vocabulary in writing and speaking"
                            ],
                            key_concepts=["Advanced conventions", "Sentence variety", "Etymology", "Advanced vocabulary"],
                            prerequisites=["Grammar mastery"],
                            difficulty_level="advanced",
                            estimated_hours=16,
                            assessment_type=["convention-mastery", "sentence-variety", "vocabulary-application"]
                        )
                    ],
                    learning_outcomes=["Demonstrate mastery of advanced language conventions"],
                    skills_developed=["Language sophistication", "Convention mastery", "Vocabulary expertise"]
                ),
                CurriculumChapter(
                    chapter_number=4,
                    chapter_name="Communication and Media",
                    topics=[
                        CurriculumTopic(
                            code="E5-4-1",
                            name="Advanced Communication Skills",
                            chapter="Communication and Media",
                            learning_objectives=[
                                "Lead group discussions and facilitate meetings",
                                "Create and deliver persuasive presentations",
                                "Interview others and present findings",
                                "Communicate effectively across different contexts"
                            ],
                            key_concepts=["Group leadership", "Persuasive presentation", "Interviewing", "Context adaptation"],
                            prerequisites=["Formal speaking skills"],
                            difficulty_level="advanced",
                            estimated_hours=16,
                            assessment_type=["leadership-assessment", "persuasive-presentations", "interview-projects"]
                        ),
                        CurriculumTopic(
                            code="E5-4-2",
                            name="Digital Literacy and Media Creation",
                            chapter="Communication and Media",
                            learning_objectives=[
                                "Create sophisticated digital content",
                                "Understand digital citizenship and ethics",
                                "Analyze media messages and techniques",
                                "Use technology for collaborative projects"
                            ],
                            key_concepts=["Digital content creation", "Digital citizenship", "Media analysis", "Technology collaboration"],
                            prerequisites=["Media literacy basics"],
                            difficulty_level="advanced",
                            estimated_hours=14,
                            assessment_type=["digital-projects", "media-analysis", "collaboration-assessment"]
                        )
                    ],
                    learning_outcomes=["Lead communications and create sophisticated digital content"],
                    skills_developed=["Leadership", "Digital expertise", "Advanced communication"]
                ),
                CurriculumChapter(
                    chapter_number=5,
                    chapter_name="Literary Scholarship",
                    topics=[
                        CurriculumTopic(
                            code="E5-5-1",
                            name="Comparative Literature and Cultural Analysis",
                            chapter="Literary Scholarship",
                            learning_objectives=[
                                "Compare literature across cultures and time periods",
                                "Understand historical and cultural contexts of texts",
                                "Analyze how literature reflects and shapes society",
                                "Develop personal literary preferences and justifications"
                            ],
                            key_concepts=["Comparative analysis", "Cultural context", "Literature and society", "Personal preferences"],
                            prerequisites=["Literary analysis skills"],
                            difficulty_level="advanced",
                            estimated_hours=16,
                            assessment_type=["comparative-analysis", "cultural-essays", "preference-justification"]
                        )
                    ],
                    learning_outcomes=["Engage in sophisticated literary scholarship"],
                    skills_developed=["Scholarly analysis", "Cultural understanding", "Independent thinking"]
                )
            ],
            yearly_learning_outcomes=[
                "Analyze complex texts with sophisticated interpretation",
                "Write arguments and adapt style for various audiences",
                "Demonstrate mastery of advanced language conventions",
                "Lead communications and create digital content",
                "Engage in literary scholarship and cultural analysis"
            ],
            assessment_pattern={
                "formative": "50%",
                "summative": "50%",
                "oral": "25%",
                "written": "50%",
                "practical": "25%"
            }
        )

def main():
    expansion = EnglishExpansion()
    
    print("EXPANDED ENGLISH CURRICULUM - GRADES 1-5")
    print("=" * 60)
    
    total_all_topics = 0
    
    # All grades 1-5
    for grade_num in range(1, 6):
        method_name = f"get_expanded_english_grade_{grade_num}"
        curriculum = getattr(expansion, method_name)()
        total_topics = sum(len(ch.topics) for ch in curriculum.chapters)
        total_all_topics += total_topics
        
        print(f"\n# Grade {grade_num} English - {total_topics} topics across {len(curriculum.chapters)} chapters")
        for chapter in curriculum.chapters:
            print(f"  • Chapter {chapter.chapter_number}: {chapter.chapter_name} ({len(chapter.topics)} topics)")
    
    print(f"\nSTATUS: English Grades 1-5 COMPLETE EXPANSION")
    print(f"Total Topics: {total_all_topics} comprehensive English topics")
    print(f"Average per Grade: {total_all_topics/5:.1f} topics")
    print("Ready for AI content generation and curriculum integration")
    print("Next: Integrate into curriculum.py")

if __name__ == "__main__":
    main()