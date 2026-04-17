"""
Step 6.2 — Pydantic Input/Output Schemas
Tools: Pydantic (via FastAPI)
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class CarInput(BaseModel):
    """Input schema for car price prediction."""
    name: str = Field(..., description="Car name (e.g., 'Maruti Swift Dzire VDI')")
    year: int = Field(..., ge=1990, le=2025, description="Manufacturing year")
    km_driven: int = Field(..., ge=0, description="Kilometers driven")
    fuel: str = Field(..., description="Fuel type: Petrol, Diesel, CNG, LPG, Electric")
    transmission: str = Field(..., description="Transmission: Manual or Automatic")
    owner: str = Field(..., description="Owner type: First Owner, Second Owner, etc.")
    seller_type: str = Field(..., description="Seller type: Individual, Dealer, Trustmark Dealer")
    mileage: float = Field(..., ge=0, description="Mileage (kmpl)")
    engine: float = Field(..., ge=0, description="Engine capacity (CC)")
    max_power: float = Field(..., ge=0, description="Max power (bhp)")
    seats: int = Field(..., ge=2, le=14, description="Number of seats")

    class Config:
        json_schema_extra = {
            "example": {
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
            }
        }


class PredictionOutput(BaseModel):
    """Output schema for price prediction."""
    predicted_price: float = Field(..., description="Predicted selling price in INR")
    currency: str = "INR"
    model_version: str = "v1.0"


class BatchCarInput(BaseModel):
    """Input schema for batch predictions."""
    cars: List[CarInput]


class BatchPredictionOutput(BaseModel):
    """Output schema for batch predictions."""
    predictions: List[PredictionOutput]
    count: int


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    model_loaded: bool
    model_version: str
    api_version: str


class ModelInfoResponse(BaseModel):
    """Model information response."""
    model_name: str
    model_version: str
    features: List[str]
    training_dataset: str
    metrics: dict
