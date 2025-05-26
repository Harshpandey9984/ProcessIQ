@echo off
echo GitHub Authentication Helper
echo ==========================
echo.
echo This batch file will help you push to GitHub using your credentials.
echo.

set username=Harshpandey9984
set token=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n

echo.
echo Setting up credentials and pushing to GitHub...

git remote set-url origin https://%username%:%token%@github.com/Harshpandey9984/ProcessIQ.git
git push -u origin master

echo.
echo Push attempt completed. Please check the output above.
echo If successful, your code is now on GitHub at: https://github.com/Harshpandey9984/ProcessIQ

pause
