# Final Verification Tool for Digital Twin Platform Authentication
# This PowerShell script performs a comprehensive test of all authentication components

# Clear screen
Clear-Host

# Configure logging to file
$LogFile = "logs/verification_results.log"
New-Item -ItemType Directory -Force -Path "logs" | Out-Null
Set-Content -Path $LogFile -Value ""

# Configuration
$BackendUrl = "http://localhost:8001"
$FrontendUrl = "http://localhost:3000"
$TestCredentials = @{
    username = "admin@example.com"
    password = "password"
}

function Write-Log {
    param (
        [string]$Message
    )
    
    Write-Host $Message
    Add-Content -Path $LogFile -Value $Message
}

function Write-Header {
    param (
        [string]$Title
    )
    
    $Header = "`n" + "="*60
    $Header += "`n $Title"
    $Header += "`n" + "="*60
    Write-Log $Header
}

function Write-TestResult {
    param (
        [bool]$Success,
        [string]$Message
    )
    
    $Mark = if ($Success) { "✓" } else { "✗" }
    $Status = if ($Success) { "SUCCESS" } else { "FAILED" }
    Write-Log "[$Mark] $Status: $Message"
}

function Test-Component {
    param (
        [string]$Name,
        [scriptblock]$TestScript
    )
    
    Write-Log "`n▶ Testing: $Name..."
    try {
        $Result = & $TestScript
        Write-TestResult -Success $Result[0] -Message $Result[1]
        return $Result[0]
    }
    catch {
        Write-TestResult -Success $false -Message "Exception occurred: $($_.Exception.Message)"
        return $false
    }
}

function Test-BackendHealth {
    try {
        $Response = Invoke-RestMethod -Uri "$BackendUrl/health" -TimeoutSec 5 -ErrorAction Stop
        return $true, "Backend is running and healthy"
    }
    catch {
        return $false, "Backend is not running or not reachable"
    }
}

function Test-FrontendConnectivity {
    try {
        $Response = Invoke-WebRequest -Uri $FrontendUrl -TimeoutSec 5 -ErrorAction Stop
        return $true, "Frontend is running (status $($Response.StatusCode))"
    }
    catch {
        return $false, "Frontend is not running or not reachable"
    }
}

function Test-LoginEndpoint {
    try {
        $Body = @{
            username = $TestCredentials.username
            password = $TestCredentials.password
        }
        
        $Response = Invoke-RestMethod -Uri "$BackendUrl/api/auth/token" -Method Post -Body $Body -ContentType "application/x-www-form-urlencoded" -TimeoutSec 5 -ErrorAction Stop
        
        if ($Response.access_token -and $Response.user) {
            return $true, "Login successful, token received for user: $($Response.user.email)"
        }
        else {
            return $false, "Login response missing token or user data"
        }
    }
    catch {
        return $false, "Login failed: $($_.Exception.Message)"
    }
}

function Test-ProtectedEndpoint {
    param (
        [string]$Token = $null
    )
    
    if (-not $Token) {
        # First, get a token
        try {
            $Body = @{
                username = $TestCredentials.username
                password = $TestCredentials.password
            }
            
            $LoginResponse = Invoke-RestMethod -Uri "$BackendUrl/api/auth/token" -Method Post -Body $Body -ContentType "application/x-www-form-urlencoded" -TimeoutSec 5 -ErrorAction Stop
            $Token = $LoginResponse.access_token
        }
        catch {
            return $false, "Could not obtain token for protected endpoint test"
        }
    }
    
    # Now try the protected endpoint
    try {
        $Headers = @{
            Authorization = "Bearer $Token"
        }
        
        $Response = Invoke-RestMethod -Uri "$BackendUrl/api/digital-twin" -Headers $Headers -TimeoutSec 5 -ErrorAction Stop
        
        return $true, "Successfully accessed protected endpoint, received $($Response.Count) items"
    }
    catch {
        return $false, "Failed to access protected endpoint: $($_.Exception.Message)"
    }
}

function Test-UnauthorizedAccess {
    try {
        $Response = Invoke-WebRequest -Uri "$BackendUrl/api/digital-twin" -TimeoutSec 5 -ErrorAction SilentlyContinue
        
        if ($Response.StatusCode -eq 401) {
            return $true, "Correctly received 401 Unauthorized for protected endpoint without token"
        }
        else {
            return $false, "Expected 401, but got $($Response.StatusCode)"
        }
    }
    catch [System.Net.WebException] {
        if ($_.Exception.Response.StatusCode -eq 401) {
            return $true, "Correctly received 401 Unauthorized for protected endpoint without token"
        }
        else {
            return $false, "Expected 401, but got $($_.Exception.Response.StatusCode)"
        }
    }
    catch {
        return $false, "Error testing unauthorized access: $($_.Exception.Message)"
    }
}

# Run the verification
Write-Header "DIGITAL TWIN PLATFORM AUTHENTICATION VERIFICATION"
Write-Log "Timestamp: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Log "Backend URL: $BackendUrl"
Write-Log "Frontend URL: $FrontendUrl"

# Count total tests and successful tests
$TotalTests = 0
$PassedTests = 0

# Test server health
Write-Header "SERVER CONNECTIVITY TESTS"

$Result = Test-Component -Name "Backend health" -TestScript { Test-BackendHealth }
$TotalTests++
if ($Result) { $PassedTests++ }

$Result = Test-Component -Name "Frontend connectivity" -TestScript { Test-FrontendConnectivity }
$TotalTests++
if ($Result) { $PassedTests++ }

# Test authentication
Write-Header "AUTHENTICATION TESTS"

$Result = Test-Component -Name "Login endpoint" -TestScript { Test-LoginEndpoint }
$TotalTests++
if ($Result) { $PassedTests++ }

if ($Result) {
    # Get token for protected endpoint test
    $Body = @{
        username = $TestCredentials.username
        password = $TestCredentials.password
    }
    
    $LoginResponse = Invoke-RestMethod -Uri "$BackendUrl/api/auth/token" -Method Post -Body $Body -ContentType "application/x-www-form-urlencoded"
    $Token = $LoginResponse.access_token
    
    $Result = Test-Component -Name "Protected endpoint access" -TestScript { Test-ProtectedEndpoint -Token $Token }
    $TotalTests++
    if ($Result) { $PassedTests++ }
}
else {
    Write-Log "Skipping protected endpoint test due to login failure"
}

$Result = Test-Component -Name "Unauthorized access handling" -TestScript { Test-UnauthorizedAccess }
$TotalTests++
if ($Result) { $PassedTests++ }

# Print summary
Write-Header "VERIFICATION SUMMARY"
$SuccessRate = if ($TotalTests -gt 0) { ($PassedTests / $TotalTests) * 100 } else { 0 }
Write-Log "Tests passed: $PassedTests/$TotalTests ($([math]::Round($SuccessRate, 1))%)"

if ($PassedTests -eq $TotalTests) {
    Write-Log "`n✅ VERIFICATION SUCCESSFUL: All authentication components are working properly!"
}
else {
    Write-Log "`n⚠️ VERIFICATION INCOMPLETE: Some tests failed, see details above."
}

Write-Host "`nVerification complete. Results saved to: $LogFile"
