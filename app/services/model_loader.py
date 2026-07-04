"""Model loading service."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import joblib

from app.core.config import Settings
from app.core.exceptions import ModelLoadError
from app.models.model_metadata import ModelMetadata

logger = logging.getLogger(__name__)


class ModelService:
    """Holds the loaded model and its metadata for inference."""

    def __init__(
        self,
        *,
        model: Any,
        metadata: ModelMetadata,
        preprocessing_metadata: dict[str, Any],
        model_path: Path,
    ) -> None:
        self.model = model
        self.metadata = metadata
        self.preprocessing_metadata = preprocessing_metadata
        self.model_path = model_path

    @property
    def is_loaded(self) -> bool:
        """Return whether the model object is available."""

        return self.model is not None


def load_model_service(settings: Settings) -> ModelService:
    """Load model artifacts once during application startup."""

    model_path, metadata_path, preprocessing_metadata_path = _resolve_artifact_paths(
        settings
    )

    logger.info("Loading model from %s", model_path)
    if not model_path.exists():
        raise ModelLoadError(f"Model artifact not found: {model_path}")

    try:
        model = joblib.load(model_path)
        metadata = ModelMetadata.from_dict(_load_json(metadata_path))
        preprocessing_metadata = _load_json(preprocessing_metadata_path)
    except Exception as exc:
        raise ModelLoadError(f"Failed to load model artifacts: {exc}") from exc

    logger.info(
        "Loaded model_id=%s model_version=%s model_type=%s",
        metadata.model_id,
        metadata.model_version,
        metadata.model_type,
    )
    return ModelService(
        model=model,
        metadata=metadata,
        preprocessing_metadata=preprocessing_metadata,
        model_path=model_path,
    )


def _resolve_artifact_paths(settings: Settings) -> tuple[Path, Path, Path]:
    """Resolve model artifacts from local disk or Hugging Face Model Hub."""

    if settings.model_source.lower() == "hf":
        return _download_hf_artifacts(settings)

    return (
        settings.model_path,
        settings.model_metadata_path,
        settings.preprocessing_metadata_path,
    )


def _download_hf_artifacts(settings: Settings) -> tuple[Path, Path, Path]:
    """Download required model artifacts from Hugging Face Model Hub."""

    try:
        from huggingface_hub import hf_hub_download
    except ImportError as exc:
        raise ModelLoadError(
            "huggingface_hub is required when MODEL_SOURCE=hf."
        ) from exc

    settings.hf_model_cache_dir.mkdir(parents=True, exist_ok=True)
    logger.info(
        "Downloading model artifacts from repo_id=%s revision=%s",
        settings.hf_model_repo_id,
        settings.hf_model_revision,
    )

    def download(file_name: str) -> Path:
        return Path(
            hf_hub_download(
                repo_id=settings.hf_model_repo_id,
                filename=file_name,
                revision=settings.hf_model_revision,
                cache_dir=settings.hf_model_cache_dir,
                repo_type="model",
            )
        )

    return (
        download("crop_yield_model.joblib"),
        download("model_metadata.json"),
        download("preprocessing_metadata.json"),
    )


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Metadata file not found: {path}")
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)
