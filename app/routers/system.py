"""System and metadata endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request

from app.core.config import Settings, get_settings
from app.schemas.common import HealthResponse, RootResponse
from app.services.dependencies import get_model_service
from app.services.model_loader import ModelService

router = APIRouter(tags=["system"])


@router.get("/", response_model=RootResponse)
def root(request: Request, settings: Settings = Depends(get_settings)) -> RootResponse:
    """Return basic API information."""

    return RootResponse(
        request_id=request.state.request_id,
        message="Crop yield prediction API is running.",
        service=settings.app_name,
        version=settings.api_version,
    )


@router.get("/health", response_model=HealthResponse)
def health(
    request: Request,
    settings: Settings = Depends(get_settings),
    model_service: ModelService = Depends(get_model_service),
) -> HealthResponse:
    """Return service health."""

    return HealthResponse(
        request_id=request.state.request_id,
        status="healthy" if model_service.is_loaded else "unhealthy",
        model_loaded=model_service.is_loaded,
        environment=settings.environment,
    )


@router.get("/version")
def version(
    request: Request,
    settings: Settings = Depends(get_settings),
    model_service: ModelService = Depends(get_model_service),
) -> dict[str, object]:
    """Return API and model version information."""

    metadata = model_service.metadata
    return {
        "success": True,
        "request_id": request.state.request_id,
        "api_version": settings.api_version,
        "model": {
            "id": metadata.model_id,
            "version": metadata.model_version,
            "type": metadata.model_type,
            "target": metadata.target_column,
            "metrics": metadata.metrics,
        },
    }
