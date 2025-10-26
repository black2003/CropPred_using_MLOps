import pandas as pd
import yaml
import pickle
import os
from sklearn.preprocessing import LabelEncoder

def load_params():
    """Load parameters from params.yaml"""
    with open("params.yaml", "r") as f:
        params = yaml.safe_load(f)
    return params

def preprocess_data():
    """
    Cleans and preprocesses the dataset.

    Steps:
        - Handles missing values (if any)
        - Encodes categorical columns (e.g., 'label')

    Returns:
        pd.DataFrame: Preprocessed dataset.
    """
    params = load_params()
    
    # Load raw data
    with open("data/raw_data.pkl", "rb") as f:
        df = pickle.load(f)
    
    # Drop duplicates if configured
    if params["preprocessing"]["drop_duplicates"]:
        df = df.drop_duplicates()

    # Fill missing values if they exist
    if params["preprocessing"]["fill_missing_strategy"] == "median":
        df = df.fillna(df.median(numeric_only=True))

    # Encode target column
    target_col = params["preprocessing"]["target_column"]
    if target_col in df.columns and params["preprocessing"]["encode_categorical"]:
        le = LabelEncoder()
        df[target_col] = le.fit_transform(df[target_col])

    print("Data preprocessing completed.")
    
    # Save processed data
    with open("data/processed_data.pkl", "wb") as f:
        pickle.dump(df, f)
    
    return df

if __name__ == "__main__":
    preprocess_data()
