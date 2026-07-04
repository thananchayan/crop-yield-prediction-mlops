"""Configuration objects for the training pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from ml.version import MODEL_VERSION

PROJECT_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class TrainingConfig:
    """Central configuration for reproducible model training."""

    dataset_path: Path = PROJECT_ROOT / "data" / "yield_df.csv"
    model_dir: Path = PROJECT_ROOT / "artifacts" / "models"
    metrics_dir: Path = PROJECT_ROOT / "artifacts" / "metrics"
    model_card_dir: Path = PROJECT_ROOT / "artifacts" / "model_cards"
    hf_export_dir: Path = PROJECT_ROOT / "artifacts" / "huggingface"
    logs_dir: Path = PROJECT_ROOT / "logs"
    model_version: str = MODEL_VERSION
    model_id: str = "crop-yield-regressor"
    hf_repo_id: str = "your-username/crop-yield-regressor"
    target_column: str = "hg/ha_yield"
    categorical_features: tuple[str, ...] = ("Area", "Item")
    numeric_features: tuple[str, ...] = (
        "Year",
        "average_rain_fall_mm_per_year",
        "pesticides_tonnes",
        "avg_temp",
    )
    test_size: float = 0.2
    random_state: int = 42
    model_name: str = "crop_yield_model.joblib"
    preprocessor_name: str = "crop_yield_preprocessor.joblib"
    metrics_name: str = "metrics.json"
    metadata_name: str = "model_metadata.json"
    preprocessing_metadata_name: str = "preprocessing_metadata.json"
    manifest_name: str = "artifact_manifest.json"
    version_file_name: str = "VERSION"
    license_name: str = "LICENSE"
    model_card_name: str = "README.md"
    model_params: dict[str, int | float | str | bool | None] = field(
        default_factory=lambda: {
            "max_iter": 300,
            "learning_rate": 0.08,
            "max_leaf_nodes": 31,
            "l2_regularization": 0.0,
            "random_state": 42,
        }
    )

    @property
    def feature_columns(self) -> list[str]:
        """Return the full feature list in model input order."""

        return [*self.categorical_features, *self.numeric_features]

    @property
    def model_path(self) -> Path:
        """Path where the fitted end-to-end model pipeline is saved."""

        return self.versioned_model_dir / self.model_name

    @property
    def preprocessor_path(self) -> Path:
        """Path where the fitted preprocessing pipeline is saved."""

        return self.versioned_model_dir / self.preprocessor_name

    @property
    def metrics_path(self) -> Path:
        """Path where evaluation metrics are saved."""

        return self.versioned_metrics_dir / self.metrics_name

    @property
    def metadata_path(self) -> Path:
        """Path where model metadata is saved."""

        return self.versioned_metrics_dir / self.metadata_name

    @property
    def preprocessing_metadata_path(self) -> Path:
        """Path where preprocessing metadata is saved."""

        return self.versioned_metrics_dir / self.preprocessing_metadata_name

    @property
    def model_card_path(self) -> Path:
        """Path where the generated model card is saved."""

        return self.versioned_model_card_dir / self.model_card_name

    @property
    def manifest_path(self) -> Path:
        """Path where the artifact manifest is saved."""

        return self.versioned_metrics_dir / self.manifest_name

    @property
    def version_file_path(self) -> Path:
        """Path where the plain-text version marker is saved."""

        return self.versioned_metrics_dir / self.version_file_name

    @property
    def license_path(self) -> Path:
        """Path to the project license copied into Hub exports."""

        return PROJECT_ROOT / self.license_name

    @property
    def versioned_model_dir(self) -> Path:
        """Directory containing model artifacts for this version."""

        return self.model_dir / self.model_version

    @property
    def versioned_metrics_dir(self) -> Path:
        """Directory containing metrics and metadata for this version."""

        return self.metrics_dir / self.model_version

    @property
    def versioned_model_card_dir(self) -> Path:
        """Directory containing model-card files for this version."""

        return self.model_card_dir / self.model_version

    @property
    def hf_export_path(self) -> Path:
        """Local Hugging Face Model Hub-ready export directory."""

        return self.hf_export_dir / self.model_id / self.model_version
