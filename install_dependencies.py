"""
Script to check for and install required dependencies for the Digital Twin Platform.
"""
import subprocess
import sys

def install_package(package):
    """Install a Python package using pip."""
    print(f"Installing {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# List of core dependencies required for the platform
required_packages = [
    "numpy", 
    "pandas", 
    "fastapi", 
    "uvicorn", 
    "pydantic", 
    "python-jose[cryptography]", 
    "passlib[bcrypt]",
    "python-multipart"
]

# Install each required package
for package in required_packages:
    try:
        install_package(package)
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package}: {e}")
    except Exception as e:
        print(f"An error occurred while installing {package}: {e}")

print("Installation complete. You can now run the Digital Twin Platform.")
