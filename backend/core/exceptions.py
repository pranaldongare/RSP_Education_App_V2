"""
Custom Exception Classes
Defines application-specific exceptions
"""


class AppException(Exception):
    """Base application exception"""
    
    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code or "APP_ERROR"
        super().__init__(self.message)


class AgentException(AppException):
    """Agent-specific exceptions"""
    
    def __init__(self, message: str, code: str = None):
        super().__init__(message, code or "AGENT_ERROR")


class CurriculumException(AppException):
    """Curriculum-related exceptions"""
    
    def __init__(self, message: str, code: str = None):
        super().__init__(message, code or "CURRICULUM_ERROR")


class ValidationException(AppException):
    """Validation exceptions"""
    
    def __init__(self, message: str, code: str = None):
        super().__init__(message, code or "VALIDATION_ERROR")


class ContentGenerationException(AgentException):
    """Content generation specific exceptions"""
    
    def __init__(self, message: str, code: str = None):
        super().__init__(message, code or "CONTENT_GENERATION_ERROR")