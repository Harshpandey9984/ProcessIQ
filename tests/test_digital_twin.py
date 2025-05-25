"""
Tests for digital twin endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

# Helper function to get auth token for tests
def get_auth_token():
    """Get a valid auth token for testing."""
    response = client.post(
        "/api/auth/login",
        data={"username": "user@example.com", "password": "password"}
    )
    return response.json()["access_token"]

def test_create_digital_twin_authenticated():
    """Test creating a digital twin when authenticated."""
    token = get_auth_token()
    
    # Sample digital twin configuration
    config = {
        "name": "Test Production Line",
        "description": "A test digital twin for automated testing",
        "process_type": "assembly_line",
        "parameters": {
            "throughput": 100,
            "cycle_time": 60,
            "defect_rate": 0.02,
            "energy_consumption": 500
        },
        "data_sources": [
            {"type": "sensor", "id": "temp_sensor_1", "data_format": "json"},
            {"type": "database", "id": "production_db", "table": "metrics"}
        ]
    }
    
    response = client.post(
        "/api/digital-twin/create",
        json=config,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["name"] == config["name"]
    assert data["status"] == "created"

def test_create_digital_twin_unauthenticated():
    """Test creating a digital twin when unauthenticated."""
    config = {
        "name": "Test Production Line",
        "description": "A test digital twin for automated testing",
        "process_type": "assembly_line",
        "parameters": {}
    }
    
    response = client.post(
        "/api/digital-twin/create",
        json=config
    )
    
    assert response.status_code == 401

def test_get_digital_twin():
    """Test getting a digital twin that exists."""
    token = get_auth_token()
    
    # First create a digital twin
    config = {
        "name": "Test Production Line",
        "description": "A test digital twin for automated testing",
        "process_type": "assembly_line",
        "parameters": {"throughput": 100}
    }
    
    create_response = client.post(
        "/api/digital-twin/create",
        json=config,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    twin_id = create_response.json()["id"]
    
    # Now retrieve the digital twin
    response = client.get(
        f"/api/digital-twin/{twin_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == twin_id
    assert data["name"] == config["name"]

def test_get_nonexistent_digital_twin():
    """Test getting a digital twin that doesn't exist."""
    token = get_auth_token()
    
    response = client.get(
        "/api/digital-twin/nonexistent-id",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 404

def test_run_scenario():
    """Test running a what-if scenario on a digital twin."""
    token = get_auth_token()
    
    # First create a digital twin
    config = {
        "name": "Test Production Line",
        "description": "A test digital twin for automated testing",
        "process_type": "assembly_line",
        "parameters": {
            "throughput": 100,
            "cycle_time": 60,
            "defect_rate": 0.02,
            "energy_consumption": 500
        }
    }
    
    create_response = client.post(
        "/api/digital-twin/create",
        json=config,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    twin_id = create_response.json()["id"]
    
    # Run a what-if scenario
    scenario = {
        "name": "Increased Throughput",
        "description": "Test scenario with increased throughput",
        "parameters": {
            "throughput": 120,
            "cycle_time": 50
        },
        "duration": 3600  # 1 hour simulation
    }
    
    response = client.post(
        f"/api/digital-twin/{twin_id}/scenarios",
        json=scenario,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "scenario_id" in data
    assert "results" in data
    assert len(data["results"]) > 0
