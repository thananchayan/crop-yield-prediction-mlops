"""Preprocessing pipeline definitions."""

from __future__ import annotations

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from ml.config import TrainingConfig


def build_preprocessor(config: TrainingConfig) -> ColumnTransformer:
    """Build the preprocessing pipeline for numeric and categorical columns."""

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", _build_one_hot_encoder()),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, list(config.numeric_features)),
            ("categorical", categorical_pipeline, list(config.categorical_features)),
        ],
        remainder="drop",
    )


def _build_one_hot_encoder() -> OneHotEncoder:
    """Build a OneHotEncoder across supported scikit-learn versions."""

    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        return OneHotEncoder(handle_unknown="ignore", sparse=False)
