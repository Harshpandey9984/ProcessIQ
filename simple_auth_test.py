"""
Simple authentication test script.
"""
import requests
import json

# Configuration
BASE_URL = "http://localhost:8001"  # Backend URL
AUTH_ENDPOINT = "/api/auth/debug-token"  # Debug authentication endpoint
PROTECTED_ENDPOINT = "/api/digital-twin/list"  # Protected endpoint for testing

def test_auth():
    """Test authentication with direct requests."""
    print("Testing authentication with debug endpoint...")
    
    # Get a token from the debug endpoint
    response = requests.post(f"{BASE_URL}{AUTH_ENDPOINT}")
    
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        token_data = response.json()
        token = token_data.get("access_token")
        print(f"Token received: {token[:20]}...")
        
        # Try accessing protected endpoint with token
        print("\nAccessing protected endpoint with token...")
        auth_response = requests.get(
            f"{BASE_URL}{PROTECTED_ENDPOINT}",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        print(f"Status code: {auth_response.status_code}")
        if auth_response.status_code == 200:
            print("Successfully accessed protected endpoint!")
            print(f"Response: {json.dumps(auth_response.json()[:1], indent=2)}")
        else:
            print(f"Failed to access protected endpoint: {auth_response.text}")
    else:
        print(f"Failed to get token: {response.text}")

if __name__ == "__main__":
    test_auth()
