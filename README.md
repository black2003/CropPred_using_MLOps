# MLOps Pipeline for Crop Recommendation

This project implements a complete MLOps pipeline for crop recommendation using DVC (Data Version Control) for pipeline management and reproducibility.

## Project Structure

```
├── data/
│   ├── Crop_recommendation.csv     # Original dataset (tracked by DVC)
│   └── *.pkl                       # Intermediate data files (generated)
├── models/
│   └── model.pkl                   # Trained model (generated)
├── plots/
│   ├── feature_importance.png      # Feature importance visualization
│   └── confusion_matrix.png        # Confusion matrix visualization
├── metrics/
│   └── metrics.json                # Model evaluation metrics
├── src/                            # Source code directory
│   ├── data_ingestion.py           # Data loading stage
│   ├── data_preprocessing.py       # Data cleaning and preprocessing
│   ├── feature_engineering.py     # Feature and target separation
│   ├── model_engineering.py       # Model training
│   ├── model_evaluation.py        # Model evaluation and visualization
│   └── run_pipeline.py            # Complete pipeline runner
├── params.yaml                     # Pipeline parameters
├── dvc.yaml                        # DVC pipeline configuration
├── requirements.txt                # Python dependencies
└── MLOPS.ipynb                     # Jupyter notebook version
```

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize DVC (if not already done):**
   ```bash
   dvc init
   ```

3. **Pull data (if using DVC remote):**
   ```bash
   dvc pull
   ```

## Running the Pipeline

### Option 1: Using DVC (Recommended)
```bash
dvc repro
```

### Option 2: Using the custom runner
```bash
python src/run_pipeline.py
```

### Option 3: Running individual stages
```bash
python src/data_ingestion.py
python src/data_preprocessing.py
python src/feature_engineering.py
python src/model_engineering.py
python src/model_evaluation.py
```

## Pipeline Stages

1. **Data Ingestion** (`src/data_ingestion.py`)
   - Loads the crop recommendation dataset
   - Saves raw data for downstream processing

2. **Data Preprocessing** (`src/data_preprocessing.py`)
   - Removes duplicates
   - Handles missing values using median imputation
   - Encodes categorical target labels

3. **Feature Engineering** (`src/feature_engineering.py`)
   - Separates features from target variable
   - Prepares data for model training

4. **Model Training** (`src/model_engineering.py`)
   - Splits data into train/test sets
   - Trains a Random Forest classifier
   - Saves the trained model

5. **Model Evaluation** (`src/model_evaluation.py`)
   - Evaluates model performance on test set
   - Performs cross-validation
   - Generates visualizations and metrics

## Configuration

All pipeline parameters are centralized in `params.yaml`:

- **Data paths and preprocessing settings**
- **Model hyperparameters**
- **Training configuration**
- **Output paths**

## Outputs

- **Model:** `models/model.pkl`
- **Metrics:** `metrics/metrics.json`
- **Visualizations:** 
  - `plots/feature_importance.png`
  - `plots/confusion_matrix.png`

## DVC Pipeline

The pipeline is defined in `dvc.yaml` with proper dependency tracking:
- Each stage has clearly defined inputs, outputs, and parameters
- Changes to code, data, or parameters trigger re-execution of affected stages
- Reproducible and version-controlled ML workflow

## Dependencies

See `requirements.txt` for the complete list of Python packages required.

## Version Control

- **Git:** Tracks code, configuration, and small files
- **DVC:** Tracks large data files and model artifacts
- **Parameters:** Centralized in `params.yaml` for easy experimentation