# PowerShell Grid Search Style DVC Experiments
# Tests combinations of key hyperparameters

Write-Host "Starting Grid Search DVC Experiments" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green

# Define parameter grids
$n_estimators = @(50, 100, 150, 200)
$max_depth = @(5, 10, 15, 20)
$min_samples_split = @(2, 5, 10)

# Counter for experiment numbering
$exp_num = 1

# Grid search over key parameters
foreach ($n_est in $n_estimators) {
    foreach ($depth in $max_depth) {
        foreach ($split in $min_samples_split) {
            Write-Host ""
            Write-Host "Experiment ${exp_num}: n_estimators=${n_est}, max_depth=${depth}, min_samples_split=${split}" -ForegroundColor Cyan
            
            dvc exp run --name "grid-exp-${exp_num}" `
                -S model.n_estimators=$n_est `
                -S model.max_depth=$depth `
                -S model.min_samples_split=$split `
                -S model.min_samples_leaf=1
            
            $exp_num++
            
            # Optional: Uncomment to limit number of experiments
            # if ($exp_num -gt 20) {
            #     break
            # }
        }
    }
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "Grid search completed! Total experiments: $($exp_num - 1)" -ForegroundColor Green
Write-Host ""
Write-Host "View all results:" -ForegroundColor Yellow
Write-Host "  dvc exp show --include-params=model"
Write-Host "  dvc exp show --sort-by=metrics.json:accuracy --sort-order=desc"
Write-Host ""
