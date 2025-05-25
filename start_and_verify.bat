@echo off
echo ==================================
echo Digital Twin Platform Verification
echo ==================================

REM Kill any existing processes
echo Stopping any running servers...
taskkill /f /im node.exe 2>nul
taskkill /f /im python.exe 2>nul

REM Create logs directory if it doesn't exist
if not exist logs mkdir logs

REM Start the backend server
echo.
echo Starting fixed backend server...
start "Digital Twin Backend" cmd /c "python fixed_backend.py > logs\backend.log 2>&1"

REM Wait a moment for the backend to start
echo Waiting for backend to initialize...
timeout /t 5 /nobreak > nul

REM Check if backend is running
echo Checking backend health...
python -c "import requests; response = requests.get('http://localhost:8001/health'); print(f'Backend status: {response.status_code}')"
if %errorlevel% neq 0 (
    echo Backend server failed to start!
    echo Check logs\backend.log for details
    goto END
)

REM Start the frontend
echo.
echo Starting frontend server...
cd app\frontend
start "Digital Twin Frontend" cmd /c "npm start > ..\..\logs\frontend.log 2>&1"
cd ..\..

echo Waiting for frontend to initialize...
timeout /t 10 /nobreak > nul

echo.
echo ==================================
echo Running verification tests...
echo ==================================
python final_verification.py

echo.
echo ==================================
echo Verification complete!
echo ==================================
echo See logs\verification_results.log for detailed results

:END
echo.
echo Press any key to open the verification log...
pause > nul
start notepad logs\verification_results.log
