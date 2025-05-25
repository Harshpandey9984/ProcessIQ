"""
Fixed Authentication Direct Test
A simple tool to test the authentication directly from the command line
"""
import requests
import sys
import json
from datetime import datetime

def print_with_timestamp(message):
    """Print a message with timestamp."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def check_server_status():
    """Check if the server is running and healthy."""
    print_with_timestamp("Checking server status...")
    try:
        response = requests.get("http://localhost:8001/health")
        if response.status_code == 200:
            data = response.json()
            print_with_timestamp(f"Server is healthy! Status: {data['status']}")
            return True
        else:
            print_with_timestamp(f"Server returned status code: {response.status_code}")
            return False
    except Exception as e:
        print_with_timestamp(f"Failed to connect to server: {str(e)}")
        return False

def check_auth_debug():
    """Check auth debug endpoint."""
    print_with_timestamp("Checking auth debug...")
    try:
        response = requests.get("http://localhost:8001/debug/auth")
        if response.status_code == 200:
            data = response.json()
            print_with_timestamp("Authentication config:")
            print(json.dumps(data, indent=2))
            return True
        else:
            print_with_timestamp(f"Auth debug failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print_with_timestamp(f"Failed to check auth debug: {str(e)}")
        return False

def test_login(username="admin@example.com", password="password"):
    """Test login functionality."""
    print_with_timestamp(f"Testing login with {username}...")
    try:
        data = {
            "username": username,
            "password": password
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        response = requests.post(
            "http://localhost:8001/api/auth/token",
            data=data,
            headers=headers
        )
        
        if response.status_code == 200:
            print_with_timestamp("Login successful!")
            result = response.json()
            print_with_timestamp(f"Token type: {result.get('token_type')}")
            print_with_timestamp(f"User: {result.get('user').get('email')}")
            print_with_timestamp(f"Role: {result.get('user').get('role')}")
            return result.get("access_token")
        else:
            print_with_timestamp(f"Login failed with status code: {response.status_code}")
            print_with_timestamp(f"Response: {response.text}")
            return None
    except Exception as e:
        print_with_timestamp(f"Login error: {str(e)}")
        return None

def test_protected_endpoint(token):
    """Test accessing a protected endpoint."""
    print_with_timestamp("Testing protected endpoint access...")
    try:
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.get(
            "http://localhost:8001/api/digital-twin",
            headers=headers
        )
        
        if response.status_code == 200:
            print_with_timestamp("Protected endpoint access successful!")
            data = response.json()
            print_with_timestamp(f"Retrieved {len(data)} digital twins")
            return True
        else:
            print_with_timestamp(f"Protected endpoint access failed with status code: {response.status_code}")
            print_with_timestamp(f"Response: {response.text}")
            return False
    except Exception as e:
        print_with_timestamp(f"Protected endpoint error: {str(e)}")
        return False

def main():
    """Run the authentication test."""
    print("\n=== FIXED AUTHENTICATION DIRECT TEST ===\n")
    
    # Step 1: Check server status
    if not check_server_status():
        print_with_timestamp("Server check failed. Please start the server and try again.")
        sys.exit(1)
    
    # Step 2: Check auth debug
    check_auth_debug()
    
    # Step 3: Test login
    token = test_login()
    if not token:
        print_with_timestamp("Login failed. Cannot proceed to protected endpoint test.")
        sys.exit(1)
    
    # Step 4: Test protected endpoint
    test_protected_endpoint(token)
    
    print("\n=== TEST COMPLETE ===\n")

if __name__ == "__main__":
    main()
