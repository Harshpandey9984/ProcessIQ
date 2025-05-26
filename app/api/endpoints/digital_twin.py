"""
API endpoints for digital twin operations.
"""

from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, Query, Body, Depends

from app.simulation.digital_twin import DigitalTwinManager
from app.models.schemas.digital_twin import (
    DigitalTwinConfig, 
    DigitalTwinStatus, 
    DigitalTwinData,
    ScenarioConfig,
    ScenarioResult
)
from app.api.deps import (
    get_current_active_user_dependency,
    require_read,
    require_write,
    require_delete
)

router = APIRouter()

dt_manager = DigitalTwinManager()

# Permission dependencies
current_user_dependency = get_current_active_user_dependency()
read_permission = require_read("digital_twin")
write_permission = require_write("digital_twin")
delete_permission = require_delete("digital_twin")

@router.post("/create", response_model=DigitalTwinStatus)
async def create_digital_twin(
    config: DigitalTwinConfig,
    current_user: Dict = Depends(write_permission)
) -> Any:
    """
    Create a new digital twin for a manufacturing process.
    """
    try:
        # Add user information to the request
        config.created_by = current_user["id"]
        status = dt_manager.create_digital_twin(config)
        return status
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Digital twin creation failed: {str(e)}"
        )

@router.get("/status/{twin_id}", response_model=DigitalTwinStatus)
async def get_digital_twin_status(
    twin_id: str,
    current_user: Dict = Depends(read_permission)
) -> Any:
    """
    Get the current status of a digital twin.
    """
    try:
        status = dt_manager.get_status(twin_id)
        return status
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Digital twin not found: {str(e)}"
        )

@router.get("/data/{twin_id}", response_model=DigitalTwinData)
async def get_digital_twin_data(
    twin_id: str,
    start_time: float = Query(None, description="Start timestamp for data retrieval"),
    end_time: float = Query(None, description="End timestamp for data retrieval"),
    current_user: Dict = Depends(read_permission)
) -> Any:
    """
    Get data from a digital twin for a specific time period.
    """
    try:
        data = dt_manager.get_data(twin_id, start_time, end_time)
        return data
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve digital twin data: {str(e)}"
        )

@router.post("/scenario/{twin_id}", response_model=ScenarioResult)
async def run_what_if_scenario(
    twin_id: str,
    scenario: ScenarioConfig = Body(..., description="What-if scenario configuration"),
    current_user: Dict = Depends(write_permission)
) -> Any:
    """
    Run a what-if scenario on a digital twin.
    """
    try:
        result = dt_manager.run_scenario(twin_id, scenario)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Scenario simulation failed: {str(e)}"
        )

@router.get("/list", response_model=List[Dict[str, Any]])
async def list_digital_twins(
    current_user: Dict = Depends(read_permission)
) -> Any:
    """
    List all available digital twins.
    """
    try:
        twins = dt_manager.list_twins()
        return twins
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list digital twins: {str(e)}"
        )

@router.delete("/{twin_id}", response_model=Dict[str, str])
async def delete_digital_twin(
    twin_id: str,
    current_user: Dict = Depends(delete_permission)
) -> Any:
    """
    Delete a digital twin.
    """
    try:
        dt_manager.delete_twin(twin_id)
        return {"status": "success", "message": f"Digital twin {twin_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Digital twin not found or deletion failed: {str(e)}"
        )
