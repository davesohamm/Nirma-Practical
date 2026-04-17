"""
Prediction Pydantic Schemas — Records, History, Analytics
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class PredictionRecord(BaseModel):
    """Schema for a stored prediction record."""
    id: Optional[str] = Field(None, description="Prediction ID")
    user_id: str = Field(..., description="User who made the prediction")
    input: Dict[str, Any] = Field(..., description="Car input data")
    prediction: Dict[str, Any] = Field(..., description="Prediction result")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    response_time_ms: float = Field(..., description="Inference response time in ms")


class PredictionHistoryResponse(BaseModel):
    """Paginated prediction history."""
    predictions: List[PredictionRecord]
    total: int
    page: int
    limit: int


class UserAnalytics(BaseModel):
    """User-level analytics."""
    total_predictions: int = 0
    avg_predicted_price: float = 0.0
    most_predicted_brands: List[Dict[str, Any]] = []
    recent_predictions: List[PredictionRecord] = []


class AdminMetrics(BaseModel):
    """Admin-level system metrics."""
    total_users: int = 0
    total_predictions: int = 0
    avg_response_time_ms: float = 0.0
    predictions_today: int = 0
    active_users: int = 0
