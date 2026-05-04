"""Admin bootstrap CLI."""

from __future__ import annotations

import argparse
import sys

from app.auth.service import NotFoundError, RoleError, ValidationError, promote_user_to_admin
from app.core.config import get_settings
from app.shared.db import get_database_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m app.admin.cli")
    subparsers = parser.add_subparsers(dest="command", required=True)
    promote = subparsers.add_parser("promote-admin", help="Promote an existing user to admin")
    group = promote.add_mutually_exclusive_group(required=True)
    group.add_argument("--email", help="Existing verified user email")
    group.add_argument("--login", help="Existing verified user login")
    promote.add_argument("--database-path", help="Explicit SQLite database path for tests or operations")
    return parser


def _resolve_settings(database_path: str | None = None):
    settings = get_settings()
    if database_path:
        return settings.__class__(
            app_name=settings.app_name,
            app_env=settings.app_env,
            app_host=settings.app_host,
            app_port=settings.app_port,
            base_url=settings.base_url,
            database_path=database_path,
            session_cookie_name=settings.session_cookie_name,
            session_expiry_hours=settings.session_expiry_hours,
            session_cookie_secure=settings.session_cookie_secure,
            email_mode=settings.email_mode,
            email_verification_token_expiry_hours=settings.email_verification_token_expiry_hours,
            password_reset_token_expiry_minutes=settings.password_reset_token_expiry_minutes,
        )
    return settings


def _promote_admin(*, email: str | None, login: str | None, database_path: str | None) -> int:
    settings = _resolve_settings(database_path)
    identifier_kind = "email" if email else "login"
    identifier_value = email or login or ""
    try:
        user = promote_user_to_admin(
            identifier_kind=identifier_kind,
            identifier_value=identifier_value,
            settings=settings,
        )
    except NotFoundError:
        print("user not found", file=sys.stderr)
        return 1
    except RoleError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except ValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    if user.role == "admin":
        print("user is admin")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "promote-admin":
        return _promote_admin(email=args.email, login=args.login, database_path=args.database_path)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
