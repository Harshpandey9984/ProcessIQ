"""
Check if servers are running on expected ports.
"""
import socket
import time
import requests

def check_port(host, port, timeout=2):
    """Check if a port is open."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def check_http(url):
    """Check if an HTTP endpoint is reachable."""
    try:
        response = requests.get(url, timeout=5)
        print(f"Response from {url}: {response.status_code}")
        return True
    except Exception as e:
        print(f"Failed to connect to {url}: {str(e)}")
        return False

if __name__ == "__main__":
    print("Checking if servers are running...")
    
    # Check backend - port 8001
    backend_running = check_port("localhost", 8001)
    print(f"Backend (port 8001): {'RUNNING' if backend_running else 'NOT RUNNING'}")
    
    # Check frontend - port 3000
    frontend_running = check_port("localhost", 3000)
    print(f"Frontend (port 3000): {'RUNNING' if frontend_running else 'NOT RUNNING'}")
    
    # Try to access API endpoints
    if backend_running:
        print("\nTrying to access backend API endpoints...")
        check_http("http://localhost:8001/health")
        check_http("http://localhost:8001/docs")
    
    if frontend_running:
        print("\nTrying to access frontend...")
        check_http("http://localhost:3000")
    
    print("\nIf any service is not running, check the logs in the logs directory.")
    print("If the backend is running but the frontend can't connect, make sure the proxy setting in package.json is correct.")
