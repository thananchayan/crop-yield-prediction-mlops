"""Domain representation of loaded model metadata."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ModelMetadata:
    """Model metadata exposed by the API."""

    model_id: str
    model_version: str
    model_type: str
    target_column: str
    feature_columns: list[str]
    metrics: dict[str, float]
    raw: dict[str, Any]

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> ModelMetadata:
        return cls(
            model_id=str(payload.get("model_id", "crop-yield-regressor")),
            model_version=str(payload.get("model_version", "unknown")),
            model_type=str(payload.get("model_type", "unknown")),
            target_column=str(payload.get("target_column", "hg/ha_yield")),
            feature_columns=list(payload.get("feature_columns", [])),
            metrics=dict(payload.get("metrics", {})),
            raw=payload,
        )
