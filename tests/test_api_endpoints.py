"""API endpoint tests."""

from __future__ import annotations

from ml.version import MODEL_VERSION


def test_root_endpoint(client) -> None:
    response = client.get("/")

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["service"] == "Crop Yield Prediction API"
    assert payload["version"] == MODEL_VERSION
    assert payload["request_id"]


def test_health_endpoint(client) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload == {
        "success": True,
        "request_id": payload["request_id"],
        "status": "healthy",
        "model_loaded": True,
        "environment": "development",
    }


def test_version_endpoint(client) -> None:
    response = client.get("/version")

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["api_version"] == MODEL_VERSION
    assert payload["model"]["id"] == "crop-yield-regressor"
    assert payload["model"]["version"] == MODEL_VERSION
    assert payload["model"]["type"] == "HistGradientBoostingRegressor"
    assert "r2" in payload["model"]["metrics"]


def test_predict_endpoint(client, valid_prediction_payload) -> None:
    response = client.post("/predict", json=valid_prediction_payload)

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["prediction"] > 0
    assert payload["unit"] == "hg/ha"
    assert payload["model_id"] == "crop-yield-regressor"
    assert payload["model_version"] == MODEL_VERSION
    assert response.headers["x-request-id"] == payload["request_id"]


def test_predict_missing_required_field(client, valid_prediction_payload) -> None:
    valid_prediction_payload.pop("avg_temp")

    response = client.post("/predict", json=valid_prediction_payload)

    assert response.status_code == 422
    payload = response.json()
    assert payload["success"] is False
    assert payload["error"]["code"] == "validation_error"
    assert payload["error"]["message"] == "Request validation failed."
    assert payload["error"]["details"][0]["loc"] == ["body", "avg_temp"]


def test_predict_wrong_datatype(client, valid_prediction_payload) -> None:
    valid_prediction_payload["year"] = "not-a-year"

    response = client.post("/predict", json=valid_prediction_payload)

    assert response.status_code == 422
    payload = response.json()
    assert payload["success"] is False
    assert payload["error"]["code"] == "validation_error"
    assert payload["error"]["details"][0]["loc"] == ["body", "year"]


def test_predict_invalid_values(client, valid_prediction_payload) -> None:
    valid_prediction_payload["avg_temp"] = 100

    response = client.post("/predict", json=valid_prediction_payload)

    assert response.status_code == 422
    payload = response.json()
    assert payload["success"] is False
    assert payload["error"]["code"] == "validation_error"
    assert payload["error"]["details"][0]["loc"] == ["body", "avg_temp"]


def test_404_handling(client) -> None:
    response = client.get("/does-not-exist")

    assert response.status_code == 404
    payload = response.json()
    assert payload["success"] is False
    assert payload["error"]["code"] == "http_error"
    assert payload["error"]["message"] == "Not Found"
    assert payload["request_id"]
