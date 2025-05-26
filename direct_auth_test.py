import requests
import json
import sys

print("===== Direct Authentication Test =====")

BASE_URL = "http://localhost:8001"
AUTH_ENDPOINT = "/api/auth/token"

def test_login(email, password):
    print(f"\nTesting login for {email}...")
    
    try:
        # Create form data for OAuth2 login
        data = {
            "username": email,
            "password": password
        }
        
        # Send POST request
        response = requests.post(
            f"{BASE_URL}{AUTH_ENDPOINT}",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✓ Login successful!")
            print(f"Token: {result.get('access_token')[:20]}...")
            print(f"User: {result.get('user', {}).get('email')}")
            return True
        else:
            print(f"✗ Login failed: {response.text}")
            return False
    
    except Exception as e:
        print(f"✗ Error during test: {str(e)}")
        return False

def test_health():
    print("Testing backend health...")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"✗ Health check failed: {response.text}")
            return False
    
    except Exception as e:
        print(f"✗ Error during health check: {str(e)}")
        return False

# Check server health first
if not test_health():
    print("\n✗ Backend server seems to be unavailable. Exiting.")
    sys.exit(1)

# Test admin login
admin_success = test_login("admin@example.com", "password")

# Test user login
user_success = test_login("user@example.com", "password")

# Summary
print("\n===== Test Results =====")
print(f"Admin login: {'✓ Success' if admin_success else '✗ Failed'}")
print(f"User login: {'✓ Success' if user_success else '✗ Failed'}")

if admin_success and user_success:
    print("\n✓ All authentication tests passed!")
    sys.exit(0)
else:
    print("\n✗ Some authentication tests failed.")
    sys.exit(1)