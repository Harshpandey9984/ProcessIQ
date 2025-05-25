"""
API endpoints for simulation operations.
"""

from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, Query

from app.simulation.engine import SimulationEngine
from app.models.schemas.simulation import (
    SimulationConfig, 
    SimulationResult,
    ProcessParameter
)

router = APIRouter()

sim_engine = SimulationEngine()

@router.post("/run", response_model=SimulationResult)
async def run_simulation(config: SimulationConfig) -> Any:
    """
    Run a manufacturing process simulation with the provided configuration.
    """
    try:
        result = sim_engine.run_simulation(config)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Simulation failed: {str(e)}"
        )

@router.get("/parameters", response_model=List[ProcessParameter])
async def get_available_parameters(process_type: str = Query(..., description="Type of manufacturing process")) -> Any:
    """
    Get available parameters for a specific manufacturing process type.
    """
    try:
        parameters = sim_engine.get_parameters(process_type)
        return parameters
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Process type not found: {str(e)}"
        )

@router.get("/process-types", response_model=List[str])
async def get_available_process_types() -> Any:
    """
    Get list of available manufacturing process types.
    """
    try:
        process_types = sim_engine.get_process_types()
        return process_types
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve process types: {str(e)}"
        )
