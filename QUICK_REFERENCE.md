# Quick Experiments Reference

## Run Experiments

### Windows (PowerShell)
```powershell
# 12 predefined experiments
.\run_experiments.ps1

# Grid search (48 experiments)
.\run_grid_experiments.ps1
```

### Linux/Mac/WSL (Bash)
```bash
# 12 predefined experiments
bash run_experiments.sh

# Grid search (48 experiments)  
bash run_grid_experiments.sh
```

## View Results

```bash
# Show all experiments
dvc exp show

# Show sorted by accuracy (best first)
dvc exp show --sort-by=metrics.json:accuracy --sort-order=desc

# Show only model parameters
dvc exp show --include-params=model

# Compare two experiments
dvc exp diff exp-baseline exp-trees-200

# View metrics
dvc metrics show
```

## Apply Best Result

```bash
# Apply experiment to workspace
dvc exp apply <experiment-name>

# Commit the changes
git add params.yaml dvc.lock
git commit -m "Applied best model configuration"
```

## Hyperparameters Being Tested

- **n_estimators**: 50, 100, 150, 200, 300
- **max_depth**: 5, 8, 10, 15, 20, 25, 30
- **min_samples_split**: 2, 5, 10
- **min_samples_leaf**: 1, 2, 4

## Expected Results

After running experiments, you can:
1. Compare accuracy across all configurations
2. Identify best hyperparameter combinations
3. Understand trade-offs (accuracy vs. training time)
4. Select final model for deployment
