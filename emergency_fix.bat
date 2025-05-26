@echo off
echo ===================================
echo Digital Twin Platform - Emergency Fix
echo ===================================

REM Create logs directory if it doesn't exist
if not exist logs mkdir logs

echo Shutting down any existing backend processes...
taskkill /FI "WINDOWTITLE eq Digital Twin Backend*" /T /F > nul 2>&1

echo Starting simplified fixed backend...
start "Digital Twin Backend" cmd /c "python simplified_fixed_backend.py > logs\emergency_fix.log 2>&1"

echo Backend started. Waiting a few seconds to initialize...
timeout /t 5 /nobreak > nul

echo Testing backend health...
python -c "import requests; import sys; try: response = requests.get('http://localhost:8001/health', timeout=5); print('Backend health:', response.status_code, response.json()); sys.exit(0) if response.status_code == 200 else sys.exit(1); except Exception as e: print('Error:', e); sys.exit(1)"
if %errorlevel% neq 0 (
    echo Backend health check failed. Check logs\emergency_fix.log for details.
    goto ERROR
)

echo ===================================
echo Backend is now running!
echo.
echo Use these login credentials:
echo - Admin: admin@example.com / password
echo - User: user@example.com / password
echo ===================================
goto END

:ERROR
echo.
echo There was an error starting the backend.
echo.

:END
pause
