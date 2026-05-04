"""Authentication routes for registration, verification, login, logout, and reset."""

from pathlib import Path

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from jinja2 import ChoiceLoader, FileSystemLoader

from app.auth.service import (
    AuthError,
    ConflictError,
    NotFoundError,
    NotVerifiedError,
    UnauthorizedError,
    ValidationError,
    authenticate_user,
    create_password_reset_request,
    create_session,
    register_user,
    reset_password,
    revoke_session,
    resend_verification_request,
    verify_email,
)
from app.core.config import get_settings
router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))
templates.env.loader = ChoiceLoader(
    [
        templates.env.loader,
        FileSystemLoader(str(Path(__file__).resolve().parents[1] / "shared" / "templates")),
    ]
)


def _template(request: Request, template_name: str, **context) -> HTMLResponse:
    payload = {"request": request, "title": context.pop("title", "Страница")}
    payload.update(context)
    return templates.TemplateResponse(request, template_name, payload)


def _login_notice(request: Request) -> str | None:
    query = request.query_params
    if query.get("registered"):
        return "Проверьте почту и подтвердите её по ссылке."
    if query.get("verified"):
        return "Почта подтверждена. Теперь можно войти."
    if query.get("reset"):
        return "Пароль изменён. Войдите с новым паролем."
    return None


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request) -> HTMLResponse:
    return _template(
        request,
        "register.html",
        title="Регистрация",
        notice=request.query_params.get("notice"),
        error=request.query_params.get("error"),
        email="",
        login="",
    )


@router.post("/register", response_class=HTMLResponse)
def register_submit(
    request: Request,
    email: str = Form(default=""),
    login: str = Form(default=""),
    password: str = Form(default=""),
    repeat_password: str = Form(default=""),
) -> HTMLResponse:
    try:
        register_user(email=email, login=login, password=password, repeat_password=repeat_password)
    except (ValidationError, ConflictError) as exc:
        return _template(
            request,
            "register.html",
            title="Регистрация",
            error=str(exc),
            email=email,
            login=login,
        )
    except AuthError as exc:
        return _template(
            request,
            "register.html",
            title="Регистрация",
            error=str(exc),
            email=email,
            login=login,
        )
    return RedirectResponse(url="/check-email?registered=1", status_code=303)


@router.get("/check-email", response_class=HTMLResponse)
def check_email_page(request: Request) -> HTMLResponse:
    if request.query_params.get("registered"):
        message = (
            "Аккаунт создан. Письмо с подтверждением отправлено. "
            "В предпросмотре письмо сохраняется во внутреннем почтовом ящике, "
            "а внешний почтовый провайдер ещё не подключён. Подтвердите почту перед входом."
        )
    elif request.query_params.get("resent"):
        message = (
            "Новое письмо с подтверждением отправлено. Проверьте почту и подтвердите её перед входом."
        )
    else:
        message = (
            "Проверьте почту и подтвердите её по ссылке. После подтверждения можно войти в кабинет."
        )
    return _template(
        request,
        "check_email.html",
        title="Проверка почты",
        message=message,
    )


@router.head("/check-email")
def check_email_head(request: Request) -> HTMLResponse:
    return check_email_page(request)


@router.get("/resend-verification", response_class=HTMLResponse)
def resend_verification_page(request: Request) -> HTMLResponse:
    return _template(
        request,
        "resend_verification.html",
        title="Повторная отправка письма",
        notice=request.query_params.get("notice"),
        error=request.query_params.get("error"),
        email="",
    )


@router.head("/resend-verification")
def resend_verification_head(request: Request) -> HTMLResponse:
    return resend_verification_page(request)


@router.post("/resend-verification", response_class=HTMLResponse)
def resend_verification_submit(
    request: Request,
    email: str = Form(default=""),
) -> HTMLResponse:
    try:
        resend_verification_request(email=email)
    except ValidationError as exc:
        return _template(
            request,
            "resend_verification.html",
            title="Повторная отправка письма",
            error=str(exc),
            email=email,
        )
    return _template(
        request,
        "resend_verification.html",
        title="Повторная отправка письма",
        notice="Если аккаунт существует и почта ещё не подтверждена, мы отправили новое письмо.",
        email="",
    )


@router.get("/verify-email/{token}", response_class=HTMLResponse)
def verify_email_page(request: Request, token: str) -> HTMLResponse:
    try:
        user = verify_email(token)
    except NotFoundError:
        return _template(
            request,
            "verify_email.html",
            title="Подтверждение почты",
            success=False,
            message="Ссылка недействительна или истекла.",
        )
    except AuthError as exc:
        return _template(
            request,
            "verify_email.html",
            title="Подтверждение почты",
            success=False,
            message=str(exc),
        )
    return _template(
        request,
        "verify_email.html",
        title="Подтверждение почты",
        success=True,
        message=f"Почта подтверждена для {user.email}. Теперь можно войти.",
    )


