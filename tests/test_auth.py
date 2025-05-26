"""
Tests for authentication endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from jose import jwt

from app.main import app
from app.api.endpoints.auth import SECRET_KEY, ALGORITHM

client = TestClient(app)

def test_login_valid_credentials():
    """Test login with valid credentials."""
    response = client.post(
        "/api/auth/login",
        data={"username": "user@example.com", "password": "password"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "user" in data
    assert data["user"]["email"] == "user@example.com"

def test_login_invalid_credentials():
    """Test login with invalid credentials."""
    response = client.post(
        "/api/auth/login",
        data={"username": "user@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "detail" in response.json()

def test_user_me_authenticated():
    """Test get current user profile when authenticated."""
    # First login to get token
    login_response = client.post(
        "/api/auth/login",
        data={"username": "user@example.com", "password": "password"}
    )
    token = login_response.json()["access_token"]
    
    # Use token to get profile
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "user@example.com"

def test_user_me_unauthenticated():
    """Test get current user profile when unauthenticated."""
    response = client.get("/api/auth/me")
    assert response.status_code == 401

def test_register_new_user():
    """Test registering a new user."""
    new_user = {
        "email": "newuser@example.com",
        "password": "securepass",
        "full_name": "New User",
        "company": "Test Company",
        "role": "user"
    }
    response = client.post(
        "/api/auth/register",
        json=new_user
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == new_user["email"]
    assert data["full_name"] == new_user["full_name"]
    assert "id" in data

def test_register_existing_email():
    """Test registering with an email that already exists."""
    existing_user = {
        "email": "user@example.com",  # This email already exists
        "password": "securepass",
        "full_name": "Duplicate User",
        "company": "Test Company",
        "role": "user"
    }
    response = client.post(
        "/api/auth/register",
        json=existing_user
    )
    assert response.status_code == 400
    assert "detail" in response.json()

def test_token_validation():
    """Test that generated tokens are valid JWT tokens."""
    login_response = client.post(
        "/api/auth/login",
        data={"username": "user@example.com", "password": "password"}
    )
    token = login_response.json()["access_token"]
    
    # Decode token and verify contents
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert "sub" in payload
    assert payload["sub"] == "user@example.com"
    assert "exp" in payload
