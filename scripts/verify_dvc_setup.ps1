# Script to verify DVC setup and data availability
# This checks if your local DVC setup is correct

Write-Host "DVC Setup Verification" -ForegroundColor Green
Write-Host "======================" -ForegroundColor Green
Write-Host ""

# 1. Check if DVC is installed
Write-Host "[1/6] Checking DVC installation..." -ForegroundColor Cyan
try {
    $dvcVersion = dvc version
    Write-Host "✓ DVC is installed" -ForegroundColor Green
    Write-Host $dvcVersion[0]
} catch {
    Write-Host "✗ DVC is not installed!" -ForegroundColor Red
    Write-Host "Install with: pip install dvc[s3]"
    exit 1
}
Write-Host ""

# 2. Check if data file exists
Write-Host "[2/6] Checking data file..." -ForegroundColor Cyan
if (Test-Path "data\Crop_recommendation.csv") {
    $fileSize = (Get-Item "data\Crop_recommendation.csv").Length / 1KB
    Write-Host "✓ Data file exists ($([math]::Round($fileSize, 2)) KB)" -ForegroundColor Green
} else {
    Write-Host "✗ Data file not found!" -ForegroundColor Red
    exit 1
}
Write-Host ""

# 3. Check if .dvc file exists
Write-Host "[3/6] Checking DVC tracking..." -ForegroundColor Cyan
if (Test-Path "data\Crop_recommendation.csv.dvc") {
    Write-Host "✓ Data is tracked by DVC" -ForegroundColor Green
    Write-Host "Content of .dvc file:" -ForegroundColor Gray
    Get-Content "data\Crop_recommendation.csv.dvc"
} else {
    Write-Host "✗ .dvc file not found!" -ForegroundColor Red
    Write-Host "Run: dvc add data/Crop_recommendation.csv"
    exit 1
}
Write-Host ""

# 4. Check DVC remote configuration
Write-Host "[4/6] Checking DVC remote..." -ForegroundColor Cyan
$remoteConfig = dvc remote list
if ($remoteConfig) {
    Write-Host "✓ DVC remote configured:" -ForegroundColor Green
    Write-Host $remoteConfig
    
    # Get default remote
    $defaultRemote = (dvc config core.remote).Trim()
    if ($defaultRemote) {
        Write-Host "Default remote: $defaultRemote" -ForegroundColor Yellow
    }
} else {
    Write-Host "✗ No DVC remote configured!" -ForegroundColor Red
    Write-Host "Run: dvc remote add -d myremote s3://your-bucket/path"
    exit 1
}
Write-Host ""

# 5. Check AWS credentials
Write-Host "[5/6] Checking AWS credentials..." -ForegroundColor Cyan
try {
    $awsIdentity = aws sts get-caller-identity 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ AWS credentials are configured" -ForegroundColor Green
        $identity = $awsIdentity | ConvertFrom-Json
        Write-Host "Account: $($identity.Account)" -ForegroundColor Gray
        Write-Host "User/Role: $($identity.Arn)" -ForegroundColor Gray
    } else {
        Write-Host "✗ AWS credentials not configured or invalid!" -ForegroundColor Red
        Write-Host "Configure with: aws configure"
    }
} catch {
    Write-Host "⚠ AWS CLI not found (optional for local work)" -ForegroundColor Yellow
}
Write-Host ""

# 6. Check if data exists in remote
Write-Host "[6/6] Checking if data exists in S3 remote..." -ForegroundColor Cyan
Write-Host "Attempting to check remote status..." -ForegroundColor Gray

# Try to get status
$statusOutput = dvc status data/Crop_recommendation.csv.dvc 2>&1
if ($LASTEXITCODE -eq 0) {
    if ($statusOutput -match "up to date") {
        Write-Host "✓ Data is pushed to remote and up to date!" -ForegroundColor Green
    } elseif ($statusOutput -match "not in cache") {
        Write-Host "⚠ Data exists locally but NOT in remote!" -ForegroundColor Yellow
        Write-Host "You need to push: dvc push" -ForegroundColor Yellow
    } else {
        Write-Host "Status: $statusOutput" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠ Could not verify remote status" -ForegroundColor Yellow
    Write-Host "Error: $statusOutput" -ForegroundColor Gray
}

Write-Host ""
Write-Host "======================" -ForegroundColor Green
Write-Host "Verification Complete" -ForegroundColor Green
Write-Host "======================" -ForegroundColor Green
Write-Host ""

# Summary and recommendations
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host ""
Write-Host "If data is NOT in remote:" -ForegroundColor Yellow
Write-Host "  1. Push data to S3: dvc push" -ForegroundColor White
Write-Host "  2. Commit DVC files: git add data/Crop_recommendation.csv.dvc .dvc/config" -ForegroundColor White
Write-Host "  3. Push to GitHub: git commit -m 'Add data to DVC' && git push" -ForegroundColor White
Write-Host ""
Write-Host "If data IS in remote:" -ForegroundColor Green
Write-Host "  1. Your setup is complete!" -ForegroundColor White
Write-Host "  2. The CI/CD pipeline should now work" -ForegroundColor White
Write-Host ""
Write-Host "To test DVC pull locally:" -ForegroundColor Cyan
Write-Host "  1. Backup and remove local data: mv data/Crop_recommendation.csv data/Crop_recommendation.csv.backup" -ForegroundColor White
Write-Host "  2. Pull from remote: dvc pull data/Crop_recommendation.csv.dvc" -ForegroundColor White
Write-Host "  3. Verify: ls data/Crop_recommendation.csv" -ForegroundColor White
Write-Host ""
