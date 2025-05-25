"""
Final Verification Tool for Digital Twin Platform Authentication
This script performs a comprehensive test of all authentication components.
"""
import requests
import json
import time
import sys
import os
from datetime import datetime

# Configure logging to file
LOG_FILE = "logs/verification_results.log"
os.makedirs("logs", exist_ok=True)

# Configuration
BACKEND_URL = "http://localhost:8001"
FRONTEND_URL = "http://localhost:3000"
TEST_CREDENTIALS = {
    "username": "admin@example.com",
    "password": "password"
}

def log_message(message):
    """Log a message to both console and file."""
    print(message)
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")

def print_header(title):
    """Print a section header."""
    header = "\n" + "="*60
    header += f"\n {title}"
    header += "\n" + "="*60
    log_message(header)

def print_result(success, message):
    """Print a test result."""
    mark = "✓" if success else "✗"
    status = "SUCCESS" if success else "FAILED"
    log_message(f"[{mark}] {status}: {message}")

def perform_test(name, test_func, *args):
    """Perform a test and print the result."""
    log_message(f"\n▶ Testing: {name}...")
    try:
        result, message = test_func(*args)
        print_result(result, message)
        return result
    except Exception as e:
        print_result(False, f"Exception occurred: {str(e)}")
        return False

def test_backend_health():
    """Test if the backend server is running and healthy."""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return response.status_code == 200, f"Backend is running (status {response.status_code})"
    except:
        return False, "Backend is not running or not reachable"

def test_frontend_connectivity():
    """Test if the frontend server is running."""
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        return response.status_code == 200, f"Frontend is running (status {response.status_code})"
    except:
        return False, "Frontend is not running or not reachable"

def test_login_endpoint():
    """Test the login endpoint directly."""
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/auth/token",
            data=TEST_CREDENTIALS,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if "access_token" in data and "user" in data:
                return True, f"Login successful, token received for user: {data['user'].get('email')}"
            else:
                return False, "Login response missing token or user data"
        else:
            return False, f"Login failed with status code: {response.status_code}, {response.text}"
    except Exception as e:
        return False, f"Login test exception: {str(e)}"

def test_protected_endpoint(token=None):
    """Test access to a protected endpoint."""
    if not token:
        # First, get a token
        try:
            login_response = requests.post(
                f"{BACKEND_URL}/api/auth/token",
                data=TEST_CREDENTIALS,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=5
            )
            if login_response.status_code != 200:
                return False, "Could not obtain token for protected endpoint test"
            token = login_response.json().get("access_token")
        except Exception as e:
            return False, f"Failed to get token: {str(e)}"
    
    # Now try the protected endpoint
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BACKEND_URL}/api/digital-twin", headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            return True, f"Successfully accessed protected endpoint, received {len(data)} items"
        else:
            return False, f"Failed to access protected endpoint: {response.status_code}, {response.text}"
    except Exception as e:
        return False, f"Protected endpoint test exception: {str(e)}"

def test_unauthorized_access():
    """Test that unauthorized access is properly blocked."""
    try:
        response = requests.get(f"{BACKEND_URL}/api/digital-twin", timeout=5)
        if response.status_code == 401:
            return True, "Correctly received 401 Unauthorized for protected endpoint without token"
        else:
            return False, f"Expected 401, but got {response.status_code}"
    except Exception as e:
        return False, f"Unauthorized test exception: {str(e)}"

def run_verification():
    """Run the complete verification suite."""
    # Clear log file
    with open(LOG_FILE, "w") as f:
        f.write("")
    
    print_header("DIGITAL TWIN PLATFORM AUTHENTICATION VERIFICATION")
    log_message(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log_message(f"Backend URL: {BACKEND_URL}")
    log_message(f"Frontend URL: {FRONTEND_URL}")
    
    # Count total tests and successful tests
    total_tests = 0
    passed_tests = 0
    
    # Test server health
    print_header("SERVER CONNECTIVITY TESTS")
    
    result = perform_test("Backend health", test_backend_health)
    total_tests += 1
    if result: passed_tests += 1
    
    result = perform_test("Frontend connectivity", test_frontend_connectivity)
    total_tests += 1
    if result: passed_tests += 1
    
    # Test authentication
    print_header("AUTHENTICATION TESTS")
    
    result = perform_test("Login endpoint", test_login_endpoint)
    total_tests += 1
    if result: passed_tests += 1
    
    if result:
        # Get token for protected endpoint test
        login_response = requests.post(
            f"{BACKEND_URL}/api/auth/token",
            data=TEST_CREDENTIALS,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        token = login_response.json().get("access_token")
        
        result = perform_test("Protected endpoint access", test_protected_endpoint, token)
        total_tests += 1
        if result: passed_tests += 1
    else:
        log_message("Skipping protected endpoint test due to login failure")
    
    result = perform_test("Unauthorized access handling", test_unauthorized_access)
    total_tests += 1
    if result: passed_tests += 1
    
    # Print summary
    print_header("VERIFICATION SUMMARY")
    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    log_message(f"Tests passed: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
    
    if passed_tests == total_tests:
        log_message("\n✅ VERIFICATION SUCCESSFUL: All authentication components are working properly!")
    else:
        log_message("\n⚠️ VERIFICATION INCOMPLETE: Some tests failed, see details above.")

if __name__ == "__main__":
    run_verification()
