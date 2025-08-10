"""
Authentication Service - RSP Education Agent V2
Handles user authentication, session management, and JWT token operations.
"""

from jose import jwt
import bcrypt
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, EmailStr, Field
import logging

from database.models import Student, UserSession
from core.exceptions import AgentException
from config.settings import settings

logger = logging.getLogger(__name__)

# JWT Configuration
JWT_SECRET_KEY = settings.secret_key
JWT_ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_DAYS = settings.refresh_token_expire_days

class UserRegistration(BaseModel):
    """User registration request model"""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    grade: str = Field(..., min_length=1, max_length=10)
    phone: Optional[str] = Field(None, max_length=20)
    school: Optional[str] = Field(None, max_length=100)
    parent_email: Optional[EmailStr] = None
    preferred_language: str = Field(default="en", max_length=10)

class UserLogin(BaseModel):
    """User login request model"""
    email: EmailStr
    password: str
    remember_me: bool = False

class TokenResponse(BaseModel):
    """Authentication token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user_info: Dict[str, Any]

class AuthService:
    """Authentication service for user management"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.AuthService")
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify a password against its hash"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except Exception as e:
            self.logger.error(f"Password verification error: {e}")
            return False
    
    def generate_student_id(self) -> str:
        """Generate a unique student ID"""
        timestamp = datetime.utcnow().strftime("%Y%m")
        random_part = secrets.token_hex(4).upper()
        return f"STU{timestamp}{random_part}"
    
    def create_jwt_token(self, student_id: str, token_type: str = "access") -> str:
        """Create a JWT token"""
        if token_type == "access":
            expire_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        else:  # refresh token
            expire_delta = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        
        expire = datetime.utcnow() + expire_delta
        
        payload = {
            "sub": student_id,
            "type": token_type,
            "exp": expire,
            "iat": datetime.utcnow()
        }
        
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return token
    
    def verify_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            self.logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            self.logger.warning(f"Invalid token: {e}")
            return None
    
    async def register_user(self, db: Session, registration: UserRegistration, 
                          user_agent: str = None, ip_address: str = None) -> TokenResponse:
        """Register a new user"""
        try:
            # Check if email already exists
            existing_user = db.query(Student).filter(Student.email == registration.email).first()
            if existing_user:
                raise AgentException("Email already registered")
            
            # Generate unique student ID
            student_id = self.generate_student_id()
            
            # Hash password
            password_hash = self.hash_password(registration.password)
            
            # Create new student
            new_student = Student(
                id=student_id,
                name=registration.name,
                email=registration.email,
                password_hash=password_hash,
                grade=registration.grade,
                phone=registration.phone,
                school=registration.school,
                parent_email=registration.parent_email,
                preferred_language=registration.preferred_language,
                login_count=0
            )
            
            db.add(new_student)
            db.commit()
            
            # Create session tokens
            access_token = self.create_jwt_token(student_id, "access")
            refresh_token = self.create_jwt_token(student_id, "refresh")
            
            # Create user session
            session = UserSession(
                student_id=student_id,
                session_token=access_token,
                refresh_token=refresh_token,
                expires_at=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
                user_agent=user_agent,
                ip_address=ip_address,
                device_type="web"
            )
            
            db.add(session)
            db.commit()
            
            self.logger.info(f"User registered successfully: {student_id}")
            
            return TokenResponse(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                user_info={
                    "student_id": student_id,
                    "name": registration.name,
                    "email": registration.email,
                    "grade": registration.grade,
                    "preferred_language": registration.preferred_language
                }
            )
            
        except IntegrityError as e:
            db.rollback()
            self.logger.error(f"Database integrity error during registration: {e}")
            raise AgentException("Registration failed due to data conflict")
        except Exception as e:
            db.rollback()
            self.logger.error(f"Registration error: {e}")
            raise AgentException(f"Registration failed: {str(e)}")
    
    async def login_user(self, db: Session, login: UserLogin, 
                        user_agent: str = None, ip_address: str = None) -> TokenResponse:
        """Authenticate and login user"""
        try:
            # Find user by email
            user = db.query(Student).filter(Student.email == login.email).first()
            if not user or not user.is_active:
                raise AgentException("Invalid email or password")
            
            # Verify password
            if not self.verify_password(login.password, user.password_hash):
                raise AgentException("Invalid email or password")
            
            # Update login info
            user.last_login = datetime.utcnow()
            user.login_count += 1
            
            # Create session tokens
            access_token = self.create_jwt_token(user.id, "access")
            refresh_token = self.create_jwt_token(user.id, "refresh")
            
            # Deactivate old sessions if not remember_me
            if not login.remember_me:
                db.query(UserSession).filter(
                    UserSession.student_id == user.id,
                    UserSession.is_active == True
                ).update({"is_active": False})
            
            # Create new session
            expire_time = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS if login.remember_me 
                                 else REFRESH_TOKEN_EXPIRE_DAYS / 7)
            
            session = UserSession(
                student_id=user.id,
                session_token=access_token,
                refresh_token=refresh_token,
                expires_at=datetime.utcnow() + expire_time,
                user_agent=user_agent,
                ip_address=ip_address,
                device_type="web"
            )
            
            db.add(session)
            db.commit()
            
            self.logger.info(f"User logged in successfully: {user.id}")
            
            return TokenResponse(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                user_info={
                    "student_id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "grade": user.grade,
                    "preferred_language": user.preferred_language,
                    "last_login": user.last_login.isoformat() if user.last_login else None
                }
            )
            
        except AgentException:
            raise
        except Exception as e:
            db.rollback()
            self.logger.error(f"Login error: {e}")
            raise AgentException(f"Login failed: {str(e)}")
    
    async def refresh_token(self, db: Session, refresh_token: str) -> TokenResponse:
        """Refresh access token using refresh token"""
        try:
            # Verify refresh token
            payload = self.verify_jwt_token(refresh_token)
            if not payload or payload.get("type") != "refresh":
                raise AgentException("Invalid refresh token")
            
            student_id = payload.get("sub")
            
            # Find active session
            session = db.query(UserSession).filter(
                UserSession.refresh_token == refresh_token,
                UserSession.is_active == True,
                UserSession.expires_at > datetime.utcnow()
            ).first()
            
            if not session:
                raise AgentException("Session expired or invalid")
            
            # Get user info
            user = db.query(Student).filter(Student.id == student_id).first()
            if not user or not user.is_active:
                raise AgentException("User not found or inactive")
            
            # Create new tokens
            new_access_token = self.create_jwt_token(student_id, "access")
            new_refresh_token = self.create_jwt_token(student_id, "refresh")
            
            # Update session
            session.session_token = new_access_token
            session.refresh_token = new_refresh_token
            session.expires_at = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
            session.last_accessed = datetime.utcnow()
            
            db.commit()
            
            return TokenResponse(
                access_token=new_access_token,
                refresh_token=new_refresh_token,
                expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                user_info={
                    "student_id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "grade": user.grade,
                    "preferred_language": user.preferred_language
                }
            )
            
        except AgentException:
            raise
        except Exception as e:
            self.logger.error(f"Token refresh error: {e}")
            raise AgentException(f"Token refresh failed: {str(e)}")
    
    async def logout_user(self, db: Session, access_token: str) -> bool:
        """Logout user and invalidate session"""
        try:
            # Find and deactivate session
            session = db.query(UserSession).filter(
                UserSession.session_token == access_token,
                UserSession.is_active == True
            ).first()
            
            if session:
                session.is_active = False
                db.commit()
                self.logger.info(f"User logged out: {session.student_id}")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Logout error: {e}")
            return False
    
    async def get_current_user(self, db: Session, access_token: str) -> Optional[Student]:
        """Get current user from access token"""
        try:
            # Verify token
            payload = self.verify_jwt_token(access_token)
            if not payload or payload.get("type") != "access":
                return None
            
            student_id = payload.get("sub")
            
            # Verify active session
            session = db.query(UserSession).filter(
                UserSession.session_token == access_token,
                UserSession.is_active == True,
                UserSession.expires_at > datetime.utcnow()
            ).first()
            
            if not session:
                return None
            
            # Get user
            user = db.query(Student).filter(
                Student.id == student_id,
                Student.is_active == True
            ).first()
            
            if user:
                # Update last accessed
                session.last_accessed = datetime.utcnow()
                db.commit()
            
            return user
            
        except Exception as e:
            self.logger.error(f"Get current user error: {e}")
            return None

# Global auth service instance
auth_service = AuthService()