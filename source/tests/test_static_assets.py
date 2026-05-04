from __future__ import annotations


def test_stylesheet_is_served(client):
    response = client.get("/static/styles.css")
    assert response.status_code == 200
    assert ".card" in response.text
    assert ".button-primary" in response.text
    assert ".top-nav" in response.text
    assert ".table-actions" in response.text
    assert ".button-danger" in response.text
    assert ".form-actions" in response.text
    assert ".textarea" in response.text
    assert ".select" in response.text
