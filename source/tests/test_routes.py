def test_landing_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Главная" in response.text
    assert "Начните делать программы без знания кода" in response.text
    assert "Вход / регистрация" in response.text
    assert "/login" in response.text
    assert "/static/styles.css" in response.text
    assert "/register" not in response.text
    assert "Войти" not in response.text
    assert "Регистрация" not in response.text


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
    assert "Уже есть аккаунт?" in register_response.text
    assert "Войти" in register_response.text
    assert "Проверьте почту" in check_email_response.text
    assert "Повторная отправка" in resend_response.text
    assert "/static/styles.css" in login_response.text
    assert "/static/styles.css" in register_response.text
    assert "Электронная почта или логин" in login_response.text
    assert "Электронная почта" in register_response.text
    assert "Подтверждение почты" in login_response.text


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
