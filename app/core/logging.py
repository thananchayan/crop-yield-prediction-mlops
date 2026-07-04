"""Logging configuration for the API."""

from __future__ import annotations

import logging

from app.core.config import Settings


def configure_logging(settings: Settings) -> None:
    """Configure process-wide API logging."""

    logging.basicConfig(
        level=settings.log_level.upper(),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        force=True,
    )
