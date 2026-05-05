def test_landing_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "OpenScript — программы, боты и MVP без знаний и опыта" in response.text
    assert (
        '<meta name="description" content="OpenScript помогает людям без технического опыта создавать простые программы, боты, MVP, помощников, агентов и автоматизации под свои задачи.">'
        in response.text
    )
    assert "Создавайте свои первые программы без знаний и опыта" in response.text
    assert "Начать работу" in response.text
    assert "Как это работает" in response.text
    assert "Для кого OpenScript" in response.text
    assert "Какие задачи можно решать с OpenScript" in response.text
    assert "Полный доступ — 4 990 ₽" in response.text
    assert "Вопросы перед стартом" in response.text
    assert "/static/styles.css" in response.text
    assert "/register" in response.text


def test_login_and_register_pages(client):
    login_response = client.get("/login")
    login_head_response = client.head("/login")
    register_response = client.get("/register")
    check_email_response = client.get("/check-email")
    resend_response = client.get("/resend-verification")
    cabinet_response = client.get("/cabinet", follow_redirects=False)
    assert login_response.status_code == 200
    assert login_head_response.status_code == 200
    assert register_response.status_code == 200
    assert check_email_response.status_code == 200
    assert resend_response.status_code == 200
    assert cabinet_response.status_code == 303
    assert cabinet_response.headers["location"] == "/login"
    assert "Вход в аккаунт" in login_response.text
    assert "Регистрация" in register_response.text
    assert "Нет аккаунта?" in login_response.text
    assert "Зарегистрироваться" in login_response.text
    assert "Забыли пароль?" in login_response.text
    assert "Уже есть аккаунт?" in register_response.text
    assert "Войти" in register_response.text
    assert "Проверьте почту" in check_email_response.text
    assert "Не пришло письмо подтверждения?" in check_email_response.text
    assert "/resend-verification" in check_email_response.text
    assert "Повторная отправка письма подтверждения" in resend_response.text
    assert "/static/styles.css" in login_response.text
    assert "/static/styles.css" in register_response.text
    assert "Электронная почта или логин" in login_response.text
    assert "Электронная почта" in register_response.text
    assert "Подтверждение почты" not in login_response.text
    assert "Не пришло письмо подтверждения?" not in login_response.text
    assert "Отправить письмо подтверждения" not in login_response.text


def test_auth_utility_pages_use_shared_base_and_styles(client):
    check_email_response = client.get("/check-email")
    verify_email_response = client.get("/verify-email/example-token")
    forgot_response = client.get("/forgot-password")
    reset_response = client.get("/reset-password/example-token")
    resend_response = client.get("/resend-verification")

    assert check_email_response.status_code == 200
    assert verify_email_response.status_code == 200
    assert forgot_response.status_code == 200
    assert reset_response.status_code == 200
    assert resend_response.status_code == 200

    for response in (
        check_email_response,
        verify_email_response,
        forgot_response,
        reset_response,
        resend_response,
    ):
        assert "/static/styles.css" in response.text
        assert "Главная" in response.text
        assert "Вход / регистрация" in response.text
        assert "Личный кабинет" not in response.text
        assert "Работа с ИИ" not in response.text
        assert "Админ-панель" not in response.text

    assert "Не пришло письмо подтверждения?" in check_email_response.text
    assert "Укажите адрес электронной почты, чтобы мы смогли найти ваш аккаунт." in forgot_response.text
    assert "Если такой адрес электронной почты зарегистрирован" not in forgot_response.text
    assert "Подтвердить почту" not in forgot_response.text
    assert "Вернуться ко входу" in forgot_response.text
    assert "Войти" in reset_response.text or "Вернуться ко входу" in reset_response.text
    assert "Повторная отправка письма подтверждения" in resend_response.text


def test_placeholder_post_routes_redirect(client):
    login_response = client.post(
        "/login",
        data={"email_or_login": "user@example.com", "password": "secret"},
        follow_redirects=False,
    )
    register_response = client.post(
        "/register",
        data={
            "email": "user@example.com",
            "login": "user123",
            "password": "Secret123",
            "repeat_password": "Secret123",
        },
        follow_redirects=False,
    )
    logout_response = client.post("/logout", follow_redirects=False)
    assert login_response.status_code == 200
    assert register_response.status_code == 303
    assert logout_response.status_code == 303
