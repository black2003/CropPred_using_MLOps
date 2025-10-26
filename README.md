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
├── app/                            # FastAPI Application
│   ├── main.py                     # FastAPI application
│   ├── test_api.py                 # API test client
│   ├── index.html                  # Web interface
│   ├── start.sh                    # Bash startup script
│   ├── start.ps1                   # PowerShell startup script
│   ├── Dockerfile                  # Docker configuration
│   ├── requirements.txt            # App-specific dependencies
│   └── README.md                   # App documentation
├── run_experiments.sh              # Bash script for 12 experiments
├── run_experiments.ps1             # PowerShell script for 12 experiments
├── run_grid_experiments.sh         # Bash script for grid search (48 experiments)
├── run_grid_experiments.ps1        # PowerShell script for grid search
├── params.yaml                     # Pipeline parameters
├── dvc.yaml                        # DVC pipeline configuration
├── requirements.txt                # Python dependencies
├── EXPERIMENTS_GUIDE.md            # Detailed guide for running experiments
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
- **Model hyperparameters** (11 Random Forest parameters)
- **Training configuration**
- **Output paths**

### Available Hyperparameters
- `n_estimators`: Number of trees in the forest
- `max_depth`: Maximum depth of trees
- `min_samples_split`: Minimum samples to split a node
- `min_samples_leaf`: Minimum samples at leaf nodes
- `max_features`: Features to consider for splits
- `criterion`: Split quality measure (gini/entropy)
- And more... (see `params.yaml` for complete list)

## Running Experiments

### Quick Experiments (12 configurations)
```bash
# Linux/Mac/WSL
bash run_experiments.sh

# Windows PowerShell
.\run_experiments.ps1
```

### Grid Search (48 combinations)
```bash
# Linux/Mac/WSL
bash run_grid_experiments.sh

# Windows PowerShell
.\run_grid_experiments.ps1
```

### View Experiment Results
```bash
# Show all experiments
dvc exp show

# Show sorted by accuracy
dvc exp show --sort-by=metrics.json:accuracy --sort-order=desc

# Compare experiments
dvc exp diff
```

📖 **For detailed experimentation guide, see [EXPERIMENTS_GUIDE.md](EXPERIMENTS_GUIDE.md)**

## FastAPI Application

### Starting the API Server

```bash
# Windows PowerShell
cd app
.\start.ps1

# Linux/Mac/WSL
cd app
bash start.sh

# Or manually
cd app
uvicorn main:app --reload
```

### Using the Application

1. **Web Interface**: Open `app/index.html` in your browser
2. **API Documentation**: Visit `http://localhost:8000/docs`
3. **Test API**: Run `python app/test_api.py`

### API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /model/info` - Model details
- `POST /predict` - Single prediction
- `POST /predict/batch` - Batch predictions

### Example Request

```python
import requests

data = {
    "N": 90, "P": 42, "K": 43,
    "temperature": 20.87, "humidity": 82.00,
    "ph": 6.50, "rainfall": 202.93
}

response = requests.post("http://localhost:8000/predict", json=data)
print(response.json())
```

📖 **For detailed API documentation, see [app/README.md](app/README.md)**

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