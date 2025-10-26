import yaml
import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def load_params():
    """Load parameters from params.yaml"""
    with open("params.yaml", "r") as f:
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
    with open("data/features.pkl", "rb") as f:
        X = pickle.load(f)
    
    with open("data/target.pkl", "rb") as f:
        y = pickle.load(f)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=params["training"]["test_size"], 
        random_state=params["training"]["random_state"]
    )

    # Extract model parameters
    model_params = params["model"]
    
    model = RandomForestClassifier(
        n_estimators=model_params["n_estimators"],
        max_depth=model_params["max_depth"] if model_params["max_depth"] is not None else None,
        min_samples_split=model_params["min_samples_split"],
        min_samples_leaf=model_params["min_samples_leaf"],
        max_features=model_params["max_features"],
        max_leaf_nodes=model_params["max_leaf_nodes"] if model_params["max_leaf_nodes"] is not None else None,
        min_impurity_decrease=model_params["min_impurity_decrease"],
        bootstrap=model_params["bootstrap"],
        oob_score=model_params["oob_score"],
        criterion=model_params["criterion"],
        random_state=model_params["random_state"]
    )

    model.fit(X_train, y_train)
    print("Model training completed.")
    print(f"Model parameters: n_estimators={model_params['n_estimators']}, max_depth={model_params['max_depth']}, "
          f"min_samples_split={model_params['min_samples_split']}, min_samples_leaf={model_params['min_samples_leaf']}")
    
    # Save model and test data
    os.makedirs("models", exist_ok=True)
    with open("models/model.pkl", "wb") as f:
        pickle.dump(model, f)
    
    with open("data/test_features.pkl", "wb") as f:
        pickle.dump(X_test, f)
    
    with open("data/test_target.pkl", "wb") as f:
        pickle.dump(y_test, f)

    return model, X_test, y_test

if __name__ == "__main__":
    train_model()
