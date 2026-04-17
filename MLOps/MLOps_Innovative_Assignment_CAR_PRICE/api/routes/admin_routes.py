"""
Admin Routes — System-wide analytics and management
GET /admin/predictions, GET /admin/users, GET /admin/metrics
"""

from fastapi import APIRouter, Depends, Query

from api.auth.dependencies import require_admin
from api.services.prediction_service import get_all_predictions
from api.services.user_service import get_all_users
from api.services.analytics_service import get_admin_metrics

router = APIRouter()


@router.get("/predictions")
def admin_predictions(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=200, description="Items per page"),
    admin: dict = Depends(require_admin)
):
    """Get all predictions across all users (admin only)."""
    return get_all_predictions(page, limit)


@router.get("/users")
def admin_users(admin: dict = Depends(require_admin)):
    """Get list of all registered users (admin only)."""
    return get_all_users()


@router.get("/metrics")
def admin_metrics(admin: dict = Depends(require_admin)):
    """Get system-wide metrics summary (admin only)."""
    return get_admin_metrics()
