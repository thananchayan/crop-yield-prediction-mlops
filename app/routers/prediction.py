"""Prediction endpoint."""

from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, Request

from app.core.config import Settings, get_settings
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.dependencies import get_model_service, get_prediction_service
from app.services.model_loader import ModelService
from app.services.prediction_service import PredictionService

logger = logging.getLogger(__name__)
router = APIRouter(tags=["prediction"])


@router.post("/predict", response_model=PredictionResponse)
def predict(
    payload: PredictionRequest,
    request: Request,
    settings: Settings = Depends(get_settings),
    model_service: ModelService = Depends(get_model_service),
    prediction_service: PredictionService = Depends(get_prediction_service),
) -> PredictionResponse:
    """Predict crop yield from validated tabular input."""

    prediction = prediction_service.predict(payload)
    logger.info(
        "Prediction completed request_id=%s model_version=%s",
        request.state.request_id,
        model_service.metadata.model_version,
    )
    return PredictionResponse(
        request_id=request.state.request_id,
        prediction=prediction,
        unit=settings.prediction_unit,
        model_id=model_service.metadata.model_id,
        model_version=model_service.metadata.model_version,
    )
