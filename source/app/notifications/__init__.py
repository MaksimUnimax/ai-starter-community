"""Notifications module."""

from app.notifications.email_service import (
    send_account_block_activation_email,
    send_email_verification,
    send_password_reset,
)

__all__ = [
    "send_account_block_activation_email",
    "send_email_verification",
    "send_password_reset",
]
