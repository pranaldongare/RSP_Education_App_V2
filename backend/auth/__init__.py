"""
Authentication module for RSP Education Agent V2
"""

from .auth_service import auth_service, AuthService, UserRegistration, UserLogin, TokenResponse

__all__ = ["auth_service", "AuthService", "UserRegistration", "UserLogin", "TokenResponse"]