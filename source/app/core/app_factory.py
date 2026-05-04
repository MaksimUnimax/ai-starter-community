"""FastAPI application factory."""

from __future__ import annotations

from fastapi import FastAPI

from app.auth.routes import router as auth_router
from app.core.config import get_settings
from app.core.health import router as health_router
from app.public_landing.routes import router as landing_router
from app.user_cabinet.routes import router as cabinet_router


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name)
    app.include_router(health_router)
    app.include_router(landing_router)
    app.include_router(auth_router)
    app.include_router(cabinet_router)
    return app
