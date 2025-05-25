"""
Test script to verify authentication endpoints with detailed debugging.
"""
import requests
import json
import logging
from urllib.parse import urlencode

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_server_health():
    """Test if the server is running"""
    logger.info("Testing server health...")
    try:
        response = requests.get("http://localhost:8001/health")
        logger.info(f"Server health response: {response.status_code} - {response.text}")
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Server health check failed: {str(e)}")
        return False

def test_login():
    """Test login endpoint with detailed logging."""
    logger.info("Testing login endpoint...")
    url = "http://localhost:8001/api/auth/token"
    
    # Form data for login - this should match the format expected by OAuth2PasswordRequestForm
    data = {
        "username": "admin@example.com",
        "password": "password"
    }
    
    # Log request details
    logger.info(f"Login URL: {url}")
    logger.info(f"Login data: {data}")
    
    try:
        # Set correct content type for form data
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        }
        logger.info(f"Request headers: {headers}")
        
        # Make request with form-encoded data
        response = requests.post(url, data=data, headers=headers)
        
        # Log response details
        logger.info(f"Login response status code: {response.status_code}")
        logger.info(f"Login response headers: {dict(response.headers)}")
        
        try:
            response_json = response.json()
            logger.info(f"Login response JSON: {json.dumps(response_json, indent=2)}")
        except:
            logger.info(f"Login response text: {response.text}")
            
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Login request failed: {str(e)}")
        return False

def test_registration():
    """Test registration endpoint with detailed logging."""
    logger.info("Testing registration endpoint...")
    url = "http://localhost:8001/api/auth/register"
    
    # JSON data for registration
    data = {
        "email": "testuser@example.com",
        "password": "password123",
        "full_name": "Test User",
        "company": "Test Company"
    }
    
    # Log request details
    logger.info(f"Registration URL: {url}")
    logger.info(f"Registration data: {data}")
    
    try:
        # Set correct content type for JSON data
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        logger.info(f"Request headers: {headers}")
        
        # Make request with JSON data
        response = requests.post(url, json=data, headers=headers)
        
        # Log response details
        logger.info(f"Registration response status code: {response.status_code}")
        logger.info(f"Registration response headers: {dict(response.headers)}")
        
        try:
            response_json = response.json()
            logger.info(f"Registration response JSON: {json.dumps(response_json, indent=2)}")
        except:
            logger.info(f"Registration response text: {response.text}")
            
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Registration request failed: {str(e)}")
        return False

def test_with_direct_http():
    """Test login using direct HTTP connection."""
    logger.info("Testing login using direct HTTP connection...")
    
    import http.client
    
    try:
        # Create form data
        form_data = urlencode({
            'username': 'admin@example.com',
            'password': 'password'
        })
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        }
        
        logger.info(f"Direct HTTP request to localhost:8001")
        logger.info(f"Path: /api/auth/token")
        logger.info(f"Headers: {headers}")
        logger.info(f"Form data: {form_data}")
        
        # Create connection
        conn = http.client.HTTPConnection("localhost", 8001)
        conn.request("POST", "/api/auth/token", form_data, headers)
        
        # Get response
        response = conn.getresponse()
        logger.info(f"Response status: {response.status} {response.reason}")
        
        # Read and log response data
        data = response.read()
        logger.info(f"Response data: {data.decode('utf-8')}")
        
        conn.close()
        return response.status == 200
    except Exception as e:
        logger.error(f"Direct HTTP request failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("====== Digital Twin Platform Auth Tests ======")
    
    # First check if the server is healthy
    if not test_server_health():
        print("❌ Server health check failed - make sure the backend is running")
        exit(1)
    
    print("\n=== Testing Login ===")
    login_success = test_login()
    print(f"{'✅ Login test passed' if login_success else '❌ Login test failed'}")
    
    print("\n=== Testing Registration ===")
    registration_success = test_registration()
    print(f"{'✅ Registration test passed' if registration_success else '❌ Registration test failed'}")
    
    print("\n=== Testing Direct HTTP ===")
    direct_success = test_with_direct_http()
    print(f"{'✅ Direct HTTP test passed' if direct_success else '❌ Direct HTTP test failed'}")
    
    print("\n====== Test Summary ======")
    print(f"Login: {'✅' if login_success else '❌'}")
    print(f"Registration: {'✅' if registration_success else '❌'}")
    print(f"Direct HTTP: {'✅' if direct_success else '❌'}")
    
    if login_success and registration_success:
        print("\n✅ All tests passed! The authentication endpoints are working correctly.")
    else:
        print("\n❌ Some tests failed. Check the logs for details.")
