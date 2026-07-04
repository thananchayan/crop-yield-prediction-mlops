"""Train and evaluate the crop yield regression model."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Any

from sklearn.model_selection import train_test_split

from ml.config import TrainingConfig
from ml.data import load_dataset, prepare_dataset, split_features_target
from ml.evaluation import evaluate_regression
from ml.model_card import generate_model_card
from ml.modeling import build_model_pipeline
from ml.utils import (
    configure_logging,
    copy_file,
    dependency_versions,
    ensure_directories,
    file_sha256,
    save_joblib,
    save_json,
    save_text,
    set_random_seed,
    utc_now_iso,
)

logger = logging.getLogger(__name__)


def train(config: TrainingConfig) -> dict[str, float]:
    """Run the full training pipeline and persist artifacts."""

    ensure_directories(
        [
            config.versioned_model_dir,
            config.versioned_metrics_dir,
            config.versioned_model_card_dir,
            config.hf_export_path,
            config.logs_dir,
        ]
    )
    configure_logging(config.logs_dir)
    set_random_seed(config.random_state)

    logger.info("Starting crop yield model training")
    logger.info("Model version: %s", config.model_version)
    logger.info("Training configuration: %s", config)

    raw_dataset = load_dataset(config.dataset_path)
    dataset_sha256 = file_sha256(config.dataset_path)
    dataset = prepare_dataset(raw_dataset, config)
    features, target = split_features_target(dataset, config)

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=config.test_size,
        random_state=config.random_state,
    )
    logger.info(
        "Train/test split complete: train_rows=%s test_rows=%s",
        len(x_train),
        len(x_test),
    )

    pipeline = build_model_pipeline(config)
    pipeline.fit(x_train, y_train)
    logger.info("Model training complete")

    predictions = pipeline.predict(x_test)
    metrics = evaluate_regression(y_test, predictions)
    logger.info("Evaluation metrics: %s", metrics)

    fitted_preprocessor = pipeline.named_steps["preprocessor"]
    model = pipeline.named_steps["model"]
    preprocessing_metadata = build_preprocessing_metadata(
        fitted_preprocessor=fitted_preprocessor,
        config=config,
    )

    save_joblib(pipeline, config.model_path)
    save_joblib(fitted_preprocessor, config.preprocessor_path)

    metadata = {
        "model_id": config.model_id,
        "model_version": config.model_version,
        "hf_repo_id": config.hf_repo_id,
        "license": "mit",
        "trained_at": utc_now_iso(),
        "dataset_path": str(config.dataset_path),
        "dataset_sha256": dataset_sha256,
        "dataset_rows": int(len(dataset)),
        "train_rows": int(len(x_train)),
        "test_rows": int(len(x_test)),
        "target_column": config.target_column,
        "feature_columns": config.feature_columns,
        "categorical_features": list(config.categorical_features),
        "numeric_features": list(config.numeric_features),
        "test_size": config.test_size,
        "random_state": config.random_state,
        "model_type": model.__class__.__name__,
        "model_params": config.model_params,
        "model_path": str(config.model_path),
        "preprocessor_path": str(config.preprocessor_path),
        "model_artifact": config.model_name,
        "preprocessor_artifact": config.preprocessor_name,
        "model_sha256": file_sha256(config.model_path),
        "preprocessor_sha256": file_sha256(config.preprocessor_path),
        "environment": dependency_versions(
            ["pandas", "numpy", "scikit-learn", "joblib"]
        ),
        "metrics": metrics,
    }
    model_card = generate_model_card(
        model_metadata=metadata,
        preprocessing_metadata=preprocessing_metadata,
        metrics=metrics,
    )

    save_json(metrics, config.metrics_path)
    save_json(metadata, config.metadata_path)
    save_json(preprocessing_metadata, config.preprocessing_metadata_path)
    save_text(model_card, config.model_card_path)
    save_text(f"{config.model_version}\n", config.version_file_path)
    copy_file(config.license_path, config.hf_export_path / config.license_name)
    manifest = build_artifact_manifest(config)
    save_json(manifest, config.manifest_path)
    export_hugging_face_package(config)

    logger.info("Saved model pipeline to %s", config.model_path)
    logger.info("Saved preprocessing pipeline to %s", config.preprocessor_path)
    logger.info("Saved metrics to %s", config.metrics_path)
    logger.info("Saved metadata to %s", config.metadata_path)
    logger.info(
        "Saved preprocessing metadata to %s", config.preprocessing_metadata_path
    )
    logger.info("Saved model card to %s", config.model_card_path)
    logger.info("Saved artifact manifest to %s", config.manifest_path)
    logger.info("Prepared Hugging Face export at %s", config.hf_export_path)

    return metrics


def build_preprocessing_metadata(
    fitted_preprocessor: Any, config: TrainingConfig
) -> dict[str, Any]:
    """Describe the fitted preprocessing pipeline for reproducibility."""

    categorical_pipeline = fitted_preprocessor.named_transformers_["categorical"]
    encoder = categorical_pipeline.named_steps["encoder"]
    categories = {
        feature: [str(value) for value in values]
        for feature, values in zip(
            config.categorical_features, encoder.categories_, strict=True
        )
    }

    return {
        "model_version": config.model_version,
        "feature_columns": config.feature_columns,
        "numeric_features": list(config.numeric_features),
        "categorical_features": list(config.categorical_features),
        "numeric_imputation": "median",
        "numeric_scaling": "standard_scaler",
        "categorical_imputation": "most_frequent",
        "categorical_encoding": "one_hot_encoder",
        "unknown_category_policy": "ignore",
        "encoded_feature_count": int(len(fitted_preprocessor.get_feature_names_out())),
        "encoded_feature_names": [
            str(feature) for feature in fitted_preprocessor.get_feature_names_out()
        ],
        "categories": categories,
    }


def export_hugging_face_package(config: TrainingConfig) -> None:
    """Create a local directory that can be uploaded to Hugging Face Model Hub."""

    files_to_copy = {
        config.model_path: config.hf_export_path / config.model_name,
        config.preprocessor_path: config.hf_export_path / config.preprocessor_name,
        config.metrics_path: config.hf_export_path / config.metrics_name,
        config.metadata_path: config.hf_export_path / config.metadata_name,
        config.preprocessing_metadata_path: (
            config.hf_export_path / config.preprocessing_metadata_name
        ),
        config.manifest_path: config.hf_export_path / config.manifest_name,
        config.version_file_path: config.hf_export_path / config.version_file_name,
        config.license_path: config.hf_export_path / config.license_name,
        config.model_card_path: config.hf_export_path / config.model_card_name,
    }

    for source, destination in files_to_copy.items():
        copy_file(source, destination)


def build_artifact_manifest(config: TrainingConfig) -> dict[str, Any]:
    """Build a checksum manifest for the versioned artifact package."""

    artifact_paths = [
        config.model_path,
        config.preprocessor_path,
        config.metrics_path,
        config.metadata_path,
        config.preprocessing_metadata_path,
        config.model_card_path,
        config.version_file_path,
        config.license_path,
    ]

    return {
        "model_id": config.model_id,
        "model_version": config.model_version,
        "hf_repo_id": config.hf_repo_id,
        "created_at": utc_now_iso(),
        "artifacts": [
            {
                "file_name": path.name,
                "path": str(path),
                "sha256": file_sha256(path),
                "size_bytes": path.stat().st_size,
            }
            for path in artifact_paths
        ],
    }


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for local training runs."""

    parser = argparse.ArgumentParser(
        description="Train the crop yield prediction model."
    )
    parser.add_argument(
        "--dataset-path",
        type=Path,
        default=TrainingConfig.dataset_path,
        help="Path to the training CSV dataset.",
    )
    parser.add_argument(
        "--model-version",
        default=TrainingConfig.model_version,
        help="Semantic model version to attach to generated artifacts.",
    )
    parser.add_argument(
        "--hf-repo-id",
        default=TrainingConfig.hf_repo_id,
        help="Target Hugging Face Model Hub repository ID.",
    )
    return parser.parse_args()


def main() -> None:
    """CLI entry point."""

    args = parse_args()
    config = TrainingConfig(
        dataset_path=args.dataset_path,
        model_version=args.model_version,
        hf_repo_id=args.hf_repo_id,
    )
    train(config)


if __name__ == "__main__":
    main()
