def test_landing_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "AI Starter Community" in response.text
    assert "Начните делать программы без знания кода" in response.text
    assert "/register" in response.text
    assert "/login" in response.text


def test_login_and_register_pages(client):
    login_response = client.get("/login")
    register_response = client.get("/register")
    check_email_response = client.get("/check-email")
    resend_response = client.get("/resend-verification")
    cabinet_response = client.get("/cabinet", follow_redirects=False)
    assert login_response.status_code == 200
    assert register_response.status_code == 200
    assert check_email_response.status_code == 200
    assert resend_response.status_code == 200
    assert cabinet_response.status_code == 303
    assert cabinet_response.headers["location"] == "/login"
    assert "Вход" in login_response.text
    assert "Регистрация" in register_response.text
    assert "Проверьте email" in check_email_response.text
    assert "Повторная отправка" in resend_response.text


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
