"""
Script to start servers and log outputs.
"""

import subprocess
import os
import time

# Create log directory
log_dir = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(log_dir, exist_ok=True)

# Get absolute paths
base_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(base_dir, "app", "frontend")
backend_dir = base_dir

# Log file paths
backend_log = os.path.join(log_dir, "backend.log")
frontend_log = os.path.join(log_dir, "frontend.log")

print(f"Starting backend server, logging to {backend_log}")
try:
    with open(backend_log, "w") as f:
        backend_process = subprocess.Popen(
            ["python", "-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
            stdout=f,
            stderr=f,
            cwd=backend_dir,
            text=True
        )
except Exception as e:
    with open(backend_log, "w") as f:
        f.write(f"Error starting backend: {str(e)}\n")
    print(f"Error starting backend: {str(e)}")

# Wait a moment before starting frontend
time.sleep(2)

print(f"Starting frontend server, logging to {frontend_log}")
try:
    with open(frontend_log, "w") as f:
        frontend_process = subprocess.Popen(
            ["npm", "start"],
            stdout=f,
            stderr=f,
            cwd=frontend_dir,
            text=True
        )
except Exception as e:
    with open(frontend_log, "w") as f:
        f.write(f"Error starting frontend: {str(e)}\n")
    print(f"Error starting frontend: {str(e)}")

print("Servers are starting in the background. Check the log files for details.")
print(f"Backend log: {backend_log}")
print(f"Frontend log: {frontend_log}")

# Keep the script running
try:
    print("Press Ctrl+C to stop the servers...")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping servers...")
    if 'backend_process' in locals():
        backend_process.terminate()
    if 'frontend_process' in locals():
        frontend_process.terminate()
    print("Servers stopped.")
