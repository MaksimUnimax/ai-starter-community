"""Authentication service layer for registration, login, tokens, and sessions."""

from __future__ import annotations

import re
from datetime import timedelta

from app.auth.schemas import UserPublic
from app.core.config import Settings, get_settings
from app.notifications.email_service import send_email_verification, send_password_reset
from app.shared.db import get_connection, get_database_path, initialize_database
from app.shared.security import (
    generate_auth_token,
    generate_session_token,
    hash_password,
    hash_token,
    validate_new_password,
    verify_password,
)
from app.shared.utils import utc_now, utc_now_iso


EMAIL_TOKEN_TYPE = "email_verification"
PASSWORD_RESET_TOKEN_TYPE = "password_reset"
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
LOGIN_RE = re.compile(r"^[a-z0-9_-]{3,32}$")


class AuthError(Exception):
    """Base class for auth-domain errors."""


class ValidationError(AuthError):
    pass


class ConflictError(AuthError):
    pass


class UnauthorizedError(AuthError):
    pass


class NotVerifiedError(AuthError):
    pass


class NotFoundError(AuthError):
    pass


def _settings(settings: Settings | None = None) -> Settings:
    return settings or get_settings()


def _database_path(settings: Settings | None = None):
    return get_database_path(_settings(settings))


def _connection(settings: Settings | None = None):
    resolved = _settings(settings)
    path = _database_path(resolved)
    initialize_database(path)
    return get_connection(path)


def _public_user_from_row(row) -> UserPublic:
    return UserPublic(
        id=int(row["id"]),
        email=str(row["email"]),
        login=str(row["login"]),
        role=str(row["role"]),
        is_active=bool(row["is_active"]),
        access_status=str(row["access_status"]),
        email_verified_at=row["email_verified_at"],
    )


def _normalize_email(value: str) -> str:
    normalized = (value or "").strip().lower()
    if not normalized:
        raise ValidationError("email is required")
    if not EMAIL_RE.fullmatch(normalized):
        raise ValidationError("invalid email")
    return normalized


def _normalize_login(value: str) -> str:
    normalized = (value or "").strip().lower()
    if not normalized:
        raise ValidationError("login is required")
    if not LOGIN_RE.fullmatch(normalized):
        raise ValidationError("login must use lowercase letters, digits, underscore or hyphen")
    return normalized


def _normalize_identifier(value: str) -> tuple[str, str]:
    raw_value = (value or "").strip()
    if not raw_value:
        raise ValidationError("email or login is required")
    if "@" in raw_value:
        return "email", _normalize_email(raw_value)
    return "login", _normalize_login(raw_value)


def _normalize_password_for_login(password: str) -> str:
    return validate_new_password(password)


def _passwords_match(password: str, repeat_password: str) -> str:
    try:
        normalized_password = validate_new_password(password)
        normalized_repeat = validate_new_password(repeat_password)
    except ValueError as exc:
        raise ValidationError(str(exc)) from exc
    if normalized_password != normalized_repeat:
        raise ValidationError("passwords do not match")
    return normalized_password


def _build_public_url(settings: Settings, path: str) -> str:
    base_url = settings.base_url.rstrip("/")
    if not path.startswith("/"):
        path = f"/{path}"
    return f"{base_url}{path}"


def _issue_auth_token(
    connection,
    user_id: int,
    token_type: str,
    expires_at_iso: str,
    target_email: str | None = None,
) -> str:
    raw_token = generate_auth_token()
    connection.execute(
        """
        INSERT INTO auth_tokens (
            user_id, token_hash, token_type, target_email,
            created_at, expires_at, used_at, revoked_at
        )
        VALUES (?, ?, ?, ?, ?, ?, NULL, NULL)
        """,
        (
            user_id,
            hash_token(raw_token),
            token_type,
            target_email,
            utc_now_iso(),
            expires_at_iso,
        ),
    )
    return raw_token


def _fetch_user_by_id(user_id: int, settings: Settings | None = None) -> UserPublic | None:
    with _connection(settings) as connection:
        row = connection.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return _public_user_from_row(row) if row else None


def _fetch_user_by_identifier(identifier_kind: str, identifier_value: str, settings: Settings | None = None):
    with _connection(settings) as connection:
        query = "SELECT * FROM users WHERE email = ?" if identifier_kind == "email" else "SELECT * FROM users WHERE login = ?"
        return connection.execute(query, (identifier_value,)).fetchone()


