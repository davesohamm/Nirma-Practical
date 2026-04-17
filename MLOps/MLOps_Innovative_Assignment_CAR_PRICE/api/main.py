"""
FastAPI Application — Car Price Prediction API v2.0
Migrated from Flask + Waitress to FastAPI + Uvicorn.

Features:
  - JWT Authentication (signup/login/roles)
  - MongoDB persistence (predictions, users, logs)
  - Prometheus metrics (/metrics)
  - CORS middleware
  - Role-based access control (user/admin)
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.database.connection import connect_db, close_db
from api.middleware.metrics import PrometheusMiddleware, metrics_endpoint
from api.routes.auth_routes import router as auth_router
from api.routes.prediction_routes import router as prediction_router
from api.routes.user_routes import router as user_router
from api.routes.admin_routes import router as admin_router
from api.routes.health_routes import router as health_router
from api.routes.mlflow_routes import router as mlflow_router


# ─── Lifespan: Startup & Shutdown ────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle — connect to MongoDB on startup, close on shutdown."""
    connect_db()
    print("[APP] FastAPI Car Price Predictor v2.0 started.")
    yield
    close_db()
    print("[APP] FastAPI Car Price Predictor v2.0 shut down.")


# ─── App Initialization ─────────────────────────────────────────────────────
app = FastAPI(
    title="Car Price Predictor API",
    description="Production-grade MLOps API for used car price prediction with JWT auth, MongoDB, and Prometheus monitoring.",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ─── CORS Middleware ─────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Prometheus Middleware ───────────────────────────────────────────────────
app.add_middleware(PrometheusMiddleware)

# ─── Register Routers ───────────────────────────────────────────────────────
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(prediction_router, tags=["Predictions"])
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(mlflow_router, prefix="/admin", tags=["MLflow & Retraining"])
app.include_router(health_router, tags=["Health"])

# ─── Prometheus Metrics Endpoint ─────────────────────────────────────────────
app.get("/metrics", tags=["Monitoring"])(metrics_endpoint)


# ─── Root Endpoint ───────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {
        "service": "Car Price Predictor API",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
