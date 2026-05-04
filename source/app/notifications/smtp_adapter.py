"""Provider-agnostic SMTP delivery helper."""

from __future__ import annotations

from email.message import EmailMessage
from email.utils import formataddr
import smtplib

from app.core.config import Settings, get_settings


class SMTPError(RuntimeError):
    """Base SMTP transport error."""


class SMTPConfigError(SMTPError):
    """Raised when SMTP configuration is missing or invalid."""


class SMTPDeliveryError(SMTPError):
    """Raised when SMTP transport fails at runtime."""


def _resolved_settings(settings: Settings | None = None) -> Settings:
    return settings or get_settings()


def validate_smtp_settings(settings: Settings | None = None) -> Settings:
    current_settings = _resolved_settings(settings)
    missing: list[str] = []
    if not current_settings.email_from_address:
        missing.append("EMAIL_FROM_ADDRESS")
    if not current_settings.smtp_host:
        missing.append("SMTP_HOST")
    if current_settings.smtp_port is None:
        missing.append("SMTP_PORT")
    if bool(current_settings.smtp_username) ^ bool(current_settings.smtp_password):
        missing.append("SMTP_USERNAME/SMTP_PASSWORD")
    if current_settings.smtp_use_tls and current_settings.smtp_use_starttls:
        raise SMTPConfigError("SMTP_USE_TLS and SMTP_USE_STARTTLS cannot both be true")
    if missing:
        raise SMTPConfigError(f"missing required SMTP settings: {', '.join(missing)}")
    if current_settings.smtp_port is not None and current_settings.smtp_port <= 0:
        raise SMTPConfigError("SMTP_PORT must be a positive integer")
    return current_settings


def _build_message(
    *,
    recipient_email: str,
    subject: str,
    body_text: str,
    settings: Settings,
) -> EmailMessage:
    message = EmailMessage()
    from_name = settings.email_from_name or settings.app_name
    message["Subject"] = subject
    message["From"] = formataddr((from_name, settings.email_from_address or ""))
    message["To"] = recipient_email
    message.set_content(body_text)
    return message


def send_smtp_email(
    *,
    recipient_email: str,
    subject: str,
    body_text: str,
    settings: Settings | None = None,
) -> None:
    current_settings = validate_smtp_settings(settings)
    message = _build_message(
        recipient_email=recipient_email,
        subject=subject,
        body_text=body_text,
        settings=current_settings,
    )

    try:
        if current_settings.smtp_use_tls:
            with smtplib.SMTP_SSL(
                current_settings.smtp_host,
                current_settings.smtp_port,
                timeout=current_settings.smtp_timeout_seconds,
            ) as client:
                if current_settings.smtp_username and current_settings.smtp_password:
                    client.login(current_settings.smtp_username, current_settings.smtp_password)
                client.send_message(message)
        else:
            with smtplib.SMTP(
                current_settings.smtp_host,
                current_settings.smtp_port,
                timeout=current_settings.smtp_timeout_seconds,
            ) as client:
                if current_settings.smtp_use_starttls:
                    client.starttls()
                if current_settings.smtp_username and current_settings.smtp_password:
                    client.login(current_settings.smtp_username, current_settings.smtp_password)
                client.send_message(message)
    except SMTPError:
        raise
    except Exception as exc:  # pragma: no cover - exercised through mocked transport
        raise SMTPDeliveryError("SMTP delivery failed") from exc
