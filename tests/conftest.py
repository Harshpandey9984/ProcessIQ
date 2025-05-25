"""
PyTest configuration file with fixtures.
"""

import os
import sys
import pytest
from fastapi.testclient import TestClient

# Add the parent directory to sys.path to allow imports from the app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app

@pytest.fixture
def client():
    """
    Create a test client for the FastAPI application.
    """
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def auth_headers():
    """
    Get authorization headers with a valid token.
    """
    client = TestClient(app)
    response = client.post(
        "/api/auth/login",
        data={"username": "user@example.com", "password": "password"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def admin_auth_headers():
    """
    Get authorization headers with a valid admin token.
    """
    client = TestClient(app)
    response = client.post(
        "/api/auth/login",
        data={"username": "admin@example.com", "password": "password"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
