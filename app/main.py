"""
FastAPI Application for Crop Recommendation Prediction
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import pickle
import numpy as np
import pandas as pd
from typing import Dict, List
import os

# Initialize FastAPI app
app = FastAPI(
    title="Crop Recommendation API",
    description="API for predicting suitable crops based on soil and climate conditions",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define input schema
class CropFeatures(BaseModel):
    N: float = Field(..., description="Nitrogen content in soil", ge=0, le=150)
    P: float = Field(..., description="Phosphorus content in soil", ge=0, le=150)
    K: float = Field(..., description="Potassium content in soil", ge=0, le=210)
    temperature: float = Field(..., description="Temperature in Celsius", ge=0, le=50)
    humidity: float = Field(..., description="Relative humidity in percentage", ge=0, le=100)
    ph: float = Field(..., description="pH value of soil", ge=0, le=14)
    rainfall: float = Field(..., description="Rainfall in mm", ge=0, le=300)
    
    class Config:
        schema_extra = {
            "example": {
                "N": 90,
                "P": 42,
                "K": 43,
                "temperature": 20.87,
                "humidity": 82.00,
                "ph": 6.50,
                "rainfall": 202.93
            }
        }

# Define output schema
class CropPrediction(BaseModel):
    predicted_crop: str
    confidence: float
    top_3_predictions: List[Dict[str, float]]
    input_features: Dict[str, float]

# Global variable for model
model = None
feature_names = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
crop_classes = [
    'rice', 'maize', 'chickpea', 'kidneybeans', 'pigeonpeas', 'mothbeans',
    'mungbean', 'blackgram', 'lentil', 'pomegranate', 'banana', 'mango',
    'grapes', 'watermelon', 'muskmelon', 'apple', 'orange', 'papaya',
    'coconut', 'cotton', 'jute', 'coffee'
]

def load_model():
    """Load the trained model"""
    global model
    # Try multiple paths for model location
    possible_paths = [
        "/app/models/model.pkl",  # Docker container path
        os.path.join("..", "models", "model.pkl"),  # Local development path
        "models/model.pkl",  # Current directory
        os.path.join(os.path.dirname(__file__), "..", "models", "model.pkl")  # Relative to app dir
    ]
    
    model_path = None
    for path in possible_paths:
        if os.path.exists(path):
            model_path = path
            break
    
    if model_path is None:
        print(f"Model file not found. Searched paths:")
        for path in possible_paths:
            print(f"  - {path} (exists: {os.path.exists(path)})")
        raise FileNotFoundError("Model file not found in any expected location")
    
    print(f"Loading model from: {model_path}")
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    
    return model

@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    try:
        load_model()
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Error loading model: {e}")
        print("Make sure to train the model first using: dvc repro")

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the HTML frontend"""
    try:
        html_path = os.path.join(os.path.dirname(__file__), "index.html")
        with open(html_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse(content="""
            <html>
                <head><title>Crop Recommendation API</title></head>
                <body>
                    <h1>Welcome to Crop Recommendation API</h1>
                    <p>Version: 1.0.0</p>
                    <h2>API Endpoints:</h2>
                    <ul>
                        <li><a href="/docs">/docs</a> - Interactive API Documentation</li>
                        <li><a href="/health">/health</a> - Health Check</li>
                        <li><a href="/model/info">/model/info</a> - Model Information</li>
                        <li>POST /predict - Single Prediction</li>
                        <li>POST /predict/batch - Batch Prediction</li>
                    </ul>
                </body>
            </html>
        """)

@app.get("/api")
async def api_info():
    """API information endpoint"""
    return {
        "message": "Welcome to Crop Recommendation API",
        "version": "1.0.0",
        "endpoints": {
            "predict": "/predict",
            "health": "/health",
            "model_info": "/model/info",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    model_loaded = model is not None
    return {
        "status": "healthy" if model_loaded else "unhealthy",
        "model_loaded": model_loaded
    }

@app.get("/model/info")
async def model_info():
    """Get model information"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "model_type": type(model).__name__,
        "n_estimators": model.n_estimators,
        "max_depth": model.max_depth,
        "n_features": len(feature_names),
        "feature_names": feature_names,
        "n_classes": len(crop_classes),
        "crop_classes": crop_classes
    }

@app.post("/predict", response_model=CropPrediction)
async def predict_crop(features: CropFeatures):
    """
    Predict suitable crop based on input features
    
    Args:
        features: Soil and climate features
        
    Returns:
        Predicted crop with confidence and top 3 recommendations
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Please train the model first.")
    
    try:
        # Prepare input data
        input_data = np.array([[
            features.N,
            features.P,
            features.K,
            features.temperature,
            features.humidity,
            features.ph,
            features.rainfall
        ]])
        
        # Make prediction
        prediction_idx = model.predict(input_data)[0]
        
        # Get prediction probabilities
        probabilities = model.predict_proba(input_data)[0]
        
        # Convert numeric prediction to crop name
        # The model predicts indices (0, 1, 2...), map to crop names
        if isinstance(prediction_idx, (int, np.integer)):
            predicted_crop = crop_classes[int(prediction_idx)]
        else:
            # If model predicts string directly (unlikely)
            predicted_crop = str(prediction_idx)
        
        # Get top 3 predictions
        top_3_indices = np.argsort(probabilities)[-3:][::-1]
        top_3_predictions = [
            {
                "crop": crop_classes[idx],
                "confidence": float(probabilities[idx])
            }
            for idx in top_3_indices
        ]
        
        # Get confidence for predicted class
        confidence = float(probabilities[int(prediction_idx)])
        
        return CropPrediction(
            predicted_crop=predicted_crop,
            confidence=confidence,
            top_3_predictions=top_3_predictions,
            input_features={
                "N": features.N,
                "P": features.P,
                "K": features.K,
                "temperature": features.temperature,
                "humidity": features.humidity,
                "ph": features.ph,
                "rainfall": features.rainfall
            }
        )
        
    except Exception as e:
        import traceback
        error_detail = f"Prediction error: {str(e)}\n{traceback.format_exc()}"
        print(error_detail)  # Log to console
        raise HTTPException(status_code=500, detail=error_detail)

@app.post("/predict/batch")
async def predict_batch(features_list: List[CropFeatures]):
    """
    Predict crops for multiple samples
    
    Args:
        features_list: List of soil and climate features
        
    Returns:
        List of predictions
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        predictions = []
        for features in features_list:
            # Prepare input data
            input_data = np.array([[
                features.N, features.P, features.K,
                features.temperature, features.humidity,
                features.ph, features.rainfall
            ]])
            
            # Make prediction
            prediction_idx = model.predict(input_data)[0]
            probabilities = model.predict_proba(input_data)[0]
            
            # Convert numeric prediction to crop name
            if isinstance(prediction_idx, (int, np.integer)):
                predicted_crop = crop_classes[int(prediction_idx)]
            else:
                predicted_crop = str(prediction_idx)
            
            confidence = float(probabilities[int(prediction_idx)])
            
            predictions.append({
                "predicted_crop": predicted_crop,
                "confidence": confidence,
                "input_features": features.dict()
            })
        
        return {"predictions": predictions, "count": len(predictions)}
        
    except Exception as e:
        import traceback
        error_detail = f"Batch prediction error: {str(e)}\n{traceback.format_exc()}"
        print(error_detail)  # Log to console
        raise HTTPException(status_code=500, detail=error_detail)

