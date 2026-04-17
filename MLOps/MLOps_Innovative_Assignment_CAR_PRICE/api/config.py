"""
Centralized Configuration — pydantic-settings based.
Reads from environment variables with sensible defaults.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # MongoDB
    MONGO_URL: str = "mongodb://mongodb:27017"
    MONGO_DB_NAME: str = "car_price_db"

    # JWT
    JWT_SECRET: str = "super-secret-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_MINUTES: int = 60

    # Model
    MODEL_VERSION: str = "v1.0"

    # MLflow
    MLFLOW_TRACKING_URI: str = "http://mlflow:5000"

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
