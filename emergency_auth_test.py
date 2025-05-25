"""
Emergency authentication test script to directly test the simplified fixed backend.
"""

import requests
import json
import sys

# Configuration
BASE_URL = "http://localhost:8001"
AUTH_ENDPOINT = "/api/auth/token"
TEST_CREDENTIALS = [
    {"email": "admin@example.com", "password": "password"},
    {"email": "user@example.com", "password": "password"}
]

def print_header(text):
    """Print a header with nice formatting."""
    print("\n" + "="*50)
    print(text)
    print("="*50)

def test_server_health():
    """Test if the server is up and running."""
    print_header("TESTING SERVER HEALTH")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print(f"Response: {response.json()}")
            print("\nServer is healthy and responding!")
            return True
        else:
            print(f"Failed health check: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return False

def get_auth_debug_info():
    """Get authentication debug information."""
    print_header("CHECKING AUTH DEBUG INFO")
    
    try:
        response = requests.get(f"{BASE_URL}/debug/auth", timeout=5)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"Failed to get auth debug info: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return False

def test_login(email, password):
    """Test login with provided credentials."""
    print_header(f"TESTING LOGIN: {email}")
    
    try:
        # Create form data for login
        data = {
            "username": email,  # Backend expects "username", not "email"
            "password": password
        }
        
        # Add detailed request information
        print(f"Request URL: {BASE_URL}{AUTH_ENDPOINT}")
        print(f"Request Method: POST")
        print(f"Request Headers: Content-Type=application/x-www-form-urlencoded")
        print(f"Request Body: username={email}&password=[HIDDEN]")
        
        # Send the login request
        response = requests.post(
            f"{BASE_URL}{AUTH_ENDPOINT}",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10
        )
        
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            token = result.get("access_token", "")
            user_info = result.get("user", {})
            
            print("\nLOGIN SUCCESSFUL!")
            print(f"Token: {token[:20]}...")
            print(f"User Email: {user_info.get('email')}")
            print(f"User Role: {user_info.get('role')}")
            return True
        else:
            print("\nLOGIN FAILED!")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")
        return False

def run_tests():
    """Run the complete test suite."""
    print_header("EMERGENCY AUTHENTICATION TEST")
    print(f"Backend URL: {BASE_URL}")
    print(f"Current time: {requests.get(f'{BASE_URL}/health').json().get('timestamp')}")
    
    # Test 1: Check if server is healthy
    if not test_server_health():
        print("\nServer health check failed. Please ensure the backend is running.")
        return False
        
    # Test 2: Get auth debug info
    get_auth_debug_info()
        
    # Test 3: Test login with each set of credentials
    results = []
    
    for cred in TEST_CREDENTIALS:
        result = test_login(cred["email"], cred["password"])
        results.append({
            "email": cred["email"],
            "success": result
        })
    
    # Show summary
    print_header("TEST RESULTS SUMMARY")
    
    all_passed = True
    for result in results:
        status = "✓ PASSED" if result["success"] else "✗ FAILED"
        print(f"{result['email']}: {status}")
        if not result["success"]:
            all_passed = False
    
    if all_passed:
        print("\nAll authentication tests passed! The system is working correctly.")
    else:
        print("\nSome authentication tests failed. Please check the detailed output above.")
    
    return all_passed

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
