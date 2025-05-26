# GitHub Authentication Helper Script
Write-Host "GitHub Authentication Helper" -ForegroundColor Cyan
Write-Host "==========================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This script will help you authenticate with GitHub using a Personal Access Token." -ForegroundColor Yellow
Write-Host ""

# Get GitHub username
$username = Read-Host -Prompt "Enter your GitHub username"

# Get Personal Access Token (will not be displayed)
$secureToken = Read-Host -Prompt "Enter your GitHub Personal Access Token" -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureToken)
$token = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

# Store credentials
Write-Host "Storing GitHub credentials..." -ForegroundColor Yellow
[System.Environment]::SetEnvironmentVariable("GIT_USERNAME", $username, "User")
[System.Environment]::SetEnvironmentVariable("GIT_PASSWORD", $token, "User")

Write-Host ""
Write-Host "Credentials stored temporarily for this session. Now trying to push..." -ForegroundColor Green

# Setup URL with credentials
$remote = git remote get-url origin
$repoUrl = $remote -replace "https://", "https://${username}:${token}@"

# Push to GitHub
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
git push -u $repoUrl master

Write-Host ""
Write-Host "Push attempt completed. Please check the output above." -ForegroundColor Cyan
Write-Host "If successful, your code is now on GitHub at: https://github.com/Harshpandey9984/ProcessIQ" -ForegroundColor Green
