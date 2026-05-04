"""Health and readiness checks."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/healthz")
def healthz() -> dict[str, object]:
    return {"ok": True, "service": "ai-starter-community"}


@router.get("/readyz")
def readyz() -> dict[str, object]:
    return {"ok": True, "ready": True}
