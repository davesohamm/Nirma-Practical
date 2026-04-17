"""
User Routes — Prediction history and personal analytics
GET /user/predictions, GET /user/analytics
"""

from fastapi import APIRouter, Depends, Query

from api.auth.dependencies import require_user
from api.services.prediction_service import get_user_predictions
from api.services.analytics_service import get_user_analytics

router = APIRouter()


@router.get("/predictions")
def user_predictions(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: dict = Depends(require_user)
):
    """Get the current user's prediction history (paginated)."""
    return get_user_predictions(current_user["_id"], page, limit)


@router.get("/analytics")
def user_analytics(current_user: dict = Depends(require_user)):
    """Get analytics for the current user."""
    return get_user_analytics(current_user["_id"])
