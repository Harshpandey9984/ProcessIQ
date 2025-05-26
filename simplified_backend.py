"""
Simplified backend for Digital Twin Platform.
This is a minimal backend to allow the frontend to connect.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
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
    description="Simplified API for Digital Twin Platform",
    version="1.0.0"
)

# ---- CORS Setup ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Authentication Setup ----
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

# ---- Models ----
class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

class UserIn(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None
    company: Optional[str] = None

# ---- Mock Data ----
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

DIGITAL_TWINS_DB = [
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
    },
    {
        "id": "3",
        "name": "Assembly Line #3",
        "process_type": "assembly_line", 
        "status": "running",
        "created_at": "2023-04-03T14:45:00Z",
        "current_metrics": {
            "quality_score": 0.95,
            "defect_rate": 0.008,
            "energy_consumption": 62.8,
            "throughput": 156.2
        }
    }
]

# ---- Helper Functions ----
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def authenticate_user(email: str, password: str):
    if email not in USERS_DB:
        return None
    user = USERS_DB[email]
    if not verify_password(password, user["hashed_password"]):
        return None
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

async def get_current_user(token: str = Depends(oauth2_scheme)):
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
    except JWTError:
        raise credentials_exception
    
    if username not in USERS_DB:
        raise credentials_exception
    
    return USERS_DB[username]

# ---- Routes ----
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Auth endpoints
@app.post("/api/auth/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, 
        expires_delta=access_token_expires
    )
    
    # Return token and user data
    user_copy = user.copy()
    del user_copy["hashed_password"]  # Don't return password hash
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": user_copy
    }

@app.post("/api/auth/register")
async def register_user(user_data: UserIn):
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
        "full_name": user_data.full_name or "New User",
        "hashed_password": hashed_password,
        "company": user_data.company,
        "role": "user",
        "is_active": True,
        "created_at": datetime.now()
    }
    
    USERS_DB[user_data.email] = new_user
    
    # Return the new user data without the password hash
    user_copy = new_user.copy()
    del user_copy["hashed_password"]
    return user_copy

# Digital Twin endpoints
@app.get("/api/digital-twin")
async def get_digital_twins(current_user = Depends(get_current_user)):
    return DIGITAL_TWINS_DB

@app.post("/api/digital-twin")
async def create_digital_twin(digital_twin: dict, current_user = Depends(get_current_user)):
    new_id = str(len(DIGITAL_TWINS_DB) + 1)
    digital_twin["id"] = new_id
    digital_twin["status"] = "created"
    digital_twin["created_at"] = datetime.now().isoformat()
    digital_twin["current_metrics"] = {
        "quality_score": 0.9,
        "defect_rate": 0.01,
        "energy_consumption": 100,
        "throughput": 50
    }
    DIGITAL_TWINS_DB.append(digital_twin)
    return digital_twin

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
