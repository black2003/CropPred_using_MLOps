"""
Unit tests for Crop Recommendation API using FastAPI TestClient
"""
import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add parent directory to path to import main
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import app

# Create test client
client = TestClient(app)

def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "endpoints" in data

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "model_loaded" in data

def test_model_info():
    """Test model info endpoint"""
    response = client.get("/model/info")
    # Will return 503 if model not loaded, which is okay in CI
    assert response.status_code in [200, 503]
    
    if response.status_code == 200:
        data = response.json()
        assert "model_type" in data
        assert "n_features" in data
        assert "feature_names" in data

def test_predict_valid_input():
    """Test prediction with valid input"""
    data = {
        "N": 90,
        "P": 42,
        "K": 43,
        "temperature": 20.87,
        "humidity": 82.00,
        "ph": 6.50,
        "rainfall": 202.93
    }
    
    response = client.post("/predict", json=data)
    
    # Will return 503 if model not loaded
    if response.status_code == 200:
        result = response.json()
        assert "predicted_crop" in result
        assert "confidence" in result
        assert "top_3_predictions" in result
        assert "input_features" in result
        assert len(result["top_3_predictions"]) == 3
    else:
        assert response.status_code == 503

def test_predict_invalid_input():
    """Test prediction with invalid input (out of range)"""
    data = {
        "N": -10,  # Invalid: negative
        "P": 42,
        "K": 43,
        "temperature": 20.87,
        "humidity": 82.00,
        "ph": 6.50,
        "rainfall": 202.93
    }
    
    response = client.post("/predict", json=data)
    assert response.status_code == 422  # Validation error

def test_predict_missing_field():
    """Test prediction with missing required field"""
    data = {
        "N": 90,
        "P": 42,
        # Missing K
        "temperature": 20.87,
        "humidity": 82.00,
        "ph": 6.50,
        "rainfall": 202.93
    }
    
    response = client.post("/predict", json=data)
    assert response.status_code == 422  # Validation error

def test_predict_batch_valid():
    """Test batch prediction with valid inputs"""
    data = [
        {
            "N": 90, "P": 42, "K": 43,
            "temperature": 20.87, "humidity": 82.00,
            "ph": 6.50, "rainfall": 202.93
        },
        {
            "N": 80, "P": 50, "K": 40,
            "temperature": 15.5, "humidity": 60.0,
            "ph": 6.8, "rainfall": 80.0
        }
    ]
    
    response = client.post("/predict/batch", json=data)
    
    # Will return 503 if model not loaded
    if response.status_code == 200:
        result = response.json()
        assert "predictions" in result
        assert "count" in result
        assert result["count"] == 2
        assert len(result["predictions"]) == 2
    else:
        assert response.status_code == 503

def test_input_validation_ranges():
    """Test input validation for all fields"""
    # Test N out of range
    data = {
        "N": 200,  # Max is 150
        "P": 42,
        "K": 43,
        "temperature": 20.87,
        "humidity": 82.00,
        "ph": 6.50,
        "rainfall": 202.93
    }
    response = client.post("/predict", json=data)
    assert response.status_code == 422

    # Test pH out of range
    data = {
        "N": 90,
        "P": 42,
        "K": 43,
        "temperature": 20.87,
        "humidity": 82.00,
        "ph": 15.0,  # Max is 14
        "rainfall": 202.93
    }
    response = client.post("/predict", json=data)
    assert response.status_code == 422

    # Test humidity out of range
    data = {
        "N": 90,
        "P": 42,
        "K": 43,
        "temperature": 20.87,
        "humidity": 120.00,  # Max is 100
        "ph": 6.50,
        "rainfall": 202.93
    }
    response = client.post("/predict", json=data)
    assert response.status_code == 422

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
