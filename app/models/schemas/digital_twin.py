"""
Schemas for digital twin data models.
"""

from typing import Dict, List, Optional, Union, Any
from pydantic import BaseModel, Field
from datetime import datetime


class DigitalTwinConfig(BaseModel):
    """Configuration for creating a digital twin."""
    name: str = Field(..., description="Name of the digital twin")
    process_type: str = Field(..., description="Type of manufacturing process")
    description: Optional[str] = None
    parameters: Dict[str, float] = Field(..., description="Initial process parameters")
    update_frequency: float = Field(1.0, description="Update frequency in Hz")
    simulation_speed_factor: float = Field(
        1.0, 
        description="Speed factor for simulation (e.g., 2.0 runs twice as fast as real-time)"
    )
    include_random_events: bool = Field(
        True,
        description="Whether to include random events like failures or disruptions"
    )
    created_by: Optional[str] = Field(None, description="ID of the user who created the digital twin")
    data_sources: Optional[List[Dict[str, Any]]] = Field(
        None, description="Data sources for the digital twin"
    )


class DigitalTwinStatus(BaseModel):
    """Status of a digital twin."""
    id: str = Field(..., description="Unique identifier for the digital twin")
    name: str
    process_type: str
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None
    status: str = "created"
    created_at: str
    status: str  # "initializing", "running", "paused", "error", "terminated"
    current_time: float
    uptime: float
    current_parameters: Dict[str, float]
    current_metrics: Dict[str, float]
    last_updated: str


class DigitalTwinData(BaseModel):
    """Data from a digital twin for a specific time period."""
    twin_id: str
    process_type: str
    start_time: float
    end_time: float
    timestamps: List[float]
    parameters: Dict[str, List[float]]
    sensor_readings: Dict[str, List[float]]
    quality_metrics: Dict[str, List[float]]
    events: List[Dict[str, Any]]  # List of events that occurred during the period


class ScenarioConfig(BaseModel):
    """Configuration for running a what-if scenario on a digital twin."""
    name: str = Field(..., description="Name of the scenario")
    parameter_changes: Dict[str, float] = Field(
        ..., description="Parameter changes to apply"
    )
    duration: float = Field(..., description="Duration to run the scenario in seconds")
    start_from_current_state: bool = Field(
        True,
        description="Whether to start from the current state or from a reset state"
    )
    random_seed: Optional[int] = Field(None, description="Random seed for reproducibility")


class ScenarioResult(BaseModel):
    """Result of a what-if scenario run on a digital twin."""
    scenario_id: str
    twin_id: str
    name: str
    start_time: float
    end_time: float
    parameter_changes: Dict[str, float]
    baseline_metrics: Dict[str, float]
    scenario_metrics: Dict[str, float]
    impact_analysis: Dict[str, float]  # Percentage changes in key metrics
    timestamps: List[float]
    time_series_data: Dict[str, List[float]]
    execution_time: float
