"""Prediction business logic."""

from __future__ import annotations

import logging

import pandas as pd

from app.core.config import Settings
from app.core.exceptions import PredictionError
from app.schemas.prediction import PredictionRequest
from app.services.model_loader import ModelService

logger = logging.getLogger(__name__)


class PredictionService:
    """Runs validated requests through the loaded model."""

    def __init__(self, model_service: ModelService, settings: Settings) -> None:
        self.model_service = model_service
        self.settings = settings

    def predict(self, payload: PredictionRequest) -> float:
        """Return a single crop yield prediction."""

        if not self.model_service.is_loaded:
            raise PredictionError("Model is not loaded.")

        input_frame = self._to_model_frame(payload)
        try:
            prediction = self.model_service.model.predict(input_frame)
        except Exception as exc:
            raise PredictionError(f"Model prediction failed: {exc}") from exc

        return float(prediction[0])

    @staticmethod
    def _to_model_frame(payload: PredictionRequest) -> pd.DataFrame:
        """Map public API field names to the training feature schema."""

        return pd.DataFrame(
            [
                {
                    "Area": payload.area.strip(),
                    "Item": payload.item.strip(),
                    "Year": payload.year,
                    "average_rain_fall_mm_per_year": (
                        payload.average_rain_fall_mm_per_year
                    ),
                    "pesticides_tonnes": payload.pesticides_tonnes,
                    "avg_temp": payload.avg_temp,
                }
            ]
        )
