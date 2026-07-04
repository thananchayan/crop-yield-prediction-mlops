"""Model loading tests."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from app.core.config import get_settings
from app.core.exceptions import ModelLoadError, PredictionError
from app.schemas.prediction import PredictionRequest
from app.services.model_loader import ModelService, load_model_service
from app.services.prediction_service import PredictionService


def test_model_loading_from_configured_artifacts() -> None:
    settings = get_settings()

    model_service = load_model_service(settings)

    assert model_service.is_loaded is True
    assert model_service.metadata.model_id == "crop-yield-regressor"
    assert model_service.metadata.model_version == "v1.0.0"
    assert model_service.preprocessing_metadata["encoded_feature_count"] > 0
    assert Path(model_service.model_path).exists()


def test_model_loading_missing_model_raises_error(tmp_path) -> None:
    settings = replace(get_settings(), model_path=tmp_path / "missing.joblib")

    with pytest.raises(ModelLoadError, match="Model artifact not found"):
        load_model_service(settings)


def test_model_loading_missing_metadata_raises_error(tmp_path) -> None:
    settings = replace(
        get_settings(),
        model_metadata_path=tmp_path / "missing_metadata.json",
    )

    with pytest.raises(ModelLoadError, match="Failed to load model artifacts"):
        load_model_service(settings)


def test_prediction_service_requires_loaded_model() -> None:
    settings = get_settings()
    model_service = ModelService(
        model=None,
        metadata=load_model_service(settings).metadata,
        preprocessing_metadata={},
        model_path=settings.model_path,
    )
    prediction_service = PredictionService(
        model_service=model_service,
        settings=settings,
    )
    request = PredictionRequest(
        area="Albania",
        item="Maize",
        year=1990,
        average_rain_fall_mm_per_year=1485.0,
        pesticides_tonnes=121.0,
        avg_temp=16.37,
    )

    with pytest.raises(PredictionError, match="Model is not loaded"):
        prediction_service.predict(request)
