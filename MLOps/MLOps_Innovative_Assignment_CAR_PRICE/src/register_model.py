"""
Step 5: Model Registry — Register best model in MLflow.
Tools: MLflow
"""

import os
import mlflow
from mlflow.tracking import MlflowClient

BASE_DIR = os.path.join(os.path.dirname(__file__), '..')


def register_best_model():
    """Step 5.1 — Register the best model in MLflow Model Registry."""
    print("=" * 60)
    print("  MODEL REGISTRY — MLflow Registration")
    print("=" * 60)

    tracking_path = os.path.abspath(os.path.join(BASE_DIR, 'mlruns'))
    mlflow.set_tracking_uri(f'file:///{tracking_path}')
    client = MlflowClient()

    # Find the best run in cat_price_prediction experiment
    experiment = client.get_experiment_by_name('car_price_prediction')
    if experiment is None:
        print("[REGISTRY] No experiment found. Train the model first.")
        return

    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["metrics.R2 DESC"],
        max_results=1
    )

    if not runs:
        print("[REGISTRY] No runs found.")
        return

    best_run = runs[0]
    run_id = best_run.info.run_id
    r2 = best_run.data.metrics.get('R2', 0)
    print(f"[REGISTRY] Best run: {run_id}")
    print(f"[REGISTRY] Best R²: {r2:.4f}")

    # Step 5.1 — Register model
    model_uri = f"runs:/{run_id}/model"
    try:
        result = mlflow.register_model(model_uri, "car-price-predictor")
        print(f"[REGISTRY] Registered model: {result.name} v{result.version}")

        # Step 5.2 — Add metadata tags
        client.set_model_version_tag(
            result.name, result.version, "training_dataset", "Car details v3.csv"
        )
        client.set_model_version_tag(
            result.name, result.version, "R2_score", str(r2)
        )
        client.set_model_version_tag(
            result.name, result.version, "stage", "Production"
        )

        # Transition to Production
        client.transition_model_version_stage(
            name=result.name,
            version=result.version,
            stage="Production"
        )
        print(f"[REGISTRY] Model transitioned to Production stage")

    except Exception as e:
        print(f"[REGISTRY] Registration note: {e}")
        print("[REGISTRY] Model may already be registered from training step.")

    print("[REGISTRY] Done.")


if __name__ == '__main__':
    register_best_model()
