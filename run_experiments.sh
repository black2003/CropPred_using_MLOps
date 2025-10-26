#!/bin/bash

# Script to run multiple DVC experiments with different hyperparameter settings
# This script runs 10+ experiments with various Random Forest configurations

echo "Starting DVC Experiments for Crop Recommendation Model"
echo "=========================================================="

# Experiment 1: Baseline (default parameters)
echo ""
echo "Experiment 1: Baseline Configuration"
dvc exp run --name "exp-baseline" \
    -S model.n_estimators=100 \
    -S model.max_depth=10 \
    -S model.min_samples_split=2 \
    -S model.min_samples_leaf=1

# Experiment 2: More trees
echo ""
echo "Experiment 2: Increased n_estimators to 200"
dvc exp run --name "exp-trees-200" \
    -S model.n_estimators=200 \
    -S model.max_depth=10 \
    -S model.min_samples_split=2 \
    -S model.min_samples_leaf=1

# Experiment 3: Even more trees
echo ""
echo "Experiment 3: Increased n_estimators to 300"
dvc exp run --name "exp-trees-300" \
    -S model.n_estimators=300 \
    -S model.max_depth=10 \
    -S model.min_samples_split=2 \
    -S model.min_samples_leaf=1

# Experiment 4: Deeper trees
echo ""
echo "Experiment 4: Increased max_depth to 20"
dvc exp run --name "exp-depth-20" \
    -S model.n_estimators=100 \
    -S model.max_depth=20 \
    -S model.min_samples_split=2 \
    -S model.min_samples_leaf=1

# Experiment 5: Very deep trees
echo ""
echo "Experiment 5: Increased max_depth to 30"
dvc exp run --name "exp-depth-30" \
    -S model.n_estimators=100 \
    -S model.max_depth=30 \
    -S model.min_samples_split=2 \
    -S model.min_samples_leaf=1

# Experiment 6: Regularization with min_samples_split
echo ""
echo "Experiment 6: Increased min_samples_split to 5"
dvc exp run --name "exp-split-5" \
    -S model.n_estimators=100 \
    -S model.max_depth=10 \
    -S model.min_samples_split=5 \
    -S model.min_samples_leaf=1

# Experiment 7: More regularization with min_samples_split
echo ""
echo "Experiment 7: Increased min_samples_split to 10"
dvc exp run --name "exp-split-10" \
    -S model.n_estimators=100 \
    -S model.max_depth=10 \
    -S model.min_samples_split=10 \
    -S model.min_samples_leaf=1

# Experiment 8: Regularization with min_samples_leaf
echo ""
echo "Experiment 8: Increased min_samples_leaf to 2"
dvc exp run --name "exp-leaf-2" \
    -S model.n_estimators=100 \
    -S model.max_depth=10 \
    -S model.min_samples_split=2 \
    -S model.min_samples_leaf=2

# Experiment 9: More regularization with min_samples_leaf
echo ""
echo "Experiment 9: Increased min_samples_leaf to 4"
dvc exp run --name "exp-leaf-4" \
    -S model.n_estimators=100 \
    -S model.max_depth=10 \
    -S model.min_samples_split=2 \
    -S model.min_samples_leaf=4

# Experiment 10: Balanced configuration
echo ""
echo "Experiment 10: Balanced - 200 trees, depth 15"
dvc exp run --name "exp-balanced" \
    -S model.n_estimators=200 \
    -S model.max_depth=15 \
    -S model.min_samples_split=5 \
    -S model.min_samples_leaf=2

# Experiment 11: High capacity model
echo ""
echo "Experiment 11: High capacity - 300 trees, depth 25"
dvc exp run --name "exp-high-capacity" \
    -S model.n_estimators=300 \
    -S model.max_depth=25 \
    -S model.min_samples_split=2 \
    -S model.min_samples_leaf=1

# Experiment 12: Regularized model
echo ""
echo "Experiment 12: Highly regularized model"
dvc exp run --name "exp-regularized" \
    -S model.n_estimators=150 \
    -S model.max_depth=8 \
    -S model.min_samples_split=10 \
    -S model.min_samples_leaf=4

echo ""
echo "=========================================================="
echo "All experiments completed!"
echo ""
echo "View results with: dvc exp show"
echo "Compare metrics with: dvc metrics diff"
echo "Generate plots with: dvc plots diff"
echo ""
