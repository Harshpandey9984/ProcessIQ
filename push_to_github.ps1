# GitHub Push with URL Credentials
$username = "Harshpandey9984"
$token = "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n"

Write-Host "Setting up credentials and pushing to GitHub..." -ForegroundColor Yellow

# Get current remote URL
$currentRemote = git remote get-url origin

# Set new URL with credentials
$repoUrl = "https://${username}:${token}@github.com/Harshpandey9984/ProcessIQ.git"
git remote set-url origin $repoUrl

# Push to GitHub
git push origin master

# Reset URL to original (for security)
git remote set-url origin $currentRemote.Replace("https://${username}:${token}@", "https://")

Write-Host "Push completed. Check above for results." -ForegroundColor Green
Write-Host "If successful, your code is now on GitHub at: https://github.com/Harshpandey9984/ProcessIQ"
