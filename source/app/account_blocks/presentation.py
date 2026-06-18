"""Shared account-block presentation and selection helpers."""

from __future__ import annotations

from fastapi import Request

from app.auth.service import ValidationError, get_user_by_email, list_users_for_admin, role_label_ru


ACCOUNT_BLOCK_MANAGEMENT_QUERY_PARAM = "account_blocks_user_email"
ACCOUNT_BLOCK_NOTICE_QUERY_PARAM = "account_blocks_notice"
ACCOUNT_BLOCK_NOTICE_MESSAGES = {
    "created": "Блок создан.",
    "updated": "Блок сохранён.",
    "deleted": "Блок удалён.",
    "activated": "Блок активирован.",
    "renewed": "Активация продлена.",
    "activated_email_sent": "Блок активирован. Уведомление отправлено на почту пользователя.",
    "activated_email_failed": "Блок активирован, но письмо отправить не удалось.",
    "selected_user_not_found": "Пользователь не найден.",
}
ACCOUNT_BLOCK_TYPE_LABELS = {
    "chatgpt": "ChatGPT",
    "server": "Сервер",
    "mail": "Почта",
    "vpn": "ВПН",
}
ACCOUNT_BLOCK_CARD_TITLE_LABELS = {
    "chatgpt": "Chat",
}
ACCOUNT_BLOCK_CARD_TYPE_LABELS = {
    "chatgpt": "GPT",
}
ACCOUNT_BLOCK_STATUS_LABELS = {
    "active": "Активно",
    "inactive": "Неактивно",
    "expired": "Истекло",
}


def _user_attr(user, key: str):
    if isinstance(user, dict):
        return user.get(key)
    return getattr(user, key)


def account_block_notice(request: Request) -> str | None:
    notice_key = (request.query_params.get(ACCOUNT_BLOCK_NOTICE_QUERY_PARAM) or "").strip().lower()
    return ACCOUNT_BLOCK_NOTICE_MESSAGES.get(notice_key)


def account_block_type_options() -> list[dict[str, str]]:
    return [
        {"value": "chatgpt", "label": "ChatGPT"},
        {"value": "server", "label": "Сервер"},
        {"value": "mail", "label": "Почта"},
        {"value": "vpn", "label": "ВПН"},
    ]


def account_block_owner_summary(user) -> dict[str, object]:
    return {
        "id": int(_user_attr(user, "id")),
        "email": _user_attr(user, "email"),
        "login": _user_attr(user, "login"),
        "role": _user_attr(user, "role"),
        "role_label": _user_attr(user, "role_label") if isinstance(user, dict) else role_label_ru(str(_user_attr(user, "role"))),
        "display_label": f"{_user_attr(user, 'login')} · {_user_attr(user, 'email')}",
    }


def account_block_owner_options(settings) -> list[dict[str, object]]:
    return [
        {
            "email": _user_attr(owner, "email"),
            "login": _user_attr(owner, "login"),
            "role": _user_attr(owner, "role"),
            "role_label": role_label_ru(str(_user_attr(owner, "role"))),
            "display_label": f"{_user_attr(owner, 'login')} · {_user_attr(owner, 'email')}",
        }
        for owner in list_users_for_admin(settings=settings)
    ]


def account_block_owner_email(settings, owner_user_id: int) -> str | None:
    for owner in list_users_for_admin(settings=settings):
        if int(_user_attr(owner, "id")) == int(owner_user_id):
            email = _user_attr(owner, "email")
            return None if email is None else str(email)
    return None


def selected_account_block_email(request: Request, fallback_email: str) -> str:
    raw_email = (request.query_params.get(ACCOUNT_BLOCK_MANAGEMENT_QUERY_PARAM) or "").strip()
    return raw_email or fallback_email


def resolve_account_block_selected_user(
    user,
    settings,
    request: Request,
    *,
    manage_mode: bool,
) -> tuple[object | None, str, str | None]:
    selected_email = selected_account_block_email(request, _user_attr(user, "email"))
    notice = account_block_notice(request)
    if not manage_mode:
        return user, _user_attr(user, "email"), notice
    if selected_email != _user_attr(user, "email"):
        try:
            selected_user = get_user_by_email(selected_email, settings=settings)
        except ValidationError:
            return None, selected_email, "Пользователь не найден."
        if selected_user is None:
            return None, selected_email, "Пользователь не найден."
        return selected_user, selected_email, notice
    return user, _user_attr(user, "email"), notice


def selected_email_for_block(request: Request, settings, fallback_email: str, owner_user_id: int) -> str:
    selected_email = selected_account_block_email(request, fallback_email)
    if selected_email != fallback_email:
        return selected_email
    owner_email = account_block_owner_email(settings, owner_user_id)
    return owner_email or fallback_email


def account_block_card_context(block, copy_data, owner_summary: dict[str, object] | None = None) -> dict[str, object]:
    type_label = ACCOUNT_BLOCK_TYPE_LABELS.get(block.type, block.type)
    return {
        "id": block.id,
        "owner_user_id": block.owner_user_id,
        "owner": owner_summary,
        "type": block.type,
        "type_label": type_label,
        "display_title": ACCOUNT_BLOCK_CARD_TITLE_LABELS.get(block.type, block.title),
        "display_type_label": ACCOUNT_BLOCK_CARD_TYPE_LABELS.get(block.type, type_label),
        "title": block.title,
        "login": copy_data.login,
        "password_secret": copy_data.password_secret,
        "status": block.status,
        "status_label": ACCOUNT_BLOCK_STATUS_LABELS.get(block.status, block.status),
        "duration_days": block.duration_days,
        "activation_day": block.activation_day,
        "activation_summary": block.activation_summary,
        "is_active": block.is_active,
        "is_expired": block.is_expired,
    }
