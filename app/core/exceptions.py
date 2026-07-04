"""Application exceptions and FastAPI exception handlers."""

from __future__ import annotations

import logging
from uuid import uuid4

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


class AppException(Exception):
    """Base exception for expected application failures."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code: str = "application_error",
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(message)


class ModelLoadError(AppException):
    """Raised when the model artifact cannot be loaded."""

    def __init__(self, message: str) -> None:
        super().__init__(
            message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error_code="model_load_error",
        )


class PredictionError(AppException):
    """Raised when prediction fails."""

    def __init__(self, message: str) -> None:
        super().__init__(
            message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="prediction_error",
        )


def register_exception_handlers(app: FastAPI) -> None:
    """Register global exception handlers."""

    @app.exception_handler(AppException)
    async def app_exception_handler(
        request: Request, exc: AppException
    ) -> JSONResponse:
        request_id = _request_id(request)
        logger.warning(
            "Application error request_id=%s error_code=%s message=%s",
            request_id,
            exc.error_code,
            exc.message,
        )
        return _error_response(
            request_id=request_id,
            status_code=exc.status_code,
            error_code=exc.error_code,
            message=exc.message,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        request_id = _request_id(request)
        logger.info(
            "Validation error request_id=%s errors=%s", request_id, exc.errors()
        )
        return _error_response(
            request_id=request_id,
            status_code=422,
            error_code="validation_error",
            message="Request validation failed.",
            details=exc.errors(),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        request_id = _request_id(request)
        return _error_response(
            request_id=request_id,
            status_code=exc.status_code,
            error_code="http_error",
            message=str(exc.detail),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        request_id = _request_id(request)
        logger.exception("Unhandled error request_id=%s", request_id, exc_info=exc)
        return _error_response(
            request_id=request_id,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="internal_server_error",
            message="An unexpected error occurred.",
        )


def _request_id(request: Request) -> str:
    return getattr(request.state, "request_id", str(uuid4()))


def _error_response(
    *,
    request_id: str,
    status_code: int,
    error_code: str,
    message: str,
    details: object | None = None,
) -> JSONResponse:
    content = {
        "success": False,
        "request_id": request_id,
        "error": {
            "code": error_code,
            "message": message,
            "details": details,
        },
    }
    return JSONResponse(status_code=status_code, content=content)
