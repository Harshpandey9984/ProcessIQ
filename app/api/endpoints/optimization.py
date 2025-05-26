"""
API endpoints for optimization operations.
"""

from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, Query, Body

from app.optimization.optimizer import ProcessOptimizer
from app.models.schemas.optimization import (
    OptimizationRequest, 
    OptimizationResult, 
    OptimizationConfig,
    OptimizationConstraint
)

router = APIRouter()

optimizer = ProcessOptimizer()

@router.post("/parameters", response_model=OptimizationResult)
async def optimize_parameters(request: OptimizationRequest) -> Any:
    """
    Optimize process parameters based on the provided configuration and constraints.
    """
    try:
        result = optimizer.optimize_parameters(request)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Optimization failed: {str(e)}"
        )

@router.post("/schedule", response_model=Dict[str, Any])
async def optimize_schedule(
    process_id: int = Query(..., description="ID of the manufacturing process"),
    config: OptimizationConfig = Body(..., description="Optimization configuration")
) -> Any:
    """
    Optimize production schedule for a specific manufacturing process.
    """
    try:
        result = optimizer.optimize_schedule(process_id, config)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Schedule optimization failed: {str(e)}"
        )

@router.get("/algorithms", response_model=List[str])
async def get_available_algorithms(
    optimization_type: str = Query(..., description="Type of optimization to perform")
) -> Any:
    """
    Get available optimization algorithms for a specific optimization type.
    """
    try:
        algorithms = optimizer.get_algorithms(optimization_type)
        return algorithms
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Optimization type not found: {str(e)}"
        )

@router.post("/multi-objective", response_model=List[OptimizationResult])
async def multi_objective_optimization(
    request: OptimizationRequest,
    num_solutions: int = Query(5, description="Number of Pareto-optimal solutions to return")
) -> Any:
    """
    Perform multi-objective optimization and return Pareto-optimal solutions.
    """
    try:
        results = optimizer.multi_objective_optimization(request, num_solutions)
        return results
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Multi-objective optimization failed: {str(e)}"
        )
