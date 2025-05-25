"""
Start both servers and verify their status.
"""

import os
import subprocess
import socket
import time

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

def create_start_script(script_path, command, log_path):
    """Create a batch script to start a server."""
    with open(script_path, "w") as f:
        f.write("@echo off\n")
        f.write(f"cd {os.path.dirname(script_path)}\n")
        f.write(f"{command} > {log_path} 2>&1\n")

# Get base directory
base_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(base_dir, "app", "frontend")

# Create logs directory
logs_dir = os.path.join(base_dir, "logs")
os.makedirs(logs_dir, exist_ok=True)

# Create start scripts
backend_log = os.path.join(logs_dir, "backend.log")
frontend_log = os.path.join(logs_dir, "frontend.log")

backend_script = os.path.join(base_dir, "start_backend.bat")
frontend_script = os.path.join(base_dir, "start_frontend.bat")

create_start_script(
    backend_script,
    "python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000",
    backend_log
)

create_start_script(
    frontend_script,
    f"cd app\\frontend && npm start",
    frontend_log
)

print("Starting backend server...")
backend_process = subprocess.Popen(backend_script, shell=True)

# Check if backend port becomes available
print("Waiting for backend server to start...")
for i in range(10):
    if check_port("localhost", 8000):
        print("Backend server is running on port 8000")
        break
    time.sleep(2)
else:
    print("Warning: Backend server may not have started properly.")
    print(f"Check the logs at: {backend_log}")

print("\nStarting frontend server...")
frontend_process = subprocess.Popen(frontend_script, shell=True)

# Check if frontend port becomes available
print("Waiting for frontend server to start...")
for i in range(10):
    if check_port("localhost", 3000):
        print("Frontend server is running on port 3000")
        break
    time.sleep(2)
else:
    print("Warning: Frontend server may not have started properly.")
    print(f"Check the logs at: {frontend_log}")

print("\nServers have been started with batch files that you can reuse:")
print(f"- Backend server: {backend_script}")
print(f"- Frontend server: {frontend_script}")
print(f"\nLog files:")
print(f"- Backend log: {backend_log}")
print(f"- Frontend log: {frontend_log}")
print("\nAccess the application at:")
print("- Frontend: http://localhost:3000")
print("- Backend API: http://localhost:8000")
print("- API Documentation: http://localhost:8000/docs")
