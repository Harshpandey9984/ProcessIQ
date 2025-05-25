"""
Schemas for simulation data models.
"""

from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field


class ProcessParameter(BaseModel):
    """Parameter for manufacturing process simulation."""
    name: str
    description: str
    unit: str
    min_value: float
    max_value: float
    default_value: float
    impact_factors: Dict[str, float] = Field(
        default_factory=dict,
        description="Dictionary of output variables and their sensitivity to this parameter"
    )


class SimulationConfig(BaseModel):
    """Configuration for running a manufacturing process simulation."""
    process_type: str = Field(..., description="Type of manufacturing process")
    duration: float = Field(..., description="Simulation duration in seconds")
    parameters: Dict[str, float] = Field(..., description="Process parameters and their values")
    random_seed: Optional[int] = Field(None, description="Random seed for reproducibility")
    include_sensor_noise: bool = Field(
        default=True,
        description="Whether to include realistic sensor noise in the output"
    )


class SimulationResult(BaseModel):
    """Results from a manufacturing process simulation."""
    simulation_id: str
    process_type: str
    duration: float
    parameters: Dict[str, float]
    timestamps: List[float]
    sensor_readings: Dict[str, List[float]]
    quality_metrics: Dict[str, float]
    energy_consumption: float
    throughput: float
    defect_rate: float
    execution_time: float
