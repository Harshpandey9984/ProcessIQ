@echo off
echo ========================================
echo Quick Start - Digital Twin Platform
echo ========================================

REM Kill any running processes
taskkill /f /im python.exe 2>nul
taskkill /f /im node.exe 2>nul

REM Create logs directory if it doesn't exist
if not exist logs mkdir logs

REM Start the backend server
echo Starting backend server...
start "Digital Twin Backend" cmd /c "python fixed_backend.py > logs\fixed_backend.log 2>&1"

REM Wait for it to start
echo Waiting for backend to initialize...
timeout /t 5 /nobreak > nul

REM Start the frontend server
echo Starting frontend server...
pushd app\frontend
start "Digital Twin Frontend" cmd /c "npm start > ..\..\logs\frontend.log 2>&1"
popd

echo ========================================
echo Servers are starting!
echo.
echo - Backend: http://localhost:8001
echo - Frontend: http://localhost:3000
echo.
echo If you encounter any issues:
echo 1. Check logs in the logs directory
echo 2. Open platform_test.html to diagnose connections
echo 3. Use direct_login_test.html for authentication testing
echo ========================================

REM Open test tools
echo Opening browser-based test tools...
start "" "platform_test.html"

echo Press any key to exit...
pause > nul
