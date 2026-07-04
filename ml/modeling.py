"""Model construction logic."""

from __future__ import annotations

from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.pipeline import Pipeline

from ml.config import TrainingConfig
from ml.preprocessing import build_preprocessor


def build_model_pipeline(config: TrainingConfig) -> Pipeline:
    """Create the full sklearn pipeline used for training and inference."""

    model = HistGradientBoostingRegressor(**config.model_params)

    return Pipeline(
        steps=[
            ("preprocessor", build_preprocessor(config)),
            ("model", model),
        ]
    )
