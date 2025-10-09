import pandas as pd
import yaml
import pickle

def load_params():
    """Load parameters from params.yaml"""
    with open("../params.yaml", "r") as f:
        params = yaml.safe_load(f)
    return params

def split_features_and_target():
    """
    Splits dataset into input features (X) and target variable (y).

    Returns:
        tuple: X (features), y (target)
    """
    params = load_params()
    target_col = params["preprocessing"]["target_column"]
    
    # Load processed data
    with open("../data/processed_data.pkl", "rb") as f:
        df = pickle.load(f)
    
    X = df.drop(columns=[target_col])
    y = df[target_col]

    print("Feature and target split completed.")
    
    # Save features and target
    with open("../data/features.pkl", "wb") as f:
        pickle.dump(X, f)
    
    with open("../data/target.pkl", "wb") as f:
        pickle.dump(y, f)
    
    return X, y

if __name__ == "__main__":
    split_features_and_target()
