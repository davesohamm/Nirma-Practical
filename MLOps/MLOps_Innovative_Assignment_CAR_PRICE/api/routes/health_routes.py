"""
Health & Model Info Routes
GET /health, GET /model-info
"""

from fastapi import APIRouter

from api.models.car import HealthResponse, ModelInfoResponse
from api.services.prediction_service import get_predictor
from api.config import settings

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health():
    """API health check endpoint."""
    predictor = get_predictor()
    return HealthResponse(
        status="healthy",
        model_loaded=predictor.loaded,
        model_version=settings.MODEL_VERSION,
        api_version="2.0.0"
    )


@router.get("/model-info", response_model=ModelInfoResponse)
def model_info():
    """Return model metadata and training info."""
    predictor = get_predictor()
    features = predictor.feature_columns if predictor.feature_columns else []
    return ModelInfoResponse(
        model_name="car-price-predictor",
        model_version=settings.MODEL_VERSION,
        features=features,
        training_dataset="Car details v3.csv (CardDekho)",
        metrics={"R2": "See MLflow", "RMSE": "See MLflow"}
    )
