#!/bin/bash

# Script to initialize DVC remote storage with data
# Run this once to push your data to S3

# Change to project root directory (parent of scripts/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.." || exit 1

echo "DVC Data Initialization Script"
echo "==============================="
echo ""
echo "Working directory: $(pwd)"
echo ""

# Check if data file exists
if [ ! -f "data/Crop_recommendation.csv" ]; then
    echo "Error: data/Crop_recommendation.csv not found!"
    echo "Please ensure the data file exists before running this script."
    exit 1
fi

echo "Data file found: data/Crop_recommendation.csv"
echo ""

# Check if DVC is initialized
if [ ! -d ".dvc" ]; then
    echo "Initializing DVC..."
    dvc init
fi

# Check if data is tracked by DVC
if [ ! -f "data/Crop_recommendation.csv.dvc" ]; then
    echo "Adding data to DVC tracking..."
    dvc add data/Crop_recommendation.csv
    git add data/Crop_recommendation.csv.dvc data/.gitignore
    git commit -m "Add data to DVC tracking"
fi

echo ""
echo "Configuring DVC remote..."
echo "Note: You need to set your S3 bucket URL"
echo ""

# Prompt for S3 URL if not set
if [ -z "$DVC_S3_URL" ]; then
    echo "Please enter your S3 bucket URL (e.g., s3://my-bucket/dvc-storage):"
    read -r DVC_S3_URL
fi

# Configure remote
dvc remote add -d -f myremote "$DVC_S3_URL"

echo ""
echo "Pushing data to DVC remote..."
dvc push

echo ""
echo "==============================="
echo "Data initialization complete!"
echo "==============================="
echo ""
echo "The data has been pushed to: $DVC_S3_URL"
echo ""
echo "Next steps:"
echo "1. Commit the DVC configuration:"
echo "   git add .dvc/config"
echo "   git commit -m 'Configure DVC remote'"
echo "   git push"
echo ""
echo "2. The CI/CD pipeline will now be able to pull the data"
echo ""
