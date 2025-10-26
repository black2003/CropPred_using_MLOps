import yaml
import pickle
import json
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score
import seaborn as sns

def load_params():
    """Load parameters from params.yaml"""
    with open("params.yaml", "r") as f:
        params = yaml.safe_load(f)
    return params

def evaluate_model():
    """
    Evaluates the trained model on test data.

    Returns:
        dict: Evaluation metrics.
    """
    params = load_params()
    
    # Load model and test data
    with open("models/model.pkl", "rb") as f:
        model = pickle.load(f)
    
    with open("data/test_features.pkl", "rb") as f:
        X_test = pickle.load(f)
    
    with open("data/test_target.pkl", "rb") as f:
        y_test = pickle.load(f)
    
    with open("data/features.pkl", "rb") as f:
        X = pickle.load(f)
    
    with open("data/target.pkl", "rb") as f:
        y = pickle.load(f)
    
    # Make predictions
    y_pred = model.predict(X_test)

    # Calculate metrics
    acc = accuracy_score(y_test, y_pred)
    
    # Cross-validation
    cv_scores = cross_val_score(model, X, y, cv=params["evaluation"]["cv_folds"])
    cv_mean = np.mean(cv_scores)
    cv_std = np.std(cv_scores)
    
    print("Model evaluation completed.")
    print(f"Accuracy: {acc:.4f}")
    print(f"CV Accuracy: {cv_mean:.4f} (+/- {cv_std * 2:.4f})")
    print("Classification Report:\n", classification_report(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

    # Save metrics
    metrics = {
        "accuracy": float(acc),
        "cv_accuracy_mean": float(cv_mean),
        "cv_accuracy_std": float(cv_std)
    }
    
    os.makedirs("metrics", exist_ok=True)
    with open(params["evaluation"]["metrics_file"], "w") as f:
        json.dump(metrics, f, indent=2)
    
    # Generate plots
    os.makedirs("plots", exist_ok=True)
    
    # Feature importance plot
    feature_importances = pd.Series(model.feature_importances_, index=X.columns)
    plt.figure(figsize=(10, 6))
    feature_importances.sort_values().plot(kind='barh', title="Feature Importance")
    plt.tight_layout()
    plt.savefig("plots/feature_importance.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    # Confusion matrix plot
    plt.figure(figsize=(8, 6))
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig("plots/confusion_matrix.png", dpi=300, bbox_inches='tight')
    plt.close()

    return metrics

if __name__ == "__main__":
    evaluate_model()
