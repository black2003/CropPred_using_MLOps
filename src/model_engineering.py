import yaml
import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def load_params():
    """Load parameters from params.yaml"""
    with open("../params.yaml", "r") as f:
        params = yaml.safe_load(f)
    return params

def train_model():
    """
    Trains a Random Forest Classifier on the dataset.

    Returns:
        model (RandomForestClassifier): Trained model.
        X_test, y_test: Test data for evaluation.
    """
    params = load_params()
    
    # Load features and target
    with open("../data/features.pkl", "rb") as f:
        X = pickle.load(f)
    
    with open("../data/target.pkl", "rb") as f:
        y = pickle.load(f)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=params["training"]["test_size"], 
        random_state=params["training"]["random_state"]
    )

    model = RandomForestClassifier(
        n_estimators=params["model"]["n_estimators"], 
        random_state=params["model"]["random_state"]
    )

    model.fit(X_train, y_train)
    print("Model training completed.")
    
    # Save model and test data
    os.makedirs("../models", exist_ok=True)
    with open("../models/model.pkl", "wb") as f:
        pickle.dump(model, f)
    
    with open("../data/test_features.pkl", "wb") as f:
        pickle.dump(X_test, f)
    
    with open("../data/test_target.pkl", "wb") as f:
        pickle.dump(y_test, f)

    return model, X_test, y_test

if __name__ == "__main__":
    train_model()
