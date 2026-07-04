"""Model evaluation helpers."""

from __future__ import annotations

import math

import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def evaluate_regression(y_true, y_pred) -> dict[str, float]:
    """Calculate standard regression metrics."""

    mse = mean_squared_error(y_true, y_pred)
    return {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "mse": float(mse),
        "rmse": float(math.sqrt(mse)),
        "r2": float(r2_score(y_true, y_pred)),
        "mean_prediction": float(np.mean(y_pred)),
    }
