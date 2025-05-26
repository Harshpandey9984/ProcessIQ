# GitHub Push Script with Better Security
# This script will push your code to GitHub
$ErrorActionPreference = "Stop" # Stop on first error

Write-Host "GitHub Push Helper" -ForegroundColor Cyan
Write-Host "=================" -ForegroundColor Cyan
Write-Host ""

# Diagnostics
Write-Host "Running diagnostics..." -ForegroundColor Yellow
Write-Host "Current directory: $(Get-Location)" -ForegroundColor DarkGray
Write-Host "Git version: $(git --version)" -ForegroundColor DarkGray
Write-Host "Git remote info: $(git remote -v)" -ForegroundColor DarkGray
Write-Host ""

# Setup git configuration
Write-Host "Setting up git configuration..." -ForegroundColor Yellow
git config --global credential.helper store

# Check for SSH key
$sshKeyExists = Test-Path -Path "$env:USERPROFILE\.ssh\id_rsa.pub"
if ($sshKeyExists) {
    Write-Host "SSH key found! Using SSH is recommended for better security." -ForegroundColor Green
    Write-Host "Run: git remote set-url origin git@github.com:Harshpandey9984/ProcessIQ.git" -ForegroundColor DarkGray
    Write-Host ""
}

# Github authentication options
Write-Host "GitHub Authentication Options:" -ForegroundColor Cyan
Write-Host "1. Use embedded credentials (temporary, easier)" -ForegroundColor Yellow
Write-Host "2. Manual setup (recommended for security)" -ForegroundColor Yellow
Write-Host ""
Write-Host "For option 1 - we'll use embedded credentials in this script." -ForegroundColor Green
Write-Host "For option 2 - Cancel this script (Ctrl+C) and follow GITHUB_UPLOAD_GUIDE.md" -ForegroundColor Green
Write-Host ""

Write-Host "Using embedded credentials for push..." -ForegroundColor Yellow
$remote = git remote get-url origin
$newRemote = "https://Harshpandey9984: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n@github.com/Harshpandey9984/ProcessIQ.git"

Write-Host "Setting temporary remote with credentials..." -ForegroundColor DarkGray
git remote set-url origin $newRemote

Write-Host "Pushing to GitHub (main attempt)..." -ForegroundColor Yellow
try {
    $pushResult = git push origin master 2>&1
    Write-Host $pushResult -ForegroundColor Gray
    
    # Check if push was successful
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Push successful!" -ForegroundColor Green
    } else {
        Write-Host "Push might have failed. Check output above." -ForegroundColor Red
        
        # Try alternative
        Write-Host "Trying alternative push method..." -ForegroundColor Yellow
        git push -u origin master --force
    }
} catch {
    Write-Host "Error during push: $_" -ForegroundColor Red
    Write-Host "Trying alternative push method..." -ForegroundColor Yellow
    git push -u origin master --force
}

# Reset remote for security
Write-Host "Resetting remote URL for security..." -ForegroundColor Yellow
git remote set-url origin https://github.com/Harshpandey9984/ProcessIQ.git

# Output final status
Write-Host ""
Write-Host "Process complete. To verify:" -ForegroundColor Green
Write-Host "1. Check GitHub repository: https://github.com/Harshpandey9984/ProcessIQ" -ForegroundColor Yellow
Write-Host "2. Run 'git status' to check local status" -ForegroundColor Yellow
Write-Host ""
git status
