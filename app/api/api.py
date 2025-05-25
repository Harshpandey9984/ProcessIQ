"""
Main API router for the Digital Twin Optimization Platform.
"""

from fastapi import APIRouter

from app.api.endpoints import simulation, optimization, models, digital_twin, auth

api_router = APIRouter()

# Include routers from endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(simulation.router, prefix="/simulation", tags=["Simulation"])
api_router.include_router(optimization.router, prefix="/optimization", tags=["Optimization"])
api_router.include_router(models.router, prefix="/models", tags=["Models"])
api_router.include_router(digital_twin.router, prefix="/digital-twin", tags=["Digital Twin"])
