"""Common response schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    """Base structured response."""

    success: bool = True
    request_id: str = Field(..., examples=["8d540da1-1856-4571-8860-9ef09524f86a"])


class RootResponse(BaseResponse):
    """Root endpoint response."""

    message: str
    service: str
    version: str


class HealthResponse(BaseResponse):
    """Health endpoint response."""

    status: str
    model_loaded: bool
    environment: str
