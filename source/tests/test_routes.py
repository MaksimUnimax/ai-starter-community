from fastapi.testclient import TestClient

from app.main import app


def test_landing_page():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "AI Starter Community" in response.text
    assert "Начните делать программы без знания кода" in response.text
    assert "/register" in response.text
    assert "/login" in response.text


def test_login_and_register_pages():
    client = TestClient(app)
    login_response = client.get("/login")
    register_response = client.get("/register")
    cabinet_response = client.get("/cabinet")
    assert login_response.status_code == 200
    assert register_response.status_code == 200
    assert cabinet_response.status_code == 200
    assert "Вход" in login_response.text
    assert "Регистрация" in register_response.text
    assert "Доступ не активирован" in cabinet_response.text


def test_placeholder_post_routes_redirect():
    client = TestClient(app)
    login_response = client.post("/login", data={"email": "user@example.com", "password": "secret"}, follow_redirects=False)
    register_response = client.post("/register", data={"email": "user@example.com", "password": "secret"}, follow_redirects=False)
    logout_response = client.post("/logout", follow_redirects=False)
    assert login_response.status_code == 303
    assert register_response.status_code == 303
    assert logout_response.status_code == 303
