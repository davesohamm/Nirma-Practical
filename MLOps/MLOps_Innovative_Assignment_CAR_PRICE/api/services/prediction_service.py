"""
Prediction Service — Handles prediction logic + MongoDB persistence.
"""

import time
from datetime import datetime, timezone
from typing import List, Optional

from api.database.connection import get_db
from api.predictor import CarPricePredictor
from api.models.car import CarInput, PredictionOutput
# Global predictor instance
predictor = CarPricePredictor()


def get_predictor() -> CarPricePredictor:
    """Return the global predictor instance."""
    return predictor


def make_prediction(car_input: CarInput, user_id: str) -> dict:
    """
    Run prediction and persist to MongoDB.
    
    Returns:
        dict with prediction result and response_time_ms.
    """
    start_time = time.time()
    price = predictor.predict(car_input)
    elapsed_ms = round((time.time() - start_time) * 1000, 2)

    result = PredictionOutput(
        predicted_price=round(price, 2),
        currency="INR",
        model_version=predictor.model_version
    )

    # Persist to MongoDB
    db = get_db()
    record = {
        "user_id": user_id,
        "input": car_input.model_dump(),
        "prediction": result.model_dump(),
        "timestamp": datetime.now(timezone.utc),
        "response_time_ms": elapsed_ms
    }
    db.predictions.insert_one(record)

    return {
        "prediction": result,
        "response_time_ms": elapsed_ms
    }


def make_batch_prediction(car_inputs: List[CarInput], user_id: str) -> dict:
    """Run batch prediction and persist each to MongoDB."""
    results = []
    total_start = time.time()

    for car_input in car_inputs:
        res = make_prediction(car_input, user_id)
        results.append(res["prediction"])

    total_elapsed = round((time.time() - total_start) * 1000, 2)
    return {
        "predictions": results,
        "count": len(results),
        "total_response_time_ms": total_elapsed
    }


def get_user_predictions(user_id: str, page: int = 1, limit: int = 20) -> dict:
    """Fetch paginated predictions for a specific user."""
    db = get_db()
    skip = (page - 1) * limit

    total = db.predictions.count_documents({"user_id": user_id})
    cursor = db.predictions.find({"user_id": user_id}) \
        .sort("timestamp", -1) \
        .skip(skip) \
        .limit(limit)

    predictions = []
    for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        predictions.append(doc)

    return {
        "predictions": predictions,
        "total": total,
        "page": page,
        "limit": limit
    }


def get_all_predictions(page: int = 1, limit: int = 50) -> dict:
    """Fetch all predictions (admin use)."""
    db = get_db()
    skip = (page - 1) * limit

    total = db.predictions.count_documents({})
    cursor = db.predictions.find({}) \
        .sort("timestamp", -1) \
        .skip(skip) \
        .limit(limit)

    predictions = []
    for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        predictions.append(doc)

    return {
        "predictions": predictions,
        "total": total,
        "page": page,
        "limit": limit
    }
