"""Session-bound CSRF helpers for browser form submissions."""

from __future__ import annotations

import base64
import hashlib
import hmac
import secrets
from collections.abc import Mapping

from fastapi import HTTPException, Request
from fastapi.responses import HTMLResponse, Response
from jinja2 import pass_context
from markupsafe import Markup, escape

from app.core.config import Settings, get_settings


CSRF_COOKIE_NAME = "ai_starter_community_csrf"
CSRF_FIELD_NAME = "_csrf_token"
_CSRF_TOKEN_LABEL = b"ai-starter-community-csrf-v1"


def _settings(settings: Settings | None = None) -> Settings:
    return settings or get_settings()


def _derive_session_csrf_token(session_token: str) -> str:
    digest = hmac.new(session_token.encode("utf-8"), _CSRF_TOKEN_LABEL, hashlib.sha256).digest()
    return base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")


def _csrf_token_from_cookies(cookies: Mapping[str, str], settings: Settings | None = None) -> str | None:
    resolved = _settings(settings)
    session_token = cookies.get(resolved.session_cookie_name)
    if session_token:
        return _derive_session_csrf_token(session_token)
    csrf_token = cookies.get(CSRF_COOKIE_NAME)
    return csrf_token or None


def issue_csrf_token(cookies: Mapping[str, str], settings: Settings | None = None) -> str:
    token = _csrf_token_from_cookies(cookies, settings=settings)
    if token:
        return token
    return secrets.token_urlsafe(32)


def configure_template_environment(templates) -> None:
    @pass_context
    def csrf_input(context) -> Markup:
        token = context.get("csrf_token")
        if not token:
            return Markup("")
        return Markup(
            f'<input type="hidden" name="{CSRF_FIELD_NAME}" value="{escape(str(token))}">'
        )

    templates.env.globals["csrf_input"] = csrf_input


def _set_csrf_cookie(response: Response, token: str, settings: Settings | None = None) -> None:
    resolved = _settings(settings)
    response.set_cookie(
        key=CSRF_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=resolved.session_cookie_secure,
        samesite="lax",
        path="/",
    )


def render_template_response(
    templates,
    request: Request,
    template_name: str,
    *,
    settings: Settings | None = None,
    status_code: int = 200,
    **context,
) -> HTMLResponse:
    resolved = _settings(settings)
    csrf_token = issue_csrf_token(request.cookies, settings=resolved)
    payload = {
        "request": request,
        "csrf_token": csrf_token,
    }
    payload.update(context)
    response = templates.TemplateResponse(request, template_name, payload, status_code=status_code)
    _set_csrf_cookie(response, csrf_token, settings=resolved)
    return response


def require_csrf_token(request: Request, submitted_token: str | None, settings: Settings | None = None) -> None:
    expected_token = _csrf_token_from_cookies(request.cookies, settings=settings)
    provided_token = (submitted_token or "").strip()
    if not expected_token or not provided_token or not hmac.compare_digest(provided_token, expected_token):
        raise HTTPException(status_code=403, detail="CSRF token is missing or invalid")
