"""
Test script to debug the authentication issue with detailed logging.
"""
import requests
import json
import sys

# Configuration
BASE_URL = "http://localhost:8001"  # Backend URL
API_ENDPOINT = "/api/auth/token"     # Authentication endpoint
PROTECTED_ENDPOINT = "/api/digital-twin/list"  # Protected endpoint for testing
TEST_CREDENTIALS = {
    "username": "admin@example.com",
    "password": "password"
}

def print_section(title):
    """Print a section header."""
    print("\n" + "="*50)
    print(title)
    print("="*50)

def test_health():
    """Test if the backend is up and running."""
    print_section("Testing Backend Health")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_direct_login():
    """Test login with direct requests to the backend."""
    print_section("Testing Direct Login")
    
    # Create form data exactly as FastAPI expects for OAuth2PasswordRequestForm
    data = {
        "username": TEST_CREDENTIALS["username"],
        "password": TEST_CREDENTIALS["password"],
        "grant_type": "password",
        "scope": "",
        "client_id": "",
        "client_secret": ""
    }
    
    print(f"Request URL: {BASE_URL}{API_ENDPOINT}")
    print(f"Request data: {json.dumps(data, indent=2)}")
    
    try:
        # Send POST request with form-urlencoded data
        response = requests.post(
            f"{BASE_URL}{API_ENDPOINT}", 
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        print(f"Status code: {response.status_code}")
        
        # Check if request was successful
        if response.status_code == 200:
            print("Login successful!")
            result = response.json()
            print(f"Token type: {result.get('token_type')}")
            print(f"Access token: {result.get('access_token')[:20]}...")
            print(f"User: {json.dumps(result.get('user'), indent=2)}")
            return True
        else:
            print(f"Login failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_authentication_flow():
    """Test the complete authentication flow."""
    print_section("Testing Authentication Flow")
    
    # First, try to make a request that requires authentication
    print("1. Attempting to access protected endpoint without token...")
    try:
        response = requests.get(f"{BASE_URL}{PROTECTED_ENDPOINT}")
        print(f"Status code: {response.status_code}")
        if response.status_code == 401:
            print("Correctly received 401 Unauthorized")
        else:
            print(f"Unexpected status: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Now login to get a token
    print("\n2. Logging in to get authentication token...")
    try:
        # Create form data exactly as FastAPI expects for OAuth2PasswordRequestForm
        login_data = {
            "username": TEST_CREDENTIALS["username"],
            "password": TEST_CREDENTIALS["password"],
            "grant_type": "password",
            "scope": "",
            "client_id": "",
            "client_secret": ""
        }
        
        login_response = requests.post(
            f"{BASE_URL}{API_ENDPOINT}", 
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            token = token_data.get("access_token")
            print(f"Token received: {token[:20]}...")
            
            # Try accessing protected endpoint with token
            print("\n3. Accessing protected endpoint with token...")
            auth_response = requests.get(
                f"{BASE_URL}{PROTECTED_ENDPOINT}",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            print(f"Status code: {auth_response.status_code}")
            if auth_response.status_code == 200:
                print("Successfully accessed protected endpoint!")
                print(f"Response: {json.dumps(auth_response.json()[:1], indent=2)}")
                return True
            else:
                print(f"Failed to access protected endpoint: {auth_response.text}")
                return False
        else:
            print(f"Login failed: {login_response.text}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Authentication Debugging Tool")
    print("----------------------------\n")
    
    # Test if backend is running
    if not test_health():
        print("\n❌ Backend is not responding. Make sure it's running on port 8001.")
        sys.exit(1)
    
    # Test direct login
    if not test_direct_login():
        print("\n❌ Direct login test failed.")
    else:
        print("\n✅ Direct login test passed!")
    
    # Test authentication flow
    if not test_authentication_flow():
        print("\n❌ Authentication flow test failed.")
    else:
        print("\n✅ Authentication flow test passed!")
