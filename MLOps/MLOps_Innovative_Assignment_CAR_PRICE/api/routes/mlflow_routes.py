"""
MLflow Routes — Model retraining trigger and MLflow status
POST /admin/retrain, GET /admin/mlflow-status
"""

import os
import json
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from api.auth.dependencies import require_admin
from api.config import settings

router = APIRouter()

# Track retraining state
_retrain_status = {"status": "idle", "message": "No retraining has been triggered yet."}


def _run_retraining():
    """Background task: run the full training pipeline."""
    global _retrain_status
    _retrain_status = {"status": "running", "message": "Model retraining in progress..."}
    try:
        from src.data_pipeline import run_pipeline
        from src.feature_engineering import run_feature_engineering
        from src.train_model import run_training

        print("[RETRAIN] Starting data pipeline...")
        run_pipeline()

        print("[RETRAIN] Starting feature engineering...")
        run_feature_engineering()

        print("[RETRAIN] Starting model training...")
        pipeline, metrics = run_training()

        # Reload the predictor with new model
        from api.services.prediction_service import get_predictor
        predictor = get_predictor()
        predictor.reload_model()

        _retrain_status = {
            "status": "completed",
            "message": "Model retraining completed successfully.",
            "metrics": {k: round(float(v), 4) for k, v in metrics.items()}
        }
        print(f"[RETRAIN] Completed. Metrics: {metrics}")

    except Exception as e:
        _retrain_status = {
            "status": "failed",
            "message": f"Retraining failed: {str(e)}"
        }
        print(f"[RETRAIN] Failed: {e}")


@router.post("/retrain")
def trigger_retrain(
    background_tasks: BackgroundTasks,
    admin: dict = Depends(require_admin)
):
    """Trigger model retraining (admin only). Runs in background."""
    if _retrain_status.get("status") == "running":
        raise HTTPException(status_code=409, detail="Retraining is already in progress.")

    background_tasks.add_task(_run_retraining)
    return {"message": "Model retraining triggered. Check /admin/retrain-status for progress."}


@router.get("/retrain-status")
def retrain_status(admin: dict = Depends(require_admin)):
    """Check the status of model retraining."""
    return _retrain_status


@router.get("/mlflow-status")
def mlflow_status(admin: dict = Depends(require_admin)):
    """Get MLflow experiment info and recent runs."""
    try:
        import mlflow
        mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)

        client = mlflow.tracking.MlflowClient()

        # Get experiment
        experiment = client.get_experiment_by_name("car_price_prediction")
        if not experiment:
            return {
                "connected": True,
                "experiment": None,
                "runs": [],
                "message": "No experiments found. Trigger a retraining to create runs."
            }

        # Get recent runs
        runs = client.search_runs(
            experiment_ids=[experiment.experiment_id],
            order_by=["start_time DESC"],
            max_results=10
        )

        run_list = []
        for run in runs:
            run_list.append({
                "run_id": run.info.run_id,
                "run_name": run.info.run_name,
                "status": run.info.status,
                "start_time": run.info.start_time,
                "metrics": {k: round(v, 4) for k, v in run.data.metrics.items()},
                "params": dict(run.data.params),
            })

        return {
            "connected": True,
            "tracking_uri": settings.MLFLOW_TRACKING_URI,
            "experiment": {
                "name": experiment.name,
                "id": experiment.experiment_id,
            },
            "runs": run_list
        }
    except Exception as e:
        return {
            "connected": False,
            "message": f"Cannot connect to MLflow: {str(e)}"
        }


@router.get("/model-metrics")
def model_metrics():
    """Get current model training metrics from saved JSON."""
    metrics_path = os.path.join(os.path.dirname(__file__), '..', '..', 'models', 'training_metrics.json')
    try:
        with open(metrics_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"message": "No training metrics found. Run training first."}
