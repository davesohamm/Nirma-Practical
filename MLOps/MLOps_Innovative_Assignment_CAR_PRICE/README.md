# Used Car Price Prediction -- End-to-End MLOps Pipeline v2.0

> A production-grade Machine Learning Operations (MLOps) pipeline for predicting used car prices using ensemble models with experiment tracking, JWT-authenticated REST API, real-time monitoring, CI/CD automation, and containerized microservice deployment.

**M.Tech Semester 2 | MLOps Elective | Nirma University**
**Subject Guide: Dr. Priyank Thakkar**

---

## Team Members

| Name | Enrollment No. | Program |
|------|---------------|---------|
| Dev Patel | 25MCD015 | M.Tech CD |
| Kinjal Rathod | 25MCD009 | M.Tech CD |
| Soham Dave | 25MCD005 | M.Tech CD |
| Vraj Prajapati | 25MCE020 | M.Tech CE |
---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Setup & Installation](#setup--installation)
6. [ML Pipeline Execution](#ml-pipeline-execution)
7. [API Documentation](#api-documentation)
8. [Authentication & Authorization](#authentication--authorization)
9. [Streamlit Dashboard](#streamlit-dashboard)
10. [MLflow Experiment Tracking](#mlflow-experiment-tracking)
11. [Monitoring (Prometheus + Grafana)](#monitoring-prometheus--grafana)
12. [CI/CD Pipeline (Jenkins)](#cicd-pipeline-jenkins)
13. [Docker Deployment](#docker-deployment)
14. [Model Performance](#model-performance)
15. [MLOps Lifecycle Phases](#mlops-lifecycle-phases)
16. [Environment Variables](#environment-variables)
17. [Service URLs](#service-urls)
18. [Dependencies](#dependencies)
19. [Acknowledgments](#acknowledgments)

---

## Project Overview

This project implements a **complete MLOps lifecycle** for a Used Car Price Prediction system. It demonstrates how a machine learning model progresses from raw data to a production-ready, monitored, authenticated, and maintainable deployment using containerized microservices.

The system is built around **6 Docker containers** working together: a FastAPI REST API serves predictions from a trained XGBoost model, MongoDB stores user accounts and prediction history, Streamlit provides an interactive frontend with role-based views, MLflow tracks all experiments and model versions, and Prometheus + Grafana deliver real-time observability.

### Key Features

- **End-to-end ML pipeline**: Data ingestion, validation, cleaning, feature engineering, multi-model training, hyperparameter tuning, and model serving
- **Experiment tracking**: MLflow for logging parameters, metrics, model artifacts, and model registry with version control
- **Production API**: FastAPI with JWT authentication, role-based access control (RBAC), Pydantic validation, and automatic OpenAPI documentation
- **Real-time monitoring**: Prometheus metrics collection with custom middleware + Grafana dashboards (active users, latency percentiles, prediction counts, error rates)
- **Active user tracking**: JWT-based sliding window (5-minute) tracking of unique active users exposed as a Prometheus gauge
- **Interactive UI**: Streamlit dashboard with role-based views -- users get price prediction forms while admins get system management panels
- **Containerized deployment**: Docker Compose orchestrating 6 microservices on a custom bridge network
- **CI/CD pipeline**: Jenkins pipeline with 8 stages (lint, build, test, deploy, health check, train, integration test)
- **Dynamic model reloading**: API hot-reloads retrained models without container restart
- **Admin-triggered retraining**: Background retraining via API endpoint, running the full pipeline inside the container and logging to MLflow
- **MongoDB persistence**: User accounts, predictions, response times, and analytics stored in MongoDB 7.0

### Dataset

- **Source**: [Vehicle Dataset from CardDekho (Kaggle)](https://www.kaggle.com/nehalbirla/vehicle-dataset-from-cardekho)
- **File**: `data/raw/car_details.csv`
- **Size**: 5,000+ records x 13 features
- **Target Variable**: `selling_price` (INR)
- **Features**: name, year, km_driven, fuel, seller_type, transmission, owner, mileage, engine, max_power, torque, seats
- A sample data generator (`scripts/generate_sample_data.py`) is included for generating synthetic training data

---

## Architecture

```
+------------------------------------------------------------------------+
|                           CLIENT LAYER                                  |
|  +--------------------+        +--------------------+                   |
|  | Streamlit UI       |        | curl / Postman     |                   |
|  | (port 8501)        |        | (HTTP Clients)     |                   |
|  +---------+----------+        +---------+----------+                   |
|            |                             |                               |
|            v                             v                               |
|  +-----------------------------------------------------+               |
|  |           FastAPI REST API (port 8000)               |               |
|  |  JWT Auth | RBAC | Pydantic | Prometheus Middleware   |               |
|  |  /predict | /auth | /admin | /health | /metrics       |               |
|  +-----------------------------------------------------+               |
|           |                |                |                            |
|           v                v                v                            |
|  +--------------+  +---------------+  +------------------+              |
|  | ML Model     |  | MongoDB 7.0   |  | Prometheus       |              |
|  | XGBoost      |  | (port 27017)  |  | (port 9090)      |              |
|  | Pipeline     |  | Users, Preds  |  | Scrapes /metrics |              |
|  | (hot-reload) |  | Logs, Stats   |  | every 15 seconds |              |
|  +--------------+  +---------------+  +--------+---------+              |
|           |                                      |                       |
|           v                                      v                       |
|  +-----------------+                   +------------------+             |
|  | MLflow Tracking |                   | Grafana 10.4     |             |
|  | (port 5000)     |                   | (port 3000)      |             |
|  | Experiments,    |                   | Admin Dashboard   |             |
|  | Model Registry  |                   | User Dashboard    |             |
|  +-----------------+                   +------------------+             |
|                                                                          |
+--------------------------------------------------------------------------+
|                        TRAINING PIPELINE                                 |
|  +-----------+  +-------------+  +-----------+  +------------+          |
|  | Data      |->| Feature     |->| Model     |->| MLflow     |          |
|  | Pipeline  |  | Engineering |  | Training  |  | Registry   |          |
|  | Step 1-2  |  | Step 3      |  | Step 4    |  | Step 5     |          |
|  +-----------+  +-------------+  +-----------+  +------------+          |
|    pandas        LabelEncoder     4 Candidate    Experiment              |
|    numpy         OneHotEncoder    Models +       Tracking +              |
|    IQR           TargetEncoder    GridSearchCV   Model Versioning        |
|    dedup         StandardScaler   XGBoost Tuned  Artifact Storage        |
|                                                                          |
+--------------------------------------------------------------------------+
|                        CI/CD (Jenkins)                                   |
|  Checkout -> Lint -> Build -> Test -> Deploy -> Health -> Train -> E2E   |
+--------------------------------------------------------------------------+
```

### Data Flow

```
Raw CSV --> Data Pipeline --> Cleaned CSV --> Feature Engineering --> Engineered CSV
                                                                         |
                                                                         v
User Request --> FastAPI --> Predictor (hot-reload) <-- Model Training + MLflow
                   |                                         |
                   v                                         v
              MongoDB (store prediction)              MLflow (log metrics)
                   |
                   v
          Prometheus (scrape metrics) --> Grafana (visualize)
```

---

## Technology Stack

| Phase | Component | Technology | Version |
|-------|-----------|-----------|---------|
| **Data Engineering** | Data Pipeline | Python, pandas, numpy | pandas 2.0+ |
| | Data Validation | Schema checks, IQR outlier detection | - |
| | Data Generation | Synthetic data generator script | - |
| **Feature Engineering** | Encoding | LabelEncoder, One-Hot, Target Encoding | scikit-learn 1.3+ |
| | Scaling | StandardScaler | scikit-learn 1.3+ |
| | Feature Selection | Correlation matrix (threshold > 0.90) | - |
| **Model Training** | Algorithms | Linear Regression, Random Forest, Gradient Boosting, XGBoost | xgboost 2.0+ |
| | Hyperparameter Tuning | GridSearchCV (3-fold CV, 8 combinations) | scikit-learn 1.3+ |
| | Pipeline | sklearn Pipeline (StandardScaler -> Model) | scikit-learn 1.3+ |
| **Experiment Tracking** | Tracking Server | MLflow (remote server, SQLite backend) | mlflow 2.8+ |
| | Model Registry | MLflow Model Registry (versioned) | mlflow 2.8+ |
| | DNS Rebinding Fix | `--allowed-hosts *` for inter-container calls | mlflow 3.x |
| **API Serving** | Web Framework | FastAPI + Uvicorn | fastapi 0.110+ |
| | Validation | Pydantic v2 | pydantic 2.0+ |
| | Authentication | JWT (python-jose) + bcrypt | python-jose 3.3+ |
| | Model Serving | Hot-reloadable Predictor with dynamic version | - |
| **Database** | Persistence | MongoDB 7.0 | 7.0 |
| | Driver | pymongo | 4.6+ |
| **Monitoring** | Metrics Collection | Prometheus | v2.51.0 |
| | Custom Middleware | Counter, Histogram, Gauge (prometheus-client) | 0.20+ |
| | Active User Tracking | JWT extraction + 5-min sliding window | - |
| | Dashboards | Grafana (auto-provisioned) | 10.4.0 |
| **Dashboard** | UI Framework | Streamlit | 1.28+ |
| | Visualization | Plotly Express | 5.18+ |
| | Design | Glassmorphism CSS, Inter font, gradient backgrounds | - |
| **Containerization** | Orchestration | Docker Compose (6 services) | 3.8 |
| | Network | Custom bridge (`car_price_mlops_network`) | - |
| | Volumes | Named volumes for MongoDB + MLflow data | - |
| **CI/CD** | Pipeline | Jenkins (8-stage Jenkinsfile, Windows `bat`) | - |
| **Orchestration** | Pipeline DAG | Apache Airflow (DAG defined) | - |

---

## Project Structure

```
car_price_mlops/
|
|-- api/                                  # FastAPI Backend Application
|   |-- __init__.py
|   |-- main.py                           # FastAPI app with lifespan, CORS, routers, middleware
|   |-- config.py                         # Pydantic-settings configuration (env vars)
|   |-- predictor.py                      # Model loading, inference, hot-reload support
|   |-- auth/                             # JWT Authentication Module
|   |   |-- jwt_handler.py                # Token creation (HS256) / verification
|   |   |-- password.py                   # bcrypt password hashing + verification
|   |   |-- dependencies.py               # FastAPI deps: get_current_user, require_user, require_admin
|   |-- database/
|   |   |-- connection.py                 # MongoDB connection manager (connect/close/get_db)
|   |-- middleware/
|   |   |-- metrics.py                    # Prometheus middleware: request tracking, active users,
|   |                                     #   JWT extraction, sliding window gauge
|   |-- models/                           # Pydantic Schemas (request/response models)
|   |   |-- user.py                       # UserSignup, UserLogin, UserResponse, TokenResponse
|   |   |-- car.py                        # CarInput, PredictionOutput, BatchCarInput, HealthResponse
|   |   |-- prediction.py                 # PredictionRecord, AdminMetrics
|   |-- routes/                           # API Route Handlers
|   |   |-- auth_routes.py                # POST /auth/signup, POST /auth/login, GET /auth/me
|   |   |-- prediction_routes.py          # POST /predict, POST /predict/batch
|   |   |-- user_routes.py                # GET /user/predictions, GET /user/analytics
|   |   |-- admin_routes.py               # GET /admin/predictions, /admin/users, /admin/metrics
|   |   |-- health_routes.py              # GET /health, GET /model-info
|   |   |-- mlflow_routes.py              # POST /admin/retrain, GET /admin/retrain-status,
|   |                                     #   GET /admin/mlflow-status, GET /admin/model-metrics
|   |-- services/
|       |-- prediction_service.py         # Prediction logic + MongoDB persistence
|       |-- user_service.py               # User CRUD (signup, authenticate, list)
|       |-- analytics_service.py          # Admin metrics aggregation, user analytics
|
|-- src/                                  # ML Pipeline Scripts
|   |-- __init__.py
|   |-- data_pipeline.py                  # Step 1-2: Load, validate, clean, outlier removal, dedup
|   |-- feature_engineering.py            # Step 3: Derive features, encode, scale, select
|   |-- train_model.py                    # Step 4: Train 4 models, GridSearchCV, MLflow logging
|   |-- register_model.py                 # Step 5: Model registry & versioning
|
|-- models/                               # Trained Model Artifacts
|   |-- car_price_model.pkl               # Best model: XGBoost Pipeline (StandardScaler + XGBRegressor)
|   |-- encoder.pkl                       # Label + Target encoders (owner, seller_type, brand)
|   |-- feature_columns.pkl              # Feature names for model input alignment
|   |-- scaler.pkl                        # StandardScaler (km_driven, engine, max_power, mileage)
|   |-- training_metrics.json             # Best model metrics, all results, tuned params, MLflow run ID
|
|-- ui/                                   # Streamlit Frontend
|   |-- app.py                            # Interactive dashboard with role-based rendering
|   |-- utils/
|       |-- api_client.py                 # HTTP client for API communication
|       |-- session.py                    # Streamlit session state management
|
|-- docker/                               # Dockerfiles
|   |-- Dockerfile.api                    # FastAPI app image (Python 3.11-slim)
|   |-- Dockerfile.ui                     # Streamlit UI image (Python 3.11-slim)
|   |-- Dockerfile.mlflow                 # MLflow tracking server image
|
|-- monitoring/                           # Monitoring Configuration
|   |-- prometheus/
|   |   |-- prometheus.yml                # Scrape config: FastAPI (15s) + self-monitoring
|   |-- grafana/
|       |-- provisioning/
|           |-- datasources/
|           |   |-- prometheus.yml        # Auto-configured Prometheus datasource (uid: prometheus)
|           |-- dashboards/
|               |-- dashboard.yml         # Dashboard provider config (folder: Car Price MLOps)
|               |-- admin_dashboard.json  # Admin Grafana dashboard (10 panels)
|               |-- user_dashboard.json   # User Grafana dashboard (6 panels)
|
|-- scripts/                              # Utility Scripts
|   |-- generate_sample_data.py           # Synthetic data generator (5000 rows, 15 brands)
|
|-- dags/                                 # Airflow Orchestration
|   |-- car_price_pipeline.py             # Weekly retraining DAG definition
|
|-- data/                                 # Dataset (raw + processed, volume-mounted)
|   |-- raw/
|   |   |-- car_details.csv               # Raw dataset (real or generated)
|   |-- processed/
|       |-- car_cleaned.csv               # Output of data pipeline (cleaned)
|       |-- car_engineered.csv            # Output of feature engineering (model-ready)
|
|-- docker-compose.yml                    # Multi-container orchestration (6 services)
|-- Jenkinsfile                           # CI/CD pipeline definition (8 stages, Windows bat)
|-- requirements.txt                      # Python dependencies (22 packages)
|-- .env                                  # Environment variables (MongoDB, JWT, MLflow, Grafana)
|-- README.md                             # This file
```

---

## Setup & Installation

### Prerequisites

- **Docker Desktop** (with Docker Compose) installed and running
- **Python 3.11+** (for local development only)
- **Jenkins** (optional, for CI/CD pipeline)

### Quick Start (Docker Compose)

```bash
# 1. Navigate to the project directory
cd car_price_mlops

# 2. Build and start all 6 services
docker-compose up -d --build

# 3. Wait ~30-45 seconds for all services to initialize
#    MongoDB needs to pass health check before API starts

# 4. Access the application
#    Streamlit UI:  http://localhost:8501
#    FastAPI API:   http://localhost:8000
#    API Docs:      http://localhost:8000/docs
#    MLflow:        http://localhost:5000
#    Grafana:       http://localhost:3000 (admin / admin)
#    Prometheus:    http://localhost:9090
```

### Generate Training Data (if not present)

```bash
# Generate 5000 synthetic car records for pipeline testing
python scripts/generate_sample_data.py
# Output: data/raw/car_details.csv
```

### Local Development (without Docker)

```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac

# Install all dependencies
pip install -r requirements.txt

# Start MongoDB locally (must be running on port 27017)

# Run the ML pipeline
python -m src.data_pipeline
python -m src.feature_engineering
python -m src.train_model

# Start the API server
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

# Start the UI (new terminal)
streamlit run ui/app.py --server.port 8501
```

### Verify Services

```bash
# Check API health
curl http://localhost:8000/health
# {"status":"healthy","model_loaded":true,"model_version":"v1.0","api_version":"2.0.0"}

# Check Prometheus targets
curl http://localhost:9090/api/v1/targets | jq '.data.activeTargets[].health'
# "up"

# Check Grafana
curl http://localhost:3000/api/health
# {"commit":"...","database":"ok","version":"10.4.0"}

# Check MLflow
curl http://localhost:5000/api/2.0/mlflow/experiments/search?max_results=10
```

---

## ML Pipeline Execution

### Step 1-2: Data Pipeline (`src/data_pipeline.py`)

Loads, validates, cleans, and preprocesses the raw dataset.

**Operations:**
1. **Load** raw CSV data (5000 rows, 13 columns)
2. **Validate** schema (13 required columns: name, year, selling_price, km_driven, fuel, seller_type, transmission, owner, mileage, engine, max_power, torque, seats)
3. **Fix data types** -- strip units from strings: `"23.4 kmpl"` -> `23.4`, `"1248 CC"` -> `1248`
4. **Handle missing values** -- median imputation for numeric, mode for categorical; drop columns with >30% missing
5. **Remove outliers** -- IQR method on selling_price and km_driven; domain rules (price 10K-10M, km < 500K, year 1990-2025)
6. **Deduplicate** exact duplicate rows
7. **Drop torque** column (complex parsing, not in final feature set)

```bash
python -m src.data_pipeline
# Output: data/processed/car_cleaned.csv (~4,687 rows after cleaning)
```

### Step 3: Feature Engineering (`src/feature_engineering.py`)

Transforms cleaned data into model-ready features using multiple encoding strategies.

**Operations:**
1. **Derive features**: `car_age` (2025 - year), `brand` (first word of name), `model_name`, `price_per_km`, `is_first_owner`
2. **Label Encoding**: `owner` (ordinal: First -> 0, Second -> 1, ...) and `seller_type` (Dealer, Individual, Trustmark)
3. **One-Hot Encoding**: `fuel` and `transmission` (with `drop_first=True` to avoid multicollinearity)
4. **Target Encoding**: `brand` -- encoded as mean selling_price per brand (handles high cardinality)
5. **Standard Scaling**: `km_driven`, `engine`, `max_power`, `mileage` (zero mean, unit variance)
6. **Feature Selection**: Remove features with correlation > 0.90 (e.g., `is_first_owner` correlates with encoded `owner`)
7. **Drop non-feature columns**: `name`, `model_name`, `brand`, `year`, `price_per_km`

```bash
python -m src.feature_engineering
# Output: data/processed/car_engineered.csv, models/encoder.pkl, models/scaler.pkl
```

**Final Feature Set (13 features):**
`km_driven`, `seller_type`, `owner`, `mileage`, `engine`, `max_power`, `seats`, `car_age`, `fuel_Diesel`, `fuel_LPG`, `fuel_Petrol`, `transmission_Manual`, `brand_encoded`

### Step 4: Model Training (`src/train_model.py`)

Trains multiple candidate models, performs hyperparameter tuning, and logs everything to MLflow.

**Candidate Models (all wrapped in sklearn Pipeline with StandardScaler):**

| Model | n_estimators | max_depth | learning_rate |
|-------|-------------|-----------|--------------|
| Linear Regression | - | - | - |
| Random Forest | 200 | 10 | - |
| Gradient Boosting | 200 | 6 | 0.1 |
| XGBoost | 300 | 6 | 0.05 |

**Hyperparameter Tuning**: GridSearchCV on XGBoost with 3-fold cross-validation:
- `n_estimators`: [300, 500]
- `max_depth`: [4, 6]
- `learning_rate`: [0.05, 0.1]
- Total fits: 8 combinations x 3 folds = 24 fits

**MLflow Logging** (for each model run):
- Parameters: all model hyperparameters
- Metrics: R2, RMSE, MAE, MAPE, CV R2 (mean and std)
- Artifacts: trained sklearn Pipeline, model signature
- Best model registered as `car-price-predictor` in MLflow Model Registry

```bash
python -m src.train_model
# Output: models/car_price_model.pkl, models/training_metrics.json
# MLflow: All runs logged to tracking server at http://localhost:5000
```

---

## API Documentation

**Base URL:** `http://localhost:8000`
**Interactive Docs:** `http://localhost:8000/docs` (Swagger UI) | `http://localhost:8000/redoc` (ReDoc)

### Complete Endpoint Reference

| Method | Endpoint | Auth | Role | Description |
|--------|----------|------|------|-------------|
| `GET` | `/` | None | - | Root endpoint -- service info and links |
| `POST` | `/auth/signup` | None | - | Register a new user (choose role: user/admin) |
| `POST` | `/auth/login` | None | - | Authenticate and receive JWT token |
| `GET` | `/auth/me` | Bearer | Any | Get current user profile |
| `POST` | `/predict` | Bearer | User | Single car price prediction |
| `POST` | `/predict/batch` | Bearer | User | Batch prediction (array of cars) |
| `GET` | `/user/predictions` | Bearer | User | User's prediction history (paginated) |
| `GET` | `/user/analytics` | Bearer | User | User's analytics (brands, avg price) |
| `GET` | `/admin/predictions` | Bearer | Admin | All predictions system-wide (paginated) |
| `GET` | `/admin/users` | Bearer | Admin | List all registered users |
| `GET` | `/admin/metrics` | Bearer | Admin | System metrics (users, predictions, response times) |
| `POST` | `/admin/retrain` | Bearer | Admin | Trigger model retraining (runs in background) |
| `GET` | `/admin/retrain-status` | Bearer | Admin | Check retraining progress (idle/running/completed/failed) |
| `GET` | `/admin/mlflow-status` | Bearer | Admin | MLflow experiment info and recent runs |
| `GET` | `/admin/model-metrics` | None | - | Current model training metrics from JSON |
| `GET` | `/health` | None | - | API health check (status, model loaded, version) |
| `GET` | `/model-info` | None | - | Model metadata (features, version, metrics) |
| `GET` | `/metrics` | None | - | Prometheus metrics endpoint (scrape target) |

### Example: Complete Workflow

```bash
# 1. Register a new user
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "mypassword123",
    "role": "user"
  }'
# Response: {"message": "User created successfully", "user_id": "..."}

# 2. Login to get JWT token
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "mypassword123"}'
# Response: {"access_token": "eyJ...", "token_type": "bearer", "role": "user", "username": "testuser"}

# 3. Predict car price (use token from step 2)
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJ..." \
  -d '{
    "name": "Maruti Swift Dzire VDI",
    "year": 2018,
    "km_driven": 45000,
    "fuel": "Diesel",
    "transmission": "Manual",
    "owner": "First Owner",
    "seller_type": "Individual",
    "mileage": 23.4,
    "engine": 1248,
    "max_power": 74.0,
    "seats": 5
  }'
# Response: {"predicted_price": 488863.28, "currency": "INR", "model_version": "XGBoost_Tuned"}

# 4. View prediction history
curl http://localhost:8000/user/predictions?page=1&limit=10 \
  -H "Authorization: Bearer eyJ..."

# 5. (Admin) Trigger model retraining
curl -X POST http://localhost:8000/admin/retrain \
  -H "Authorization: Bearer <admin_token>"
# Response: {"message": "Model retraining triggered. Check /admin/retrain-status for progress."}

# 6. (Admin) Check retraining progress
curl http://localhost:8000/admin/retrain-status \
  -H "Authorization: Bearer <admin_token>"
# Response: {"status": "completed", "message": "...", "metrics": {"RMSE": ..., "R2": ...}}

# 7. (Admin) View MLflow experiment runs
curl http://localhost:8000/admin/mlflow-status \
  -H "Authorization: Bearer <admin_token>"
```

### Prediction Input Schema

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `name` | string | Yes | Car name with brand and model | "Maruti Swift VXI" |
| `year` | integer | Yes | Manufacturing year | 2018 |
| `km_driven` | integer | Yes | Total kilometers driven | 45000 |
| `fuel` | string | Yes | Fuel type (Petrol/Diesel/CNG/LPG) | "Diesel" |
| `transmission` | string | Yes | Manual or Automatic | "Manual" |
| `owner` | string | Yes | Ownership history | "First Owner" |
| `seller_type` | string | Yes | Individual/Dealer/Trustmark Dealer | "Individual" |
| `mileage` | float | Yes | Fuel efficiency (kmpl) | 23.4 |
| `engine` | float | Yes | Engine displacement (CC) | 1248.0 |
| `max_power` | float | Yes | Max power output (bhp) | 74.0 |
| `seats` | integer | Yes | Number of seats | 5 |

---

## Authentication & Authorization

### JWT-Based Authentication

| Property | Value |
|----------|-------|
| **Algorithm** | HS256 |
| **Token Expiry** | 60 minutes (configurable via `JWT_EXPIRY_MINUTES`) |
| **Password Hashing** | bcrypt (salted, 12 rounds) |
| **Token Location** | `Authorization: Bearer <token>` header |
| **Library** | python-jose (with cryptography backend) |

### Role-Based Access Control (RBAC)

| Role | Capabilities |
|------|-------------|
| **User** | Predict car prices, view own prediction history, view own analytics (brand distribution, avg price) |
| **Admin** | View all users, view all predictions system-wide, view system metrics, trigger model retraining, check MLflow status, access monitoring links |

### Authentication Flow

```
1. POST /auth/signup  -->  Create user in MongoDB (username, email, hashed password, role)
2. POST /auth/login   -->  Verify credentials, return JWT with {sub: username, role: user/admin}
3. Protected routes    -->  Extract JWT from Authorization header
                            --> Decode and verify signature + expiry
                            --> Load user from MongoDB by username (sub claim)
                            --> Check role for admin-only routes
4. Active user tracking -->  Prometheus middleware extracts user ID from JWT on every request
```

### FastAPI Dependencies

- `get_current_user`: Extracts and validates JWT, returns user dict from MongoDB
- `require_user`: Ensures user role is "user" (rejects admin)
- `require_admin`: Ensures user role is "admin" (rejects regular users)

---

## Streamlit Dashboard

The Streamlit UI provides a **premium dark-themed** interface with role-based rendering -- users and admins see completely different views.

### User View (Role: user)

| Tab | Features |
|-----|----------|
| **Price Prediction** | Car details form in sidebar (name, year, km, fuel, transmission, owner, seller, mileage, engine, power, seats). Prediction result shown as a gradient card with price range estimate (Low/Best/High at -15%/0%/+15%) |
| **Prediction History** | Paginated table of past predictions with car details, predicted price, response time, and timestamp. Line chart of predicted prices over time |
| **Analytics** | Total predictions count, average predicted price, unique brands. Bar chart of most predicted brands by count |

### Admin View (Role: admin)

| Tab | Features |
|-----|----------|
| **System Metrics** | 5 metric cards: Total Users, Total Predictions, Avg Response Time (ms), Today's Predictions, Active Users (24h). Quick links to Grafana, Prometheus, MLflow, and API Docs |
| **User Management** | Table of all registered users (username, email, role, active status, created date). Pie chart of users by role. Stat cards for total users, admin count, user count |
| **All Predictions** | System-wide prediction table with user ID, car, year, price, fuel, model version, response time, and date. Price distribution histogram |

### UI Design

- **Theme**: Dark gradient background (`#0f0c29` to `#302b63`) with glassmorphism cards
- **Font**: Inter (Google Fonts) with weights 300-800
- **Components**: Custom CSS classes for `.price-card`, `.glass-card`, `.stat-box`, `.student-card`, `.auth-card`
- **Footer**: Student names and submission details displayed as styled cards
- **Responsive**: Wide layout with sidebar for input forms (user) or navigation (admin)

---

## MLflow Experiment Tracking

### Overview

MLflow is deployed as a remote tracking server inside a Docker container. All model training runs (both local and in-container retraining) log to this central server.

### Configuration

| Property | Value |
|----------|-------|
| **Tracking URI** | `http://mlflow:5000` (inside Docker network) |
| **Backend Store** | SQLite (`/mlflow/mlflow.db`) |
| **Artifact Store** | Local filesystem (`/mlflow/artifacts`) |
| **DNS Rebinding Protection** | Disabled via `--allowed-hosts *` (required for inter-container calls where Host header is `mlflow:5000`) |
| **Data Volume** | `car_price_mlflow_data` (persists across restarts) |
| **Web UI** | `http://localhost:5000` |

### What Gets Logged

| Category | Details |
|----------|---------|
| **Experiment** | `car_price_prediction` |
| **Parameters** | `n_estimators`, `max_depth`, `learning_rate`, `random_state`, and all model-specific params |
| **Metrics** | R2, RMSE, MAE, MAPE, CV_R2_mean, CV_R2_std |
| **Artifacts** | Trained sklearn Pipeline (pickle), MLflow model signature, conda env, pip requirements |
| **Model Registry** | `car-price-predictor` with automatic version incrementing |

### Runs Created Per Training

Each training session creates **5 MLflow runs**:
1. `LinearRegression` -- baseline model
2. `RandomForest` -- ensemble with 200 trees
3. `GradientBoosting` -- boosting with 200 trees
4. `XGBoost` -- gradient boosting with 300 trees
5. `BEST_XGBoost_Tuned` -- GridSearchCV best model, registered in Model Registry

### Retraining Flow

```
Admin triggers POST /admin/retrain
    |
    v (background task)
1. Data Pipeline: Load CSV -> Validate -> Clean -> Save
2. Feature Engineering: Derive -> Encode -> Scale -> Select -> Save
3. Model Training: Train 4 models -> Log to MLflow -> GridSearchCV tuning
4. Save best model to models/car_price_model.pkl
5. Register in MLflow Model Registry as "car-price-predictor"
6. Hot-reload: predictor.reload_model() -> API serves new model immediately
    |
    v
Check progress: GET /admin/retrain-status
  -> {"status": "completed", "metrics": {"R2": 0.535, "RMSE": 196642}}
```

### Accessing MLflow

- **Web UI**: `http://localhost:5000` -- browse experiments, compare runs, view artifacts
- **API**: `GET /admin/mlflow-status` -- returns experiment info and last 10 runs via API
- **Programmatic**: `mlflow.set_tracking_uri("http://localhost:5000")` in Python

---

## Monitoring (Prometheus + Grafana)

### Prometheus Configuration

- **Scrape interval**: 15 seconds
- **Evaluation interval**: 15 seconds
- **Targets**: FastAPI API (`api:8000/metrics`) + self-monitoring (`localhost:9090/metrics`)

### Custom Prometheus Metrics

The FastAPI app exposes these metrics via the `PrometheusMiddleware` at `/metrics`:

| Metric Name | Type | Labels | Description |
|-------------|------|--------|-------------|
| `http_requests_total` | Counter | `method`, `endpoint`, `status` | Total HTTP requests by endpoint and status code |
| `http_request_duration_seconds` | Histogram | `method`, `endpoint` | Request latency with buckets: 10ms, 25ms, 50ms, 100ms, 250ms, 500ms, 1s, 2.5s, 5s, 10s |
| `http_errors_total` | Counter | `method`, `endpoint`, `status` | Error responses (4xx/5xx) |
| `predictions_total` | Counter | `model_version` | Total predictions made, labeled by model version |
| `model_inference_seconds` | Histogram | `model_version` | Model inference latency with buckets: 5ms, 10ms, 25ms, 50ms, 100ms, 250ms, 500ms, 1s |
| `active_users_gauge` | Gauge | - | Currently active unique users (5-minute sliding window) |
| `predictions_today_total` | Counter | - | Predictions made today |

### How Active Users Tracking Works

```
Every authenticated request -> Prometheus Middleware intercepts
    |
    v
Extract JWT from Authorization header -> Decode token
    |
    v
Get user ID (sub claim) -> Record in _active_users dict with timestamp
    |
    v
Cleanup: Remove entries older than 5 minutes
    |
    v
Update Gauge: active_users_gauge.set(count of unique users in window)
```

This uses a thread-safe sliding window (`threading.Lock`, `dict[str, float]`) that is cleaned up on every metrics scrape and every authenticated request. The window size is 300 seconds (5 minutes).

### Grafana Dashboards

Both dashboards are **auto-provisioned** on Grafana startup via provisioning YAML files. No manual setup required.

**Admin Dashboard** (`http://localhost:3000/d/car-price-admin-dashboard`):

| Panel | Type | Query |
|-------|------|-------|
| API Request Rate | Time Series | `rate(http_requests_total[1m])` by endpoint |
| Latency p95 | Gauge | `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))` |
| Latency p99 | Gauge | `histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))` |
| Active Users | Stat | `active_users_gauge` |
| Total Predictions | Stat | `predictions_total` |
| Error Rate | Time Series | `rate(http_errors_total[5m])` |
| Model Inference Time | Time Series | `rate(model_inference_seconds_sum[5m]) / rate(model_inference_seconds_count[5m])` |
| Requests by Endpoint | Pie Chart | `increase(http_requests_total[1h])` by endpoint |
| Predictions Over Time | Time Series | `increase(predictions_total[5m])` |
| Active Users Over Time | Time Series | `active_users_gauge` |

**User Dashboard** (`http://localhost:3000/d/car-price-user-dashboard`):

| Panel | Type | Query |
|-------|------|-------|
| Predictions Over Time | Time Series | `increase(predictions_total[5m])` |
| Total Predictions | Stat | `predictions_total` |
| Avg Inference Time | Gauge | `rate(model_inference_seconds_sum[5m]) / rate(model_inference_seconds_count[5m])` |
| Active Users | Stat | `active_users_gauge` |
| Request Rate | Time Series | `rate(http_requests_total{endpoint="/predict"}[1m])` |
| Predictions by Version | Pie Chart | `predictions_total` by model_version |

### Dashboard Configuration

- **Datasource**: Auto-provisioned Prometheus (`uid: prometheus`, `url: http://prometheus:9090`)
- **Refresh**: 10 seconds with `liveNow: true`
- **Folder**: `Car Price MLOps`
- **Credentials**: admin / admin (configurable via `GF_SECURITY_ADMIN_PASSWORD`)

---

## CI/CD Pipeline (Jenkins)

### Pipeline Overview (8 Stages)

The project includes a **Jenkinsfile** with 8 sequential stages designed for local Windows deployment:

| Stage | Name | What It Does |
|-------|------|-------------|
| 1 | **Checkout** | Verify workspace files exist (local repo, not Git) |
| 2 | **Lint & Validate** | Python syntax check (`py_compile`) on 5 key files; verify `requirements.txt`, all 3 Dockerfiles, and `docker-compose.yml` exist and are valid |
| 3 | **Build Images** | `docker-compose build --parallel` -- builds API, UI, and MLflow images |
| 4 | **Unit Tests** | Run `pytest` if tests directory exists; validate model artifacts are present |
| 5 | **Deploy** | `docker-compose down --remove-orphans` then `docker-compose up -d` -- deploys all 6 services |
| 6 | **Health Check** | `curl` health endpoints for API, Prometheus, Grafana, and MLflow; list running containers |
| 7 | **Model Training** | Execute full training pipeline inside the API container via `docker-compose exec -T api python -c "..."` (data pipeline -> feature engineering -> model training) |
| 8 | **Integration Test** | End-to-end tests: signup, login, health check, model info, metrics endpoint verification |

### Pipeline Configuration

```groovy
environment {
    PROJECT_NAME    = 'car-price-mlops'
    COMPOSE_FILE    = 'docker-compose.yml'
    API_URL         = 'http://localhost:8000'
    MLFLOW_URL      = 'http://localhost:5000'
    GRAFANA_URL     = 'http://localhost:3000'
    PROMETHEUS_URL  = 'http://localhost:9090'
    UI_URL          = 'http://localhost:8501'
}

options {
    timestamps()
    timeout(time: 30, unit: 'MINUTES')
    buildDiscarder(logRotator(numToKeepStr: '5'))
}
```

### Jenkins Setup (Local Windows)

1. Install **Jenkins** on your Windows machine
2. Create a new **Pipeline** job
3. Under "Pipeline" configuration, select **Pipeline script from SCM**
4. Set SCM to **None** (local repo, no Git)
5. Set the script path to `Jenkinsfile`
6. Point the workspace to the project directory
7. Ensure Docker Desktop is running
8. Run the pipeline

### Post-Build Actions

- **On Success**: Prints all 6 service URLs and team details
- **On Failure**: Collects Docker container logs (`docker-compose logs --tail=50`) for debugging
- **Always**: Prints pipeline completion timestamp

---

## Docker Deployment

### Services (docker-compose.yml)

| Service | Image | Port | Container Name | Description |
|---------|-------|------|----------------|-------------|
| `mongodb` | `mongo:7.0` | 27017 | `car_price_mongodb` | Database for users, predictions, and logs. Health-checked with `mongosh ping` |
| `api` | Custom (`Dockerfile.api`) | 8000 | `car_price_api` | FastAPI backend with ML model, JWT auth, Prometheus metrics. Depends on MongoDB (healthy) |
| `ui` | Custom (`Dockerfile.ui`) | 8501 | `car_price_ui` | Streamlit frontend with role-based views. Depends on API |
| `mlflow` | Custom (`Dockerfile.mlflow`) | 5000 | `car_price_mlflow` | MLflow tracking server (SQLite + local artifacts). `--allowed-hosts *` for DNS rebinding fix |
| `prometheus` | `prom/prometheus:v2.51.0` | 9090 | `car_price_prometheus` | Metrics collection. Scrapes API `/metrics` every 15s |
| `grafana` | `grafana/grafana:10.4.0` | 3000 | `car_price_grafana` | Monitoring dashboards. Auto-provisioned datasource and 2 dashboards |

### Network

All services communicate on the `car_price_mlops_network` custom bridge network. This enables DNS resolution between containers (e.g., API calls `http://mlflow:5000`, UI calls `http://api:8000`).

### Volumes

| Volume / Mount | Type | Purpose |
|---------------|------|---------|
| `car_price_mongo_data` | Named volume | MongoDB data persistence across restarts |
| `car_price_mlflow_data` | Named volume | MLflow experiments, runs, and artifacts persistence |
| `./models:/app/models` | Bind mount | Model artifacts shared between host and API container (enables hot-reload) |
| `./data:/app/data` | Bind mount | Training data accessible to API container for in-container retraining |
| `./monitoring/prometheus/prometheus.yml` | Bind mount (ro) | Prometheus scrape configuration |
| `./monitoring/grafana/provisioning` | Bind mount (ro) | Grafana datasource and dashboard provisioning |

### Docker Commands

```bash
# Build and start all services
docker-compose up -d --build

# Start without rebuild (use cached images)
docker-compose up -d

# View real-time logs
docker-compose logs -f api         # API logs
docker-compose logs -f mlflow      # MLflow logs
docker-compose logs -f ui          # Streamlit logs

# Check container status
docker-compose ps

# Restart a specific service
docker-compose restart api

# Stop all services
docker-compose down

# Stop and remove volumes (full reset)
docker-compose down -v

# Rebuild a specific service
docker-compose build api && docker-compose up -d api
```

### Dependency Order

```
mongodb (health check: mongosh ping)
    |
    v (condition: service_healthy)
   api
    |
    +---> ui (depends_on: api)
    +---> prometheus (depends_on: api)
                |
                v
              grafana (depends_on: prometheus)
              
mlflow (independent, starts in parallel)
```

---

## Model Performance

### Candidate Model Comparison

All models are trained using sklearn Pipeline (`StandardScaler` -> `Model`) and evaluated on 20% test split:

| Model | R2 | RMSE | MAE | MAPE | CV R2 (5-fold) |
|-------|-----|------|-----|------|----------------|
| Linear Regression | 0.4753 | 208,877 | 160,969 | 86.32% | 0.4670 |
| Random Forest | 0.5216 | 199,450 | 147,298 | 72.92% | 0.5428 |
| Gradient Boosting | 0.4807 | 207,810 | 154,393 | 75.95% | 0.5015 |
| XGBoost | 0.4967 | 204,575 | 150,644 | 74.12% | 0.5073 |
| **XGBoost (Tuned)** | **0.5350** | **196,643** | **146,903** | **73.74%** | **Best CV** |

### Best Model: XGBoost (Tuned via GridSearchCV)

| Property | Value |
|----------|-------|
| **Algorithm** | XGBoost wrapped in sklearn Pipeline |
| **Pipeline** | StandardScaler -> XGBRegressor |
| **R2 Score** | **0.5350** |
| **RMSE** | Rs. 1,96,643 |
| **MAE** | Rs. 1,46,903 |
| **MAPE** | 73.74% |
| **Tuned n_estimators** | 300 |
| **Tuned max_depth** | 4 |
| **Tuned learning_rate** | 0.05 |
| **MLflow Run ID** | Logged and tracked |
| **Registry** | `car-price-predictor` v1 |

### Dynamic Model Versioning

After retraining, the API's `predict` endpoint returns the actual model name (e.g., `"XGBoost_Tuned"`) in the response:

```json
{
  "predicted_price": 488863.28,
  "currency": "INR",
  "model_version": "XGBoost_Tuned"
}
```

The predictor supports **hot-reloading** -- when retraining completes, the model, encoders, feature columns, and metrics are reloaded without restarting the container.

---

## MLOps Lifecycle Phases

| Phase | Name | Status | Tools & Implementation |
|-------|------|--------|----------------------|
| 1 | Data Collection | Done | Raw CSV ingestion, synthetic data generator script |
| 2 | Data Preprocessing | Done | pandas, numpy, IQR outlier detection, deduplication |
| 3 | Feature Engineering | Done | StandardScaler, LabelEncoder, One-Hot, Target Encoding, correlation-based selection |
| 4 | Model Training | Done | sklearn Pipeline, XGBoost, GridSearchCV (3-fold CV) |
| 5 | Experiment Tracking | Done | MLflow remote tracking server (SQLite backend, artifact storage) |
| 6 | Model Registry | Done | MLflow Model Registry (`car-price-predictor`, versioned) |
| 7 | API Serving | Done | FastAPI + Uvicorn + Pydantic v2 (18 endpoints) |
| 8 | Authentication | Done | JWT (python-jose, HS256) + bcrypt + RBAC (user/admin) |
| 9 | Database | Done | MongoDB 7.0 (users, predictions, logs collections) |
| 10 | Interactive Dashboard | Done | Streamlit + Plotly (role-based: user prediction forms, admin management panels) |
| 11 | Containerization | Done | Docker Compose (6 services, custom network, named volumes, health checks) |
| 12 | Monitoring | Done | Prometheus (custom middleware, 7 metrics) + Grafana (2 auto-provisioned dashboards, 16 panels total) |
| 13 | CI/CD Pipeline | Done | Jenkins (8-stage Jenkinsfile, Windows bat commands, integration tests) |
| 14 | Pipeline Orchestration | Done | Apache Airflow DAG defined (weekly retraining schedule) |
| 15 | Dynamic Retraining | Done | Admin-triggered via API, background execution, MLflow logging, model hot-reload |
| 16 | Active User Monitoring | Done | JWT-based 5-minute sliding window, Prometheus gauge, Grafana visualization |

---

## Environment Variables

All environment variables are defined in `.env` and consumed by `docker-compose.yml`:

| Variable | Default | Description |
|----------|---------|-------------|
| `MONGO_URL` | `mongodb://mongodb:27017` | MongoDB connection string (Docker DNS) |
| `MONGO_DB_NAME` | `car_price_db` | MongoDB database name |
| `JWT_SECRET` | (set in .env) | JWT signing secret key (change in production) |
| `JWT_ALGORITHM` | `HS256` | JWT signing algorithm |
| `JWT_EXPIRY_MINUTES` | `60` | JWT token expiration time in minutes |
| `MODEL_VERSION` | `v1.0` | Static model version label (health endpoint) |
| `MLFLOW_TRACKING_URI` | `http://mlflow:5000` | MLflow tracking server URL (Docker DNS) |
| `GF_SECURITY_ADMIN_PASSWORD` | `admin` | Grafana admin password |
| `API_URL` | `http://api:8000` | API URL for Streamlit UI container |

---

## Service URLs

| Service | URL | Port | Credentials |
|---------|-----|------|-------------|
| Streamlit UI | http://localhost:8501 | 8501 | Signup/Login in the app |
| FastAPI API | http://localhost:8000 | 8000 | JWT token (via /auth/login) |
| API Docs (Swagger) | http://localhost:8000/docs | 8000 | Open access |
| API Docs (ReDoc) | http://localhost:8000/redoc | 8000 | Open access |
| MLflow Tracking UI | http://localhost:5000 | 5000 | Open access |
| Grafana Dashboards | http://localhost:3000 | 3000 | admin / admin |
| Grafana Admin Dashboard | http://localhost:3000/d/car-price-admin-dashboard | 3000 | admin / admin |
| Grafana User Dashboard | http://localhost:3000/d/car-price-user-dashboard | 3000 | admin / admin |
| Prometheus | http://localhost:9090 | 9090 | Open access |
| Prometheus Targets | http://localhost:9090/targets | 9090 | Open access |
| MongoDB | localhost:27017 | 27017 | No auth (development mode) |

---

## Dependencies

### Python Packages (requirements.txt)

| Category | Package | Version | Purpose |
|----------|---------|---------|---------|
| **Core ML** | pandas | >= 2.0.0 | Data manipulation and analysis |
| | numpy | >= 1.24.0 | Numerical computing |
| | scikit-learn | >= 1.3.0 | ML algorithms, Pipeline, GridSearchCV, StandardScaler |
| | xgboost | >= 2.0.0 | Gradient boosting model |
| | joblib | >= 1.3.0 | Model serialization (pickle) |
| **Experiment Tracking** | mlflow | >= 2.8.0 | Experiment tracking, model registry, artifact storage |
| **API Framework** | fastapi | >= 0.110.0 | REST API framework with async support |
| | uvicorn[standard] | >= 0.29.0 | ASGI server for FastAPI |
| | pydantic | >= 2.0.0 | Request/response validation schemas |
| | pydantic-settings | >= 2.0.0 | Environment-based configuration |
| **Authentication** | python-jose[cryptography] | >= 3.3.0 | JWT token creation and verification |
| | bcrypt | >= 4.0.0 | Password hashing (salted, 12 rounds) |
| **Database** | pymongo | >= 4.6.0 | MongoDB driver |
| **Monitoring** | prometheus-client | >= 0.20.0 | Prometheus metrics (Counter, Histogram, Gauge) |
| **Dashboard** | streamlit | >= 1.28.0 | Interactive web dashboard |
| | plotly | >= 5.18.0 | Charting (line, bar, pie, histogram) |
| | requests | >= 2.31.0 | HTTP client for API communication |
| **Utilities** | python-docx | >= 0.8.11 | Document generation |

### Docker Images

| Image | Version | Size (approx) |
|-------|---------|---------------|
| python | 3.11-slim | ~120MB (base for API, UI, MLflow) |
| mongo | 7.0 | ~700MB |
| prom/prometheus | v2.51.0 | ~230MB |
| grafana/grafana | 10.4.0 | ~400MB |

---

## Acknowledgments

- [CardDekho / Kaggle](https://www.kaggle.com/nehalbirla/vehicle-dataset-from-cardekho) for the vehicle dataset
- [MLflow](https://mlflow.org/) for experiment tracking and model registry
- [FastAPI](https://fastapi.tiangolo.com/) for the high-performance API framework
- [Streamlit](https://streamlit.io/) for rapid dashboard development
- [XGBoost](https://xgboost.readthedocs.io/) for gradient boosting
- [scikit-learn](https://scikit-learn.org/) for ML pipeline and preprocessing
- [Prometheus](https://prometheus.io/) for metrics collection
- [Grafana](https://grafana.com/) for monitoring dashboards
- [MongoDB](https://www.mongodb.com/) for NoSQL persistence
- [Docker](https://www.docker.com/) for containerization
- [Jenkins](https://www.jenkins.io/) for CI/CD automation

---

**Project: Used Car Price Predictor -- MLOps Pipeline v2.0**
**M.Tech Semester 2 | MLOps Elective | Nirma University**
**Subject Guide: Dr. Priyank Thakkar Sir**
**Team: Vraj Prajapati (25MCE020) | Dev Patel (25MCD015) | Kinjal Rathod (25MCD009) | Soham Dave (25MCD005)**
