"""Provider-agnostic SMTP delivery helper."""

from __future__ import annotations

from dataclasses import dataclass
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


@dataclass(frozen=True)
class SMTPProfile:
    channel: str
    from_address: str | None
    from_name: str | None
    host: str | None
    port: int | None
    username: str | None
    password: str | None
    use_tls: bool
    use_starttls: bool
    timeout_seconds: int
    from_address_name: str
    host_name: str
    port_name: str
    username_name: str
    password_name: str
    use_tls_name: str
    use_starttls_name: str

    @property
    def configured(self) -> bool:
        if not self.from_address or not self.host or self.port is None or self.port <= 0:
            return False
        if bool(self.username) ^ bool(self.password):
            return False
        if self.use_tls and self.use_starttls:
            return False
        return True


def _resolved_settings(settings: Settings | None = None) -> Settings:
    return settings or get_settings()


def _smtp_profile_from_settings(settings: Settings, smtp_channel: str) -> SMTPProfile:
    if smtp_channel not in {"primary", "registration"}:
        raise SMTPConfigError(f"unsupported smtp channel: {smtp_channel}")
    return SMTPProfile(
        channel="primary",
        from_address=settings.email_from_address,
        from_name=settings.email_from_name,
        host=settings.smtp_host,
        port=settings.smtp_port,
        username=settings.smtp_username,
        password=settings.smtp_password,
        use_tls=settings.smtp_use_tls,
        use_starttls=settings.smtp_use_starttls,
        timeout_seconds=settings.smtp_timeout_seconds,
        from_address_name="EMAIL_FROM_ADDRESS",
        host_name="SMTP_HOST",
        port_name="SMTP_PORT",
        username_name="SMTP_USERNAME",
        password_name="SMTP_PASSWORD",
        use_tls_name="SMTP_USE_TLS",
        use_starttls_name="SMTP_USE_STARTTLS",
    )


def build_smtp_profile(settings: Settings | None = None, *, smtp_channel: str = "primary") -> SMTPProfile:
    current_settings = _resolved_settings(settings)
    return _smtp_profile_from_settings(current_settings, smtp_channel)


def validate_smtp_settings(settings: Settings | None = None, *, smtp_channel: str = "primary") -> SMTPProfile:
    profile = build_smtp_profile(settings, smtp_channel=smtp_channel)
    missing: list[str] = []
    if not profile.from_address:
        missing.append(profile.from_address_name)
    if not profile.host:
        missing.append(profile.host_name)
    if profile.port is None:
        missing.append(profile.port_name)
    if bool(profile.username) ^ bool(profile.password):
        missing.append(f"{profile.username_name}/{profile.password_name}")
    if profile.use_tls and profile.use_starttls:
        raise SMTPConfigError(f"{profile.use_tls_name} and {profile.use_starttls_name} cannot both be true")
    if missing:
        raise SMTPConfigError(f"missing required SMTP settings: {', '.join(missing)}")
    if profile.port is not None and profile.port <= 0:
        raise SMTPConfigError(f"{profile.port_name} must be a positive integer")
    return profile


def _build_message(
    *,
    recipient_email: str,
    subject: str,
    body_text: str,
    profile: SMTPProfile,
    settings: Settings | None = None,
) -> EmailMessage:
    message = EmailMessage()
    current_settings = _resolved_settings(settings)
    from_name = profile.from_name or current_settings.app_name
    message["Subject"] = subject
    message["From"] = formataddr((from_name, profile.from_address or ""))
    message["To"] = recipient_email
    message.set_content(body_text)
    return message


def send_smtp_email(
    *,
    recipient_email: str,
    subject: str,
    body_text: str,
    settings: Settings | None = None,
    smtp_channel: str = "primary",
    smtp_profile: SMTPProfile | None = None,
) -> None:
    current_settings = _resolved_settings(settings)
    current_profile = smtp_profile or validate_smtp_settings(current_settings, smtp_channel=smtp_channel)
    message = _build_message(
        recipient_email=recipient_email,
        subject=subject,
        body_text=body_text,
        profile=current_profile,
        settings=current_settings,
    )

    try:
        if current_profile.use_tls:
            with smtplib.SMTP_SSL(
                current_profile.host,
                current_profile.port,
                timeout=current_profile.timeout_seconds,
            ) as client:
                if current_profile.username and current_profile.password:
                    client.login(current_profile.username, current_profile.password)
                client.send_message(message)
        else:
            with smtplib.SMTP(
                current_profile.host,
                current_profile.port,
                timeout=current_profile.timeout_seconds,
            ) as client:
                if current_profile.use_starttls:
                    client.starttls()
                if current_profile.username and current_profile.password:
                    client.login(current_profile.username, current_profile.password)
                client.send_message(message)
    except SMTPError:
        raise
    except Exception as exc:  # pragma: no cover - exercised through mocked transport
        raise SMTPDeliveryError("SMTP delivery failed") from exc
