"""
Troubleshooting script to verify server connectivity.
This script checks if the frontend and backend servers are reachable.
"""

import socket
import time
import requests
from urllib.error import URLError

def check_port(host, port):
    """Check if a port is open on the host."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def check_http(url):
    """Check if an HTTP endpoint is reachable."""
    try:
        response = requests.get(url, timeout=5)
        return response.status_code < 500
    except:
        return False

def main():
    """Main function."""
    print("Digital Twin Platform Connectivity Checker")
    print("-----------------------------------------")
    
    # Check backend connectivity
    backend_port_open = check_port("localhost", 8001)
    print(f"Backend server port (8001) open: {backend_port_open}")
    
    # Check frontend connectivity
    frontend_port_open = check_port("localhost", 3000)
    print(f"Frontend server port (3000) open: {frontend_port_open}")
    
    # Try to access backend API
    if backend_port_open:
        backend_health = check_http("http://localhost:8001/health")
        backend_api_docs = check_http("http://localhost:8001/docs")
        print(f"Backend health endpoint: {backend_health}")
        print(f"Backend API docs: {backend_api_docs}")
    
    # Try to access frontend
    if frontend_port_open:
        frontend_reachable = check_http("http://localhost:3000")
        print(f"Frontend reachable: {frontend_reachable}")
    
    print("\nTroubleshooting Tips:")
    if not backend_port_open:
        print("- Backend server is not running. Try starting it with:")
        print("  cd digital-twin-platform; python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001")
    
    if not frontend_port_open:
        print("- Frontend server is not running. Try starting it with:")
        print("  cd digital-twin-platform\\app\\frontend; npm install; npm start")
    
    if backend_port_open and not (backend_health or backend_api_docs):
        print("- Backend server is running but HTTP endpoints are not responding.")
        print("  Check the backend logs for errors.")
    
    if frontend_port_open and not frontend_reachable:
        print("- Frontend server is running but not serving content.")
        print("  Check the frontend logs for errors.")

if __name__ == "__main__":
    main()
