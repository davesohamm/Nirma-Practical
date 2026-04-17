"""
Analytics Service — MongoDB aggregation queries.
"""

from datetime import datetime, timezone, timedelta
from api.database.connection import get_db


def get_user_analytics(user_id: str) -> dict:
    """Get analytics for a specific user."""
    db = get_db()

    # Total predictions
    total = db.predictions.count_documents({"user_id": user_id})

    # Average predicted price
    avg_pipeline = [
        {"$match": {"user_id": user_id}},
        {"$group": {"_id": None, "avg_price": {"$avg": "$prediction.predicted_price"}}}
    ]
    avg_result = list(db.predictions.aggregate(avg_pipeline))
    avg_price = round(avg_result[0]["avg_price"], 2) if avg_result else 0.0

    # Most predicted brands (top 5)
    brand_pipeline = [
        {"$match": {"user_id": user_id}},
        {"$project": {
            "brand": {"$arrayElemAt": [{"$split": ["$input.name", " "]}, 0]}
        }},
        {"$group": {"_id": "$brand", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 5}
    ]
    brand_result = list(db.predictions.aggregate(brand_pipeline))
    brands = [{"brand": b["_id"], "count": b["count"]} for b in brand_result]

    # Recent predictions (last 5)
    recent = list(
        db.predictions.find({"user_id": user_id})
        .sort("timestamp", -1)
        .limit(5)
    )
    for doc in recent:
        doc["id"] = str(doc.pop("_id"))

    return {
        "total_predictions": total,
        "avg_predicted_price": avg_price,
        "most_predicted_brands": brands,
        "recent_predictions": recent
    }


def get_admin_metrics() -> dict:
    """Get system-wide admin metrics."""
    db = get_db()

    total_users = db.users.count_documents({})
    total_predictions = db.predictions.count_documents({})

    # Average response time
    avg_rt_pipeline = [
        {"$group": {"_id": None, "avg_rt": {"$avg": "$response_time_ms"}}}
    ]
    avg_rt_result = list(db.predictions.aggregate(avg_rt_pipeline))
    avg_rt = round(avg_rt_result[0]["avg_rt"], 2) if avg_rt_result else 0.0

    # Predictions today
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    predictions_today = db.predictions.count_documents({"timestamp": {"$gte": today}})

    # Active users (users who predicted in last 24h)
    yesterday = datetime.now(timezone.utc) - timedelta(hours=24)
    active_pipeline = [
        {"$match": {"timestamp": {"$gte": yesterday}}},
        {"$group": {"_id": "$user_id"}},
        {"$count": "active"}
    ]
    active_result = list(db.predictions.aggregate(active_pipeline))
    active_users = active_result[0]["active"] if active_result else 0

    return {
        "total_users": total_users,
        "total_predictions": total_predictions,
        "avg_response_time_ms": avg_rt,
        "predictions_today": predictions_today,
        "active_users": active_users
    }
