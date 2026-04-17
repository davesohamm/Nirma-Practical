# 🚗 Used Car Price Prediction — Run Instructions

## Prerequisites

- Python 3.10+ with virtual environment
- All dependencies installed: `pip install -r requirements.txt`
- **Nginx** installed (see `nginx-1.28.2/` bundled in project)

---

## Quick Start (Run Everything)

Open a terminal in the project root (`e:\Nirma\Sem_2\MLOps\car_price_mlops`) and run:

```bash
# Activate virtual environment
venv\Scripts\activate

# Step 1: Data Pipeline — Load, clean, preprocess raw data
python -m src.data_pipeline

# Step 2: Feature Engineering — Encoding, scaling, feature selection
python -m src.feature_engineering

# Step 3: Model Training — Train 4 models + GridSearchCV + MLflow tracking
python -m src.train_model

# Step 4: Model Registry — Register best model in MLflow
python -m src.register_model

# Step 5: Start Flask API via Waitress (backend on http://127.0.0.1:8000)
python -m api.serve

# Step 6: Start Nginx Reverse Proxy (port 80 → port 8000)
#   Open a NEW terminal (Admin privileges recommended):
cd nginx-1.28.2
nginx.exe

# Step 7: Start Streamlit Dashboard (runs on http://localhost:8501)
#   Open a NEW terminal, activate venv, then:
python -m streamlit run ui/app.py --server.port 8501
```
  
---

## Step-by-Step Details

### Step 1: Data Pipeline (`src/data_pipeline.py`)

Loads raw data from `Dataset/Car details v3.csv`, validates schema, cleans data:
- Strips units from mileage, engine, max_power columns
- Imputes missing values (median for numeric, mode for categorical)
- Removes outliers using IQR method + domain rules
- Deduplicates rows

**Output:** `data/processed/car_cleaned.csv` (~6,479 rows × 12 columns)

```bash
python -m src.data_pipeline
```

---

### Step 2: Feature Engineering (`src/feature_engineering.py`)

Creates derived features and encodes/scales data:
- Derives: `car_age`, `brand`, `model_name`, `price_per_km`, `is_first_owner`
- Label encodes: `owner`, `seller_type`
- One-hot encodes: `fuel`, `transmission`
- Target encodes: `brand`
- Standard scales: `km_driven`, `engine`, `max_power`, `mileage`
- Removes highly correlated features (threshold > 0.90)

**Output:**
- `data/processed/car_engineered.csv`
- `models/encoder.pkl`, `models/scaler.pkl`

```bash
python -m src.feature_engineering
```

---

### Step 3: Model Training (`src/train_model.py`)

Trains 4 candidate models with MLflow experiment tracking:
- Linear Regression
- Random Forest
- Gradient Boosting
- XGBoost

Then performs GridSearchCV hyperparameter tuning on XGBoost (5-fold CV, 18 combinations).

**Expected Results:**

| Model             | R²     | RMSE     | MAE      | MAPE    |
|-------------------|--------|----------|----------|---------|
| Linear Regression | 0.7311 | 132,730  | 103,332  | 37.66%  |
| Random Forest     | 0.8853 | 86,689   | 60,578   | 16.80%  |
| Gradient Boosting | 0.8922 | 84,029   | 57,523   | 15.98%  |
| XGBoost           | 0.8918 | 84,182   | 57,673   | 16.20%  |
| **XGBoost_Tuned** | **0.9004** | **80,788** | **56,084** | **15.52%** |

**Output:**
- `models/car_price_model.pkl` (best model pipeline)
- `models/feature_columns.pkl` (feature list for inference)
- `models/training_metrics.json` (all metrics)
- `mlruns/` (MLflow experiment data)

```bash
python -m src.train_model
```

---

### Step 4: Model Registry (`src/register_model.py`)

Registers the best model in MLflow Model Registry and transitions it to Production stage.

```bash
python -m src.register_model
```

---

### Step 5: Flask API + Waitress (`api/main.py`, `api/serve.py`)

The Flask app is served via **Waitress** (production WSGI server).

REST API endpoints:
- `POST /predict` — Single car price prediction
- `POST /predict/batch` — Batch prediction
- `GET /health` — API health check
- `GET /model-info` — Model metadata

**Start Waitress backend:**
```bash
python -m api.serve
```

**Test prediction:**
```bash
curl -X POST http://localhost:8000/predict ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Maruti Swift Dzire VDI\",\"year\":2018,\"km_driven\":45000,\"fuel\":\"Diesel\",\"transmission\":\"Manual\",\"owner\":\"First Owner\",\"seller_type\":\"Individual\",\"mileage\":23.4,\"engine\":1248,\"max_power\":74.0,\"seats\":5}"
```

