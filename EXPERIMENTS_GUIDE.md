# DVC Experiments Guide

This guide explains how to run experiments with different hyperparameter configurations.

## Hyperparameters

The project now includes the following Random Forest hyperparameters in `params.yaml`:

### Model Parameters
- **n_estimators** (default: 100): Number of trees in the forest
- **max_depth** (default: 10): Maximum depth of the tree
- **min_samples_split** (default: 2): Minimum samples required to split an internal node
- **min_samples_leaf** (default: 1): Minimum samples required to be at a leaf node
- **max_features** (default: "sqrt"): Number of features to consider for best split
- **max_leaf_nodes** (default: null): Maximum number of leaf nodes
- **min_impurity_decrease** (default: 0.0): Minimum impurity decrease required for split
- **bootstrap** (default: true): Whether bootstrap samples are used when building trees
- **oob_score** (default: false): Whether to use out-of-bag samples to estimate accuracy
- **criterion** (default: "gini"): Function to measure split quality ("gini" or "entropy")
- **random_state** (default: 42): Random seed for reproducibility

### Training Parameters
- **test_size** (default: 0.2): Proportion of dataset for testing
- **random_state** (default: 42): Random seed for train-test split

## Running Experiments

### Option 1: Pre-defined Experiments (12 experiments)
These scripts run specific experiment configurations testing different aspects:

**Linux/Mac/WSL:**
```bash
bash run_experiments.sh
```

**Windows PowerShell:**
```powershell
.\run_experiments.ps1
```

**Experiments included:**
1. Baseline configuration
2. 200 estimators
3. 300 estimators
4. Max depth 20
5. Max depth 30
6. Min samples split 5
7. Min samples split 10
8. Min samples leaf 2
9. Min samples leaf 4
10. Balanced (200 trees, depth 15, split 5, leaf 2)
11. High capacity (300 trees, depth 25)
12. Regularized (150 trees, depth 8, split 10, leaf 4)

### Option 2: Grid Search Experiments (48 experiments)
Tests combinations of key hyperparameters:
- n_estimators: [50, 100, 150, 200]
- max_depth: [5, 10, 15, 20]
- min_samples_split: [2, 5, 10]

**Linux/Mac/WSL:**
```bash
bash run_grid_experiments.sh
```

**Windows PowerShell:**
```powershell
.\run_grid_experiments.ps1
```

### Option 3: Manual Single Experiment
Run a single experiment with custom parameters:

```bash
dvc exp run --name "my-experiment" \
    -S model.n_estimators=250 \
    -S model.max_depth=12 \
    -S model.min_samples_split=3 \
    -S model.min_samples_leaf=2
```

## Viewing Results

### Show all experiments
```bash
dvc exp show
```

### Show experiments with specific parameters
```bash
dvc exp show --include-params=model.n_estimators,model.max_depth
```

### Show experiments sorted by accuracy
```bash
dvc exp show --sort-by=metrics.json:accuracy --sort-order=desc
```

### Compare experiments
```bash
dvc exp diff
```

### Compare specific experiments
```bash
dvc exp diff exp-baseline exp-trees-200
```

## Managing Experiments

### Apply best experiment to workspace
```bash
# First, find the best experiment name from dvc exp show
dvc exp apply <experiment-name>
```

### Push experiment to workspace
```bash
dvc exp branch <experiment-name> <branch-name>
git checkout <branch-name>
```

### Clean up experiments
```bash
# Remove specific experiment
dvc exp remove <experiment-name>

# Remove all experiments
dvc exp remove --all

# Garbage collect experiment artifacts
dvc exp gc
```

## Analyzing Results

### View metrics
```bash
dvc metrics show
```

### Compare metrics across experiments
```bash
dvc metrics diff
```

### View plots
```bash
dvc plots show
```

### Compare plots across experiments
```bash
dvc plots diff
```

## Tips for Experimentation

1. **Start with fewer experiments**: Test the scripts with 2-3 experiments first
2. **Monitor resources**: Grid search can create many experiments quickly
3. **Use meaningful names**: Name experiments descriptively for easy comparison
4. **Track git commits**: Each experiment can be associated with a git commit
5. **Clean up regularly**: Remove unsuccessful experiments to keep workspace clean
6. **Document findings**: Keep notes on which parameters work best

## Example Workflow

```bash
# 1. Run baseline
dvc repro

# 2. Run predefined experiments
bash run_experiments.sh

# 3. View results sorted by accuracy
dvc exp show --sort-by=metrics.json:accuracy --sort-order=desc

# 4. Apply the best experiment
dvc exp apply exp-best-one

# 5. Commit the best configuration
git add params.yaml dvc.lock
git commit -m "Apply best model configuration"

# 6. Clean up other experiments
dvc exp gc
```

## Hyperparameter Tuning Guidelines

### For Better Accuracy:
- Increase `n_estimators` (more trees = better but slower)
- Increase `max_depth` (deeper trees capture more patterns)
- Try `criterion="entropy"` instead of "gini"

### For Faster Training:
- Decrease `n_estimators`
- Decrease `max_depth`
- Increase `min_samples_split` and `min_samples_leaf`

### For Preventing Overfitting:
- Decrease `max_depth`
- Increase `min_samples_split`
- Increase `min_samples_leaf`
- Set a reasonable `max_leaf_nodes`
- Increase `min_impurity_decrease`

### For More Robust Models:
- Increase `n_estimators`
- Enable `bootstrap=true`
- Enable `oob_score=true` for out-of-bag validation
