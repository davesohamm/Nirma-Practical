"""
Airflow DAG — Used Car Price Pipeline (Step 1)
Orchestrates: download → validate → preprocess → train
Tools: Apache Airflow
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'mlops',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
}


def download_data():
    """Task 1: Download / load dataset from source."""
    from src.data_pipeline import load_data
    df = load_data()
    print(f"Downloaded {len(df)} records")


def validate_data():
    """Task 2: Validate schema, row counts, column integrity."""
    from src.data_pipeline import load_data, validate_data
    df = load_data()
    validate_data(df)


def preprocess_data():
    """Task 3: Run cleaning and feature engineering pipeline."""
    from src.data_pipeline import run_pipeline
    from src.feature_engineering import run_feature_engineering
    run_pipeline()
    run_feature_engineering()


def trigger_training():
    """Task 4: Kick off model training pipeline."""
    from src.train_model import run_training
    run_training()


# ─── DAG Definition ──────────────────────────────────────────────────────────
with DAG(
    dag_id='car_price_pipeline',
    default_args=default_args,
    description='End-to-end used car price prediction MLOps pipeline',
    schedule_interval='@weekly',  # Runs weekly
    catchup=False,
    tags=['mlops', 'car-price'],
) as dag:

    t1 = PythonOperator(task_id='download_data', python_callable=download_data)
    t2 = PythonOperator(task_id='validate_data', python_callable=validate_data)
    t3 = PythonOperator(task_id='preprocess_data', python_callable=preprocess_data)
    t4 = PythonOperator(task_id='trigger_training', python_callable=trigger_training)

    # Task dependencies
    t1 >> t2 >> t3 >> t4
