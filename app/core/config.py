"""Environment-driven application configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from ml.version import MODEL_VERSION

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _csv_env(name: str, default: str = "") -> list[str]:
    value = os.getenv(name, default)
    return [item.strip() for item in value.split(",") if item.strip()]


@dataclass(frozen=True)
class Settings:
    """Typed application settings loaded from environment variables."""

    app_name: str = field(
        default_factory=lambda: os.getenv("APP_NAME", "Crop Yield Prediction API")
    )
    environment: str = field(
        default_factory=lambda: os.getenv("APP_ENV", "development")
    )
    api_version: str = field(default_factory=lambda: os.getenv("API_VERSION", "v1.0.0"))
    model_version: str = MODEL_VERSION
    model_source: str = field(
        default_factory=lambda: os.getenv("MODEL_SOURCE", "local")
    )
    hf_model_repo_id: str = field(
        default_factory=lambda: os.getenv(
            "HF_MODEL_REPO_ID", "thananchayan/crop-yield-regressor"
        )
    )
    hf_model_revision: str = field(
        default_factory=lambda: os.getenv("HF_MODEL_REVISION", "main")
    )
    hf_model_cache_dir: Path = field(
        default_factory=lambda: Path(
            os.getenv("HF_MODEL_CACHE_DIR", str(PROJECT_ROOT / ".cache" / "hf_models"))
        )
    )
    model_path: Path = field(
        default_factory=lambda: Path(
            os.getenv(
                "MODEL_PATH",
                str(
                    PROJECT_ROOT
                    / "artifacts"
                    / "models"
                    / "v1.0.0"
                    / "crop_yield_model.joblib"
                ),
            )
        )
    )
    model_metadata_path: Path = field(
        default_factory=lambda: Path(
            os.getenv(
                "MODEL_METADATA_PATH",
                str(
                    PROJECT_ROOT
                    / "artifacts"
                    / "metrics"
                    / "v1.0.0"
                    / "model_metadata.json"
                ),
            )
        )
    )
    preprocessing_metadata_path: Path = field(
        default_factory=lambda: Path(
            os.getenv(
                "PREPROCESSING_METADATA_PATH",
                str(
                    PROJECT_ROOT
                    / "artifacts"
                    / "metrics"
                    / "v1.0.0"
                    / "preprocessing_metadata.json"
                ),
            )
        )
    )
    prediction_unit: str = field(
        default_factory=lambda: os.getenv("PREDICTION_UNIT", "hg/ha")
    )
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    frontend_dist_dir: Path = field(
        default_factory=lambda: Path(
            os.getenv("FRONTEND_DIST_DIR", str(PROJECT_ROOT / "frontend" / "dist"))
        )
    )
    cors_origins: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "cors_origins",
            _csv_env("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000"),
        )


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""

    return Settings()
