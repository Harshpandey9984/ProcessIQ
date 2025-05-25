@echo off
echo ==================================
echo Digital Twin Platform Restart
echo ==================================

REM Kill any existing processes
echo Stopping any running servers...
taskkill /f /im node.exe 2>nul
taskkill /f /im python.exe 2>nul

REM Create logs directory if it doesn't exist
if not exist logs mkdir logs

REM Start the backend server
echo.
echo Starting FIXED backend server...
start "Digital Twin Backend" cmd /c "python fixed_backend.py > logs\backend.log 2>&1"

REM Wait a moment for the backend to start
timeout /t 3 /nobreak > nul

REM Start the frontend
echo.
echo Starting frontend server...
cd app\frontend
start "Digital Twin Frontend" cmd /c "npm start > ..\..\logs\frontend.log 2>&1"
cd ..\..

echo.
echo ==================================
echo Servers restarted!
echo.
echo Frontend URL: http://localhost:3000
echo Backend URL: http://localhost:8001
echo API Documentation: http://localhost:8001/docs
echo.
echo Use these credentials to log in:
echo - Admin: admin@example.com / password
echo - User: user@example.com / password
echo ==================================
echo.
echo After the servers start, try:
echo 1. Open platform_test.html in your browser to test connectivity
echo 2. Navigate to http://localhost:3000 in your browser
echo.
echo If you have issues, check:
echo - logs\backend.log for backend errors
echo - logs\frontend.log for frontend errors
echo.

pause
