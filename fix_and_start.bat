@echo off
echo ===================================
echo Digital Twin Platform Fix and Start
echo ===================================

echo Creating logs directory if it doesn't exist...
if not exist logs mkdir logs

echo Starting the debug backend...
start "Digital Twin Debug Backend" cmd /c "python debug_backend.py > logs\debug_backend.log 2>&1"
echo Backend started!

timeout /t 3 /nobreak > nul

echo Testing API connectivity...
python test_auth_detailed.py > logs\auth_test.log 2>&1
echo Test completed! Check logs\auth_test.log for results.

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
echo Try using debug_login.html in a browser for direct API access

pause
