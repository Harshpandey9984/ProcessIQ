"""
Simple connectivity checker for the Digital Twin Platform
"""
import requests
import socket

def check_port(host, port):
    """Check if a port is open on the host."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        print(f"Socket error: {e}")
        return False

def check_http(url):
    """Check if an HTTP endpoint is reachable."""
    try:
        response = requests.get(url, timeout=5)
        return response.status_code, response.text
    except requests.exceptions.ConnectionError:
        return None, "Connection refused"
    except Exception as e:
        return None, str(e)

print("=== Digital Twin Platform Connectivity Check ===")

# Check backend port
backend_port = check_port("localhost", 8001)
print(f"Backend port (8001) open: {'Yes' if backend_port else 'No'}")

# Check frontend port
frontend_port = check_port("localhost", 3000)
print(f"Frontend port (3000) open: {'Yes' if frontend_port else 'No'}")

# Check backend endpoints if port is open
if backend_port:
    print("\nTesting backend endpoints:")
    status, text = check_http("http://localhost:8001/health")
    print(f"  Health check: {'OK' if status == 200 else 'Failed'} - Status: {status}")
    if status == 200:
        print(f"  Response: {text[:100]}")
    
    # Try token endpoint
    status, text = check_http("http://localhost:8001/api/auth/token")
    print(f"  Auth token endpoint: {'OK' if status == 405 or status == 401 else 'Failed'} - Status: {status}")
    # We expect a 405 Method Not Allowed since we're using GET instead of POST
    # Or a 401 Unauthorized if it's working and expecting credentials

# Check frontend if port is open
if frontend_port:
    print("\nTesting frontend:")
    status, text = check_http("http://localhost:3000")
    print(f"  Frontend response: {'OK' if status == 200 else 'Failed'} - Status: {status}")
    if status == 200:
        print(f"  Response available")

print("\n=== Troubleshooting Recommendations ===")
if not backend_port:
    print("1. Backend server is not running - Run the following:")
    print("   cd digital-twin-platform")
    print("   python debug_backend.py")

if not frontend_port:
    print("2. Frontend server is not running - Run the following:")
    print("   cd digital-twin-platform\\app\\frontend")
    print("   npm start")

if backend_port and frontend_port:
    print("Both servers appear to be running. Check if:")
    print("1. A firewall is blocking connections")
    print("2. There are errors in the server logs:")
    print("   - Check logs/debug_backend.log")
    print("   - Check logs/frontend.log")
    print("3. Try clearing browser cache or using a different browser")
