"""
Schemas for optimization data models.
"""

from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field


class OptimizationConstraint(BaseModel):
    """Constraint for optimization."""
    parameter: str = Field(..., description="Parameter or output variable name")
    min_value: Optional[float] = Field(None, description="Minimum allowed value")
    max_value: Optional[float] = Field(None, description="Maximum allowed value")
    equals_value: Optional[float] = Field(None, description="Required exact value")
    weight: float = Field(1.0, description="Weight for soft constraints")
    is_hard_constraint: bool = Field(
        default=True, 
        description="If True, constraint must be satisfied; if False, it's a preference"
    )


class OptimizationConfig(BaseModel):
    """Configuration for optimization algorithms."""
    algorithm: str = Field(..., description="Optimization algorithm to use")
    max_iterations: int = Field(100, description="Maximum number of iterations")
    tolerance: float = Field(0.001, description="Convergence tolerance")
    exploration_rate: float = Field(0.1, description="Exploration rate for RL-based methods")
    use_intel_optimizations: bool = Field(True, description="Whether to use Intel-optimized algorithms")


class OptimizationRequest(BaseModel):
    """Request for parameter optimization."""
    process_type: str = Field(..., description="Type of manufacturing process")
    target_variable: str = Field(..., description="Variable to optimize")
    maximize: bool = Field(True, description="If True, maximize target; if False, minimize")
    parameters_to_optimize: List[str] = Field(..., description="List of parameters to optimize")
    fixed_parameters: Dict[str, float] = Field(
        default_factory=dict,
        description="Parameters to keep fixed at specified values"
    )
    constraints: List[OptimizationConstraint] = Field(
        default_factory=list,
        description="Constraints on parameters or output variables"
    )
    config: OptimizationConfig


class OptimizedParameter(BaseModel):
    """Optimized parameter value."""
    name: str
    value: float
    original_value: Optional[float] = None
    unit: str
    improvement_percent: Optional[float] = None


class OptimizationResult(BaseModel):
    """Result of an optimization run."""
    optimization_id: str
    process_type: str
    target_variable: str
    initial_value: float
    optimized_value: float
    improvement_percent: float
    parameters: List[OptimizedParameter]
    expected_quality_impact: Dict[str, float]
    expected_energy_impact: float
    expected_throughput_impact: float
    confidence_score: float
    execution_time: float
