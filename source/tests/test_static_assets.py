from __future__ import annotations

from pathlib import Path

def test_favicon_svg_is_served_and_matches_constraints(client):
    favicon_path = Path(__file__).resolve().parents[1] / "app" / "static" / "favicon.svg"
    svg_text = favicon_path.read_text(encoding="utf-8")

    response = client.get("/static/favicon.svg")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("image/svg+xml")
    assert favicon_path.exists()
    assert "<svg" in svg_text
    assert '<rect x="500" y="500" width="23000" height="23000" rx="4200" ry="4200" fill="#FEF8EC"/>' in svg_text
    assert svg_text.count("<rect") == 1
    assert 'transform="translate(12000 12000) scale(0.95) translate(-12000 -12000)"' in svg_text
    assert "scale(0.85)" not in svg_text
    assert "clipPath" not in svg_text
    assert "<image" not in svg_text
    assert "<text" not in svg_text
    assert "OS" not in svg_text
    assert "base64" not in svg_text.lower()
    assert "data:image" not in svg_text.lower()
    assert "blue" not in svg_text.lower()
    assert "#0000ff" not in svg_text.lower()
    assert "#00f" not in svg_text.lower()
    assert "cloud" not in svg_text.lower()
    assert "speech" not in svg_text.lower()


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
    assert ".accounts-title" in response.text
    assert ".accounts-builder-shell" in response.text
    assert ".accounts-grid" in response.text
    assert ".account-card" in response.text
    assert ".account-card__body" in response.text
    assert ".account-card__edit-form" in response.text
    assert ".account-actions--view" in response.text
    assert ".account-actions--edit" in response.text
    assert ".account-action-form" in response.text
    assert "grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));" in response.text
    assert "align-items: stretch;" in response.text
    assert "display: flex;" in response.text
    assert "flex-direction: column;" in response.text
    assert "height: 100%;" in response.text
    assert "margin-top: auto;" in response.text
    assert ".accounts-builder .select {" in response.text
    assert "min-height: 38px;" in response.text
    assert ".accounts-builder .button {" in response.text
    assert "grid-column: 1 / -1;" in response.text
    assert "min-width: 160px;" in response.text
    assert ".account-card__delete {" in response.text
    assert ".account-actions {" in response.text
    assert ".account-actions .button {" in response.text
    assert ".account-actions .button:disabled {" in response.text
    assert ".account-password-toggle {" in response.text
    assert ".prompts-library-card {" in response.text
    assert "--prompt-card-collapsed-height: 192px;" in response.text
    assert ".prompts-library-header {" in response.text
    assert ".prompts-grid {" in response.text
    assert ".prompt-card {" in response.text
    assert ".prompt-card__filename" in response.text
    assert ".prompt-card__header-actions" in response.text
    assert ".prompt-card__toggle" in response.text
    assert ".prompt-card__body" in response.text
    assert ".prompt-card--collapsed" in response.text
    assert "height: var(--prompt-card-collapsed-height);" in response.text
    assert "display: -webkit-box;" in response.text
    assert "-webkit-line-clamp: 2;" in response.text
    assert "text-overflow: ellipsis;" in response.text
    assert ".prompt-textarea {" in response.text
    assert ".prompt-actions {" in response.text
    assert ".prompt-card--custom," in response.text
    assert ".prompt-card--editing" in response.text
    assert "@media (max-width: 640px)" in response.text
    assert "--prompt-card-collapsed-height: 176px;" in response.text
    assert ".paid-options-card {" in response.text
    assert ".paid-options-header {" in response.text
    assert ".paid-options-count {" in response.text
    assert ".paid-options-grid {" in response.text
    assert ".paid-option-card {" in response.text
    assert "height: 100%;" in response.text
    assert ".paid-option__headline {" in response.text
    assert ".paid-option__intro {" in response.text
    assert ".paid-option__meta {" in response.text
    assert ".paid-option__buy {" in response.text
    assert ".paid-options-notice {" in response.text
    assert "margin-top: auto;" in response.text

    assert "font-size: clamp(1.2rem, 1.8vw, 1.55rem);" in response.text
    assert ".account-card__detail {" in response.text
    assert "Срок завершён" not in response.text
    assert "Осталось после активации" not in response.text

    template_path = Path(__file__).resolve().parents[1] / "app" / "user_cabinet" / "templates" / "cabinet.html"
    template_text = template_path.read_text(encoding="utf-8")
    assert 'name="title"' not in template_text
    assert 'name="email"' not in template_text
    assert 'name="owner_user_id"' not in template_text
    assert 'Владелец' not in template_text
    assert "Осталось после активации" not in template_text
    assert "data-account-card-edit-form" in template_text
    assert "account-owner-group__title" not in template_text
    assert "account-owner-group__meta" not in template_text
    assert "account-card__owner-line" not in template_text
    assert "Срок действия" not in template_text


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
    assert "editButton.disabled = editing;" in response.text
    assert "saveButton.disabled = !editing;" in response.text
    assert "actions.append(copyLoginButton, editButton, copyPasswordButton, saveButton);" in response.text
    assert "Скопировать логин" in response.text
    assert "Скопировать пароль" in response.text
    assert "Показать пароль" in response.text
    assert "Скрыть пароль" in response.text
    assert "Удалить" in response.text
    assert "account-edit-row" not in response.text
    assert "account-save-row" not in response.text


def test_cabinet_prompts_library_script_is_served(client):
    response = client.get("/static/cabinet-prompts-library.js")
    assert response.status_code == 200
    assert "openscript:cabinet:prompts-library:v1" in response.text
    assert "Промпт скопирован" in response.text
    assert "Промпт сохранён" in response.text
    assert "Версия курса восстановлена" in response.text
    assert "Промпт скачан" in response.text
    assert "Развернуть" in response.text
    assert "Свернуть" in response.text
    assert "data-prompt-edit" in response.text
    assert "data-prompt-save" in response.text
    assert "data-prompt-copy" in response.text
    assert "data-prompt-download" in response.text
    assert "data-prompt-reset" in response.text
    assert "data-prompt-delete" in response.text
    assert "data-prompt-toggle" in response.text
    assert "data-prompt-body" in response.text
    assert "prompt-card--collapsed" in response.text
    assert "prompt-card--expanded" in response.text
    assert "isExpanded: false" in response.text
    assert "prompt.isExpanded = true;" in response.text
    assert "data-prompts-custom-template" in response.text
    assert 'querySelector("[data-prompt-custom]")' in response.text
    assert "prompt-card--editing" in response.text
    assert "setPromptCardExpanded" in response.text
    assert 'toggleButton.addEventListener("click"' in response.text


def test_global_templates_link_to_favicon():
    public_landing = (Path(__file__).resolve().parents[1] / "app" / "public_landing/templates/index.html").read_text(encoding="utf-8")
    shared_base = (Path(__file__).resolve().parents[1] / "app" / "shared/templates/base.html").read_text(encoding="utf-8")
    admin_base = (Path(__file__).resolve().parents[1] / "app" / "admin/templates/base.html").read_text(encoding="utf-8")

    assert 'rel="icon" href="/static/favicon.svg" type="image/svg+xml"' in public_landing
    assert 'rel="shortcut icon" href="/static/favicon.svg" type="image/svg+xml"' in public_landing

    for template in (shared_base, admin_base):
        assert 'rel="icon" href="/static/favicon.svg" type="image/svg+xml"' in template
        assert 'rel="shortcut icon" href="/static/favicon.svg" type="image/svg+xml"' in template
