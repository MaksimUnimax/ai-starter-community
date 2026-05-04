"""Security helpers for password and token handling."""

from __future__ import annotations

import bcrypt
import hashlib
import secrets


def normalize_password_input(password: str) -> str:
    normalized = (password or "").strip()
    if not normalized:
        raise ValueError("password is required")
    if any(character.isspace() for character in normalized):
        raise ValueError("password must not contain spaces")
    return normalized


def validate_new_password(password: str) -> str:
    normalized = normalize_password_input(password)
    if len(normalized) < 8:
        raise ValueError("password must be at least 8 characters long")
    if len(normalized) > 128:
        raise ValueError("password must be at most 128 characters long")
    return normalized


def hash_password(password: str) -> str:
    normalized = validate_new_password(password)
    return bcrypt.hashpw(normalized.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    normalized = validate_new_password(password)
    try:
        return bcrypt.checkpw(normalized.encode("utf-8"), password_hash.encode("utf-8"))
    except (ValueError, TypeError):
        return False


def generate_session_token() -> str:
    return secrets.token_urlsafe(32)


def generate_auth_token() -> str:
    return secrets.token_urlsafe(32)


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