def register_user(
    email: str,
    login: str,
    password: str,
    repeat_password: str,
    settings: Settings | None = None,
) -> UserPublic:
    resolved = _settings(settings)
    normalized_email = _normalize_email(email)
    normalized_login = _normalize_login(login)
    normalized_password = _passwords_match(password, repeat_password)

    with _connection(resolved) as connection:
        existing = connection.execute(
            "SELECT id FROM users WHERE email = ? OR login = ?",
            (normalized_email, normalized_login),
        ).fetchone()
        if existing:
            raise ConflictError("email or login already exists")

        now_iso = utc_now_iso()
        password_hash = hash_password(normalized_password)
        cursor = connection.execute(
            """
            INSERT INTO users (
                email, login, password_hash, role, is_active,
                email_verified_at, access_status, created_at, updated_at
            )
            VALUES (?, ?, ?, 'user', 1, NULL, 'not_activated', ?, ?)
            """,
            (normalized_email, normalized_login, password_hash, now_iso, now_iso),
        )
        user_id = int(cursor.lastrowid)
        verification_token = _issue_auth_token(
            connection,
            user_id=user_id,
            token_type=EMAIL_TOKEN_TYPE,
            expires_at_iso=(utc_now() + timedelta(hours=resolved.email_verification_token_expiry_hours)).isoformat(),
            target_email=normalized_email,
        )

    verification_link = _build_public_url(resolved, f"/verify-email/{verification_token}")
    send_email_verification(normalized_email, verification_link, settings=resolved)
    user = _fetch_user_by_id(user_id, settings=resolved)
    if user is None:
        raise AuthError("registration succeeded but user lookup failed")
    return user


def verify_email(token: str, settings: Settings | None = None) -> UserPublic:
    resolved = _settings(settings)
    token_hash = hash_token(token or "")
    now_iso = utc_now_iso()
    with _connection(resolved) as connection:
        row = connection.execute(
            """
            SELECT at.id AS token_id, at.user_id, u.id, u.email, u.login, u.role,
                   u.is_active, u.email_verified_at, u.access_status
            FROM auth_tokens AS at
            JOIN users AS u ON u.id = at.user_id
            WHERE at.token_hash = ?
              AND at.token_type = ?
              AND at.used_at IS NULL
              AND at.revoked_at IS NULL
              AND at.expires_at > ?
            """,
            (token_hash, EMAIL_TOKEN_TYPE, now_iso),
        ).fetchone()
        if not row:
            raise NotFoundError("verification token not found or expired")
        connection.execute(
            "UPDATE users SET email_verified_at = ?, updated_at = ? WHERE id = ?",
            (now_iso, now_iso, int(row["user_id"])),
        )
        connection.execute(
            "UPDATE auth_tokens SET used_at = ? WHERE id = ?",
            (now_iso, int(row["token_id"])),
        )
        user_row = connection.execute("SELECT * FROM users WHERE id = ?", (int(row["user_id"]),)).fetchone()
        if user_row is None:
            raise AuthError("verified user lookup failed")
        return _public_user_from_row(user_row)


def authenticate_user(email_or_login: str, password: str, settings: Settings | None = None) -> UserPublic:
    identifier_kind, identifier_value = _normalize_identifier(email_or_login)
    resolved = _settings(settings)
    user_row = _fetch_user_by_identifier(identifier_kind, identifier_value, settings=resolved)
    if user_row is None or not bool(user_row["is_active"]):
        raise UnauthorizedError("invalid credentials")
    if user_row["email_verified_at"] is None:
        raise NotVerifiedError("email is not verified")
    try:
        if not verify_password(password, str(user_row["password_hash"])):
            raise UnauthorizedError("invalid credentials")
    except ValueError as exc:
        raise ValidationError(str(exc)) from exc
    return _public_user_from_row(user_row)


def create_session(user_id: int, settings: Settings | None = None) -> str:
    resolved = _settings(settings)
    raw_token = generate_session_token()
    token_hash = hash_token(raw_token)
    now = utc_now()
    expires_at = now + timedelta(hours=resolved.session_expiry_hours)
    with _connection(resolved) as connection:
        connection.execute(
            """
            INSERT INTO sessions (
                user_id, token_hash, created_at, expires_at, revoked_at
            )
            VALUES (?, ?, ?, ?, NULL)
            """,
            (user_id, token_hash, now.isoformat(), expires_at.isoformat()),
        )
    return raw_token


