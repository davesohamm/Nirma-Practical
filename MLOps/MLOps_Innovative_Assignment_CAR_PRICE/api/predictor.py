"""
Step 6.3 — Model Loading and Inference Logic
Loads the trained sklearn Pipeline and performs predictions.
Supports dynamic model reloading after retraining.
Tools: joblib, pandas, scikit-learn Pipeline
"""

import os
import json
import numpy as np
import pandas as pd
import joblib

BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
MODELS_DIR = os.path.join(BASE_DIR, 'models')


class CarPricePredictor:
    """Encapsulates model loading and prediction logic with hot-reload support."""

    def __init__(self):
        self.pipeline = None      # sklearn Pipeline (scaler + model)
        self.encoders = None
        self.feature_columns = None
        self.loaded = False
        self.model_version = "v1.0"
        self._load_model()

    def _load_model(self):
        """Load the trained Pipeline and encoders."""
        try:
            model_path = os.path.join(MODELS_DIR, 'car_price_model.pkl')
            encoder_path = os.path.join(MODELS_DIR, 'encoder.pkl')
            feature_path = os.path.join(MODELS_DIR, 'feature_columns.pkl')

            self.pipeline = joblib.load(model_path)
            self.encoders = joblib.load(encoder_path)
            self.feature_columns = joblib.load(feature_path)
            self.loaded = True

            # Load model version from training metrics if available
            metrics_path = os.path.join(MODELS_DIR, 'training_metrics.json')
            if os.path.exists(metrics_path):
                with open(metrics_path, 'r') as f:
                    metrics_data = json.load(f)
                    self.model_version = metrics_data.get('best_model', 'v1.0')

            print(f"[PREDICTOR] Model loaded from {model_path}")
            print(f"[PREDICTOR] Model version: {self.model_version}")
            print(f"[PREDICTOR] Features: {self.feature_columns}")
        except Exception as e:
            print(f"[PREDICTOR] Error loading model: {e}")
            self.loaded = False

    def reload_model(self):
        """Hot-reload the model after retraining."""
        print("[PREDICTOR] Reloading model...")
        self._load_model()
        return self.loaded

    def preprocess(self, car_input) -> pd.DataFrame:
        """Transform raw car input into model-ready features."""
        data = {
            'year': car_input.year,
            'km_driven': car_input.km_driven,
            'mileage': car_input.mileage,
            'engine': car_input.engine,
            'max_power': car_input.max_power,
            'seats': car_input.seats,
        }

        # Derived features (Step 3.1)
        data['car_age'] = 2025 - car_input.year
        data['is_first_owner'] = 1 if car_input.owner == 'First Owner' else 0

        # Label encoding for owner and seller_type (Step 3.2)
        if 'owner' in self.encoders:
            le_owner = self.encoders['owner']
            owner_val = car_input.owner if car_input.owner in le_owner.classes_ else le_owner.classes_[0]
            data['owner'] = le_owner.transform([owner_val])[0]
        else:
            data['owner'] = 0

        if 'seller_type' in self.encoders:
            le_seller = self.encoders['seller_type']
            seller_val = car_input.seller_type if car_input.seller_type in le_seller.classes_ else le_seller.classes_[0]
            data['seller_type'] = le_seller.transform([seller_val])[0]
        else:
            data['seller_type'] = 0

        # One-hot encoding for fuel and transmission (Step 3.2)
        fuel_types = ['Diesel', 'Electric', 'LPG', 'Petrol']
        for ft in fuel_types:
            data[f'fuel_{ft}'] = 1 if car_input.fuel == ft else 0

        data['transmission_Manual'] = 1 if car_input.transmission == 'Manual' else 0

        # Target encoding for brand (Step 3.2)
        brand = car_input.name.split()[0] if car_input.name else 'Unknown'
        brand_map = self.encoders.get('brand_target', {})
        data['brand_encoded'] = brand_map.get(brand, np.mean(list(brand_map.values())) if brand_map else 0)

        # Build dataframe with correct column order
        df = pd.DataFrame([data])

        # Ensure all expected columns exist
        for col in self.feature_columns:
            if col not in df.columns:
                df[col] = 0

        # Select and order columns to match training
        df = df[self.feature_columns]

        return df

    def predict(self, car_input) -> float:
        """Run prediction through the full sklearn Pipeline."""
        features = self.preprocess(car_input)
        prediction = self.pipeline.predict(features)[0]
        return max(float(prediction), 0)

    def predict_batch(self, car_inputs) -> list:
        """Batch prediction."""
        return [self.predict(car) for car in car_inputs]

    def get_model_info(self) -> dict:
        """Return model metadata."""
        metrics_path = os.path.join(MODELS_DIR, 'training_metrics.json')
        metrics = {}
        if os.path.exists(metrics_path):
            with open(metrics_path, 'r') as f:
                metrics = json.load(f)
        return {
            "loaded": self.loaded,
            "model_version": self.model_version,
            "feature_count": len(self.feature_columns) if self.feature_columns else 0,
            "features": self.feature_columns or [],
            "training_metrics": metrics.get("best_metrics", {}),
        }
