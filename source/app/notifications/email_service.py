"""Dev/test email delivery abstraction backed by SQLite outbox rows."""

from __future__ import annotations

from app.core.config import Settings, get_settings
from app.shared.db import get_connection, get_database_path, initialize_database
from app.shared.utils import utc_now_iso


class EmailModeError(RuntimeError):
    pass


def _resolved_settings(settings: Settings | None = None) -> Settings:
    return settings or get_settings()


def _queue_email(
    recipient_email: str,
    subject: str,
    body_text: str,
    template_key: str,
    settings: Settings | None = None,
) -> int:
    current_settings = _resolved_settings(settings)
    if current_settings.email_mode.lower() != "outbox":
        raise EmailModeError("only outbox email mode is supported in this stage")
    database_path = get_database_path(current_settings)
    initialize_database(database_path)
    with get_connection(database_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO email_outbox (
                recipient_email, subject, body_text, template_key,
                status, created_at, sent_at, error
            )
            VALUES (?, ?, ?, ?, 'queued', ?, NULL, NULL)
            """,
            (recipient_email, subject, body_text, template_key, utc_now_iso()),
        )
        return int(cursor.lastrowid)


def send_email_verification(
    recipient_email: str,
    verification_link: str,
    settings: Settings | None = None,
) -> int:
    subject = "AI Starter Community: подтверждение email"
    body_text = (
        "Здравствуйте.\n\n"
        "Для подтверждения email используйте ссылку:\n"
        f"{verification_link}\n\n"
        "Если вы не регистрировались, просто игнорируйте это письмо."
    )
    return _queue_email(recipient_email, subject, body_text, "email_verification", settings=settings)


def send_password_reset(
    recipient_email: str,
    reset_link: str,
    settings: Settings | None = None,
) -> int:
    subject = "AI Starter Community: сброс пароля"
    body_text = (
        "Здравствуйте.\n\n"
        "Для сброса пароля используйте ссылку:\n"
        f"{reset_link}\n\n"
        "Если вы не запрашивали сброс, просто игнорируйте это письмо."
    )
    return _queue_email(recipient_email, subject, body_text, "password_reset", settings=settings)
