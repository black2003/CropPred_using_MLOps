# Script to fix Git/DVC tracking conflicts
# This removes .pkl files from Git tracking so DVC can manage them

Write-Host "Fixing Git/DVC Tracking Conflicts" -ForegroundColor Green
Write-Host "===================================" -ForegroundColor Green
Write-Host ""

# List of files to remove from Git tracking
$filesToRemove = @(
    "data/raw_data.pkl",
    "data/processed_data.pkl", 
    "data/features.pkl",
    "data/target.pkl",
    "data/test_features.pkl",
    "data/test_target.pkl"
)

Write-Host "Files to remove from Git tracking:" -ForegroundColor Cyan
$filesToRemove | ForEach-Object { Write-Host "  - $_" -ForegroundColor Gray }
Write-Host ""

# Check which files actually exist in Git
$trackedFiles = @()
foreach ($file in $filesToRemove) {
    $gitLsResult = git ls-files $file 2>$null
    if ($LASTEXITCODE -eq 0 -and $gitLsResult) {
        $trackedFiles += $file
        Write-Host "✓ $file is tracked by Git" -ForegroundColor Yellow
    } else {
        Write-Host "○ $file is not tracked by Git (skipping)" -ForegroundColor Gray
    }
}

Write-Host ""

if ($trackedFiles.Count -eq 0) {
    Write-Host "No files need to be removed from Git tracking." -ForegroundColor Green
    Write-Host "You can proceed with running the pipeline." -ForegroundColor Green
    exit 0
}

Write-Host "Removing $($trackedFiles.Count) files from Git tracking..." -ForegroundColor Cyan
Write-Host ""

# Remove files from Git tracking (but keep them locally)
foreach ($file in $trackedFiles) {
    Write-Host "Removing $file from Git..." -ForegroundColor Gray
    git rm --cached $file
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Removed $file" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed to remove $file" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Updating .gitignore..." -ForegroundColor Cyan

# Ensure data/.gitignore exists and has the right content
$gitignoreContent = @"
/Crop_recommendation.csv
# DVC-managed data files - these are outputs from the pipeline
/raw_data.pkl
/processed_data.pkl
/features.pkl
/target.pkl
/test_features.pkl
/test_target.pkl
"@

Set-Content -Path "data/.gitignore" -Value $gitignoreContent -Force
Write-Host "✓ Updated data/.gitignore" -ForegroundColor Green

Write-Host ""
Write-Host "===================================" -ForegroundColor Green
Write-Host "Fix Applied Successfully!" -ForegroundColor Green
Write-Host "===================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Stage and commit the changes:" -ForegroundColor Yellow
Write-Host "   git add data/.gitignore" -ForegroundColor White
Write-Host "   git commit -m 'Fix: Stop tracking DVC-managed .pkl files'" -ForegroundColor White
Write-Host ""
Write-Host "2. Push to GitHub:" -ForegroundColor Yellow
Write-Host "   git push" -ForegroundColor White
Write-Host ""
Write-Host "3. After pushing, the CI/CD pipeline will be able to run dvc repro successfully!" -ForegroundColor Green
Write-Host ""
