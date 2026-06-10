"""Email delivery abstraction with outbox and SMTP modes."""

from __future__ import annotations

from app.core.config import Settings, get_settings
from app.shared.db import get_connection, get_database_path, initialize_database
from app.shared.utils import utc_now_iso
from app.notifications.smtp_adapter import (
    SMTPConfigError,
    SMTPDeliveryError,
    SMTPError,
    build_smtp_profile,
    send_smtp_email,
    validate_smtp_settings,
)


class EmailModeError(RuntimeError):
    pass


class EmailConfigError(RuntimeError):
    pass


class EmailDeliveryError(RuntimeError):
    pass


SMTP_AUDIT_REDACTED_BODY = "[redacted: sent via smtp]"
CONFIRMATION_INITIAL_PURPOSE = "confirmation_initial"
CONFIRMATION_RESEND_PURPOSE = "confirmation_resend"
PASSWORD_RESET_PURPOSE = "password_reset"


def _resolved_settings(settings: Settings | None = None) -> Settings:
    return settings or get_settings()


def _email_mode(settings: Settings) -> str:
    return (settings.email_mode or "").strip().lower()


def _record_email_outbox(
    recipient_email: str,
    subject: str,
    body_text: str,
    template_key: str,
    *,
    purpose: str,
    smtp_channel: str,
    from_address: str | None,
    provider_configured: bool,
    fallback_reason: str | None = None,
    status: str,
    error: str | None = None,
    sent_at: str | None = None,
    settings: Settings | None = None,
) -> int:
    current_settings = _resolved_settings(settings)
    database_path = get_database_path(current_settings)
    initialize_database(database_path)
    with get_connection(database_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO email_outbox (
                recipient_email, subject, body_text, template_key,
                purpose, smtp_channel, from_address, provider_configured,
                fallback_reason, status, created_at, sent_at, error
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                recipient_email,
                subject,
                body_text,
                template_key,
                purpose,
                smtp_channel,
                from_address,
                1 if provider_configured else 0,
                fallback_reason,
                status,
                utc_now_iso(),
                sent_at,
                error,
            ),
        )
        return int(cursor.lastrowid)


def _update_email_outbox(
    email_id: int,
    *,
    status: str,
    error: str | None = None,
    sent_at: str | None = None,
    body_text: str | None = None,
    settings: Settings | None = None,
) -> None:
    current_settings = _resolved_settings(settings)
    database_path = get_database_path(current_settings)
    initialize_database(database_path)
    updates = ["status = ?", "sent_at = ?", "error = ?"]
    params: list[object] = [status, sent_at, error]
    if body_text is not None:
        updates.insert(0, "body_text = ?")
        params.insert(0, body_text)
    params.append(int(email_id))
    with get_connection(database_path) as connection:
        connection.execute(
            f"UPDATE email_outbox SET {', '.join(updates)} WHERE id = ?",
            params,
        )


def _queue_email(
    recipient_email: str,
    subject: str,
    body_text: str,
    template_key: str,
    *,
    purpose: str,
    settings: Settings | None = None,
) -> int:
    current_settings = _resolved_settings(settings)
    mode = _email_mode(current_settings)
    if mode == "outbox":
        profile = build_smtp_profile(current_settings)
        return _record_email_outbox(
            recipient_email,
            subject,
            body_text,
            template_key,
            purpose=purpose,
            smtp_channel=profile.channel,
            from_address=profile.from_address,
            provider_configured=profile.configured,
            status="queued",
            settings=current_settings,
        )
    if mode == "smtp":
        try:
            profile = validate_smtp_settings(current_settings)
        except SMTPConfigError as exc:
            raise EmailConfigError(str(exc)) from exc
        email_id = _record_email_outbox(
            recipient_email,
            subject,
            SMTP_AUDIT_REDACTED_BODY,
            template_key,
            purpose=purpose,
            smtp_channel=profile.channel,
            from_address=profile.from_address,
            provider_configured=profile.configured,
            status="queued",
            settings=current_settings,
        )
        try:
            send_smtp_email(
                recipient_email=recipient_email,
                subject=subject,
                body_text=body_text,
                settings=current_settings,
            )
        except SMTPConfigError as exc:
            _update_email_outbox(
                email_id,
                status="failed",
                error=str(exc),
                body_text=SMTP_AUDIT_REDACTED_BODY,
                settings=current_settings,
            )
            raise EmailConfigError(str(exc)) from exc
        except SMTPDeliveryError as exc:
            _update_email_outbox(
                email_id,
                status="failed",
                error=str(exc),
                body_text=SMTP_AUDIT_REDACTED_BODY,
                settings=current_settings,
            )
            raise EmailDeliveryError(str(exc)) from exc
        except SMTPError as exc:
            _update_email_outbox(
                email_id,
                status="failed",
                error=str(exc),
                body_text=SMTP_AUDIT_REDACTED_BODY,
                settings=current_settings,
            )
            raise EmailDeliveryError("SMTP delivery failed") from exc
        _update_email_outbox(
            email_id,
            status="sent",
            sent_at=utc_now_iso(),
            body_text=SMTP_AUDIT_REDACTED_BODY,
            settings=current_settings,
        )
        return email_id
    raise EmailModeError(f"unsupported email mode: {current_settings.email_mode}")


def send_email_verification(
    recipient_email: str,
    verification_link: str,
    settings: Settings | None = None,
    *,
    purpose: str = CONFIRMATION_INITIAL_PURPOSE,
) -> int:
    subject = "Подтверждение email"
    body_text = (
        "Здравствуйте.\n\n"
        "Для подтверждения email используйте ссылку:\n"
        f"{verification_link}\n\n"
        "Если вы не регистрировались, просто игнорируйте это письмо."
    )
    return _queue_email(
        recipient_email,
        subject,
        body_text,
        "email_verification",
        purpose=purpose,
        settings=settings,
    )


def send_password_reset(
    recipient_email: str,
    reset_link: str,
    settings: Settings | None = None,
) -> int:
    subject = "Сброс пароля"
    body_text = (
        "Здравствуйте.\n\n"
        "Для сброса пароля используйте ссылку:\n"
        f"{reset_link}\n\n"
        "Если вы не запрашивали сброс, просто игнорируйте это письмо."
    )
    return _queue_email(
        recipient_email,
        subject,
        body_text,
        "password_reset",
        purpose=PASSWORD_RESET_PURPOSE,
        settings=settings,
    )
