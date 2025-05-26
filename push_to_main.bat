@echo off
echo GitHub Push to Main Branch - Updated Script
echo =========================================
echo.
echo This updated script will push changes to the main branch on GitHub.
echo.
echo IMPORTANT NOTES:
echo 1. You need to generate a NEW GitHub Personal Access Token
echo 2. Make sure token has "repo" scope permissions
echo.

REM Switch to main branch first
git checkout main

REM Ask for credentials
set /p username=Enter GitHub username: 
set /p token=Enter NEW GitHub Personal Access Token: 

REM Configure remote with credentials
echo.
echo Setting up credentials and pushing to main branch...
git remote set-url origin https://%username%:%token%@github.com/Harshpandey9984/ProcessIQ.git
git push -u origin main

echo.
echo Push attempt completed. Please check the output above.
echo If successful, your code is now on GitHub at: https://github.com/Harshpandey9984/ProcessIQ

echo.
echo After uploading, it's recommended to reset your remote URL to remove credentials:
echo git remote set-url origin https://github.com/Harshpandey9984/ProcessIQ.git

pause
