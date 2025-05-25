@echo off
echo ===================================
echo Digital Twin Platform Starter
echo ===================================

REM Create logs directory if it doesn't exist
if not exist logs mkdir logs

REM First, install necessary dependencies
echo Installing backend dependencies...
pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt] pydantic email-validator python-multipart > logs\backend_install.log 2>&1
if %errorlevel% neq 0 (
    echo Failed to install backend dependencies. See logs\backend_install.log for details.
    goto ERROR
)

REM Start the super debug backend in a new window
echo Starting super debug backend server...
start "Digital Twin Backend" cmd /c "cd /d %~dp0 && python super_debug_backend.py > logs\super_debug_backend.log 2>&1"
if %errorlevel% neq 0 (
    echo Failed to start backend server.
    goto ERROR
)

REM Verify the backend is running by checking the health endpoint
echo Checking if backend is running...
timeout /t 5 /nobreak > nul
python -c "import requests; import sys; try: response = requests.get('http://localhost:8001/health', timeout=5); print(f'Backend health check: {response.status_code}'); sys.exit(0 if response.status_code == 200 else 1); except Exception as e: print(f'Error connecting to backend: {e}'); sys.exit(1)"
if %errorlevel% neq 0 (
    echo Backend health check failed. Check logs\backend.log for details.
    goto ERROR
)
echo Backend is running on http://localhost:8001

REM Wait a moment for the backend to start
timeout /t 3 /nobreak > nul

REM Check if npm exists
where npm > nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: npm not found. Please install Node.js.
    goto ERROR
)

REM Check if the frontend directory exists
if not exist app\frontend (
    echo ERROR: Frontend directory not found at app\frontend
    goto ERROR
)

REM Install frontend dependencies
echo Installing frontend dependencies...
cd app\frontend
npm install > ..\..\logs\frontend_install.log 2>&1
if %errorlevel% neq 0 (
    echo Failed to install frontend dependencies. See logs\frontend_install.log for details.
    cd ..\..
    goto ERROR
)

REM Start the frontend
echo Starting frontend server...
echo Current directory: %cd%
start "Digital Twin Frontend" cmd /c "npm start > ..\..\logs\frontend.log 2>&1"
if %errorlevel% neq 0 (
    echo Failed to start frontend server.
    cd ..\..
    goto ERROR
)

echo Frontend starting, this may take a moment...
timeout /t 10 /nobreak > nul

REM Return to the original directory
cd ..\..

echo.
echo ===================================
echo Servers are starting!
echo.
echo Frontend: http://localhost:3000
echo Backend: http://localhost:8001
echo API Documentation: http://localhost:8001/docs
echo.
echo Login with:
echo - Admin: admin@example.com / password
echo - User: user@example.com / password
echo ===================================
echo.
echo Check the logs directory for detailed logs if you encounter issues.
echo.
goto END

:ERROR
echo.
echo There was an error starting the servers. Please check the logs.
echo.

:END
pause
