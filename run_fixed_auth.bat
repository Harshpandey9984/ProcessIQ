@echo off
echo ========================================
echo Digital Twin Platform Authentication Fix
echo ========================================

REM Kill any running Python processes
echo Stopping any running Python processes...
taskkill /f /im python.exe 2>nul

REM Create logs directory if it doesn't exist
if not exist logs mkdir logs

REM Start the fixed backend server
echo.
echo Starting fixed backend server...
start "Digital Twin Backend" cmd /c "python fixed_backend.py > logs\fixed_backend.log 2>&1"

REM Wait for backend to initialize
echo Waiting for backend to initialize...
timeout /t 5 /nobreak > nul

REM Check if backend is running
echo Checking backend health...
python -c "import requests; import sys; try: response = requests.get('http://localhost:8001/health'); print(f'Backend status: {response.status_code}'); sys.exit(0 if response.status_code == 200 else 1); except Exception as e: print(f'Error connecting to backend: {e}'); sys.exit(1)"
if %errorlevel% neq 0 (
    echo Backend server failed to start!
    echo Check logs\fixed_backend.log for details
    goto ERROR
)

echo.
echo Fixed backend is running successfully!
echo Backend URL: http://localhost:8001

REM Run authentication test
echo.
echo Running authentication test...
python fixed_auth_test.py > logs\fixed_auth_test.log 2>&1
if %errorlevel% neq 0 (
    echo Authentication test failed!
    echo Check logs\fixed_auth_test.log for details
    goto ERROR
)

echo.
echo Authentication test completed successfully!

REM Start frontend if needed
echo.
set /p START_FRONTEND=Do you want to start the frontend server too? (y/n): 
if /i "%START_FRONTEND%"=="y" (
    echo Starting frontend server...
    cd app\frontend
    start "Digital Twin Frontend" cmd /c "npm start > ..\..\logs\frontend.log 2>&1"
    cd ..\..
    echo Frontend starting at http://localhost:3000
    echo Please wait for it to initialize...
)

echo.
echo ========================================
echo Authentication Fix Complete!
echo ========================================
echo.
echo You can now:
echo - Access the backend at: http://localhost:8001
echo - API documentation at: http://localhost:8001/docs
echo - Check authentication status at: http://localhost:8001/debug/auth
echo.
echo Test login credentials:
echo - Admin: admin@example.com / password
echo - User: user@example.com / password
echo.
goto END

:ERROR
echo.
echo ========================================
echo ERROR: Authentication fix failed!
echo ========================================
echo.
echo Please check the log files for details.

:END
pause
