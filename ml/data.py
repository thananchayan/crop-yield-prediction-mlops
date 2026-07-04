"""Dataset loading and validation logic."""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from ml.config import TrainingConfig

logger = logging.getLogger(__name__)


def load_dataset(path: Path) -> pd.DataFrame:
    """Load the crop yield dataset from CSV."""

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    logger.info("Loading dataset from %s", path)
    dataset = pd.read_csv(path)
    logger.info("Loaded dataset with shape rows=%s columns=%s", *dataset.shape)
    return dataset


def prepare_dataset(dataset: pd.DataFrame, config: TrainingConfig) -> pd.DataFrame:
    """Clean schema issues and enforce feature/target columns."""

    dataset = dataset.copy()
    dataset = _drop_index_columns(dataset)
    _validate_required_columns(dataset, config)

    selected_columns = [*config.feature_columns, config.target_column]
    dataset = dataset[selected_columns]
    dataset = dataset.drop_duplicates()

    for column in config.numeric_features + (config.target_column,):
        dataset[column] = pd.to_numeric(dataset[column], errors="coerce")

    for column in config.categorical_features:
        dataset[column] = dataset[column].astype("string").str.strip()

    dataset = dataset.dropna(subset=[config.target_column])
    logger.info("Prepared dataset with shape rows=%s columns=%s", *dataset.shape)
    return dataset


def split_features_target(
    dataset: pd.DataFrame, config: TrainingConfig
) -> tuple[pd.DataFrame, pd.Series]:
    """Split the prepared dataset into model features and target."""

    features = dataset[config.feature_columns]
    target = dataset[config.target_column]
    return features, target


def _drop_index_columns(dataset: pd.DataFrame) -> pd.DataFrame:
    """Remove CSV-exported index columns such as 'Unnamed: 0'."""

    index_like_columns = [
        column for column in dataset.columns if column.startswith("Unnamed:")
    ]
    if index_like_columns:
        logger.info("Dropping index-like columns: %s", index_like_columns)
        dataset = dataset.drop(columns=index_like_columns)
    return dataset


def _validate_required_columns(dataset: pd.DataFrame, config: TrainingConfig) -> None:
    """Raise a clear error when expected dataset columns are missing."""

    required_columns = set(config.feature_columns + [config.target_column])
    missing_columns = sorted(required_columns.difference(dataset.columns))
    if missing_columns:
        raise ValueError(f"Dataset is missing required columns: {missing_columns}")
