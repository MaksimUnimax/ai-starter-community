"""FastAPI application factory."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.auth.routes import router as auth_router
from app.admin.routes import router as admin_router
from app.core.config import get_settings
from app.core.health import router as health_router
from app.public_landing.routes import router as landing_router
from app.materials.routes import router as materials_router
from app.user_cabinet.routes import router as cabinet_router


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name)
    app.mount(
        "/static",
        StaticFiles(directory=str(Path(__file__).resolve().parents[1] / "static")),
        name="static",
    )
    app.include_router(health_router)
    app.include_router(landing_router)
    app.include_router(auth_router)
    app.include_router(cabinet_router)
    app.include_router(materials_router)
    app.include_router(admin_router)
    return app
