"""Authenticated encryption helpers for account-block password secrets."""

from __future__ import annotations

import base64
import binascii
import secrets

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from app.core.config import Settings, get_settings


ENCRYPTED_SECRET_PREFIX = "enc:v1:"
AES_GCM_NONCE_SIZE = 12
AES_GCM_KEY_SIZE = 32


class PasswordSecretCryptoError(ValueError):
    """Base class for account-block password-secret crypto errors."""


class PasswordSecretKeyMissingError(PasswordSecretCryptoError):
    """Raised when encryption is required but the runtime key is missing."""


class PasswordSecretEnvelopeError(PasswordSecretCryptoError):
    """Raised when an encrypted secret envelope is malformed."""


class PasswordSecretDecryptError(PasswordSecretCryptoError):
    """Raised when decryption fails."""


def _settings(settings: Settings | None = None) -> Settings:
    return settings or get_settings()


def _base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _base64url_decode(value: str, *, field_name: str) -> bytes:
    raw_value = (value or "").strip()
    if not raw_value:
        raise PasswordSecretEnvelopeError(f"{field_name} is required")
    padded_value = raw_value + "=" * (-len(raw_value) % 4)
    try:
        return base64.b64decode(padded_value.encode("ascii"), altchars=b"-_", validate=True)
    except (binascii.Error, UnicodeError) as exc:
        raise PasswordSecretEnvelopeError(f"{field_name} is invalid") from exc


def _decode_key_material(settings: Settings | None = None) -> bytes:
    resolved = _settings(settings)
    encoded_key = getattr(resolved, "account_blocks_password_secret_key", None)
    if not encoded_key:
        raise PasswordSecretKeyMissingError("password_secret encryption key is not configured")
    key = _base64url_decode(encoded_key, field_name="password_secret encryption key")
    if len(key) != AES_GCM_KEY_SIZE:
        raise PasswordSecretEnvelopeError("password_secret encryption key is invalid")
    return key


def encrypt_password_secret(password_secret: str, *, settings: Settings | None = None) -> str:
    normalized = (password_secret or "").strip()
    if not normalized:
        return ""

    key = _decode_key_material(settings)
    nonce = secrets.token_bytes(AES_GCM_NONCE_SIZE)
    ciphertext = AESGCM(key).encrypt(nonce, normalized.encode("utf-8"), None)
    return f"{ENCRYPTED_SECRET_PREFIX}{_base64url_encode(nonce)}.{_base64url_encode(ciphertext)}"


def decrypt_password_secret(stored_value: str | None, *, settings: Settings | None = None) -> str:
    normalized = "" if stored_value is None else str(stored_value)
    if not normalized:
        return ""
    if not normalized.startswith(ENCRYPTED_SECRET_PREFIX):
        return normalized

    key = _decode_key_material(settings)
    payload = normalized[len(ENCRYPTED_SECRET_PREFIX) :]
    try:
        nonce_text, ciphertext_text = payload.split(".", 1)
    except ValueError as exc:
        raise PasswordSecretEnvelopeError("password_secret envelope is invalid") from exc

    nonce = _base64url_decode(nonce_text, field_name="password_secret nonce")
    ciphertext = _base64url_decode(ciphertext_text, field_name="password_secret ciphertext")
    if len(nonce) != AES_GCM_NONCE_SIZE:
        raise PasswordSecretEnvelopeError("password_secret nonce is invalid")
    if not ciphertext:
        raise PasswordSecretEnvelopeError("password_secret ciphertext is invalid")

    try:
        plaintext = AESGCM(key).decrypt(nonce, ciphertext, None)
    except Exception as exc:  # pragma: no cover - cryptography validates internals
        raise PasswordSecretDecryptError("password_secret could not be decrypted") from exc

    try:
        return plaintext.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise PasswordSecretDecryptError("password_secret could not be decrypted") from exc


def store_password_secret(password_secret: str | None, *, settings: Settings | None = None) -> str:
    normalized = "" if password_secret is None else str(password_secret).strip()
    if not normalized:
        return ""
    return encrypt_password_secret(normalized, settings=settings)
