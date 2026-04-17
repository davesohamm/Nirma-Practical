"""
Step 4: Model Training with MLflow Tracking
Handles: train/test split, candidate models, hyperparameter tuning, evaluation.
Tools: scikit-learn (Pipeline, GridSearchCV), XGBoost, MLflow
"""

import os
import json
import warnings
import numpy as np
import pandas as pd
import joblib
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from xgboost import XGBRegressor

warnings.filterwarnings('ignore')

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
ENGINEERED_DATA_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'car_engineered.csv')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

# MLflow tracking URI — uses env var or falls back to remote server
MLFLOW_TRACKING_URI = os.environ.get('MLFLOW_TRACKING_URI', 'http://localhost:5000')


def mean_absolute_percentage_error(y_true, y_pred):
    """MAPE metric."""
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    mask = y_true != 0
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100


def load_engineered_data():
    """Load engineered dataset and split into X, y."""
    df = pd.read_csv(ENGINEERED_DATA_PATH)
    y = df['selling_price']
    X = df.drop(columns=['selling_price'])
    print(f"[TRAIN] Loaded data: X={X.shape}, y={y.shape}")
    return X, y


def get_candidate_pipelines():
    """
    Step 4.2 — Candidate models wrapped in sklearn Pipelines.
    Each pipeline includes a StandardScaler + model for a clean,
    reproducible training workflow.
    """
    pipelines = {
        'LinearRegression': Pipeline([
            ('scaler', StandardScaler()),
            ('model', LinearRegression())
        ]),
        'RandomForest': Pipeline([
            ('scaler', StandardScaler()),
            ('model', RandomForestRegressor(
                n_estimators=200, max_depth=10, random_state=42, n_jobs=1
            ))
        ]),
        'GradientBoosting': Pipeline([
            ('scaler', StandardScaler()),
            ('model', GradientBoostingRegressor(
                n_estimators=200, max_depth=6, learning_rate=0.1, random_state=42
            ))
        ]),
        'XGBoost': Pipeline([
            ('scaler', StandardScaler()),
            ('model', XGBRegressor(
                n_estimators=300, max_depth=6, learning_rate=0.05,
                random_state=42, n_jobs=1, verbosity=0
            ))
        ]),
    }
    return pipelines


def evaluate_model(y_true, y_pred):
    """Step 4.5 — Compute evaluation metrics."""
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    mape = mean_absolute_percentage_error(y_true, y_pred)
    return {'RMSE': rmse, 'MAE': mae, 'R2': r2, 'MAPE': mape}


def train_and_evaluate(X_train, X_test, y_train, y_test):
    """
    Step 4.3 — Train all candidate pipelines and log to MLflow.
    Returns the best pipeline name and fitted pipeline.
    """
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment('car_price_prediction')

    pipelines = get_candidate_pipelines()
    results = {}
    best_r2 = -np.inf
    best_name = None
    best_pipeline = None

    for name, pipeline in pipelines.items():
        print(f"\n{'─' * 50}")
        print(f"  Training: {name}")
        print(f"{'─' * 50}")

        with mlflow.start_run(run_name=name):
            # Train
            pipeline.fit(X_train, y_train)
            y_pred = pipeline.predict(X_test)

            # Evaluate
            metrics = evaluate_model(y_test, y_pred)
            results[name] = metrics

            # 5-fold Cross Validation (Step 4.4)
            cv_scores = cross_val_score(pipeline, X_train, y_train,
                                        cv=5, scoring='r2', n_jobs=1)

            # Log to MLflow (Step 4.3)
            model_obj = pipeline.named_steps['model']
            params = model_obj.get_params()
            mlflow.log_params({k: v for k, v in params.items()
                              if isinstance(v, (int, float, str, bool))})
            mlflow.log_metrics(metrics)
            mlflow.log_metric('CV_R2_mean', cv_scores.mean())
            mlflow.log_metric('CV_R2_std', cv_scores.std())
            mlflow.sklearn.log_model(pipeline, artifact_path="model")

            print(f"  RMSE:  {metrics['RMSE']:,.0f}")
            print(f"  MAE:   {metrics['MAE']:,.0f}")
            print(f"  R2:    {metrics['R2']:.4f}")
            print(f"  MAPE:  {metrics['MAPE']:.2f}%")
            print(f"  CV R2: {cv_scores.mean():.4f} +/- {cv_scores.std():.4f}")

            if metrics['R2'] > best_r2:
                best_r2 = metrics['R2']
                best_name = name
                best_pipeline = pipeline

    return results, best_name, best_pipeline


