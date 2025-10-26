"""
Test client for Crop Recommendation API
"""
import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_root():
    """Test root endpoint"""
    print("Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_health():
    """Test health check"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_model_info():
    """Test model info endpoint"""
    print("Testing model info endpoint...")
    response = requests.get(f"{BASE_URL}/model/info")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_single_prediction():
    """Test single prediction"""
    print("Testing single prediction...")
    
    # Example 1: Rice
    data = {
        "N": 90,
        "P": 42,
        "K": 43,
        "temperature": 20.87,
        "humidity": 82.00,
        "ph": 6.50,
        "rainfall": 202.93
    }
    
    response = requests.post(f"{BASE_URL}/predict", json=data)
    print(f"Status: {response.status_code}")
    print(f"Input: {json.dumps(data, indent=2)}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_multiple_predictions():
    """Test multiple different predictions"""
    print("Testing multiple different crop scenarios...")
    
    test_cases = [
        {
            "name": "Rice-favorable conditions",
            "data": {
                "N": 90, "P": 42, "K": 43,
                "temperature": 20.87, "humidity": 82.00,
                "ph": 6.50, "rainfall": 202.93
            }
        },
        {
            "name": "Wheat-favorable conditions",
            "data": {
                "N": 80, "P": 50, "K": 40,
                "temperature": 15.5, "humidity": 60.0,
                "ph": 6.8, "rainfall": 80.0
            }
        },
        {
            "name": "Cotton-favorable conditions",
            "data": {
                "N": 120, "P": 40, "K": 60,
                "temperature": 28.0, "humidity": 70.0,
                "ph": 7.2, "rainfall": 120.0
            }
        },
        {
            "name": "Apple-favorable conditions",
            "data": {
                "N": 20, "P": 135, "K": 200,
                "temperature": 22.5, "humidity": 90.0,
                "ph": 6.0, "rainfall": 180.0
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{test_case['name']}:")
        response = requests.post(f"{BASE_URL}/predict", json=test_case['data'])
        if response.status_code == 200:
            result = response.json()
            print(f"  Predicted Crop: {result['predicted_crop']}")
            print(f"  Confidence: {result['confidence']:.2%}")
            print(f"  Top 3 Predictions:")
            for pred in result['top_3_predictions']:
                print(f"    - {pred['crop']}: {pred['confidence']:.2%}")
        else:
            print(f"  Error: {response.status_code}")

def test_batch_prediction():
    """Test batch prediction"""
    print("\n\nTesting batch prediction...")
    
    batch_data = [
        {
            "N": 90, "P": 42, "K": 43,
            "temperature": 20.87, "humidity": 82.00,
            "ph": 6.50, "rainfall": 202.93
        },
        {
            "N": 80, "P": 50, "K": 40,
            "temperature": 15.5, "humidity": 60.0,
            "ph": 6.8, "rainfall": 80.0
        },
        {
            "N": 120, "P": 40, "K": 60,
            "temperature": 28.0, "humidity": 70.0,
            "ph": 7.2, "rainfall": 120.0
        }
    ]
    
    response = requests.post(f"{BASE_URL}/predict/batch", json=batch_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Number of predictions: {result['count']}")
        for i, pred in enumerate(result['predictions'], 1):
            print(f"\nSample {i}:")
            print(f"  Predicted Crop: {pred['predicted_crop']}")
            print(f"  Confidence: {pred['confidence']:.2%}")
    else:
        print(f"Response: {json.dumps(response.json(), indent=2)}\n")

if __name__ == "__main__":
    print("=" * 60)
    print("Crop Recommendation API - Test Client")
    print("=" * 60)
    print("\nMake sure the API server is running:")
    print("  cd app")
    print("  uvicorn main:app --reload")
    print("\n" + "=" * 60 + "\n")
    
    try:
        test_root()
        test_health()
        test_model_info()
        test_single_prediction()
        test_multiple_predictions()
        test_batch_prediction()
        
        print("\n" + "=" * 60)
        print("All tests completed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to API server.")
        print("Please start the server first:")
        print("  cd app")
        print("  uvicorn main:app --reload")
    except Exception as e:
        print(f"\nError during testing: {e}")
