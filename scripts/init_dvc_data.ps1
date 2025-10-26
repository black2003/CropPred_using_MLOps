# PowerShell Script to initialize DVC remote storage with data
# Run this once to push your data to S3

# Change to project root directory (parent of scripts/)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location "$ScriptDir\.."

Write-Host "DVC Data Initialization Script" -ForegroundColor Green
Write-Host "===============================" -ForegroundColor Green
Write-Host ""
Write-Host "Working directory: $(Get-Location)" -ForegroundColor Cyan
Write-Host ""

# Check if data file exists
if (-not (Test-Path "data/Crop_recommendation.csv")) {
    Write-Host "Error: data/Crop_recommendation.csv not found!" -ForegroundColor Red
    Write-Host "Please ensure the data file exists before running this script."
    exit 1
}

Write-Host "Data file found: data/Crop_recommendation.csv" -ForegroundColor Green
Write-Host ""

# Check if DVC is initialized
if (-not (Test-Path ".dvc")) {
    Write-Host "Initializing DVC..." -ForegroundColor Cyan
    dvc init
}

# Check if data is tracked by DVC
if (-not (Test-Path "data/Crop_recommendation.csv.dvc")) {
    Write-Host "Adding data to DVC tracking..." -ForegroundColor Cyan
    dvc add data/Crop_recommendation.csv
    git add data/Crop_recommendation.csv.dvc data/.gitignore
    git commit -m "Add data to DVC tracking"
}

Write-Host ""
Write-Host "Configuring DVC remote..." -ForegroundColor Cyan
Write-Host "Note: You need to set your S3 bucket URL" -ForegroundColor Yellow
Write-Host ""

# Prompt for S3 URL if not set
if (-not $env:DVC_S3_URL) {
    $DVC_S3_URL = Read-Host "Please enter your S3 bucket URL (e.g., s3://my-bucket/dvc-storage)"
} else {
    $DVC_S3_URL = $env:DVC_S3_URL
}

# Configure remote
dvc remote add -d -f myremote $DVC_S3_URL

Write-Host ""
Write-Host "Pushing data to DVC remote..." -ForegroundColor Cyan
dvc push

Write-Host ""
Write-Host "===============================" -ForegroundColor Green
Write-Host "Data initialization complete!" -ForegroundColor Green
Write-Host "===============================" -ForegroundColor Green
Write-Host ""
Write-Host "The data has been pushed to: $DVC_S3_URL" -ForegroundColor Yellow
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Commit the DVC configuration:"
Write-Host "   git add .dvc/config"
Write-Host "   git commit -m 'Configure DVC remote'"
Write-Host "   git push"
Write-Host ""
Write-Host "2. The CI/CD pipeline will now be able to pull the data"
Write-Host ""
