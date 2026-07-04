"""Model card generation for Hugging Face Model Hub exports."""

from __future__ import annotations

from typing import Any


def generate_model_card(
    model_metadata: dict[str, Any],
    preprocessing_metadata: dict[str, Any],
    metrics: dict[str, float],
) -> str:
    """Create a Hugging Face-compatible model card."""

    feature_columns = "\n".join(
        f"- `{column}`" for column in model_metadata["feature_columns"]
    )
    metrics_table = "\n".join(
        f"| {metric} | {value:.6f} |" for metric, value in metrics.items()
    )
    categorical_features = ", ".join(
        f"`{column}`" for column in preprocessing_metadata["categorical_features"]
    )
    numeric_features = ", ".join(
        f"`{column}`" for column in preprocessing_metadata["numeric_features"]
    )

    return f"""---
library_name: scikit-learn
license: mit
tags:
- tabular-regression
- crop-yield
- agriculture
- sklearn
- mlops
metrics:
- mean_absolute_error
- mean_squared_error
- r2
pipeline_tag: tabular-regression
---

# {model_metadata["model_id"]}

## Model Details

- **Version:** `{model_metadata["model_version"]}`
- **Model type:** `{model_metadata["model_type"]}`
- **Task:** Crop yield regression
- **Target:** `{model_metadata["target_column"]}`
- **Target unit:** hectograms per hectare (`hg/ha`)
- **Framework:** scikit-learn
- **Training timestamp:** `{model_metadata["trained_at"]}`

## Intended Use

This model predicts crop yield from country, crop, year, rainfall, pesticide usage,
and average temperature features. It is intended for portfolio demonstration,
MLOps workflows, API serving examples, and educational experimentation.

It should not be used as the sole basis for agricultural, financial, insurance,
or policy decisions without validation on current local agronomic data.

## Features

{feature_columns}

## Preprocessing

- Numeric features: {numeric_features}
- Categorical features: {categorical_features}
- Numeric imputation: `{preprocessing_metadata["numeric_imputation"]}`
- Numeric scaling: `{preprocessing_metadata["numeric_scaling"]}`
- Categorical imputation: `{preprocessing_metadata["categorical_imputation"]}`
- Categorical encoding: `{preprocessing_metadata["categorical_encoding"]}`
- Unknown categories during inference: `{preprocessing_metadata["unknown_category_policy"]}`
- Encoded feature count: `{preprocessing_metadata["encoded_feature_count"]}`

## Evaluation

Holdout split configuration:

- Test size: `{model_metadata["test_size"]}`
- Random state: `{model_metadata["random_state"]}`

| Metric | Value |
| --- | ---: |
{metrics_table}

## Reproducibility

- Dataset SHA-256: `{model_metadata["dataset_sha256"]}`
- Training rows after cleaning: `{model_metadata["dataset_rows"]}`
- Train rows: `{model_metadata["train_rows"]}`
- Test rows: `{model_metadata["test_rows"]}`
- Python version: `{model_metadata["environment"]["python"]}`
- pandas version: `{model_metadata["environment"]["pandas"]}`
- numpy version: `{model_metadata["environment"]["numpy"]}`
- scikit-learn version: `{model_metadata["environment"]["scikit-learn"]}`
- joblib version: `{model_metadata["environment"]["joblib"]}`

The full sklearn inference artifact is saved as:

- `{model_metadata["model_artifact"]}`

The fitted preprocessing artifact is saved as:

- `{model_metadata["preprocessor_artifact"]}`

## Versioned Artifacts

This export contains:

- `crop_yield_model.joblib`
- `crop_yield_preprocessor.joblib`
- `metrics.json`
- `model_metadata.json`
- `preprocessing_metadata.json`
- `artifact_manifest.json`
- `VERSION`
- `LICENSE`
- `README.md`

## Limitations

The model is trained on historical tabular data and may not generalize to unseen
regions, new farming practices, extreme climate events, or changed measurement
methods. Input values should be validated by the serving API before inference.
"""
