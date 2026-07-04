"""FastAPI application entry point."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import get_settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging
from app.routers.prediction import router as prediction_router
from app.routers.system import router as system_router
from app.services.model_loader import load_model_service

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load application resources once during startup."""

    settings = get_settings()
    configure_logging(settings)
    logger.info("Starting %s in %s mode", settings.app_name, settings.environment)

    app.state.settings = settings
    app.state.model_service = load_model_service(settings)

    yield

    logger.info("Shutting down %s", settings.app_name)


def create_app() -> FastAPI:
    """Application factory used by ASGI servers and tests."""

    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=settings.api_version,
        description="Production-style crop yield prediction REST API.",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials="*" not in settings.cors_origins,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )
    register_exception_handlers(app)
    register_middlewares(app)
    app.include_router(system_router)
    app.include_router(prediction_router)
    mount_frontend(app)
    return app


def mount_frontend(app: FastAPI) -> None:
    """Serve the built React frontend when available."""

    settings = get_settings()
    if settings.frontend_dist_dir.exists():
        app.mount(
            "/",
            StaticFiles(directory=settings.frontend_dist_dir, html=True),
            name="frontend",
        )


def register_middlewares(app: FastAPI) -> None:
    """Register request middleware."""

    @app.middleware("http")
    async def request_context_middleware(request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid4()))
        request.state.request_id = request_id
        started_at = perf_counter()

        response = await call_next(request)
        duration_ms = round((perf_counter() - started_at) * 1000, 2)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time-Ms"] = str(duration_ms)

        logger.info(
            "request_id=%s method=%s path=%s status_code=%s duration_ms=%s",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        return response


app = create_app()
