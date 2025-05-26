"""
Authentication verification script for Digital Twin Platform.
This script tests the authentication endpoints to ensure they're working correctly.
"""

import requests
import sys
import json
from datetime import datetime

BASE_URL = "http://localhost:8001"
LOG_FILE = "logs/verification_results.log"

def log_message(message):
    """Log a message to both console and file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"{timestamp} - {message}"
    print(log_line)
    
    with open(LOG_FILE, "a") as f:
        f.write(log_line + "\n")

def test_health():
    """Test the health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        log_message(f"Health check: {response.status_code}")
        if response.status_code == 200:
            log_message(f"Health response: {response.json()}")
            return True
        return False
    except Exception as e:
        log_message(f"Health check failed: {str(e)}")
        return False

def test_auth_debug():
    """Test the auth debug endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/debug/auth")
        log_message(f"Auth debug check: {response.status_code}")
        if response.status_code == 200:
            log_message(f"Auth debug response: {json.dumps(response.json(), indent=2)}")
            return True
        return False
    except Exception as e:
        log_message(f"Auth debug check failed: {str(e)}")
        return False

def test_login(email="admin@example.com", password="password"):
    """Test the login endpoint"""
    try:
        # Create form data for login
        data = {
            "username": email,
            "password": password
        }
        
        log_message(f"Attempting login with: {email} / {password}")
        
        # Send the login request
        response = requests.post(
            f"{BASE_URL}/api/auth/token",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        log_message(f"Login response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            log_message("Login successful!")
            log_message(f"Token type: {result.get('token_type')}")
            log_message(f"User: {result.get('user', {}).get('email')}")
            log_message(f"User role: {result.get('user', {}).get('role')}")
            # Return the token
            return result.get("access_token")
        else:
            log_message(f"Login failed: {response.text}")
            return None
            
    except Exception as e:
        log_message(f"Login request failed: {str(e)}")
        return None

def test_protected_endpoint(token):
    """Test access to a protected endpoint"""
    if not token:
        log_message("No token provided, skipping protected endpoint test")
        return False
        
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/digital-twin", headers=headers)
        log_message(f"Protected endpoint status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            log_message(f"Retrieved {len(data)} digital twins")
            return True
        else:
            log_message(f"Failed to access protected endpoint: {response.text}")
            return False
    except Exception as e:
        log_message(f"Protected endpoint request failed: {str(e)}")
        return False

def run_verification():
    """Run the full verification process"""
    log_message("==== Starting Authentication Verification ====")
    
    # Step 1: Check server health
    log_message("\n-- Testing Server Health --")
    if not test_health():
        log_message("❌ Health check failed - exiting")
        return False
    log_message("✅ Health check passed")
    
    # Step 2: Check auth debug endpoint
    log_message("\n-- Testing Auth Debug Endpoint --")
    if not test_auth_debug():
        log_message("❌ Auth debug endpoint check failed")
    else:
        log_message("✅ Auth debug endpoint check passed")
    
    # Step 3: Test admin login
    log_message("\n-- Testing Admin Login --")
    admin_token = test_login("admin@example.com", "password")
    if not admin_token:
        log_message("❌ Admin login failed - exiting")
        return False
    log_message("✅ Admin login successful")
    
    # Step 4: Test user login
    log_message("\n-- Testing User Login --")
    user_token = test_login("user@example.com", "password")
    if not user_token:
        log_message("❌ User login failed")
    else:
        log_message("✅ User login successful")
    
    # Step 5: Test protected endpoint with admin token
    log_message("\n-- Testing Protected Endpoint Access --")
    if test_protected_endpoint(admin_token):
        log_message("✅ Protected endpoint access successful")
    else:
        log_message("❌ Protected endpoint access failed")
    
    log_message("\n==== Authentication Verification Complete ====")
    log_message("✅ All critical tests passed!")
    return True

if __name__ == "__main__":
    # Create log directory if it doesn't exist
    import os
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    # Run verification
    success = run_verification()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
