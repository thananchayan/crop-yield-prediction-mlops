"""Shared pytest fixtures for API tests."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture(scope="session")
def client() -> TestClient:
    """Create a test client with the real startup lifecycle."""

    app = create_app()
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def valid_prediction_payload() -> dict[str, object]:
    """Return a valid prediction request payload."""

    return {
        "area": "Albania",
        "item": "Maize",
        "year": 1990,
        "average_rain_fall_mm_per_year": 1485.0,
        "pesticides_tonnes": 121.0,
        "avg_temp": 16.37,
    }
