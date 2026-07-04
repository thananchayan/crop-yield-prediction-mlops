"""Prediction request and response schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field

from app.schemas.common import BaseResponse


class PredictionRequest(BaseModel):
    """Validated crop yield prediction request."""

    area: str = Field(..., min_length=1, max_length=100, examples=["Albania"])
    item: str = Field(..., min_length=1, max_length=100, examples=["Maize"])
    year: int = Field(..., ge=1900, le=2100, examples=[1990])
    average_rain_fall_mm_per_year: float = Field(..., ge=0, examples=[1485.0])
    pesticides_tonnes: float = Field(..., ge=0, examples=[121.0])
    avg_temp: float = Field(..., ge=-50, le=60, examples=[16.37])

    model_config = {
        "json_schema_extra": {
            "example": {
                "area": "Albania",
                "item": "Maize",
                "year": 1990,
                "average_rain_fall_mm_per_year": 1485.0,
                "pesticides_tonnes": 121.0,
                "avg_temp": 16.37,
            }
        }
    }


class PredictionResponse(BaseResponse):
    """Structured prediction response."""

    prediction: float
    unit: str
    model_id: str
    model_version: str
