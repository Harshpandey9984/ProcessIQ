"""
Simplified standalone backend for the Digital Twin Platform.
This file contains a minimal backend that supports login functionality.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import secrets
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# ---- Basic Configuration ----
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

# ---- Initialize App ----
app = FastAPI(
    title="Digital Twin Platform API",
    description="Minimal API for Digital Twin Platform",
    version="1.0.0"
)

# Allow CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Models ----
class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    email: str
    password: str
    
# Add registration model
class UserRegister(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None
    company: Optional[str] = None
    role: Optional[str] = "user"

# ---- Authentication Setup ----
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

# ---- Mock Data ----
USERS_DB = {
    "admin@example.com": {
        "id": "1",
        "email": "admin@example.com",
        "full_name": "Admin User",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password"
        "role": "admin",
        "is_active": True
    },
    "user@example.com": {
        "id": "2", 
        "email": "user@example.com",
        "full_name": "Regular User",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password"
        "role": "user",
        "is_active": True
    }
}

# ---- Helper Functions ----
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(email):
    if email in USERS_DB:
        return USERS_DB[email]
    return None

def authenticate_user(email, password):
    user = get_user(email)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ---- Endpoints ----
@app.get("/")
def read_root():
    return {"message": "Digital Twin Platform API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/auth/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print(f"Login attempt: {form_data.username}")
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]},
        expires_delta=access_token_expires
    )
    
    # Create a copy of user without the hashed password
    user_copy = user.copy()
    del user_copy["hashed_password"]
    
    print(f"Login successful for: {user['email']}")
    return {"access_token": access_token, "token_type": "bearer", "user": user_copy}

@app.get("/api/digital-twin")
def get_digital_twins():
    """Return a list of digital twins."""
    print("Getting digital twins")
    return [
        {
            "id": "1",
            "name": "Injection Molding Line #1",
            "process_type": "injection_molding",
            "status": "running", 
            "created_at": "2023-04-01T10:30:00Z",
            "current_metrics": {
                "quality_score": 0.92,
                "defect_rate": 0.012,
                "energy_consumption": 120.5,
                "throughput": 42.3
            }
        },
        {
            "id": "2",
            "name": "CNC Machining Cell",
            "process_type": "cnc_machining",
            "status": "running",
            "created_at": "2023-04-02T09:15:00Z",
            "current_metrics": {
                "quality_score": 0.89,
                "defect_rate": 0.021,
                "energy_consumption": 75.2,
                "throughput": 18.7
            }
        }
    ]

@app.post("/api/auth/register")
async def register(user_data: UserRegister):
    """Register a new user."""
    print(f"Registration attempt: {user_data.email}")
    
    # Check if user already exists
    if user_data.email in USERS_DB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash the password
    hashed_password = pwd_context.hash(user_data.password)
    
    # Create new user
    user_id = f"{len(USERS_DB) + 1}"
    new_user = {
        "id": user_id,
        "email": user_data.email,
        "full_name": user_data.full_name or "New User",
        "hashed_password": hashed_password,
        "company": user_data.company,
        "role": user_data.role,
        "is_active": True
    }
    
    # Add to database
    USERS_DB[user_data.email] = new_user
    
    # Return user without password
    user_copy = new_user.copy()
    del user_copy["hashed_password"]
    
    print(f"Registration successful for: {user_data.email}")
    return user_copy

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