@router.head("/verify-email/{token}")
def verify_email_head(request: Request, token: str) -> HTMLResponse:
    return verify_email_page(request, token)


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request) -> HTMLResponse:
    return _template(
        request,
        "login.html",
        title="Вход",
        notice=_login_notice(request),
        error=request.query_params.get("error"),
        email_or_login="",
    )


@router.head("/login")
def login_head(request: Request) -> HTMLResponse:
    return login_page(request)


@router.post("/login")
def login_submit(
    request: Request,
    email_or_login: str = Form(default=""),
    password: str = Form(default=""),
):
    settings = get_settings()
    try:
        user = authenticate_user(email_or_login=email_or_login, password=password, settings=settings)
        session_token = create_session(user.id, settings=settings)
    except NotVerifiedError:
        return _template(
            request,
            "login.html",
            title="Вход",
            error="Почта не подтверждена. Проверьте почту или запросите новое письмо.",
            unverified=True,
            email_or_login=email_or_login,
        )
    except ValidationError as exc:
        return _template(
            request,
            "login.html",
            title="Вход",
            error=str(exc),
            email_or_login=email_or_login,
        )
    except UnauthorizedError:
        return _template(
            request,
            "login.html",
            title="Вход",
            error="Неверная почта, логин или пароль.",
            email_or_login=email_or_login,
        )
    except AuthError as exc:
        return _template(
            request,
            "login.html",
            title="Вход",
            error=str(exc),
            email_or_login=email_or_login,
        )
    response = RedirectResponse(url="/cabinet", status_code=303)
    response.set_cookie(
        key=settings.session_cookie_name,
        value=session_token,
        max_age=settings.session_expiry_hours * 3600,
        httponly=True,
        secure=settings.session_cookie_secure,
        samesite="lax",
        path="/",
    )
    return response


@router.post("/logout")
def logout(request: Request) -> RedirectResponse:
    settings = get_settings()
    session_token = request.cookies.get(settings.session_cookie_name)
    if session_token:
        revoke_session(session_token, settings=settings)
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie(key=settings.session_cookie_name, path="/")
    return response


@router.get("/forgot-password", response_class=HTMLResponse)
def forgot_password_page(request: Request) -> HTMLResponse:
    return _template(
        request,
        "forgot_password.html",
        title="Сброс пароля",
        notice=request.query_params.get("notice"),
        error=request.query_params.get("error"),
        email="",
    )


@router.head("/forgot-password")
def forgot_password_head(request: Request) -> HTMLResponse:
    return forgot_password_page(request)


@router.post("/forgot-password", response_class=HTMLResponse)
def forgot_password_submit(
    request: Request,
    email: str = Form(default=""),
) -> HTMLResponse:
    try:
        create_password_reset_request(email=email)
    except ValidationError as exc:
        return _template(
            request,
            "forgot_password.html",
            title="Сброс пароля",
            error=str(exc),
            email=email,
        )
    return _template(
        request,
        "forgot_password.html",
        title="Сброс пароля",
        notice="Если такой адрес электронной почты зарегистрирован, мы отправим ссылку для восстановления.",
        email="",
    )


@router.get("/reset-password/{token}", response_class=HTMLResponse)
def reset_password_page(request: Request, token: str) -> HTMLResponse:
    return _template(
        request,
        "reset_password.html",
        title="Новый пароль",
        token=token,
        error=request.query_params.get("error"),
        notice=request.query_params.get("notice"),
        success=False,
    )


@router.head("/reset-password/{token}")
def reset_password_head(request: Request, token: str) -> HTMLResponse:
    return reset_password_page(request, token)


@router.post("/reset-password", response_class=HTMLResponse)
def reset_password_submit(
    request: Request,
    token: str = Form(default=""),
    password: str = Form(default=""),
    repeat_password: str = Form(default=""),
) -> HTMLResponse:
    try:
        reset_password(token=token, new_password=password, repeat_password=repeat_password)
    except (ValidationError, NotFoundError, AuthError) as exc:
        return _template(
            request,
            "reset_password.html",
            title="Новый пароль",
            token=token,
            error=str(exc),
            success=False,
        )
    return _template(
        request,
        "reset_password.html",
        title="Новый пароль",
        token="",
        success=True,
        notice="Пароль изменён. Теперь можно войти в систему.",
    )