---

### Step 6: Nginx Reverse Proxy (`nginx-1.28.2/`)

Nginx acts as a **reverse proxy**, forwarding traffic from **port 80 → port 8000** (Waitress).

**Architecture:** `Client → Nginx (port 80) → Waitress (port 8000) → Flask App`

**Start Nginx:**
```bash
cd nginx-1.28.2
nginx.exe
```

**Stop Nginx:**
```bash
cd nginx-1.28.2
nginx.exe -s stop
```

**Reload Nginx (after config changes):**
```bash
cd nginx-1.28.2
nginx.exe -s reload
```

**Test via Nginx (port 80):**
```bash
curl http://localhost/health
curl -X POST http://localhost/predict -H "Content-Type: application/json" -d "{...}"
```

**Nginx Config Location:** `nginx-1.28.2/conf/nginx.conf`

Key configuration:
- `upstream flask_backend` → defines backend pool at `127.0.0.1:8000`
- `proxy_pass http://flask_backend` → forwards all requests
- CORS headers added for cross-origin Streamlit access
- Access/error logs in `nginx-1.28.2/logs/`

---

### Step 7: Streamlit Dashboard (`ui/app.py`)

Interactive dashboard with:
- Sidebar input form (car attributes)
- Price prediction display with confidence range
- Feature importance chart
- Market analysis tab (price by brand, fuel, year)
- Model insights tab

```bash
python -m streamlit run ui/app.py --server.port 8501
```

**Dashboard URL:** http://localhost:8501

> **Note:** The Streamlit UI can work standalone (local prediction fallback) or with the API server running on port 8000 for API-based prediction.

---

### Step 8 (Optional): View MLflow UI

```bash
mlflow ui --backend-store-uri mlruns --port 5000
```

**MLflow URL:** http://localhost:5000

---

## Service URLs Summary

| Service         | URL                          | Port  |
|-----------------|------------------------------|-------|
| Flask API       | http://localhost:8000        | 8000  |
| Nginx Proxy     | http://localhost             | 80    |
| Streamlit UI    | http://localhost:8501        | 8501  |
| MLflow UI       | http://localhost:5000        | 5000  |

---

## Project Structure

```
car_price_mlops/
├── data/
│   ├── raw/car_details.csv           # Raw dataset
│   └── processed/
│       ├── car_cleaned.csv           # After data pipeline
│       └── car_engineered.csv        # After feature engineering
├── models/
│   ├── car_price_model.pkl           # Trained model pipeline
│   ├── encoder.pkl                   # Label/target encoders
│   ├── scaler.pkl                    # StandardScaler
│   ├── feature_columns.pkl           # Feature column names
│   └── training_metrics.json         # Training results
├── src/
│   ├── data_pipeline.py              # Step 1: Load, validate, clean
│   ├── feature_engineering.py        # Step 2: Encode, scale, select
│   ├── train_model.py                # Step 3: Train + MLflow
│   └── register_model.py             # Step 4: MLflow registry
├── api/
│   ├── main.py                       # Step 5: Flask app (routes + validation)
│   ├── serve.py                      # Waitress WSGI entry point
│   ├── schemas.py                    # Pydantic validation models
│   └── predictor.py                  # Inference logic
├── nginx-1.28.2/                     # Nginx reverse proxy
│   ├── conf/nginx.conf               # ← Configured for reverse proxy
│   ├── logs/                         # Access & error logs
│   └── nginx.exe                     # Nginx executable
├── ui/
│   └── app.py                        # Step 7: Streamlit dashboard
├── dags/
│   └── car_price_pipeline.py         # Airflow DAG definition
├── mlruns/                           # MLflow experiment data
├── Dataset/                          # Original dataset files
├── requirements.txt
├── README.md
└── steps.md                          # This file
```

---

## Technology Stack

| Component          | Technology                     |
|--------------------|--------------------------------|
| ML Framework       | scikit-learn, XGBoost          |
| Pipeline           | sklearn Pipeline               |
| Experiment Tracking| MLflow                         |
| API                | Flask + Pydantic               |
| WSGI Server        | Waitress                       |
| Reverse Proxy      | Nginx                          |
| Dashboard          | Streamlit + Plotly              |
| Orchestration      | Apache Airflow (DAG defined)   |
| Data Processing    | pandas, numpy                  |
