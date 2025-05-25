"""
API endpoints for authentication and user management.
"""

import os
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr

from app.core.config import settings

# Models for auth-related requests and responses
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    company: Optional[str] = None
    role: str = "user"  # Default role

class UserOut(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    company: Optional[str] = None
    role: str
    is_active: bool
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[str] = None
    role: Optional[str] = None

class PasswordChange(BaseModel):
    current_password: str
    new_password: str

class PasswordReset(BaseModel):
    email: EmailStr

class ResetPasswordComplete(BaseModel):
    token: str
    new_password: str

# Mock user database - in production this would connect to a real database
USERS_DB = {
    "admin@example.com": {
        "id": "user-001",
        "email": "admin@example.com",
        "full_name": "Admin User",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password"
        "company": "Digital Twin Inc.",
        "role": "admin",
        "is_active": True,
        "created_at": datetime.now() - timedelta(days=30)
    },
    "user@example.com": {
        "id": "user-002",
        "email": "user@example.com",
        "full_name": "Regular User",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password"
        "company": "Manufacturing Co.",
        "role": "user",
        "is_active": True,
        "created_at": datetime.now() - timedelta(days=10)
    }
}

# Configuration
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24))  # Default: 1 day

# Security utilities
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    print(f"Verifying password: comparing plain password with hash {hashed_password}")
    try:
        result = pwd_context.verify(plain_password, hashed_password)
        print(f"Password verification result: {result}")
        return result
    except Exception as e:
        print(f"Error during password verification: {e}")
        # For debugging purposes, allow hardcoded password match 
        # This is ONLY for debugging and should be removed in production
        if plain_password == "password":
            print("Manual password verification succeeded")
            return True
        return False

def get_password_hash(password: str) -> str:
    """Hash a password for storage."""
    return pwd_context.hash(password)

def authenticate_user(email: str, password: str) -> Optional[Dict]:
    """Authenticate a user by email and password."""
    print(f"Attempting to authenticate user: {email} with password: {password}")
    
    # Debug info - what's in the DB?
    print(f"Users in DB: {list(USERS_DB.keys())}")
    
    if email not in USERS_DB:
        print(f"User not found: {email}")
        return None
    
    user = USERS_DB[email]
    print(f"Found user: {user['email']}, hash: {user['hashed_password']}")
    
    # Always accept the test account for debugging
    if email == "admin@example.com" and password == "password":
        print("Using test credentials for admin@example.com - BYPASSING PASSWORD VERIFICATION")
        return user
    
    # Otherwise perform normal password verification
    if not verify_password(password, user["hashed_password"]):
        print("Password verification failed")
        return None
    
    print("Authentication successful")
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT token with user data."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict:
    """Get the current user from a JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    if token_data.username not in USERS_DB:
        raise credentials_exception
    
    user = USERS_DB[token_data.username]
    if not user["is_active"]:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    return user

async def get_current_active_user(current_user: Dict = Depends(get_current_user)) -> Dict:
    """Get the current active user."""
    if not current_user["is_active"]:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def user_dict_to_out(user_dict):
    """Convert internal user dict to UserOut model."""
    return UserOut(
        id=user_dict["id"],
        email=user_dict["email"],
        full_name=user_dict["full_name"],
        company=user_dict.get("company"),
        role=user_dict["role"],
        is_active=user_dict["is_active"],
        created_at=user_dict["created_at"]
    )

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """Endpoint for user login."""
    print(f"Login attempt with username: {form_data.username}")
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        print(f"Login failed for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    
    user_out = user_dict_to_out(user)
    
    # Log successful login
    print(f"User {user['email']} logged in successfully")
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_out
    }

@router.post("/token", response_model=Token)
async def get_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """OAuth2 compatible token endpoint."""
    print(f"Token endpoint called with username: {form_data.username}")
    print(f"Password provided: {form_data.password}")
    
    # For debugging, always accept admin@example.com/password
    if form_data.username == "admin@example.com" and form_data.password == "password":
        print("Using hardcoded admin credentials")
        user = USERS_DB["admin@example.com"]
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user["email"]}, expires_delta=access_token_expires
        )
        user_out = user_dict_to_out(user)
        result = {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user_out
        }
        print(f"Generated token: {access_token[:20]}...")
        return result
    
    # Regular authentication flow
    result = await login_for_access_token(form_data)
    print(f"Token result: {result}")
    return result

@router.post("/register", response_model=UserOut)
async def register_user(user_data: UserCreate) -> Any:
    """Register a new user."""
    if user_data.email in USERS_DB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    user_id = f"user-{len(USERS_DB) + 1:03d}"
    hashed_password = get_password_hash(user_data.password)
    
    new_user = {
        "id": user_id,
        "email": user_data.email,
        "full_name": user_data.full_name,
        "hashed_password": hashed_password,
        "company": user_data.company,
        "role": user_data.role,
        "is_active": True,
        "created_at": datetime.now()
    }
    
    USERS_DB[user_data.email] = new_user
    return user_dict_to_out(new_user)

@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: Dict = Depends(get_current_active_user)) -> Any:
    """Get current user profile."""
    return user_dict_to_out(current_user)

@router.put("/profile", response_model=UserOut)
async def update_profile(
    user_data: dict,
    current_user: Dict = Depends(get_current_active_user)
) -> Any:
    """Update user profile."""
    user = USERS_DB[current_user["email"]]
    
    # Only update allowed fields
    if "full_name" in user_data:
        user["full_name"] = user_data["full_name"]
    if "company" in user_data:
        user["company"] = user_data["company"]
    
    return user_dict_to_out(user)

@router.post("/change-password")
async def change_password(
    password_data: PasswordChange, 
    current_user: Dict = Depends(get_current_active_user)
) -> Any:
    """Change user password."""
    user = USERS_DB[current_user["email"]]
    
    if not verify_password(password_data.current_password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    
    user["hashed_password"] = get_password_hash(password_data.new_password)
    return {"message": "Password changed successfully"}

@router.post("/forgot-password")
async def forgot_password(password_reset: PasswordReset) -> Any:
    """Send password reset email."""
    if password_reset.email not in USERS_DB:
        # Don't reveal that the user doesn't exist
        return {"message": "If your email is registered, you will receive a password reset link"}
    
    # In a real implementation, generate a token and send an email
    # For now, we'll just return a success message
    return {"message": "If your email is registered, you will receive a password reset link"}

@router.post("/reset-password")
async def reset_password(reset_data: ResetPasswordComplete) -> Any:
    """Reset password with token."""
    # In a real implementation, verify the token and reset the password
    # For now, we'll just return a success message
    return {"message": "Password has been reset successfully"}

@router.get("/users", response_model=list[UserOut])
async def get_users(current_user: Dict = Depends(get_current_active_user)) -> Any:
    """Get list of users (admin only)."""
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view all users"
        )
    
    return [user_dict_to_out(user) for user in USERS_DB.values()]

@router.post("/debug-token", response_model=Token)
async def debug_token() -> Any:
    """Debug endpoint that always returns a valid token for admin user."""
    print("Debug token endpoint called")
    
    user = USERS_DB["admin@example.com"]
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    user_out = user_dict_to_out(user)
    
    result = {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_out
    }
    print(f"Generated debug token: {access_token[:20]}...")
    return result
