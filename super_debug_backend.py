"""
Super simplified authentication server for debugging.
This uses direct plain-text password comparison and verbose logging.
"""

import uvicorn
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
import sys

# Configure logging to both file and console
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("logs/super_debug_backend.log"),
                        logging.StreamHandler(sys.stdout)
                    ])
logger = logging.getLogger("super-debug")

# ---- Basic Configuration ----
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

# ---- Models ----
class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

class UserIn(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None

# ---- Initialize App ----
app = FastAPI(
    title="Super Debug Auth API",
    description="Super simplified authentication API for debugging",
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
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

# ---- Mock Data with Plain Text Passwords ----
logger.info("Initializing user database with plain text passwords")
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
        "full_name": "Regular User",
        "password": "password",  # Plain text for debugging
        "role": "user",
        "is_active": True
    }
}
logger.info(f"Users available: {', '.join(USERS_DB.keys())}")

# ---- Helper Functions ----
def authenticate_user(email: str, password: str):
    """Ultra-simplified authentication with direct string comparison and verbose logging."""
    logger.info(f"AUTH ATTEMPT: Email='{email}', Password length={len(password)}")
    
    if email not in USERS_DB:
        logger.warning(f"AUTH FAILED: User '{email}' not found in database")
        return None
        
    user = USERS_DB[email]
    expected_password = user["password"]
    
    # Ultra-simple direct comparison
    if password != expected_password:
        logger.warning(f"AUTH FAILED: Password mismatch for '{email}'")
        logger.warning(f"AUTH FAILED: Expected='{expected_password}', Got='{password}'")
        return None
        
    logger.info(f"AUTH SUCCESS: User '{email}' authenticated successfully")
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT token with the provided data."""
    logger.info(f"Creating token for: {data.get('sub', 'unknown')}")
    
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    logger.info(f"Token created successfully")
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get the current user from a JWT token."""
    logger.info("Validating token")
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            logger.warning("Token missing 'sub' claim")
            raise credentials_exception
            
        if email not in USERS_DB:
            logger.warning(f"User '{email}' from token not found in database")
            raise credentials_exception
            
        user = USERS_DB[email]
        logger.info(f"Token valid for user: {email}")
        return user
        
    except JWTError as e:
        logger.error(f"JWT error: {str(e)}")
        raise credentials_exception
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise credentials_exception

# ---- Endpoints ----
@app.get("/", tags=["health"])
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Super Debug Auth API", "version": "1.0.0"}

@app.get("/health", tags=["health"])
def health_check():
    logger.info("Health check endpoint accessed")
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/debug/auth", tags=["debug"])
def debug_auth_config():
    """Debug endpoint to verify authentication configuration."""
    logger.info("Auth debug endpoint accessed")
    return {
        "auth_configured": True,
        "token_url": "/api/auth/token",
        "users": [{"email": k, "password": "password"} for k in USERS_DB.keys()],
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/auth/token", response_model=Token, tags=["auth"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """OAuth2 compatible token login endpoint with enhanced logging."""
    logger.info("==== LOGIN ATTEMPT START ====")
    logger.info(f"Login attempt for: {form_data.username}")
    logger.info(f"Password provided (length): {len(form_data.password)}")
    logger.info(f"Raw form_data: {form_data}")
    
    # Try to authenticate
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        logger.warning("Login failed - returning 401")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    logger.info("Creating access token")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, 
        expires_delta=access_token_expires
    )
    
    # Return token and user data
    user_copy = user.copy()
    del user_copy["password"]  # Don't return password
    
    logger.info("Login successful - returning token and user data")
    logger.info("==== LOGIN ATTEMPT END ====")
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": user_copy
    }

# --- Main App ---
if __name__ == "__main__":
    logger.info("Starting Super Debug Auth Server on port 8001")
    uvicorn.run(app, host="0.0.0.0", port=8001)
