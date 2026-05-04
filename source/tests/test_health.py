def test_healthz(client):
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"ok": True, "service": "ai-starter-community"}


def test_readyz(client):
    response = client.get("/readyz")
    assert response.status_code == 200
    assert response.json() == {"ok": True, "ready": True}


def test_public_pages_still_work(client):
    root_response = client.get("/")
    login_response = client.get("/login")
    register_response = client.get("/register")
    forgot_response = client.get("/forgot-password")

    assert root_response.status_code == 200
    assert "Главная" in root_response.text
    assert login_response.status_code == 200
    assert register_response.status_code == 200
    assert forgot_response.status_code == 200
