#!/bin/bash

# Grid Search Style DVC Experiments
# Tests combinations of key hyperparameters

echo "Starting Grid Search DVC Experiments"
echo "======================================"

# Define parameter grids
n_estimators=(50 100 150 200)
max_depth=(5 10 15 20)
min_samples_split=(2 5 10)

# Counter for experiment numbering
exp_num=1

# Grid search over key parameters
for n_est in "${n_estimators[@]}"; do
    for depth in "${max_depth[@]}"; do
        for split in "${min_samples_split[@]}"; do
            echo ""
            echo "Experiment ${exp_num}: n_estimators=${n_est}, max_depth=${depth}, min_samples_split=${split}"
            
            dvc exp run --name "grid-exp-${exp_num}" \
                -S model.n_estimators=${n_est} \
                -S model.max_depth=${depth} \
                -S model.min_samples_split=${split} \
                -S model.min_samples_leaf=1
            
            exp_num=$((exp_num + 1))
            
            # Optional: Uncomment to limit number of experiments
            # if [ ${exp_num} -gt 20 ]; then
            #     break 3
            # fi
        done
    done
done

echo ""
echo "======================================"
echo "Grid search completed! Total experiments: $((exp_num - 1))"
echo ""
echo "View all results:"
echo "  dvc exp show --include-params=model"
echo "  dvc exp show --sort-by=metrics.json:accuracy --sort-order=desc"
echo ""
