import os
from pathlib import Path
from typing import Optional, List
from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Application
    app_name: str = "RSP Education Agent API"
    app_version: str = "2.0.0"
    debug: bool = Field(default=False, env="DEBUG")
    
    # Server
    server_host: str = Field(default="0.0.0.0", env="SERVER_HOST")
    server_port: int = Field(default=8000, env="SERVER_PORT")
    
    # Database
    database_url: str = Field(default="sqlite+aiosqlite:///./rsp_education.db", env="DATABASE_URL")
    database_echo: bool = Field(default=False, env="DATABASE_ECHO")
    
    # Redis
    redis_url: str = Field(default="redis://localhost:6379", env="REDIS_URL")
    
    # Authentication
    secret_key: str = Field(default="dev-secret-key-change-in-production", env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")
    
    # AI Models
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4-turbo-preview", env="OPENAI_MODEL")
    anthropic_api_key: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    anthropic_model: str = Field(default="claude-3-5-sonnet-20241022", env="ANTHROPIC_MODEL")
    
    # Vector Database
    pinecone_api_key: Optional[str] = Field(default=None, env="PINECONE_API_KEY")
    pinecone_environment: Optional[str] = Field(default=None, env="PINECONE_ENVIRONMENT")
    pinecone_index_name: str = Field(default="rsp-education", env="PINECONE_INDEX_NAME")
    
    # Speech Services
    azure_speech_key: Optional[str] = Field(default=None, env="AZURE_SPEECH_KEY")
    azure_speech_region: str = Field(default="eastus", env="AZURE_SPEECH_REGION")
    
    # Agent Configuration
    max_concurrent_agents: int = Field(default=10, env="MAX_CONCURRENT_AGENTS")
    agent_timeout_seconds: int = Field(default=300, env="AGENT_TIMEOUT_SECONDS")
    agent_retry_attempts: int = Field(default=3, env="AGENT_RETRY_ATTEMPTS")
    
    # Rate Limiting
    rate_limit_requests: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(default=60, env="RATE_LIMIT_WINDOW")
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")
    
    # CORS
    cors_origins: List[str] = Field(default=["*"], env="CORS_ORIGINS")
    
    # File Storage
    upload_path: Path = Field(default=Path("uploads"), env="UPLOAD_PATH")
    max_file_size: int = Field(default=10 * 1024 * 1024, env="MAX_FILE_SIZE")  # 10MB
    
    # Monitoring
    sentry_dsn: Optional[str] = Field(default=None, env="SENTRY_DSN")
    enable_metrics: bool = Field(default=True, env="ENABLE_METRICS")
    
    @validator('cors_origins', pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v
    
    @validator('upload_path', pre=True)
    def parse_upload_path(cls, v):
        if isinstance(v, str):
            return Path(v)
        return v
    
    def create_upload_path(self):
        """Create upload directory if it doesn't exist"""
        self.upload_path.mkdir(parents=True, exist_ok=True)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()

# CBSE Curriculum Configuration
CBSE_CURRICULUM = {
    "mathematics": {
        "grades": {
            "1": ["Numbers up to 20", "Basic Shapes", "Simple Addition/Subtraction"],
            "2": ["Numbers up to 100", "Multiplication Tables", "Measurement"],
            "3": ["Numbers up to 1000", "Fractions", "Geometry"],
            "4": ["Large Numbers", "Decimals", "Area and Perimeter"],
            "5": ["Factors and Multiples", "Data Handling", "Volume"],
            "6": ["Integers", "Algebra Basics", "Ratio and Proportion"],
            "7": ["Rational Numbers", "Linear Equations", "Triangles"],
            "8": ["Rational Numbers", "Linear Equations in One Variable", "Quadrilaterals"],
            "9": ["Number Systems", "Polynomials", "Coordinate Geometry"],
            "10": ["Real Numbers", "Linear Equations in Two Variables", "Trigonometry"],
            "11": ["Sets", "Relations and Functions", "Trigonometric Functions"],
            "12": ["Relations and Functions", "Algebra", "Calculus"]
        }
    },
    "science": {
        "grades": {
            "1": ["Plants and Animals", "Our Body", "Food"],
            "2": ["Living and Non-living", "Plants Around Us", "Animals Around Us"],
            "3": ["Plants", "Animals", "Our Environment"],
            "4": ["Food", "Shelter", "Water"],
            "5": ["Our Environment", "Food and Health", "Natural Resources"],
            "6": ["Food", "Fibre to Fabric", "The Living Organisms"],
            "7": ["Nutrition in Plants", "Weather and Climate", "Acids and Bases"],
            "8": ["Crop Production", "Microorganisms", "Force and Pressure"],
            "9": ["Matter", "Atoms and Molecules", "Gravitation"],
            "10": ["Chemical Reactions", "Life Processes", "Light"],
            "11": ["Physical World", "Units and Measurements", "Motion"],
            "12": ["Electric Charges", "Current Electricity", "Magnetic Effects"]
        }
    },
    "english": {
        "grades": {
            "1": ["Alphabets", "Simple Words", "Basic Grammar"],
            "2": ["Phonics", "Simple Sentences", "Story Reading"],
            "3": ["Reading Comprehension", "Creative Writing", "Grammar"],
            "4": ["Literature", "Grammar Rules", "Composition"],
            "5": ["Advanced Reading", "Essay Writing", "Poetry"],
            "6": ["Literature Analysis", "Grammar", "Creative Expression"],
            "7": ["Prose and Poetry", "Grammar", "Writing Skills"],
            "8": ["Literature", "Language Study", "Writing"],
            "9": ["Literature", "Language and Grammar", "Writing"],
            "10": ["Literature", "Grammar", "Writing and Speaking"],
            "11": ["Prose", "Poetry", "Supplementary Reader"],
            "12": ["Prose", "Poetry", "English Core"]
        }
    },
    "social_studies": {
        "grades": {
            "1": ["My Family", "My School", "My Neighbourhood"],
            "2": ["My Community", "Festivals", "Transport"],
            "3": ["Our Environment", "Government", "Culture"],
            "4": ["Our Past", "Our Earth", "Our Government"],
            "5": ["Our Country India", "World Geography", "Civics"],
            "6": ["History", "Geography", "Political Science"],
            "7": ["Medieval History", "Environment", "Democracy"],
            "8": ["Modern History", "Resources", "Indian Constitution"],
            "9": ["French Revolution", "Physical Features", "Democracy"],
            "10": ["Nationalism", "Resources and Development", "Power Sharing"],
            "11": ["Ancient World", "Physical Geography", "Political Theory"],
            "12": ["Modern World", "Human Geography", "Politics in India"]
        }
    }
}

# Agent Roles Configuration
AGENT_ROLES = {
    "learning_coordinator": {
        "name": "Learning Coordinator",
        "description": "Orchestrates overall learning journey and coordinates between agents",
        "capabilities": ["session_management", "learning_path_optimization", "agent_coordination"]
    },
    "content_generator": {
        "name": "Content Generator",
        "description": "Creates educational content, questions, and explanations",
        "capabilities": ["content_creation", "question_generation", "explanation_generation"]
    },
    "assessment_agent": {
        "name": "Assessment Agent", 
        "description": "Evaluates student performance and provides feedback",
        "capabilities": ["answer_evaluation", "performance_analysis", "feedback_generation"]
    },
    "adaptive_learning": {
        "name": "Adaptive Learning Agent",
        "description": "Personalizes learning experience based on student progress",
        "capabilities": ["difficulty_adjustment", "learning_style_detection", "personalization"]
    },
    "engagement_agent": {
        "name": "Engagement Agent",
        "description": "Maintains student motivation and engagement",
        "capabilities": ["gamification", "motivation", "progress_tracking"]
    },
    "analytics_agent": {
        "name": "Analytics Agent",
        "description": "Analyzes learning patterns and generates insights",
        "capabilities": ["data_analysis", "pattern_recognition", "reporting"]
    },
    "voice_interaction": {
        "name": "Voice & Interaction Agent",
        "description": "Handles speech, conversation, and UI interactions",
        "capabilities": ["speech_processing", "conversation_management", "ui_interaction"]
    }
}