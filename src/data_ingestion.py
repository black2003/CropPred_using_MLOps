import pandas as pd
import yaml
import pickle
import os

def load_params():
    """Load parameters from params.yaml"""
    with open("params.yaml", "r") as f:
        params = yaml.safe_load(f)
    return params

def load_data():
    """
    Loads the dataset from a given CSV file path.

    Returns:
        pd.DataFrame: Loaded dataset as a pandas DataFrame.
    """
    params = load_params()
    file_path = params["data"]["source"]
    
    try:
        df = pd.read_csv(file_path)
        print(f"Data loaded successfully. Shape: {df.shape}")
        
        # Save raw data for next stage
        os.makedirs("data", exist_ok=True)
        with open("data/raw_data.pkl", "wb") as f:
            pickle.dump(df, f)
        
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

if __name__ == "__main__":
    load_data()