def hyperparameter_tuning(X_train, y_train):
    """
    Step 4.4 — Hyperparameter tuning with GridSearchCV for XGBoost.
    Uses sklearn Pipeline inside GridSearchCV.
    """
    print(f"\n{'=' * 60}")
    print("  HYPERPARAMETER TUNING — XGBoost via GridSearchCV + Pipeline")
    print(f"{'=' * 60}")

    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('model', XGBRegressor(random_state=42, n_jobs=1, verbosity=0))
    ])

    # Parameter grid — note: prefixed with 'model__' for pipeline step
    param_grid = {
        'model__n_estimators': [300, 500],
        'model__max_depth': [4, 6],
        'model__learning_rate': [0.05, 0.1],
    }

    grid_search = GridSearchCV(
        pipeline, param_grid, cv=3, scoring='r2',
        n_jobs=1, verbose=1, return_train_score=True
    )
    grid_search.fit(X_train, y_train)

    print(f"\n  Best Params: {grid_search.best_params_}")
    print(f"  Best CV R2:  {grid_search.best_score_:.4f}")

    return grid_search.best_estimator_, grid_search.best_params_


def run_training():
    """Execute the full training pipeline."""
    print("=" * 60)
    print("  MODEL TRAINING — Used Car Price Prediction")
    print("=" * 60)

    X, y = load_engineered_data()

    # Step 4.1 — Train-Test Split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"[SPLIT] Train: {X_train.shape}, Test: {X_test.shape}")

    # Step 4.2-4.3 — Train candidate models + MLflow tracking
    results, best_name, best_pipeline = train_and_evaluate(
        X_train, X_test, y_train, y_test
    )

    # Step 4.4 — Hyperparameter tuning for XGBoost
    tuned_pipeline, tuned_params = hyperparameter_tuning(X_train, y_train)

    # Evaluate tuned model
    y_pred_tuned = tuned_pipeline.predict(X_test)
    tuned_metrics = evaluate_model(y_test, y_pred_tuned)

    print(f"\n{'=' * 60}")
    print("  TUNED XGBOOST RESULTS")
    print(f"{'=' * 60}")
    print(f"  RMSE:  {tuned_metrics['RMSE']:,.0f}")
    print(f"  MAE:   {tuned_metrics['MAE']:,.0f}")
    print(f"  R2:    {tuned_metrics['R2']:.4f}")
    print(f"  MAPE:  {tuned_metrics['MAPE']:.2f}%")

    # Pick the overall best
    if tuned_metrics['R2'] >= results[best_name]['R2']:
        final_pipeline = tuned_pipeline
        final_name = 'XGBoost_Tuned'
        final_metrics = tuned_metrics
    else:
        final_pipeline = best_pipeline
        final_name = best_name
        final_metrics = results[best_name]

    # Log final best to MLflow and register model
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment('car_price_prediction')
    with mlflow.start_run(run_name=f"BEST_{final_name}") as run:
        mlflow.log_params(tuned_params if final_name == 'XGBoost_Tuned' else {})
        mlflow.log_metrics(final_metrics)
        mlflow.sklearn.log_model(
            final_pipeline,
            artifact_path="model",
            registered_model_name="car-price-predictor"
        )
        best_run_id = run.info.run_id

    # Step 4.6 — Save final model as .pkl
    os.makedirs(MODELS_DIR, exist_ok=True)
    model_path = os.path.join(MODELS_DIR, 'car_price_model.pkl')
    joblib.dump(final_pipeline, model_path)

    # Save feature list for inference
    feature_path = os.path.join(MODELS_DIR, 'feature_columns.pkl')
    joblib.dump(X.columns.tolist(), feature_path)

    # Save metrics to JSON for reference
    all_results = {name: {k: float(v) for k, v in m.items()} for name, m in results.items()}
    all_results['XGBoost_Tuned'] = {k: float(v) for k, v in tuned_metrics.items()}
    metrics_path = os.path.join(MODELS_DIR, 'training_metrics.json')
    with open(metrics_path, 'w') as f:
        json.dump({
            'best_model': final_name,
            'best_metrics': {k: float(v) for k, v in final_metrics.items()},
            'all_results': all_results,
            'tuned_params': {k: str(v) for k, v in tuned_params.items()},
            'mlflow_run_id': best_run_id,
        }, f, indent=2)

    print(f"\n{'=' * 60}")
    print(f"  BEST MODEL: {final_name}")
    print(f"  R2 = {final_metrics['R2']:.4f} | RMSE = {final_metrics['RMSE']:,.0f}")
    print(f"  MLflow Run ID: {best_run_id}")
    print(f"  Model saved to {model_path}")
    print(f"  Metrics saved to {metrics_path}")
    print(f"{'=' * 60}")

    return final_pipeline, final_metrics


if __name__ == '__main__':
    run_training()
