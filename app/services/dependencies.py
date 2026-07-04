"""FastAPI dependency providers."""

from __future__ import annotations

from fastapi import Request

from app.core.config import Settings, get_settings
from app.services.model_loader import ModelService
from app.services.prediction_service import PredictionService


def get_model_service(request: Request) -> ModelService:
    """Return the startup-loaded model service."""

    return request.app.state.model_service


def get_prediction_service(request: Request) -> PredictionService:
    """Return a prediction service wired with the loaded model."""

    settings: Settings = get_settings()
    model_service = get_model_service(request)
    return PredictionService(model_service=model_service, settings=settings)
