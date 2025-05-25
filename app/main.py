"""
Main application file for the Digital Twin Optimization Platform.
This initializes the FastAPI server and coordinates the different components.
"""

import os
import sys
import logging
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.middleware import RateLimiter

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.api.api import api_router
from app.core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Digital Twin Optimization Platform",
    description="AI-powered platform for optimizing manufacturing processes",
    version="1.0.0",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://localhost:3000"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Set up rate limiting - applies primarily to auth endpoints
app.add_middleware(
    RateLimiter,
    requests_limit=100,  # 100 requests per minute limit
    window_seconds=60,   # 1 minute window
    block_duration_seconds=300  # Block for 5 minutes if limit exceeded
)

# Include API router
app.include_router(api_router, prefix="/api")

# Mount static files for the frontend
app.mount("/", StaticFiles(directory="app/frontend/build", html=True), name="static")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    logger.info("Starting Digital Twin Optimization Platform")
    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG,
    )
