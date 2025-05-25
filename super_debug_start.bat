@echo off
echo ===================================
echo Super Debug Authentication Starter
echo ===================================

echo Creating logs directory if it doesn't exist...
if not exist logs mkdir logs

echo Stopping any existing backend processes...
taskkill /FI "WINDOWTITLE eq Digital Twin*" /F > nul 2>&1

echo Installing basic dependencies...
pip install fastapi uvicorn python-jose python-multipart > logs\install_basic.log 2>&1

echo Starting super debug backend...
start "Digital Twin Backend" cmd /c "python super_debug_backend.py > logs\super_debug_backend.log 2>&1"

echo Waiting for backend to initialize...
timeout /t 5 /nobreak > nul

echo Testing backend health...
python -c "import requests; resp = requests.get('http://localhost:8001/health'); print('Backend status:', resp.status_code); print(resp.json())"

echo Starting frontend...
cd app\frontend
start "Digital Twin Frontend" cmd /c "npm start > ..\..\logs\frontend.log 2>&1"
cd ..\..

echo ===================================
echo Servers starting!
echo.
echo Frontend: http://localhost:3000
echo Backend: http://localhost:8001
echo.
echo Login with:
echo - admin@example.com / password
echo - user@example.com / password
echo ===================================
echo.

pause
