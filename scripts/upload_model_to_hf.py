"""Upload the versioned model package to Hugging Face Model Hub."""

from __future__ import annotations

import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXPORT_DIR = (
    PROJECT_ROOT / "artifacts" / "huggingface" / "crop-yield-regressor" / "v1.0.0"
)
REQUIRED_FILES = {
    "README.md",
    "LICENSE",
    "VERSION",
    "artifact_manifest.json",
    "crop_yield_model.joblib",
    "crop_yield_preprocessor.joblib",
    "metrics.json",
    "model_metadata.json",
    "preprocessing_metadata.json",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Upload crop-yield-regressor artifacts to Hugging Face Model Hub."
    )
    parser.add_argument(
        "--repo-id",
        required=True,
        help="Target model repository, for example username/crop-yield-regressor.",
    )
    parser.add_argument(
        "--export-dir",
        type=Path,
        default=DEFAULT_EXPORT_DIR,
        help="Directory containing the Hugging Face-ready model package.",
    )
    parser.add_argument(
        "--revision",
        default="main",
        help="Target branch or revision on the Hugging Face repository.",
    )
    parser.add_argument(
        "--private",
        action="store_true",
        help="Create the repository as private if it does not already exist.",
    )
    return parser.parse_args()


def validate_export_dir(export_dir: Path) -> None:
    if not export_dir.exists():
        raise FileNotFoundError(f"Export directory does not exist: {export_dir}")

    missing_files = sorted(
        file_name
        for file_name in REQUIRED_FILES
        if not (export_dir / file_name).exists()
    )
    if missing_files:
        raise FileNotFoundError(
            f"Export directory is missing required files: {missing_files}"
        )


def upload_model(repo_id: str, export_dir: Path, revision: str, private: bool) -> str:
    validate_export_dir(export_dir)

    from huggingface_hub import HfApi

    api = HfApi()
    api.create_repo(
        repo_id=repo_id,
        repo_type="model",
        private=private,
        exist_ok=True,
    )
    commit_info = api.upload_folder(
        repo_id=repo_id,
        repo_type="model",
        folder_path=str(export_dir),
        revision=revision,
        commit_message="Upload crop yield prediction model artifacts",
    )
    return str(commit_info.commit_url)


def main() -> None:
    args = parse_args()
    commit_url = upload_model(
        repo_id=args.repo_id,
        export_dir=args.export_dir,
        revision=args.revision,
        private=args.private,
    )
    print(f"Uploaded model artifacts: {commit_url}")


if __name__ == "__main__":
    main()
