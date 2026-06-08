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
    assert ".nav-form" in response.text
    assert "button.nav-button" in response.text
    assert ".inline-form" in response.text
    assert ".compact-form" in response.text
    assert ".danger-zone" in response.text
    assert ".empty-state" in response.text
    assert ".accounts-card" in response.text
    assert ".accounts-grid" in response.text
    assert ".account-card" in response.text
    assert ".account-password-row" in response.text
    assert "display: flex;" in response.text
    assert "width: min(100%, 320px);" in response.text
    assert "max-width: 340px;" in response.text
    assert ".accounts-builder .select {" in response.text
    assert "min-height: 38px;" in response.text
    assert ".accounts-builder .button {" in response.text
    assert ".account-card__delete {" in response.text
    assert ".account-actions .button {" in response.text
    assert ".account-password-toggle {" in response.text


def test_cabinet_local_accounts_script_is_served(client):
    response = client.get("/static/cabinet-local-accounts.js")
    assert response.status_code == 200
    assert "openscript:cabinet:local-accounts:v1" in response.text
    assert "Редактировать" in response.text
    assert "Сохранить" in response.text
    assert "account-card--editing" in response.text
    assert "readOnly = !account.isEditing" in response.text
    assert "persisted: false" in response.text
    assert "isEditing: true" in response.text
    assert "Скопировать логин" in response.text
    assert "Скопировать пароль" in response.text
    assert "Показать пароль" in response.text
    assert "Скрыть пароль" in response.text
    assert "Удалить" in response.text
