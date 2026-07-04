"""Shared utilities for training and artifact management."""

from __future__ import annotations

import json
import logging
import random
import shutil
import sys
from datetime import datetime, timezone
from hashlib import sha256
from importlib import metadata
from pathlib import Path
from typing import Any

import joblib
import numpy as np


def ensure_directories(paths: list[Path]) -> None:
    """Create required output directories."""

    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def configure_logging(log_dir: Path, level: int = logging.INFO) -> None:
    """Configure console and file logging for training runs."""

    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "training.log"

    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file),
        ],
        force=True,
    )


def set_random_seed(seed: int) -> None:
    """Set random seeds used by Python and NumPy."""

    random.seed(seed)
    np.random.seed(seed)


def save_json(payload: dict[str, Any], path: Path) -> None:
    """Persist a dictionary as formatted JSON."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, sort_keys=True)


def save_text(content: str, path: Path) -> None:
    """Persist text content using UTF-8 encoding."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def save_joblib(obj: Any, path: Path) -> None:
    """Persist an object using joblib."""

    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(obj, path)


def copy_file(source: Path, destination: Path) -> None:
    """Copy a file while creating the destination directory."""

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def file_sha256(path: Path) -> str:
    """Calculate the SHA-256 checksum of a file."""

    digest = sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def dependency_versions(package_names: list[str]) -> dict[str, str]:
    """Return installed package versions for reproducibility metadata."""

    versions = {"python": sys.version.split()[0]}
    for package_name in package_names:
        try:
            versions[package_name] = metadata.version(package_name)
        except metadata.PackageNotFoundError:
            versions[package_name] = "not-installed"
    return versions


def utc_now_iso() -> str:
    """Return a timezone-aware UTC timestamp."""

    return datetime.now(timezone.utc).isoformat()
