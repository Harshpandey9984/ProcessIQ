@echo off
echo ===================================
echo Running Authentication Verification
echo ===================================

REM Create logs directory if it doesn't exist
if not exist logs mkdir logs

REM Install required dependencies
pip install requests > logs\verify_install.log 2>&1

echo Running verification...
python verify_auth.py
if %errorlevel% neq 0 (
    echo Verification failed. Check logs\verification_results.log for details.
) else (
    echo Verification completed successfully!
)

echo.
echo Opening log file...
start notepad logs\verification_results.log
