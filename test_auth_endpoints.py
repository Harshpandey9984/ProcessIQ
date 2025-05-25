"""
Test script to verify authentication endpoints.
"""
import requests
import json

def test_login():
    """Test login endpoint."""
    print("Testing login endpoint...")
    url = "http://localhost:8001/api/auth/token"
    
    # Form data for login
    data = {
        "username": "admin@example.com",
        "password": "password"
    }
    
    # Make the request
    response = requests.post(url, data=data)
    
    # Print results
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        print("Login successful!")
        print(json.dumps(response.json(), indent=2))
    else:
        print("Login failed.")
        print(response.text)

def test_registration():
    """Test registration endpoint."""
    print("\nTesting registration endpoint...")
    url = "http://localhost:8001/api/auth/register"
    
    # JSON data for registration
    data = {
        "email": "newuser@example.com",
        "password": "password123",
        "full_name": "New Test User",
        "company": "Test Company"
    }
    
    # Make the request
    response = requests.post(url, json=data)
    
    # Print results
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        print("Registration successful!")
        print(json.dumps(response.json(), indent=2))
    else:
        print("Registration failed.")
        print(response.text)

if __name__ == "__main__":
    test_login()
    test_registration()
