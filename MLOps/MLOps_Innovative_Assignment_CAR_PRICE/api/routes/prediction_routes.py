"""
Prediction Routes — Single and Batch prediction
POST /predict, POST /predict/batch
"""

from fastapi import APIRouter, HTTPException, status, Depends

from api.models.car import (
    CarInput, PredictionOutput,
    BatchCarInput, BatchPredictionOutput
)
from api.services.prediction_service import make_prediction, make_batch_prediction, get_predictor
from api.auth.dependencies import require_user
from api.middleware.metrics import PREDICTION_COUNT, INFERENCE_TIME
from api.config import settings

import time

router = APIRouter()


@router.post("/predict", response_model=PredictionOutput)
def predict(car: CarInput, current_user: dict = Depends(require_user)):
    """Predict the selling price of a used car."""
    predictor = get_predictor()
    if not predictor.loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded. Train the model first."
        )

    try:
        start = time.time()
        result = make_prediction(car, current_user["_id"])
        elapsed = time.time() - start

        # Update Prometheus metrics
        PREDICTION_COUNT.labels(model_version=settings.MODEL_VERSION).inc()
        INFERENCE_TIME.labels(model_version=settings.MODEL_VERSION).observe(elapsed)

        return result["prediction"]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@router.post("/predict/batch", response_model=BatchPredictionOutput)
def predict_batch(batch: BatchCarInput, current_user: dict = Depends(require_user)):
    """Batch prediction for multiple cars."""
    predictor = get_predictor()
    if not predictor.loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded."
        )

    try:
        start = time.time()
        result = make_batch_prediction(batch.cars, current_user["_id"])
        elapsed = time.time() - start

        # Update Prometheus metrics
        PREDICTION_COUNT.labels(model_version=settings.MODEL_VERSION).inc(len(batch.cars))
        INFERENCE_TIME.labels(model_version=settings.MODEL_VERSION).observe(elapsed)

        return BatchPredictionOutput(
            predictions=result["predictions"],
            count=result["count"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch prediction failed: {str(e)}"
        )
