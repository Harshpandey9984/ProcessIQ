"""
Quick test script to verify authentication endpoints.
"""
import requests
import json

BASE_URL = "http://localhost:8001"

def test_health_check():
    """Test the health check endpoint."""
    response = requests.get(f"{BASE_URL}/health")
    print("Health Check Response:", response.status_code)
    print(json.dumps(response.json(), indent=2))
    return response.status_code == 200

def test_login(email="admin@example.com", password="password"):
    """Test user login."""
    print(f"\nTesting login for: {email}")
    url = f"{BASE_URL}/api/auth/token"
    data = {
        "username": email,  # backend expects 'username' not 'email'
        "password": password
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    try:
        response = requests.post(url, data=data, headers=headers)
        print("Login Response:", response.status_code)
        if response.status_code == 200:
            print("Login successful!")
            user_data = response.json()
            print(f"User: {user_data['user']['full_name']}")
            print(f"Role: {user_data['user']['role']}")
            print(f"Token Type: {user_data['token_type']}")
            return True
        else:
            print("Login failed")
            print("Response:", response.text)
            return False
    except Exception as e:
        print(f"Error during login: {e}")
        return False

def test_register(email="newuser@example.com", password="password123"):
    """Test user registration."""
    print(f"\nTesting registration for: {email}")
    url = f"{BASE_URL}/api/auth/register"
    data = {
        "email": email,
        "password": password,
        "full_name": "New Test User"
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        print("Register Response:", response.status_code)
        if response.status_code == 200:
            print("Registration successful!")
            print(json.dumps(response.json(), indent=2))
            return True
        else:
            print("Registration failed")
            print("Response:", response.text)
            return False
    except Exception as e:
        print(f"Error during registration: {e}")
        return False

if __name__ == "__main__":
    print("=== Testing Digital Twin Platform API ===")
    
    if test_health_check():
        print("\n✅ Health check passed\n")
    else:
        print("\n❌ Health check failed\n")
        exit(1)
        
    if test_login():
        print("\n✅ Login test passed\n")
    else:
        print("\n❌ Login test failed\n")
    
    if test_register():
        print("\n✅ Registration test passed\n")
    else:
        print("\n❌ Registration test failed\n")
    
    # Now test login with the newly registered user
    if test_login(email="newuser@example.com", password="password123"):
        print("\n✅ Login with new user passed\n")
    else:
        print("\n❌ Login with new user failed\n")
