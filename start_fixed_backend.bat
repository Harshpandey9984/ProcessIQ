@echo off
echo ==================================
echo Digital Twin Platform - Fixed Backend
echo ==================================

REM Kill any existing processes
echo Stopping any running servers...
taskkill /f /im python.exe 2>nul

REM Create logs directory if it doesn't exist
if not exist logs mkdir logs

REM Start the fixed backend server
echo.
echo Starting fixed backend server...
start "Digital Twin Backend" cmd /c "python fixed_backend.py > logs\fixed_backend.log 2>&1"

REM Wait a moment for the backend to start
echo Waiting for backend to initialize...
timeout /t 5 /nobreak > nul

REM Check if backend is running
echo Checking backend health...
python -c "import requests; import sys; try: response = requests.get('http://localhost:8001/health'); print(f'Backend status: {response.status_code}'); sys.exit(0 if response.status_code == 200 else 1); except: print('Error connecting to backend'); sys.exit(1)"
if %errorlevel% neq 0 (
    echo Backend server failed to start!
    echo Check logs\fixed_backend.log for details
    goto END
)

echo.
echo ==================================
echo Fixed backend is running!
echo Backend URL: http://localhost:8001
echo ==================================

:END
echo.
pause
