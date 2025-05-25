@echo off
echo ===================================
echo Digital Twin Platform Fix and Start
echo ===================================

echo Creating logs directory if it doesn't exist...
if not exist logs mkdir logs

echo Installing required dependencies...
pip install fastapi uvicorn python-jose[cryptography] python-multipart > logs\install.log 2>&1
if %errorlevel% neq 0 (
    echo Failed to install dependencies. See logs\install.log for details.
    goto ERROR
)

echo Starting the simplified fixed backend...
start "Digital Twin Fixed Backend" cmd /c "python simplified_fixed_backend.py > logs\simplified_fixed_backend.log 2>&1"
echo Backend started!

timeout /t 3 /nobreak > nul

echo Testing backend health...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8001/health' -UseBasicParsing; Write-Host \"Health check status: $($response.StatusCode)\"; } catch { Write-Host \"Health check failed: $_\"; exit 1 }"
if %errorlevel% neq 0 (
    echo Backend health check failed. Check logs\simplified_fixed_backend.log
    goto ERROR
)

echo Starting the frontend...
cd app\frontend
start "Digital Twin Frontend" cmd /c "npm start > ..\..\logs\frontend.log 2>&1"
cd ..\..

echo ===================================
echo Servers are starting!
echo.
echo Frontend URL: http://localhost:3000
echo Backend URL: http://localhost:8001
echo API Documentation: http://localhost:8001/docs
echo.
echo Use these credentials to log in:
echo - Admin: admin@example.com / password
echo - User: user@example.com / password
echo ===================================

echo You can now try logging in at http://localhost:3000
echo If you have issues, check the logs directory

goto END

:ERROR
echo.
echo There was an error starting the servers. Please check the logs.
echo.

:END
pause