def get_user_by_session_token(raw_token: str | None, settings: Settings | None = None) -> UserPublic | None:
    if not raw_token:
        return None
    resolved = _settings(settings)
    token_hash = hash_token(raw_token)
    now_iso = utc_now_iso()
    with _connection(resolved) as connection:
        row = connection.execute(
            """
            SELECT u.*
            FROM sessions AS s
            JOIN users AS u ON u.id = s.user_id
            WHERE s.token_hash = ?
              AND s.revoked_at IS NULL
              AND s.expires_at > ?
              AND u.is_active = 1
            """,
            (token_hash, now_iso),
        ).fetchone()
        return _public_user_from_row(row) if row else None


def revoke_session(raw_token: str | None, settings: Settings | None = None) -> bool:
    if not raw_token:
        return False
    resolved = _settings(settings)
    token_hash = hash_token(raw_token)
    now_iso = utc_now_iso()
    with _connection(resolved) as connection:
        cursor = connection.execute(
            """
            UPDATE sessions
            SET revoked_at = ?
            WHERE token_hash = ? AND revoked_at IS NULL
            """,
            (now_iso, token_hash),
        )
        return cursor.rowcount > 0


def create_password_reset_request(email: str, settings: Settings | None = None) -> bool:
    resolved = _settings(settings)
    normalized_email = _normalize_email(email)
    with _connection(resolved) as connection:
        user_row = connection.execute(
            "SELECT * FROM users WHERE email = ?",
            (normalized_email,),
        ).fetchone()
        if user_row is None or not bool(user_row["is_active"]) or user_row["email_verified_at"] is None:
            return False
        now_iso = utc_now_iso()
        connection.execute(
            """
            UPDATE auth_tokens
            SET revoked_at = ?
            WHERE user_id = ? AND token_type = ? AND used_at IS NULL AND revoked_at IS NULL
            """,
            (now_iso, int(user_row["id"]), PASSWORD_RESET_TOKEN_TYPE),
        )
        reset_token = _issue_auth_token(
            connection,
            user_id=int(user_row["id"]),
            token_type=PASSWORD_RESET_TOKEN_TYPE,
            expires_at_iso=(utc_now() + timedelta(minutes=resolved.password_reset_token_expiry_minutes)).isoformat(),
            target_email=normalized_email,
        )

    reset_link = _build_public_url(resolved, f"/reset-password/{reset_token}")
    send_password_reset(normalized_email, reset_link, settings=resolved)
    return True


def reset_password(
    token: str,
    new_password: str,
    repeat_password: str,
    settings: Settings | None = None,
) -> UserPublic:
    resolved = _settings(settings)
    normalized_password = _passwords_match(new_password, repeat_password)
    token_hash = hash_token(token or "")
    now_iso = utc_now_iso()
    with _connection(resolved) as connection:
        row = connection.execute(
            """
            SELECT at.id AS token_id, at.user_id, u.id, u.email, u.login, u.role,
                   u.is_active, u.email_verified_at, u.access_status
            FROM auth_tokens AS at
            JOIN users AS u ON u.id = at.user_id
            WHERE at.token_hash = ?
              AND at.token_type = ?
              AND at.used_at IS NULL
              AND at.revoked_at IS NULL
              AND at.expires_at > ?
            """,
            (token_hash, PASSWORD_RESET_TOKEN_TYPE, now_iso),
        ).fetchone()
        if not row:
            raise NotFoundError("password reset token not found or expired")
        new_password_hash = hash_password(normalized_password)
        connection.execute(
            "UPDATE users SET password_hash = ?, updated_at = ? WHERE id = ?",
            (new_password_hash, now_iso, int(row["user_id"])),
        )
        connection.execute(
            "UPDATE auth_tokens SET used_at = ? WHERE id = ?",
            (now_iso, int(row["token_id"])),
        )
        connection.execute(
            "UPDATE sessions SET revoked_at = ? WHERE user_id = ? AND revoked_at IS NULL",
            (now_iso, int(row["user_id"])),
        )
        user_row = connection.execute("SELECT * FROM users WHERE id = ?", (int(row["user_id"]),)).fetchone()
        if user_row is None:
            raise AuthError("reset user lookup failed")
        return _public_user_from_row(user_row)
