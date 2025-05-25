"""
Simple backend with hardcoded password verification for debugging.
"""

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import secrets
import logging
from datetime import datetime, timedelta
from jose import JWTError, jwt

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='logs/debug_login.log',
                    filemode='a')
logger = logging.getLogger(__name__)

# Console handler
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(console)

# ---- Basic Configuration ----
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

# ---- Initialize App ----
app = FastAPI(
    title="Digital Twin Platform API",
    description="Debug API for Digital Twin Platform",
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
    role: Optional[str] = "user"

# ---- Authentication Setup ----
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

# ---- Mock Data ----
USERS_DB = {
    "admin@example.com": {
        "id": "1",
        "email": "admin@example.com",
        "full_name": "Admin User",
        "password": "password",  # Plain text for debugging
        "role": "admin",
        "is_active": True
    },
    "user@example.com": {
        "id": "2", 
        "email": "user@example.com",
        "password": "password",  # Plain text for debugging
        "full_name": "Regular User",
        "role": "user",
        "is_active": True
    }
}

# ---- Digital Twin Mock Data ----
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
    }
]

# ---- Helper Functions ----
def authenticate_user(email: str, password: str):
    logger.info(f"DEBUG AUTH: Authenticating user: {email}")
    logger.info(f"DEBUG AUTH: Password provided: {password}")
    
    if email not in USERS_DB:
        logger.warning(f"DEBUG AUTH: User not found: {email}")
        return None
        
    user = USERS_DB[email]
    
    # Simple direct comparison - for debugging only!
    if password != user["password"]:
        logger.warning(f"DEBUG AUTH: Password mismatch for {email}")
        logger.warning(f"DEBUG AUTH: Expected '{user['password']}', got '{password}'")
        return None
        
    logger.info(f"DEBUG AUTH: Authentication successful for user: {email}")
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
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
            
        if email not in USERS_DB:
            raise credentials_exception
            
        user = USERS_DB[email]
        return user
    except JWTError:
        raise credentials_exception
    except Exception:
        raise credentials_exception

# ---- Endpoints ----
@app.get("/", tags=["health"])
def read_root():
    return {"message": "Digital Twin Platform Debug API", "version": "1.0.0"}

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/debug/auth", tags=["debug"])
def debug_auth_config():
    """Debug endpoint to verify authentication configuration."""
    logger.info("Debug auth configuration endpoint accessed")
    return {
        "auth_configured": True,
        "token_url": "/api/auth/token",
        "register_url": "/api/auth/register",
        "users": [{"email": k, "password": "password"} for k in USERS_DB.keys()],
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/auth/token", response_model=Token, tags=["auth"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    logger.info(f"DEBUG LOGIN: Login attempt received for: {form_data.username}")
    logger.info(f"DEBUG LOGIN: Password provided (length): {len(form_data.password)}")
    
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        logger.warning(f"DEBUG LOGIN: Login failed for: {form_data.username}")
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
    
    # Return token and user data (excluding password)
    user_copy = user.copy()
    del user_copy["password"]  # Don't return password
    
    logger.info(f"DEBUG LOGIN: Login successful for: {user['email']}")
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": user_copy
    }

@app.post("/api/auth/register", tags=["auth"])
async def register_user(user_data: UserIn):
    if user_data.email in USERS_DB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user_id = f"{len(USERS_DB) + 1}"
    new_user = {
        "id": user_id,
        "email": user_data.email,
        "full_name": user_data.full_name or "New User",
        "password": user_data.password,
        "company": user_data.company,
        "role": user_data.role,
        "is_active": True
    }
    
    # Add to database
    USERS_DB[user_data.email] = new_user
    
    # Return user without password
    user_copy = new_user.copy()
    del user_copy["password"]
    
    logger.info(f"User registered: {user_data.email}")
    return user_copy

@app.get("/api/digital-twin", tags=["digital-twin"])
async def get_digital_twins(current_user = Depends(get_current_user)):
    """Return a list of digital twins."""
    return DIGITAL_TWINS_DB

@app.get("/api/digital-twin/{twin_id}", tags=["digital-twin"])
async def get_digital_twin(twin_id: str, current_user = Depends(get_current_user)):
    """Return a specific digital twin."""
    for twin in DIGITAL_TWINS_DB:
        if twin["id"] == twin_id:
            return twin
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Digital twin with ID {twin_id} not found"
    )

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting debug login backend server on port 8001...")
    uvicorn.run(app, host="0.0.0.0", port=8001)
