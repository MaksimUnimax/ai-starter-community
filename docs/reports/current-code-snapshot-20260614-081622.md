# CURRENT CODE SNAPSHOT REPORT

Generated UTC: 2026-06-14T08:16:22.698474+00:00

## 1. CURRENT_STATE_GATE

```text
pwd
/opt/ai-starter-community

git branch --show-current
fix/carousel-arrow-button-visuals

git rev-parse HEAD
f458d7d745d7aec42eb9a8d73e658174e5ca0d3f

git show -s --format='%H %s' HEAD
f458d7d745d7aec42eb9a8d73e658174e5ca0d3f Restore landing favicon and tariff binding

git rev-parse origin/design/product-story-03
f458d7d745d7aec42eb9a8d73e658174e5ca0d3f

git status --short --untracked-files=all
 M source/app/admin/routes.py
 M source/app/admin/templates/tariff_form.html
 M source/app/admin/templates/tariffs.html
 M source/app/admin/templates/users.html
 M source/app/auth/service.py
 M source/app/auth/templates/login.html
 M source/app/auth/templates/register.html
 M source/app/materials/routes.py
 M source/app/public_landing/routes.py
 M source/app/shared/db.py
 M source/app/shared/templates/base.html
 M source/app/tariffs/schemas.py
 M source/app/tariffs/service.py
 M source/tests/test_admin_tariff_crud_ui.py
 M source/tests/test_context_navigation.py
 M source/tests/test_landing_tariff_binding.py
 M source/tests/test_materials_flow.py
 M source/tests/test_routes.py
 M source/tests/test_static_assets.py
?? source/app/.backup_20260515_1013_center_hero/index.html
?? source/app/.backup_20260515_1013_center_hero/styles.css
?? source/app/.backup_20260515_1216_hero_v2_replace/MANIFEST.md
?? source/app/.backup_20260515_1216_hero_v2_replace/index.html
?? source/app/.backup_20260515_1216_hero_v2_replace/styles.css
?? source/app/.backup_20260516_0326_mobile_hero/index.html
?? source/app/.backup_20260516_0326_mobile_hero/styles.css
?? source/app/account_blocks/__init__.py
?? source/app/account_blocks/schemas.py
?? source/app/account_blocks/service.py
?? source/app/admin/templates/account_blocks.html
?? source/app/materials/course_content/drafts/dair_smoke_20260529/README.md
?? source/app/materials/course_content/drafts/dair_smoke_20260529/assets/git-carousel/github-step-01.png
?? source/app/materials/course_content/drafts/dair_smoke_20260529/assets/git-carousel/github-step-02.png
?? source/app/materials/course_content/drafts/dair_smoke_20260529/assets/git-carousel/github-step-03.png
?? source/app/materials/course_content/drafts/dair_smoke_20260529/assets/git-carousel/github-step-04.png
?? source/app/materials/course_content/drafts/dair_smoke_20260529/assets/git-carousel/github-step-05.png
?? source/app/materials/course_content/drafts/dair_smoke_20260529/assets/git-carousel/github-step-06.png
?? source/app/materials/templates/learning_locked.html
?? source/app/mp6mqk06-image.png
?? source/app/mp6ntlxh-human_ai_hero_background_transparent.png
?? source/app/mp6oibxq-7d089bfd-f89a-4f15-8e4d-2b943ba1649e.png
?? source/app/mp6rg4ub-hero_blueprint_NO_SQUARES_transparent.png
?? source/app/mp7ny41g-mobile_vitruvian_NO_SQUARES_transparent.webp
?? source/app/shared/tariff_display.py
?? source/app/shared/templates/tariff_pricing_section.html
?? source/app/static/auth-password-toggle.js
?? source/app/static/course-assets/dair-smoke-20260529/git-carousel/github-step-01.png
?? source/app/static/course-assets/dair-smoke-20260529/git-carousel/github-step-02.png
?? source/app/static/course-assets/dair-smoke-20260529/git-carousel/github-step-03.png
?? source/app/static/course-assets/dair-smoke-20260529/git-carousel/github-step-04.png
?? source/app/static/course-assets/dair-smoke-20260529/git-carousel/github-step-05.png
?? source/app/static/course-assets/dair-smoke-20260529/git-carousel/github-step-06.png
?? source/app/static/videos/amnezia-vpn-guide.mp4
?? source/app/user_cabinet/templates/access_locked.html
?? source/tests/test_account_blocks_activation.py
?? source/tests/test_account_blocks_admin_ui.py
?? source/tests/test_account_blocks_permissions.py
?? source/tests/test_account_blocks_service.py
?? source/tests/test_admin_paid_access_grant.py
?? source/tests/test_admin_user_roles.py
?? source/tests/test_auth_roles.py
?? source/tests/test_cabinet_paid_options.py
?? source/uv.lock

git diff --stat
 source/app/admin/routes.py                  | 49 ++++++++++++++++++--
 source/app/admin/templates/tariff_form.html |  9 ++++
 source/app/admin/templates/tariffs.html     |  4 +-
 source/app/admin/templates/users.html       | 26 ++++++-----
 source/app/auth/service.py                  | 33 ++++++++++++++
 source/app/auth/templates/login.html        |  7 ++-
 source/app/auth/templates/register.html     | 12 ++++-
 source/app/materials/routes.py              | 70 +++++++++++++++++++++++++++--
 source/app/public_landing/routes.py         | 30 ++++++++++---
 source/app/shared/db.py                     | 36 +++++++++++++++
 source/app/shared/templates/base.html       | 10 ++---
 source/app/tariffs/schemas.py               |  3 ++
 source/app/tariffs/service.py               | 39 +++++++++++++---
 source/tests/test_admin_tariff_crud_ui.py   |  8 ++++
 source/tests/test_context_navigation.py     |  3 ++
 source/tests/test_landing_tariff_binding.py | 43 ++++++++++++++----
 source/tests/test_materials_flow.py         | 51 ++++++++++-----------
 source/tests/test_routes.py                 | 10 ++---
 source/tests/test_static_assets.py          |  3 +-
 19 files changed, 364 insertions(+), 82 deletions(-)

git diff --check
(no output)

git diff --name-status
M	source/app/admin/routes.py
M	source/app/admin/templates/tariff_form.html
M	source/app/admin/templates/tariffs.html
M	source/app/admin/templates/users.html
M	source/app/auth/service.py
M	source/app/auth/templates/login.html
M	source/app/auth/templates/register.html
M	source/app/materials/routes.py
M	source/app/public_landing/routes.py
M	source/app/shared/db.py
M	source/app/shared/templates/base.html
M	source/app/tariffs/schemas.py
M	source/app/tariffs/service.py
M	source/tests/test_admin_tariff_crud_ui.py
M	source/tests/test_context_navigation.py
M	source/tests/test_landing_tariff_binding.py
M	source/tests/test_materials_flow.py
M	source/tests/test_routes.py
M	source/tests/test_static_assets.py

git ls-files --others --exclude-standard | sort
source/app/.backup_20260515_1013_center_hero/index.html
source/app/.backup_20260515_1013_center_hero/styles.css
source/app/.backup_20260515_1216_hero_v2_replace/MANIFEST.md
source/app/.backup_20260515_1216_hero_v2_replace/index.html
source/app/.backup_20260515_1216_hero_v2_replace/styles.css
source/app/.backup_20260516_0326_mobile_hero/index.html
source/app/.backup_20260516_0326_mobile_hero/styles.css
source/app/account_blocks/__init__.py
source/app/account_blocks/schemas.py
source/app/account_blocks/service.py
source/app/admin/templates/account_blocks.html
source/app/materials/course_content/drafts/dair_smoke_20260529/README.md
source/app/materials/course_content/drafts/dair_smoke_20260529/assets/git-carousel/github-step-01.png
source/app/materials/course_content/drafts/dair_smoke_20260529/assets/git-carousel/github-step-02.png
source/app/materials/course_content/drafts/dair_smoke_20260529/assets/git-carousel/github-step-03.png
source/app/materials/course_content/drafts/dair_smoke_20260529/assets/git-carousel/github-step-04.png
source/app/materials/course_content/drafts/dair_smoke_20260529/assets/git-carousel/github-step-05.png
source/app/materials/course_content/drafts/dair_smoke_20260529/assets/git-carousel/github-step-06.png
source/app/materials/templates/learning_locked.html
source/app/mp6mqk06-image.png
source/app/mp6ntlxh-human_ai_hero_background_transparent.png
source/app/mp6oibxq-7d089bfd-f89a-4f15-8e4d-2b943ba1649e.png
source/app/mp6rg4ub-hero_blueprint_NO_SQUARES_transparent.png
source/app/mp7ny41g-mobile_vitruvian_NO_SQUARES_transparent.webp
source/app/shared/tariff_display.py
source/app/shared/templates/tariff_pricing_section.html
source/app/static/auth-password-toggle.js
source/app/static/course-assets/dair-smoke-20260529/git-carousel/github-step-01.png
source/app/static/course-assets/dair-smoke-20260529/git-carousel/github-step-02.png
source/app/static/course-assets/dair-smoke-20260529/git-carousel/github-step-03.png
source/app/static/course-assets/dair-smoke-20260529/git-carousel/github-step-04.png
source/app/static/course-assets/dair-smoke-20260529/git-carousel/github-step-05.png
source/app/static/course-assets/dair-smoke-20260529/git-carousel/github-step-06.png
source/app/static/videos/amnezia-vpn-guide.mp4
source/app/user_cabinet/templates/access_locked.html
source/tests/test_account_blocks_activation.py
source/tests/test_account_blocks_admin_ui.py
source/tests/test_account_blocks_permissions.py
source/tests/test_account_blocks_service.py
source/tests/test_admin_paid_access_grant.py
source/tests/test_admin_user_roles.py
source/tests/test_auth_roles.py
source/tests/test_cabinet_paid_options.py
source/uv.lock
```


## 2. MODIFIED_AND_UNTRACKED_FILE_LIST

Tracked modified files:
- `source/app/admin/routes.py`
- `source/app/admin/templates/tariff_form.html`
- `source/app/admin/templates/tariffs.html`
- `source/app/admin/templates/users.html`
- `source/app/auth/service.py`
- `source/app/auth/templates/login.html`
- `source/app/auth/templates/register.html`
- `source/app/materials/routes.py`
- `source/app/public_landing/routes.py`
- `source/app/shared/db.py`
- `source/app/shared/templates/base.html`
- `source/app/tariffs/schemas.py`
- `source/app/tariffs/service.py`
- `source/tests/test_admin_tariff_crud_ui.py`
- `source/tests/test_context_navigation.py`
- `source/tests/test_landing_tariff_binding.py`
- `source/tests/test_materials_flow.py`
- `source/tests/test_routes.py`
- `source/tests/test_static_assets.py`

Untracked files:
- `source/app/.backup_20260515_1013_center_hero/index.html`
- `source/app/.backup_20260515_1013_center_hero/styles.css`
- `source/app/.backup_20260515_1216_hero_v2_replace/MANIFEST.md`
- `source/app/.backup_20260515_1216_hero_v2_replace/index.html`
- `source/app/.backup_20260515_1216_hero_v2_replace/styles.css`
- `source/app/.backup_20260516_0326_mobile_hero/index.html`
- `source/app/.backup_20260516_0326_mobile_hero/styles.css`
- `source/app/account_blocks/__init__.py`
- `source/app/account_blocks/schemas.py`
- `source/app/account_blocks/service.py`
- `source/app/admin/templates/account_blocks.html`
- `source/app/materials/course_content/drafts/dair_smoke_20260529/README.md`
- `source/app/materials/course_content/drafts/dair_smoke_20260529/assets/git-carousel/github-step-01.png`
- `source/app/materials/course_content/drafts/dair_smoke_20260529/assets/git-carousel/github-step-02.png`
- `source/app/materials/course_content/drafts/dair_smoke_20260529/assets/git-carousel/github-step-03.png`
- `source/app/materials/course_content/drafts/dair_smoke_20260529/assets/git-carousel/github-step-04.png`
- `source/app/materials/course_content/drafts/dair_smoke_20260529/assets/git-carousel/github-step-05.png`
- `source/app/materials/course_content/drafts/dair_smoke_20260529/assets/git-carousel/github-step-06.png`
- `source/app/materials/templates/learning_locked.html`
- `source/app/mp6mqk06-image.png`
- `source/app/mp6ntlxh-human_ai_hero_background_transparent.png`
- `source/app/mp6oibxq-7d089bfd-f89a-4f15-8e4d-2b943ba1649e.png`
- `source/app/mp6rg4ub-hero_blueprint_NO_SQUARES_transparent.png`
- `source/app/mp7ny41g-mobile_vitruvian_NO_SQUARES_transparent.webp`
- `source/app/shared/tariff_display.py`
- `source/app/shared/templates/tariff_pricing_section.html`
- `source/app/static/auth-password-toggle.js`
- `source/app/static/course-assets/dair-smoke-20260529/git-carousel/github-step-01.png`
- `source/app/static/course-assets/dair-smoke-20260529/git-carousel/github-step-02.png`
- `source/app/static/course-assets/dair-smoke-20260529/git-carousel/github-step-03.png`
- `source/app/static/course-assets/dair-smoke-20260529/git-carousel/github-step-04.png`
- `source/app/static/course-assets/dair-smoke-20260529/git-carousel/github-step-05.png`
- `source/app/static/course-assets/dair-smoke-20260529/git-carousel/github-step-06.png`
- `source/app/static/videos/amnezia-vpn-guide.mp4`
- `source/app/user_cabinet/templates/access_locked.html`
- `source/tests/test_account_blocks_activation.py`
- `source/tests/test_account_blocks_admin_ui.py`
- `source/tests/test_account_blocks_permissions.py`
- `source/tests/test_account_blocks_service.py`
- `source/tests/test_admin_paid_access_grant.py`
- `source/tests/test_admin_user_roles.py`
- `source/tests/test_auth_roles.py`
- `source/tests/test_cabinet_paid_options.py`
- `source/uv.lock`

Files referenced by tracked code:
```text
source/tests/test_cabinet_prompts_library.py:9:from app.user_cabinet.prompts_library import load_cabinet_prompts
source/tests/test_cabinet_prompts_library.py:78:    assert "openscript:cabinet:prompts-library:v1" in client.get("/static/cabinet-prompts-library.js").text
source/tests/test_auth_flow.py:659:    assert 'auth-password-toggle.js' in login_response.text
source/tests/test_auth_flow.py:678:    assert 'auth-password-toggle.js' in body
source/tests/test_account_blocks_service.py:8:from app.account_blocks.schemas import AccountBlockCreateInput, AccountBlockUpdateInput
source/tests/test_account_blocks_service.py:9:from app.account_blocks.service import (
source/tests/test_account_blocks_service.py:17:    list_account_blocks_for_viewer,
source/tests/test_account_blocks_service.py:59:def test_account_blocks_table_and_supported_types_exist(test_settings):
source/tests/test_account_blocks_service.py:66:        assert "account_blocks" in tables
source/tests/test_account_blocks_service.py:69:            for row in conn.execute("PRAGMA table_info(account_blocks)").fetchall()
source/tests/test_account_blocks_service.py:151:    all_blocks = list_account_blocks_for_viewer(admin, settings=test_settings)
source/tests/test_account_blocks_service.py:154:    owner_blocks = list_account_blocks_for_viewer(owner, settings=test_settings)
source/tests/test_account_blocks_service.py:166:        deleted = conn.execute("SELECT 1 FROM account_blocks WHERE id = ?", (moderator_block.id,)).fetchone()
source/tests/test_account_blocks_service.py:197:    own_blocks = list_account_blocks_for_viewer(owner, settings=test_settings)
source/tests/test_account_blocks_activation.py:10:from app.account_blocks.schemas import AccountBlockCreateInput
source/tests/test_account_blocks_activation.py:11:from app.account_blocks.service import (
source/tests/test_account_blocks_activation.py:73:    with patch("app.account_blocks.service.utc_now", return_value=fixed_now):
source/tests/test_account_blocks_activation.py:123:    with patch("app.account_blocks.service.utc_now", return_value=activation_now):
source/tests/test_account_blocks_activation.py:126:    with patch("app.account_blocks.service.utc_now", return_value=day_17_now):
source/tests/test_account_blocks_activation.py:134:    with patch("app.account_blocks.service.utc_now", return_value=day_60_now):
source/tests/test_account_blocks_activation.py:142:    with patch("app.account_blocks.service.utc_now", return_value=expired_now):
source/tests/test_account_blocks_activation.py:151:    with patch("app.account_blocks.service.utc_now", return_value=expired_now):
source/tests/test_account_blocks_activation.py:159:def test_user_cannot_activate_account_blocks(test_settings):
source/tests/test_account_blocks_activation.py:194:    with patch("app.account_blocks.service.utc_now", return_value=activation_now):
source/tests/test_account_blocks_activation.py:197:    with patch("app.account_blocks.service.utc_now", return_value=renewal_now):
source/tests/test_account_blocks_activation.py:216:    with patch("app.account_blocks.service.utc_now", return_value=renewal_now):
source/app/user_cabinet/templates/cabinet.html:31:  {% set vpn_account_blocks = account_block_blocks | selectattr('type', 'equalto', 'vpn') | list %}
source/app/user_cabinet/templates/cabinet.html:32:  {% set regular_account_blocks = account_block_blocks | rejectattr('type', 'equalto', 'vpn') | list %}
source/app/user_cabinet/templates/cabinet.html:40:      {% if account_blocks_manage_mode %}
source/app/user_cabinet/templates/cabinet.html:46:              name="account_blocks_user_email"
source/app/user_cabinet/templates/cabinet.html:69:    {% if account_blocks_manage_mode and account_block_selected_user_summary %}
source/app/user_cabinet/templates/cabinet.html:78:    {% if account_blocks_manage_mode %}
source/app/user_cabinet/templates/cabinet.html:111:    {% if regular_account_blocks %}
source/app/user_cabinet/templates/cabinet.html:113:        {% for block in regular_account_blocks %}
source/app/user_cabinet/templates/cabinet.html:127:                {% if account_blocks_manage_mode %}
source/app/user_cabinet/templates/cabinet.html:161:                {% if account_blocks_manage_mode %}
source/app/user_cabinet/templates/cabinet.html:187:              {% if account_blocks_manage_mode %}
source/app/user_cabinet/templates/cabinet.html:219:      {% if not account_blocks_manage_mode or account_block_selected_user_summary %}
source/app/user_cabinet/templates/cabinet.html:225:  {% for block in vpn_account_blocks %}
source/app/user_cabinet/templates/cabinet.html:253:          {% if account_blocks_manage_mode %}
source/app/user_cabinet/templates/cabinet.html:670:  <script src="/static/cabinet-prompts-library.js"></script>
source/tests/test_account_blocks_cabinet_ui.py:9:from app.account_blocks.schemas import AccountBlockCreateInput
source/tests/test_account_blocks_cabinet_ui.py:10:from app.account_blocks.service import activate_account_block, create_account_block
source/tests/test_account_blocks_cabinet_ui.py:105:def test_user_sees_compact_server_backed_account_blocks_and_copy_only_controls(client, test_settings):
source/tests/test_account_blocks_cabinet_ui.py:140:    with patch("app.account_blocks.service.utc_now", return_value=fixed_now):
source/tests/test_account_blocks_cabinet_ui.py:142:    with patch("app.account_blocks.service.utc_now", return_value=fixed_now):
source/tests/test_account_blocks_cabinet_ui.py:146:    with patch("app.account_blocks.service.utc_now", return_value=fixed_now):
source/tests/test_account_blocks_cabinet_ui.py:254:        with patch("app.account_blocks.service.utc_now", return_value=fixed_now):
source/tests/test_account_blocks_cabinet_ui.py:258:    with patch("app.account_blocks.service.utc_now", return_value=fixed_now):
source/tests/test_account_blocks_cabinet_ui.py:279:def test_user_with_no_active_account_blocks_sees_new_empty_state(client, test_settings):
source/tests/test_account_blocks_cabinet_ui.py:321:    cabinet_response = client.get(f"/cabinet?account_blocks_user_email={owner_a.email}")
source/tests/test_account_blocks_cabinet_ui.py:335:    assert f'action="/cabinet/account-blocks?{urlencode({"account_blocks_user_email": owner_a.email})}' in builder_shell
source/tests/test_account_blocks_cabinet_ui.py:346:        f"/cabinet/account-blocks?{urlencode({'account_blocks_user_email': owner_a.email})}",
source/tests/test_account_blocks_cabinet_ui.py:356:    assert create_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'created', 'account_blocks_user_email': owner_a.email})}"
source/tests/test_account_blocks_cabinet_ui.py:359:        row = conn.execute("SELECT * FROM account_blocks WHERE login = ?", ("mod-block-login",)).fetchone()
source/tests/test_account_blocks_cabinet_ui.py:380:    assert update_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'updated', 'account_blocks_user_email': owner_a.email})}"
source/tests/test_account_blocks_cabinet_ui.py:391:    with patch("app.account_blocks.service.utc_now", return_value=activation_now):
source/tests/test_account_blocks_cabinet_ui.py:393:            f"/cabinet/account-blocks/{block_id}/activate?{urlencode({'account_blocks_user_email': owner_a.email})}",
source/tests/test_account_blocks_cabinet_ui.py:400:    assert activate_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'activated_email_sent', 'account_blocks_user_email': owner_a.email})}"
source/tests/test_account_blocks_cabinet_ui.py:403:        updated_row = conn.execute("SELECT * FROM account_blocks WHERE id = ?", (block_id,)).fetchone()
source/tests/test_account_blocks_cabinet_ui.py:432:    with patch("app.account_blocks.service.utc_now", return_value=renewal_now):
source/tests/test_account_blocks_cabinet_ui.py:433:        active_page = client.get(f"/cabinet?{urlencode({'account_blocks_user_email': owner_a.email})}")
source/tests/test_account_blocks_cabinet_ui.py:443:    assert f'/cabinet/account-blocks/{block_id}/delete?{urlencode({"account_blocks_user_email": owner_a.email})}' in accounts_section
source/tests/test_account_blocks_cabinet_ui.py:444:    assert f'/cabinet/account-blocks/{block_id}/activate?{urlencode({"account_blocks_user_email": owner_a.email})}' in accounts_section
source/tests/test_account_blocks_cabinet_ui.py:445:    assert f'/cabinet/account-blocks/{block_id}/renew?{urlencode({"account_blocks_user_email": owner_a.email})}' in accounts_section
source/tests/test_account_blocks_cabinet_ui.py:455:    with patch("app.account_blocks.service.utc_now", return_value=renewal_now):
source/tests/test_account_blocks_cabinet_ui.py:457:            f"/cabinet/account-blocks/{block_id}/renew?{urlencode({'account_blocks_user_email': owner_a.email})}",
source/tests/test_account_blocks_cabinet_ui.py:464:    assert renew_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'renewed', 'account_blocks_user_email': owner_a.email})}"
source/tests/test_account_blocks_cabinet_ui.py:467:        renewed_row = conn.execute("SELECT * FROM account_blocks WHERE id = ?", (block_id,)).fetchone()
source/tests/test_account_blocks_cabinet_ui.py:472:        f"/cabinet/account-blocks/{block_id}/delete?{urlencode({'account_blocks_user_email': owner_a.email})}",
source/tests/test_account_blocks_cabinet_ui.py:476:    assert delete_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'deleted', 'account_blocks_user_email': owner_a.email})}"
source/tests/test_account_blocks_cabinet_ui.py:479:        deleted_row = conn.execute("SELECT 1 FROM account_blocks WHERE id = ?", (block_id,)).fetchone()
source/tests/test_account_blocks_cabinet_ui.py:501:def test_moderator_can_manage_account_blocks_but_cannot_access_admin_dashboard(client, test_settings):
source/tests/test_account_blocks_cabinet_ui.py:508:    admin_blocks_response = client.get("/admin/account-blocks?account_blocks_user_email=test@example.com")
source/tests/test_account_blocks_cabinet_ui.py:512:        f"/cabinet/account-blocks?{urlencode({'account_blocks_user_email': owner.email})}",
source/tests/test_account_blocks_cabinet_ui.py:521:    assert create_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'created', 'account_blocks_user_email': owner.email})}"
source/tests/test_account_blocks_cabinet_ui.py:524:        row = conn.execute("SELECT * FROM account_blocks WHERE login = ?", ("moderator-login",)).fetchone()
source/tests/test_account_blocks_cabinet_ui.py:540:    assert update_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'updated', 'account_blocks_user_email': owner.email})}"
source/tests/test_account_blocks_cabinet_ui.py:543:    with patch("app.account_blocks.service.utc_now", return_value=activation_now):
source/tests/test_account_blocks_cabinet_ui.py:545:            f"/cabinet/account-blocks/{block_id}/activate?{urlencode({'account_blocks_user_email': owner.email})}",
source/tests/test_account_blocks_cabinet_ui.py:550:    assert activate_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'activated_email_sent', 'account_blocks_user_email': owner.email})}"
source/tests/test_account_blocks_cabinet_ui.py:553:        activated_row = conn.execute("SELECT * FROM account_blocks WHERE id = ?", (block_id,)).fetchone()
source/tests/test_account_blocks_cabinet_ui.py:557:    with patch("app.account_blocks.service.utc_now", return_value=activation_now + timedelta(days=1)):
source/tests/test_account_blocks_cabinet_ui.py:558:        active_page = client.get(f"/cabinet?{urlencode({'account_blocks_user_email': owner.email})}")
source/tests/test_account_blocks_cabinet_ui.py:564:        f"/cabinet/account-blocks/{block_id}/renew?{urlencode({'account_blocks_user_email': owner.email})}",
source/tests/test_account_blocks_cabinet_ui.py:569:    assert renew_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'renewed', 'account_blocks_user_email': owner.email})}"
source/tests/test_account_blocks_cabinet_ui.py:572:        f"/cabinet/account-blocks/{block_id}/delete?{urlencode({'account_blocks_user_email': owner.email})}",
source/tests/test_account_blocks_cabinet_ui.py:576:    assert delete_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'deleted', 'account_blocks_user_email': owner.email})}"
source/tests/test_account_blocks_cabinet_ui.py:643:    with patch("app.account_blocks.service.utc_now", return_value=activation_now):
source/tests/test_account_blocks_cabinet_ui.py:647:    with patch("app.account_blocks.service.utc_now", return_value=expired_now):
source/app/user_cabinet/routes.py:15:    can_manage_account_blocks,
source/app/user_cabinet/routes.py:25:from app.account_blocks.schemas import AccountBlockCreateInput, AccountBlockUpdateInput
source/app/user_cabinet/routes.py:26:from app.account_blocks.service import (
source/app/user_cabinet/routes.py:35:    list_account_blocks_for_viewer,
source/app/user_cabinet/routes.py:41:from app.shared.tariff_display import get_homepage_tariff_context
source/app/user_cabinet/routes.py:44:from app.user_cabinet.prompts_library import load_cabinet_prompts
source/app/user_cabinet/routes.py:138:    notice_key = (request.query_params.get("account_blocks_notice") or "").strip().lower()
source/app/user_cabinet/routes.py:143:    raw_email = (request.query_params.get("account_blocks_user_email") or "").strip()
source/app/user_cabinet/routes.py:178:    manage_mode = can_manage_account_blocks(user)
source/app/user_cabinet/routes.py:198:    manage_mode = can_manage_account_blocks(user)
source/app/user_cabinet/routes.py:203:        visible_blocks = list_account_blocks_for_viewer(user, owner_user_id=int(selected_user.id), settings=settings)
source/app/user_cabinet/routes.py:216:        "account_blocks_manage_mode": manage_mode,
source/app/user_cabinet/routes.py:217:        "account_block_query_string": f"?{urlencode({'account_blocks_user_email': selected_email})}" if manage_mode else "",
source/app/user_cabinet/routes.py:240:    query = {"account_blocks_notice": notice_key}
source/app/user_cabinet/routes.py:242:        query["account_blocks_user_email"] = selected_user_email
source/app/user_cabinet/routes.py:389:        "access_locked.html",
source/app/user_cabinet/routes.py:556:    if not can_manage_account_blocks(user):
source/app/user_cabinet/routes.py:590:    if not can_manage_account_blocks(user):
source/app/user_cabinet/routes.py:623:    if not can_manage_account_blocks(user):
source/app/user_cabinet/routes.py:650:    if not can_manage_account_blocks(user):
source/app/user_cabinet/routes.py:703:    if not can_manage_account_blocks(user):
source/app/account_blocks/service.py:11:from app.auth.service import can_manage_account_blocks
source/app/account_blocks/service.py:214:    if actor is None or not can_manage_account_blocks(actor):
source/app/account_blocks/service.py:221:    if can_manage_account_blocks(actor):
source/app/account_blocks/service.py:301:        return connection.execute("SELECT * FROM account_blocks WHERE id = ?", (int(block_id),)).fetchone()
source/app/account_blocks/service.py:313:def list_account_blocks_for_viewer(
source/app/account_blocks/service.py:320:        if can_manage_account_blocks(viewer):
source/app/account_blocks/service.py:325:                    FROM account_blocks
source/app/account_blocks/service.py:333:                    FROM account_blocks
source/app/account_blocks/service.py:346:                FROM account_blocks
source/app/account_blocks/service.py:407:            INSERT INTO account_blocks (
source/app/account_blocks/service.py:431:        row = connection.execute("SELECT * FROM account_blocks WHERE id = ?", (block_id,)).fetchone()
source/app/account_blocks/service.py:447:        row = connection.execute("SELECT * FROM account_blocks WHERE id = ?", (int(block_id),)).fetchone()
source/app/account_blocks/service.py:464:            f"UPDATE account_blocks SET {', '.join(updates)} WHERE id = ?",
source/app/account_blocks/service.py:467:        updated = connection.execute("SELECT * FROM account_blocks WHERE id = ?", (int(block_id),)).fetchone()
source/app/account_blocks/service.py:481:        row = connection.execute("SELECT * FROM account_blocks WHERE id = ?", (int(block_id),)).fetchone()
source/app/account_blocks/service.py:484:        connection.execute("DELETE FROM account_blocks WHERE id = ?", (int(block_id),))
source/app/account_blocks/service.py:534:        row = connection.execute("SELECT * FROM account_blocks WHERE id = ?", (int(block_id),)).fetchone()
source/app/account_blocks/service.py:544:            UPDATE account_blocks
source/app/account_blocks/service.py:565:        updated = connection.execute("SELECT * FROM account_blocks WHERE id = ?", (int(block_id),)).fetchone()
source/app/account_blocks/service.py:585:        row = connection.execute("SELECT * FROM account_blocks WHERE id = ?", (int(block_id),)).fetchone()
source/app/account_blocks/service.py:601:            UPDATE account_blocks
source/app/account_blocks/service.py:616:        updated = connection.execute("SELECT * FROM account_blocks WHERE id = ?", (int(block_id),)).fetchone()
source/app/account_blocks/__init__.py:22:    list_account_blocks_for_viewer,
source/app/shared/db.py:60:CREATE TABLE IF NOT EXISTS account_blocks (
source/app/shared/db.py:81:CREATE INDEX IF NOT EXISTS idx_account_blocks_owner_user_id ON account_blocks(owner_user_id);
source/app/shared/db.py:82:CREATE INDEX IF NOT EXISTS idx_account_blocks_owner_user_type ON account_blocks(owner_user_id, type);
source/app/shared/db.py:83:CREATE INDEX IF NOT EXISTS idx_account_blocks_status ON account_blocks(status);
source/tests/test_account_blocks_admin_ui.py:9:from app.account_blocks.schemas import AccountBlockCreateInput
source/tests/test_account_blocks_admin_ui.py:10:from app.account_blocks.service import create_account_block
source/tests/test_account_blocks_admin_ui.py:87:    response = client.get(f"/admin/account-blocks?{urlencode({'account_blocks_user_email': owner.email})}")
source/tests/test_account_blocks_admin_ui.py:95:    assert 'name="account_blocks_user_email"' in body
source/tests/test_account_blocks_admin_ui.py:99:    assert f'action="/admin/account-blocks?{urlencode({"account_blocks_user_email": owner.email})}' in body
source/tests/test_account_blocks_admin_ui.py:105:        f"/admin/account-blocks?{urlencode({'account_blocks_user_email': owner.email})}",
source/tests/test_account_blocks_admin_ui.py:116:    assert create_response.headers["location"] == f"/admin/account-blocks?{urlencode({'account_blocks_notice': 'created', 'account_blocks_user_email': owner.email})}"
source/tests/test_account_blocks_admin_ui.py:119:        row = conn.execute("SELECT * FROM account_blocks WHERE login = ?", ("admin-ui-login",)).fetchone()
source/tests/test_account_blocks_admin_ui.py:127:    with patch("app.account_blocks.service.utc_now", return_value=activation_now):
source/tests/test_account_blocks_admin_ui.py:129:            f"/admin/account-blocks/{block_id}/activate?{urlencode({'account_blocks_user_email': owner.email})}",
source/tests/test_account_blocks_admin_ui.py:134:    assert activate_response.headers["location"] == f"/admin/account-blocks?{urlencode({'account_blocks_notice': 'activated_email_sent', 'account_blocks_user_email': owner.email})}"
source/tests/test_account_blocks_admin_ui.py:137:        activated_row = conn.execute("SELECT * FROM account_blocks WHERE id = ?", (block_id,)).fetchone()
source/tests/test_account_blocks_admin_ui.py:157:    with patch("app.account_blocks.service.utc_now", return_value=activation_now):
source/tests/test_account_blocks_admin_ui.py:158:        active_page = client.get(f"/admin/account-blocks?{urlencode({'account_blocks_user_email': owner.email})}")
source/tests/test_account_blocks_admin_ui.py:165:    with patch("app.account_blocks.service.utc_now", return_value=renewal_now):
source/tests/test_account_blocks_admin_ui.py:167:            f"/admin/account-blocks/{block_id}/renew?{urlencode({'account_blocks_user_email': owner.email})}",
source/tests/test_account_blocks_admin_ui.py:172:    assert renew_response.headers["location"] == f"/admin/account-blocks?{urlencode({'account_blocks_notice': 'renewed', 'account_blocks_user_email': owner.email})}"
source/tests/test_account_blocks_admin_ui.py:175:        renewed_row = conn.execute("SELECT * FROM account_blocks WHERE id = ?", (block_id,)).fetchone()
source/tests/test_account_blocks_admin_ui.py:179:    with patch("app.account_blocks.service.utc_now", return_value=renewal_now):
source/tests/test_account_blocks_admin_ui.py:180:        renewed_page = client.get(f"/admin/account-blocks?{urlencode({'account_blocks_user_email': owner.email})}")
source/tests/test_account_blocks_permissions.py:4:from app.auth.service import can_manage_account_blocks, is_admin_role
source/tests/test_account_blocks_permissions.py:11:    assert can_manage_account_blocks("admin")
source/tests/test_account_blocks_permissions.py:12:    assert can_manage_account_blocks("moderator")
source/tests/test_account_blocks_permissions.py:13:    assert not can_manage_account_blocks("user")
source/tests/test_account_blocks_permissions.py:14:    assert not can_manage_account_blocks(None)
source/tests/test_account_blocks_permissions.py:49:    assert can_manage_account_blocks(admin)
source/tests/test_account_blocks_permissions.py:50:    assert can_manage_account_blocks(moderator)
source/tests/test_account_blocks_permissions.py:51:    assert not can_manage_account_blocks(user)
source/tests/test_account_blocks_permissions.py:55:    assert can_manage_account_blocks("ADMIN")
source/tests/test_account_blocks_permissions.py:56:    assert can_manage_account_blocks(" moderator ")
source/tests/test_account_blocks_permissions.py:57:    assert not can_manage_account_blocks("guest")
source/app/admin/templates/account_blocks.html:26:            name="account_blocks_user_email"
source/app/admin/templates/account_blocks.html:355:  <script src="/static/cabinet-prompts-library.js"></script>
source/app/notifications/email_service.py:19:    from app.account_blocks.schemas import AccountBlockActivationNotification
source/app/materials/templates/learning_locked.html:60:    {% include "tariff_pricing_section.html" %}
source/app/materials/routes.py:79:        "access_locked.html",
source/app/auth/service.py:176:def can_manage_account_blocks(user: UserPublic | None) -> bool:
source/app/auth/templates/login.html:46:  <script src="/static/auth-password-toggle.js" defer></script>
source/app/auth/templates/register.html:64:  <script src="/static/auth-password-toggle.js" defer></script>
source/tests/test_static_assets.py:101:def test_cabinet_prompts_library_script_is_served(client):
source/tests/test_static_assets.py:102:    response = client.get("/static/cabinet-prompts-library.js")
```


| path | tracked yes/no | untracked exists yes/no | referenced by tracked code yes/no | clean checkout risk yes/no |
|---|---|---|---|---|
| `source/app/static/auth-password-toggle.js` | no | yes | yes | yes |
| `source/app/shared/tariff_display.py` | no | yes | yes | yes |
| `source/app/shared/templates/tariff_pricing_section.html` | no | yes | no | yes |
| `source/app/materials/templates/learning_locked.html` | no | yes | no | no |
| `source/app/user_cabinet/templates/access_locked.html` | no | yes | yes | yes |
| `source/app/user_cabinet/prompts_library.py` | yes | yes | yes | no |
| `source/app/static/cabinet-prompts-library.js` | yes | yes | yes | no |
| `source/app/account_blocks/__init__.py` | no | yes | yes | yes |
| `source/app/account_blocks/schemas.py` | no | yes | yes | yes |
| `source/app/account_blocks/service.py` | no | yes | yes | yes |
| `source/app/admin/templates/account_blocks.html` | no | yes | no | yes |


## 3. AUTH_FORM_CURRENT_CODE

### source/app/auth/templates/login.html

- tracking state: tracked

```html
{% extends "base.html" %}

{% block content %}
  <section class="card stack">
    <div class="stack">
      <p class="muted">Вход в аккаунт</p>
      <h1 class="section-title">Вход в аккаунт</h1>
      <p>Войдите по электронной почте или логину.</p>
    </div>

    {% if notice %}
      <div class="alert alert-info">{{ notice }}</div>
    {% endif %}
    {% if error %}
      <div class="alert alert-error">{{ error }}</div>
    {% endif %}
    {% if unverified %}
      <div class="alert alert-info stack login-unverified">
        <p class="login-unverified__title">Email не подтверждён.</p>
        <p class="login-unverified__text">Не пришло письмо подтверждения?</p>
        <a class="button button-secondary login-unverified__action" href="/resend-verification">Отправить письмо подтверждения ещё раз</a>
      </div>
    {% endif %}

    <form class="form" method="post" action="/login">
      <label class="form-row">
        <span>Электронная почта или логин</span>
        <input class="input" type="text" name="email_or_login" value="{{ email_or_login or '' }}" autocomplete="username">
      </label>
      <label class="form-row">
        <span>Пароль</span>
        <div class="password-field" data-password-field>
          <input class="input" type="password" name="password" autocomplete="current-password" data-password-input>
          <button class="button button-secondary password-toggle" type="button" data-password-toggle aria-pressed="false" aria-label="Показать пароль">Показать пароль</button>
        </div>
      </label>
      <button class="button button-primary" type="submit">Войти</button>
    </form>

    <div class="actions">
      <p>Нет аккаунта? <a href="/register">Зарегистрироваться</a></p>
      <a class="button button-secondary" href="/forgot-password">Забыли пароль?</a>
    </div>
  </section>

  <script src="/static/auth-password-toggle.js" defer></script>
{% endblock %}
```

```diff
diff --git a/source/app/auth/templates/login.html b/source/app/auth/templates/login.html
index 6bd0797..c727784 100644
--- a/source/app/auth/templates/login.html
+++ b/source/app/auth/templates/login.html
@@ -29,7 +29,10 @@
       </label>
       <label class="form-row">
         <span>Пароль</span>
-        <input class="input" type="password" name="password" autocomplete="current-password">
+        <div class="password-field" data-password-field>
+          <input class="input" type="password" name="password" autocomplete="current-password" data-password-input>
+          <button class="button button-secondary password-toggle" type="button" data-password-toggle aria-pressed="false" aria-label="Показать пароль">Показать пароль</button>
+        </div>
       </label>
       <button class="button button-primary" type="submit">Войти</button>
     </form>
@@ -39,4 +42,6 @@
       <a class="button button-secondary" href="/forgot-password">Забыли пароль?</a>
     </div>
   </section>
+
+  <script src="/static/auth-password-toggle.js" defer></script>
 {% endblock %}
```


### source/app/auth/templates/register.html

- tracking state: tracked

```html
{% extends "base.html" %}

{% block content %}
  <section class="card stack">
    <div class="stack">
      <p class="muted">Создание аккаунта</p>
      <h1 class="section-title">Регистрация</h1>
      {% if registration_closed %}
        <div class="alert alert-info">
          <p>{{ notice }}</p>
        </div>
        <div class="actions">
          <a class="button button-primary" href="/login">Перейти ко входу</a>
        </div>
      {% else %}
        <p>Создайте аккаунт, затем подтвердите почту по ссылке из письма.</p>
        <p>После регистрации вы увидите страницу подтверждения почты.</p>
      {% endif %}
    </div>

    {% if not registration_closed %}
      {% if notice %}
        <div class="alert alert-info">{{ notice }}</div>
      {% endif %}
      {% if error %}
        <div class="alert alert-error">{{ error }}</div>
      {% endif %}
    {% endif %}

    {% if not registration_closed %}
      <form class="form" method="post" action="/register">
        <label class="form-row">
          <span>Электронная почта</span>
          <input class="input" type="email" name="email" value="{{ email or '' }}" autocomplete="email">
        </label>
        <label class="form-row">
          <span>Логин</span>
          <input class="input" type="text" name="login" value="{{ login or '' }}" autocomplete="username">
        </label>
        <label class="form-row">
          <span>Пароль</span>
          <div class="password-field" data-password-field>
            <input class="input" type="password" name="password" autocomplete="new-password" data-password-input>
            <button class="button button-secondary password-toggle" type="button" data-password-toggle aria-pressed="false" aria-label="Показать пароль">Показать пароль</button>
          </div>
        </label>
        <label class="form-row">
          <span>Повтор пароля</span>
          <div class="password-field" data-password-field>
            <input class="input" type="password" name="repeat_password" autocomplete="new-password" data-password-input>
            <button class="button button-secondary password-toggle" type="button" data-password-toggle aria-pressed="false" aria-label="Показать пароль">Показать пароль</button>
          </div>
        </label>
        <button class="button button-primary" type="submit">Создать аккаунт</button>
      </form>
    {% endif %}

    <div class="stack">
      <p>Уже есть аккаунт?</p>
      <a class="button button-secondary" href="/login">Войти</a>
    </div>
  </section>

  <script src="/static/auth-password-toggle.js" defer></script>
{% endblock %}
```

```diff
diff --git a/source/app/auth/templates/register.html b/source/app/auth/templates/register.html
index fff4e07..15cd91c 100644
--- a/source/app/auth/templates/register.html
+++ b/source/app/auth/templates/register.html
@@ -39,11 +39,17 @@
         </label>
         <label class="form-row">
           <span>Пароль</span>
-          <input class="input" type="password" name="password" autocomplete="new-password">
+          <div class="password-field" data-password-field>
+            <input class="input" type="password" name="password" autocomplete="new-password" data-password-input>
+            <button class="button button-secondary password-toggle" type="button" data-password-toggle aria-pressed="false" aria-label="Показать пароль">Показать пароль</button>
+          </div>
         </label>
         <label class="form-row">
           <span>Повтор пароля</span>
-          <input class="input" type="password" name="repeat_password" autocomplete="new-password">
+          <div class="password-field" data-password-field>
+            <input class="input" type="password" name="repeat_password" autocomplete="new-password" data-password-input>
+            <button class="button button-secondary password-toggle" type="button" data-password-toggle aria-pressed="false" aria-label="Показать пароль">Показать пароль</button>
+          </div>
         </label>
         <button class="button button-primary" type="submit">Создать аккаунт</button>
       </form>
@@ -54,4 +60,6 @@
       <a class="button button-secondary" href="/login">Войти</a>
     </div>
   </section>
+
+  <script src="/static/auth-password-toggle.js" defer></script>
 {% endblock %}
```


### source/app/auth/templates/reset_password.html

- tracking state: tracked

```html
{% extends "base.html" %}

{% block content %}
  <section class="card stack">
    <div class="stack">
      <p class="muted">Восстановление доступа</p>
      <h1 class="section-title">Новый пароль</h1>
    </div>

    {% if success %}
      <div class="alert alert-info">{{ notice or "Пароль изменён." }}</div>
      <div class="actions">
        <a class="button button-primary" href="/login">Войти</a>
      </div>
    {% else %}
      <p>Введите новый пароль.</p>
      <p class="form-help">Правила: минимум 8 символов, без пробелов внутри. Пробелы по краям будут убраны.</p>
      {% if notice %}
        <div class="alert alert-info">{{ notice }}</div>
      {% endif %}
      {% if error %}
        <div class="alert alert-error">{{ error }}</div>
      {% endif %}
      <form class="form" method="post" action="/reset-password">
        <input type="hidden" name="token" value="{{ token }}">
        <label class="form-row">
          <span>Новый пароль</span>
          <input class="input" type="password" name="password" autocomplete="new-password">
        </label>
        <label class="form-row">
          <span>Повтор пароля</span>
          <input class="input" type="password" name="repeat_password" autocomplete="new-password">
        </label>
        <button class="button button-primary" type="submit">Сменить пароль</button>
      </form>
      <div class="actions">
        <a class="button button-secondary" href="/login">Вернуться ко входу</a>
      </div>
    {% endif %}
  </section>
{% endblock %}
```

```diff
(no diff)
```


### source/app/auth/templates/forgot_password.html

- tracking state: tracked

```html
{% extends "base.html" %}

{% block content %}
  <section class="card stack">
    <div class="stack">
      <p class="muted">Восстановление доступа</p>
      <h1 class="section-title">Сброс пароля</h1>
      <p>Укажите адрес электронной почты, чтобы мы смогли найти ваш аккаунт.</p>
    </div>

    {% if notice %}
      <div class="alert alert-info">{{ notice }}</div>
    {% endif %}
    {% if error %}
      <div class="alert alert-error">{{ error }}</div>
    {% endif %}

    <form class="form" method="post" action="/forgot-password">
      <label class="form-row">
        <span>Электронная почта</span>
        <input class="input" type="email" name="email" value="{{ email or '' }}" autocomplete="email">
      </label>
      <button class="button button-primary" type="submit">Отправить ссылку</button>
    </form>

    <div class="actions">
      <a class="button button-secondary" href="/login">Вернуться ко входу</a>
    </div>
  </section>
{% endblock %}
```

```diff
(no diff)
```


## 4. AUTH_MENU_CURRENT_CODE

- path: `source/app/shared/templates/base.html`
- tracking state: tracked
```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>OpenScript — первый ИИ-бот без опыта в программировании</title>
  <meta name="description" content="OpenScript помогает пройти первый проект с ИИ-наставником, создать своего первого ИИ-бота и понять, как дальше делать боты, автоматизации и MVP самостоятельно.">
  <link rel="icon" href="/static/favicon.svg" type="image/svg+xml">
  <link rel="shortcut icon" href="/static/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/static/styles.css">
</head>
  <body class="page{% if request.url.path == '/' %} page--landing{% endif %}">
    <div class="page-shell">
      <header class="top-nav" aria-label="Основная навигация">
        <div class="nav-inner">
          <div class="nav-brand-row">
            <a class="nav-logo" href="/">OpenScript</a>
            {% if current_user %}
              <div class="nav-account-compact" aria-label="Текущий аккаунт">
                <span class="nav-account-name">{{ current_user.login or current_user.email or "Аккаунт" }}</span>
                <span class="nav-account-email">{{ current_user.email or current_user.login or "Аккаунт" }}</span>
              </div>
            {% endif %}
          </div>
          <div class="nav-menu-row">
            <nav class="nav-links" aria-label="Навигация">
              {% if current_user %}
                <a class="button button-secondary nav-pill" href="/">Главная</a>
                {% if current_user.materials_access_granted or current_user.role in ["admin", "moderator"] %}
                  <a class="button button-secondary nav-pill" href="/materials/drafts/dair-smoke-20260529/">Обучение</a>
                {% else %}
                  <button class="button button-secondary nav-pill" type="button" disabled>Обучение</button>
                {% endif %}
                <a class="button button-secondary nav-pill" href="/cabinet">Личный кабинет</a>
                {% if current_user.role == "admin" %}
                  <a class="button button-secondary nav-pill" href="/admin">Админ-панель</a>
                {% endif %}
                <a class="button button-secondary nav-pill nav-settings" href="/cabinet/settings" title="Настройки" aria-label="Настройки">
                  <span class="nav-settings-label">Настройки</span>
                </a>
                <form class="nav-form" method="post" action="/logout">
                  <button class="button button-secondary nav-pill" type="submit">Выйти</button>
                </form>
              {% else %}
                <a class="nav-link" href="#what-you-get">Что вы получите</a>
                <a class="nav-link" href="#first-project">Первый проект</a>
                <a class="nav-link" href="#how-it-works">Как проходит работа</a>
                <a class="nav-link" href="#pricing">Цена</a>
                <a class="nav-link" href="/login">Войти</a>
              {% endif %}
            </nav>
          </div>
        </div>
      </header>
      <main class="page-content">
        {% block content %}{% endblock %}
      </main>
    </div>
    <footer class="site-footer" aria-label="Юридическая информация">
      <div class="site-footer-inner">
        <p class="site-footer-title">OpenScript</p>
        <address class="site-footer-legal">
          <p>ИП Ягофаров М.Р.</p>
          <p>ИНН: 741705866660</p>
          <p>ОГРНИП: 320745600093211</p>
          <p>Email: <a href="mailto:OpenScripts@yandex.com">OpenScripts@yandex.com</a></p>
        </address>
      </div>
    </footer>
  </body>
</html>
```

```diff
diff --git a/source/app/shared/templates/base.html b/source/app/shared/templates/base.html
index b81aa0c..9dc8195 100644
--- a/source/app/shared/templates/base.html
+++ b/source/app/shared/templates/base.html
@@ -42,11 +42,11 @@
                   <button class="button button-secondary nav-pill" type="submit">Выйти</button>
                 </form>
               {% else %}
-                <a href="#what-you-get">Что вы получите</a>
-                <a href="#first-project">Первый проект</a>
-                <a href="#how-it-works">Как проходит работа</a>
-                <a href="#pricing">Цена</a>
-                <a href="/login">Войти</a>
+                <a class="nav-link" href="#what-you-get">Что вы получите</a>
+                <a class="nav-link" href="#first-project">Первый проект</a>
+                <a class="nav-link" href="#how-it-works">Как проходит работа</a>
+                <a class="nav-link" href="#pricing">Цена</a>
+                <a class="nav-link" href="/login">Войти</a>
               {% endif %}
             </nav>
           </div>
```


- path: `source/app/static/styles.css`
- tracking state: tracked
```css

:root {
  color-scheme: light;
  --bg: #faf6f1;
  --surface: #fffefc;
  --surface-alt: #f5ede3;
  --text: #2a2118;
  --muted: #786a5e;
  --border: #eadfce;
  --primary: #c45c26;
  --primary-hover: #a84a1c;
  --secondary: #f5ede3;
  --secondary-hover: #eadfce;
  --danger: #9f2b2b;
  --danger-bg: #fbeaea;
  --info-bg: #fff7ef;
  --info-border: #f1d4bd;
  --error-bg: #fff0f0;
  --error-border: #f1b3b3;
  --shadow: 0 12px 40px rgba(42, 33, 24, 0.06);
  --radius: 24px;
  --radius-sm: 12px;
  --font-display: Georgia, "Times New Roman", "Iowan Old Style", serif;
  --font-body: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
  --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}

* {
  box-sizing: border-box;
}

html {
  background: var(--bg);
  scroll-behavior: smooth;
}

body {
  margin: 0;
  color: var(--text);
  font-family: var(--font-body);
  line-height: 1.65;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg);
  -webkit-font-smoothing: antialiased;
}

a {
  color: var(--primary);
  text-decoration-thickness: 1px;
  text-underline-offset: 0.15em;
}

a:hover {
  color: var(--primary-hover);
}

.page-shell {
  width: min(1120px, calc(100% - 32px));
  margin: 0 auto;
  padding: 24px 0 40px;
  flex: 1 0 auto;
}

.top-nav {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 10px 18px;
  margin-bottom: 20px;
  background: rgba(255, 254, 252, 0.92);
  border: 1px solid var(--border);
  border-radius: 20px;
  box-shadow: var(--shadow);
  position: relative;
  z-index: 5;
}

.nav-logo {
  flex: 0 0 auto;
  text-decoration: none;
  font-family: var(--font-display);
  font-size: 1.18rem;
  font-weight: 700;
  letter-spacing: -0.03em;
  color: var(--text);
}

.nav-logo:hover {
  color: var(--primary);
}

.top-nav .nav-inner {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
}

.top-nav .nav-brand-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  width: 100%;
  min-width: 0;
}

.top-nav .nav-menu-row {
  display: flex;
  width: 100%;
  min-width: 0;
}

.top-nav .nav-menu-row .nav-links {
  justify-content: flex-start;
}

.nav-form {
  margin: 0;
}

.top-nav .nav-links {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
  min-width: 0;
}

.top-nav .nav-links .nav-pill {
  min-height: 40px;
  padding: 8px 14px;
  line-height: 1;
  white-space: nowrap;
}

.top-nav .nav-links .nav-pill:disabled {
  opacity: 0.68;
  cursor: default;
  pointer-events: none;
}

.course-access-badge {
  display: flex;
  flex-direction: column;
  gap: 4px;
  align-items: center;
  justify-content: center;
  width: min(100%, 34rem);
  margin: 18px auto 0;
  padding: 12px 14px;
  border-radius: 16px;
  border: 1px solid rgba(196, 92, 38, 0.2);
  background: rgba(255, 255, 255, 0.82);
  box-shadow: 0 10px 24px rgba(42, 33, 24, 0.05);
  text-align: center;
}

.course-access-badge p {
  margin: 0;
  font-size: 0.98rem;
  line-height: 1.45;
}

.course-access-badge p:first-child {
  font-weight: 600;
}

.password-field {
  display: flex;
  align-items: stretch;
  gap: 10px;
}

.password-field .input {
  flex: 1 1 auto;
}

.password-toggle {
  flex: 0 0 auto;
  min-width: 142px;
  white-space: nowrap;
}

.top-nav .nav-account-compact {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 2px;
  min-width: 0;
}

.top-nav .nav-account-name {
  color: var(--text);
  font-weight: 700;
  line-height: 1.15;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 220px;
}

.top-nav .nav-account-email {
  color: var(--muted);
  font-size: 0.88rem;
  line-height: 1.15;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 260px;
}

.top-nav .nav-settings {
  min-height: 40px;
  padding: 8px 12px;
}

.top-nav .nav-settings-label {
  display: inline;
}

.top-nav .logout-form {
  margin: 0;
}

.nav-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  border-radius: 999px;
  color: var(--muted);
  text-decoration: none;
  background: transparent;
  transition: background-color 0.2s ease, color 0.2s ease;
}

.nav-link:hover {
  background: var(--bg);
  color: var(--text);
}

button.nav-button {
  min-height: 0;
  border: 0;
  background: transparent;
  color: var(--text);
  font: inherit;
  font-weight: 600;
}

button.nav-button:hover {
  background: var(--bg);
  color: var(--text);
}

.page-content {
  display: grid;
  gap: 16px;
}

.site-footer {
  flex: 0 0 auto;
  margin-top: auto;
  padding: 20px 0 28px;
  border-top: 1px solid var(--border);
  background: rgba(255, 254, 252, 0.72);
}

.site-footer-inner {
  width: min(1120px, calc(100% - 32px));
  margin: 0 auto;
  display: grid;
  gap: 6px;
  color: var(--muted);
  font-size: 0.95rem;
}

.site-footer-title {
  margin: 0;
  color: var(--text);
  font-weight: 700;
}

.site-footer-legal {
  margin: 0;
  font-style: normal;
  display: grid;
  gap: 2px;
}

.site-footer-legal p {
  margin: 0;
}

.site-footer a {
  color: inherit;
}

.site-footer a:hover {
  color: var(--primary-hover);
}

.card,
.card-grid > .card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 24px;
  box-shadow: var(--shadow);
  padding: 28px;
}

.card-grid {
  display: grid;
  gap: 16px;
}

.card-grid.tight {
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
}

.form {
  display: grid;
  gap: 14px;
}

.form-row {
  display: grid;
  gap: 6px;
}

.form-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
}

.inline-form {
  margin: 0;
}

.compact-form {
  gap: 10px;
}

.danger-zone {
  display: flex;
  align-items: flex-start;
}

.textarea {
  width: 100%;
  min-height: 120px;
  padding: 10px 12px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background: var(--surface);
  color: var(--text);
  font: inherit;
  resize: vertical;
}

.select {
  width: 100%;
  min-height: 44px;
  padding: 10px 12px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background: var(--surface);
  color: var(--text);
  font: inherit;
}

.checkbox-row {
  display: inline-flex;
  gap: 8px;
  align-items: center;
}

.form-help,
.muted {
  color: var(--muted);
}

.input,
input,
textarea,
select {
  width: 100%;
  min-height: 44px;
  padding: 10px 12px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background: var(--surface);
  color: var(--text);
  font: inherit;
}

textarea {
  min-height: 120px;
  resize: vertical;
}

.input:focus,
input:focus,
textarea:focus,
select:focus {
  outline: 2px solid rgba(33, 68, 216, 0.18);
  outline-offset: 1px;
  border-color: rgba(33, 68, 216, 0.5);
}

.button,
.btn,
button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  min-height: 44px;
  padding: 12px 18px;
  border: 1px solid transparent;
  border-radius: 999px;
  background: var(--secondary);
  color: var(--text);
  font: inherit;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
}

.button:hover,
.btn:hover,
button:hover {
  background: var(--secondary-hover);
}

.button-primary,
.btn-primary {
  background: var(--primary);
  color: #fff;
}

.button-primary:hover,
.btn-primary:hover {
  background: var(--primary-hover);
  color: #fff;
}

.button-secondary,
.btn-secondary {
  background: var(--secondary);
  color: var(--text);
}

.button-secondary:hover,
.btn-secondary:hover {
  background: var(--secondary-hover);
}

.button-danger,
.btn-danger {
  background: var(--danger-bg);
  color: var(--danger);
}

.button-danger:hover,
.btn-danger:hover {
  background: #f7dada;
  color: var(--danger);
}

.alert {
  padding: 12px 14px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border);
}

.alert-info {
  background: var(--info-bg);
  border-color: var(--info-border);
}

.alert-error {
  background: var(--error-bg);
  border-color: var(--error-border);
}

.login-unverified {
  gap: 10px;
}

.login-unverified__title,
.login-unverified__text {
  margin: 0;
}

.login-unverified__title {
  font-weight: 700;
}

.login-unverified__text {
  color: var(--muted);
}

.login-unverified__action {
  align-self: flex-start;
  width: fit-content;
  min-height: 40px;
}

.table {
  width: 100%;
  border-collapse: collapse;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
}

.table th,
.table td {
  padding: 12px 14px;
  border-bottom: 1px solid var(--border);
  vertical-align: top;
  text-align: left;
}

.table th {
  background: var(--surface-alt);
  color: var(--muted);
  font-weight: 700;
}

.table tr:last-child td {
  border-bottom: none;
}

.table-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}

.table-actions form {
  margin: 0;
}

.empty-state {
  display: grid;
  gap: 10px;
  padding: 12px 14px;
  border: 1px dashed var(--border);
  border-radius: var(--radius-sm);
  background: var(--surface-alt);
}

.badge {
  display: inline-flex;
  align-items: center;
  min-height: 26px;
  padding: 2px 10px;
  border-radius: 999px;
  background: #e9eef7;
  color: var(--text);
  font-size: 0.92rem;
  font-weight: 600;
}

.badge-muted {
  background: #eef2f7;
  color: var(--muted);
}

.badge-success {
  background: #e6f5ea;
  color: #21613b;
}

.stack {
  display: grid;
  gap: 14px;
}

.section-title {
  margin: 0 0 8px;
  font-family: var(--font-display);
  font-weight: 400;
  line-height: 1.12;
  letter-spacing: -0.03em;
}

.section-heading {
  margin-bottom: 2px;
}

.settings-shell {
  width: min(860px, calc(100% - 32px));
  margin: 0 auto;
}

.settings-card {
  gap: 20px;
}

.settings-header {
  gap: 10px;
}

.settings-lead {
  margin: 0;
  max-width: 56ch;
  color: var(--muted);
}

.settings-meta {
  display: grid;
  gap: 10px;
  max-width: 520px;
  padding: 14px 16px;
  border: 1px solid var(--border);
  border-radius: 18px;
  background: var(--surface-alt);
}

.settings-meta-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: space-between;
  align-items: baseline;
}

.settings-meta-label {
  color: var(--muted);
  font-size: 0.88rem;
}

.settings-form-card {
  display: grid;
  gap: 16px;
  max-width: 620px;
}

.settings-form {
  width: 100%;
  max-width: 100%;
}

.settings-actions {
  justify-content: flex-start;
}

.settings-actions .button {
  width: auto;
}

.course-head {
  position: relative;
  overflow: hidden;
  padding: 36px 28px 44px;
  border: 1px solid var(--border);
  border-radius: 24px;
  background: var(--surface);
  box-shadow: var(--shadow);
}

.course-head::after {
  content: "";
  position: absolute;
  inset: auto -120px -140px auto;
  width: 300px;
  height: 300px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(196, 92, 38, 0.14), transparent 68%);
  pointer-events: none;
}

.hero-bg-visual {
  position: absolute;
  inset: 0;
  pointer-events: none;
  user-select: none;
  overflow: hidden;
}

.hero-bg-desktop {
  display: block;
}

.hero-bg-mobile {
  display: none;
}

.hero-bg-visual img {
  position: absolute;
  left: 50%;
  top: 33%;
  width: min(1280px, 108vw);
  max-width: none;
  height: auto;
  transform: translate(-50%, -50%);
  opacity: 0.76;
  filter: sepia(0.04) saturate(1.55) contrast(1.75) brightness(0.72);
}

.hero-wrap {
  position: relative;
  z-index: 1;
  display: flex;
  justify-content: center;
}

.hero-copy {
  width: min(900px, 100%);
  margin: 0 auto;
  text-align: center;
}

.course-head h1 {
  margin: 14px auto 0;
  max-width: 1000px;
  color: var(--text);
  font-family: var(--font-display);
  font-size: clamp(2.4rem, 5.8vw, 4.4rem);
  font-weight: 400;
  line-height: 1.02;
  letter-spacing: -0.045em;
  text-wrap: balance;
}

.course-headline {
  margin: 14px auto 0;
  max-width: 900px;
  color: var(--text);
  font-family: var(--font-display);
  font-size: clamp(1.4rem, 2.9vw, 2.2rem);
  font-weight: 700;
  line-height: 1.12;
  letter-spacing: -0.03em;
}

.course-note {
  margin: 16px auto 0;
  max-width: 720px;
  color: var(--accent-strong);
  font-size: 1.05rem;
}

.course-head-actions,
.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 24px;
  justify-content: center;
}

.course-head .eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  font-family: var(--font-mono);
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--accent);
}

.course-head-actions .btn {
  min-width: 220px;
}

.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 24px;
  box-shadow: var(--shadow);
}

.course-intro {
  padding: 28px;
  display: grid;
  gap: 16px;
}

.course-intro-body {
  display: grid;
  gap: 14px;
}

.course-intro-part {
  display: grid;
  gap: 8px;
  padding: 16px 18px;
  border: 1px solid var(--border);
  border-radius: 18px;
  background: var(--surface-alt);
  box-shadow: 0 6px 14px rgba(42, 33, 24, 0.04);
}

.course-intro-part h3 {
  margin: 0;
  font-family: var(--font-display);
  font-size: 1.12rem;
  line-height: 1.18;
  text-align: left;
  color: var(--text);
}

.course-intro-part p {
  margin: 0;
  max-width: 900px;
  text-align: left;
  line-height: 1.45;
}

.course-intro-part p + p {
  margin-top: 8px;
}

.course-intro .section-heading {
  margin-bottom: 2px;
  text-align: left;
}

.course-paywall-note {
  max-width: 720px;
}

.pricing-shell,
.public-landing-page .pricing-shell {
  border: 1px solid var(--border);
  border-radius: 28px;
  background: linear-gradient(180deg, #fffaf5 0%, var(--surface) 100%);
  padding: 38px;
}

.price-head,
.public-landing-page .price-head {
  max-width: 720px;
  text-align: center;
  margin: 0 auto 22px;
}

.price-value,
.public-landing-page .price-value {
  margin: 14px 0 0;
  font-family: var(--font-display);
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 400;
  line-height: 1;
  letter-spacing: -0.04em;
}

.offer-grid,
.public-landing-page .offer-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
  margin-top: 24px;
}

.offer-group,
.public-landing-page .offer-group {
  padding: 24px;
  border-radius: 22px;
  border: 1px solid var(--border);
  background: var(--surface);
}

.offer-group h3,
.public-landing-page .offer-group h3 {
  margin: 0;
  font-family: var(--font-display);
  font-size: 1.12rem;
  letter-spacing: -0.02em;
}

.offer-group p,
.public-landing-page .offer-group p {
  margin: 10px 0 0;
  color: var(--muted);
  font-size: 0.92rem;
}

.offer-group ul,
.public-landing-page .offer-group ul {
  margin-top: 14px;
}

.pricing-actions,
.public-landing-page .pricing-actions {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 14px;
  margin-top: 28px;
}

.pricing-note,
.public-landing-page .pricing-note {
  max-width: 720px;
  text-align: center;
  color: var(--muted);
  font-size: 0.92rem;
}

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
}

.learning-card {
  gap: 20px;
  text-align: center;
  align-items: center;
}

.learning-card-title {
  color: var(--accent-strong);
  text-align: center;
}

.learning-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
  align-items: stretch;
  width: 100%;
}

.learning-column {
  display: flex;
  flex-direction: column;
  gap: 14px;
  align-items: center;
  min-width: 0;
  padding: 20px;
  border: 1px solid var(--border);
  border-radius: 20px;
  background: var(--surface-alt);
  text-align: center;
}

.learning-column .section-title {
  font-size: clamp(1.4rem, 2vw, 1.8rem);
  color: var(--accent-strong);
  text-align: center;
}

.learning-button {
  align-self: center;
  min-width: min(100%, 240px);
}

.learning-card-note,
.learning-card-lock {
  margin: 0;
  width: min(60ch, 100%);
  margin-left: auto;
  margin-right: auto;
  text-align: center;
}

.learning-card .button:disabled,
.learning-card button:disabled {
  background: var(--surface-alt);
  border-color: var(--border);
  color: var(--muted);
  box-shadow: none;
  opacity: 0.72;
  cursor: not-allowed;
  pointer-events: none;
}

.accounts-card {
  gap: 16px;
}

.accounts-header {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: space-between;
  align-items: flex-start;
}

.accounts-intro {
  flex: 1 1 320px;
  max-width: 56ch;
}

.accounts-role-note {
  margin: 0;
  color: var(--muted);
  max-width: 60ch;
}

.accounts-builder-shell {
  flex: 1 1 100%;
  width: min(100%, 680px);
  display: grid;
  gap: 10px;
  padding: 12px 14px;
  border: 1px solid var(--border);
  border-radius: 18px;
  background: var(--surface-alt);
}

.accounts-builder {
  width: 100%;
}

.accounts-builder--server {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px 10px;
  align-items: end;
  justify-content: stretch;
}

.accounts-type-field {
  flex: 1 1 180px;
  min-width: 180px;
  max-width: 220px;
}

.accounts-builder--server .accounts-type-field {
  width: 100%;
  min-width: 0;
  max-width: none;
  flex: 1 1 auto;
}

.accounts-field {
  display: grid;
  gap: 4px;
}

.accounts-field > span {
  color: var(--muted);
  font-weight: 600;
  font-size: 0.84rem;
}

.accounts-field--wide {
  grid-column: span 2;
}

.accounts-builder .select {
  min-height: 38px;
  padding: 8px 10px;
  border-radius: 10px;
  font-size: 0.95rem;
}

.accounts-builder--server .select,
.accounts-builder--server .input {
  width: 100%;
}

.accounts-builder .button {
  min-height: 38px;
  padding: 8px 12px;
  font-size: 0.92rem;
  white-space: nowrap;
}

.accounts-builder--server .button {
  grid-column: 1 / -1;
  justify-self: start;
  min-width: 160px;
}

.accounts-duration-note {
  margin: 0;
  grid-column: 1 / -1;
  color: var(--muted);
  font-size: 0.92rem;
}

.accounts-owner-groups {
  display: grid;
  gap: 16px;
}

.account-owner-group {
  display: grid;
  gap: 12px;
}

.accounts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 280px));
  gap: 12px;
  justify-content: start;
  align-items: stretch;
}

.account-card {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  min-width: 0;
  max-width: 280px;
  gap: 10px;
  padding: 14px;
  border: 1px solid var(--border);
  border-radius: 18px;
  background: var(--surface-alt);
  box-shadow: none;
}

.account-card__headline {
  gap: 8px;
  min-width: 0;
}

.account-card__title-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: space-between;
  align-items: center;
}

.account-card--editing {
  border-color: rgba(196, 92, 38, 0.36);
  background: #fffaf4;
}

.account-card--locked .account-card__edit {
  display: inline-flex;
}

.account-card--editing .account-card__save {
  display: inline-flex;
}

.account-card__header {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  align-items: center;
}

.account-card__title {
  margin: 0;
  font-family: var(--font-display);
  font-size: 0.98rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.12;
}

.account-card__badges {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  justify-content: flex-end;
  align-items: center;
}

.account-card__type-badge,
.account-card__status-badge {
  display: inline-flex;
  align-items: center;
  flex: 0 0 auto;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  line-height: 1;
  white-space: nowrap;
}

.account-card__type-badge {
  background: var(--surface);
  color: var(--text);
  border: 1px solid var(--border);
}

.account-card__status-badge {
  background: var(--accent-soft);
  color: var(--accent-strong);
}

.account-card__status-badge--active {
  background: rgba(84, 145, 61, 0.14);
  color: #2f6c2f;
}

.account-card__status-badge--inactive {
  background: var(--surface);
  color: var(--muted);
}

.account-card__status-badge--expired {
  background: rgba(159, 43, 43, 0.12);
  color: var(--danger);
}

.account-card__owner-line {
  margin: 0;
  color: var(--muted);
  font-size: 0.84rem;
}

.account-card__body,
.account-card__form,
.account-card__readonly,
.account-card__edit-form {
  display: flex;
  flex-direction: column;
  flex: 1 1 auto;
  gap: 12px;
  min-height: 0;
}

.account-card__edit-form[hidden] {
  display: none;
}

.account-card__edit-form:not([hidden]) {
  display: grid;
}

.account-card--editing .account-card__readonly {
  display: none;
}

.account-card--editing .account-card__edit-form {
  display: grid;
}

.account-card__details {
  display: grid;
  gap: 6px;
  margin-top: auto;
}

.account-card__detail {
  margin: 0;
  color: var(--muted);
  font-size: 0.88rem;
  line-height: 1.35;
}

.accounts-card--cabinet .accounts-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
  justify-content: start;
  align-items: stretch;
}

.accounts-card--cabinet .account-card {
  width: 100%;
  max-width: none;
  min-width: 0;
}

.accounts-card--cabinet .account-card--vpn {
  grid-column: 1 / -1;
}

.accounts-card--cabinet .account-card__headline {
  display: grid;
  gap: 8px;
  min-width: 0;
}

.accounts-card--cabinet .account-card__title-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 8px 10px;
  align-items: center;
}

.accounts-card--cabinet .account-card__title {
  word-break: normal;
  overflow-wrap: normal;
  white-space: nowrap;
  hyphens: none;
}

.accounts-card--cabinet .account-card__badges {
  align-items: center;
}

.accounts-card--cabinet .account-field__control {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 8px;
  align-items: stretch;
}

.accounts-card--cabinet .account-password-row {
  align-items: stretch;
}

.accounts-card--cabinet .account-card__details {
  align-items: start;
}

.accounts-card--cabinet .account-card__detail {
  min-height: 1.35em;
}

.account-card--vpn {
  border-color: rgba(196, 92, 38, 0.26);
  background: linear-gradient(180deg, #fffdf8 0%, #fff7ee 100%);
}

.accounts-card--cabinet .account-card--vpn .account-card__header {
  align-items: flex-start;
}

.accounts-card--cabinet .account-card--vpn .account-card__title-row {
  grid-template-columns: 1fr;
}

.accounts-card--cabinet .account-card--vpn .account-card__badges {
  display: none;
}

.vpn-card__body {
  display: grid;
  gap: 14px;
}

.vpn-card__link {
  width: fit-content;
  max-width: 100%;
  justify-self: start;
  padding-inline: 18px;
  min-width: 220px;
  justify-content: center;
  text-align: center;
  text-decoration: none;
}

.vpn-card__video-panel {
  display: grid;
  gap: 12px;
  padding: 12px;
  border: 1px solid rgba(234, 223, 206, 0.9);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.86);
}

.vpn-card__video {
  display: block;
  width: 100%;
  height: auto;
  border-radius: 12px;
  background: #000;
  aspect-ratio: 16 / 9;
}

.cabinet-vpn-section {
  gap: 0;
}

.cabinet-vpn-disclosure {
  display: grid;
  gap: 14px;
  padding: 16px 18px;
  border: 1px solid rgba(234, 223, 206, 0.96);
  border-radius: 20px;
  background: linear-gradient(180deg, #fffdf8 0%, #fff7ee 100%);
}

.cabinet-vpn-disclosure > summary {
  display: grid;
  gap: 0;
  cursor: pointer;
  list-style: none;
  outline: none;
}

.cabinet-vpn-disclosure > summary::-webkit-details-marker {
  display: none;
}

.cabinet-vpn-disclosure > summary:focus-visible {
  border-radius: 12px;
  box-shadow: 0 0 0 3px rgba(214, 127, 63, 0.2);
}

.cabinet-vpn-summary__title {
  margin: 0 0 8px;
}

.cabinet-vpn-summary__hint {
  margin: 0;
}

.cabinet-vpn-content {
  display: grid;
  gap: 14px;
}

.cabinet-vpn-note {
  margin: 0;
  color: var(--text);
  font-size: 1rem;
  line-height: 1.65;
  font-weight: 500;
}

.cabinet-vpn-content .account-actions--view {
  margin-top: 4px;
}

.accounts-card--cabinet .account-card--vpn .account-card__details {
  gap: 8px;
}

.accounts-card--cabinet .account-card--vpn .account-card__detail {
  margin: 0;
}

.account-card__delete {
  flex: 0 0 auto;
  min-height: 32px;
  padding: 7px 10px;
  border-radius: 999px;
  background: var(--surface);
  border-color: var(--border);
  color: var(--danger);
  box-shadow: none;
  font-size: 0.82rem;
  line-height: 1.1;
}

.account-card__delete:hover {
  background: var(--danger-bg);
  border-color: #f0c3c3;
  color: var(--danger);
}

.account-field {
  display: grid;
  gap: 4px;
}

.account-field > span {
  display: flex;
  align-items: center;
  color: var(--muted);
  font-weight: 600;
  font-size: 0.84rem;
  line-height: 1.2;
  min-height: 1.2em;
}

.account-field__input {
  width: 100%;
  min-width: 0;
}

.account-field__actions {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 6px;
  align-items: stretch;
}

.account-field__actions--split {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.account-field__control {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 6px;
  align-items: stretch;
}

.account-password-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 6px;
  align-items: stretch;
}

.account-card .input {
  flex: 1 1 auto;
  min-width: 0;
  min-height: 38px;
  padding: 8px 10px;
  border-radius: 10px;
  font-size: 0.95rem;
  line-height: 1.2;
}

.account-card .input[readonly] {
  background: var(--surface);
  color: var(--text);
  cursor: default;
}

.account-card .select {
  min-height: 38px;
  padding: 8px 10px;
  border-radius: 10px;
  font-size: 0.95rem;
}

.account-password-toggle {
  flex: 0 0 auto;
  min-height: 38px;
  padding: 8px 10px;
  border-radius: 999px;
  font-size: 0.82rem;
  line-height: 1.1;
  align-self: stretch;
  width: 100%;
}

.account-copy-button {
  flex: 0 0 auto;
  min-height: 38px;
  padding: 8px 10px;
  border-radius: 999px;
  font-size: 0.82rem;
  line-height: 1.1;
  align-self: stretch;
  width: 100%;
}

.account-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  align-items: stretch;
}

.account-actions--view {
  margin-top: auto;
}

.account-action-form {
  margin: 0;
  display: flex;
  flex: 1 1 120px;
  align-items: stretch;
}

.account-actions .button {
  width: 100%;
  min-width: 0;
  min-height: 32px;
  padding: 7px 10px;
  border-radius: 999px;
  font-size: 0.82rem;
  line-height: 1.1;
  white-space: nowrap;
  align-self: stretch;
}

.account-actions--view .button,
.account-actions--edit .button {
  flex: 1 1 120px;
}

.account-actions--view .account-action-form .button {
  flex: 1 1 auto;
}

.account-card__save,
.account-card__activate,
.account-card__edit-toggle,
.account-card__cancel {
  min-width: 0;
}

.account-actions .button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.accounts-empty,
.accounts-notice {
  margin: 0;
}

.accounts-notice {
  min-height: 1.5em;
  color: var(--muted);
}

@media (max-width: 980px) {
  .accounts-card--cabinet .accounts-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 720px) {
  .accounts-card--cabinet .accounts-grid {
    grid-template-columns: 1fr;
  }

  .accounts-card--cabinet .account-card {
    width: 100%;
    max-width: none;
    flex-basis: 100%;
  }

  .accounts-card--cabinet .account-card__title-row {
    grid-template-columns: 1fr;
  }

  .accounts-card--cabinet .account-card__badges {
    justify-content: flex-start;
  }

  .cabinet-vpn-disclosure {
    padding: 14px;
  }

  .cabinet-vpn-content .vpn-card__link {
    width: 100%;
    min-width: 0;
    justify-self: stretch;
  }

  .accounts-card--cabinet .account-field__control {
    grid-template-columns: 1fr;
    align-items: stretch;
  }

  .accounts-card--cabinet .account-password-row {
    grid-template-columns: 1fr;
  }

  .accounts-card--cabinet .account-field__actions,
  .accounts-card--cabinet .account-field__actions--split {
    grid-template-columns: 1fr;
  }

  .accounts-card--cabinet .account-copy-button {
    width: 100%;
  }

  .accounts-card--cabinet .account-card__detail {
    min-height: 0;
  }
}

.prompts-library-card {
  gap: 16px;
  --prompt-card-collapsed-height: 192px;
}

.prompts-library-header {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: space-between;
  align-items: flex-start;
}

.prompts-library-intro {
  flex: 1 1 360px;
  max-width: 72ch;
}

.prompts-add-button {
  flex: 0 0 auto;
  min-height: 38px;
  padding: 8px 12px;
  align-self: flex-start;
}

.prompts-section {
  display: grid;
  gap: 12px;
}

.prompts-section__header {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  align-items: flex-end;
}

.prompts-section__title {
  font-size: clamp(1.2rem, 2vw, 1.55rem);
  color: var(--accent-strong);
}

.prompts-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: flex-start;
}

.prompt-card {
  display: grid;
  flex: 1 1 420px;
  width: min(100%, 560px);
  gap: 12px;
  padding: 16px;
  border: 1px solid var(--border);
  border-radius: 18px;
  background: var(--surface-alt);
  box-shadow: none;
}

.prompt-card--custom,
.prompt-card--editing {
  border-color: rgba(196, 92, 38, 0.36);
  background: #fffaf4;
}

.prompt-card--collapsed {
  display: flex;
  flex-direction: column;
  height: var(--prompt-card-collapsed-height);
  overflow: hidden;
  gap: 10px;
}

.prompt-card__header {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  align-items: flex-start;
}

.prompt-card__intro {
  flex: 1 1 auto;
  min-width: 0;
}

.prompt-card__title {
  margin: 0;
  font-family: var(--font-display);
  font-size: 1.02rem;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.prompt-card--collapsed .prompt-card__title {
  display: -webkit-box;
  overflow: hidden;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

.prompt-card__meta {
  margin: 0;
  color: var(--muted);
  font-size: 0.84rem;
}

.prompt-card--collapsed .prompt-card__meta,
.prompt-card--collapsed .prompt-card__filename {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.prompt-card__filename {
  margin: 0;
  color: var(--muted);
  font-size: 0.78rem;
}

.prompt-card__header-actions {
  display: flex;
  flex-direction: column;
  gap: 6px;
  justify-items: end;
  align-items: start;
  flex: 0 0 auto;
}

.prompt-card__badge {
  flex: 0 0 auto;
  padding: 4px 10px;
  border-radius: 999px;
  background: var(--accent-soft);
  color: var(--accent-strong);
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  white-space: nowrap;
}

.prompt-card__toggle {
  min-height: 32px;
  padding: 7px 12px;
  border-radius: 999px;
  font-size: 0.8rem;
  line-height: 1.1;
}

.prompt-card__body {
  display: grid;
  gap: 12px;
  min-height: 0;
}

.prompt-field {
  display: grid;
  gap: 4px;
}

.prompt-field > span {
  color: var(--muted);
  font-weight: 600;
  font-size: 0.84rem;
}

.prompt-card .input,
.prompt-textarea {
  min-width: 0;
}

.prompt-card .input {
  min-height: 38px;
  padding: 8px 10px;
  border-radius: 10px;
  font-size: 0.95rem;
}

.prompt-card .input[readonly],
.prompt-textarea[readonly] {
  background: var(--surface);
  color: var(--text);
  cursor: default;
}

.prompt-title-field {
  display: grid;
  gap: 4px;
}

.prompt-title-field > span {
  color: var(--muted);
  font-weight: 600;
  font-size: 0.84rem;
}

.prompt-textarea {
  min-height: 220px;
  padding: 12px 14px;
  border-radius: 14px;
  resize: vertical;
  font-family: var(--font-mono);
  font-size: 0.92rem;
  line-height: 1.6;
}

.prompt-card--collapsed .prompt-card__body[hidden] {
  display: none;
}

.prompt-card--collapsed .prompt-card__header {
  flex: 1 1 auto;
  align-items: stretch;
}

.prompt-card--collapsed .prompt-card__intro {
  justify-content: flex-start;
}

.prompt-card--collapsed .prompt-card__header-actions {
  justify-content: flex-start;
}

@media (max-width: 640px) {
  .prompts-library-card {
    --prompt-card-collapsed-height: 176px;
  }
}

.prompt-actions {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 6px;
  align-items: stretch;
}

.prompt-actions .button {
  width: 100%;
  min-width: 0;
  min-height: 32px;
  padding: 7px 10px;
  border-radius: 999px;
  font-size: 0.82rem;
  line-height: 1.1;
  white-space: nowrap;
}

.prompt-actions .button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.prompts-empty,
.prompts-notice {
  margin: 0;
}

.prompts-notice {
  min-height: 1.5em;
  color: var(--muted);
}

.paid-options-card {
  gap: 16px;
}

.paid-options-header {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: space-between;
  align-items: flex-start;
}

.paid-options-intro {
  flex: 1 1 360px;
  max-width: 72ch;
}

.paid-options-count {
  margin: 0;
  color: var(--muted);
  font-size: 0.92rem;
  font-weight: 600;
}

.paid-options-grid {
  display: grid;
  gap: 12px;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  align-items: stretch;
}

.paid-option-card {
  display: flex;
  flex-direction: column;
  gap: 12px;
  height: 100%;
  min-height: 248px;
  padding: 16px;
  border: 1px solid var(--border);
  border-radius: 18px;
  background: var(--surface-alt);
  box-shadow: none;
}

.paid-option__intro {
  gap: 8px;
  min-height: 7.25rem;
}

.paid-option__headline {
  display: flex;
  gap: 10px;
  justify-content: space-between;
  align-items: flex-start;
  min-height: 2.75rem;
}

.paid-option__title {
  margin: 0;
  font-family: var(--font-display);
  font-size: 1.02rem;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.paid-option__badge {
  flex: 0 0 auto;
  padding: 4px 10px;
  border-radius: 999px;
  background: var(--accent-soft);
  color: var(--accent-strong);
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  white-space: nowrap;
}

.paid-option__description,
.paid-option__price,
.paid-option__duration,
.paid-option__renewable {
  margin: 0;
}

.paid-option__description {
  color: var(--text);
  min-height: 2.75rem;
}

.paid-option__meta {
  gap: 6px;
  min-height: 4.5rem;
}

.paid-option__price,
.paid-option__duration,
.paid-option__renewable {
  color: var(--muted);
  font-size: 0.92rem;
}

.paid-option__price {
  font-weight: 700;
  color: var(--text);
}

.paid-option__actions {
  margin-top: auto;
  padding-top: 2px;
}

.paid-option__buy {
  min-width: 0;
}

.paid-options-empty,
.paid-options-notice {
  margin: 0;
}

.paid-options-notice {
  min-height: 1.5em;
  color: var(--muted);
}

@media (max-width: 640px) {
  .paid-option__intro {
    min-height: 6.25rem;
  }

  .paid-option__headline {
    min-height: 2.4rem;
  }

  .paid-option__description {
    min-height: 2.2rem;
  }

  .paid-option__meta {
    min-height: 4rem;
  }

  .paid-option-card {
    min-height: 224px;
  }
}

h1,
h2,
h3 {
  margin: 0;
  line-height: 1.12;
  font-family: var(--font-display);
}

h1 {
  font-size: clamp(2.4rem, 5.8vw, 4.4rem);
  font-weight: 400;
  letter-spacing: -0.045em;
}

h2 {
  font-size: clamp(1.8rem, 3.4vw, 2.9rem);
  font-weight: 400;
}

h3 {
  font-size: 1.22rem;
  font-weight: 700;
  line-height: 1.18;
  letter-spacing: -0.02em;
}




/* ===== Landing Page: Concept 02 Human Start ===== */

:root {
  --bg: #faf6f1;
  --surface: #fffefc;
  --surface-alt: #f5ede3;
  --fg: #2a2118;
  --muted: #786a5e;
  --border: #eadfce;
  --accent: #c45c26;
  --accent-soft: rgba(196, 92, 38, 0.1);
  --accent-strong: #a84a1c;
  --success: #47644a;
  --success-soft: rgba(71, 100, 74, 0.1);
  --shadow: 0 12px 40px rgba(42, 33, 24, 0.06);
  --font-display: Georgia, "Times New Roman", "Iowan Old Style", serif;
  --font-body: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
  --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}

*,
*::before,
*::after { box-sizing: border-box; }

html { scroll-behavior: smooth; }

.public-landing-page {
  margin: 0;
  font-family: var(--font-body);
  background: var(--bg);
  color: var(--fg);
  line-height: 1.65;
  -webkit-font-smoothing: antialiased;
}

.public-landing-page a { color: inherit; }

.public-landing-page .container {
  width: min(1120px, calc(100% - 32px));
  margin: 0 auto;
}

.public-landing-page .eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-family: var(--font-mono);
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--accent);
}

.public-landing-page .section {
  padding: 56px 0;
}

.public-landing-page .section-header {
  max-width: 760px;
  margin: 0 auto 30px;
  text-align: center;
}

.public-landing-page .section-header.align-left {
  margin-left: 0;
  text-align: left;
}

.public-landing-page .section-title {
  margin: 12px 0 0;
  font-family: var(--font-display);
  font-size: clamp(1.8rem, 3.4vw, 2.9rem);
  font-weight: 400;
  line-height: 1.12;
  letter-spacing: -0.03em;
}

.public-landing-page .section-desc {
  margin: 14px 0 0;
  font-size: 1.02rem;
  color: var(--muted);
}

.public-landing-page .nav {
  position: sticky;
  top: 0;
  z-index: 20;
  padding: 12px 0;
  background: color-mix(in srgb, var(--bg) 88%, white 12%);
  backdrop-filter: blur(10px);
}

.public-landing-page .nav-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 10px 18px;
  border: 1px solid var(--border);
  border-radius: 20px;
  background: rgba(255, 254, 252, 0.92);
}

.public-landing-page .nav-logo {
  flex: 0 0 auto;
  text-decoration: none;
  font-family: var(--font-display);
  font-size: 1.18rem;
  font-weight: 700;
  letter-spacing: -0.03em;
}

.public-landing-page .nav-links {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  flex-wrap: wrap;
  gap: 6px;
}

.public-landing-page .nav-links a {
  text-decoration: none;
  font-size: 0.88rem;
  font-weight: 500;
  color: var(--muted);
  padding: 8px 14px;
  border-radius: 999px;
  transition: background-color 0.2s ease, color 0.2s ease;
}

.public-landing-page .nav-links a:hover {
  background: var(--bg);
  color: var(--fg);
}

.public-landing-page .nav-links .nav-cta {
  background: var(--accent);
  color: #fff;
}

.public-landing-page .nav-links .nav-cta:hover {
  background: var(--accent-strong);
  color: #fff;
}

.public-landing-page .hero {
  padding: 28px 0 42px;
}

.public-landing-page .hero-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.public-landing-page .hero-copy {
  padding: 12px 0;
  max-width: 900px;
  margin: 0 auto;
}

.public-landing-page .hero-title {
  margin: 14px auto 0;
  font-family: var(--font-display);
  font-size: clamp(2.4rem, 5.8vw, 4.4rem);
  font-weight: 400;
  line-height: 1.02;
  letter-spacing: -0.045em;
  text-wrap: balance;
  max-width: 1000px;
}

.public-landing-page .hero-lead {
  margin: 16px auto 0;
  max-width: 720px;
  font-size: 1.08rem;
  color: var(--muted);
}

.public-landing-page .hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 24px;
  justify-content: center;
}

.public-landing-page .hero-bg-visual {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  user-select: none;
  overflow: hidden;
}

.public-landing-page .hero-bg-desktop {
  display: block !important;
}

.public-landing-page .hero-bg-mobile {
  display: none !important;
}

.public-landing-page .hero-bg-desktop img {
  position: absolute;
  left: 50%;
  top: 33%;
  width: min(1280px, 108vw);
  max-width: none;
  height: auto;
  transform: translate(-50%, -50%);
  opacity: 0.76;
  filter: sepia(0.04) saturate(1.55) contrast(1.75) brightness(0.72);
}

.public-landing-page .hero-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 20px;
}

.hero-badge,
.public-landing-page .mini-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--muted);
  font-size: 0.82rem;
  font-weight: 600;
}

.hero-badge-dot,
.public-landing-page .mini-badge-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--accent);
  flex: 0 0 auto;
}

.public-landing-page .btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 26px;
  border-radius: 999px;
  border: 1px solid transparent;
  font-size: 0.95rem;
  font-weight: 700;
  text-decoration: none;
  transition: transform 0.2s ease, background-color 0.2s ease, border-color 0.2s ease, color 0.2s ease;
}

.public-landing-page .btn:hover { transform: translateY(-1px); }

.public-landing-page .btn-primary {
  background: var(--accent);
  color: #fff;
}

.public-landing-page .btn-primary:hover {
  background: var(--accent-strong);
}

.public-landing-page .btn-secondary {
  background: var(--surface);
  border-color: var(--border);
  color: var(--fg);
}

.public-landing-page .btn-secondary:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.public-landing-page .card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 24px;
  padding: 28px;
  box-shadow: var(--shadow);
}

.public-landing-page .card.flat-shadow { box-shadow: none; }

.public-landing-page .card-kicker {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  font-family: var(--font-mono);
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--accent);
}

.public-landing-page .card-title {
  margin: 0;
  font-family: var(--font-display);
  font-size: 1.22rem;
  font-weight: 700;
  line-height: 1.18;
  letter-spacing: -0.02em;
}

.card-text,
.card-list,
.public-landing-page .card-note {
  color: var(--muted);
}

.public-landing-page .card-text {
  margin: 10px 0 0;
  font-size: 0.95rem;
}

.public-landing-page .card-list {
  margin: 14px 0 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 10px;
}

.card-list li,
.detail-list li,
.offer-group li,
.limit-list li,
.public-landing-page .faq-item p {
  position: relative;
  padding-left: 18px;
}

.card-list li::before,
.detail-list li::before,
.offer-group li::before,
.limit-list li::before,
.public-landing-page .check-list li::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0.62em;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--accent);
}

.public-landing-page .hero-cards {
  margin-top: 40px;
}

.public-landing-page .hero-summary {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.public-landing-page .hero-summary .card {
  padding: 24px;
}

.public-landing-page .hero-summary .card-list {
  gap: 12px;
}

.public-landing-page .hero-summary .card-list li {
  padding-left: 22px;
  font-size: 0.94rem;
}

.public-landing-page .product-strip {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 12px;
  margin-top: 18px;
}

.public-landing-page .strip-item {
  padding: 16px 18px;
  background: var(--surface-alt);
  border: 1px solid var(--border);
  border-radius: 18px;
}

.public-landing-page .strip-item strong {
  display: block;
  margin-bottom: 4px;
  font-size: 0.92rem;
}

.public-landing-page .strip-item span {
  color: var(--muted);
  font-size: 0.86rem;
}

.compare-grid,
.triple-grid,
.levels-grid,
.community-grid,
.public-landing-page .faq-grid {
  display: grid;
  gap: 16px;
}

.public-landing-page .compare-grid {
  grid-template-columns: 1fr 1fr;
}

.public-landing-page .compare-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 24px;
  padding: 26px;
}

.compare-card h3,
.level-card h3,
.step-card h3,
.community-card h3,
.public-landing-page .faq-item summary {
  margin: 0;
  font-family: var(--font-display);
  font-size: 1.18rem;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.compare-card ul,
.detail-list,
.offer-group ul,
.limit-list,
.public-landing-page .check-list {
  margin: 14px 0 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 10px;
  color: var(--muted);
}

.public-landing-page .check-list li {
  position: relative;
  padding-left: 18px;
}

.public-landing-page .compare-card.now {
  background: linear-gradient(180deg, #fff8f3 0%, var(--surface) 100%);
}

.public-landing-page .triple-grid {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.public-landing-page .project-highlight {
  background: linear-gradient(180deg, #fff8f1 0%, #fffefc 100%);
  border: 1px solid #e8d4be;
}

.public-landing-page .project-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.05fr) minmax(0, 0.95fr);
  gap: 18px;
}

.public-landing-page .detail-box {
  padding: 22px;
  border-radius: 20px;
  border: 1px solid var(--border);
  background: var(--bg);
}

.public-landing-page .detail-box h3 {
  margin: 0;
  font-family: var(--font-display);
  font-size: 1.1rem;
  letter-spacing: -0.02em;
}

.public-landing-page .detail-list {
  margin-top: 12px;
}

.public-landing-page .project-note {
  margin-top: 18px;
  padding: 18px 20px;
  border-radius: 20px;
  background: var(--accent-soft);
  color: var(--fg);
  font-size: 0.95rem;
}

.public-landing-page .two-column {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.public-landing-page .estimate-intro {
  max-width: 760px;
  margin: 0 auto 22px;
  text-align: center;
  color: var(--muted);
}

.public-landing-page .levels-grid {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.public-landing-page .level-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 24px;
  padding: 26px;
}

.public-landing-page .level-meta {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  padding: 6px 12px;
  border-radius: 999px;
  background: var(--surface-alt);
  color: var(--accent);
  font-size: 0.78rem;
  font-weight: 700;
}

.public-landing-page .level-card p {
  margin: 10px 0 0;
  color: var(--muted);
  font-size: 0.94rem;
}

.public-landing-page .example-card {
  margin-top: 18px;
  padding: 28px;
}

.public-landing-page .example-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
  margin-top: 18px;
}

.public-landing-page .example-option {
  padding: 20px;
  border-radius: 18px;
  border: 1px solid var(--border);
  background: var(--bg);
}

.public-landing-page .example-option strong {
  display: block;
  margin-bottom: 8px;
  font-size: 1rem;
}

.public-landing-page .example-option p {
  margin: 0;
  color: var(--muted);
  font-size: 0.9rem;
}

.public-landing-page .process-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 14px;
  position: relative;
}

.public-landing-page .process-grid::before {
  content: "";
  position: absolute;
  top: 28px;
  left: 9%;
  right: 9%;
  height: 2px;
  background: repeating-linear-gradient(to right, var(--border) 0, var(--border) 8px, transparent 8px, transparent 18px);
}

.public-landing-page .step-card {
  position: relative;
  z-index: 1;
  padding: 0 8px;
  text-align: center;
}

.public-landing-page .step-num {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  margin-bottom: 14px;
  border-radius: 50%;
  background: var(--accent);
  color: #fff;
  font-family: var(--font-display);
  font-size: 1.12rem;
  font-weight: 700;
}

.public-landing-page .step-card p {
  margin: 8px 0 0;
  color: var(--muted);
  font-size: 0.9rem;
}

.public-landing-page .pricing-shell {
  border: 1px solid var(--border);
  border-radius: 28px;
  background: linear-gradient(180deg, #fffaf5 0%, var(--surface) 100%);
  padding: 38px;
}

.public-landing-page .price-head {
  max-width: 720px;
  text-align: center;
  margin: 0 auto 22px;
}

.public-landing-page .price-value {
  margin: 14px 0 0;
  font-family: var(--font-display);
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 400;
  line-height: 1;
  letter-spacing: -0.04em;
}

.public-landing-page .offer-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
  margin-top: 24px;
}

.public-landing-page .offer-group {
  padding: 24px;
  border-radius: 22px;
  border: 1px solid var(--border);
  background: var(--surface);
}

.public-landing-page .offer-group h3 {
  margin: 0;
  font-family: var(--font-display);
  font-size: 1.12rem;
  letter-spacing: -0.02em;
}

.public-landing-page .offer-group p {
  margin: 10px 0 0;
  color: var(--muted);
  font-size: 0.92rem;
}

.public-landing-page .offer-group ul {
  margin-top: 14px;
}

.public-landing-page .pricing-actions {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 14px;
  margin-top: 28px;
}

.public-landing-page .pricing-note {
  max-width: 720px;
  text-align: center;
  color: var(--muted);
  font-size: 0.92rem;
}

.public-landing-page .community-grid {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.public-landing-page .community-card {
  padding: 24px;
  border: 1px solid var(--border);
  border-radius: 22px;
  background: var(--surface);
}

.public-landing-page .community-card p {
  margin: 10px 0 0;
  color: var(--muted);
  font-size: 0.92rem;
}

.public-landing-page .limits-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.public-landing-page .limit-card {
  padding: 28px;
}

.public-landing-page .limit-card.bad {
  background: #fffaf6;
}

.public-landing-page .limit-card.good {
  background: linear-gradient(180deg, #fffefc 0%, #f8f3eb 100%);
}

.public-landing-page .limit-card h3 {
  margin: 0;
  font-family: var(--font-display);
  font-size: 1.2rem;
  letter-spacing: -0.02em;
}

.public-landing-page .limit-list {
  margin-top: 14px;
}

.public-landing-page .faq-list {
  display: grid;
  gap: 10px;
}

.public-landing-page .faq-item {
  border: 1px solid var(--border);
  border-radius: 20px;
  background: var(--surface);
  overflow: hidden;
}

.public-landing-page .faq-item summary {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 22px 24px;
  cursor: pointer;
  list-style: none;
}

.public-landing-page .faq-item summary::-webkit-details-marker { display: none; }

.public-landing-page .faq-item summary::after {
  content: "+";
  margin-left: auto;
  color: var(--muted);
  font-size: 1.2rem;
  font-family: var(--font-mono);
}

.public-landing-page .faq-item[open] summary::after { content: "−"; }

.public-landing-page .faq-item p {
  margin: 0;
  padding: 0 24px 22px 42px;
  color: var(--muted);
  font-size: 0.94rem;
}

.public-landing-page .final-cta {
  text-align: center;
  padding: 38px 30px;
  border-radius: 28px;
  border: 1px solid var(--border);
  background: linear-gradient(180deg, #fff7f1 0%, var(--surface) 100%);
}

.public-landing-page .final-cta p {
  max-width: 700px;
  margin: 14px auto 0;
  color: var(--muted);
}

.public-landing-page .final-actions {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 24px;
}

.public-landing-page .footer {
  padding: 42px 0 56px;
  border-top: 1px solid var(--border);
}

.public-landing-page .footer-inner {
  display: grid;
  gap: 8px;
  color: var(--muted);
  font-size: 0.86rem;
}

.public-landing-page .footer-title {
  color: var(--fg);
  font-family: var(--font-display);
  font-size: 1rem;
  font-weight: 700;
}

.public-landing-page .reveal {
  opacity: 0;
  transform: translateY(18px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}

.public-landing-page .reveal.is-visible {
  opacity: 1;
  transform: none;
}

@media (max-width: 980px) {
  .hero-wrap,
  .project-layout,
  .two-column,
  .compare-grid,
  .limits-grid,
  .public-landing-page .offer-grid {
    grid-template-columns: 1fr;
  }

  .offer-grid {
    grid-template-columns: 1fr;
  }

  .triple-grid,
  .levels-grid,
  .community-grid,
  .product-strip,
  .public-landing-page .example-grid {
    grid-template-columns: 1fr 1fr;
  }

  .public-landing-page .process-grid {
    grid-template-columns: 1fr 1fr 1fr;
  }

  .public-landing-page .process-grid::before { display: none; }
}

@media (max-width: 720px) {
  .public-landing-page .container { width: min(100% - 24px, 1120px); }

  .settings-shell {
    width: min(100% - 24px, 1120px);
  }

  .settings-meta,
  .settings-form-card {
    max-width: none;
  }

  .settings-actions .button {
    width: 100%;
  }

  .course-head {
    padding: 24px 18px 28px;
  }

  .course-head .hero-bg-desktop,
  .course-head .hero-bg-desktop img {
    display: none !important;
  }

  .course-head .hero-bg-mobile {
    display: block !important;
  }

  .course-head .hero-bg-mobile img {
    position: absolute;
    left: 50%;
    top: 42%;
    width: 118vw;
    max-width: none;
    height: auto;
    transform: translate(-50%, -50%);
    opacity: 0.62;
    filter: sepia(0.04) saturate(1.45) contrast(1.45) brightness(0.86);
  }

  .course-intro {
    padding: 20px;
  }

  .pricing-shell,
  .public-landing-page .pricing-shell {
    padding: 22px;
    border-radius: 20px;
  }

  .offer-grid,
  .public-landing-page .offer-grid {
    gap: 14px;
  }

  .course-head-actions,
  .pricing-actions,
  .public-landing-page .final-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .course-head-actions .btn,
  .pricing-actions .btn {
    width: 100%;
    min-width: 0;
  }

  .course-access-badge {
    width: 100%;
  }

  .password-field {
    flex-direction: column;
  }

  .password-toggle {
    width: 100%;
    min-width: 0;
  }

  .public-landing-page .nav-inner {
    flex-direction: column;
    align-items: stretch;
    text-align: center;
  }

  .public-landing-page .nav-links {
    justify-content: center;
  }

  .public-landing-page .hero {
    padding: 24px 0 24px;
  }

  .public-landing-page .hero-bg-desktop,
  .public-landing-page .hero-bg-desktop img {
    display: none !important;
  }

  .public-landing-page .hero-bg-mobile {
    display: block !important;
  }

  .public-landing-page .hero-bg-mobile img {
    position: absolute;
    left: 50%;
    top: 42%;
    width: 118vw;
    max-width: none;
    height: auto;
    transform: translate(-50%, -50%);
    opacity: 0.62;
    filter: sepia(0.04) saturate(1.45) contrast(1.45) brightness(0.86);
  }

  .top-nav {
    padding: 10px 12px;
    gap: 10px;
  }

  .top-nav .nav-inner {
    width: 100%;
    gap: 10px;
  }

  .top-nav .nav-brand-row {
    flex-direction: column;
    align-items: stretch;
    gap: 8px;
  }

  .top-nav .nav-logo {
    text-align: center;
    font-size: 1.08rem;
    line-height: 1.1;
  }

  .top-nav .nav-account-compact {
    width: 100%;
    text-align: center;
    align-items: center;
  }

  .top-nav .nav-links {
    width: 100%;
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 8px;
    justify-content: stretch;
    align-items: stretch;
  }

  .top-nav .nav-links .nav-pill,
  .top-nav .nav-links a,
  .top-nav .nav-links button,
  .top-nav .nav-links .button,
  .top-nav .nav-links .logout-form {
    width: 100%;
  }

  .top-nav .nav-links .nav-pill,
  .top-nav .nav-links a,
  .top-nav .nav-links button {
    min-height: 38px;
    padding: 10px 12px;
    font-size: 0.92rem;
    line-height: 1.15;
    text-align: center;
    white-space: normal;
  }

  .top-nav .nav-form {
    width: 100%;
  }

  .top-nav .nav-form > .button {
    width: 100%;
  }

  .top-nav .nav-account-name,
  .top-nav .nav-account-email {
    max-width: 100%;
    white-space: normal;
    overflow: visible;
    text-overflow: clip;
    overflow-wrap: anywhere;
  }

  .learning-grid {
    grid-template-columns: 1fr;
  }

  .learning-column {
    padding: 18px;
  }

  .learning-button {
    width: 100%;
    align-self: stretch;
  }

  .accounts-header {
    flex-direction: column;
  }

  .accounts-builder {
    width: 100%;
    flex: 1 1 auto;
    align-items: stretch;
    justify-content: flex-start;
  }

  .accounts-builder--server {
    grid-template-columns: 1fr;
  }

  .accounts-type-field {
    min-width: 0;
    width: 100%;
    max-width: none;
  }

  .accounts-field--wide {
    grid-column: auto;
  }

  .accounts-builder .button {
    width: 100%;
  }

  .accounts-builder--server .button {
    justify-self: stretch;
    width: 100%;
  }

  .accounts-grid {
    grid-template-columns: 1fr;
  }

  .account-card {
    width: 100%;
    max-width: none;
    flex-basis: 100%;
  }

  .account-card__title-row {
    flex-direction: column;
  }

  .account-field__control {
    flex-direction: column;
    align-items: stretch;
  }

  .account-actions .button {
    width: 100%;
  }

  .account-password-row {
    flex-direction: column;
  }

  .account-password-toggle {
    width: 100%;
  }

  .account-copy-button {
    width: 100%;
  }

  .account-actions--view .button,
  .account-actions--edit .button {
    flex: 1 1 100%;
  }

  .prompts-library-header,
  .prompts-section__header {
    flex-direction: column;
    align-items: stretch;
  }

  .prompts-add-button {
    width: 100%;
  }

  .prompt-actions {
    grid-template-columns: 1fr;
  }

  .public-landing-page .hero-title {
    font-size: clamp(2rem, 10vw, 3rem);
  }

  .public-landing-page .hero-summary {
    grid-template-columns: 1fr;
  }

  .public-landing-page .hero-cards {
    margin-top: 28px;
  }

  .public-landing-page .section {
    padding: 40px 0;
  }

  .card,
  .pricing-shell,
  .team-card,
  .compare-card,
  .level-card,
  .offer-group,
  .community-card,
  .limit-card,
  .public-landing-page .final-cta {
    padding: 22px;
    border-radius: 20px;
  }

  .triple-grid,
  .levels-grid,
  .community-grid,
  .product-strip,
  .example-grid,
  .public-landing-page .process-grid {
    grid-template-columns: 1fr;
  }

  .public-landing-page .faq-item summary {
    padding: 18px 20px;
    font-size: 1.02rem;
  }

  .public-landing-page .faq-item p {
    padding: 0 20px 18px 38px;
  }

  .public-landing-page .btn {
    width: 100%;
  }
}

@media (max-width: 520px) {
  .top-nav .nav-links {
    grid-template-columns: 1fr;
  }

  .top-nav .nav-account-name,
  .top-nav .nav-account-email {
    max-width: 100%;
    overflow-wrap: anywhere;
  }

  .prompt-card {
    padding: 14px;
  }

  .prompt-textarea {
    min-height: 180px;
  }
}

@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  .public-landing-page .reveal {
    opacity: 1;
    transform: none;
    transition: none;
  }
}

body.page--landing {
  --bg: #faf6f1;
  --surface: #fffefc;
  --surface-alt: #f5ede3;
  --fg: #2a2118;
  --muted: #786a5e;
  --border: #eadfce;
  --accent: #c45c26;
  --accent-soft: rgba(196, 92, 38, 0.1);
  --accent-strong: #a84a1c;
  --success: #47644a;
  --success-soft: rgba(71, 100, 74, 0.1);
  --shadow: 0 12px 40px rgba(42, 33, 24, 0.06);
  --font-display: Georgia, "Times New Roman", "Iowan Old Style", serif;
  --font-body: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
  --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}
```

```diff
(no diff)
```


## 5. PASSWORD_TOGGLE_CURRENT_CODE

```text
source/tests/test_auth_flow.py:657:    assert 'data-password-field' in login_response.text
source/tests/test_auth_flow.py:658:    assert 'data-password-toggle' in login_response.text
source/tests/test_auth_flow.py:659:    assert 'auth-password-toggle.js' in login_response.text
source/tests/test_auth_flow.py:660:    assert 'Показать пароль' in login_response.text
source/tests/test_auth_flow.py:676:    assert 'data-password-field' in body
source/tests/test_auth_flow.py:677:    assert 'data-password-toggle' in body
source/tests/test_auth_flow.py:678:    assert 'auth-password-toggle.js' in body
source/tests/test_account_blocks_cabinet_ui.py:275:    assert accounts_section.count('aria-label="Показать пароль"') == 3
source/app/user_cabinet/templates/cabinet.html:150:                      aria-label="Показать пароль"
source/app/user_cabinet/templates/cabinet.html:201:                        aria-label="Показать пароль"
source/app/user_cabinet/templates/cabinet.html:500:          button.setAttribute("aria-label", "Показать пароль");
source/app/user_cabinet/templates/cabinet.html:561:          passwordToggle.setAttribute("aria-label", isVisible ? "Скрыть пароль" : "Показать пароль");
source/tests/test_static_assets.py:94:    assert "Показать пароль" in response.text
source/tests/test_static_assets.py:95:    assert "Скрыть пароль" in response.text
source/app/static/cabinet-local-accounts.js:232:    toggleButton.setAttribute("aria-label", account.passwordVisible ? "Скрыть пароль" : "Показать пароль");
source/app/static/cabinet-local-accounts.js:261:      toggleButton.setAttribute("aria-label", updated.passwordVisible ? "Скрыть пароль" : "Показать пароль");
source/app/static/auth-password-toggle.js:2:  document.querySelectorAll("[data-password-field]").forEach((field) => {
source/app/static/auth-password-toggle.js:3:    const input = field.querySelector("[data-password-input]");
source/app/static/auth-password-toggle.js:4:    const toggle = field.querySelector("[data-password-toggle]");
source/app/static/auth-password-toggle.js:11:      toggle.textContent = visible ? "Скрыть пароль" : "Показать пароль";
source/app/static/auth-password-toggle.js:12:      toggle.setAttribute("aria-label", visible ? "Скрыть пароль" : "Показать пароль");
source/app/auth/templates/register.html:42:          <div class="password-field" data-password-field>
source/app/auth/templates/register.html:43:            <input class="input" type="password" name="password" autocomplete="new-password" data-password-input>
source/app/auth/templates/register.html:44:            <button class="button button-secondary password-toggle" type="button" data-password-toggle aria-pressed="false" aria-label="Показать пароль">Показать пароль</button>
source/app/auth/templates/register.html:49:          <div class="password-field" data-password-field>
source/app/auth/templates/register.html:50:            <input class="input" type="password" name="repeat_password" autocomplete="new-password" data-password-input>
source/app/auth/templates/register.html:51:            <button class="button button-secondary password-toggle" type="button" data-password-toggle aria-pressed="false" aria-label="Показать пароль">Показать пароль</button>
source/app/auth/templates/register.html:64:  <script src="/static/auth-password-toggle.js" defer></script>
source/app/auth/templates/login.html:32:        <div class="password-field" data-password-field>
source/app/auth/templates/login.html:33:          <input class="input" type="password" name="password" autocomplete="current-password" data-password-input>
source/app/auth/templates/login.html:34:          <button class="button button-secondary password-toggle" type="button" data-password-toggle aria-pressed="false" aria-label="Показать пароль">Показать пароль</button>
source/app/auth/templates/login.html:46:  <script src="/static/auth-password-toggle.js" defer></script>
```


```text
git ls-files --error-unmatch source/app/static/auth-password-toggle.js || true


test -f source/app/static/auth-password-toggle.js && sed -n '1,260p' source/app/static/auth-password-toggle.js || true
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-password-field]").forEach((field) => {
    const input = field.querySelector("[data-password-input]");
    const toggle = field.querySelector("[data-password-toggle]");
    if (!input || !toggle) {
      return;
    }

    const syncToggle = () => {
      const visible = input.type === "text";
      toggle.textContent = visible ? "Скрыть пароль" : "Показать пароль";
      toggle.setAttribute("aria-label", visible ? "Скрыть пароль" : "Показать пароль");
      toggle.setAttribute("aria-pressed", String(visible));
    };

    toggle.addEventListener("click", () => {
      input.type = input.type === "password" ? "text" : "password";
      syncToggle();
    });

    syncToggle();
  });
});


git diff -- source/app/static/auth-password-toggle.js
(no diff)
```


| classification | value |
|---|---|
| referenced by tracked source | yes |
| JS file tracked | no |
| JS file exists untracked | yes |
| clean checkout risk | yes |


## 6. LANDING_TARIFF_CURRENT_CODE

### source/app/public_landing/routes.py

- tracking state: tracked

```py
"""Public landing routes."""

from decimal import Decimal
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import ChoiceLoader, FileSystemLoader

from app.auth.service import get_current_user_from_cookies
from app.core.config import get_settings
from app.tariffs.service import get_homepage_tariff, seed_initial_catalog

router = APIRouter()
LANDING_TITLE = "OpenScript — программы, боты и MVP без знаний и опыта"
LANDING_META_DESCRIPTION = (
    "OpenScript помогает людям без технического опыта создавать простые программы, "
    "боты, MVP, помощников, агентов и автоматизации под свои задачи."
)
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))
templates.env.loader = ChoiceLoader(
    [
        templates.env.loader,
        FileSystemLoader(str(Path(__file__).resolve().parents[1] / "shared" / "templates")),
    ]
)


def _template(request: Request, template_name: str, **context) -> HTMLResponse:
    settings = get_settings()
    homepage_tariff = get_homepage_tariff(settings=settings)
    if homepage_tariff is None:
        seed_initial_catalog(settings=settings)
        homepage_tariff = get_homepage_tariff(settings=settings)
    payload = {
        "request": request,
        "title": context.pop("title", "Главная"),
        "current_user": get_current_user_from_cookies(request.cookies, settings=settings),
        "homepage_tariff": homepage_tariff,
        "homepage_tariff_price_display": _format_price(homepage_tariff.price_amount_minor, homepage_tariff.currency)
        if homepage_tariff is not None
        else None,
    }
    payload.update(context)
    return templates.TemplateResponse(request, template_name, payload)


def _format_price(amount_minor: int | None, currency: str | None) -> str:
    if amount_minor is None:
        return "Цена не указана"

    amount = Decimal(int(amount_minor)) / Decimal(100)
    if amount == amount.to_integral():
        amount_text = f"{int(amount):,}".replace(",", " ")
    else:
        amount_text = f"{amount:,.2f}".replace(",", " ").replace(".", ",")

    currency_code = (currency or "RUB").upper()
    currency_suffix = "₽" if currency_code == "RUB" else currency_code
    return f"{amount_text} {currency_suffix}"


@router.get("/", response_class=HTMLResponse)
def landing_page(request: Request) -> HTMLResponse:
    return _template(
        request,
        "index.html",
        title=LANDING_TITLE,
        meta_description=LANDING_META_DESCRIPTION,
    )


@router.head("/")
def landing_head(request: Request) -> HTMLResponse:
    return landing_page(request)
```

```diff
diff --git a/source/app/public_landing/routes.py b/source/app/public_landing/routes.py
index ece9e38..8700cf1 100644
--- a/source/app/public_landing/routes.py
+++ b/source/app/public_landing/routes.py
@@ -1,5 +1,6 @@
 """Public landing routes."""
 
+from decimal import Decimal
 from pathlib import Path
 
 from fastapi import APIRouter, Request
@@ -9,8 +10,7 @@ from jinja2 import ChoiceLoader, FileSystemLoader
 
 from app.auth.service import get_current_user_from_cookies
 from app.core.config import get_settings
-from app.shared.tariff_display import get_homepage_tariff_context
-from app.tariffs.service import seed_initial_catalog
+from app.tariffs.service import get_homepage_tariff, seed_initial_catalog
 
 router = APIRouter()
 LANDING_TITLE = "OpenScript — программы, боты и MVP без знаний и опыта"
@@ -29,20 +29,38 @@ templates.env.loader = ChoiceLoader(
 
 def _template(request: Request, template_name: str, **context) -> HTMLResponse:
     settings = get_settings()
-    tariff_context = get_homepage_tariff_context(settings=settings)
-    if tariff_context["homepage_tariff"] is None:
+    homepage_tariff = get_homepage_tariff(settings=settings)
+    if homepage_tariff is None:
         seed_initial_catalog(settings=settings)
-        tariff_context = get_homepage_tariff_context(settings=settings)
+        homepage_tariff = get_homepage_tariff(settings=settings)
     payload = {
         "request": request,
         "title": context.pop("title", "Главная"),
         "current_user": get_current_user_from_cookies(request.cookies, settings=settings),
+        "homepage_tariff": homepage_tariff,
+        "homepage_tariff_price_display": _format_price(homepage_tariff.price_amount_minor, homepage_tariff.currency)
+        if homepage_tariff is not None
+        else None,
     }
-    payload.update(tariff_context)
     payload.update(context)
     return templates.TemplateResponse(request, template_name, payload)
 
 
+def _format_price(amount_minor: int | None, currency: str | None) -> str:
+    if amount_minor is None:
+        return "Цена не указана"
+
+    amount = Decimal(int(amount_minor)) / Decimal(100)
+    if amount == amount.to_integral():
+        amount_text = f"{int(amount):,}".replace(",", " ")
+    else:
+        amount_text = f"{amount:,.2f}".replace(",", " ").replace(".", ",")
+
+    currency_code = (currency or "RUB").upper()
+    currency_suffix = "₽" if currency_code == "RUB" else currency_code
+    return f"{amount_text} {currency_suffix}"
+
+
 @router.get("/", response_class=HTMLResponse)
 def landing_page(request: Request) -> HTMLResponse:
     return _template(
```


### source/app/public_landing/templates/index.html

- tracking state: tracked

```html

<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="/static/favicon.svg" type="image/svg+xml">
<link rel="shortcut icon" href="/static/favicon.svg" type="image/svg+xml">
<title>OpenScript — Первый ИИ-бот без опыта</title>
<style>
:root {
  --bg: #faf6f1;
  --surface: #fffefc;
  --surface-alt: #f5ede3;
  --fg: #2a2118;
  --muted: #786a5e;
  --border: #eadfce;
  --accent: #c45c26;
  --accent-soft: rgba(196, 92, 38, 0.1);
  --accent-strong: #a84a1c;
  --success: #47644a;
  --success-soft: rgba(71, 100, 74, 0.1);
  --shadow: 0 12px 40px rgba(42, 33, 24, 0.06);
  --font-display: Georgia, "Times New Roman", "Iowan Old Style", serif;
  --font-body: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
  --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}

*,
*::before,
*::after { box-sizing: border-box; }

html { scroll-behavior: smooth; }

body {
  margin: 0;
  padding-top: 0;
  font-family: var(--font-body);
  background: var(--bg);
  color: var(--fg);
  line-height: 1.65;
  -webkit-font-smoothing: antialiased;
}

a { color: inherit; }

.container {
  width: min(1120px, calc(100% - 32px));
  margin: 0 auto;
}

.eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-family: var(--font-mono);
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--accent);
}

.section {
  padding: 56px 0;
}

.section-header {
  max-width: 760px;
  margin: 0 auto 30px;
  text-align: center;
}

.section-header.align-left {
  margin-left: 0;
  text-align: left;
}

.section-title {
  margin: 12px 0 0;
  font-family: var(--font-display);
  font-size: clamp(1.8rem, 3.4vw, 2.9rem);
  font-weight: 400;
  line-height: 1.12;
  letter-spacing: -0.03em;
}

.section-desc {
  margin: 14px 0 0;
  font-size: 1.02rem;
  color: var(--muted);
}

.nav {
  position: relative;
  z-index: 20;
  padding: 12px 0;
  background: color-mix(in srgb, var(--bg) 88%, white 12%);
  backdrop-filter: blur(10px);
}

.nav-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 10px 18px;
  border: 1px solid var(--border);
  border-radius: 20px;
  background: rgba(255, 254, 252, 0.92);
}

.nav-logo {
  flex: 0 0 auto;
  text-decoration: none;
  font-family: var(--font-display);
  font-size: 1.18rem;
  font-weight: 700;
  letter-spacing: -0.03em;
}

.nav-links {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  flex-wrap: wrap;
  gap: 6px;
}

.nav-links a {
  text-decoration: none;
  font-size: 0.88rem;
  font-weight: 500;
  color: var(--muted);
  padding: 8px 14px;
  border-radius: 999px;
  transition: background-color 0.2s ease, color 0.2s ease;
}

.nav-links a:hover {
  background: var(--bg);
  color: var(--fg);
}

.nav-links .nav-cta {
  background: var(--accent);
  color: #fff;
}

.nav-links .nav-cta:hover {
  background: var(--accent-strong);
  color: #fff;
}

.nav-form {
  margin: 0;
}

.nav-links .nav-button {
  display: inline-flex;
  align-items: center;
  padding: 8px 14px;
  border: 0;
  background: transparent;
  font: inherit;
  cursor: pointer;
  border-radius: 999px;
  color: var(--muted);
  transition: background-color 0.2s ease, color 0.2s ease;
}

.nav-links .nav-button:hover {
  background: var(--bg);
  color: var(--fg);
}

.hero {
  position: relative;
  overflow: hidden;
  padding: 28px 0 42px;
}

.hero-wrap {
  display: block;
  position: relative;
  z-index: 2;
}

.hero-copy {
  position: relative;
  max-width: 900px;
  margin: 0 auto;
  text-align: center;
  padding: 18px 24px 20px;
  border-radius: 32px;
}

.hero-copy::before {
  content: "";
  position: absolute;
  z-index: -1;
  inset: -20px -34px;
  border-radius: 40px;
  background: radial-gradient(
    circle at 50% 45%,
    rgba(250, 246, 241, 0.78) 0%,
    rgba(250, 246, 241, 0.52) 46%,
    rgba(250, 246, 241, 0) 76%
  );
}

.hero-title {
  margin: 14px auto 0;
  font-family: var(--font-display);
  font-size: clamp(2.4rem, 5.8vw, 4.4rem);
  font-weight: 400;
  line-height: 1.02;
  letter-spacing: -0.045em;
  text-wrap: balance;
  max-width: 1000px;
}

.hero-lead {
  margin: 16px auto 0;
  max-width: 760px;
  font-size: 1.08rem;
  color: var(--muted);
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 24px;
  justify-content: center;
}

.hero-bg-visual {
  position: absolute;
  z-index: 0;
  inset: 0;
  pointer-events: none;
  user-select: none;
  overflow: hidden;
}

.hero-bg-desktop {
  display: block !important;
}

.hero-bg-mobile {
  display: none !important;
}

.hero-bg-desktop img {
  position: absolute;
  left: 50%;
  top: 33%;
  width: min(1280px, 108vw);
  max-width: none;
  height: auto;
  transform: translate(-50%, -50%);
  opacity: 0.76;
  filter: sepia(0.04) saturate(1.55) contrast(1.75) brightness(0.72);
}

.hero-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 20px;
}

.hero-badge,
.mini-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--muted);
  font-size: 0.82rem;
  font-weight: 600;
}

.hero-badge-dot,
.mini-badge-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--accent);
  flex: 0 0 auto;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 26px;
  border-radius: 999px;
  border: 1px solid transparent;
  font-size: 0.95rem;
  font-weight: 700;
  text-decoration: none;
  transition: transform 0.2s ease, background-color 0.2s ease, border-color 0.2s ease, color 0.2s ease;
}

.btn:hover { transform: translateY(-1px); }

.btn-primary {
  background: var(--accent);
  color: #fff;
}

.btn-primary:hover {
  background: var(--accent-strong);
}

.btn-secondary {
  background: var(--surface);
  border-color: var(--border);
  color: var(--fg);
}

.btn-secondary:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 24px;
  padding: 28px;
  box-shadow: var(--shadow);
}

.card.flat-shadow { box-shadow: none; }

.card-kicker {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  font-family: var(--font-mono);
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--accent);
}

.card-title {
  margin: 0;
  font-family: var(--font-display);
  font-size: 1.22rem;
  font-weight: 700;
  line-height: 1.18;
  letter-spacing: -0.02em;
}

.card-text,
.card-list,
.card-note {
  color: var(--muted);
}

.card-text {
  margin: 10px 0 0;
  font-size: 0.95rem;
}

.card-list {
  margin: 14px 0 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 10px;
}

.card-list li,
.detail-list li,
.offer-group li,
.limit-list li,
.faq-item p {
  position: relative;
  padding-left: 18px;
}

.card-list li::before,
.detail-list li::before,
.offer-group li::before,
.limit-list li::before,
.check-list li::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0.62em;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--accent);
}

.hero-cards {
  position: relative;
  z-index: 2;
  margin-top: 42px;
}

.hero-summary {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
  align-items: stretch;
}

.hero-summary .card {
  padding: 24px;
  height: 100%;
  background: rgba(255, 254, 252, 0.92);
  backdrop-filter: blur(10px);
}

.hero-summary .card-list {
  gap: 12px;
}

.hero-summary .card-list li {
  padding-left: 22px;
  font-size: 0.94rem;
}

.product-strip {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 12px;
  margin-top: 18px;
}

.strip-item {
  padding: 16px 18px;
  background: var(--surface-alt);
  border: 1px solid var(--border);
  border-radius: 18px;
}

.strip-item strong {
  display: block;
  margin-bottom: 4px;
  font-size: 0.92rem;
}

.strip-item span {
  color: var(--muted);
  font-size: 0.86rem;
}

.compare-grid,
.triple-grid,
.levels-grid,
.community-grid,
.faq-grid {
  display: grid;
  gap: 16px;
}

.compare-grid {
  grid-template-columns: 1fr 1fr;
}

.compare-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 24px;
  padding: 26px;
}

.compare-card h3,
.level-card h3,
.step-card h3,
.community-card h3,
.faq-item summary {
  margin: 0;
  font-family: var(--font-display);
  font-size: 1.18rem;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.compare-card ul,
.detail-list,
.offer-group ul,
.limit-list,
.check-list {
  margin: 14px 0 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 10px;
  color: var(--muted);
}

.check-list li {
  position: relative;
  padding-left: 18px;
}

.compare-card.now {
  background: linear-gradient(180deg, #fff8f3 0%, var(--surface) 100%);
}

.triple-grid {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.project-highlight {
  background: linear-gradient(180deg, #fff8f1 0%, #fffefc 100%);
  border: 1px solid #e8d4be;
}

.project-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.05fr) minmax(0, 0.95fr);
  gap: 18px;
}

.detail-box {
  padding: 22px;
  border-radius: 20px;
  border: 1px solid var(--border);
  background: var(--bg);
}

.detail-box h3 {
  margin: 0;
  font-family: var(--font-display);
  font-size: 1.1rem;
  letter-spacing: -0.02em;
}

.detail-list {
  margin-top: 12px;
}

.project-note {
  margin-top: 18px;
  padding: 18px 20px;
  border-radius: 20px;
  background: var(--accent-soft);
  color: var(--fg);
  font-size: 0.95rem;
}

.two-column {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.estimate-intro {
  max-width: 760px;
  margin: 0 auto 22px;
  text-align: center;
  color: var(--muted);
}

.levels-grid {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.level-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 24px;
  padding: 26px;
}

.level-meta {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  padding: 6px 12px;
  border-radius: 999px;
  background: var(--surface-alt);
  color: var(--accent);
  font-size: 0.78rem;
  font-weight: 700;
}

.level-card p {
  margin: 10px 0 0;
  color: var(--muted);
  font-size: 0.94rem;
}

.example-card {
  margin-top: 18px;
  padding: 28px;
}

.example-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
  margin-top: 18px;
}

.example-option {
  padding: 20px;
  border-radius: 18px;
  border: 1px solid var(--border);
  background: var(--bg);
}

.example-option strong {
  display: block;
  margin-bottom: 8px;
  font-size: 1rem;
}

.example-option p {
  margin: 0;
  color: var(--muted);
  font-size: 0.9rem;
}

.process-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 14px;
  position: relative;
}

.process-grid::before {
  content: "";
  position: absolute;
  top: 28px;
  left: 9%;
  right: 9%;
  height: 2px;
  background: repeating-linear-gradient(to right, var(--border) 0, var(--border) 8px, transparent 8px, transparent 18px);
}

.step-card {
  position: relative;
  z-index: 1;
  padding: 0 8px;
  text-align: center;
}

.step-num {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  margin-bottom: 14px;
  border-radius: 50%;
  background: var(--accent);
  color: #fff;
  font-family: var(--font-display);
  font-size: 1.12rem;
  font-weight: 700;
}

.step-card p {
  margin: 8px 0 0;
  color: var(--muted);
  font-size: 0.9rem;
}

.pricing-shell {
  border: 1px solid var(--border);
  border-radius: 28px;
  background: linear-gradient(180deg, #fffaf5 0%, var(--surface) 100%);
  padding: 38px;
}

.price-head {
  max-width: 720px;
  text-align: center;
  margin: 0 auto 22px;
}

.price-value {
  margin: 14px 0 0;
  font-family: var(--font-display);
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 400;
  line-height: 1;
  letter-spacing: -0.04em;
}

.offer-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
  margin-top: 24px;
}

.offer-group {
  padding: 24px;
  border-radius: 22px;
  border: 1px solid var(--border);
  background: var(--surface);
}

.offer-group h3 {
  margin: 0;
  font-family: var(--font-display);
  font-size: 1.12rem;
  letter-spacing: -0.02em;
}

.offer-group p {
  margin: 10px 0 0;
  color: var(--muted);
  font-size: 0.92rem;
}

.offer-group ul {
  margin-top: 14px;
}

.pricing-actions {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 14px;
  margin-top: 28px;
}

.pricing-note {
  max-width: 720px;
  text-align: center;
  color: var(--muted);
  font-size: 0.92rem;
}

.community-grid {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.community-card {
  padding: 24px;
  border: 1px solid var(--border);
  border-radius: 22px;
  background: var(--surface);
}

.community-card p {
  margin: 10px 0 0;
  color: var(--muted);
  font-size: 0.92rem;
}

.limits-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.limit-card {
  padding: 28px;
}

.limit-card.bad {
  background: #fffaf6;
}

.limit-card.good {
  background: linear-gradient(180deg, #fffefc 0%, #f8f3eb 100%);
}

.limit-card h3 {
  margin: 0;
  font-family: var(--font-display);
  font-size: 1.2rem;
  letter-spacing: -0.02em;
}

.limit-list {
  margin-top: 14px;
}

.faq-list {
  display: grid;
  gap: 10px;
}

.faq-item {
  border: 1px solid var(--border);
  border-radius: 20px;
  background: var(--surface);
  overflow: hidden;
}

.faq-item summary {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 22px 24px;
  cursor: pointer;
  list-style: none;
}

.faq-item summary::-webkit-details-marker { display: none; }

.faq-item summary::after {
  content: "+";
  margin-left: auto;
  color: var(--muted);
  font-size: 1.2rem;
  font-family: var(--font-mono);
}

.faq-item[open] summary::after { content: "−"; }

.faq-item p {
  margin: 0;
  padding: 0 24px 22px 42px;
  color: var(--muted);
  font-size: 0.94rem;
}

.final-cta {
  text-align: center;
  padding: 38px 30px;
  border-radius: 28px;
  border: 1px solid var(--border);
  background: linear-gradient(180deg, #fff7f1 0%, var(--surface) 100%);
}

.final-cta p {
  max-width: 700px;
  margin: 14px auto 0;
  color: var(--muted);
}

.final-actions {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 24px;
}

.footer {
  padding: 42px 0 56px;
  border-top: 1px solid var(--border);
}

.footer-inner {
  display: grid;
  gap: 8px;
  color: var(--muted);
  font-size: 0.86rem;
}

.footer-title {
  color: var(--fg);
  font-family: var(--font-display);
  font-size: 1rem;
  font-weight: 700;
}

.reveal {
  opacity: 0;
  transform: translateY(18px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}

.reveal.is-visible {
  opacity: 1;
  transform: none;
}

@media (max-width: 980px) {
  .hero-wrap,
  .project-layout,
  .two-column,
  .compare-grid,
  .limits-grid,
  .offer-grid {
    grid-template-columns: 1fr;
  }

  .triple-grid,
  .levels-grid,
  .community-grid,
  .product-strip,
  .example-grid {
    grid-template-columns: 1fr 1fr;
  }

  .process-grid {
    grid-template-columns: 1fr 1fr 1fr;
  }

  .process-grid::before { display: none; }
}

@media (max-width: 768px) {
  .container { width: min(100% - 24px, 1120px); }

  .nav-inner {
    flex-direction: column;
    align-items: stretch;
    text-align: center;
  }

  .nav-links {
    justify-content: center;
  }

  .hero {
    padding: 18px 0 28px;
  }

  .hero-bg-desktop,
  .hero-bg-desktop img {
    display: none !important;
  }

  .hero-bg-mobile {
    display: block !important;
  }

  .hero-bg-mobile img {
    position: absolute;
    left: 50%;
    top: 30%;
    width: min(560px, 138vw);
    max-width: none;
    height: auto;
    transform: translate(-50%, -50%);
    opacity: 0.76;
    filter: sepia(0.04) saturate(1.55) contrast(1.75) brightness(0.72);
  }

  .hero-copy {
    position: relative;
    padding: 16px 14px 18px;
  }

  .hero-copy::before {
    content: "";
    position: absolute;
    z-index: -1;
    inset: -12px -10px;
    border-radius: 28px;
    background: radial-gradient(
      circle at 50% 42%,
      rgba(250, 246, 241, 0.70) 0%,
      rgba(250, 246, 241, 0.42) 50%,
      rgba(250, 246, 241, 0) 76%
    );
  }

  .hero-title {
    font-size: clamp(2rem, 10vw, 3rem);
  }

  .hero-summary {
    grid-template-columns: 1fr;
  }

  .hero-cards {
    margin-top: 28px;
  }



  .section {
    padding: 40px 0;
  }

  .card,
  .pricing-shell,
  .team-card,
  .compare-card,
  .level-card,
  .offer-group,
  .community-card,
  .limit-card,
  .final-cta {
    padding: 22px;
    border-radius: 20px;
  }

  .triple-grid,
  .levels-grid,
  .community-grid,
  .product-strip,
  .example-grid,
  .process-grid {
    grid-template-columns: 1fr;
  }

  .faq-item summary {
    padding: 18px 20px;
    font-size: 1.02rem;
  }

  .faq-item p {
    padding: 0 20px 18px 38px;
  }

  .hero-actions,
  .final-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .btn {
    width: 100%;
  }
}

@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  .reveal {
    opacity: 1;
    transform: none;
    transition: none;
  }
}
</style>
</head>
<body>
{% if current_user %}
  {% set primary_cta_href = '/materials/drafts/dair-smoke-20260529/' %}
  {% set primary_cta_label = 'Перейти к обучению' %}
  {% set secondary_cta_href = '/cabinet' %}
  {% set secondary_cta_label = 'Личный кабинет' %}
{% else %}
  {% set primary_cta_href = '/login' %}
  {% set primary_cta_label = 'Начать первый проект' %}
  {% set secondary_cta_href = '#pricing' %}
  {% set secondary_cta_label = 'Посмотреть, что входит' %}
{% endif %}

<nav class="nav">
  <div class="container nav-inner">
    <a href="/" class="nav-logo">OpenScript</a>
    <div class="nav-links">
      {% if current_user %}
        <a href="/materials/drafts/dair-smoke-20260529/">Обучение</a>
        <a href="/cabinet">Личный кабинет</a>
        {% if current_user.role == 'admin' %}
          <a href="/admin">Админ-панель</a>
        {% endif %}
        <form class="nav-form" method="post" action="/logout">
          <button class="nav-button" type="submit">Выйти</button>
        </form>
      {% else %}
        <a href="#what-you-get">Что вы получите</a>
        <a href="#first-project">Первый проект</a>
        <a href="#how-it-works">Как проходит работа</a>
        <a href="#pricing">Цена</a>
        <a href="/login">Войти</a>
        <a href="{{ primary_cta_href }}" class="nav-cta">{{ primary_cta_label }}</a>
      {% endif %}
    </div>
  </div>
</nav>

<section class="hero">
  <div class="hero-bg-visual hero-bg-desktop" aria-hidden="true">
    <img src="{{ request.url_for('static', path='images/human_ai_hero_background_v2.png') }}" alt="" decoding="async" draggable="false">
  </div>
  <div class="hero-bg-visual hero-bg-mobile" aria-hidden="true">
    <img src="{{ request.url_for('static', path='images/mobile_vitruvian_NO_SQUARES_transparent.webp') }}" alt="" decoding="async" draggable="false">
  </div>
  <div class="container hero-wrap">
    <div class="hero-copy">
      <span class="eyebrow">Первый управляемый опыт с ИИ</span>
      <h1 class="hero-title">Создайте первого ИИ-бота без опыта в программировании</h1>
      <p class="hero-lead">OpenScript проводит вас через первый реальный проект с ИИ-наставником: вы создаёте рабочий инструмент, понимаете процесс разработки и получаете метод, чтобы дальше самостоятельно делать своих ботов, автоматизаций и MVP без опыта в программировании.</p>
      <div class="hero-actions">
        <a href="{{ primary_cta_href }}" class="btn btn-primary">{{ primary_cta_label }}</a>
        <a href="{{ secondary_cta_href }}" class="btn btn-secondary">{{ secondary_cta_label }}</a>
      </div>
    </div>
  </div>
  <div class="container hero-cards">
    <div class="hero-summary reveal">
      <div class="card flat-shadow" id="what-you-get">
        <span class="card-kicker">СМЫСЛ ПРОДУКТА</span>
        <h2 class="card-title">Программирование стало доступно без технической базы и больших бюджетов</h2>
        <p class="card-text">Раньше для создания бота, автоматизации или простого сервиса нужны были знания программирования, разработчик или большой бюджет. Сейчас эту работу можно делать вместе с ИИ: описать задачу, получить код, проверить результат и постепенно собирать рабочий инструмент.</p>
        <p class="card-text">OpenScript нужен, чтобы пройти этот первый путь не вслепую: создать своего первого ИИ-бота, понять принцип работы и дальше продолжать уже самостоятельно.</p>
      </div>
      <div class="card flat-shadow">
        <span class="card-kicker">ЧТО ВЫ ПОЛУЧАЕТЕ ЗА ПЕРВЫЙ МЕСЯЦ</span>
        <h2 class="card-title">Создадите своего первого ИИ-бота</h2>
        <ul class="card-list">
          <li>Пройдёте первый проект от задачи до рабочего результата;</li>
          <li>Создадите своего первого ИИ-бота;</li>
          <li>Получите подписку ChatGPT Plus на месяц;</li>
          <li>Получите сервер и окружение для старта;</li>
          <li>Научитесь ставить задачу ИИ и проверять результат;</li>
          <li>Поймёте, как продолжать уже со своей идеей.</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-header align-left">
      <span class="eyebrow">Что вы покупаете</span>
      <h2 class="section-title">Вы покупаете не курс, а первый управляемый опыт разработки</h2>
    </div>
    <div class="triple-grid reveal">
      <div class="card">
        <h3 class="card-title">Первый рабочий проект</h3>
        <p class="card-text">Вы не смотрите набор уроков и не получаете абстрактную теорию. Вы проходите реальную работу над первым ИИ-ботом и в конце получаете рабочий результат.</p>
      </div>
      <div class="card">
        <h3 class="card-title">ИИ-наставник в первом проекте</h3>
        <p class="card-text">Во время стартового проекта ИИ-наставник объясняет базовые вещи простым языком, помогает понять шаги разработки и не даёт потеряться в технических деталях.</p>
      </div>
      <div class="card">
        <h3 class="card-title">Навык для самостоятельной работы</h3>
        <p class="card-text">После первого проекта у вас остаётся не только ИИ-бот, но и понимание, как дальше ставить задачи, проверять результат и создавать другие продукты уже самостоятельно.</p>
      </div>
    </div>
  </div>
</section>

<section class="section" id="first-project">
  <div class="container">
    <div class="section-header">
      <span class="eyebrow">Ключевой блок</span>
      <h2 class="section-title">Первый проект: ИИ-бот для учёта расходов</h2>
    </div>
    <div class="card project-highlight reveal">
      <div class="project-layout">
        <div class="detail-box">
          <h3>Что делает бот</h3>
          <ul class="detail-list">
            <li>Помогает фиксировать расходы;</li>
            <li>Раскладывает траты по категориям;</li>
            <li>Показывает понятную сводку;</li>
            <li>Помогает видеть, куда уходят деньги;</li>
            <li>Становится первым примером вашего собственного ИИ-инструмента.</li>
          </ul>
        </div>
        <div class="detail-box">
          <h3>Что у вас остаётся после проекта</h3>
          <ul class="detail-list">
            <li>Рабочий ИИ-бот;</li>
            <li>Пошаговая дорожная карта;</li>
            <li>Материалы и инструкции;</li>
            <li>Понимание процесса разработки;</li>
            <li>Основа для следующих ботов, автоматизаций и MVP.</li>
          </ul>
        </div>
      </div>
      <div class="two-column" style="margin-top: 16px;">
        <div class="detail-box">
          <h3>Что вы понимаете по ходу</h3>
          <ul class="detail-list">
            <li>Как описывать задачу;</li>
            <li>Как превращать задачу в понятное ТЗ;</li>
            <li>Как разбивать работу на шаги;</li>
            <li>Как давать задания техническому ИИ-исполнителю;</li>
            <li>Как проверять результат;</li>
            <li>Как исправлять ошибки;</li>
            <li>Как не ломать проект при доработках.</li>
          </ul>
        </div>
        <div class="detail-box">
          <h3>Итог первого месяца</h3>
          <p class="card-text">В итоге вы сами создадите первого ИИ-бота и увидите весь путь его появления: от задачи и ТЗ до проверки результата. У вас останется рабочий бот, материалы, дорожная карта и главное — понимание, как дальше создавать другие продукты с помощью ИИ уже самостоятельно.</p>
        </div>
      </div>
      <div class="project-note">Задача первого проекта — не сделать вас профессиональным программистом за месяц, а дать первый управляемый опыт разработки, после которого вы понимаете принцип работы и можете двигаться дальше со своими задачами.</div>
    </div>
  </div>
</section>

<section class="section" id="how-it-works">
  <div class="container">
    <div class="section-header">
      <h2 class="section-title">Как проходит работа</h2>
      <p class="section-desc">OpenScript показывает общий принцип работы с ИИ-разработкой: вы формулируете задачу, ИИ помогает разложить её на шаги, технический ИИ-исполнитель выполняет работу, а вы проверяете результат и принимаете решения.</p>
    </div>
    <div class="process-grid reveal">
      <div class="step-card">
        <span class="step-num">1</span>
        <h3>Вы описываете задачу</h3>
        <p>Вы простыми словами объясняете, какой инструмент хотите получить и какую проблему он должен решать.</p>
      </div>
      <div class="step-card">
        <span class="step-num">2</span>
        <h3>Задача превращается в понятный план</h3>
        <p>ИИ помогает разложить задачу на шаги, выделить первую версию и убрать лишнее, чтобы проект можно было реально довести до результата.</p>
      </div>
      <div class="step-card">
        <span class="step-num">3</span>
        <h3>Технический ИИ-исполнитель делает изменения</h3>
        <p>Он пишет код, запускает проверки, возвращает отчёт и показывает, что именно было сделано.</p>
      </div>
      <div class="step-card">
        <span class="step-num">4</span>
        <h3>Вы проверяете результат</h3>
        <p>Вы смотрите, что получилось, задаёте вопросы, просите исправления и постепенно учитесь понимать, как управлять процессом.</p>
      </div>
      <div class="step-card">
        <span class="step-num">5</span>
        <h3>Вы повторяете подход на своих проектах</h3>
        <p>После стартового проекта вы можете использовать тот же принцип для своих ботов, автоматизаций и MVP.</p>
      </div>
    </div>
  </div>
</section>

<section class="section" id="pricing">
  <div class="container">
    <div class="pricing-shell reveal">
      <div class="price-head">
        <span class="eyebrow">Цена</span>
        <h2 class="section-title">Стартовый месяц OpenScript — {{ homepage_tariff_price_display }}</h2>
        <p class="section-desc">Это первый управляемый месяц, в котором вы проходите стартовый проект, получаете рабочую среду, материалы, инструкции и поддержку, чтобы начать создавать свои инструменты с ИИ.</p>
      </div>
      <div class="offer-grid">
        <div class="offer-group">
          <h3>Первый месяц</h3>
          <p>Всё, что нужно, чтобы пройти стартовый проект и не застрять на первых шагах. Подписка ChatGPT Plus входит в стоимость и остаётся у вас.</p>
          <ul>
            <li>Подписка ChatGPT Plus на месяц;</li>
            <li>Сервер и окружение для старта;</li>
            <li>Первый проект с ИИ-наставником;</li>
            <li>Дорожная карта разработки;</li>
            <li>Помощь на первых шагах.</li>
          </ul>
        </div>
        <div class="offer-group">
          <h3>Навсегда</h3>
          <p>Остаётся у вас после оплаты и помогает повторять подход уже на своих идеях.</p>
          <ul>
            <li>Доступ к материалам;</li>
            <li>Пошаговые инструкции;</li>
            <li>База команд и промптов;</li>
            <li>Правила работы с техническим ИИ-исполнителем;</li>
            <li>Дорожная карта первого проекта;</li>
            <li>Понимание, как повторять подход на своих идеях.</li>
          </ul>
        </div>
        <div class="offer-group">
          <h3>Комьюнити</h3>
          <p>Поддержка вокруг главного результата: первого проекта и навыка самостоятельной работы.</p>
          <ul>
            <li>Помощь, если застряли;</li>
            <li>Обмен идеями;</li>
            <li>Обсуждение проектов;</li>
            <li>Поиск соратников;</li>
            <li>Возможность объединяться для более крупных продуктов.</li>
          </ul>
        </div>
      </div>
      <div class="pricing-actions">
        <a href="{{ primary_cta_href }}" class="btn btn-primary">{{ primary_cta_label }}</a>
        <a href="{{ secondary_cta_href }}" class="btn btn-secondary">{{ secondary_cta_label }}</a>
        <p class="pricing-note">После первого месяца вы сможете продолжать самостоятельно. Продление OpenScript не обязательно, но внешние инструменты, серверы и API при необходимости оплачиваются отдельно.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-header">
      <h2 class="section-title">Комьюнити помогает не застрять и найти соратников</h2>
      <p class="section-desc">OpenScript — это не только материалы. В комьюнити можно задавать вопросы, смотреть, что делают другие, находить людей с похожими задачами и объединяться для более крупных продуктов.</p>
    </div>
    <div class="community-grid reveal">
      <div class="community-card">
        <h3>Получить помощь, если застряли</h3>
        <p>Можно быстро задать вопрос и не тратить дни на тупик, который уже проходил кто-то другой.</p>
      </div>
      <div class="community-card">
        <h3>Посмотреть примеры других участников</h3>
        <p>Чужие проекты помогают понять масштаб, уровень сложности и хорошие первые шаги.</p>
      </div>
      <div class="community-card">
        <h3>Найти соратников для задачи</h3>
        <p>Если хотите расти дальше, комьюнити помогает искать людей под совместные продукты и MVP.</p>
      </div>
      <div class="community-card">
        <h3>Продолжить развитие после первого проекта</h3>
        <p>Это не главный продукт, а поддерживающая среда вокруг вашего старта и следующих шагов.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-header">
      <span class="eyebrow">FAQ</span>
      <h2 class="section-title">Вопросы перед стартом</h2>
    </div>
    <div class="faq-list reveal">
      <details class="faq-item">
        <summary>Нужно ли уметь программировать?</summary>
        <p>Нет. OpenScript рассчитан на людей без опыта в программировании и технической разработке. Ваша задача — научиться описывать задачу, понимать шаги и проверять результат.</p>
      </details>
      <details class="faq-item">
        <summary>Это курс?</summary>
        <p>Не совсем. В OpenScript есть материалы и объяснения, но главный смысл — пройти первый реальный проект и создать своего первого ИИ-бота.</p>
      </details>
      <details class="faq-item">
        <summary>Кто объясняет, если я не понимаю?</summary>
        <p>В стартовом проекте объясняет ИИ-наставник. Он помогает идти по дорожной карте и понимать базовые вещи простым языком.</p>
      </details>
      <details class="faq-item">
        <summary>Что я получу за первый месяц?</summary>
        <p>Вы создадите первого ИИ-бота, пройдёте дорожную карту, получите материалы и поймёте, как дальше работать со своими задачами.</p>
      </details>
      <details class="faq-item">
        <summary>Смогу ли я потом продолжать без OpenScript?</summary>
        <p>Да. Цель первого месяца — дать вам метод и понимание процесса, чтобы вы могли продолжать самостоятельно. При этом внешние инструменты, серверы или API при необходимости оплачиваются отдельно.</p>
      </details>
      <details class="faq-item">
        <summary>Что входит в {{ homepage_tariff_price_display }}?</summary>
        <p>Стартовый месяц, помощь с рабочей средой, ChatGPT Plus на месяц, сервер и окружение для старта, первый проект с ИИ-наставником, материалы, инструкции и доступ к комьюнити.</p>
      </details>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="final-cta reveal">
      <span class="eyebrow">Финальный шаг</span>
      <h2 class="section-title">Начните с первого ИИ-бота — дальше сможете идти со своими идеями</h2>
      <p>OpenScript нужен, чтобы пройти стартовый барьер: создать первый рабочий инструмент, понять процесс разработки и получить метод, который можно применять дальше самостоятельно.</p>
      <div class="final-actions">
        <a href="{{ primary_cta_href }}" class="btn btn-primary">{{ primary_cta_label }}</a>
        <a href="{{ secondary_cta_href }}" class="btn btn-secondary">{{ secondary_cta_label }}</a>
      </div>
    </div>
  </div>
</section>

<footer class="footer">
  <div class="container footer-inner">
    <div class="footer-title">Юридическая информация</div>
    <div>ИП Ягофаров М.Р.</div>
    <div>ИНН: 741705866660</div>
    <div>ОГРНИП: 320745600093211</div>
    <div>Email: <a href="mailto:OpenScripts@yandex.com">OpenScripts@yandex.com</a></div>
    <div>OpenScript не гарантирует трудоустройство, не обещает стать разработчиком за месяц и не заменяет полноценную команду разработки для сложных продуктов.</div>
  </div>
</footer>

<script>
(function () {
  const revealTargets = Array.from(document.querySelectorAll(".reveal"));
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (reducedMotion || revealTargets.length === 0) {
    revealTargets.forEach((el) => el.classList.add("is-visible"));
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });

  revealTargets.forEach((el) => observer.observe(el));
})();
</script>
</body>
</html>
```

```diff
(no diff)
```


### source/app/tariffs/service.py

- tracking state: tracked

```py
"""Tariff catalog services and seed helpers."""

from __future__ import annotations

import re
import sqlite3
import secrets
from dataclasses import asdict

from app.core.config import Settings, get_settings
from app.shared.db import get_connection, get_database_path, initialize_database
from app.shared.utils import utc_now_iso

from .schemas import TariffCreateInput, TariffOptionLinkInput, TariffPublic, TariffUpdateInput


STARTER_TARIFF_CODE = "starter_4990_rub"
STARTER_TARIFF_TITLE = "Стартовый доступ"
STARTER_TARIFF_DESCRIPTION = "Базовый тариф для старта работы с сервисом."

CODE_RE = re.compile(r"^[a-z0-9_-]{3,64}$")
TITLE_MAX_LENGTH = 200
DESCRIPTION_MAX_LENGTH = 4000
INT_RE = re.compile(r"^-?\d+$")
CURRENCY_RE = re.compile(r"^[A-Z]{3}$")
ALLOWED_STATUSES = {"active", "hidden", "archived"}
_UNSET = object()


class CatalogError(Exception):
    """Base class for tariff catalog errors."""


class ValidationError(CatalogError):
    pass


class ConflictError(CatalogError):
    pass


class NotFoundError(CatalogError):
    pass


def _settings(settings: Settings | None = None) -> Settings:
    return settings or get_settings()


def _database_path(settings: Settings | None = None):
    return get_database_path(_settings(settings))


def _connection(settings: Settings | None = None):
    resolved = _settings(settings)
    path = _database_path(resolved)
    initialize_database(path)
    return get_connection(path)


def _normalize_code(value: str, field_name: str = "code") -> str:
    normalized = ("" if value is None else str(value)).strip().lower()
    if not normalized:
        raise ValidationError(f"{field_name} is required")
    if not CODE_RE.fullmatch(normalized):
        raise ValidationError(f"{field_name} must be 3-64 chars of lowercase letters, digits, underscore or hyphen")
    return normalized


def _generate_unique_code(connection, prefix: str, table_name: str) -> str:
    for _ in range(100):
        candidate = f"{prefix}{secrets.token_hex(8)}"
        row = connection.execute(f"SELECT 1 FROM {table_name} WHERE code = ?", (candidate,)).fetchone()
        if row is None:
            return candidate
    raise CatalogError("failed to generate code")


def _resolve_create_code(connection, value, *, prefix: str, table_name: str) -> tuple[str, bool]:
    raw = "" if value is None else str(value).strip().lower()
    if raw:
        return _normalize_code(raw), False
    return _generate_unique_code(connection, prefix, table_name), True


def _normalize_title(value: str) -> str:
    normalized = ("" if value is None else str(value)).strip()
    if not normalized:
        raise ValidationError("title is required")
    if len(normalized) > TITLE_MAX_LENGTH:
        raise ValidationError(f"title must be at most {TITLE_MAX_LENGTH} characters")
    return normalized


def _normalize_description(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = str(value).strip()
    if not normalized:
        return None
    if len(normalized) > DESCRIPTION_MAX_LENGTH:
        raise ValidationError(f"description must be at most {DESCRIPTION_MAX_LENGTH} characters")
    return normalized


def _normalize_currency(value: str | None) -> str:
    normalized = "RUB" if value is None else str(value).strip().upper()
    if not CURRENCY_RE.fullmatch(normalized):
        raise ValidationError("currency must be a 3-letter uppercase code")
    return normalized


def _normalize_status(value: str | None) -> str:
    normalized = "active" if value is None else str(value).strip().lower()
    if normalized not in ALLOWED_STATUSES:
        raise ValidationError("status must be active, hidden, or archived")
    return normalized


def _normalize_int(value, field_name: str, *, allow_none: bool = False, minimum: int = 0) -> int | None:
    if value is None:
        if allow_none:
            return None
        raise ValidationError(f"{field_name} is required")
    if isinstance(value, bool):
        raise ValidationError(f"{field_name} must be an integer")
    if isinstance(value, int):
        normalized = value
    else:
        raw = str(value).strip()
        if not INT_RE.fullmatch(raw):
            raise ValidationError(f"{field_name} must be an integer")
        normalized = int(raw)
    if normalized < minimum:
        raise ValidationError(f"{field_name} must be >= {minimum}")
    return normalized


def _normalize_boolish(value, field_name: str) -> int:
    if isinstance(value, bool):
        return 1 if value else 0
    if isinstance(value, int) and value in {0, 1}:
        return value
    raw = str(value).strip().lower()
    if raw in {"1", "true", "yes", "on"}:
        return 1
    if raw in {"0", "false", "no", "off"}:
        return 0
    raise ValidationError(f"{field_name} must be a boolean")


def _tariff_from_row(row) -> TariffPublic:
    return TariffPublic(
        id=int(row["id"]),
        code=str(row["code"]),
        title=str(row["title"]),
        description=row["description"],
        price_amount_minor=int(row["price_amount_minor"]),
        currency=str(row["currency"]),
        status=str(row["status"]),
        show_on_homepage=bool(row["show_on_homepage"]),
        sort_order=int(row["sort_order"]),
        created_at=str(row["created_at"]),
        updated_at=str(row["updated_at"]),
    )


def _tariff_row_is_visible(row, include_hidden: bool, include_archived: bool) -> bool:
    status = str(row["status"])
    if status == "hidden" and not include_hidden:
        return False
    if status == "archived" and not include_archived:
        return False
    return True


def _lookup_tariff_row(
    connection,
    code: str,
    *,
    include_hidden: bool = True,
    include_archived: bool = True,
):
    normalized_code = ("" if code is None else str(code)).strip().lower()
    if not normalized_code:
        return None
    row = connection.execute("SELECT * FROM tariffs WHERE code = ?", (normalized_code,)).fetchone()
    if row is None or not _tariff_row_is_visible(row, include_hidden, include_archived):
        return None
    return row


def _paid_option_row_from_link(row) -> dict:
    payload = dict(row)
    payload["is_renewable"] = bool(payload["is_renewable"])
    return payload


def _linked_option_rows(
    connection,
    tariff_id: int,
    *,
    include_hidden: bool = False,
    include_archived: bool = False,
) -> list[dict]:
    statuses = ["active"]
    if include_hidden:
        statuses.append("hidden")
    if include_archived:
        statuses.append("archived")
    placeholders = ",".join("?" for _ in statuses)
    rows = connection.execute(
        f"""
        SELECT
            po.*,
            topt.included_duration_days,
            topt.included_quantity,
            topt.created_at AS link_created_at
        FROM tariff_options AS topt
        JOIN paid_options AS po ON po.id = topt.option_id
        WHERE topt.tariff_id = ?
          AND po.status IN ({placeholders})
        ORDER BY po.sort_order ASC, po.id ASC, po.code ASC
        """,
        (tariff_id, *statuses),
    ).fetchall()
    return [_paid_option_row_from_link(row) for row in rows]


def _lookup_paid_option_row(
    connection,
    code: str,
    *,
    include_hidden: bool = True,
    include_archived: bool = True,
):
    normalized_code = ("" if code is None else str(code)).strip().lower()
    if not normalized_code:
        return None
    row = connection.execute("SELECT * FROM paid_options WHERE code = ?", (normalized_code,)).fetchone()
    if row is None:
        return None
    status = str(row["status"])
    if status == "hidden" and not include_hidden:
        return None
    if status == "archived" and not include_archived:
        return None
    return row


def _lookup_link_row(connection, tariff_id: int, option_id: int):
    return connection.execute(
        """
        SELECT
            po.*,
            topt.included_duration_days,
            topt.included_quantity,
            topt.created_at AS link_created_at
        FROM tariff_options AS topt
        JOIN paid_options AS po ON po.id = topt.option_id
        WHERE topt.tariff_id = ? AND topt.option_id = ?
        """,
        (tariff_id, option_id),
    ).fetchone()


def _coerce_create_payload(
    data: TariffCreateInput | None,
    *,
    code: str | None,
    title: str | None,
    description: str | None,
    price_amount_minor,
    currency: str | None,
    status: str | None,
    show_on_homepage,
    sort_order,
) -> dict:
    if data is not None:
        if any(value is not None for value in (code, title, description, price_amount_minor, currency, status, show_on_homepage, sort_order)):
            raise ValidationError("pass either data or keyword arguments, not both")
        return asdict(data)
    return {
        "code": code,
        "title": title,
        "description": description,
        "price_amount_minor": price_amount_minor,
        "currency": currency,
        "status": status,
        "show_on_homepage": show_on_homepage,
        "sort_order": sort_order,
    }


def _coerce_update_payload(
    data: TariffUpdateInput | None,
    *,
    title,
    description,
    price_amount_minor,
    currency,
    status,
    show_on_homepage,
    sort_order,
) -> dict:
    if data is not None:
        if any(value is not _UNSET for value in (title, description, price_amount_minor, currency, status, show_on_homepage, sort_order)):
            raise ValidationError("pass either data or keyword arguments, not both")
        return asdict(data)
    return {
        "title": title,
        "description": description,
        "price_amount_minor": price_amount_minor,
        "currency": currency,
        "status": status,
        "show_on_homepage": show_on_homepage,
        "sort_order": sort_order,
    }


def _coerce_link_payload(
    data: TariffOptionLinkInput | None,
    *,
    included_duration_days,
    included_quantity,
) -> dict:
    if data is not None:
        if any(value is not _UNSET for value in (included_duration_days, included_quantity)):
            raise ValidationError("pass either data or keyword arguments, not both")
        return asdict(data)
    return {
        "included_duration_days": included_duration_days,
        "included_quantity": included_quantity,
    }


def list_tariffs(
    include_hidden: bool = False,
    include_archived: bool = False,
    settings: Settings | None = None,
) -> list[TariffPublic]:
    statuses = ["active"]
    if include_hidden:
        statuses.append("hidden")
    if include_archived:
        statuses.append("archived")
    placeholders = ",".join("?" for _ in statuses)
    with _connection(settings) as connection:
        rows = connection.execute(
            f"SELECT * FROM tariffs WHERE status IN ({placeholders}) ORDER BY sort_order ASC, id ASC, code ASC",
            tuple(statuses),
        ).fetchall()
        return [_tariff_from_row(row) for row in rows]


def list_tariffs_for_admin(settings: Settings | None = None) -> list[TariffPublic]:
    return list_tariffs(include_hidden=True, include_archived=True, settings=settings)


def get_tariff_by_code(code: str, settings: Settings | None = None) -> TariffPublic | None:
    with _connection(settings) as connection:
        row = connection.execute("SELECT * FROM tariffs WHERE code = ?", ((code or "").strip().lower(),)).fetchone()
        return _tariff_from_row(row) if row else None


def get_tariff_with_options(
    code: str,
    include_hidden: bool = False,
    include_archived: bool = False,
    settings: Settings | None = None,
) -> dict:
    normalized_code = _normalize_code(code)
    with _connection(settings) as connection:
        tariff_row = _lookup_tariff_row(
            connection,
            normalized_code,
            include_hidden=include_hidden,
            include_archived=include_archived,
        )
        if tariff_row is None:
            raise NotFoundError("tariff not found")
        return {
            "tariff": _tariff_from_row(tariff_row),
            "options": _linked_option_rows(
                connection,
                int(tariff_row["id"]),
                include_hidden=include_hidden,
                include_archived=include_archived,
            ),
        }


def create_tariff(
    *,
    data: TariffCreateInput | None = None,
    code: str | None = None,
    title: str | None = None,
    description: str | None = None,
    price_amount_minor=None,
    currency: str | None = None,
    status: str | None = None,
    show_on_homepage=None,
    sort_order=None,
    settings: Settings | None = None,
) -> TariffPublic:
    payload = _coerce_create_payload(
        data,
        code=code,
        title=title,
        description=description,
        price_amount_minor=price_amount_minor,
        currency=currency,
        status=status,
        show_on_homepage=show_on_homepage,
        sort_order=sort_order,
    )
    normalized_title = _normalize_title(payload["title"])
    normalized_description = _normalize_description(payload["description"])
    normalized_price = _normalize_int(payload["price_amount_minor"], "price_amount_minor", allow_none=False, minimum=0)
    normalized_currency = _normalize_currency("RUB" if payload["currency"] is None else payload["currency"])
    normalized_status = _normalize_status("active" if payload["status"] is None else payload["status"])
    normalized_show_on_homepage = _normalize_boolish(False if payload["show_on_homepage"] is None else payload["show_on_homepage"], "show_on_homepage")
    normalized_sort_order = _normalize_int(0 if payload["sort_order"] is None else payload["sort_order"], "sort_order", allow_none=False, minimum=0)

    resolved = _settings(settings)
    now_iso = utc_now_iso()
    with _connection(resolved) as connection:
        normalized_code, generated = _resolve_create_code(connection, payload["code"], prefix="tariff_", table_name="tariffs")
        if not generated:
            existing = connection.execute("SELECT id FROM tariffs WHERE code = ?", (normalized_code,)).fetchone()
            if existing is not None:
                raise ConflictError("tariff code already exists")
        while True:
            try:
                cursor = connection.execute(
                    """
                    INSERT INTO tariffs (
                        code, title, description, price_amount_minor, currency,
                        status, show_on_homepage, sort_order, created_at, updated_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        normalized_code,
                        normalized_title,
                        normalized_description,
                        normalized_price,
                        normalized_currency,
                        normalized_status,
                        normalized_show_on_homepage,
                        normalized_sort_order,
                        now_iso,
                        now_iso,
                    ),
                )
            except sqlite3.IntegrityError as exc:
                if not generated:
                    raise ConflictError("tariff code already exists") from exc
                normalized_code = _generate_unique_code(connection, "tariff_", "tariffs")
                continue
            row = connection.execute("SELECT * FROM tariffs WHERE id = ?", (cursor.lastrowid,)).fetchone()
            if row is None:
                raise CatalogError("tariff creation failed")
            return _tariff_from_row(row)


def update_tariff(
    code: str,
    *,
    data: TariffUpdateInput | None = None,
    title=_UNSET,
    description=_UNSET,
    price_amount_minor=_UNSET,
    currency=_UNSET,
    status=_UNSET,
    show_on_homepage=_UNSET,
    sort_order=_UNSET,
    settings: Settings | None = None,
) -> TariffPublic:
    normalized_code = _normalize_code(code)
    payload = _coerce_update_payload(
        data,
        title=title,
        description=description,
        price_amount_minor=price_amount_minor,
        currency=currency,
        status=status,
        show_on_homepage=show_on_homepage,
        sort_order=sort_order,
    )
    updates: dict[str, object] = {}
    if payload["title"] is not _UNSET:
        updates["title"] = _normalize_title(payload["title"])
    if payload["description"] is not _UNSET:
        updates["description"] = _normalize_description(payload["description"])
    if payload["price_amount_minor"] is not _UNSET:
        updates["price_amount_minor"] = _normalize_int(payload["price_amount_minor"], "price_amount_minor", minimum=0)
    if payload["currency"] is not _UNSET:
        if payload["currency"] is None:
            raise ValidationError("currency is required")
        updates["currency"] = _normalize_currency(payload["currency"])
    if payload["status"] is not _UNSET:
        if payload["status"] is None:
            raise ValidationError("status is required")
        updates["status"] = _normalize_status(payload["status"])
    if payload["show_on_homepage"] is not _UNSET and payload["show_on_homepage"] is not None:
        updates["show_on_homepage"] = _normalize_boolish(payload["show_on_homepage"], "show_on_homepage")
    if payload["sort_order"] is not _UNSET:
        updates["sort_order"] = _normalize_int(payload["sort_order"], "sort_order", minimum=0)

    resolved = _settings(settings)
    now_iso = utc_now_iso()
    with _connection(resolved) as connection:
        row = connection.execute("SELECT * FROM tariffs WHERE code = ?", (normalized_code,)).fetchone()
        if row is None:
            raise NotFoundError("tariff not found")
        if not updates:
            return _tariff_from_row(row)
        set_clause = ", ".join(f"{column} = ?" for column in updates)
        params = (*updates.values(), now_iso, normalized_code)
        connection.execute(
            f"UPDATE tariffs SET {set_clause}, updated_at = ? WHERE code = ?",
            params,
        )
        updated = connection.execute("SELECT * FROM tariffs WHERE code = ?", (normalized_code,)).fetchone()
        if updated is None:
            raise CatalogError("tariff update failed")
        return _tariff_from_row(updated)


def get_homepage_tariff(settings: Settings | None = None) -> TariffPublic | None:
    with _connection(settings) as connection:
        row = connection.execute(
            """
            SELECT *
            FROM tariffs
            WHERE status = 'active' AND show_on_homepage = 1
            ORDER BY sort_order ASC, id ASC, code ASC
            LIMIT 1
            """
        ).fetchone()
        if row is not None:
            return _tariff_from_row(row)
        fallback = connection.execute(
            """
            SELECT *
            FROM tariffs
            WHERE status = 'active'
            ORDER BY sort_order ASC, id ASC, code ASC
            LIMIT 1
            """
        ).fetchone()
        return _tariff_from_row(fallback) if fallback is not None else None


def archive_tariff(code: str, settings: Settings | None = None) -> bool:
    normalized_code = _normalize_code(code)
    now_iso = utc_now_iso()
    with _connection(settings) as connection:
        row = connection.execute("SELECT * FROM tariffs WHERE code = ?", (normalized_code,)).fetchone()
        if row is None:
            raise NotFoundError("tariff not found")
        if str(row["status"]) == "archived":
            return False
        connection.execute(
            "UPDATE tariffs SET status = ?, updated_at = ? WHERE code = ?",
            ("archived", now_iso, normalized_code),
        )
        return True


def list_tariff_options(
    tariff_code: str,
    include_hidden: bool = False,
    include_archived: bool = False,
    settings: Settings | None = None,
) -> list[dict]:
    normalized_code = (tariff_code or "").strip().lower()
    if not normalized_code:
        return []
    with _connection(settings) as connection:
        tariff_row = connection.execute("SELECT * FROM tariffs WHERE code = ?", (normalized_code,)).fetchone()
        if tariff_row is None:
            return []
        return _linked_option_rows(
            connection,
            int(tariff_row["id"]),
            include_hidden=include_hidden,
            include_archived=include_archived,
        )


def list_active_tariffs_with_options(settings: Settings | None = None) -> list[dict]:
    with _connection(settings) as connection:
        tariffs = connection.execute(
            """
            SELECT *
            FROM tariffs
            WHERE status = 'active'
            ORDER BY sort_order ASC, id ASC, code ASC
            """
        ).fetchall()
        result: list[dict] = []
        for tariff_row in tariffs:
            tariff_payload = dict(tariff_row)
            tariff_payload["options"] = _linked_option_rows(
                connection,
                int(tariff_row["id"]),
                include_hidden=False,
                include_archived=False,
            )
            result.append(tariff_payload)
        return result


def _upsert_tariff_option_link(
    connection,
    tariff_row,
    option_row,
    *,
    included_duration_days: int | None,
    included_quantity: int | None,
) -> dict:
    existing = _lookup_link_row(connection, int(tariff_row["id"]), int(option_row["id"]))
    now_iso = utc_now_iso()
    if existing is None:
        connection.execute(
            """
            INSERT INTO tariff_options (
                tariff_id, option_id, included_duration_days, included_quantity, created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                int(tariff_row["id"]),
                int(option_row["id"]),
                included_duration_days,
                included_quantity,
                now_iso,
            ),
        )
    else:
        connection.execute(
            """
            UPDATE tariff_options
            SET included_duration_days = ?, included_quantity = ?
            WHERE tariff_id = ? AND option_id = ?
            """,
            (
                included_duration_days,
                included_quantity,
                int(tariff_row["id"]),
                int(option_row["id"]),
            ),
        )
    updated = _lookup_link_row(connection, int(tariff_row["id"]), int(option_row["id"]))
    if updated is None:
        raise CatalogError("tariff option link update failed")
    return _paid_option_row_from_link(updated)


def attach_option_to_tariff(
    tariff_code: str,
    option_code: str,
    *,
    data: TariffOptionLinkInput | None = None,
    included_duration_days=_UNSET,
    included_quantity=_UNSET,
    settings: Settings | None = None,
) -> dict:
    payload = _coerce_link_payload(
        data,
        included_duration_days=included_duration_days,
        included_quantity=included_quantity,
    )
    normalized_duration = None if payload["included_duration_days"] is _UNSET else _normalize_int(
        payload["included_duration_days"],
        "included_duration_days",
        allow_none=True,
        minimum=0,
    )
    normalized_quantity = None if payload["included_quantity"] is _UNSET else _normalize_int(
        payload["included_quantity"],
        "included_quantity",
        allow_none=True,
        minimum=0,
    )
    normalized_tariff_code = _normalize_code(tariff_code)
    normalized_option_code = _normalize_code(option_code)

    with _connection(settings) as connection:
        tariff_row = _lookup_tariff_row(connection, normalized_tariff_code, include_hidden=True, include_archived=True)
        if tariff_row is None:
            raise NotFoundError("tariff not found")
        if str(tariff_row["status"]) == "archived":
            raise ValidationError("archived tariff cannot be modified")
        option_row = _lookup_paid_option_row(connection, normalized_option_code, include_hidden=True, include_archived=True)
        if option_row is None:
            raise NotFoundError("paid option not found")
        if str(option_row["status"]) == "archived":
            raise ValidationError("archived paid option cannot be attached")
        return _upsert_tariff_option_link(
            connection,
            tariff_row,
            option_row,
            included_duration_days=normalized_duration,
            included_quantity=normalized_quantity,
        )


def update_tariff_option_link(
    tariff_code: str,
    option_code: str,
    *,
    data: TariffOptionLinkInput | None = None,
    included_duration_days=_UNSET,
    included_quantity=_UNSET,
    settings: Settings | None = None,
) -> dict:
    payload = _coerce_link_payload(
        data,
        included_duration_days=included_duration_days,
        included_quantity=included_quantity,
    )
    normalized_duration = None if payload["included_duration_days"] is _UNSET else _normalize_int(
        payload["included_duration_days"],
        "included_duration_days",
        allow_none=True,
        minimum=0,
    )
    normalized_quantity = None if payload["included_quantity"] is _UNSET else _normalize_int(
        payload["included_quantity"],
        "included_quantity",
        allow_none=True,
        minimum=0,
    )
    normalized_tariff_code = _normalize_code(tariff_code)
    normalized_option_code = _normalize_code(option_code)

    with _connection(settings) as connection:
        tariff_row = _lookup_tariff_row(connection, normalized_tariff_code, include_hidden=True, include_archived=True)
        if tariff_row is None:
            raise NotFoundError("tariff not found")
        option_row = _lookup_paid_option_row(connection, normalized_option_code, include_hidden=True, include_archived=True)
        if option_row is None:
            raise NotFoundError("paid option not found")
        existing = _lookup_link_row(connection, int(tariff_row["id"]), int(option_row["id"]))
        if existing is None:
            raise NotFoundError("tariff option link not found")
        normalized_duration = (
            existing["included_duration_days"]
            if payload["included_duration_days"] is _UNSET
            else _normalize_int(payload["included_duration_days"], "included_duration_days", allow_none=True, minimum=0)
        )
        normalized_quantity = (
            existing["included_quantity"]
            if payload["included_quantity"] is _UNSET
            else _normalize_int(payload["included_quantity"], "included_quantity", allow_none=True, minimum=0)
        )
        return _upsert_tariff_option_link(
            connection,
            tariff_row,
            option_row,
            included_duration_days=normalized_duration,
            included_quantity=normalized_quantity,
        )


def detach_option_from_tariff(
    tariff_code: str,
    option_code: str,
    settings: Settings | None = None,
) -> bool:
    normalized_tariff_code = _normalize_code(tariff_code)
    normalized_option_code = _normalize_code(option_code)
    with _connection(settings) as connection:
        tariff_row = _lookup_tariff_row(connection, normalized_tariff_code, include_hidden=True, include_archived=True)
        if tariff_row is None:
            raise NotFoundError("tariff not found")
        option_row = _lookup_paid_option_row(connection, normalized_option_code, include_hidden=True, include_archived=True)
        if option_row is None:
            raise NotFoundError("paid option not found")
        cursor = connection.execute(
            "DELETE FROM tariff_options WHERE tariff_id = ? AND option_id = ?",
            (int(tariff_row["id"]), int(option_row["id"])),
        )
        return cursor.rowcount > 0


def upsert_tariff(
    *,
    code: str,
    title: str,
    price_amount_minor: int,
    currency: str = "RUB",
    description: str | None = None,
    status: str = "active",
    show_on_homepage: bool = False,
    sort_order: int = 0,
    settings: Settings | None = None,
) -> TariffPublic:
    normalized_code = (code or "").strip().lower()
    with _connection(settings) as connection:
        row = connection.execute("SELECT * FROM tariffs WHERE code = ?", (normalized_code,)).fetchone()
        if row is not None:
            return _tariff_from_row(row)
    return create_tariff(
        code=code,
        title=title,
        price_amount_minor=price_amount_minor,
        currency=currency,
        description=description,
        status=status,
        show_on_homepage=show_on_homepage,
        sort_order=sort_order,
        settings=settings,
    )


def seed_initial_catalog(database_path: str | None = None, settings: Settings | None = None) -> None:
    resolved = _settings(settings)
    path = database_path or str(_database_path(resolved))
    initialize_database(path)
    with get_connection(path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        now_iso = utc_now_iso()

        def upsert_option(
            code: str,
            title: str,
            description: str | None = None,
            price_amount_minor: int | None = None,
            default_duration_days: int | None = None,
            status: str = "active",
            is_renewable: int = 1,
            sort_order: int = 0,
        ) -> None:
            normalized_code = code.strip().lower()
            row = connection.execute("SELECT * FROM paid_options WHERE code = ?", (normalized_code,)).fetchone()
            if row is None:
                connection.execute(
                    """
                    INSERT INTO paid_options (
                        code, title, description, price_amount_minor, currency,
                        default_duration_days, status, is_renewable, sort_order,
                        created_at, updated_at
                    )
                    VALUES (?, ?, ?, ?, 'RUB', ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        normalized_code,
                        title,
                        description,
                        price_amount_minor,
                        default_duration_days,
                        status,
                        is_renewable,
                        sort_order,
                        now_iso,
                        now_iso,
                    ),
                )

        upsert_tariff(
            code=STARTER_TARIFF_CODE,
            title=STARTER_TARIFF_TITLE,
            description=STARTER_TARIFF_DESCRIPTION,
            price_amount_minor=499000,
            currency="RUB",
            status="active",
            show_on_homepage=True,
            sort_order=0,
            settings=resolved,
        )
        upsert_option(
            code="ai_gpt_tool",
            title="AI / GPT-инструмент",
            description="Базовый AI-инструмент для старта.",
            price_amount_minor=None,
            default_duration_days=None,
            status="active",
            is_renewable=1,
            sort_order=0,
        )
        upsert_option(
            code="server",
            title="Сервер",
            description="Серверная часть для базового рабочего окружения.",
            price_amount_minor=None,
            default_duration_days=None,
            status="active",
            is_renewable=1,
            sort_order=1,
        )
        upsert_option(
            code="vpn",
            title="VPN",
            description="Защищённый доступ для рабочих задач.",
            price_amount_minor=None,
            default_duration_days=None,
            status="active",
            is_renewable=1,
            sort_order=2,
        )
        _ensure_tariff_option_link(connection, STARTER_TARIFF_CODE, "ai_gpt_tool")
        _ensure_tariff_option_link(connection, STARTER_TARIFF_CODE, "server")
        _ensure_tariff_option_link(connection, STARTER_TARIFF_CODE, "vpn")


def _ensure_tariff_option_link(
    connection,
    tariff_code: str,
    option_code: str,
    included_duration_days: int | None = None,
    included_quantity: int | None = None,
) -> None:
    tariff_row = connection.execute("SELECT * FROM tariffs WHERE code = ?", (tariff_code,)).fetchone()
    option_row = connection.execute("SELECT * FROM paid_options WHERE code = ?", (option_code,)).fetchone()
    if tariff_row is None or option_row is None:
        return
    existing = connection.execute(
        "SELECT id FROM tariff_options WHERE tariff_id = ? AND option_id = ?",
        (int(tariff_row["id"]), int(option_row["id"])),
    ).fetchone()
    if existing is None:
        connection.execute(
            """
            INSERT INTO tariff_options (
                tariff_id, option_id, included_duration_days, included_quantity, created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                int(tariff_row["id"]),
                int(option_row["id"]),
                included_duration_days,
                included_quantity,
                utc_now_iso(),
            ),
        )
```

```diff
diff --git a/source/app/tariffs/service.py b/source/app/tariffs/service.py
index 65a6b92..4f79a7e 100644
--- a/source/app/tariffs/service.py
+++ b/source/app/tariffs/service.py
@@ -158,6 +158,7 @@ def _tariff_from_row(row) -> TariffPublic:
         price_amount_minor=int(row["price_amount_minor"]),
         currency=str(row["currency"]),
         status=str(row["status"]),
+        show_on_homepage=bool(row["show_on_homepage"]),
         sort_order=int(row["sort_order"]),
         created_at=str(row["created_at"]),
         updated_at=str(row["updated_at"]),
@@ -272,10 +273,11 @@ def _coerce_create_payload(
     price_amount_minor,
     currency: str | None,
     status: str | None,
+    show_on_homepage,
     sort_order,
 ) -> dict:
     if data is not None:
-        if any(value is not None for value in (code, title, description, price_amount_minor, currency, status, sort_order)):
+        if any(value is not None for value in (code, title, description, price_amount_minor, currency, status, show_on_homepage, sort_order)):
             raise ValidationError("pass either data or keyword arguments, not both")
         return asdict(data)
     return {
@@ -285,6 +287,7 @@ def _coerce_create_payload(
         "price_amount_minor": price_amount_minor,
         "currency": currency,
         "status": status,
+        "show_on_homepage": show_on_homepage,
         "sort_order": sort_order,
     }
 
@@ -297,10 +300,11 @@ def _coerce_update_payload(
     price_amount_minor,
     currency,
     status,
+    show_on_homepage,
     sort_order,
 ) -> dict:
     if data is not None:
-        if any(value is not _UNSET for value in (title, description, price_amount_minor, currency, status, sort_order)):
+        if any(value is not _UNSET for value in (title, description, price_amount_minor, currency, status, show_on_homepage, sort_order)):
             raise ValidationError("pass either data or keyword arguments, not both")
         return asdict(data)
     return {
@@ -309,6 +313,7 @@ def _coerce_update_payload(
         "price_amount_minor": price_amount_minor,
         "currency": currency,
         "status": status,
+        "show_on_homepage": show_on_homepage,
         "sort_order": sort_order,
     }
 
@@ -394,6 +399,7 @@ def create_tariff(
     price_amount_minor=None,
     currency: str | None = None,
     status: str | None = None,
+    show_on_homepage=None,
     sort_order=None,
     settings: Settings | None = None,
 ) -> TariffPublic:
@@ -405,6 +411,7 @@ def create_tariff(
         price_amount_minor=price_amount_minor,
         currency=currency,
         status=status,
+        show_on_homepage=show_on_homepage,
         sort_order=sort_order,
     )
     normalized_title = _normalize_title(payload["title"])
@@ -412,6 +419,7 @@ def create_tariff(
     normalized_price = _normalize_int(payload["price_amount_minor"], "price_amount_minor", allow_none=False, minimum=0)
     normalized_currency = _normalize_currency("RUB" if payload["currency"] is None else payload["currency"])
     normalized_status = _normalize_status("active" if payload["status"] is None else payload["status"])
+    normalized_show_on_homepage = _normalize_boolish(False if payload["show_on_homepage"] is None else payload["show_on_homepage"], "show_on_homepage")
     normalized_sort_order = _normalize_int(0 if payload["sort_order"] is None else payload["sort_order"], "sort_order", allow_none=False, minimum=0)
 
     resolved = _settings(settings)
@@ -428,9 +436,9 @@ def create_tariff(
                     """
                     INSERT INTO tariffs (
                         code, title, description, price_amount_minor, currency,
-                        status, sort_order, created_at, updated_at
+                        status, show_on_homepage, sort_order, created_at, updated_at
                     )
-                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
+                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                     """,
                     (
                         normalized_code,
@@ -439,6 +447,7 @@ def create_tariff(
                         normalized_price,
                         normalized_currency,
                         normalized_status,
+                        normalized_show_on_homepage,
                         normalized_sort_order,
                         now_iso,
                         now_iso,
@@ -464,6 +473,7 @@ def update_tariff(
     price_amount_minor=_UNSET,
     currency=_UNSET,
     status=_UNSET,
+    show_on_homepage=_UNSET,
     sort_order=_UNSET,
     settings: Settings | None = None,
 ) -> TariffPublic:
@@ -475,6 +485,7 @@ def update_tariff(
         price_amount_minor=price_amount_minor,
         currency=currency,
         status=status,
+        show_on_homepage=show_on_homepage,
         sort_order=sort_order,
     )
     updates: dict[str, object] = {}
@@ -492,6 +503,8 @@ def update_tariff(
         if payload["status"] is None:
             raise ValidationError("status is required")
         updates["status"] = _normalize_status(payload["status"])
+    if payload["show_on_homepage"] is not _UNSET and payload["show_on_homepage"] is not None:
+        updates["show_on_homepage"] = _normalize_boolish(payload["show_on_homepage"], "show_on_homepage")
     if payload["sort_order"] is not _UNSET:
         updates["sort_order"] = _normalize_int(payload["sort_order"], "sort_order", minimum=0)
 
@@ -516,10 +529,19 @@ def update_tariff(
 
 
 def get_homepage_tariff(settings: Settings | None = None) -> TariffPublic | None:
-    # The current schema no longer stores a homepage flag; keep startup working
-    # by exposing the first active tariff in the existing sort order.
     with _connection(settings) as connection:
         row = connection.execute(
+            """
+            SELECT *
+            FROM tariffs
+            WHERE status = 'active' AND show_on_homepage = 1
+            ORDER BY sort_order ASC, id ASC, code ASC
+            LIMIT 1
+            """
+        ).fetchone()
+        if row is not None:
+            return _tariff_from_row(row)
+        fallback = connection.execute(
             """
             SELECT *
             FROM tariffs
@@ -528,7 +550,7 @@ def get_homepage_tariff(settings: Settings | None = None) -> TariffPublic | None
             LIMIT 1
             """
         ).fetchone()
-        return _tariff_from_row(row) if row is not None else None
+        return _tariff_from_row(fallback) if fallback is not None else None
 
 
 def archive_tariff(code: str, settings: Settings | None = None) -> bool:
@@ -773,6 +795,7 @@ def upsert_tariff(
     currency: str = "RUB",
     description: str | None = None,
     status: str = "active",
+    show_on_homepage: bool = False,
     sort_order: int = 0,
     settings: Settings | None = None,
 ) -> TariffPublic:
@@ -788,6 +811,7 @@ def upsert_tariff(
         currency=currency,
         description=description,
         status=status,
+        show_on_homepage=show_on_homepage,
         sort_order=sort_order,
         settings=settings,
     )
@@ -844,6 +868,7 @@ def seed_initial_catalog(database_path: str | None = None, settings: Settings |
             price_amount_minor=499000,
             currency="RUB",
             status="active",
+            show_on_homepage=True,
             sort_order=0,
             settings=resolved,
         )
```


### source/app/tariffs/schemas.py

- tracking state: tracked

```py
"""Tariff catalog schemas."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TariffPublic:
    id: int
    code: str
    title: str
    description: str | None
    price_amount_minor: int
    currency: str
    status: str
    show_on_homepage: bool
    sort_order: int
    created_at: str
    updated_at: str


TariffView = TariffPublic


@dataclass(frozen=True, slots=True)
class TariffCreateInput:
    title: str
    description: str | None = None
    price_amount_minor: int = 0
    currency: str = "RUB"
    status: str = "active"
    show_on_homepage: bool = False
    sort_order: int = 0
    code: str | None = None


@dataclass(frozen=True, slots=True)
class TariffUpdateInput:
    title: str | None = None
    description: str | None = None
    price_amount_minor: int | None = None
    currency: str | None = None
    status: str | None = None
    show_on_homepage: bool | None = None
    sort_order: int | None = None


@dataclass(frozen=True, slots=True)
class TariffOptionLinkInput:
    included_duration_days: int | None = None
    included_quantity: int | None = None
```

```diff
diff --git a/source/app/tariffs/schemas.py b/source/app/tariffs/schemas.py
index 83ad592..bfb076f 100644
--- a/source/app/tariffs/schemas.py
+++ b/source/app/tariffs/schemas.py
@@ -14,6 +14,7 @@ class TariffPublic:
     price_amount_minor: int
     currency: str
     status: str
+    show_on_homepage: bool
     sort_order: int
     created_at: str
     updated_at: str
@@ -29,6 +30,7 @@ class TariffCreateInput:
     price_amount_minor: int = 0
     currency: str = "RUB"
     status: str = "active"
+    show_on_homepage: bool = False
     sort_order: int = 0
     code: str | None = None
 
@@ -40,6 +42,7 @@ class TariffUpdateInput:
     price_amount_minor: int | None = None
     currency: str | None = None
     status: str | None = None
+    show_on_homepage: bool | None = None
     sort_order: int | None = None
 
 
```


### source/app/shared/db.py

- tracking state: tracked

```py
"""SQLite persistence helpers for the AI Starter Community MVP."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from app.core.config import Settings, database_path_from_settings

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    login TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user',
    is_active INTEGER NOT NULL DEFAULT 1,
    email_verified_at TEXT NULL,
    materials_access_granted_at TEXT NULL,
    access_status TEXT NOT NULL DEFAULT 'not_activated',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash TEXT UNIQUE NOT NULL,
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    revoked_at TEXT NULL
);

CREATE TABLE IF NOT EXISTS auth_tokens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash TEXT UNIQUE NOT NULL,
    token_type TEXT NOT NULL,
    target_email TEXT NULL,
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    used_at TEXT NULL,
    revoked_at TEXT NULL
);

CREATE TABLE IF NOT EXISTS email_outbox (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipient_email TEXT NOT NULL,
    subject TEXT NOT NULL,
    body_text TEXT NOT NULL,
    template_key TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'queued',
    created_at TEXT NOT NULL,
    sent_at TEXT NULL,
    error TEXT NULL
);

CREATE TABLE IF NOT EXISTS account_blocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type TEXT NOT NULL,
    title TEXT NOT NULL,
    login TEXT NOT NULL DEFAULT '',
    password_secret TEXT NOT NULL DEFAULT '',
    email TEXT NULL,
    status TEXT NOT NULL DEFAULT 'inactive',
    duration_days INTEGER NOT NULL DEFAULT 60,
    activated_at TEXT NULL,
    expires_at TEXT NULL,
    created_by_user_id INTEGER NULL REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id INTEGER NULL REFERENCES users(id) ON DELETE SET NULL,
    activated_by_user_id INTEGER NULL REFERENCES users(id) ON DELETE SET NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    CHECK (type IN ('chatgpt', 'server', 'mail')),
    CHECK (status IN ('inactive', 'active', 'expired'))
);

CREATE INDEX IF NOT EXISTS idx_account_blocks_owner_user_id ON account_blocks(owner_user_id);
CREATE INDEX IF NOT EXISTS idx_account_blocks_owner_user_type ON account_blocks(owner_user_id, type);
CREATE INDEX IF NOT EXISTS idx_account_blocks_status ON account_blocks(status);

CREATE TABLE IF NOT EXISTS tariffs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    description TEXT NULL,
    price_amount_minor INTEGER NOT NULL,
    currency TEXT NOT NULL DEFAULT 'RUB',
    status TEXT NOT NULL DEFAULT 'active',
    show_on_homepage INTEGER NOT NULL DEFAULT 0,
    sort_order INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS paid_options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    description TEXT NULL,
    price_amount_minor INTEGER NULL,
    currency TEXT NOT NULL DEFAULT 'RUB',
    default_duration_days INTEGER NULL,
    status TEXT NOT NULL DEFAULT 'active',
    is_renewable INTEGER NOT NULL DEFAULT 1,
    sort_order INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tariff_options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tariff_id INTEGER NOT NULL REFERENCES tariffs(id) ON DELETE CASCADE,
    option_id INTEGER NOT NULL REFERENCES paid_options(id) ON DELETE CASCADE,
    included_duration_days INTEGER NULL,
    included_quantity INTEGER NULL,
    created_at TEXT NOT NULL,
    UNIQUE(tariff_id, option_id)
);
"""


def get_database_path(settings: Settings | None = None) -> Path:
    return database_path_from_settings(settings)


def ensure_database_parent_exists(path: Path | str) -> Path:
    db_path = Path(path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return db_path


def get_connection(path: Path | str) -> sqlite3.Connection:
    db_path = Path(path)
    connection = sqlite3.connect(str(db_path))
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(path: Path | str) -> None:
    db_path = ensure_database_parent_exists(path)
    with sqlite3.connect(str(db_path)) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(SCHEMA_SQL)
        _ensure_users_materials_access_granted_at_column(connection)
        _ensure_tariffs_show_on_homepage_column(connection)


def _ensure_users_materials_access_granted_at_column(connection: sqlite3.Connection) -> None:
    columns = {
        row[1]
        for row in connection.execute("PRAGMA table_info(users)").fetchall()
    }
    if "materials_access_granted_at" not in columns:
        connection.execute("ALTER TABLE users ADD COLUMN materials_access_granted_at TEXT NULL")


def _ensure_tariffs_show_on_homepage_column(connection: sqlite3.Connection) -> None:
    columns = {
        row[1]
        for row in connection.execute("PRAGMA table_info(tariffs)").fetchall()
    }
    if "show_on_homepage" not in columns:
        connection.execute("ALTER TABLE tariffs ADD COLUMN show_on_homepage INTEGER NOT NULL DEFAULT 0")
```

```diff
diff --git a/source/app/shared/db.py b/source/app/shared/db.py
index ad4ecfe..c3de955 100644
--- a/source/app/shared/db.py
+++ b/source/app/shared/db.py
@@ -57,6 +57,31 @@ CREATE TABLE IF NOT EXISTS email_outbox (
     error TEXT NULL
 );
 
+CREATE TABLE IF NOT EXISTS account_blocks (
+    id INTEGER PRIMARY KEY AUTOINCREMENT,
+    owner_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
+    type TEXT NOT NULL,
+    title TEXT NOT NULL,
+    login TEXT NOT NULL DEFAULT '',
+    password_secret TEXT NOT NULL DEFAULT '',
+    email TEXT NULL,
+    status TEXT NOT NULL DEFAULT 'inactive',
+    duration_days INTEGER NOT NULL DEFAULT 60,
+    activated_at TEXT NULL,
+    expires_at TEXT NULL,
+    created_by_user_id INTEGER NULL REFERENCES users(id) ON DELETE SET NULL,
+    updated_by_user_id INTEGER NULL REFERENCES users(id) ON DELETE SET NULL,
+    activated_by_user_id INTEGER NULL REFERENCES users(id) ON DELETE SET NULL,
+    created_at TEXT NOT NULL,
+    updated_at TEXT NOT NULL,
+    CHECK (type IN ('chatgpt', 'server', 'mail')),
+    CHECK (status IN ('inactive', 'active', 'expired'))
+);
+
+CREATE INDEX IF NOT EXISTS idx_account_blocks_owner_user_id ON account_blocks(owner_user_id);
+CREATE INDEX IF NOT EXISTS idx_account_blocks_owner_user_type ON account_blocks(owner_user_id, type);
+CREATE INDEX IF NOT EXISTS idx_account_blocks_status ON account_blocks(status);
+
 CREATE TABLE IF NOT EXISTS tariffs (
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     code TEXT UNIQUE NOT NULL,
@@ -65,6 +90,7 @@ CREATE TABLE IF NOT EXISTS tariffs (
     price_amount_minor INTEGER NOT NULL,
     currency TEXT NOT NULL DEFAULT 'RUB',
     status TEXT NOT NULL DEFAULT 'active',
+    show_on_homepage INTEGER NOT NULL DEFAULT 0,
     sort_order INTEGER NOT NULL DEFAULT 0,
     created_at TEXT NOT NULL,
     updated_at TEXT NOT NULL
@@ -121,6 +147,7 @@ def initialize_database(path: Path | str) -> None:
         connection.execute("PRAGMA foreign_keys = ON")
         connection.executescript(SCHEMA_SQL)
         _ensure_users_materials_access_granted_at_column(connection)
+        _ensure_tariffs_show_on_homepage_column(connection)
 
 
 def _ensure_users_materials_access_granted_at_column(connection: sqlite3.Connection) -> None:
@@ -130,3 +157,12 @@ def _ensure_users_materials_access_granted_at_column(connection: sqlite3.Connect
     }
     if "materials_access_granted_at" not in columns:
         connection.execute("ALTER TABLE users ADD COLUMN materials_access_granted_at TEXT NULL")
+
+
+def _ensure_tariffs_show_on_homepage_column(connection: sqlite3.Connection) -> None:
+    columns = {
+        row[1]
+        for row in connection.execute("PRAGMA table_info(tariffs)").fetchall()
+    }
+    if "show_on_homepage" not in columns:
+        connection.execute("ALTER TABLE tariffs ADD COLUMN show_on_homepage INTEGER NOT NULL DEFAULT 0")
```


### source/app/admin/routes.py

- tracking state: tracked

```py
"""Admin dashboard routes."""

from __future__ import annotations

import re
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from app.auth.service import (
    ADMIN_USER_DEFAULT_SORT,
    ALLOWED_ADMIN_USER_ACCESS_STATUSES,
    ALLOWED_ROLES,
    ROLE_LABELS_RU,
    NotFoundError as AuthNotFoundError,
    RoleError,
    get_user_by_session_token,
    list_users_for_admin,
    set_user_materials_access,
    update_user_role,
)
from app.admin.course_export import build_course_export
from app.core.config import get_settings
from app.paid_options.schemas import PaidOptionCreateInput, PaidOptionUpdateInput
from app.paid_options.service import (
    ConflictError as PaidOptionConflictError,
    NotFoundError as PaidOptionNotFoundError,
    ValidationError as PaidOptionValidationError,
    archive_paid_option,
    create_paid_option,
    get_paid_option_by_code,
    list_paid_options,
    list_paid_options_for_admin,
    update_paid_option,
)
from app.shared.utils import page_title
from app.tariffs.schemas import TariffCreateInput, TariffUpdateInput
from app.tariffs.service import (
    ConflictError as TariffConflictError,
    NotFoundError as TariffNotFoundError,
    ValidationError as TariffValidationError,
    attach_option_to_tariff,
    archive_tariff,
    detach_option_from_tariff,
    create_tariff,
    get_tariff_by_code,
    list_tariff_options,
    list_tariffs_for_admin,
    update_tariff_option_link,
    update_tariff,
)

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))

TARIFF_CODE_RE = re.compile(r"^[a-z0-9_-]{3,64}$")
ALLOWED_TARIFF_STATUSES = {"active", "hidden", "archived"}
ADMIN_USER_SORT_OPTIONS = {"desc": "Сначала новые", "asc": "Сначала старые"}


def _admin_user_filter_error(message: str) -> PlainTextResponse:
    lowered = message.lower()
    if "role" in lowered and "unsupported" in lowered:
        text = "Выберите допустимую роль."
    elif "access status" in lowered or "status" in lowered:
        text = "Выберите допустимый статус доступа."
    elif "created sort" in lowered:
        text = "Выберите допустимый порядок сортировки."
    elif "date" in lowered:
        text = "Укажите корректную дату регистрации."
    else:
        text = "Не удалось применить фильтр."
    return PlainTextResponse(text, status_code=400)


def _parse_admin_user_date(value: str | None) -> date | None:
    raw = (value or "").strip()
    if not raw:
        return None
    return date.fromisoformat(raw)


def _parse_admin_user_filters(request: Request) -> tuple[dict[str, object], str | None]:
    query = request.query_params
    raw_role = (query.get("role") or "all").strip().lower()
    if raw_role in {"", "all"}:
        role = None
        role_value = "all"
    elif raw_role in ALLOWED_ROLES:
        role = raw_role
        role_value = raw_role
    else:
        return {}, "unsupported role"

    raw_access_status = (query.get("access_status") or "all").strip().lower()
    if raw_access_status in {"", "all"}:
        access_status = None
        access_status_value = "all"
    elif raw_access_status in ALLOWED_ADMIN_USER_ACCESS_STATUSES:
        access_status = raw_access_status
        access_status_value = raw_access_status
    else:
        return {}, "unsupported access status"

    raw_created_sort = (query.get("created_sort") or ADMIN_USER_DEFAULT_SORT).strip().lower() or ADMIN_USER_DEFAULT_SORT
    if raw_created_sort not in ADMIN_USER_SORT_OPTIONS:
        return {}, "unsupported created sort"

    try:
        created_from = _parse_admin_user_date(query.get("created_from"))
        created_to = _parse_admin_user_date(query.get("created_to"))
    except ValueError:
        return {}, "invalid date"

    return {
        "role": role,
        "access_status": access_status,
        "created_from": created_from,
        "created_to": created_to,
        "created_sort": raw_created_sort,
        "filter_role": role_value,
        "filter_access_status": access_status_value,
        "created_from_value": (query.get("created_from") or "").strip(),
        "created_to_value": (query.get("created_to") or "").strip(),
        "query_string": request.url.query,
    }, None


def _status_label(value: str) -> str:
    return {
        "active": "активен",
        "hidden": "скрыт",
        "archived": "архив",
    }.get(value, value)


def _role_error_response(message: str) -> PlainTextResponse:
    lowered = message.lower()
    if "last admin" in lowered:
        text = "Нельзя изменить роль последнего администратора."
    elif "unsupported role" in lowered:
        text = "Выберите допустимую роль."
    else:
        text = "Не удалось изменить роль пользователя."
    return PlainTextResponse(text, status_code=400)


def _admin_users_redirect(request: Request) -> RedirectResponse:
    redirect_url = "/admin/users"
    if request.url.query:
        redirect_url = f"{redirect_url}?{request.url.query}"
    return RedirectResponse(url=redirect_url, status_code=303)


def _template(request: Request, template_name: str, **context) -> HTMLResponse:
    status_code = context.pop("status_code", 200)
    payload = {"request": request, "title": context.pop("title", page_title("AI Starter Community"))}
    payload.update(context)
    return templates.TemplateResponse(request, template_name, payload, status_code=status_code)


def _admin_user_or_redirect(request: Request, settings=None):
    resolved = settings or get_settings()
    session_token = request.cookies.get(resolved.session_cookie_name)
    user = get_user_by_session_token(session_token, settings=resolved)
    if user is None:
        return None, RedirectResponse(url="/login", status_code=303)
    if user.role != "admin":
        return user, PlainTextResponse("Доступ запрещён\nУ вашей учётной записи нет прав администратора.", status_code=403)
    return user, None


def _format_minor_amount(amount_minor: int) -> str:
    amount = Decimal(amount_minor) / Decimal(100)
    return f"{amount:,.2f}".replace(",", " ").replace(".", ",")


def _format_price_input(amount_minor: int) -> str:
    amount = Decimal(amount_minor) / Decimal(100)
    text = format(amount, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def _empty_tariff_form_data() -> dict[str, str]:
    return {
        "code": "",
        "title": "",
        "description": "",
        "price_rub": "",
        "currency": "RUB",
        "status": "active",
        "show_on_homepage": "0",
        "sort_order": "0",
    }


def _tariff_form_data_from_tariff(tariff) -> dict[str, str]:
    return {
        "code": tariff.code,
        "title": tariff.title,
        "description": tariff.description or "",
        "price_rub": _format_price_input(tariff.price_amount_minor),
        "currency": tariff.currency,
        "status": tariff.status,
        "show_on_homepage": "1" if tariff.show_on_homepage else "0",
        "sort_order": str(tariff.sort_order),
    }


def _tariff_form_data_from_form(form) -> dict[str, str]:
    return {
        "code": _normalize_text(form.get("code")),
        "title": _normalize_text(form.get("title")),
        "description": _normalize_text(form.get("description")),
        "price_rub": _normalize_text(form.get("price_rub")),
        "currency": _normalize_text(form.get("currency")) or "RUB",
        "status": _normalize_text(form.get("status")) or "active",
        "show_on_homepage": "1" if _checkbox_is_true(form.get("show_on_homepage")) else "0",
        "sort_order": _normalize_text(form.get("sort_order")) or "0",
    }


def _parse_positive_money_to_minor(value: str | None) -> tuple[int | None, str | None]:
    raw = (value or "").strip()
    if not raw:
        return None, "price is required"
    raw = raw.replace(",", ".")
    try:
        amount = Decimal(raw)
    except InvalidOperation:
        return None, "price must be a valid ruble amount"
    if not amount.is_finite() or amount < 0:
        return None, "price must be a non-negative amount"
    minor = amount * Decimal(100)
    if minor != minor.to_integral_value():
        return None, "price must have at most 2 decimal places"
    return int(minor), None


def _parse_non_negative_int(value: str | None, field_name: str, default: int = 0) -> tuple[int | None, str | None]:
    raw = (value or "").strip()
    if not raw:
        return default, None
    try:
        parsed = int(raw)
    except ValueError:
        return None, f"{field_name} must be an integer"
    if parsed < 0:
        return None, f"{field_name} must be greater than or equal to 0"
    return parsed, None


def _parse_optional_non_negative_int(value: str | None, field_name: str) -> tuple[int | None, str | None]:
    raw = (value or "").strip()
    if not raw:
        return None, None
    try:
        parsed = int(raw)
    except ValueError:
        return None, f"{field_name} must be an integer"
    if parsed < 0:
        return None, f"{field_name} must be greater than or equal to 0"
    return parsed, None


def _normalize_text(value: str | None) -> str:
    return (value or "").strip()


def _tariff_form_errors_from_service(exc: Exception) -> dict[str, str]:
    message = str(exc)
    lowered = message.lower()
    if "code already exists" in lowered:
        return {"code": "Тариф с таким кодом уже существует."}
    if "code is required" in lowered or lowered.startswith("code "):
        return {"code": "Укажите системный код тарифа."}
    if lowered.startswith("title "):
        return {"title": "Укажите название тарифа."}
    if lowered.startswith("description "):
        return {"description": "Описание тарифа слишком длинное."}
    if "price_amount_minor" in lowered:
        if "at most 2 decimal places" in lowered:
            return {"price_rub": "Цена может содержать не более 2 знаков после запятой."}
        if "non-negative" in lowered:
            return {"price_rub": "Цена не может быть отрицательной."}
        return {"price_rub": "Введите корректную цену в рублях."}
    if lowered.startswith("currency "):
        return {"currency": "Валюта должна быть кодом из 3 заглавных букв."}
    if lowered.startswith("status "):
        return {"status": "Статус должен быть активен, скрыт или архив."}
    if lowered.startswith("sort_order "):
        return {"sort_order": "Порядок сортировки должен быть целым числом не меньше 0."}
    return {"form": "Не удалось сохранить тариф."}


def _validate_tariff_form_input(
    *,
    raw_code: str | None = None,
    raw_title: str | None = None,
    raw_description: str | None = None,
    raw_price_rub: str | None = None,
    raw_currency: str | None = None,
    raw_status: str | None = None,
    raw_show_on_homepage=None,
    raw_sort_order: str | None = None,
    include_code: bool = True,
) -> tuple[dict[str, object], dict[str, str]]:
    errors: dict[str, str] = {}
    code = _normalize_text(raw_code).lower()
    title = _normalize_text(raw_title)
    description = _normalize_text(raw_description) or None
    price_minor, price_error = _parse_positive_money_to_minor(raw_price_rub)
    currency = (_normalize_text(raw_currency) or "RUB").upper()
    status = (_normalize_text(raw_status) or "active").lower()
    show_on_homepage = _checkbox_is_true(raw_show_on_homepage)
    sort_order, sort_error = _parse_non_negative_int(raw_sort_order, "sort_order")

    if include_code:
        if code and not TARIFF_CODE_RE.fullmatch(code):
            errors["code"] = "Системный код тарифа должен содержать 3-64 символа: строчные латинские буквы, цифры, подчёркивание или дефис."
        elif code is None or code == "":
            code = None
    elif code == "":
        code = None
    if not title:
        errors["title"] = "Укажите название тарифа."
    elif len(title) > 200:
        errors["title"] = "Название тарифа должно быть не длиннее 200 символов."
    if description is not None and len(description) > 4000:
        errors["description"] = "Описание тарифа должно быть не длиннее 4000 символов."
    if price_error:
        if price_error == "price is required":
            errors["price_rub"] = "Укажите цену тарифа."
        elif price_error == "price must be a valid ruble amount":
            errors["price_rub"] = "Введите корректную цену в рублях."
        elif price_error == "price must be a non-negative amount":
            errors["price_rub"] = "Цена не может быть отрицательной."
        else:
            errors["price_rub"] = "Цена может содержать не более 2 знаков после запятой."
    if not re.fullmatch(r"^[A-Z]{3}$", currency):
        errors["currency"] = "Валюта должна быть кодом из 3 заглавных букв."
    if status not in ALLOWED_TARIFF_STATUSES:
        errors["status"] = "Статус должен быть активен, скрыт или архив."
    if sort_error:
        errors["sort_order"] = "Порядок сортировки должен быть целым числом не меньше 0."

    payload = {
        "code": code,
        "title": title,
        "description": description,
        "price_amount_minor": price_minor,
        "currency": currency,
        "status": status,
        "show_on_homepage": show_on_homepage,
        "sort_order": sort_order if sort_order is not None else 0,
    }
    return payload, errors


def _paid_options_for_admin(settings):
    rows = []
    for option in list_paid_options_for_admin(settings=settings):
        rows.append(
            {
                "code": option.code,
                "title": option.title,
                "description": option.description or "—",
                "price_display": "отдельная цена не задана"
                if option.price_amount_minor is None
                else _format_minor_amount(option.price_amount_minor),
                "currency": option.currency,
                "default_duration_days": "—" if option.default_duration_days is None else option.default_duration_days,
                "status_label": _status_label(option.status),
                "is_renewable": option.is_renewable,
                "sort_order": option.sort_order,
                "created_at": option.created_at,
                "updated_at": option.updated_at,
            }
        )
    return rows


def _empty_tariff_option_attach_form_data() -> dict[str, str]:
    return {
        "option_code": "",
        "included_duration_days": "",
        "included_quantity": "",
    }


def _tariff_option_form_value(value) -> str:
    if value is None:
        return ""
    return str(value)


def _tariff_option_link_rows(settings, tariff_code: str, *, link_overrides: dict[str, dict[str, str]] | None = None) -> list[dict[str, object]]:
    linked_rows = list_tariff_options(tariff_code, include_hidden=True, include_archived=True, settings=settings)
    rows: list[dict[str, object]] = []
    for link in linked_rows:
        code = str(link["code"])
        override = (link_overrides or {}).get(code, {})
        rows.append(
            {
                "code": code,
                "title": str(link["title"]),
                "status_label": _status_label(str(link["status"])),
                "included_duration_days": _tariff_option_form_value(override.get("included_duration_days", link["included_duration_days"])),
                "included_quantity": _tariff_option_form_value(override.get("included_quantity", link["included_quantity"])),
            }
        )
    return rows


def _tariff_options_page_context(
    settings,
    tariff,
    *,
    attach_form_data: dict[str, str] | None = None,
    errors: dict[str, str] | None = None,
    link_overrides: dict[str, dict[str, str]] | None = None,
) -> dict[str, object]:
    linked_options = _tariff_option_link_rows(settings, tariff.code, link_overrides=link_overrides)
    linked_codes = {option["code"] for option in linked_options}
    available_paid_options = [
        {
            "code": option.code,
            "title": option.title,
            "status_label": _status_label(option.status),
        }
        for option in list_paid_options(settings=settings)
        if option.code not in linked_codes
    ]
    return {
        "tariff": tariff,
        "linked_options": linked_options,
        "available_paid_options": available_paid_options,
        "attach_form_data": attach_form_data or _empty_tariff_option_attach_form_data(),
        "errors": errors or {},
    }


def _render_tariff_options_page(
    request: Request,
    settings,
    tariff,
    *,
    attach_form_data: dict[str, str] | None = None,
    errors: dict[str, str] | None = None,
    link_overrides: dict[str, dict[str, str]] | None = None,
    status_code: int = 200,
):
    return _template(
        request,
        "tariff_options.html",
        status_code=status_code,
        title=page_title(f"Опции тарифа: {tariff.title}"),
        **_tariff_options_page_context(
            settings,
            tariff,
            attach_form_data=attach_form_data,
            errors=errors,
            link_overrides=link_overrides,
        ),
    )


def _empty_paid_option_form_data() -> dict[str, object]:
    return {
        "code": "",
        "title": "",
        "description": "",
        "price_rub": "",
        "currency": "RUB",
        "default_duration_days": "",
        "status": "active",
        "is_renewable": True,
        "sort_order": "0",
    }


def _paid_option_form_data_from_option(option) -> dict[str, object]:
    return {
        "code": option.code,
        "title": option.title,
        "description": option.description or "",
        "price_rub": "" if option.price_amount_minor is None else _format_price_input(option.price_amount_minor),
        "currency": option.currency,
        "default_duration_days": "" if option.default_duration_days is None else str(option.default_duration_days),
        "status": option.status,
        "is_renewable": bool(option.is_renewable),
        "sort_order": str(option.sort_order),
    }


def _paid_option_form_data_from_form(form) -> dict[str, object]:
    return {
        "code": _normalize_text(form.get("code")),
        "title": _normalize_text(form.get("title")),
        "description": _normalize_text(form.get("description")),
        "price_rub": _normalize_text(form.get("price_rub")),
        "currency": _normalize_text(form.get("currency")) or "RUB",
        "default_duration_days": _normalize_text(form.get("default_duration_days")),
        "status": _normalize_text(form.get("status")) or "active",
        "is_renewable": _checkbox_is_true(form.get("is_renewable")),
        "sort_order": _normalize_text(form.get("sort_order")) or "0",
    }


def _checkbox_is_true(value) -> bool:
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return value != 0
    raw = str(value).strip().lower()
    return raw not in {"", "0", "false", "off", "no"}


def _parse_optional_money_to_minor(value: str | None) -> tuple[int | None, str | None]:
    raw = (value or "").strip()
    if not raw:
        return None, None
    raw = raw.replace(",", ".")
    try:
        amount = Decimal(raw)
    except InvalidOperation:
        return None, "price must be a valid ruble amount"
    if not amount.is_finite() or amount < 0:
        return None, "price must be a non-negative amount"
    minor = amount * Decimal(100)
    if minor != minor.to_integral_value():
        return None, "price must have at most 2 decimal places"
    return int(minor), None


def _paid_option_form_errors_from_service(exc: Exception) -> dict[str, str]:
    message = str(exc)
    lowered = message.lower()
    if "code already exists" in lowered:
        return {"code": "Платная опция с таким кодом уже существует."}
    if "code is required" in lowered or lowered.startswith("code "):
        return {"code": "Укажите системный код платной опции."}
    if lowered.startswith("title "):
        return {"title": "Укажите название платной опции."}
    if lowered.startswith("description "):
        return {"description": "Описание платной опции слишком длинное."}
    if "price_amount_minor" in lowered:
        if "at most 2 decimal places" in lowered:
            return {"price_rub": "Цена может содержать не более 2 знаков после запятой."}
        if "non-negative" in lowered:
            return {"price_rub": "Цена не может быть отрицательной."}
        return {"price_rub": "Введите корректную цену в рублях."}
    if lowered.startswith("currency "):
        return {"currency": "Валюта должна быть кодом из 3 заглавных букв."}
    if lowered.startswith("default_duration_days "):
        return {"default_duration_days": "Срок по умолчанию должен быть целым числом не меньше 0."}
    if lowered.startswith("status "):
        return {"status": "Статус должен быть активен, скрыт или архив."}
    if lowered.startswith("is_renewable "):
        return {"is_renewable": "Значение поля «Можно продлевать» некорректно."}
    if lowered.startswith("sort_order "):
        return {"sort_order": "Порядок сортировки должен быть целым числом не меньше 0."}
    return {"form": "Не удалось сохранить платную опцию."}


def _validate_paid_option_form_input(
    *,
    raw_code: str | None = None,
    raw_title: str | None = None,
    raw_description: str | None = None,
    raw_price_rub: str | None = None,
    raw_currency: str | None = None,
    raw_default_duration_days: str | None = None,
    raw_status: str | None = None,
    raw_is_renewable=None,
    raw_sort_order: str | None = None,
    include_code: bool = True,
) -> tuple[dict[str, object], dict[str, str]]:
    errors: dict[str, str] = {}
    code = _normalize_text(raw_code).lower()
    title = _normalize_text(raw_title)
    description = _normalize_text(raw_description) or None
    price_minor, price_error = _parse_optional_money_to_minor(raw_price_rub)
    currency = (_normalize_text(raw_currency) or "RUB").upper()
    default_duration_days, duration_error = _parse_optional_non_negative_int(raw_default_duration_days, "default_duration_days")
    status = (_normalize_text(raw_status) or "active").lower()
    is_renewable = _checkbox_is_true(raw_is_renewable)
    sort_order, sort_error = _parse_non_negative_int(raw_sort_order, "sort_order")

    if include_code:
        if code and not TARIFF_CODE_RE.fullmatch(code):
            errors["code"] = "Системный код платной опции должен содержать 3-64 символа: строчные латинские буквы, цифры, подчёркивание или дефис."
        elif code == "":
            code = None
    elif code == "":
        code = None
    if not title:
        errors["title"] = "Укажите название платной опции."
    elif len(title) > 200:
        errors["title"] = "Название платной опции должно быть не длиннее 200 символов."
    if description is not None and len(description) > 4000:
        errors["description"] = "Описание платной опции должно быть не длиннее 4000 символов."
    if price_error:
        if price_error == "price must be a valid ruble amount":
            errors["price_rub"] = "Введите корректную цену в рублях."
        elif price_error == "price must be a non-negative amount":
            errors["price_rub"] = "Цена не может быть отрицательной."
        else:
            errors["price_rub"] = "Цена может содержать не более 2 знаков после запятой."
    if not re.fullmatch(r"^[A-Z]{3}$", currency):
        errors["currency"] = "Валюта должна быть кодом из 3 заглавных букв."
    if duration_error:
        errors["default_duration_days"] = "Срок по умолчанию должен быть целым числом не меньше 0."
    if status not in ALLOWED_TARIFF_STATUSES:
        errors["status"] = "Статус должен быть активен, скрыт или архив."
    if sort_error:
        errors["sort_order"] = "Порядок сортировки должен быть целым числом не меньше 0."

    payload = {
        "code": code,
        "title": title,
        "description": description,
        "price_amount_minor": price_minor,
        "currency": currency,
        "default_duration_days": default_duration_days,
        "status": status,
        "is_renewable": is_renewable,
        "sort_order": sort_order if sort_order is not None else 0,
    }
    return payload, errors


def _tariffs_for_admin(settings):
    tariffs = list_tariffs_for_admin(settings=settings)
    rows = []
    for tariff in tariffs:
        linked_options = list_tariff_options(tariff.code, include_hidden=True, include_archived=True, settings=settings)
        rows.append(
            {
                "code": tariff.code,
                "title": tariff.title,
                "description": tariff.description or "—",
                "price_display": _format_minor_amount(tariff.price_amount_minor),
                "currency": tariff.currency,
                "status_label": _status_label(tariff.status),
                "show_on_homepage_label": "Да" if tariff.show_on_homepage else "Нет",
                "sort_order": tariff.sort_order,
                "included_options_summary": ", ".join(option["title"] for option in linked_options) if linked_options else "—",
                "created_at": tariff.created_at,
                "updated_at": tariff.updated_at,
            }
        )
    return rows


def _render_tariff_form(
    request: Request,
    *,
    mode: str,
    form_data: dict[str, str],
    errors: dict[str, str] | None = None,
    tariff=None,
    status_code: int = 200,
):
    is_create = mode == "create"
    return _template(
        request,
        "tariff_form.html",
        status_code=status_code,
        title=page_title("Создать тариф" if is_create else "Редактировать тариф"),
        mode=mode,
        is_create=is_create,
        tariff=tariff,
        form_data=form_data,
        errors=errors or {},
        submit_label="Создать тариф" if is_create else "Сохранить изменения",
    )


def _validate_tariff_option_link_form_input(
    *,
    raw_option_code: str | None = None,
    raw_included_duration_days: str | None = None,
    raw_included_quantity: str | None = None,
    include_option_code: bool = True,
) -> tuple[dict[str, str], dict[str, str]]:
    errors: dict[str, str] = {}
    option_code = _normalize_text(raw_option_code).lower()
    duration_days, duration_error = _parse_optional_non_negative_int(raw_included_duration_days, "included_duration_days")
    quantity, quantity_error = _parse_optional_non_negative_int(raw_included_quantity, "included_quantity")

    if include_option_code:
        if not option_code:
            errors["option_code"] = "Выберите платную опцию."
        elif not TARIFF_CODE_RE.fullmatch(option_code):
            errors["option_code"] = "Системный код платной опции должен содержать 3-64 символа: строчные латинские буквы, цифры, подчёркивание или дефис."
    if duration_error:
        errors["included_duration_days"] = "Включённый срок должен быть целым числом не меньше 0."
    if quantity_error:
        errors["included_quantity"] = "Включённое количество должно быть целым числом не меньше 0."

    payload = {
        "option_code": option_code,
        "included_duration_days": "" if duration_days is None else str(duration_days),
        "included_quantity": "" if quantity is None else str(quantity),
    }
    return payload, errors


@router.api_route("/admin", methods=["GET", "HEAD"], response_class=HTMLResponse)
def admin_dashboard(request: Request):
    settings = get_settings()
    user, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    return _template(
        request,
        "dashboard.html",
        title=page_title("Админ-панель"),
        admin_email=user.email,
        admin_login=user.login,
    )


@router.get("/admin/course-export")
def admin_course_export(request: Request):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response

    export = build_course_export()
    headers = {
        "Content-Disposition": f'attachment; filename="{export.filename}"',
    }
    return Response(content=export.content, media_type="application/zip", headers=headers)


@router.api_route("/admin/users", methods=["GET", "HEAD"], response_class=HTMLResponse)
def admin_users(request: Request):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    filters, error = _parse_admin_user_filters(request)
    if error is not None:
        return _admin_user_filter_error(error)
    return _template(
        request,
        "users.html",
        title=page_title("Пользователи"),
        users=list_users_for_admin(
            settings=settings,
            role=filters["role"],
            access_status=filters["access_status"],
            created_from=filters["created_from"],
            created_to=filters["created_to"],
            created_sort=filters["created_sort"],
        ),
        allowed_roles=ALLOWED_ROLES,
        role_labels=ROLE_LABELS_RU,
        filter_role=filters["filter_role"],
        filter_access_status=filters["filter_access_status"],
        created_from_value=filters["created_from_value"],
        created_to_value=filters["created_to_value"],
        created_sort=filters["created_sort"],
        query_string=filters["query_string"],
    )


@router.post("/admin/users/{user_id}/role")
async def admin_user_role_update(request: Request, user_id: int):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    form = await request.form()
    role = _normalize_text(form.get("role"))
    try:
        update_user_role(user_id=user_id, new_role=role, settings=settings)
    except AuthNotFoundError:
        raise HTTPException(status_code=404, detail="user not found")
    except RoleError as exc:
        return _role_error_response(str(exc))
    return _admin_users_redirect(request)


@router.post("/admin/users/{user_id}/materials-access/grant")
def admin_user_materials_access_grant(request: Request, user_id: int):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    try:
        set_user_materials_access(user_id=user_id, granted=True, settings=settings)
    except AuthNotFoundError as exc:
        raise HTTPException(status_code=404, detail="user not found") from exc
    return _admin_users_redirect(request)


@router.post("/admin/users/{user_id}/materials-access/revoke")
def admin_user_materials_access_revoke(request: Request, user_id: int):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    try:
        set_user_materials_access(user_id=user_id, granted=False, settings=settings)
    except AuthNotFoundError as exc:
        raise HTTPException(status_code=404, detail="user not found") from exc
    return _admin_users_redirect(request)


@router.api_route("/admin/tariffs", methods=["GET", "HEAD"], response_class=HTMLResponse)
def admin_tariffs(request: Request):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    return _template(
        request,
        "tariffs.html",
        title=page_title("Тарифы"),
        tariffs=_tariffs_for_admin(settings=settings),
    )


@router.api_route("/admin/tariffs/new", methods=["GET", "HEAD"], response_class=HTMLResponse)
def admin_tariffs_new(request: Request):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    return _render_tariff_form(request, mode="create", form_data=_empty_tariff_form_data())


@router.post("/admin/tariffs/new", response_class=HTMLResponse)
async def admin_tariffs_new_submit(request: Request):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response

    form = await request.form()
    payload, errors = _validate_tariff_form_input(
        raw_code=form.get("code"),
        raw_title=form.get("title"),
        raw_description=form.get("description"),
        raw_price_rub=form.get("price_rub"),
        raw_currency=form.get("currency"),
        raw_status=form.get("status"),
        raw_show_on_homepage=form.get("show_on_homepage"),
        raw_sort_order=form.get("sort_order"),
        include_code=True,
    )
    if errors:
        return _render_tariff_form(
            request,
            mode="create",
            form_data=_tariff_form_data_from_form(form),
            errors=errors,
            status_code=400,
        )

    try:
        create_tariff(data=TariffCreateInput(**payload), settings=settings)
    except TariffConflictError as exc:
        errors = _tariff_form_errors_from_service(exc)
        return _render_tariff_form(
            request,
            mode="create",
            form_data=_tariff_form_data_from_form(form),
            errors=errors,
            status_code=400,
        )
    except TariffValidationError as exc:
        errors = _tariff_form_errors_from_service(exc)
        return _render_tariff_form(
            request,
            mode="create",
            form_data=_tariff_form_data_from_form(form),
            errors=errors,
            status_code=400,
        )

    return RedirectResponse(url="/admin/tariffs", status_code=303)


@router.api_route("/admin/tariffs/{code}/edit", methods=["GET", "HEAD"], response_class=HTMLResponse)
def admin_tariffs_edit(request: Request, code: str):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response

    tariff = get_tariff_by_code(code, settings=settings)
    if tariff is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return _render_tariff_form(request, mode="edit", form_data=_tariff_form_data_from_tariff(tariff), tariff=tariff)


@router.post("/admin/tariffs/{code}/edit", response_class=HTMLResponse)
async def admin_tariffs_edit_submit(request: Request, code: str):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response

    tariff = get_tariff_by_code(code, settings=settings)
    if tariff is None:
        raise HTTPException(status_code=404, detail="Not Found")

    form = await request.form()
    payload, errors = _validate_tariff_form_input(
        raw_title=form.get("title"),
        raw_description=form.get("description"),
        raw_price_rub=form.get("price_rub"),
        raw_currency=form.get("currency"),
        raw_status=form.get("status"),
        raw_show_on_homepage=form.get("show_on_homepage"),
        raw_sort_order=form.get("sort_order"),
        include_code=False,
    )
    posted_code = _normalize_text(form.get("code")).lower()
    if posted_code and posted_code != tariff.code:
        errors["code"] = "Системный код нельзя изменить после создания."
    if errors:
        return _render_tariff_form(
            request,
            mode="edit",
            form_data={**_tariff_form_data_from_tariff(tariff), **_tariff_form_data_from_form(form)},
            tariff=tariff,
            errors=errors,
            status_code=400,
        )

    try:
        update_tariff(
            code=tariff.code,
            data=TariffUpdateInput(
                title=payload["title"],
                description=payload["description"],
                price_amount_minor=payload["price_amount_minor"],
                currency=payload["currency"],
                status=payload["status"],
                show_on_homepage=payload["show_on_homepage"],
                sort_order=payload["sort_order"],
            ),
            settings=settings,
        )
    except TariffNotFoundError:
        raise HTTPException(status_code=404, detail="Not Found")
    except (TariffConflictError, TariffValidationError) as exc:
        errors = _tariff_form_errors_from_service(exc)
        return _render_tariff_form(
            request,
            mode="edit",
            form_data={**_tariff_form_data_from_tariff(tariff), **_tariff_form_data_from_form(form)},
            tariff=tariff,
            errors=errors,
            status_code=400,
        )

    return RedirectResponse(url="/admin/tariffs", status_code=303)


@router.post("/admin/tariffs/{code}/archive")
def admin_tariffs_archive(request: Request, code: str):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    try:
        archive_tariff(code, settings=settings)
    except TariffNotFoundError:
        raise HTTPException(status_code=404, detail="Not Found")
    return RedirectResponse(url="/admin/tariffs", status_code=303)


def _tariff_option_link_errors_from_service(exc: Exception) -> dict[str, str]:
    message = str(exc)
    lowered = message.lower()
    if "archived paid option" in lowered:
        return {"option_code": "Архивные опции нельзя добавлять к тарифу."}
    if "paid option" in lowered or "option" in lowered:
        return {"option_code": "Платная опция не найдена или недоступна для добавления."}
    if "included_duration_days" in lowered:
        return {"included_duration_days": "Включённый срок должен быть целым числом не меньше 0."}
    if "included_quantity" in lowered:
        return {"included_quantity": "Включённое количество должно быть целым числом не меньше 0."}
    return {"form": "Не удалось изменить связь тарифа и опции."}


@router.api_route("/admin/tariffs/{code}/options", methods=["GET", "HEAD"], response_class=HTMLResponse)
def admin_tariff_options(request: Request, code: str):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response

    tariff = get_tariff_by_code(code, settings=settings)
    if tariff is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return _render_tariff_options_page(request, settings, tariff)


@router.post("/admin/tariffs/{code}/options/attach", response_class=HTMLResponse)
async def admin_tariff_options_attach(request: Request, code: str):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response

    tariff = get_tariff_by_code(code, settings=settings)
    if tariff is None:
        raise HTTPException(status_code=404, detail="Not Found")

    form = await request.form()
    payload, errors = _validate_tariff_option_link_form_input(
        raw_option_code=form.get("option_code"),
        raw_included_duration_days=form.get("included_duration_days"),
        raw_included_quantity=form.get("included_quantity"),
        include_option_code=True,
    )
    if errors:
        return _render_tariff_options_page(
            request,
            settings,
            tariff,
            attach_form_data=payload,
            errors=errors,
            status_code=400,
        )

    try:
        attach_option_to_tariff(
            code,
            payload["option_code"],
            included_duration_days=None if payload["included_duration_days"] == "" else int(payload["included_duration_days"]),
            included_quantity=None if payload["included_quantity"] == "" else int(payload["included_quantity"]),
            settings=settings,
        )
    except TariffNotFoundError:
        raise HTTPException(status_code=404, detail="Not Found")
    except TariffValidationError as exc:
        errors = _tariff_option_link_errors_from_service(exc)
        return _render_tariff_options_page(
            request,
            settings,
            tariff,
            attach_form_data=payload,
            errors=errors,
            status_code=400,
        )

    return RedirectResponse(url=f"/admin/tariffs/{tariff.code}/options", status_code=303)


@router.post("/admin/tariffs/{code}/options/{option_code}/update", response_class=HTMLResponse)
async def admin_tariff_options_update(request: Request, code: str, option_code: str):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response

    tariff = get_tariff_by_code(code, settings=settings)
    if tariff is None:
        raise HTTPException(status_code=404, detail="Not Found")

    form = await request.form()
    payload, errors = _validate_tariff_option_link_form_input(
        raw_included_duration_days=form.get("included_duration_days"),
        raw_included_quantity=form.get("included_quantity"),
        include_option_code=False,
    )
    if errors:
        return _render_tariff_options_page(
            request,
            settings,
            tariff,
            errors=errors,
            link_overrides={
                option_code: {
                    "included_duration_days": payload["included_duration_days"],
                    "included_quantity": payload["included_quantity"],
                }
            },
            status_code=400,
        )

    try:
        update_tariff_option_link(
            code,
            option_code,
            included_duration_days=None if payload["included_duration_days"] == "" else int(payload["included_duration_days"]),
            included_quantity=None if payload["included_quantity"] == "" else int(payload["included_quantity"]),
            settings=settings,
        )
    except TariffNotFoundError:
        raise HTTPException(status_code=404, detail="Not Found")
    except TariffValidationError as exc:
        errors = _tariff_option_link_errors_from_service(exc)
        return _render_tariff_options_page(
            request,
            settings,
            tariff,
            errors=errors,
            link_overrides={
                option_code: {
                    "included_duration_days": payload["included_duration_days"],
                    "included_quantity": payload["included_quantity"],
                }
            },
            status_code=400,
        )

    return RedirectResponse(url=f"/admin/tariffs/{tariff.code}/options", status_code=303)


@router.post("/admin/tariffs/{code}/options/{option_code}/detach")
def admin_tariff_options_detach(request: Request, code: str, option_code: str):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response

    tariff = get_tariff_by_code(code, settings=settings)
    if tariff is None:
        raise HTTPException(status_code=404, detail="Not Found")

    try:
        detached = detach_option_from_tariff(code, option_code, settings=settings)
    except TariffNotFoundError:
        raise HTTPException(status_code=404, detail="Not Found")
    if not detached:
        raise HTTPException(status_code=404, detail="Not Found")

    return RedirectResponse(url=f"/admin/tariffs/{tariff.code}/options", status_code=303)


@router.api_route("/admin/paid-options", methods=["GET", "HEAD"], response_class=HTMLResponse)
def admin_paid_options(request: Request):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    return _template(
        request,
        "paid_options.html",
        title=page_title("Платные опции"),
        paid_options=_paid_options_for_admin(settings=settings),
    )


@router.api_route("/admin/paid-options/new", methods=["GET", "HEAD"], response_class=HTMLResponse)
def admin_paid_options_new(request: Request):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    return _template(
        request,
        "paid_option_form.html",
        title=page_title("Создать платную опцию"),
        mode="create",
        is_create=True,
        option=None,
        form_data=_empty_paid_option_form_data(),
        errors={},
        submit_label="Создать платную опцию",
    )


@router.post("/admin/paid-options/new", response_class=HTMLResponse)
async def admin_paid_options_new_submit(request: Request):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response

    form = await request.form()
    payload, errors = _validate_paid_option_form_input(
        raw_code=form.get("code"),
        raw_title=form.get("title"),
        raw_description=form.get("description"),
        raw_price_rub=form.get("price_rub"),
        raw_currency=form.get("currency"),
        raw_default_duration_days=form.get("default_duration_days"),
        raw_status=form.get("status"),
        raw_is_renewable=form.get("is_renewable"),
        raw_sort_order=form.get("sort_order"),
        include_code=True,
    )
    if errors:
        return _template(
            request,
            "paid_option_form.html",
            status_code=400,
            title=page_title("Создать платную опцию"),
            mode="create",
            is_create=True,
            option=None,
            form_data=_paid_option_form_data_from_form(form),
            errors=errors,
            submit_label="Создать платную опцию",
        )

    try:
        create_paid_option(data=PaidOptionCreateInput(**payload), settings=settings)
    except PaidOptionConflictError as exc:
        errors = _paid_option_form_errors_from_service(exc)
        return _template(
            request,
            "paid_option_form.html",
            status_code=400,
            title=page_title("Создать платную опцию"),
            mode="create",
            is_create=True,
            option=None,
            form_data=_paid_option_form_data_from_form(form),
            errors=errors,
            submit_label="Создать платную опцию",
        )
    except PaidOptionValidationError as exc:
        errors = _paid_option_form_errors_from_service(exc)
        return _template(
            request,
            "paid_option_form.html",
            status_code=400,
            title=page_title("Создать платную опцию"),
            mode="create",
            is_create=True,
            option=None,
            form_data=_paid_option_form_data_from_form(form),
            errors=errors,
            submit_label="Создать платную опцию",
        )

    return RedirectResponse(url="/admin/paid-options", status_code=303)


@router.api_route("/admin/paid-options/{code}/edit", methods=["GET", "HEAD"], response_class=HTMLResponse)
def admin_paid_options_edit(request: Request, code: str):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response

    option = get_paid_option_by_code(code, settings=settings)
    if option is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return _template(
        request,
        "paid_option_form.html",
        title=page_title("Редактировать платную опцию"),
        mode="edit",
        is_create=False,
        option=option,
        form_data=_paid_option_form_data_from_option(option),
        errors={},
        submit_label="Сохранить изменения",
    )


@router.post("/admin/paid-options/{code}/edit", response_class=HTMLResponse)
async def admin_paid_options_edit_submit(request: Request, code: str):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response

    option = get_paid_option_by_code(code, settings=settings)
    if option is None:
        raise HTTPException(status_code=404, detail="Not Found")

    form = await request.form()
    payload, errors = _validate_paid_option_form_input(
        raw_title=form.get("title"),
        raw_description=form.get("description"),
        raw_price_rub=form.get("price_rub"),
        raw_currency=form.get("currency"),
        raw_default_duration_days=form.get("default_duration_days"),
        raw_status=form.get("status"),
        raw_is_renewable=form.get("is_renewable"),
        raw_sort_order=form.get("sort_order"),
        include_code=False,
    )
    posted_code = _normalize_text(form.get("code")).lower()
    if posted_code and posted_code != option.code:
        errors["code"] = "Системный код нельзя изменить после создания."
    if errors:
        return _template(
            request,
            "paid_option_form.html",
            status_code=400,
            title=page_title("Редактировать платную опцию"),
            mode="edit",
            is_create=False,
            option=option,
            form_data={**_paid_option_form_data_from_option(option), **_paid_option_form_data_from_form(form)},
            errors=errors,
            submit_label="Сохранить изменения",
        )

    try:
        update_paid_option(
            code=option.code,
            data=PaidOptionUpdateInput(
                title=payload["title"],
                description=payload["description"],
                price_amount_minor=payload["price_amount_minor"],
                currency=payload["currency"],
                default_duration_days=payload["default_duration_days"],
                status=payload["status"],
                is_renewable=payload["is_renewable"],
                sort_order=payload["sort_order"],
            ),
            settings=settings,
        )
    except PaidOptionNotFoundError:
        raise HTTPException(status_code=404, detail="Not Found")
    except (PaidOptionConflictError, PaidOptionValidationError) as exc:
        errors = _paid_option_form_errors_from_service(exc)
        return _template(
            request,
            "paid_option_form.html",
            status_code=400,
            title=page_title("Редактировать платную опцию"),
            mode="edit",
            is_create=False,
            option=option,
            form_data={**_paid_option_form_data_from_option(option), **_paid_option_form_data_from_form(form)},
            errors=errors,
            submit_label="Сохранить изменения",
        )

    return RedirectResponse(url="/admin/paid-options", status_code=303)


@router.post("/admin/paid-options/{code}/archive")
def admin_paid_options_archive(request: Request, code: str):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    try:
        archive_paid_option(code, settings=settings)
    except PaidOptionNotFoundError:
        raise HTTPException(status_code=404, detail="Not Found")
    return RedirectResponse(url="/admin/paid-options", status_code=303)
```

```diff
diff --git a/source/app/admin/routes.py b/source/app/admin/routes.py
index fdbd980..4b44d30 100644
--- a/source/app/admin/routes.py
+++ b/source/app/admin/routes.py
@@ -20,6 +20,7 @@ from app.auth.service import (
     RoleError,
     get_user_by_session_token,
     list_users_for_admin,
+    set_user_materials_access,
     update_user_role,
 )
 from app.admin.course_export import build_course_export
@@ -148,6 +149,13 @@ def _role_error_response(message: str) -> PlainTextResponse:
     return PlainTextResponse(text, status_code=400)
 
 
+def _admin_users_redirect(request: Request) -> RedirectResponse:
+    redirect_url = "/admin/users"
+    if request.url.query:
+        redirect_url = f"{redirect_url}?{request.url.query}"
+    return RedirectResponse(url=redirect_url, status_code=303)
+
+
 def _template(request: Request, template_name: str, **context) -> HTMLResponse:
     status_code = context.pop("status_code", 200)
     payload = {"request": request, "title": context.pop("title", page_title("AI Starter Community"))}
@@ -187,6 +195,7 @@ def _empty_tariff_form_data() -> dict[str, str]:
         "price_rub": "",
         "currency": "RUB",
         "status": "active",
+        "show_on_homepage": "0",
         "sort_order": "0",
     }
 
@@ -199,6 +208,7 @@ def _tariff_form_data_from_tariff(tariff) -> dict[str, str]:
         "price_rub": _format_price_input(tariff.price_amount_minor),
         "currency": tariff.currency,
         "status": tariff.status,
+        "show_on_homepage": "1" if tariff.show_on_homepage else "0",
         "sort_order": str(tariff.sort_order),
     }
 
@@ -211,6 +221,7 @@ def _tariff_form_data_from_form(form) -> dict[str, str]:
         "price_rub": _normalize_text(form.get("price_rub")),
         "currency": _normalize_text(form.get("currency")) or "RUB",
         "status": _normalize_text(form.get("status")) or "active",
+        "show_on_homepage": "1" if _checkbox_is_true(form.get("show_on_homepage")) else "0",
         "sort_order": _normalize_text(form.get("sort_order")) or "0",
     }
 
@@ -296,6 +307,7 @@ def _validate_tariff_form_input(
     raw_price_rub: str | None = None,
     raw_currency: str | None = None,
     raw_status: str | None = None,
+    raw_show_on_homepage=None,
     raw_sort_order: str | None = None,
     include_code: bool = True,
 ) -> tuple[dict[str, object], dict[str, str]]:
@@ -306,6 +318,7 @@ def _validate_tariff_form_input(
     price_minor, price_error = _parse_positive_money_to_minor(raw_price_rub)
     currency = (_normalize_text(raw_currency) or "RUB").upper()
     status = (_normalize_text(raw_status) or "active").lower()
+    show_on_homepage = _checkbox_is_true(raw_show_on_homepage)
     sort_order, sort_error = _parse_non_negative_int(raw_sort_order, "sort_order")
 
     if include_code:
@@ -344,6 +357,7 @@ def _validate_tariff_form_input(
         "price_amount_minor": price_minor,
         "currency": currency,
         "status": status,
+        "show_on_homepage": show_on_homepage,
         "sort_order": sort_order if sort_order is not None else 0,
     }
     return payload, errors
@@ -637,6 +651,7 @@ def _tariffs_for_admin(settings):
                 "price_display": _format_minor_amount(tariff.price_amount_minor),
                 "currency": tariff.currency,
                 "status_label": _status_label(tariff.status),
+                "show_on_homepage_label": "Да" if tariff.show_on_homepage else "Нет",
                 "sort_order": tariff.sort_order,
                 "included_options_summary": ", ".join(option["title"] for option in linked_options) if linked_options else "—",
                 "created_at": tariff.created_at,
@@ -775,10 +790,33 @@ async def admin_user_role_update(request: Request, user_id: int):
         raise HTTPException(status_code=404, detail="user not found")
     except RoleError as exc:
         return _role_error_response(str(exc))
-    redirect_url = "/admin/users"
-    if request.url.query:
-        redirect_url = f"{redirect_url}?{request.url.query}"
-    return RedirectResponse(url=redirect_url, status_code=303)
+    return _admin_users_redirect(request)
+
+
+@router.post("/admin/users/{user_id}/materials-access/grant")
+def admin_user_materials_access_grant(request: Request, user_id: int):
+    settings = get_settings()
+    _, response = _admin_user_or_redirect(request, settings=settings)
+    if response is not None:
+        return response
+    try:
+        set_user_materials_access(user_id=user_id, granted=True, settings=settings)
+    except AuthNotFoundError as exc:
+        raise HTTPException(status_code=404, detail="user not found") from exc
+    return _admin_users_redirect(request)
+
+
+@router.post("/admin/users/{user_id}/materials-access/revoke")
+def admin_user_materials_access_revoke(request: Request, user_id: int):
+    settings = get_settings()
+    _, response = _admin_user_or_redirect(request, settings=settings)
+    if response is not None:
+        return response
+    try:
+        set_user_materials_access(user_id=user_id, granted=False, settings=settings)
+    except AuthNotFoundError as exc:
+        raise HTTPException(status_code=404, detail="user not found") from exc
+    return _admin_users_redirect(request)
 
 
 @router.api_route("/admin/tariffs", methods=["GET", "HEAD"], response_class=HTMLResponse)
@@ -819,6 +857,7 @@ async def admin_tariffs_new_submit(request: Request):
         raw_price_rub=form.get("price_rub"),
         raw_currency=form.get("currency"),
         raw_status=form.get("status"),
+        raw_show_on_homepage=form.get("show_on_homepage"),
         raw_sort_order=form.get("sort_order"),
         include_code=True,
     )
@@ -886,6 +925,7 @@ async def admin_tariffs_edit_submit(request: Request, code: str):
         raw_price_rub=form.get("price_rub"),
         raw_currency=form.get("currency"),
         raw_status=form.get("status"),
+        raw_show_on_homepage=form.get("show_on_homepage"),
         raw_sort_order=form.get("sort_order"),
         include_code=False,
     )
@@ -911,6 +951,7 @@ async def admin_tariffs_edit_submit(request: Request, code: str):
                 price_amount_minor=payload["price_amount_minor"],
                 currency=payload["currency"],
                 status=payload["status"],
+                show_on_homepage=payload["show_on_homepage"],
                 sort_order=payload["sort_order"],
             ),
             settings=settings,
```


### source/app/admin/templates/tariff_form.html

- tracking state: tracked

```html
{% extends "base.html" %}

{% block content %}
  <section class="card stack">
    <div class="stack">
      <p class="muted">Каталог тарифов</p>
      <h1 class="section-title">{% if is_create %}Создание тарифа{% else %}Редактирование тарифа{% endif %}</h1>
    </div>

    {% if errors.form %}
      <div class="alert alert-error">{{ errors.form }}</div>
    {% endif %}

    <form class="form" method="post">
      <label class="form-row">
        <span>Системный код</span>
        {% if is_create %}
          <input class="input" type="text" name="code" value="{{ form_data.code }}">
          <span class="form-help">Нужен программе. Можно оставить пустым — система создаст код автоматически.</span>
        {% else %}
          <input class="input" type="text" name="code" value="{{ tariff.code }}" readonly>
          <span class="form-help">Системный код нельзя изменить после создания.</span>
        {% endif %}
        {% if errors.code %}
          <span class="alert alert-error">{{ errors.code }}</span>
        {% endif %}
      </label>

      <label class="form-row">
        <span>Название</span>
        <input class="input" type="text" name="title" value="{{ form_data.title }}">
        {% if errors.title %}
          <span class="alert alert-error">{{ errors.title }}</span>
        {% endif %}
      </label>

      <label class="form-row">
        <span>Описание</span>
        <textarea class="textarea" name="description">{{ form_data.description }}</textarea>
        {% if errors.description %}
          <span class="alert alert-error">{{ errors.description }}</span>
        {% endif %}
      </label>

      <label class="form-row">
        <span>Цена, ₽</span>
        <input class="input" type="text" name="price_rub" value="{{ form_data.price_rub }}">
        {% if errors.price_rub %}
          <span class="alert alert-error">{{ errors.price_rub }}</span>
        {% endif %}
      </label>

      <label class="form-row">
        <span>Валюта</span>
        <input class="input" type="text" name="currency" value="{{ form_data.currency }}">
        {% if errors.currency %}
          <span class="alert alert-error">{{ errors.currency }}</span>
        {% endif %}
      </label>

      <label class="form-row">
        <span>Статус</span>
        <select class="select" name="status">
          <option value="active" {% if form_data.status == "active" %}selected{% endif %}>активен</option>
          <option value="hidden" {% if form_data.status == "hidden" %}selected{% endif %}>скрыт</option>
          <option value="archived" {% if form_data.status == "archived" %}selected{% endif %}>архив</option>
        </select>
        {% if errors.status %}
          <span class="alert alert-error">{{ errors.status }}</span>
        {% endif %}
      </label>

      <label class="form-row">
        <span>Отображать на главной</span>
        <input type="checkbox" name="show_on_homepage" value="1" {% if form_data.show_on_homepage == "1" %}checked{% endif %}>
        <span class="form-help">Активный тариф с этим флагом может быть выбран для публичного блока цен.</span>
        {% if errors.show_on_homepage %}
          <span class="alert alert-error">{{ errors.show_on_homepage }}</span>
        {% endif %}
      </label>

      <label class="form-row">
        <span>Порядок сортировки</span>
        <input class="input" type="number" name="sort_order" min="0" step="1" value="{{ form_data.sort_order }}">
        {% if errors.sort_order %}
          <span class="alert alert-error">{{ errors.sort_order }}</span>
        {% endif %}
      </label>

      <div class="form-actions">
        <button class="button button-primary" type="submit">{{ submit_label }}</button>
        <a class="button button-secondary" href="/admin/tariffs">Назад к списку</a>
      </div>
    </form>
  </section>
{% endblock %}
```

```diff
diff --git a/source/app/admin/templates/tariff_form.html b/source/app/admin/templates/tariff_form.html
index 54d0587..b131002 100644
--- a/source/app/admin/templates/tariff_form.html
+++ b/source/app/admin/templates/tariff_form.html
@@ -70,6 +70,15 @@
         {% endif %}
       </label>
 
+      <label class="form-row">
+        <span>Отображать на главной</span>
+        <input type="checkbox" name="show_on_homepage" value="1" {% if form_data.show_on_homepage == "1" %}checked{% endif %}>
+        <span class="form-help">Активный тариф с этим флагом может быть выбран для публичного блока цен.</span>
+        {% if errors.show_on_homepage %}
+          <span class="alert alert-error">{{ errors.show_on_homepage }}</span>
+        {% endif %}
+      </label>
+
       <label class="form-row">
         <span>Порядок сортировки</span>
         <input class="input" type="number" name="sort_order" min="0" step="1" value="{{ form_data.sort_order }}">
```


### source/app/admin/templates/tariffs.html

- tracking state: tracked

```html
{% extends "base.html" %}

{% block content %}
  <section class="card stack">
    <div class="stack">
      <p class="muted">Каталог тарифов</p>
      <h1 class="section-title">Тарифы</h1>
    </div>

    <div class="actions">
      <a class="button button-primary" href="/admin/tariffs/new">Создать тариф</a>
    </div>

    <table class="table">
      <thead>
        <tr>
          <th>Код</th>
          <th>Название</th>
          <th>Описание</th>
          <th>Цена, ₽</th>
          <th>Валюта</th>
          <th>Статус</th>
          <th>На главной</th>
          <th>Порядок сортировки</th>
          <th>Включённые опции</th>
          <th>Создан</th>
          <th>Обновлён</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        {% for tariff in tariffs %}
          <tr>
            <td>{{ tariff.code }}</td>
            <td>{{ tariff.title }}</td>
            <td>{{ tariff.description }}</td>
            <td>{{ tariff.price_display }}</td>
            <td>{{ tariff.currency }}</td>
            <td>{{ tariff.status_label }}</td>
            <td>{{ tariff.show_on_homepage_label }}</td>
            <td>{{ tariff.sort_order }}</td>
            <td>{{ tariff.included_options_summary }}</td>
            <td>{{ tariff.created_at }}</td>
            <td>{{ tariff.updated_at }}</td>
            <td>
              <div class="table-actions">
                <a class="button button-secondary" href="/admin/tariffs/{{ tariff.code }}/options">Настроить опции</a>
                <a class="button button-secondary" href="/admin/tariffs/{{ tariff.code }}/edit">Редактировать</a>
                <form method="post" action="/admin/tariffs/{{ tariff.code }}/archive">
                  <button class="button button-danger" type="submit">Архивировать</button>
                </form>
              </div>
            </td>
          </tr>
        {% else %}
          <tr>
            <td colspan="12">Тарифов пока нет.</td>
          </tr>
        {% endfor %}
      </tbody>
    </table>
  </section>
{% endblock %}
```

```diff
diff --git a/source/app/admin/templates/tariffs.html b/source/app/admin/templates/tariffs.html
index 4cbf393..2a56f43 100644
--- a/source/app/admin/templates/tariffs.html
+++ b/source/app/admin/templates/tariffs.html
@@ -20,6 +20,7 @@
           <th>Цена, ₽</th>
           <th>Валюта</th>
           <th>Статус</th>
+          <th>На главной</th>
           <th>Порядок сортировки</th>
           <th>Включённые опции</th>
           <th>Создан</th>
@@ -36,6 +37,7 @@
             <td>{{ tariff.price_display }}</td>
             <td>{{ tariff.currency }}</td>
             <td>{{ tariff.status_label }}</td>
+            <td>{{ tariff.show_on_homepage_label }}</td>
             <td>{{ tariff.sort_order }}</td>
             <td>{{ tariff.included_options_summary }}</td>
             <td>{{ tariff.created_at }}</td>
@@ -52,7 +54,7 @@
           </tr>
         {% else %}
           <tr>
-            <td colspan="11">Тарифов пока нет.</td>
+            <td colspan="12">Тарифов пока нет.</td>
           </tr>
         {% endfor %}
       </tbody>
```


### source/app/shared/tariff_display.py

- tracking state: untracked

```py
"""Shared tariff display helpers."""

from __future__ import annotations

from decimal import Decimal

from app.core.config import Settings, get_settings
from app.tariffs.service import get_homepage_tariff


def format_tariff_price(amount_minor: int | None, currency: str | None) -> str:
    if amount_minor is None:
        return "Цена не указана"

    amount = Decimal(int(amount_minor)) / Decimal(100)
    if amount == amount.to_integral():
        amount_text = f"{int(amount):,}".replace(",", " ")
    else:
        amount_text = f"{amount:,.2f}".replace(",", " ").replace(".", ",")

    currency_code = (currency or "RUB").upper()
    currency_suffix = "₽" if currency_code == "RUB" else currency_code
    return f"{amount_text} {currency_suffix}"


def get_homepage_tariff_context(settings: Settings | None = None) -> dict[str, object]:
    resolved = settings or get_settings()
    homepage_tariff = get_homepage_tariff(settings=resolved)
    return {
        "homepage_tariff": homepage_tariff,
        "homepage_tariff_price_display": (
            format_tariff_price(homepage_tariff.price_amount_minor, homepage_tariff.currency)
            if homepage_tariff is not None
            else None
        ),
    }
```


### source/app/shared/templates/tariff_pricing_section.html

- tracking state: untracked

```html
<section class="section{% if pricing_section_class %} {{ pricing_section_class }}{% endif %}"{% if pricing_section_id %} id="{{ pricing_section_id }}"{% endif %}>
  <div class="{% if pricing_container_class %}{{ pricing_container_class }}{% else %}container{% endif %}">
    <div class="{{ pricing_shell_class or 'pricing-shell' }}">
      <div class="price-head">
        <span class="eyebrow">{{ pricing_eyebrow or "Цена" }}</span>
        {% if homepage_tariff %}
          <h2 class="section-title">{{ homepage_tariff.title }} — {{ homepage_tariff_price_display }}</h2>
          <p class="section-desc">{{ homepage_tariff.description or pricing_fallback_description or "Это активный тариф, отмеченный для показа на главной странице. Он подтягивается из каталога тарифов." }}</p>
        {% else %}
          <h2 class="section-title">{{ pricing_empty_title or "Актуальный тариф на главной выбирается из каталога" }}</h2>
          <p class="section-desc">{{ pricing_empty_description or "Когда активный тариф будет отмечен для главной страницы, здесь появятся его название и цена. Сейчас показывается нейтральная информация без числовой цены." }}</p>
        {% endif %}
      </div>
      <div class="offer-grid">
        <div class="offer-group">
          <h3>Первый месяц</h3>
          <p>Всё, что нужно, чтобы пройти стартовый проект и не застрять на первых шагах. Подписка ChatGPT Plus входит в стоимость и остаётся у вас.</p>
          <ul>
            <li>Подписка ChatGPT Plus на месяц;</li>
            <li>Сервер и окружение для старта;</li>
            <li>Первый проект с ИИ-наставником;</li>
            <li>Дорожная карта разработки;</li>
            <li>Помощь на первых шагах.</li>
          </ul>
        </div>
        <div class="offer-group">
          <h3>Навсегда</h3>
          <p>Остаётся у вас после оплаты и помогает повторять подход уже на своих идеях.</p>
          <ul>
            <li>Доступ к материалам;</li>
            <li>Пошаговые инструкции;</li>
            <li>База команд и промптов;</li>
            <li>Правила работы с техническим ИИ-исполнителем;</li>
            <li>Дорожная карта первого проекта;</li>
            <li>Понимание, как повторять подход на своих идеях.</li>
          </ul>
        </div>
        <div class="offer-group">
          <h3>Комьюнити</h3>
          <p>Поддержка вокруг главного результата: первого проекта и навыка самостоятельной работы.</p>
          <ul>
            <li>Помощь, если застряли;</li>
            <li>Обмен идеями;</li>
            <li>Обсуждение проектов;</li>
            <li>Поиск соратников;</li>
            <li>Возможность объединяться для более крупных продуктов.</li>
          </ul>
        </div>
      </div>
      <div class="pricing-actions">
        <a href="{{ primary_cta_href }}" class="btn btn-primary">{{ primary_cta_label }}</a>
        <a href="{{ secondary_cta_href }}" class="btn btn-secondary">{{ secondary_cta_label }}</a>
        <p class="pricing-note">{{ pricing_note_text or "После первого месяца вы сможете продолжать самостоятельно. Продление OpenScript не обязательно, но внешние инструменты, серверы и API при необходимости оплачиваются отдельно." }}</p>
      </div>
    </div>
  </div>
</section>
```


## 7. ADMIN_ACCESS_CURRENT_CODE

### source/app/admin/routes.py

```py
"""Admin dashboard routes."""

from __future__ import annotations

import re
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from app.auth.service import (
    ADMIN_USER_DEFAULT_SORT,
    ALLOWED_ADMIN_USER_ACCESS_STATUSES,
    ALLOWED_ROLES,
    ROLE_LABELS_RU,
    NotFoundError as AuthNotFoundError,
    RoleError,
    get_user_by_session_token,
    list_users_for_admin,
    set_user_materials_access,
    update_user_role,
)
from app.admin.course_export import build_course_export
from app.core.config import get_settings
from app.paid_options.schemas import PaidOptionCreateInput, PaidOptionUpdateInput
from app.paid_options.service import (
    ConflictError as PaidOptionConflictError,
    NotFoundError as PaidOptionNotFoundError,
    ValidationError as PaidOptionValidationError,
    archive_paid_option,
    create_paid_option,
    get_paid_option_by_code,
    list_paid_options,
    list_paid_options_for_admin,
    update_paid_option,
)
from app.shared.utils import page_title
from app.tariffs.schemas import TariffCreateInput, TariffUpdateInput
from app.tariffs.service import (
    ConflictError as TariffConflictError,
    NotFoundError as TariffNotFoundError,
    ValidationError as TariffValidationError,
    attach_option_to_tariff,
    archive_tariff,
    detach_option_from_tariff,
    create_tariff,
    get_tariff_by_code,
    list_tariff_options,
    list_tariffs_for_admin,
    update_tariff_option_link,
    update_tariff,
)

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))

TARIFF_CODE_RE = re.compile(r"^[a-z0-9_-]{3,64}$")
ALLOWED_TARIFF_STATUSES = {"active", "hidden", "archived"}
ADMIN_USER_SORT_OPTIONS = {"desc": "Сначала новые", "asc": "Сначала старые"}


def _admin_user_filter_error(message: str) -> PlainTextResponse:
    lowered = message.lower()
    if "role" in lowered and "unsupported" in lowered:
        text = "Выберите допустимую роль."
    elif "access status" in lowered or "status" in lowered:
        text = "Выберите допустимый статус доступа."
    elif "created sort" in lowered:
        text = "Выберите допустимый порядок сортировки."
    elif "date" in lowered:
        text = "Укажите корректную дату регистрации."
    else:
        text = "Не удалось применить фильтр."
    return PlainTextResponse(text, status_code=400)


def _parse_admin_user_date(value: str | None) -> date | None:
    raw = (value or "").strip()
    if not raw:
        return None
    return date.fromisoformat(raw)


def _parse_admin_user_filters(request: Request) -> tuple[dict[str, object], str | None]:
    query = request.query_params
    raw_role = (query.get("role") or "all").strip().lower()
    if raw_role in {"", "all"}:
        role = None
        role_value = "all"
    elif raw_role in ALLOWED_ROLES:
        role = raw_role
        role_value = raw_role
    else:
        return {}, "unsupported role"

    raw_access_status = (query.get("access_status") or "all").strip().lower()
    if raw_access_status in {"", "all"}:
        access_status = None
        access_status_value = "all"
    elif raw_access_status in ALLOWED_ADMIN_USER_ACCESS_STATUSES:
        access_status = raw_access_status
        access_status_value = raw_access_status
    else:
        return {}, "unsupported access status"

    raw_created_sort = (query.get("created_sort") or ADMIN_USER_DEFAULT_SORT).strip().lower() or ADMIN_USER_DEFAULT_SORT
    if raw_created_sort not in ADMIN_USER_SORT_OPTIONS:
        return {}, "unsupported created sort"

    try:
        created_from = _parse_admin_user_date(query.get("created_from"))
        created_to = _parse_admin_user_date(query.get("created_to"))
    except ValueError:
        return {}, "invalid date"

    return {
        "role": role,
        "access_status": access_status,
        "created_from": created_from,
        "created_to": created_to,
        "created_sort": raw_created_sort,
        "filter_role": role_value,
        "filter_access_status": access_status_value,
        "created_from_value": (query.get("created_from") or "").strip(),
        "created_to_value": (query.get("created_to") or "").strip(),
        "query_string": request.url.query,
    }, None


def _status_label(value: str) -> str:
    return {
        "active": "активен",
        "hidden": "скрыт",
        "archived": "архив",
    }.get(value, value)


def _role_error_response(message: str) -> PlainTextResponse:
    lowered = message.lower()
    if "last admin" in lowered:
        text = "Нельзя изменить роль последнего администратора."
    elif "unsupported role" in lowered:
        text = "Выберите допустимую роль."
    else:
        text = "Не удалось изменить роль пользователя."
    return PlainTextResponse(text, status_code=400)


def _admin_users_redirect(request: Request) -> RedirectResponse:
    redirect_url = "/admin/users"
    if request.url.query:
        redirect_url = f"{redirect_url}?{request.url.query}"
    return RedirectResponse(url=redirect_url, status_code=303)


def _template(request: Request, template_name: str, **context) -> HTMLResponse:
    status_code = context.pop("status_code", 200)
    payload = {"request": request, "title": context.pop("title", page_title("AI Starter Community"))}
    payload.update(context)
    return templates.TemplateResponse(request, template_name, payload, status_code=status_code)


def _admin_user_or_redirect(request: Request, settings=None):
    resolved = settings or get_settings()
    session_token = request.cookies.get(resolved.session_cookie_name)
    user = get_user_by_session_token(session_token, settings=resolved)
    if user is None:
        return None, RedirectResponse(url="/login", status_code=303)
    if user.role != "admin":
        return user, PlainTextResponse("Доступ запрещён\nУ вашей учётной записи нет прав администратора.", status_code=403)
    return user, None


def _format_minor_amount(amount_minor: int) -> str:
    amount = Decimal(amount_minor) / Decimal(100)
    return f"{amount:,.2f}".replace(",", " ").replace(".", ",")


def _format_price_input(amount_minor: int) -> str:
    amount = Decimal(amount_minor) / Decimal(100)
    text = format(amount, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def _empty_tariff_form_data() -> dict[str, str]:
    return {
        "code": "",
        "title": "",
        "description": "",
        "price_rub": "",
        "currency": "RUB",
        "status": "active",
        "show_on_homepage": "0",
        "sort_order": "0",
    }


def _tariff_form_data_from_tariff(tariff) -> dict[str, str]:
    return {
        "code": tariff.code,
        "title": tariff.title,
        "description": tariff.description or "",
        "price_rub": _format_price_input(tariff.price_amount_minor),
        "currency": tariff.currency,
        "status": tariff.status,
        "show_on_homepage": "1" if tariff.show_on_homepage else "0",
        "sort_order": str(tariff.sort_order),
    }


def _tariff_form_data_from_form(form) -> dict[str, str]:
    return {
        "code": _normalize_text(form.get("code")),
        "title": _normalize_text(form.get("title")),
        "description": _normalize_text(form.get("description")),
        "price_rub": _normalize_text(form.get("price_rub")),
        "currency": _normalize_text(form.get("currency")) or "RUB",
        "status": _normalize_text(form.get("status")) or "active",
        "show_on_homepage": "1" if _checkbox_is_true(form.get("show_on_homepage")) else "0",
        "sort_order": _normalize_text(form.get("sort_order")) or "0",
    }


def _parse_positive_money_to_minor(value: str | None) -> tuple[int | None, str | None]:
    raw = (value or "").strip()
    if not raw:
        return None, "price is required"
    raw = raw.replace(",", ".")
    try:
        amount = Decimal(raw)
    except InvalidOperation:
        return None, "price must be a valid ruble amount"
    if not amount.is_finite() or amount < 0:
        return None, "price must be a non-negative amount"
    minor = amount * Decimal(100)
    if minor != minor.to_integral_value():
        return None, "price must have at most 2 decimal places"
    return int(minor), None


def _parse_non_negative_int(value: str | None, field_name: str, default: int = 0) -> tuple[int | None, str | None]:
    raw = (value or "").strip()
    if not raw:
        return default, None
    try:
        parsed = int(raw)
    except ValueError:
        return None, f"{field_name} must be an integer"
    if parsed < 0:
        return None, f"{field_name} must be greater than or equal to 0"
    return parsed, None


def _parse_optional_non_negative_int(value: str | None, field_name: str) -> tuple[int | None, str | None]:
    raw = (value or "").strip()
    if not raw:
        return None, None
    try:
        parsed = int(raw)
    except ValueError:
        return None, f"{field_name} must be an integer"
    if parsed < 0:
        return None, f"{field_name} must be greater than or equal to 0"
    return parsed, None


def _normalize_text(value: str | None) -> str:
    return (value or "").strip()


def _tariff_form_errors_from_service(exc: Exception) -> dict[str, str]:
    message = str(exc)
    lowered = message.lower()
    if "code already exists" in lowered:
        return {"code": "Тариф с таким кодом уже существует."}
    if "code is required" in lowered or lowered.startswith("code "):
        return {"code": "Укажите системный код тарифа."}
    if lowered.startswith("title "):
        return {"title": "Укажите название тарифа."}
    if lowered.startswith("description "):
        return {"description": "Описание тарифа слишком длинное."}
    if "price_amount_minor" in lowered:
        if "at most 2 decimal places" in lowered:
            return {"price_rub": "Цена может содержать не более 2 знаков после запятой."}
        if "non-negative" in lowered:
            return {"price_rub": "Цена не может быть отрицательной."}
        return {"price_rub": "Введите корректную цену в рублях."}
    if lowered.startswith("currency "):
        return {"currency": "Валюта должна быть кодом из 3 заглавных букв."}
    if lowered.startswith("status "):
        return {"status": "Статус должен быть активен, скрыт или архив."}
    if lowered.startswith("sort_order "):
        return {"sort_order": "Порядок сортировки должен быть целым числом не меньше 0."}
    return {"form": "Не удалось сохранить тариф."}


def _validate_tariff_form_input(
    *,
    raw_code: str | None = None,
    raw_title: str | None = None,
    raw_description: str | None = None,
    raw_price_rub: str | None = None,
    raw_currency: str | None = None,
    raw_status: str | None = None,
    raw_show_on_homepage=None,
    raw_sort_order: str | None = None,
    include_code: bool = True,
) -> tuple[dict[str, object], dict[str, str]]:
    errors: dict[str, str] = {}
    code = _normalize_text(raw_code).lower()
    title = _normalize_text(raw_title)
    description = _normalize_text(raw_description) or None
    price_minor, price_error = _parse_positive_money_to_minor(raw_price_rub)
    currency = (_normalize_text(raw_currency) or "RUB").upper()
    status = (_normalize_text(raw_status) or "active").lower()
    show_on_homepage = _checkbox_is_true(raw_show_on_homepage)
    sort_order, sort_error = _parse_non_negative_int(raw_sort_order, "sort_order")

    if include_code:
        if code and not TARIFF_CODE_RE.fullmatch(code):
            errors["code"] = "Системный код тарифа должен содержать 3-64 символа: строчные латинские буквы, цифры, подчёркивание или дефис."
        elif code is None or code == "":
            code = None
    elif code == "":
        code = None
    if not title:
        errors["title"] = "Укажите название тарифа."
    elif len(title) > 200:
        errors["title"] = "Название тарифа должно быть не длиннее 200 символов."
    if description is not None and len(description) > 4000:
        errors["description"] = "Описание тарифа должно быть не длиннее 4000 символов."
    if price_error:
        if price_error == "price is required":
            errors["price_rub"] = "Укажите цену тарифа."
        elif price_error == "price must be a valid ruble amount":
            errors["price_rub"] = "Введите корректную цену в рублях."
        elif price_error == "price must be a non-negative amount":
            errors["price_rub"] = "Цена не может быть отрицательной."
        else:
            errors["price_rub"] = "Цена может содержать не более 2 знаков после запятой."
    if not re.fullmatch(r"^[A-Z]{3}$", currency):
        errors["currency"] = "Валюта должна быть кодом из 3 заглавных букв."
    if status not in ALLOWED_TARIFF_STATUSES:
        errors["status"] = "Статус должен быть активен, скрыт или архив."
    if sort_error:
        errors["sort_order"] = "Порядок сортировки должен быть целым числом не меньше 0."

    payload = {
        "code": code,
        "title": title,
        "description": description,
        "price_amount_minor": price_minor,
        "currency": currency,
        "status": status,
        "show_on_homepage": show_on_homepage,
        "sort_order": sort_order if sort_order is not None else 0,
    }
    return payload, errors


def _paid_options_for_admin(settings):
    rows = []
    for option in list_paid_options_for_admin(settings=settings):
        rows.append(
            {
                "code": option.code,
                "title": option.title,
                "description": option.description or "—",
                "price_display": "отдельная цена не задана"
                if option.price_amount_minor is None
                else _format_minor_amount(option.price_amount_minor),
                "currency": option.currency,
                "default_duration_days": "—" if option.default_duration_days is None else option.default_duration_days,
                "status_label": _status_label(option.status),
                "is_renewable": option.is_renewable,
                "sort_order": option.sort_order,
                "created_at": option.created_at,
                "updated_at": option.updated_at,
            }
        )
    return rows


def _empty_tariff_option_attach_form_data() -> dict[str, str]:
    return {
        "option_code": "",
        "included_duration_days": "",
        "included_quantity": "",
    }


def _tariff_option_form_value(value) -> str:
    if value is None:
        return ""
    return str(value)


def _tariff_option_link_rows(settings, tariff_code: str, *, link_overrides: dict[str, dict[str, str]] | None = None) -> list[dict[str, object]]:
    linked_rows = list_tariff_options(tariff_code, include_hidden=True, include_archived=True, settings=settings)
    rows: list[dict[str, object]] = []
    for link in linked_rows:
        code = str(link["code"])
        override = (link_overrides or {}).get(code, {})
        rows.append(
            {
                "code": code,
                "title": str(link["title"]),
                "status_label": _status_label(str(link["status"])),
                "included_duration_days": _tariff_option_form_value(override.get("included_duration_days", link["included_duration_days"])),
                "included_quantity": _tariff_option_form_value(override.get("included_quantity", link["included_quantity"])),
            }
        )
    return rows


def _tariff_options_page_context(
    settings,
    tariff,
    *,
    attach_form_data: dict[str, str] | None = None,
    errors: dict[str, str] | None = None,
    link_overrides: dict[str, dict[str, str]] | None = None,
) -> dict[str, object]:
    linked_options = _tariff_option_link_rows(settings, tariff.code, link_overrides=link_overrides)
    linked_codes = {option["code"] for option in linked_options}
    available_paid_options = [
        {
            "code": option.code,
            "title": option.title,
            "status_label": _status_label(option.status),
        }
        for option in list_paid_options(settings=settings)
        if option.code not in linked_codes
    ]
    return {
        "tariff": tariff,
        "linked_options": linked_options,
        "available_paid_options": available_paid_options,
        "attach_form_data": attach_form_data or _empty_tariff_option_attach_form_data(),
        "errors": errors or {},
    }


def _render_tariff_options_page(
    request: Request,
    settings,
    tariff,
    *,
    attach_form_data: dict[str, str] | None = None,
    errors: dict[str, str] | None = None,
    link_overrides: dict[str, dict[str, str]] | None = None,
    status_code: int = 200,
):
    return _template(
        request,
        "tariff_options.html",
        status_code=status_code,
        title=page_title(f"Опции тарифа: {tariff.title}"),
        **_tariff_options_page_context(
            settings,
            tariff,
            attach_form_data=attach_form_data,
            errors=errors,
            link_overrides=link_overrides,
        ),
    )


def _empty_paid_option_form_data() -> dict[str, object]:
    return {
        "code": "",
        "title": "",
        "description": "",
        "price_rub": "",
        "currency": "RUB",
        "default_duration_days": "",
        "status": "active",
        "is_renewable": True,
        "sort_order": "0",
    }


def _paid_option_form_data_from_option(option) -> dict[str, object]:
    return {
        "code": option.code,
        "title": option.title,
        "description": option.description or "",
        "price_rub": "" if option.price_amount_minor is None else _format_price_input(option.price_amount_minor),
        "currency": option.currency,
        "default_duration_days": "" if option.default_duration_days is None else str(option.default_duration_days),
        "status": option.status,
        "is_renewable": bool(option.is_renewable),
        "sort_order": str(option.sort_order),
    }


def _paid_option_form_data_from_form(form) -> dict[str, object]:
    return {
        "code": _normalize_text(form.get("code")),
        "title": _normalize_text(form.get("title")),
        "description": _normalize_text(form.get("description")),
        "price_rub": _normalize_text(form.get("price_rub")),
        "currency": _normalize_text(form.get("currency")) or "RUB",
        "default_duration_days": _normalize_text(form.get("default_duration_days")),
        "status": _normalize_text(form.get("status")) or "active",
        "is_renewable": _checkbox_is_true(form.get("is_renewable")),
        "sort_order": _normalize_text(form.get("sort_order")) or "0",
    }


def _checkbox_is_true(value) -> bool:
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return value != 0
    raw = str(value).strip().lower()
    return raw not in {"", "0", "false", "off", "no"}


def _parse_optional_money_to_minor(value: str | None) -> tuple[int | None, str | None]:
    raw = (value or "").strip()
    if not raw:
        return None, None
    raw = raw.replace(",", ".")
    try:
        amount = Decimal(raw)
    except InvalidOperation:
        return None, "price must be a valid ruble amount"
    if not amount.is_finite() or amount < 0:
        return None, "price must be a non-negative amount"
    minor = amount * Decimal(100)
    if minor != minor.to_integral_value():
        return None, "price must have at most 2 decimal places"
    return int(minor), None


def _paid_option_form_errors_from_service(exc: Exception) -> dict[str, str]:
    message = str(exc)
    lowered = message.lower()
    if "code already exists" in lowered:
        return {"code": "Платная опция с таким кодом уже существует."}
    if "code is required" in lowered or lowered.startswith("code "):
        return {"code": "Укажите системный код платной опции."}
    if lowered.startswith("title "):
        return {"title": "Укажите название платной опции."}
    if lowered.startswith("description "):
        return {"description": "Описание платной опции слишком длинное."}
    if "price_amount_minor" in lowered:
        if "at most 2 decimal places" in lowered:
            return {"price_rub": "Цена может содержать не более 2 знаков после запятой."}
        if "non-negative" in lowered:
            return {"price_rub": "Цена не может быть отрицательной."}
        return {"price_rub": "Введите корректную цену в рублях."}
    if lowered.startswith("currency "):
        return {"currency": "Валюта должна быть кодом из 3 заглавных букв."}
    if lowered.startswith("default_duration_days "):
        return {"default_duration_days": "Срок по умолчанию должен быть целым числом не меньше 0."}
    if lowered.startswith("status "):
        return {"status": "Статус должен быть активен, скрыт или архив."}
    if lowered.startswith("is_renewable "):
        return {"is_renewable": "Значение поля «Можно продлевать» некорректно."}
    if lowered.startswith("sort_order "):
        return {"sort_order": "Порядок сортировки должен быть целым числом не меньше 0."}
    return {"form": "Не удалось сохранить платную опцию."}


def _validate_paid_option_form_input(
    *,
    raw_code: str | None = None,
    raw_title: str | None = None,
    raw_description: str | None = None,
    raw_price_rub: str | None = None,
    raw_currency: str | None = None,
    raw_default_duration_days: str | None = None,
    raw_status: str | None = None,
    raw_is_renewable=None,
    raw_sort_order: str | None = None,
    include_code: bool = True,
) -> tuple[dict[str, object], dict[str, str]]:
    errors: dict[str, str] = {}
    code = _normalize_text(raw_code).lower()
    title = _normalize_text(raw_title)
    description = _normalize_text(raw_description) or None
    price_minor, price_error = _parse_optional_money_to_minor(raw_price_rub)
    currency = (_normalize_text(raw_currency) or "RUB").upper()
    default_duration_days, duration_error = _parse_optional_non_negative_int(raw_default_duration_days, "default_duration_days")
    status = (_normalize_text(raw_status) or "active").lower()
    is_renewable = _checkbox_is_true(raw_is_renewable)
    sort_order, sort_error = _parse_non_negative_int(raw_sort_order, "sort_order")

    if include_code:
        if code and not TARIFF_CODE_RE.fullmatch(code):
            errors["code"] = "Системный код платной опции должен содержать 3-64 символа: строчные латинские буквы, цифры, подчёркивание или дефис."
        elif code == "":
            code = None
    elif code == "":
        code = None
    if not title:
        errors["title"] = "Укажите название платной опции."
    elif len(title) > 200:
        errors["title"] = "Название платной опции должно быть не длиннее 200 символов."
    if description is not None and len(description) > 4000:
        errors["description"] = "Описание платной опции должно быть не длиннее 4000 символов."
    if price_error:
        if price_error == "price must be a valid ruble amount":
            errors["price_rub"] = "Введите корректную цену в рублях."
        elif price_error == "price must be a non-negative amount":
            errors["price_rub"] = "Цена не может быть отрицательной."
        else:
            errors["price_rub"] = "Цена может содержать не более 2 знаков после запятой."
    if not re.fullmatch(r"^[A-Z]{3}$", currency):
        errors["currency"] = "Валюта должна быть кодом из 3 заглавных букв."
    if duration_error:
        errors["default_duration_days"] = "Срок по умолчанию должен быть целым числом не меньше 0."
    if status not in ALLOWED_TARIFF_STATUSES:
        errors["status"] = "Статус должен быть активен, скрыт или архив."
    if sort_error:
        errors["sort_order"] = "Порядок сортировки должен быть целым числом не меньше 0."

    payload = {
        "code": code,
        "title": title,
        "description": description,
        "price_amount_minor": price_minor,
        "currency": currency,
        "default_duration_days": default_duration_days,
        "status": status,
        "is_renewable": is_renewable,
        "sort_order": sort_order if sort_order is not None else 0,
    }
    return payload, errors


def _tariffs_for_admin(settings):
    tariffs = list_tariffs_for_admin(settings=settings)
    rows = []
    for tariff in tariffs:
        linked_options = list_tariff_options(tariff.code, include_hidden=True, include_archived=True, settings=settings)
        rows.append(
            {
                "code": tariff.code,
                "title": tariff.title,
                "description": tariff.description or "—",
                "price_display": _format_minor_amount(tariff.price_amount_minor),
                "currency": tariff.currency,
                "status_label": _status_label(tariff.status),
                "show_on_homepage_label": "Да" if tariff.show_on_homepage else "Нет",
                "sort_order": tariff.sort_order,
                "included_options_summary": ", ".join(option["title"] for option in linked_options) if linked_options else "—",
                "created_at": tariff.created_at,
                "updated_at": tariff.updated_at,
            }
        )
    return rows


def _render_tariff_form(
    request: Request,
    *,
    mode: str,
    form_data: dict[str, str],
    errors: dict[str, str] | None = None,
    tariff=None,
    status_code: int = 200,
):
    is_create = mode == "create"
    return _template(
        request,
        "tariff_form.html",
        status_code=status_code,
        title=page_title("Создать тариф" if is_create else "Редактировать тариф"),
        mode=mode,
        is_create=is_create,
        tariff=tariff,
        form_data=form_data,
        errors=errors or {},
        submit_label="Создать тариф" if is_create else "Сохранить изменения",
    )


def _validate_tariff_option_link_form_input(
    *,
    raw_option_code: str | None = None,
    raw_included_duration_days: str | None = None,
    raw_included_quantity: str | None = None,
    include_option_code: bool = True,
) -> tuple[dict[str, str], dict[str, str]]:
    errors: dict[str, str] = {}
    option_code = _normalize_text(raw_option_code).lower()
    duration_days, duration_error = _parse_optional_non_negative_int(raw_included_duration_days, "included_duration_days")
    quantity, quantity_error = _parse_optional_non_negative_int(raw_included_quantity, "included_quantity")

    if include_option_code:
        if not option_code:
            errors["option_code"] = "Выберите платную опцию."
        elif not TARIFF_CODE_RE.fullmatch(option_code):
            errors["option_code"] = "Системный код платной опции должен содержать 3-64 символа: строчные латинские буквы, цифры, подчёркивание или дефис."
    if duration_error:
        errors["included_duration_days"] = "Включённый срок должен быть целым числом не меньше 0."
    if quantity_error:
        errors["included_quantity"] = "Включённое количество должно быть целым числом не меньше 0."

    payload = {
        "option_code": option_code,
        "included_duration_days": "" if duration_days is None else str(duration_days),
        "included_quantity": "" if quantity is None else str(quantity),
    }
    return payload, errors


@router.api_route("/admin", methods=["GET", "HEAD"], response_class=HTMLResponse)
def admin_dashboard(request: Request):
    settings = get_settings()
    user, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    return _template(
        request,
        "dashboard.html",
        title=page_title("Админ-панель"),
        admin_email=user.email,
        admin_login=user.login,
    )


@router.get("/admin/course-export")
def admin_course_export(request: Request):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response

    export = build_course_export()
    headers = {
        "Content-Disposition": f'attachment; filename="{export.filename}"',
    }
    return Response(content=export.content, media_type="application/zip", headers=headers)


@router.api_route("/admin/users", methods=["GET", "HEAD"], response_class=HTMLResponse)
def admin_users(request: Request):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    filters, error = _parse_admin_user_filters(request)
    if error is not None:
        return _admin_user_filter_error(error)
    return _template(
        request,
        "users.html",
        title=page_title("Пользователи"),
        users=list_users_for_admin(
            settings=settings,
            role=filters["role"],
            access_status=filters["access_status"],
            created_from=filters["created_from"],
            created_to=filters["created_to"],
            created_sort=filters["created_sort"],
        ),
        allowed_roles=ALLOWED_ROLES,
        role_labels=ROLE_LABELS_RU,
        filter_role=filters["filter_role"],
        filter_access_status=filters["filter_access_status"],
        created_from_value=filters["created_from_value"],
        created_to_value=filters["created_to_value"],
        created_sort=filters["created_sort"],
        query_string=filters["query_string"],
    )


@router.post("/admin/users/{user_id}/role")
async def admin_user_role_update(request: Request, user_id: int):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    form = await request.form()
    role = _normalize_text(form.get("role"))
    try:
        update_user_role(user_id=user_id, new_role=role, settings=settings)
    except AuthNotFoundError:
        raise HTTPException(status_code=404, detail="user not found")
    except RoleError as exc:
        return _role_error_response(str(exc))
    return _admin_users_redirect(request)


@router.post("/admin/users/{user_id}/materials-access/grant")
def admin_user_materials_access_grant(request: Request, user_id: int):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    try:
        set_user_materials_access(user_id=user_id, granted=True, settings=settings)
    except AuthNotFoundError as exc:
        raise HTTPException(status_code=404, detail="user not found") from exc
    return _admin_users_redirect(request)


@router.post("/admin/users/{user_id}/materials-access/revoke")
def admin_user_materials_access_revoke(request: Request, user_id: int):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    try:
        set_user_materials_access(user_id=user_id, granted=False, settings=settings)
    except AuthNotFoundError as exc:
        raise HTTPException(status_code=404, detail="user not found") from exc
    return _admin_users_redirect(request)


@router.api_route("/admin/tariffs", methods=["GET", "HEAD"], response_class=HTMLResponse)
def admin_tariffs(request: Request):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    return _template(
        request,
        "tariffs.html",
        title=page_title("Тарифы"),
        tariffs=_tariffs_for_admin(settings=settings),
    )


@router.api_route("/admin/tariffs/new", methods=["GET", "HEAD"], response_class=HTMLResponse)
def admin_tariffs_new(request: Request):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    return _render_tariff_form(request, mode="create", form_data=_empty_tariff_form_data())


@router.post("/admin/tariffs/new", response_class=HTMLResponse)
async def admin_tariffs_new_submit(request: Request):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response

    form = await request.form()
    payload, errors = _validate_tariff_form_input(
        raw_code=form.get("code"),
        raw_title=form.get("title"),
        raw_description=form.get("description"),
        raw_price_rub=form.get("price_rub"),
        raw_currency=form.get("currency"),
        raw_status=form.get("status"),
        raw_show_on_homepage=form.get("show_on_homepage"),
        raw_sort_order=form.get("sort_order"),
        include_code=True,
    )
    if errors:
        return _render_tariff_form(
            request,
            mode="create",
            form_data=_tariff_form_data_from_form(form),
            errors=errors,
            status_code=400,
        )

    try:
        create_tariff(data=TariffCreateInput(**payload), settings=settings)
    except TariffConflictError as exc:
        errors = _tariff_form_errors_from_service(exc)
        return _render_tariff_form(
            request,
            mode="create",
            form_data=_tariff_form_data_from_form(form),
            errors=errors,
            status_code=400,
        )
    except TariffValidationError as exc:
        errors = _tariff_form_errors_from_service(exc)
        return _render_tariff_form(
            request,
            mode="create",
            form_data=_tariff_form_data_from_form(form),
            errors=errors,
            status_code=400,
        )

    return RedirectResponse(url="/admin/tariffs", status_code=303)


@router.api_route("/admin/tariffs/{code}/edit", methods=["GET", "HEAD"], response_class=HTMLResponse)
def admin_tariffs_edit(request: Request, code: str):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response

    tariff = get_tariff_by_code(code, settings=settings)
    if tariff is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return _render_tariff_form(request, mode="edit", form_data=_tariff_form_data_from_tariff(tariff), tariff=tariff)


@router.post("/admin/tariffs/{code}/edit", response_class=HTMLResponse)
async def admin_tariffs_edit_submit(request: Request, code: str):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response

    tariff = get_tariff_by_code(code, settings=settings)
    if tariff is None:
        raise HTTPException(status_code=404, detail="Not Found")

    form = await request.form()
    payload, errors = _validate_tariff_form_input(
        raw_title=form.get("title"),
        raw_description=form.get("description"),
        raw_price_rub=form.get("price_rub"),
        raw_currency=form.get("currency"),
        raw_status=form.get("status"),
        raw_show_on_homepage=form.get("show_on_homepage"),
        raw_sort_order=form.get("sort_order"),
        include_code=False,
    )
    posted_code = _normalize_text(form.get("code")).lower()
    if posted_code and posted_code != tariff.code:
        errors["code"] = "Системный код нельзя изменить после создания."
    if errors:
        return _render_tariff_form(
            request,
            mode="edit",
            form_data={**_tariff_form_data_from_tariff(tariff), **_tariff_form_data_from_form(form)},
            tariff=tariff,
            errors=errors,
            status_code=400,
        )

    try:
        update_tariff(
            code=tariff.code,
            data=TariffUpdateInput(
                title=payload["title"],
                description=payload["description"],
                price_amount_minor=payload["price_amount_minor"],
                currency=payload["currency"],
                status=payload["status"],
                show_on_homepage=payload["show_on_homepage"],
                sort_order=payload["sort_order"],
            ),
            settings=settings,
        )
    except TariffNotFoundError:
        raise HTTPException(status_code=404, detail="Not Found")
    except (TariffConflictError, TariffValidationError) as exc:
        errors = _tariff_form_errors_from_service(exc)
        return _render_tariff_form(
            request,
            mode="edit",
            form_data={**_tariff_form_data_from_tariff(tariff), **_tariff_form_data_from_form(form)},
            tariff=tariff,
            errors=errors,
            status_code=400,
        )

    return RedirectResponse(url="/admin/tariffs", status_code=303)


@router.post("/admin/tariffs/{code}/archive")
def admin_tariffs_archive(request: Request, code: str):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    try:
        archive_tariff(code, settings=settings)
    except TariffNotFoundError:
        raise HTTPException(status_code=404, detail="Not Found")
    return RedirectResponse(url="/admin/tariffs", status_code=303)


def _tariff_option_link_errors_from_service(exc: Exception) -> dict[str, str]:
    message = str(exc)
    lowered = message.lower()
    if "archived paid option" in lowered:
        return {"option_code": "Архивные опции нельзя добавлять к тарифу."}
    if "paid option" in lowered or "option" in lowered:
        return {"option_code": "Платная опция не найдена или недоступна для добавления."}
    if "included_duration_days" in lowered:
        return {"included_duration_days": "Включённый срок должен быть целым числом не меньше 0."}
    if "included_quantity" in lowered:
        return {"included_quantity": "Включённое количество должно быть целым числом не меньше 0."}
    return {"form": "Не удалось изменить связь тарифа и опции."}


@router.api_route("/admin/tariffs/{code}/options", methods=["GET", "HEAD"], response_class=HTMLResponse)
def admin_tariff_options(request: Request, code: str):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response

    tariff = get_tariff_by_code(code, settings=settings)
    if tariff is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return _render_tariff_options_page(request, settings, tariff)


@router.post("/admin/tariffs/{code}/options/attach", response_class=HTMLResponse)
async def admin_tariff_options_attach(request: Request, code: str):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response

    tariff = get_tariff_by_code(code, settings=settings)
    if tariff is None:
        raise HTTPException(status_code=404, detail="Not Found")

    form = await request.form()
    payload, errors = _validate_tariff_option_link_form_input(
        raw_option_code=form.get("option_code"),
        raw_included_duration_days=form.get("included_duration_days"),
        raw_included_quantity=form.get("included_quantity"),
        include_option_code=True,
    )
    if errors:
        return _render_tariff_options_page(
            request,
            settings,
            tariff,
            attach_form_data=payload,
            errors=errors,
            status_code=400,
        )

    try:
        attach_option_to_tariff(
            code,
            payload["option_code"],
            included_duration_days=None if payload["included_duration_days"] == "" else int(payload["included_duration_days"]),
            included_quantity=None if payload["included_quantity"] == "" else int(payload["included_quantity"]),
            settings=settings,
        )
    except TariffNotFoundError:
        raise HTTPException(status_code=404, detail="Not Found")
    except TariffValidationError as exc:
        errors = _tariff_option_link_errors_from_service(exc)
        return _render_tariff_options_page(
            request,
            settings,
            tariff,
            attach_form_data=payload,
            errors=errors,
            status_code=400,
        )

    return RedirectResponse(url=f"/admin/tariffs/{tariff.code}/options", status_code=303)


@router.post("/admin/tariffs/{code}/options/{option_code}/update", response_class=HTMLResponse)
async def admin_tariff_options_update(request: Request, code: str, option_code: str):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response

    tariff = get_tariff_by_code(code, settings=settings)
    if tariff is None:
        raise HTTPException(status_code=404, detail="Not Found")

    form = await request.form()
    payload, errors = _validate_tariff_option_link_form_input(
        raw_included_duration_days=form.get("included_duration_days"),
        raw_included_quantity=form.get("included_quantity"),
        include_option_code=False,
    )
    if errors:
        return _render_tariff_options_page(
            request,
            settings,
            tariff,
            errors=errors,
            link_overrides={
                option_code: {
                    "included_duration_days": payload["included_duration_days"],
                    "included_quantity": payload["included_quantity"],
                }
            },
            status_code=400,
        )

    try:
        update_tariff_option_link(
            code,
            option_code,
            included_duration_days=None if payload["included_duration_days"] == "" else int(payload["included_duration_days"]),
            included_quantity=None if payload["included_quantity"] == "" else int(payload["included_quantity"]),
            settings=settings,
        )
    except TariffNotFoundError:
        raise HTTPException(status_code=404, detail="Not Found")
    except TariffValidationError as exc:
        errors = _tariff_option_link_errors_from_service(exc)
        return _render_tariff_options_page(
            request,
            settings,
            tariff,
            errors=errors,
            link_overrides={
                option_code: {
                    "included_duration_days": payload["included_duration_days"],
                    "included_quantity": payload["included_quantity"],
                }
            },
            status_code=400,
        )

    return RedirectResponse(url=f"/admin/tariffs/{tariff.code}/options", status_code=303)


@router.post("/admin/tariffs/{code}/options/{option_code}/detach")
def admin_tariff_options_detach(request: Request, code: str, option_code: str):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response

    tariff = get_tariff_by_code(code, settings=settings)
    if tariff is None:
        raise HTTPException(status_code=404, detail="Not Found")

    try:
        detached = detach_option_from_tariff(code, option_code, settings=settings)
    except TariffNotFoundError:
        raise HTTPException(status_code=404, detail="Not Found")
    if not detached:
        raise HTTPException(status_code=404, detail="Not Found")

    return RedirectResponse(url=f"/admin/tariffs/{tariff.code}/options", status_code=303)


@router.api_route("/admin/paid-options", methods=["GET", "HEAD"], response_class=HTMLResponse)
def admin_paid_options(request: Request):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    return _template(
        request,
        "paid_options.html",
        title=page_title("Платные опции"),
        paid_options=_paid_options_for_admin(settings=settings),
    )


@router.api_route("/admin/paid-options/new", methods=["GET", "HEAD"], response_class=HTMLResponse)
def admin_paid_options_new(request: Request):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    return _template(
        request,
        "paid_option_form.html",
        title=page_title("Создать платную опцию"),
        mode="create",
        is_create=True,
        option=None,
        form_data=_empty_paid_option_form_data(),
        errors={},
        submit_label="Создать платную опцию",
    )


@router.post("/admin/paid-options/new", response_class=HTMLResponse)
async def admin_paid_options_new_submit(request: Request):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response

    form = await request.form()
    payload, errors = _validate_paid_option_form_input(
        raw_code=form.get("code"),
        raw_title=form.get("title"),
        raw_description=form.get("description"),
        raw_price_rub=form.get("price_rub"),
        raw_currency=form.get("currency"),
        raw_default_duration_days=form.get("default_duration_days"),
        raw_status=form.get("status"),
        raw_is_renewable=form.get("is_renewable"),
        raw_sort_order=form.get("sort_order"),
        include_code=True,
    )
    if errors:
        return _template(
            request,
            "paid_option_form.html",
            status_code=400,
            title=page_title("Создать платную опцию"),
            mode="create",
            is_create=True,
            option=None,
            form_data=_paid_option_form_data_from_form(form),
            errors=errors,
            submit_label="Создать платную опцию",
        )

    try:
        create_paid_option(data=PaidOptionCreateInput(**payload), settings=settings)
    except PaidOptionConflictError as exc:
        errors = _paid_option_form_errors_from_service(exc)
        return _template(
            request,
            "paid_option_form.html",
            status_code=400,
            title=page_title("Создать платную опцию"),
            mode="create",
            is_create=True,
            option=None,
            form_data=_paid_option_form_data_from_form(form),
            errors=errors,
            submit_label="Создать платную опцию",
        )
    except PaidOptionValidationError as exc:
        errors = _paid_option_form_errors_from_service(exc)
        return _template(
            request,
            "paid_option_form.html",
            status_code=400,
            title=page_title("Создать платную опцию"),
            mode="create",
            is_create=True,
            option=None,
            form_data=_paid_option_form_data_from_form(form),
            errors=errors,
            submit_label="Создать платную опцию",
        )

    return RedirectResponse(url="/admin/paid-options", status_code=303)


@router.api_route("/admin/paid-options/{code}/edit", methods=["GET", "HEAD"], response_class=HTMLResponse)
def admin_paid_options_edit(request: Request, code: str):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response

    option = get_paid_option_by_code(code, settings=settings)
    if option is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return _template(
        request,
        "paid_option_form.html",
        title=page_title("Редактировать платную опцию"),
        mode="edit",
        is_create=False,
        option=option,
        form_data=_paid_option_form_data_from_option(option),
        errors={},
        submit_label="Сохранить изменения",
    )


@router.post("/admin/paid-options/{code}/edit", response_class=HTMLResponse)
async def admin_paid_options_edit_submit(request: Request, code: str):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response

    option = get_paid_option_by_code(code, settings=settings)
    if option is None:
        raise HTTPException(status_code=404, detail="Not Found")

    form = await request.form()
    payload, errors = _validate_paid_option_form_input(
        raw_title=form.get("title"),
        raw_description=form.get("description"),
        raw_price_rub=form.get("price_rub"),
        raw_currency=form.get("currency"),
        raw_default_duration_days=form.get("default_duration_days"),
        raw_status=form.get("status"),
        raw_is_renewable=form.get("is_renewable"),
        raw_sort_order=form.get("sort_order"),
        include_code=False,
    )
    posted_code = _normalize_text(form.get("code")).lower()
    if posted_code and posted_code != option.code:
        errors["code"] = "Системный код нельзя изменить после создания."
    if errors:
        return _template(
            request,
            "paid_option_form.html",
            status_code=400,
            title=page_title("Редактировать платную опцию"),
            mode="edit",
            is_create=False,
            option=option,
            form_data={**_paid_option_form_data_from_option(option), **_paid_option_form_data_from_form(form)},
            errors=errors,
            submit_label="Сохранить изменения",
        )

    try:
        update_paid_option(
            code=option.code,
            data=PaidOptionUpdateInput(
                title=payload["title"],
                description=payload["description"],
                price_amount_minor=payload["price_amount_minor"],
                currency=payload["currency"],
                default_duration_days=payload["default_duration_days"],
                status=payload["status"],
                is_renewable=payload["is_renewable"],
                sort_order=payload["sort_order"],
            ),
            settings=settings,
        )
    except PaidOptionNotFoundError:
        raise HTTPException(status_code=404, detail="Not Found")
    except (PaidOptionConflictError, PaidOptionValidationError) as exc:
        errors = _paid_option_form_errors_from_service(exc)
        return _template(
            request,
            "paid_option_form.html",
            status_code=400,
            title=page_title("Редактировать платную опцию"),
            mode="edit",
            is_create=False,
            option=option,
            form_data={**_paid_option_form_data_from_option(option), **_paid_option_form_data_from_form(form)},
            errors=errors,
            submit_label="Сохранить изменения",
        )

    return RedirectResponse(url="/admin/paid-options", status_code=303)


@router.post("/admin/paid-options/{code}/archive")
def admin_paid_options_archive(request: Request, code: str):
    settings = get_settings()
    _, response = _admin_user_or_redirect(request, settings=settings)
    if response is not None:
        return response
    try:
        archive_paid_option(code, settings=settings)
    except PaidOptionNotFoundError:
        raise HTTPException(status_code=404, detail="Not Found")
    return RedirectResponse(url="/admin/paid-options", status_code=303)
```

```diff
diff --git a/source/app/admin/routes.py b/source/app/admin/routes.py
index fdbd980..4b44d30 100644
--- a/source/app/admin/routes.py
+++ b/source/app/admin/routes.py
@@ -20,6 +20,7 @@ from app.auth.service import (
     RoleError,
     get_user_by_session_token,
     list_users_for_admin,
+    set_user_materials_access,
     update_user_role,
 )
 from app.admin.course_export import build_course_export
@@ -148,6 +149,13 @@ def _role_error_response(message: str) -> PlainTextResponse:
     return PlainTextResponse(text, status_code=400)
 
 
+def _admin_users_redirect(request: Request) -> RedirectResponse:
+    redirect_url = "/admin/users"
+    if request.url.query:
+        redirect_url = f"{redirect_url}?{request.url.query}"
+    return RedirectResponse(url=redirect_url, status_code=303)
+
+
 def _template(request: Request, template_name: str, **context) -> HTMLResponse:
     status_code = context.pop("status_code", 200)
     payload = {"request": request, "title": context.pop("title", page_title("AI Starter Community"))}
@@ -187,6 +195,7 @@ def _empty_tariff_form_data() -> dict[str, str]:
         "price_rub": "",
         "currency": "RUB",
         "status": "active",
+        "show_on_homepage": "0",
         "sort_order": "0",
     }
 
@@ -199,6 +208,7 @@ def _tariff_form_data_from_tariff(tariff) -> dict[str, str]:
         "price_rub": _format_price_input(tariff.price_amount_minor),
         "currency": tariff.currency,
         "status": tariff.status,
+        "show_on_homepage": "1" if tariff.show_on_homepage else "0",
         "sort_order": str(tariff.sort_order),
     }
 
@@ -211,6 +221,7 @@ def _tariff_form_data_from_form(form) -> dict[str, str]:
         "price_rub": _normalize_text(form.get("price_rub")),
         "currency": _normalize_text(form.get("currency")) or "RUB",
         "status": _normalize_text(form.get("status")) or "active",
+        "show_on_homepage": "1" if _checkbox_is_true(form.get("show_on_homepage")) else "0",
         "sort_order": _normalize_text(form.get("sort_order")) or "0",
     }
 
@@ -296,6 +307,7 @@ def _validate_tariff_form_input(
     raw_price_rub: str | None = None,
     raw_currency: str | None = None,
     raw_status: str | None = None,
+    raw_show_on_homepage=None,
     raw_sort_order: str | None = None,
     include_code: bool = True,
 ) -> tuple[dict[str, object], dict[str, str]]:
@@ -306,6 +318,7 @@ def _validate_tariff_form_input(
     price_minor, price_error = _parse_positive_money_to_minor(raw_price_rub)
     currency = (_normalize_text(raw_currency) or "RUB").upper()
     status = (_normalize_text(raw_status) or "active").lower()
+    show_on_homepage = _checkbox_is_true(raw_show_on_homepage)
     sort_order, sort_error = _parse_non_negative_int(raw_sort_order, "sort_order")
 
     if include_code:
@@ -344,6 +357,7 @@ def _validate_tariff_form_input(
         "price_amount_minor": price_minor,
         "currency": currency,
         "status": status,
+        "show_on_homepage": show_on_homepage,
         "sort_order": sort_order if sort_order is not None else 0,
     }
     return payload, errors
@@ -637,6 +651,7 @@ def _tariffs_for_admin(settings):
                 "price_display": _format_minor_amount(tariff.price_amount_minor),
                 "currency": tariff.currency,
                 "status_label": _status_label(tariff.status),
+                "show_on_homepage_label": "Да" if tariff.show_on_homepage else "Нет",
                 "sort_order": tariff.sort_order,
                 "included_options_summary": ", ".join(option["title"] for option in linked_options) if linked_options else "—",
                 "created_at": tariff.created_at,
@@ -775,10 +790,33 @@ async def admin_user_role_update(request: Request, user_id: int):
         raise HTTPException(status_code=404, detail="user not found")
     except RoleError as exc:
         return _role_error_response(str(exc))
-    redirect_url = "/admin/users"
-    if request.url.query:
-        redirect_url = f"{redirect_url}?{request.url.query}"
-    return RedirectResponse(url=redirect_url, status_code=303)
+    return _admin_users_redirect(request)
+
+
+@router.post("/admin/users/{user_id}/materials-access/grant")
+def admin_user_materials_access_grant(request: Request, user_id: int):
+    settings = get_settings()
+    _, response = _admin_user_or_redirect(request, settings=settings)
+    if response is not None:
+        return response
+    try:
+        set_user_materials_access(user_id=user_id, granted=True, settings=settings)
+    except AuthNotFoundError as exc:
+        raise HTTPException(status_code=404, detail="user not found") from exc
+    return _admin_users_redirect(request)
+
+
+@router.post("/admin/users/{user_id}/materials-access/revoke")
+def admin_user_materials_access_revoke(request: Request, user_id: int):
+    settings = get_settings()
+    _, response = _admin_user_or_redirect(request, settings=settings)
+    if response is not None:
+        return response
+    try:
+        set_user_materials_access(user_id=user_id, granted=False, settings=settings)
+    except AuthNotFoundError as exc:
+        raise HTTPException(status_code=404, detail="user not found") from exc
+    return _admin_users_redirect(request)
 
 
 @router.api_route("/admin/tariffs", methods=["GET", "HEAD"], response_class=HTMLResponse)
@@ -819,6 +857,7 @@ async def admin_tariffs_new_submit(request: Request):
         raw_price_rub=form.get("price_rub"),
         raw_currency=form.get("currency"),
         raw_status=form.get("status"),
+        raw_show_on_homepage=form.get("show_on_homepage"),
         raw_sort_order=form.get("sort_order"),
         include_code=True,
     )
@@ -886,6 +925,7 @@ async def admin_tariffs_edit_submit(request: Request, code: str):
         raw_price_rub=form.get("price_rub"),
         raw_currency=form.get("currency"),
         raw_status=form.get("status"),
+        raw_show_on_homepage=form.get("show_on_homepage"),
         raw_sort_order=form.get("sort_order"),
         include_code=False,
     )
@@ -911,6 +951,7 @@ async def admin_tariffs_edit_submit(request: Request, code: str):
                 price_amount_minor=payload["price_amount_minor"],
                 currency=payload["currency"],
                 status=payload["status"],
+                show_on_homepage=payload["show_on_homepage"],
                 sort_order=payload["sort_order"],
             ),
             settings=settings,
```


### source/app/admin/templates/users.html

```html
{% extends "base.html" %}

{% block content %}
  <section class="card stack">
    <div class="stack">
      <p class="muted">Просмотр безопасных данных</p>
      <h1 class="section-title">Пользователи</h1>
      <p class="form-help">Показаны только безопасные поля учётных записей. Через эту страницу можно назначать и убирать модераторов, а также выдавать и отзывать платный доступ.</p>
    </div>

    <form class="stack" method="get" action="/admin/users">
      <div class="card-grid tight">
        <label class="form-row">
          <span>Дата регистрации с</span>
          <input class="input" type="date" name="created_from" value="{{ created_from_value or '' }}">
        </label>
        <label class="form-row">
          <span>Дата регистрации по</span>
          <input class="input" type="date" name="created_to" value="{{ created_to_value or '' }}">
        </label>
        <label class="form-row">
          <span>Роль</span>
          <select class="select" name="role">
            <option value="all" {% if filter_role == "all" %}selected{% endif %}>Все роли</option>
            <option value="user" {% if filter_role == "user" %}selected{% endif %}>Пользователь</option>
            <option value="moderator" {% if filter_role == "moderator" %}selected{% endif %}>Модератор</option>
            <option value="admin" {% if filter_role == "admin" %}selected{% endif %}>Администратор</option>
          </select>
        </label>
        <label class="form-row">
          <span>Статус доступа</span>
          <select class="select" name="access_status">
            <option value="all" {% if filter_access_status == "all" %}selected{% endif %}>Все статусы</option>
            <option value="not_activated" {% if filter_access_status == "not_activated" %}selected{% endif %}>Не активирован</option>
            <option value="activated" {% if filter_access_status == "activated" %}selected{% endif %}>Активирован</option>
          </select>
        </label>
        <label class="form-row">
          <span>Сортировка по дате регистрации</span>
          <select class="select" name="created_sort">
            <option value="desc" {% if created_sort == "desc" %}selected{% endif %}>Сначала новые</option>
            <option value="asc" {% if created_sort == "asc" %}selected{% endif %}>Сначала старые</option>
          </select>
        </label>
      </div>

      <div class="actions">
        <button class="button button-primary" type="submit">Применить фильтр</button>
        <a class="button button-secondary" href="/admin/users">Сбросить</a>
      </div>
    </form>

    <table class="table">
      <thead>
        <tr>
          <th>Идентификатор</th>
          <th>Электронная почта</th>
          <th>Логин</th>
          <th>Роль</th>
          <th>Изменить роль</th>
          <th>Активен</th>
          <th>Подтверждён email</th>
          <th>Статус доступа</th>
          <th>Доступ к материалам</th>
          <th>Создан</th>
          <th>Обновлён</th>
        </tr>
      </thead>
      <tbody>
        {% for user in users %}
          <tr>
            <td>{{ user.id }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.login }}</td>
            <td>
              {{ user.role_label }}
            </td>
            <td>
              <form class="compact-form" method="post" action="/admin/users/{{ user.id }}/role{% if query_string %}?{{ query_string }}{% endif %}">
                <label class="form-row">
                  <span class="muted">Роль</span>
                  <select class="select" name="role">
                    {% for role in allowed_roles %}
                      <option value="{{ role }}" {% if user.role == role %}selected{% endif %}>{{ role_labels[role] }}</option>
                    {% endfor %}
                  </select>
                </label>
                <button class="button button-secondary" type="submit">Сохранить роль</button>
              </form>
            </td>
            <td>{{ "да" if user.is_active else "нет" }}</td>
            <td>{{ "подтверждён" if user.email_verified else "не подтверждён" }}</td>
            <td>
              <div class="stack">
                <span class="badge {% if user.materials_access_granted %}badge-success{% else %}badge-muted{% endif %}">
                  {% if user.materials_access_granted %}Доступ выдан{% else %}Доступ не выдан{% endif %}
                </span>
                {% if user.materials_access_granted %}
                  <form class="compact-form" method="post" action="/admin/users/{{ user.id }}/materials-access/revoke{% if query_string %}?{{ query_string }}{% endif %}">
                    <button class="button button-secondary" type="submit">Отозвать доступ</button>
                  </form>
                {% else %}
                  <form class="compact-form" method="post" action="/admin/users/{{ user.id }}/materials-access/grant{% if query_string %}?{{ query_string }}{% endif %}">
                    <button class="button button-primary" type="submit">Выдать доступ</button>
                  </form>
                {% endif %}
              </div>
            </td>
            <td>{{ user.created_at }}</td>
            <td>{{ user.updated_at }}</td>
          </tr>
        {% else %}
          <tr>
            <td colspan="11">Пользователей пока нет.</td>
          </tr>
        {% endfor %}
      </tbody>
    </table>
  </section>
{% endblock %}
```

```diff
diff --git a/source/app/admin/templates/users.html b/source/app/admin/templates/users.html
index 135f87d..cb72162 100644
--- a/source/app/admin/templates/users.html
+++ b/source/app/admin/templates/users.html
@@ -5,7 +5,7 @@
     <div class="stack">
       <p class="muted">Просмотр безопасных данных</p>
       <h1 class="section-title">Пользователи</h1>
-      <p class="form-help">Показаны только безопасные поля учётных записей.</p>
+      <p class="form-help">Показаны только безопасные поля учётных записей. Через эту страницу можно назначать и убирать модераторов, а также выдавать и отзывать платный доступ.</p>
     </div>
 
     <form class="stack" method="get" action="/admin/users">
@@ -91,17 +91,21 @@
             <td>{{ "да" if user.is_active else "нет" }}</td>
             <td>{{ "подтверждён" if user.email_verified else "не подтверждён" }}</td>
             <td>
-              {% if user.access_status == "not_activated" %}
-                не активирован
-              {% elif user.access_status == "activated" %}
-                активирован
-              {% elif user.access_status == "blocked" %}
-                заблокирован
-              {% else %}
-                {{ user.access_status }}
-              {% endif %}
+              <div class="stack">
+                <span class="badge {% if user.materials_access_granted %}badge-success{% else %}badge-muted{% endif %}">
+                  {% if user.materials_access_granted %}Доступ выдан{% else %}Доступ не выдан{% endif %}
+                </span>
+                {% if user.materials_access_granted %}
+                  <form class="compact-form" method="post" action="/admin/users/{{ user.id }}/materials-access/revoke{% if query_string %}?{{ query_string }}{% endif %}">
+                    <button class="button button-secondary" type="submit">Отозвать доступ</button>
+                  </form>
+                {% else %}
+                  <form class="compact-form" method="post" action="/admin/users/{{ user.id }}/materials-access/grant{% if query_string %}?{{ query_string }}{% endif %}">
+                    <button class="button button-primary" type="submit">Выдать доступ</button>
+                  </form>
+                {% endif %}
+              </div>
             </td>
-            <td>{{ "да" if user.materials_access_granted else "нет" }}</td>
             <td>{{ user.created_at }}</td>
             <td>{{ user.updated_at }}</td>
           </tr>
```


### source/app/auth/service.py

```py
"""Authentication service layer for registration, login, tokens, and sessions."""

from __future__ import annotations

import re
from datetime import date, datetime, time, timedelta, timezone
from collections.abc import Mapping

from app.auth.schemas import UserPublic
from app.core.config import Settings, get_settings
from app.notifications.email_service import (
    EmailConfigError,
    EmailDeliveryError,
    EmailModeError,
    send_email_verification,
    send_password_reset,
)
from app.shared.db import get_connection, get_database_path, initialize_database
from app.shared.security import (
    generate_auth_token,
    generate_session_token,
    hash_password,
    hash_token,
    validate_new_password,
    verify_password,
)
from app.shared.utils import utc_now, utc_now_iso


EMAIL_TOKEN_TYPE = "email_verification"
PASSWORD_RESET_TOKEN_TYPE = "password_reset"
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
LOGIN_RE = re.compile(r"^[a-z0-9_-]{3,32}$")
ROLE_USER = "user"
ROLE_MODERATOR = "moderator"
ROLE_ADMIN = "admin"
ALLOWED_ROLES = (ROLE_USER, ROLE_MODERATOR, ROLE_ADMIN)
ALLOWED_ADMIN_USER_ACCESS_STATUSES = ("not_activated", "activated")
ALLOWED_ADMIN_USER_SORT_ORDERS = ("desc", "asc")
ADMIN_USER_DEFAULT_SORT = "desc"
ROLE_LABELS_RU = {
    ROLE_USER: "пользователь",
    ROLE_MODERATOR: "модератор",
    ROLE_ADMIN: "администратор",
}
EMAIL_DELIVERY_FAILURE_MESSAGE_RU = "Не удалось отправить письмо. Попробуйте позже."


class AuthError(Exception):
    """Base class for auth-domain errors."""


class ValidationError(AuthError):
    pass


class ConflictError(AuthError):
    pass


class UnauthorizedError(AuthError):
    pass


class NotVerifiedError(AuthError):
    pass


class NotFoundError(AuthError):
    pass


class RoleError(AuthError):
    pass


def _settings(settings: Settings | None = None) -> Settings:
    return settings or get_settings()


def _database_path(settings: Settings | None = None):
    return get_database_path(_settings(settings))


def _connection(settings: Settings | None = None):
    resolved = _settings(settings)
    path = _database_path(resolved)
    initialize_database(path)
    return get_connection(path)


def _public_user_from_row(row) -> UserPublic:
    return UserPublic(
        id=int(row["id"]),
        email=str(row["email"]),
        login=str(row["login"]),
        role=str(row["role"]),
        is_active=bool(row["is_active"]),
        access_status=str(row["access_status"]),
        email_verified_at=row["email_verified_at"],
        materials_access_granted_at=row["materials_access_granted_at"],
    )


def _normalize_email(value: str) -> str:
    normalized = (value or "").strip().lower()
    if not normalized:
        raise ValidationError("email is required")
    if not EMAIL_RE.fullmatch(normalized):
        raise ValidationError("invalid email")
    return normalized


def _normalize_login(value: str) -> str:
    normalized = (value or "").strip().lower()
    if not normalized:
        raise ValidationError("login is required")
    if not LOGIN_RE.fullmatch(normalized):
        raise ValidationError("login must use lowercase letters, digits, underscore or hyphen")
    return normalized


def _normalize_identifier(value: str) -> tuple[str, str]:
    raw_value = (value or "").strip()
    if not raw_value:
        raise ValidationError("email or login is required")
    if "@" in raw_value:
        return "email", _normalize_email(raw_value)
    return "login", _normalize_login(raw_value)


def _normalize_password_for_login(password: str) -> str:
    return validate_new_password(password)


def _passwords_match(password: str, repeat_password: str) -> str:
    try:
        normalized_password = validate_new_password(password)
        normalized_repeat = validate_new_password(repeat_password)
    except ValueError as exc:
        raise ValidationError(str(exc)) from exc
    if normalized_password != normalized_repeat:
        raise ValidationError("passwords do not match")
    return normalized_password


def normalize_role(value: str) -> str:
    normalized = (value or "").strip().lower()
    if normalized not in ALLOWED_ROLES:
        raise RoleError("unsupported role")
    return normalized


def role_label_ru(role: str) -> str:
    return ROLE_LABELS_RU.get(role, role)


def is_admin_role(role: str) -> bool:
    return role == ROLE_ADMIN


def has_staff_materials_access(role: str) -> bool:
    return role in {ROLE_ADMIN, ROLE_MODERATOR}


def user_can_access_materials(user: UserPublic | None) -> bool:
    return bool(
        user
        and (
            user.materials_access_granted_at is not None
            or has_staff_materials_access(user.role)
        )
    )


def can_manage_account_blocks(user: UserPublic | None) -> bool:
    return bool(user and has_staff_materials_access(user.role))


def _build_public_url(settings: Settings, path: str) -> str:
    base_url = settings.base_url.rstrip("/")
    if not path.startswith("/"):
        path = f"/{path}"
    return f"{base_url}{path}"


def _raise_email_delivery_error(exc: Exception) -> None:
    raise AuthError(EMAIL_DELIVERY_FAILURE_MESSAGE_RU) from exc


def _issue_auth_token(
    connection,
    user_id: int,
    token_type: str,
    expires_at_iso: str,
    target_email: str | None = None,
) -> str:
    raw_token = generate_auth_token()
    connection.execute(
        """
        INSERT INTO auth_tokens (
            user_id, token_hash, token_type, target_email,
            created_at, expires_at, used_at, revoked_at
        )
        VALUES (?, ?, ?, ?, ?, ?, NULL, NULL)
        """,
        (
            user_id,
            hash_token(raw_token),
            token_type,
            target_email,
            utc_now_iso(),
            expires_at_iso,
        ),
    )
    return raw_token


def _fetch_user_by_id(user_id: int, settings: Settings | None = None) -> UserPublic | None:
    with _connection(settings) as connection:
        row = connection.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return _public_user_from_row(row) if row else None


def get_user_by_email(email: str, settings: Settings | None = None) -> UserPublic | None:
    normalized_email = _normalize_email(email)
    with _connection(settings) as connection:
        row = connection.execute("SELECT * FROM users WHERE email = ?", (normalized_email,)).fetchone()
        return _public_user_from_row(row) if row else None


def get_current_user_from_cookies(
    cookies: Mapping[str, str],
    settings: Settings | None = None,
) -> UserPublic | None:
    resolved = _settings(settings)
    session_token = cookies.get(resolved.session_cookie_name)
    if not session_token:
        return None
    return get_user_by_session_token(session_token, settings=resolved)


def _admin_user_from_row(row) -> dict[str, object]:
    role = str(row["role"])
    return {
        "id": int(row["id"]),
        "email": str(row["email"]),
        "login": str(row["login"]),
        "role": role,
        "role_label": role_label_ru(role),
        "is_active": bool(row["is_active"]),
        "email_verified": row["email_verified_at"] is not None,
        "materials_access_granted": row["materials_access_granted_at"] is not None,
        "access_status": str(row["access_status"]),
        "created_at": str(row["created_at"]),
        "updated_at": str(row["updated_at"]),
    }


def _admin_user_created_bound(value: date, *, upper: bool = False) -> str:
    target_date = value + timedelta(days=1) if upper else value
    return datetime.combine(target_date, time.min, tzinfo=timezone.utc).isoformat()


def list_users_for_admin(
    settings: Settings | None = None,
    *,
    role: str | None = None,
    access_status: str | None = None,
    created_from: date | None = None,
    created_to: date | None = None,
    created_sort: str = ADMIN_USER_DEFAULT_SORT,
) -> list[dict[str, object]]:
    """Return a safe summary of users for admin read-only lists."""
    if role is not None and role not in ALLOWED_ROLES:
        raise RoleError("unsupported role")
    if access_status is not None and access_status not in ALLOWED_ADMIN_USER_ACCESS_STATUSES:
        raise ValidationError("unsupported access status")
    if created_sort not in ALLOWED_ADMIN_USER_SORT_ORDERS:
        raise ValidationError("unsupported created sort")

    where_clauses: list[str] = []
    params: list[object] = []
    if role is not None:
        where_clauses.append("role = ?")
        params.append(role)
    if access_status is not None:
        where_clauses.append("access_status = ?")
        params.append(access_status)
    if created_from is not None:
        where_clauses.append("julianday(created_at) >= julianday(?)")
        params.append(_admin_user_created_bound(created_from))
    if created_to is not None:
        where_clauses.append("julianday(created_at) < julianday(?)")
        params.append(_admin_user_created_bound(created_to, upper=True))

    where_sql = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""
    sort_sql = "DESC" if created_sort == "desc" else "ASC"
    with _connection(settings) as connection:
        rows = connection.execute(
            """
            SELECT
                id, email, login, role, is_active,
                email_verified_at, materials_access_granted_at,
                access_status, created_at, updated_at
            FROM users
            {where_sql}
            ORDER BY julianday(created_at) {sort_sql}, id {sort_sql}
            """.format(where_sql=where_sql, sort_sql=sort_sql),
            params,
        ).fetchall()
        return [_admin_user_from_row(row) for row in rows]


def _fetch_user_by_role_identifier(identifier_kind: str, identifier_value: str, settings: Settings | None = None):
    with _connection(settings) as connection:
        query = "SELECT * FROM users WHERE email = ?" if identifier_kind == "email" else "SELECT * FROM users WHERE login = ?"
        return connection.execute(query, (identifier_value,)).fetchone()


def _fetch_user_by_identifier(identifier_kind: str, identifier_value: str, settings: Settings | None = None):
    return _fetch_user_by_role_identifier(identifier_kind, identifier_value, settings=settings)


def promote_user_to_admin(
    *,
    identifier_kind: str,
    identifier_value: str,
    settings: Settings | None = None,
) -> UserPublic:
    resolved = _settings(settings)
    if identifier_kind not in {"email", "login"}:
        raise ValidationError("identifier_kind must be email or login")
    normalized_value = _normalize_email(identifier_value) if identifier_kind == "email" else _normalize_login(identifier_value)
    with _connection(resolved) as connection:
        row = connection.execute(
            "SELECT * FROM users WHERE email = ?" if identifier_kind == "email" else "SELECT * FROM users WHERE login = ?",
            (normalized_value,),
        ).fetchone()
        if row is None:
            raise NotFoundError("user not found")
        if str(row["role"]) not in ALLOWED_ROLES:
            raise RoleError("unsupported role")
        if is_admin_role(str(row["role"])):
            return _public_user_from_row(row)
        now_iso = utc_now_iso()
        connection.execute(
            "UPDATE users SET role = ?, updated_at = ? WHERE id = ?",
            (ROLE_ADMIN, now_iso, int(row["id"])),
        )
        updated = connection.execute("SELECT * FROM users WHERE id = ?", (int(row["id"]),)).fetchone()
        if updated is None:
            raise AuthError("role update failed")
        return _public_user_from_row(updated)


def update_user_role(
    *,
    user_id: int,
    new_role: str,
    settings: Settings | None = None,
) -> UserPublic:
    resolved = _settings(settings)
    normalized_role = normalize_role(new_role)
    with _connection(resolved) as connection:
        row = connection.execute("SELECT * FROM users WHERE id = ?", (int(user_id),)).fetchone()
        if row is None:
            raise NotFoundError("user not found")

        current_role = str(row["role"])
        if is_admin_role(current_role) and not is_admin_role(normalized_role):
            admin_count = int(
                connection.execute("SELECT COUNT(*) AS count FROM users WHERE role = ?", (ROLE_ADMIN,)).fetchone()["count"]
            )
            if admin_count <= 1:
                raise RoleError("last admin cannot be demoted")

        if current_role == normalized_role:
            return _public_user_from_row(row)

        now_iso = utc_now_iso()
        connection.execute(
            "UPDATE users SET role = ?, updated_at = ? WHERE id = ?",
            (normalized_role, now_iso, int(user_id)),
        )
        updated = connection.execute("SELECT * FROM users WHERE id = ?", (int(user_id),)).fetchone()
        if updated is None:
            raise AuthError("role update failed")
        return _public_user_from_row(updated)


def set_user_materials_access(
    *,
    user_id: int,
    granted: bool,
    settings: Settings | None = None,
) -> UserPublic:
    resolved = _settings(settings)
    target_access_status = "activated" if granted else "not_activated"
    target_granted_at = utc_now_iso() if granted else None
    with _connection(resolved) as connection:
        row = connection.execute("SELECT * FROM users WHERE id = ?", (int(user_id),)).fetchone()
        if row is None:
            raise NotFoundError("user not found")
        current_granted = row["materials_access_granted_at"] is not None
        current_access_status = str(row["access_status"])
        if current_granted == granted and current_access_status == target_access_status:
            return _public_user_from_row(row)

        now_iso = utc_now_iso()
        connection.execute(
            """
            UPDATE users
            SET materials_access_granted_at = ?, access_status = ?, updated_at = ?
            WHERE id = ?
            """,
            (target_granted_at, target_access_status, now_iso, int(user_id)),
        )
        updated = connection.execute("SELECT * FROM users WHERE id = ?", (int(user_id),)).fetchone()
        if updated is None:
            raise AuthError("materials access update failed")
        return _public_user_from_row(updated)


def register_user(
    email: str,
    login: str,
    password: str,
    repeat_password: str,
    settings: Settings | None = None,
) -> UserPublic:
    resolved = _settings(settings)
    normalized_email = _normalize_email(email)
    normalized_login = _normalize_login(login)
    normalized_password = _passwords_match(password, repeat_password)

    with _connection(resolved) as connection:
        existing = connection.execute(
            "SELECT id FROM users WHERE email = ? OR login = ?",
            (normalized_email, normalized_login),
        ).fetchone()
        if existing:
            raise ConflictError("email or login already exists")

        now_iso = utc_now_iso()
        password_hash = hash_password(normalized_password)
        cursor = connection.execute(
            """
            INSERT INTO users (
                email, login, password_hash, role, is_active,
                email_verified_at, access_status, created_at, updated_at
            )
            VALUES (?, ?, ?, 'user', 1, NULL, 'not_activated', ?, ?)
            """,
            (normalized_email, normalized_login, password_hash, now_iso, now_iso),
        )
        user_id = int(cursor.lastrowid)
        verification_token = _issue_auth_token(
            connection,
            user_id=user_id,
            token_type=EMAIL_TOKEN_TYPE,
            expires_at_iso=(utc_now() + timedelta(hours=resolved.email_verification_token_expiry_hours)).isoformat(),
            target_email=normalized_email,
        )

    verification_link = _build_public_url(resolved, f"/verify-email/{verification_token}")
    try:
        send_email_verification(normalized_email, verification_link, settings=resolved)
    except (EmailModeError, EmailConfigError, EmailDeliveryError) as exc:
        _raise_email_delivery_error(exc)
    user = _fetch_user_by_id(user_id, settings=resolved)
    if user is None:
        raise AuthError("registration succeeded but user lookup failed")
    return user


def resend_verification_request(email: str, settings: Settings | None = None) -> bool:
    resolved = _settings(settings)
    normalized_email = _normalize_email(email)
    with _connection(resolved) as connection:
        user_row = connection.execute(
            "SELECT * FROM users WHERE email = ?",
            (normalized_email,),
        ).fetchone()
        if user_row is None or not bool(user_row["is_active"]) or user_row["email_verified_at"] is not None:
            return False
        now_iso = utc_now_iso()
        connection.execute(
            """
            UPDATE auth_tokens
            SET revoked_at = ?
            WHERE user_id = ? AND token_type = ? AND used_at IS NULL AND revoked_at IS NULL
            """,
            (now_iso, int(user_row["id"]), EMAIL_TOKEN_TYPE),
        )
        verification_token = _issue_auth_token(
            connection,
            user_id=int(user_row["id"]),
            token_type=EMAIL_TOKEN_TYPE,
            expires_at_iso=(utc_now() + timedelta(hours=resolved.email_verification_token_expiry_hours)).isoformat(),
            target_email=normalized_email,
        )

    verification_link = _build_public_url(resolved, f"/verify-email/{verification_token}")
    try:
        send_email_verification(normalized_email, verification_link, settings=resolved)
    except (EmailModeError, EmailConfigError, EmailDeliveryError) as exc:
        _raise_email_delivery_error(exc)
    return True


def is_verification_resend_rate_limited(
    email: str,
    *,
    settings: Settings | None = None,
    cooldown_seconds: int = 60,
) -> bool:
    resolved = _settings(settings)
    normalized_email = _normalize_email(email)
    if cooldown_seconds <= 0:
        return False

    cooldown_started_at = utc_now() - timedelta(seconds=cooldown_seconds)
    with _connection(resolved) as connection:
        row = connection.execute(
            """
            SELECT created_at
            FROM auth_tokens
            WHERE token_type = ?
              AND target_email = ?
              AND created_at >= ?
            ORDER BY created_at DESC
            LIMIT 1
            """,
            (EMAIL_TOKEN_TYPE, normalized_email, cooldown_started_at.isoformat()),
        ).fetchone()
    return row is not None


def verify_email(token: str, settings: Settings | None = None) -> UserPublic:
    resolved = _settings(settings)
    token_hash = hash_token(token or "")
    now_iso = utc_now_iso()
    with _connection(resolved) as connection:
        row = connection.execute(
            """
            SELECT at.id AS token_id, at.user_id, u.id, u.email, u.login, u.role,
                   u.is_active, u.email_verified_at, u.access_status
            FROM auth_tokens AS at
            JOIN users AS u ON u.id = at.user_id
            WHERE at.token_hash = ?
              AND at.token_type = ?
              AND at.used_at IS NULL
              AND at.revoked_at IS NULL
              AND at.expires_at > ?
            """,
            (token_hash, EMAIL_TOKEN_TYPE, now_iso),
        ).fetchone()
        if not row:
            raise NotFoundError("verification token not found or expired")
        connection.execute(
            "UPDATE users SET email_verified_at = ?, updated_at = ? WHERE id = ?",
            (now_iso, now_iso, int(row["user_id"])),
        )
        connection.execute(
            "UPDATE auth_tokens SET used_at = ? WHERE id = ?",
            (now_iso, int(row["token_id"])),
        )
        user_row = connection.execute("SELECT * FROM users WHERE id = ?", (int(row["user_id"]),)).fetchone()
        if user_row is None:
            raise AuthError("verified user lookup failed")
        return _public_user_from_row(user_row)


def authenticate_user(email_or_login: str, password: str, settings: Settings | None = None) -> UserPublic:
    identifier_kind, identifier_value = _normalize_identifier(email_or_login)
    resolved = _settings(settings)
    user_row = _fetch_user_by_identifier(identifier_kind, identifier_value, settings=resolved)
    if user_row is None or not bool(user_row["is_active"]):
        raise UnauthorizedError("invalid credentials")
    if user_row["email_verified_at"] is None:
        raise NotVerifiedError("email is not verified")
    try:
        if not verify_password(password, str(user_row["password_hash"])):
            raise UnauthorizedError("invalid credentials")
    except ValueError as exc:
        raise ValidationError(str(exc)) from exc
    return _public_user_from_row(user_row)


def create_session(user_id: int, settings: Settings | None = None) -> str:
    resolved = _settings(settings)
    raw_token = generate_session_token()
    token_hash = hash_token(raw_token)
    now = utc_now()
    expires_at = now + timedelta(hours=resolved.session_expiry_hours)
    with _connection(resolved) as connection:
        connection.execute(
            """
            INSERT INTO sessions (
                user_id, token_hash, created_at, expires_at, revoked_at
            )
            VALUES (?, ?, ?, ?, NULL)
            """,
            (user_id, token_hash, now.isoformat(), expires_at.isoformat()),
        )
    return raw_token


def get_user_by_session_token(raw_token: str | None, settings: Settings | None = None) -> UserPublic | None:
    if not raw_token:
        return None
    resolved = _settings(settings)
    token_hash = hash_token(raw_token)
    now_iso = utc_now_iso()
    with _connection(resolved) as connection:
        row = connection.execute(
            """
            SELECT u.*
            FROM sessions AS s
            JOIN users AS u ON u.id = s.user_id
            WHERE s.token_hash = ?
              AND s.revoked_at IS NULL
              AND s.expires_at > ?
              AND u.is_active = 1
            """,
            (token_hash, now_iso),
        ).fetchone()
        return _public_user_from_row(row) if row else None


def revoke_session(raw_token: str | None, settings: Settings | None = None) -> bool:
    if not raw_token:
        return False
    resolved = _settings(settings)
    token_hash = hash_token(raw_token)
    now_iso = utc_now_iso()
    with _connection(resolved) as connection:
        cursor = connection.execute(
            """
            UPDATE sessions
            SET revoked_at = ?
            WHERE token_hash = ? AND revoked_at IS NULL
            """,
            (now_iso, token_hash),
        )
        return cursor.rowcount > 0


def create_password_reset_request(email: str, settings: Settings | None = None) -> bool:
    resolved = _settings(settings)
    normalized_email = _normalize_email(email)
    with _connection(resolved) as connection:
        user_row = connection.execute(
            "SELECT * FROM users WHERE email = ?",
            (normalized_email,),
        ).fetchone()
        if user_row is None or not bool(user_row["is_active"]) or user_row["email_verified_at"] is None:
            return False
        now_iso = utc_now_iso()
        connection.execute(
            """
            UPDATE auth_tokens
            SET revoked_at = ?
            WHERE user_id = ? AND token_type = ? AND used_at IS NULL AND revoked_at IS NULL
            """,
            (now_iso, int(user_row["id"]), PASSWORD_RESET_TOKEN_TYPE),
        )
        reset_token = _issue_auth_token(
            connection,
            user_id=int(user_row["id"]),
            token_type=PASSWORD_RESET_TOKEN_TYPE,
            expires_at_iso=(utc_now() + timedelta(minutes=resolved.password_reset_token_expiry_minutes)).isoformat(),
            target_email=normalized_email,
        )

    reset_link = _build_public_url(resolved, f"/reset-password/{reset_token}")
    try:
        send_password_reset(normalized_email, reset_link, settings=resolved)
    except (EmailModeError, EmailConfigError, EmailDeliveryError) as exc:
        return False
    return True


def reset_password(
    token: str,
    new_password: str,
    repeat_password: str,
    settings: Settings | None = None,
) -> UserPublic:
    resolved = _settings(settings)
    normalized_password = _passwords_match(new_password, repeat_password)
    token_hash = hash_token(token or "")
    now_iso = utc_now_iso()
    with _connection(resolved) as connection:
        row = connection.execute(
            """
            SELECT at.id AS token_id, at.user_id, u.id, u.email, u.login, u.role,
                   u.is_active, u.email_verified_at, u.access_status
            FROM auth_tokens AS at
            JOIN users AS u ON u.id = at.user_id
            WHERE at.token_hash = ?
              AND at.token_type = ?
              AND at.used_at IS NULL
              AND at.revoked_at IS NULL
              AND at.expires_at > ?
            """,
            (token_hash, PASSWORD_RESET_TOKEN_TYPE, now_iso),
        ).fetchone()
        if not row:
            raise NotFoundError("password reset token not found or expired")
        new_password_hash = hash_password(normalized_password)
        connection.execute(
            "UPDATE users SET password_hash = ?, updated_at = ? WHERE id = ?",
            (new_password_hash, now_iso, int(row["user_id"])),
        )
        connection.execute(
            "UPDATE auth_tokens SET used_at = ? WHERE id = ?",
            (now_iso, int(row["token_id"])),
        )
        connection.execute(
            "UPDATE sessions SET revoked_at = ? WHERE user_id = ? AND revoked_at IS NULL",
            (now_iso, int(row["user_id"])),
        )
        user_row = connection.execute("SELECT * FROM users WHERE id = ?", (int(row["user_id"]),)).fetchone()
        if user_row is None:
            raise AuthError("reset user lookup failed")
        return _public_user_from_row(user_row)


def change_password(
    *,
    user_id: int,
    current_password: str,
    new_password: str,
    repeat_password: str,
    settings: Settings | None = None,
) -> UserPublic:
    resolved = _settings(settings)
    with _connection(resolved) as connection:
        row = connection.execute("SELECT * FROM users WHERE id = ?", (int(user_id),)).fetchone()
        if row is None:
            raise NotFoundError("user not found")
        if not bool(row["is_active"]):
            raise UnauthorizedError("user is not active")
        try:
            current_password_ok = verify_password(current_password, str(row["password_hash"]))
        except ValueError as exc:
            raise ValidationError(str(exc)) from exc
        if not current_password_ok:
            raise UnauthorizedError("invalid credentials")
        normalized_password = _passwords_match(new_password, repeat_password)
        new_password_hash = hash_password(normalized_password)
        now_iso = utc_now_iso()
        connection.execute(
            "UPDATE users SET password_hash = ?, updated_at = ? WHERE id = ?",
            (new_password_hash, now_iso, int(row["id"])),
        )
        updated = connection.execute("SELECT * FROM users WHERE id = ?", (int(row["id"]),)).fetchone()
        if updated is None:
            raise AuthError("password change user lookup failed")
        return _public_user_from_row(updated)
```

```diff
diff --git a/source/app/auth/service.py b/source/app/auth/service.py
index 6b78271..3110b5e 100644
--- a/source/app/auth/service.py
+++ b/source/app/auth/service.py
@@ -389,6 +389,39 @@ def update_user_role(
         return _public_user_from_row(updated)
 
 
+def set_user_materials_access(
+    *,
+    user_id: int,
+    granted: bool,
+    settings: Settings | None = None,
+) -> UserPublic:
+    resolved = _settings(settings)
+    target_access_status = "activated" if granted else "not_activated"
+    target_granted_at = utc_now_iso() if granted else None
+    with _connection(resolved) as connection:
+        row = connection.execute("SELECT * FROM users WHERE id = ?", (int(user_id),)).fetchone()
+        if row is None:
+            raise NotFoundError("user not found")
+        current_granted = row["materials_access_granted_at"] is not None
+        current_access_status = str(row["access_status"])
+        if current_granted == granted and current_access_status == target_access_status:
+            return _public_user_from_row(row)
+
+        now_iso = utc_now_iso()
+        connection.execute(
+            """
+            UPDATE users
+            SET materials_access_granted_at = ?, access_status = ?, updated_at = ?
+            WHERE id = ?
+            """,
+            (target_granted_at, target_access_status, now_iso, int(user_id)),
+        )
+        updated = connection.execute("SELECT * FROM users WHERE id = ?", (int(user_id),)).fetchone()
+        if updated is None:
+            raise AuthError("materials access update failed")
+        return _public_user_from_row(updated)
+
+
 def register_user(
     email: str,
     login: str,
```


### source/tests/test_admin_paid_access_grant.py

```py
from __future__ import annotations

import re
import sqlite3

from app.auth.service import authenticate_user, create_session, register_user, verify_email
from app.shared.db import get_database_path


def _connect(settings):
    conn = sqlite3.connect(str(get_database_path(settings)))
    conn.row_factory = sqlite3.Row
    return conn


def _extract_verify_token(settings, email: str) -> str:
    with _connect(settings) as conn:
        row = conn.execute(
            "SELECT body_text FROM email_outbox WHERE recipient_email = ? AND template_key = ? ORDER BY id DESC LIMIT 1",
            (email, "email_verification"),
        ).fetchone()
    assert row is not None
    match = re.search(r"/verify-email/([A-Za-z0-9_-]+)", row["body_text"])
    assert match
    return match.group(1)


def _create_verified_user(test_settings, *, email: str, login: str, role: str = "user") -> None:
    register_user(
        email=email,
        login=login,
        password="Secret123",
        repeat_password="Secret123",
        settings=test_settings,
    )
    verify_email(_extract_verify_token(test_settings, email), settings=test_settings)
    if role != "user":
        with _connect(test_settings) as conn:
            conn.execute("UPDATE users SET role = ? WHERE email = ?", (role, email))
            conn.commit()


def _login_as(client, test_settings, email: str):
    user = authenticate_user(email, "Secret123", settings=test_settings)
    session_token = create_session(user.id, settings=test_settings)
    client.cookies.set(test_settings.session_cookie_name, session_token)
    return user


def _user_row(test_settings, email: str):
    with _connect(test_settings) as conn:
        return conn.execute(
            """
            SELECT email, role, access_status, materials_access_granted_at
            FROM users
            WHERE email = ?
            """,
            (email,),
        ).fetchone()


def test_admin_users_page_shows_paid_access_state_and_controls(client, test_settings):
    _create_verified_user(test_settings, email="admin-access-admin@example.com", login="adminaccessadmin", role="admin")
    _create_verified_user(test_settings, email="admin-access-open@example.com", login="adminaccessopen")
    with _connect(test_settings) as conn:
        conn.execute(
            "UPDATE users SET materials_access_granted_at = CURRENT_TIMESTAMP, access_status = 'activated' WHERE email = ?",
            ("admin-access-open@example.com",),
        )
        conn.commit()

    _login_as(client, test_settings, "admin-access-admin@example.com")
    response = client.get("/admin/users")
    assert response.status_code == 200
    body = response.text
    assert "Доступ к материалам" in body
    assert "Доступ выдан" in body
    assert "Доступ не выдан" in body
    assert "Выдать доступ" in body
    assert "Отозвать доступ" in body
    assert "/materials-access/grant" in body
    assert "/materials-access/revoke" in body
    assert "materials_access_granted_at" not in body.lower()
    assert "password_hash" not in body.lower()
    assert "token_hash" not in body.lower()


def test_admin_can_grant_and_revoke_paid_access(client, test_settings):
    _create_verified_user(test_settings, email="admin-grant-admin@example.com", login="admingrantadmin", role="admin")
    _create_verified_user(test_settings, email="admin-grant-user@example.com", login="admingrantuser")

    _login_as(client, test_settings, "admin-grant-admin@example.com")
    target_user = authenticate_user("admin-grant-user@example.com", "Secret123", settings=test_settings)

    grant_response = client.post(f"/admin/users/{target_user.id}/materials-access/grant", follow_redirects=False)
    assert grant_response.status_code == 303

    granted = _user_row(test_settings, "admin-grant-user@example.com")
    assert granted is not None
    assert granted["materials_access_granted_at"] is not None
    assert granted["access_status"] == "activated"

    client.cookies.clear()
    _login_as(client, test_settings, "admin-grant-user@example.com")
    cabinet_response = client.get("/cabinet")
    assert cabinet_response.status_code == 200
    assert "Аккаунты" in cabinet_response.text
    assert "/static/cabinet-local-accounts.js" in cabinet_response.text

    materials_response = client.get("/materials")
    assert materials_response.status_code == 200
    assert "Работа с ИИ" in materials_response.text
    assert "Доступ к материалам и урокам откроется после оплаты тарифа." not in materials_response.text

    client.cookies.clear()
    _login_as(client, test_settings, "admin-grant-admin@example.com")
    revoke_response = client.post(f"/admin/users/{target_user.id}/materials-access/revoke", follow_redirects=False)
    assert revoke_response.status_code == 303

    revoked = _user_row(test_settings, "admin-grant-user@example.com")
    assert revoked is not None
    assert revoked["materials_access_granted_at"] is None
    assert revoked["access_status"] == "not_activated"

    client.cookies.clear()
    _login_as(client, test_settings, "admin-grant-user@example.com")
    locked_cabinet = client.get("/cabinet")
    assert locked_cabinet.status_code == 200
    assert "Личный кабинет будет доступен после оплаты" in locked_cabinet.text
    assert "После оплаты тарифа откроются личный кабинет, обучение и материалы." in locked_cabinet.text
    assert "/static/cabinet-local-accounts.js" not in locked_cabinet.text

    locked_materials = client.get("/materials")
    assert locked_materials.status_code == 200
    assert "Раздел «Работа с ИИ» закрыт" in locked_materials.text
    assert "Доступ к материалам и урокам откроется после оплаты тарифа." in locked_materials.text


def test_non_admins_cannot_grant_or_revoke_paid_access(client, test_settings):
    _create_verified_user(test_settings, email="admin-grant-target@example.com", login="admingranttarget")
    _create_verified_user(test_settings, email="admin-grant-admin2@example.com", login="admingrantadmin2", role="admin")

    target_user = authenticate_user("admin-grant-target@example.com", "Secret123", settings=test_settings)
    anonymous_response = client.post(f"/admin/users/{target_user.id}/materials-access/grant", follow_redirects=False)
    assert anonymous_response.status_code == 303
    assert anonymous_response.headers["location"] == "/login"

    _login_as(client, test_settings, "admin-grant-target@example.com")
    target_again = authenticate_user("admin-grant-admin2@example.com", "Secret123", settings=test_settings)
    user_grant_response = client.post(f"/admin/users/{target_again.id}/materials-access/grant")
    assert user_grant_response.status_code == 403
    user_revoke_response = client.post(f"/admin/users/{target_again.id}/materials-access/revoke")
    assert user_revoke_response.status_code == 403

    client.cookies.clear()
    _create_verified_user(test_settings, email="admin-grant-moderator@example.com", login="admingrantmoderator", role="moderator")
    _login_as(client, test_settings, "admin-grant-moderator@example.com")
    moderator_grant_response = client.post(f"/admin/users/{target_again.id}/materials-access/grant")
    assert moderator_grant_response.status_code == 403
    moderator_revoke_response = client.post(f"/admin/users/{target_again.id}/materials-access/revoke")
    assert moderator_revoke_response.status_code == 403


def test_access_status_alone_does_not_unlock_paid_access(client, test_settings):
    _create_verified_user(test_settings, email="admin-grant-status-only@example.com", login="admingrantstatus")
    with _connect(test_settings) as conn:
        conn.execute(
            "UPDATE users SET access_status = 'activated' WHERE email = ?",
            ("admin-grant-status-only@example.com",),
        )
        conn.commit()

    user = authenticate_user("admin-grant-status-only@example.com", "Secret123", settings=test_settings)
    assert user.access_status == "activated"
    assert user.materials_access_granted_at is None

    _login_as(client, test_settings, "admin-grant-status-only@example.com")
    cabinet_response = client.get("/cabinet")
    materials_response = client.get("/materials")
    assert cabinet_response.status_code == 200
    assert materials_response.status_code == 200
    assert "Личный кабинет будет доступен после оплаты" in cabinet_response.text
    assert "После оплаты тарифа откроются личный кабинет, обучение и материалы." in cabinet_response.text
    assert "Раздел «Работа с ИИ» закрыт" in materials_response.text
```


### source/tests/test_admin_readonly_lists.py

```py
from __future__ import annotations

import re
import sqlite3

import pytest

from app.auth.service import authenticate_user, create_session, register_user, verify_email
from app.shared.db import get_database_path
from app.tariffs.service import STARTER_TARIFF_CODE, seed_initial_catalog


def _connect(settings):
    conn = sqlite3.connect(str(get_database_path(settings)))
    conn.row_factory = sqlite3.Row
    return conn


def _extract_verify_token(settings, email: str) -> str:
    with _connect(settings) as conn:
        row = conn.execute(
            "SELECT body_text FROM email_outbox WHERE recipient_email = ? AND template_key = ? ORDER BY id DESC LIMIT 1",
            (email, "email_verification"),
        ).fetchone()
    assert row is not None
    match = re.search(r"/verify-email/([A-Za-z0-9_-]+)", row["body_text"])
    assert match
    return match.group(1)


def _make_user(client, test_settings, email: str, login: str, role: str = "user") -> None:
    register_user(
        email=email,
        login=login,
        password="Secret123",
        repeat_password="Secret123",
        settings=test_settings,
    )
    token = _extract_verify_token(test_settings, email)
    verify_email(token, settings=test_settings)
    with _connect(test_settings) as conn:
        conn.execute("UPDATE users SET role = ? WHERE email = ?", (role, email))
        conn.commit()
    user = authenticate_user(email, "Secret123", settings=test_settings)
    session_token = create_session(user.id, settings=test_settings)
    client.cookies.set(test_settings.session_cookie_name, session_token)


@pytest.mark.parametrize(
    ("path",),
    [
        ("/admin/users",),
        ("/admin/tariffs",),
        ("/admin/paid-options",),
    ],
)
def test_anonymous_admin_list_pages_redirect_to_login(client, path):
    response = client.get(path, follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/login"


@pytest.mark.parametrize(
    ("path",),
    [
        ("/admin/users",),
        ("/admin/tariffs",),
        ("/admin/paid-options",),
    ],
)
def test_normal_user_gets_forbidden_on_admin_list_pages(client, test_settings, path):
    _make_user(client, test_settings, "user@example.com", "regularuser", role="user")
    response = client.get(path)
    assert response.status_code == 403
    assert "Доступ запрещён" in response.text
    assert "прав администратора" in response.text
    assert "Forbidden" not in response.text


@pytest.mark.parametrize(
    ("path",),
    [
        ("/admin/users",),
        ("/admin/tariffs",),
        ("/admin/paid-options",),
    ],
)
def test_moderator_gets_forbidden_on_admin_list_pages(client, test_settings, path):
    _make_user(client, test_settings, "moderator@example.com", "moderatoruser", role="moderator")
    response = client.get(path)
    assert response.status_code == 403
    assert "Доступ запрещён" in response.text
    assert "прав администратора" in response.text


@pytest.mark.parametrize(
    ("path",),
    [
        ("/admin/users",),
        ("/admin/tariffs",),
        ("/admin/paid-options",),
    ],
)
def test_admin_user_can_open_admin_list_pages(client, test_settings, path):
    _make_user(client, test_settings, "admin@example.com", "adminuser", role="admin")
    if path != "/admin/users":
        seed_initial_catalog(settings=test_settings)
    response = client.get(path)
    assert response.status_code == 200


def test_admin_users_shows_safe_fields_and_hides_sensitive_data(client, test_settings):
    _make_user(client, test_settings, "admin@example.com", "adminuser", role="admin")
    register_user(
        email="viewer@example.com",
        login="vieweruser",
        password="Secret123",
        repeat_password="Secret123",
        settings=test_settings,
    )
    with _connect(test_settings) as conn:
        conn.execute(
            """
            UPDATE users
            SET role = ?, is_active = 0, email_verified_at = NULL,
                materials_access_granted_at = CURRENT_TIMESTAMP,
                access_status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE email = ?
            """,
            ("user", "activated", "viewer@example.com"),
        )
        conn.commit()

    response = client.get("/admin/users")
    assert response.status_code == 200
    body = response.text
    assert "/static/styles.css" in body
    assert "Пользователи" in body
    assert "admin@example.com" in body
    assert "viewer@example.com" in body
    assert "adminuser" in body
    assert "vieweruser" in body
    assert "Идентификатор" in body
    assert "Электронная почта" in body
    assert "Логин" in body
    assert "Роль" in body
    assert "Изменить роль" in body
    assert "Активен" in body
    assert "Подтверждён email" in body
    assert "Статус доступа" in body
    assert "Доступ к материалам" in body
    assert "администратор" in body
    assert "пользователь" in body
    assert "модератор" in body
    assert "Сохранить роль" in body
    assert "/admin/users/" in body
    assert "/role" in body
    assert "подтверждён" in body
    assert "не подтверждён" in body
    assert "да" in body
    assert "нет" in body
    assert "verified" not in body.lower()
    assert "unverified" not in body.lower()
    assert "password_hash" not in body.lower()
    assert "token_hash" not in body.lower()
    assert "raw token" not in body.lower()
    assert "cookie" not in body.lower()
    assert "email_outbox" not in body.lower()


def test_admin_tariffs_shows_starter_tariff_and_admin_controls(client, test_settings):
    _make_user(client, test_settings, "admin@example.com", "adminuser", role="admin")
    seed_initial_catalog(settings=test_settings)

    response = client.get("/admin/tariffs")
    assert response.status_code == 200
    body = response.text
    assert "/static/styles.css" in body
    assert "Тарифы" in body
    assert "Код" in body
    assert "Название" in body
    assert "Описание" in body
    assert "Цена, ₽" in body
    assert "Валюта" in body
    assert "Статус" in body
    assert "Порядок сортировки" in body
    assert "Включённые опции" in body
    assert "Действия" in body
    assert "Code" not in body
    assert "Title" not in body
    assert "Price" not in body
    assert STARTER_TARIFF_CODE in body
    assert "Стартовый доступ" in body
    assert "AI / GPT-инструмент" in body
    assert "активен" in body
    assert "/admin/tariffs/new" in body
    assert f"/admin/tariffs/{STARTER_TARIFF_CODE}/options" in body
    assert f"/admin/tariffs/{STARTER_TARIFF_CODE}/edit" in body
    assert f"/admin/tariffs/{STARTER_TARIFF_CODE}/archive" in body
    assert "/admin/paid-options/new" not in body
    assert "/admin/payments" not in body


def test_admin_paid_options_shows_catalog_and_admin_controls(client, test_settings):
    _make_user(client, test_settings, "admin@example.com", "adminuser", role="admin")
    seed_initial_catalog(settings=test_settings)

    response = client.get("/admin/paid-options")
    assert response.status_code == 200
    body = response.text
    assert "/static/styles.css" in body
    assert "Платные опции" in body
    assert "Код" in body
    assert "Название" in body
    assert "Описание" in body
    assert "Цена, ₽" in body
    assert "Валюта" in body
    assert "Срок по умолчанию, дней" in body
    assert "Статус" in body
    assert "Можно продлевать" in body
    assert "Порядок сортировки" in body
    assert "Действия" in body
    assert "Code" not in body
    assert "Title" not in body
    assert "Default duration days" not in body
    assert "AI / GPT-инструмент" in body
    assert "Сервер" in body
    assert "VPN" in body
    assert "отдельная цена не задана" in body
    assert "активен" in body
    assert "/admin/paid-options/new" in body
    assert "/admin/paid-options/ai_gpt_tool/edit" in body
    assert "/admin/paid-options/ai_gpt_tool/archive" in body
    assert "/admin/tariffs/" not in body
    assert "/admin/payments" not in body


def test_admin_dashboard_links_to_read_only_list_pages(client, test_settings):
    _make_user(client, test_settings, "admin@example.com", "adminuser", role="admin")
    response = client.get("/admin")
    assert response.status_code == 200
    body = response.text
    assert "/static/styles.css" in body
    assert "Админ-панель" in body
    assert "Пользователи" in body
    assert "Тарифы" in body
    assert "Платные опции" in body
    assert "Работа с ИИ" in body
    assert "Личный кабинет" in body
    assert "Выйти" in body
    assert "На главную" in body
    assert '/admin/users' in body
    assert '/admin/tariffs' in body
    assert '/admin/paid-options' in body
    assert '/materials' in body
    assert 'Платежи' in body
```

```diff
(no diff)
```


## 8. MATERIALS_CURRENT_CODE

### source/app/materials/routes.py

```py
"""Materials page routes."""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from jinja2 import ChoiceLoader, FileSystemLoader

from app.auth.service import get_current_user_from_cookies
from app.core.config import get_settings
from app.materials.course_loader import (
    get_lesson,
    list_lessons,
    load_course,
    render_markdown,
    LessonNotFoundError,
)
from app.materials.service import user_has_materials_access

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))
templates.env.loader = ChoiceLoader(
    [
        templates.env.loader,
        FileSystemLoader(str(Path(__file__).resolve().parents[1] / "user_cabinet" / "templates")),
        FileSystemLoader(str(Path(__file__).resolve().parents[1] / "shared" / "templates")),
    ]
)
LESSON_TEST_URL = "/materials/drafts/dair-smoke-20260529/"
LESSON_TEST_STYLES_URL = "/materials/drafts/dair-smoke-20260529/styles.css"
LESSON_TEST_SCRIPT_URL = "/materials/drafts/dair-smoke-20260529/script.js"
LESSON_TEST_ROOT = Path(__file__).resolve().parent / "course_content" / "drafts" / "dair_smoke_20260529"


def _require_learning_access(request: Request):
    settings = get_settings()
    user = get_current_user_from_cookies(request.cookies, settings=settings)
    if user is None:
        return None, RedirectResponse(url="/login", status_code=303)
    if not user_has_materials_access(user):
        raise HTTPException(status_code=403, detail="learning access required")
    return user, None


def _read_lesson_test_asset(filename: str) -> str:
    path = LESSON_TEST_ROOT / filename
    if not path.is_file():
        raise HTTPException(status_code=404, detail=f"Missing lesson test file: {filename}")
    return path.read_text(encoding="utf-8")


def _template(request: Request, template_name: str, **context) -> HTMLResponse:
    payload = {
        "request": request,
        "title": context.pop("title", "Работа с ИИ"),
        "current_user": get_current_user_from_cookies(request.cookies, settings=get_settings()),
    }
    payload.update(context)
    return templates.TemplateResponse(request, template_name, payload)


def _locked_response(
    request: Request,
    *,
    title: str,
    locked_title: str,
    locked_message: str,
    locked_action_label: str = "На главную",
    locked_action_url: str = "/",
    locked_secondary_label: str | None = None,
    locked_secondary_url: str | None = None,
    current_user=None,
):
    return _template(
        request,
        "access_locked.html",
        title=title,
        locked_title=locked_title,
        locked_message=locked_message,
        locked_action_label=locked_action_label,
        locked_action_url=locked_action_url,
        locked_secondary_label=locked_secondary_label,
        locked_secondary_url=locked_secondary_url,
        current_user=current_user,
    )


@router.get("/materials", response_class=HTMLResponse)
def materials_page(request: Request):
    settings = get_settings()
    user = get_current_user_from_cookies(request.cookies, settings=settings)
    if user is None:
        return RedirectResponse(url="/login", status_code=303)
    if not user_has_materials_access(user):
        return _locked_response(
            request,
            title="Работа с ИИ",
            locked_title="Раздел «Работа с ИИ» закрыт",
            locked_message="Доступ к материалам и урокам откроется после оплаты тарифа.",
            locked_action_label="На главную",
            locked_action_url="/",
            locked_secondary_label="В личный кабинет",
            locked_secondary_url="/cabinet",
            current_user=user,
        )
    course = load_course()
    return _template(
        request,
        "materials.html",
        title="Работа с ИИ",
        course_title=course["title"],
        course_audience=course["audience"],
        lessons=list_lessons(),
        user_email=user.email,
        user_login=user.login,
        lesson_test_url=LESSON_TEST_URL,
    )


@router.head("/materials")
def materials_head(request: Request):
    settings = get_settings()
    user = get_current_user_from_cookies(request.cookies, settings=settings)
    if user is None:
        return RedirectResponse(url="/login", status_code=303)
    return materials_page(request)


@router.get("/materials/lessons/{slug}", response_class=HTMLResponse)
def lesson_page(request: Request, slug: str):
    settings = get_settings()
    user = get_current_user_from_cookies(request.cookies, settings=settings)
    if user is None:
        return RedirectResponse(url="/login", status_code=303)
    try:
        lesson = get_lesson(slug)
    except LessonNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if not user_has_materials_access(user):
        return _locked_response(
            request,
            title=lesson["title"],
            locked_title=lesson["title"],
            locked_message="Урок и его материалы откроются после оплаты тарифа.",
            locked_action_label="К разделу материалов",
            locked_action_url="/materials",
            locked_secondary_label="На главную",
            locked_secondary_url="/",
            current_user=user,
        )
    return _template(
        request,
        "lesson.html",
        title=lesson["title"],
        course_title=load_course()["title"],
        lesson=lesson,
        lesson_html=render_markdown(lesson["content"]),
    )


@router.head("/materials/lessons/{slug}")
def lesson_head(request: Request, slug: str):
    return lesson_page(request, slug)


@router.get(LESSON_TEST_URL, response_class=HTMLResponse)
def lesson_test_page(request: Request):
    settings = get_settings()
    user = get_current_user_from_cookies(request.cookies, settings=settings)
    if user is None:
        return RedirectResponse(url="/login", status_code=303)
    if not user_has_materials_access(user):
        return _locked_response(
            request,
            title="Работа с ИИ",
            locked_title="Раздел «Работа с ИИ» закрыт",
            locked_message="Доступ к материалам и урокам откроется после оплаты тарифа.",
            locked_action_label="На главную",
            locked_action_url="/",
            locked_secondary_label="В личный кабинет",
            locked_secondary_url="/cabinet",
            current_user=user,
        )
    return HTMLResponse(_read_lesson_test_asset("index.html"))


@router.get(LESSON_TEST_STYLES_URL)
def lesson_test_styles(request: Request):
    _, redirect_response = _require_learning_access(request)
    if redirect_response is not None:
        return redirect_response
    return Response(
        _read_lesson_test_asset("styles.css"),
        media_type="text/css; charset=utf-8",
    )


@router.get(LESSON_TEST_SCRIPT_URL)
def lesson_test_script(request: Request):
    _, redirect_response = _require_learning_access(request)
    if redirect_response is not None:
        return redirect_response
    return Response(
        _read_lesson_test_asset("script.js"),
        media_type="application/javascript; charset=utf-8",
    )
```

```diff
diff --git a/source/app/materials/routes.py b/source/app/materials/routes.py
index dc08d7e..5848736 100644
--- a/source/app/materials/routes.py
+++ b/source/app/materials/routes.py
@@ -25,6 +25,7 @@ templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "tem
 templates.env.loader = ChoiceLoader(
     [
         templates.env.loader,
+        FileSystemLoader(str(Path(__file__).resolve().parents[1] / "user_cabinet" / "templates")),
         FileSystemLoader(str(Path(__file__).resolve().parents[1] / "shared" / "templates")),
     ]
 )
@@ -61,12 +62,50 @@ def _template(request: Request, template_name: str, **context) -> HTMLResponse:
     return templates.TemplateResponse(request, template_name, payload)
 
 
+def _locked_response(
+    request: Request,
+    *,
+    title: str,
+    locked_title: str,
+    locked_message: str,
+    locked_action_label: str = "На главную",
+    locked_action_url: str = "/",
+    locked_secondary_label: str | None = None,
+    locked_secondary_url: str | None = None,
+    current_user=None,
+):
+    return _template(
+        request,
+        "access_locked.html",
+        title=title,
+        locked_title=locked_title,
+        locked_message=locked_message,
+        locked_action_label=locked_action_label,
+        locked_action_url=locked_action_url,
+        locked_secondary_label=locked_secondary_label,
+        locked_secondary_url=locked_secondary_url,
+        current_user=current_user,
+    )
+
+
 @router.get("/materials", response_class=HTMLResponse)
 def materials_page(request: Request):
     settings = get_settings()
     user = get_current_user_from_cookies(request.cookies, settings=settings)
     if user is None:
         return RedirectResponse(url="/login", status_code=303)
+    if not user_has_materials_access(user):
+        return _locked_response(
+            request,
+            title="Работа с ИИ",
+            locked_title="Раздел «Работа с ИИ» закрыт",
+            locked_message="Доступ к материалам и урокам откроется после оплаты тарифа.",
+            locked_action_label="На главную",
+            locked_action_url="/",
+            locked_secondary_label="В личный кабинет",
+            locked_secondary_url="/cabinet",
+            current_user=user,
+        )
     course = load_course()
     return _template(
         request,
@@ -100,6 +139,18 @@ def lesson_page(request: Request, slug: str):
         lesson = get_lesson(slug)
     except LessonNotFoundError as exc:
         raise HTTPException(status_code=404, detail=str(exc)) from exc
+    if not user_has_materials_access(user):
+        return _locked_response(
+            request,
+            title=lesson["title"],
+            locked_title=lesson["title"],
+            locked_message="Урок и его материалы откроются после оплаты тарифа.",
+            locked_action_label="К разделу материалов",
+            locked_action_url="/materials",
+            locked_secondary_label="На главную",
+            locked_secondary_url="/",
+            current_user=user,
+        )
     return _template(
         request,
         "lesson.html",
@@ -117,9 +168,22 @@ def lesson_head(request: Request, slug: str):
 
 @router.get(LESSON_TEST_URL, response_class=HTMLResponse)
 def lesson_test_page(request: Request):
-    _, redirect_response = _require_learning_access(request)
-    if redirect_response is not None:
-        return redirect_response
+    settings = get_settings()
+    user = get_current_user_from_cookies(request.cookies, settings=settings)
+    if user is None:
+        return RedirectResponse(url="/login", status_code=303)
+    if not user_has_materials_access(user):
+        return _locked_response(
+            request,
+            title="Работа с ИИ",
+            locked_title="Раздел «Работа с ИИ» закрыт",
+            locked_message="Доступ к материалам и урокам откроется после оплаты тарифа.",
+            locked_action_label="На главную",
+            locked_action_url="/",
+            locked_secondary_label="В личный кабинет",
+            locked_secondary_url="/cabinet",
+            current_user=user,
+        )
     return HTMLResponse(_read_lesson_test_asset("index.html"))
 
 
```


### source/app/materials/templates/materials.html

```html
{% extends "base.html" %}

{% block content %}
  <section class="stack">
    <div class="card stack">
      <div class="stack">
        <p class="muted">Раздел «Работа с ИИ»</p>
        <h1 class="section-title">{{ course_title }}</h1>
        <p>Курс для новичков без опыта программирования.</p>
        <p class="form-help">Сначала мы разбираем схему работы, потом переходим к практическим урокам.</p>
      </div>

      <div class="card-grid tight">
        <section class="card stack">
          <h2 class="section-title">Для кого курс</h2>
          <p class="muted">{{ course_audience }}</p>
        </section>
        <section class="card stack">
          <h2 class="section-title">Как устроен старт</h2>
          <p class="muted">Уроки идут по одному, с готовыми ответами и проверкой результата.</p>
        </section>
      </div>

      {% if lesson_test_url %}
        <section class="card stack">
          <p class="muted">Карта курса</p>
          <h2 class="section-title">Как разрабатывать с помощью ChatGPT и Codex</h2>
          <p class="form-help">Открой карту из 9 уроков, проверь навигацию, карточки, проверку знаний и прогресс.</p>
          <div class="actions">
            <a class="button button-secondary" href="{{ lesson_test_url }}">Открыть карту курса</a>
          </div>
        </section>
      {% endif %}
    </div>

    <section class="stack">
      <div class="card stack">
        <h2 class="section-title">Уроки курса</h2>
        <p class="form-help">Сейчас доступен первый реальный урок. Дальше список будет расти.</p>
      </div>

      <div class="card-grid">
        {% for lesson in lessons %}
          <article class="card stack">
            <p class="muted">Урок {{ lesson.order }}</p>
            <h3 class="section-title">{{ lesson.title }}</h3>
            <p class="form-help">Статус: {{ lesson.status }}</p>
            <div class="actions">
              <a class="button button-primary" href="/materials/lessons/{{ lesson.slug }}">Открыть урок</a>
            </div>
          </article>
        {% endfor %}
      </div>
    </section>

    <div class="actions">
      <a class="button button-primary" href="/cabinet">Вернуться в личный кабинет</a>
      <a class="button button-secondary" href="/">На главную</a>
    </div>
  </section>
{% endblock %}
```

```diff
(no diff)
```


### source/app/materials/templates/lesson.html

```html
{% extends "base.html" %}

{% block content %}
  <section class="stack">
    <div class="card stack">
      <div class="stack">
        <p class="muted">Раздел «Работа с ИИ»</p>
        <a href="/materials">← К списку уроков</a>
        <h1 class="section-title">{{ lesson.title }}</h1>
        <p class="form-help">Урок {{ lesson.order }} из курса «{{ course_title }}»</p>
      </div>
    </div>

    <article class="card stack lesson-content">
      {{ lesson_html | safe }}
    </article>

    <div class="actions">
      <a class="button button-primary" href="/materials">Вернуться к материалам</a>
      <a class="button button-secondary" href="/cabinet">В кабинет</a>
    </div>
  </section>
{% endblock %}
```

```diff
(no diff)
```


### source/app/materials/templates/learning_locked.html

```html
{% extends "base.html" %}

{% block content %}
  <section class="stack">
    <header class="card course-head">
      <div class="hero-bg-visual hero-bg-desktop" aria-hidden="true">
        <img src="/static/images/human_ai_hero_background_v2.png" alt="" decoding="async" draggable="false">
      </div>
      <div class="hero-bg-visual hero-bg-mobile" aria-hidden="true">
        <img src="/static/images/mobile_vitruvian_NO_SQUARES_transparent.webp" alt="" decoding="async" draggable="false">
      </div>
      <div class="hero-wrap">
        <div class="hero-copy">
          <span class="eyebrow">Обучение</span>
          <h1>Работа с ИИ</h1>
          <p class="course-headline">Как разрабатывать с помощью ChatGPT и Codex</p>
          <p class="course-note">Курс показывает, как вести проектную работу с ИИ без ручного написания кода: от простой идеи до проверенного результата.</p>
          {% if current_user %}
            <div class="course-access-badge" role="status" aria-live="polite">
              <p>Вы вошли как {{ current_user.login }}.</p>
              <p>Полный доступ откроется после оплаты тарифа.</p>
            </div>
          {% endif %}
        </div>
      </div>
    </header>

    <section class="card stack course-intro">
      <div class="section-heading">
        <h2>Вступление к курсу</h2>
      </div>
      <div class="course-intro-body">
        <section class="course-intro-part">
          <h3>Что изучаем</h3>
          <p>В этом курсе вы изучаете, как вести проектную работу с помощью ChatGPT и Codex без ручного написания кода.</p>
          <p>Курс показывает, как простая идея пользователя превращается в понятную задачу, затем в план работы, затем в выполнение на сервере через Codex, а после этого - в проверенный результат.</p>
        </section>
        <section class="course-intro-part">
          <h3>Зачем это нужно</h3>
          <p>Без понятной схемы работа с ИИ быстро превращается в хаос: пользователь формулирует задачу без конкретики, ChatGPT может неправильно понять цель, а Codex может выполнить не тот шаг или изменить лишнее.</p>
          <p>Курс нужен, чтобы научиться управлять процессом: описывать желание обычными словами, вместе с ChatGPT уточнять задачу, получать документацию и план работы, проверять отчёт и принимать результат по фактам.</p>
        </section>
        <section class="course-intro-part">
          <h3>Где это применяется</h3>
          <p>Эта схема применяется в реальных проектных задачах: при создании сайта, страницы, сервиса, бота, автоматизации, личного кабинета, учебного проекта или отдельной функции.</p>
          <p>Пользователю не нужно заранее знать программирование, дизайн, вёрстку, архитектуру, документацию или техническое задание. Достаточно описать, что он хочет получить. Дальше ChatGPT помогает продумать задачу, подготовить документы, спланировать внешний вид, разбить работу на шаги и дать Codex точное задание.</p>
        </section>
      </div>
    </section>

    {% set pricing_section_id = "pricing" %}
    {% set pricing_section_class = "course-pricing-block" %}
    {% set pricing_shell_class = "pricing-shell" %}
    {% set pricing_eyebrow = "Цена" %}
    {% set pricing_fallback_description = "Это активный тариф, отмеченный для показа на главной странице. Он подтягивается из каталога тарифов." %}
    {% set primary_cta_href = "/" %}
    {% set primary_cta_label = "На главную" %}
    {% set secondary_cta_href = "/cabinet" %}
    {% set secondary_cta_label = "В личный кабинет" %}
    {% include "tariff_pricing_section.html" %}
  </section>
{% endblock %}
```


### source/tests/test_materials_flow.py

```py
from __future__ import annotations

import hashlib
import sqlite3
from urllib.parse import unquote

from app.auth.service import authenticate_user, create_session, register_user, verify_email
from app.materials.routes import LESSON_TEST_SCRIPT_URL, LESSON_TEST_STYLES_URL, LESSON_TEST_URL
from app.materials.service import user_has_materials_access
from app.shared.db import get_database_path, initialize_database
from app.user_cabinet.routes import (
    LEARNING_PROJECT_DOWNLOAD_URL,
    LEARNING_PROJECT_FILE_PATH,
    LEARNING_PROJECT_FILE_NAME,
)


def _connect(settings):
    conn = sqlite3.connect(str(get_database_path(settings)))
    conn.row_factory = sqlite3.Row
    return conn


def _extract_token_from_db(settings, email: str) -> str:
    import re

    with _connect(settings) as conn:
        row = conn.execute(
            "SELECT body_text FROM email_outbox WHERE recipient_email = ? AND template_key = ? ORDER BY id DESC LIMIT 1",
            (email, "email_verification"),
        ).fetchone()
    assert row is not None
    match = re.search(r"/verify-email/([A-Za-z0-9_-]+)", row["body_text"])
    assert match
    return match.group(1)


def _prepare_verified_user(
    client,
    test_settings,
    email: str,
    login: str,
    grant_access: bool = False,
    role: str = "user",
):
    initialize_database(get_database_path(test_settings))
    register_user(
        email=email,
        login=login,
        password="Secret123",
        repeat_password="Secret123",
        settings=test_settings,
    )
    token = _extract_token_from_db(test_settings, email)
    verify_email(token, settings=test_settings)
    if grant_access or role != "user":
        with _connect(test_settings) as conn:
            if role != "user":
                conn.execute("UPDATE users SET role = ? WHERE email = ?", (role, email))
            if grant_access:
                conn.execute(
                    "UPDATE users SET materials_access_granted_at = CURRENT_TIMESTAMP WHERE email = ?",
                    (email,),
                )
            conn.commit()


def _login_verified_user(client, test_settings, email: str):
    user = authenticate_user(email, "Secret123", settings=test_settings)
    session_token = create_session(user.id, settings=test_settings)
    client.cookies.set(test_settings.session_cookie_name, session_token)


def _prepare_and_login_verified_user(
    client,
    test_settings,
    email: str,
    login: str,
    grant_access: bool = False,
    role: str = "user",
):
    _prepare_verified_user(client, test_settings, email, login, grant_access=grant_access, role=role)
    _login_verified_user(client, test_settings, email)


def test_materials_redirects_unauthenticated_user(client):
    response = client.get("/materials", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/login"


def test_shared_stylesheet_uses_main_page_theme(client):
    response = client.get("/static/styles.css")
    assert response.status_code == 200
    assert "--bg: #faf6f1;" in response.text
    assert "--primary: #c45c26;" in response.text
    assert "font-family: var(--font-display);" in response.text
    assert ".learning-card-note," in response.text
    assert "width: min(60ch, 100%);" in response.text
    assert "margin-left: auto;" in response.text
    assert "margin-right: auto;" in response.text
    assert "text-align: center;" in response.text


def test_materials_shows_locked_state_without_access(client, test_settings):
    _prepare_and_login_verified_user(client, test_settings, "materials-locked@example.com", "materialslocked")
    response = client.get("/materials")
    assert response.status_code == 200
    assert "/static/styles.css" in response.text
    assert "Доступ ограничен" in response.text
    assert "Раздел «Работа с ИИ» закрыт" in response.text
    assert "Доступ к материалам и урокам откроется после оплаты тарифа." in response.text
    assert "В личный кабинет" in response.text
    assert "Курс для новичков без опыта программирования." not in response.text
    assert "Уроки курса" not in response.text
    assert "Как мы работаем: ChatGPT проектирует, Codex выполняет, пользователь проверяет" not in response.text
    assert "/materials/lessons/kak-my-rabotaem-chatgpt-codex-user" not in response.text
    assert "/cabinet" in response.text
    assert "/admin" not in response.text
    assert "Payment" not in response.text
    assert "Locked" not in response.text

    lesson_response = client.get("/materials/lessons/kak-my-rabotaem-chatgpt-codex-user")
    assert lesson_response.status_code == 200
    assert "Доступ ограничен" in lesson_response.text
    assert "Урок и его материалы откроются после оплаты тарифа." in lesson_response.text
    assert "lesson-content" not in lesson_response.text

def test_materials_shows_placeholder_sections_when_access_granted(client, test_settings):
    _prepare_and_login_verified_user(client, test_settings, "materials-open@example.com", "materialsopen", grant_access=True)
    response = client.get("/materials")
    assert response.status_code == 200
    assert "Работа с ИИ" in response.text
    assert "Курс для новичков без опыта программирования." in response.text
    assert "Уроки курса" in response.text
    assert "Как мы работаем: ChatGPT проектирует, Codex выполняет, пользователь проверяет" in response.text
    assert "/materials/lessons/kak-my-rabotaem-chatgpt-codex-user" in response.text
    assert "/static/styles.css" in response.text
    assert "Личный кабинет" in response.text
    assert "Вернуться в личный кабинет" in response.text
    assert "/cabinet" in response.text
    assert "/admin" not in response.text
    assert "Payment" not in response.text
    assert "Content" not in response.text


def test_cabinet_contains_materials_link_and_locked_hint(client, test_settings):
    _prepare_and_login_verified_user(client, test_settings, "materials-cabinet@example.com", "materialscabinet")
    response = client.get("/cabinet")
    assert response.status_code == 200
    assert "Главная" in response.text
    assert "Личный кабинет будет доступен после оплаты" in response.text
    assert "После оплаты тарифа откроются личный кабинет, обучение и материалы." in response.text
    assert "Обучающий блок" not in response.text
    assert "Перейти к обучению" not in response.text
    assert "Обучающий проект" not in response.text
    assert "Скачать файл" not in response.text
    assert "Доступ откроется после оплаты." not in response.text
    assert response.text.count('class="button button-primary learning-button"') == 0
    assert "К обучению" in response.text
    assert 'href="/materials/drafts/dair-smoke-20260529/"' in response.text
    assert 'href="/cabinet/learning/project-file"' not in response.text
    assert "Аккаунты" not in response.text
    assert "/static/cabinet-local-accounts.js" not in response.text
    assert "Пройдите обучение, затем скачайте файл, вставьте в чат ChatGPT и следуйте его инструкциям." not in response.text
    assert "Раздел «Работа с ИИ» будет доступен после оплаты." not in response.text


def test_staff_roles_can_open_materials_without_payment_marker(client, test_settings):
    for role, email, login in [
        ("admin", "materials-admin@example.com", "materialsadmin"),
        ("moderator", "materials-moderator@example.com", "materialsmode"),
    ]:
        client.cookies.clear()
        _prepare_and_login_verified_user(client, test_settings, email, login, role=role)
        response = client.get("/materials")
        assert response.status_code == 200
        assert "Работа с ИИ" in response.text
        assert "Уроки курса" in response.text
        assert "Как мы работаем: ChatGPT проектирует, Codex выполняет, пользователь проверяет" in response.text
        assert "/materials/lessons/kak-my-rabotaem-chatgpt-codex-user" in response.text
        assert "Раздел «Работа с ИИ» будет доступен после оплаты." not in response.text


def test_cabinet_access_labels_for_staff_and_paid_user(client, test_settings):
    _prepare_and_login_verified_user(client, test_settings, "cabinet-paid@example.com", "cabinetpaid", grant_access=True)
    paid_response = client.get("/cabinet")
    assert paid_response.status_code == 200
    assert "Аккаунты" in paid_response.text
    assert "/static/cabinet-local-accounts.js" in paid_response.text
    assert "Перейти к обучению" in paid_response.text
    assert "Скачать файл" in paid_response.text
    assert 'href="/materials/drafts/dair-smoke-20260529/"' in paid_response.text
    assert 'href="/cabinet/learning/project-file"' in paid_response.text

    client.cookies.clear()
    _prepare_and_login_verified_user(client, test_settings, "cabinet-moderator@example.com", "cabinetmod", role="moderator")
    moderator_response = client.get("/cabinet")
    assert moderator_response.status_code == 200
    assert "Аккаунты" in moderator_response.text
    assert "Перейти к обучению" in moderator_response.text
    assert "Скачать файл" in moderator_response.text
    assert 'href="/materials/drafts/dair-smoke-20260529/"' in moderator_response.text
    assert 'href="/cabinet/learning/project-file"' in moderator_response.text

    client.cookies.clear()
    _prepare_and_login_verified_user(client, test_settings, "cabinet-admin@example.com", "cabinetadm", role="admin")
    admin_response = client.get("/cabinet")
    assert admin_response.status_code == 200
    assert "Аккаунты" in admin_response.text
    assert "Перейти к обучению" in admin_response.text
    assert "Скачать файл" in admin_response.text
    assert 'href="/materials/drafts/dair-smoke-20260529/"' in admin_response.text
    assert 'href="/cabinet/learning/project-file"' in admin_response.text


def test_learning_access_helper_and_project_download_route(client, test_settings):
    client.cookies.clear()
    anonymous_response = client.get(LEARNING_PROJECT_DOWNLOAD_URL, follow_redirects=False)
    assert anonymous_response.status_code == 303
    assert anonymous_response.headers["location"] == "/login"

    _prepare_and_login_verified_user(client, test_settings, "learning-locked@example.com", "learninglocked")
    locked_response = client.get(LEARNING_PROJECT_DOWNLOAD_URL, follow_redirects=False)
    assert locked_response.status_code == 403
    assert user_has_materials_access(authenticate_user("learning-locked@example.com", "Secret123", settings=test_settings)) is False

    with _connect(test_settings) as conn:
        conn.execute(
            "UPDATE users SET materials_access_granted_at = CURRENT_TIMESTAMP WHERE email = ?",
            ("learning-locked@example.com",),
        )
        conn.commit()

    unlocked_user = authenticate_user("learning-locked@example.com", "Secret123", settings=test_settings)
    assert user_has_materials_access(unlocked_user) is True

    client.cookies.clear()
    session_token = create_session(unlocked_user.id, settings=test_settings)
    client.cookies.set(test_settings.session_cookie_name, session_token)
    download_response = client.get(LEARNING_PROJECT_DOWNLOAD_URL)
    assert download_response.status_code == 200
    assert "attachment" in download_response.headers.get("content-disposition", "").lower()
    assert LEARNING_PROJECT_FILE_NAME in unquote(download_response.headers.get("content-disposition", ""))
    assert hashlib.sha256(download_response.content).hexdigest() == hashlib.sha256(LEARNING_PROJECT_FILE_PATH.read_bytes()).hexdigest()
    assert LEARNING_PROJECT_FILE_PATH.is_file()
    assert "/static/" not in str(LEARNING_PROJECT_FILE_PATH)

    client.cookies.clear()
    _prepare_and_login_verified_user(client, test_settings, "learning-admin@example.com", "learningadmin", role="admin")
    assert user_has_materials_access(authenticate_user("learning-admin@example.com", "Secret123", settings=test_settings)) is True
    admin_download_response = client.get(LEARNING_PROJECT_DOWNLOAD_URL)
    assert admin_download_response.status_code == 200
    assert hashlib.sha256(admin_download_response.content).hexdigest() == hashlib.sha256(LEARNING_PROJECT_FILE_PATH.read_bytes()).hexdigest()


def test_materials_redirects_unauthenticated_user_is_unchanged(client):
    response = client.get("/materials", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/login"


def test_materials_access_column_exists_after_schema_init(test_settings):
    initialize_database(get_database_path(test_settings))
    with _connect(test_settings) as conn:
        columns = {row["name"] for row in conn.execute("PRAGMA table_info(users)").fetchall()}
    assert "materials_access_granted_at" in columns
```

```diff
diff --git a/source/tests/test_materials_flow.py b/source/tests/test_materials_flow.py
index 10e2f76..a5d83d0 100644
--- a/source/tests/test_materials_flow.py
+++ b/source/tests/test_materials_flow.py
@@ -107,25 +107,24 @@ def test_materials_shows_locked_state_without_access(client, test_settings):
     response = client.get("/materials")
     assert response.status_code == 200
     assert "/static/styles.css" in response.text
-    assert "Работа с ИИ" in response.text
-    assert "Курс для новичков без опыта программирования." in response.text
-    assert "Уроки курса" in response.text
-    assert "Как мы работаем: ChatGPT проектирует, Codex выполняет, пользователь проверяет" in response.text
-    assert "/materials/lessons/kak-my-rabotaem-chatgpt-codex-user" in response.text
-    assert "Вернуться в личный кабинет" in response.text
+    assert "Доступ ограничен" in response.text
+    assert "Раздел «Работа с ИИ» закрыт" in response.text
+    assert "Доступ к материалам и урокам откроется после оплаты тарифа." in response.text
+    assert "В личный кабинет" in response.text
+    assert "Курс для новичков без опыта программирования." not in response.text
+    assert "Уроки курса" not in response.text
+    assert "Как мы работаем: ChatGPT проектирует, Codex выполняет, пользователь проверяет" not in response.text
+    assert "/materials/lessons/kak-my-rabotaem-chatgpt-codex-user" not in response.text
     assert "/cabinet" in response.text
-    assert "Доступные тарифы" not in response.text
-    assert "Оплата" not in response.text
-    assert "Что дальше" not in response.text
-    assert "Раздел «Работа с ИИ» будет доступен после оплаты." not in response.text
-    assert "После первой оплаты доступ к разделу останется навсегда." not in response.text
-    assert "Быстрый старт" not in response.text
-    assert "Как работать с AI-агентом" not in response.text
-    assert "Команды для копирования" not in response.text
     assert "/admin" not in response.text
     assert "Payment" not in response.text
     assert "Locked" not in response.text
 
+    lesson_response = client.get("/materials/lessons/kak-my-rabotaem-chatgpt-codex-user")
+    assert lesson_response.status_code == 200
+    assert "Доступ ограничен" in lesson_response.text
+    assert "Урок и его материалы откроются после оплаты тарифа." in lesson_response.text
+    assert "lesson-content" not in lesson_response.text
 
 def test_materials_shows_placeholder_sections_when_access_granted(client, test_settings):
     _prepare_and_login_verified_user(client, test_settings, "materials-open@example.com", "materialsopen", grant_access=True)
@@ -150,18 +149,20 @@ def test_cabinet_contains_materials_link_and_locked_hint(client, test_settings):
     response = client.get("/cabinet")
     assert response.status_code == 200
     assert "Главная" in response.text
-    assert "Обучающий блок" in response.text
-    assert "Обучение" in response.text
-    assert "Перейти к обучению" in response.text
-    assert "Обучающий проект" in response.text
-    assert "Скачать файл" in response.text
-    assert "Доступ откроется после оплаты." in response.text
-    assert response.text.count('class="button button-primary learning-button"') == 2
-    assert 'href="/materials/drafts/dair-smoke-20260529/"' not in response.text
+    assert "Личный кабинет будет доступен после оплаты" in response.text
+    assert "После оплаты тарифа откроются личный кабинет, обучение и материалы." in response.text
+    assert "Обучающий блок" not in response.text
+    assert "Перейти к обучению" not in response.text
+    assert "Обучающий проект" not in response.text
+    assert "Скачать файл" not in response.text
+    assert "Доступ откроется после оплаты." not in response.text
+    assert response.text.count('class="button button-primary learning-button"') == 0
+    assert "К обучению" in response.text
+    assert 'href="/materials/drafts/dair-smoke-20260529/"' in response.text
     assert 'href="/cabinet/learning/project-file"' not in response.text
-    assert "Аккаунты" in response.text
-    assert "/static/cabinet-local-accounts.js" in response.text
-    assert "Пройдите обучение, затем скачайте файл, вставьте в чат ChatGPT и следуйте его инструкциям." in response.text
+    assert "Аккаунты" not in response.text
+    assert "/static/cabinet-local-accounts.js" not in response.text
+    assert "Пройдите обучение, затем скачайте файл, вставьте в чат ChatGPT и следуйте его инструкциям." not in response.text
     assert "Раздел «Работа с ИИ» будет доступен после оплаты." not in response.text
 
 
```


## 9. CABINET_CURRENT_CODE

### source/app/user_cabinet/routes.py

```py
"""User cabinet routes guarded by the session cookie."""

from decimal import Decimal
import logging
from pathlib import Path
from urllib.parse import urlencode

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from jinja2 import ChoiceLoader, FileSystemLoader

from app.auth.service import (
    AuthError,
    can_manage_account_blocks,
    NotFoundError,
    UnauthorizedError,
    ValidationError,
    change_password,
    get_current_user_from_cookies,
    get_user_by_email,
    list_users_for_admin,
    role_label_ru,
)
from app.account_blocks.schemas import AccountBlockCreateInput, AccountBlockUpdateInput
from app.account_blocks.service import (
    AccountBlockNotFoundError,
    AccountBlockPermissionError,
    AccountBlockValidationError,
    activate_account_block,
    create_account_block,
    delete_account_block,
    get_account_block_copy_data,
    get_account_block_public,
    list_account_blocks_for_viewer,
    renew_account_block,
    update_account_block,
)
from app.core.config import get_settings
from app.notifications.email_service import send_account_block_activation_email
from app.shared.tariff_display import get_homepage_tariff_context
from app.paid_options.service import list_paid_options
from app.materials.service import user_has_materials_access
from app.user_cabinet.prompts_library import load_cabinet_prompts

router = APIRouter()
logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))
templates.env.loader = ChoiceLoader(
    [
        templates.env.loader,
        FileSystemLoader(str(Path(__file__).resolve().parents[1] / "shared" / "templates")),
    ]
)
LEARNING_COURSE_URL = "/materials/drafts/dair-smoke-20260529/"
LEARNING_PROJECT_DOWNLOAD_URL = "/cabinet/learning/project-file"
LEARNING_PROJECT_FILE_NAME = "02_СТАРТ_ПРОЕКТА_GIT_ДОКУМЕНТАЦИЯ_СТРУКТУРА.md"
LEARNING_PROJECT_FILE_PATH = Path(__file__).resolve().parent / "private_files" / LEARNING_PROJECT_FILE_NAME
BASE_CABINET_PAID_OPTION_CODE = "ai_gpt_tool"
ACCOUNT_BLOCK_DURATION_DAYS = 60
ACCOUNT_BLOCK_CREATE_DEFAULT_DURATION_DAYS = 30
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


def _account_block_owner_summary(user) -> dict[str, object]:
    return {
        "id": int(user["id"]) if isinstance(user, dict) else int(user.id),
        "email": user["email"] if isinstance(user, dict) else user.email,
        "login": user["login"] if isinstance(user, dict) else user.login,
        "role": user["role"] if isinstance(user, dict) else user.role,
        "role_label": user.get("role_label") if isinstance(user, dict) else role_label_ru(user.role),
        "display_label": f"{user['login']} · {user['email']}" if isinstance(user, dict) else f"{user.login} · {user.email}",
    }


def _user_attr(user, key: str):
    if isinstance(user, dict):
        return user.get(key)
    return getattr(user, key)


def _account_block_owner_email(settings, owner_user_id: int) -> str | None:
    for owner in list_users_for_admin(settings=settings):
        if int(_user_attr(owner, "id")) == int(owner_user_id):
            return str(_user_attr(owner, "email"))
    return None


def _account_block_card_context(block, copy_data, owner_summary: dict[str, object] | None = None) -> dict[str, object]:
    return {
        "id": block.id,
        "owner_user_id": block.owner_user_id,
        "owner": owner_summary,
        "type": block.type,
        "type_label": ACCOUNT_BLOCK_TYPE_LABELS.get(block.type, block.type),
        "display_title": ACCOUNT_BLOCK_CARD_TITLE_LABELS.get(block.type, block.title),
        "display_type_label": ACCOUNT_BLOCK_CARD_TYPE_LABELS.get(block.type, ACCOUNT_BLOCK_TYPE_LABELS.get(block.type, block.type)),
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


def _account_block_notice(request: Request) -> str | None:
    notice_key = (request.query_params.get("account_blocks_notice") or "").strip().lower()
    return ACCOUNT_BLOCK_NOTICE_MESSAGES.get(notice_key)


def _selected_account_block_email(request: Request, fallback_email: str) -> str:
    raw_email = (request.query_params.get("account_blocks_user_email") or "").strip()
    return raw_email or fallback_email


def _paid_option_duration_days(option) -> int:
    if option.default_duration_days is not None and int(option.default_duration_days) > 0:
        return int(option.default_duration_days)
    return ACCOUNT_BLOCK_DURATION_DAYS


def _active_paid_options_for_cabinet(settings):
    options = [
        option
        for option in list_paid_options(settings=settings)
        if option.code != BASE_CABINET_PAID_OPTION_CODE
    ]
    options.sort(key=_cabinet_paid_option_sort_key)
    return [
        {
            "id": option.id,
            "code": option.code,
            "title": option.title,
            "description": option.description,
            "formatted_price": _format_price(option.price_amount_minor, option.currency),
            "currency": option.currency,
            "default_duration_days": option.default_duration_days,
            "resolved_duration_days": _paid_option_duration_days(option),
            "is_renewable": option.is_renewable,
            "status": option.status,
        }
        for option in options
    ]


def _resolve_account_block_selected_user(user, settings, request: Request) -> tuple[object | None, str, str | None]:
    manage_mode = can_manage_account_blocks(user)
    notice = _account_block_notice(request)
    selected_email = _selected_account_block_email(request, user.email)

    if not manage_mode:
        return user, user.email, notice

    if selected_email != user.email:
        try:
            selected_user = get_user_by_email(selected_email, settings=settings)
        except ValidationError:
            return None, selected_email, "Пользователь не найден."
        if selected_user is None:
            return None, selected_email, "Пользователь не найден."
        return selected_user, selected_email, notice

    return user, user.email, notice


def _account_block_management_context(user, settings, request: Request) -> dict[str, object]:
    manage_mode = can_manage_account_blocks(user)
    selected_user, selected_email, notice = _resolve_account_block_selected_user(user, settings, request)
    selected_owner_summary = _account_block_owner_summary(selected_user) if selected_user is not None else None
    selected_blocks = []
    if selected_user is not None:
        visible_blocks = list_account_blocks_for_viewer(user, owner_user_id=int(selected_user.id), settings=settings)
        if not manage_mode:
            visible_blocks = [block for block in visible_blocks if block.is_active]
        selected_blocks = [
            _account_block_card_context(
                block,
                get_account_block_copy_data(actor=user, block_id=block.id, settings=settings),
                selected_owner_summary,
            )
            for block in visible_blocks
        ]

    return {
        "account_blocks_manage_mode": manage_mode,
        "account_block_query_string": f"?{urlencode({'account_blocks_user_email': selected_email})}" if manage_mode else "",
        "account_block_owner_options": [
            {
                "email": _user_attr(owner, "email"),
                "login": _user_attr(owner, "login"),
                "role": _user_attr(owner, "role"),
                "role_label": role_label_ru(_user_attr(owner, "role")),
                "display_label": f"{_user_attr(owner, 'login')} · {_user_attr(owner, 'email')}",
            }
            for owner in list_users_for_admin(settings=settings)
        ]
        if manage_mode
        else [],
        "account_block_selected_user": selected_user,
        "account_block_selected_user_email": selected_email,
        "account_block_selected_user_summary": selected_owner_summary,
        "account_block_blocks": selected_blocks,
        "account_block_notice": notice,
        "account_block_create_default_duration_days": ACCOUNT_BLOCK_CREATE_DEFAULT_DURATION_DAYS,
    }


def _cabinet_account_block_redirect(*, notice_key: str, selected_user_email: str | None = None) -> RedirectResponse:
    query = {"account_blocks_notice": notice_key}
    if selected_user_email:
        query["account_blocks_user_email"] = selected_user_email
    return RedirectResponse(url=f"/cabinet?{urlencode(query)}", status_code=303)


def _selected_email_for_block(request: Request, settings, fallback_email: str, owner_user_id: int) -> str:
    selected_email = _selected_account_block_email(request, fallback_email)
    if selected_email != fallback_email:
        return selected_email
    owner_email = _account_block_owner_email(settings, owner_user_id)
    return owner_email or fallback_email


def _parse_account_block_form_fields(
    *,
    owner_user_id: int,
    block_type: str,
    login: str,
    password_secret: str,
    duration_days: int,
) -> AccountBlockCreateInput:
    return AccountBlockCreateInput(
        owner_user_id=owner_user_id,
        type=block_type,
        login=login,
        password_secret=password_secret,
        duration_days=duration_days,
    )


def _parse_account_block_update_fields(
    *,
    login: str | None,
    password_secret: str | None,
) -> AccountBlockUpdateInput:
    return AccountBlockUpdateInput(
        login=login if login is not None else None,
        password_secret=password_secret if password_secret is not None else None,
    )


def _parse_account_block_duration(value: str | None, *, default: int = ACCOUNT_BLOCK_DURATION_DAYS) -> int:
    raw = (value or "").strip()
    if not raw:
        return default
    try:
        parsed = int(raw)
    except ValueError as exc:
        raise AccountBlockValidationError("duration_days must be an integer") from exc
    if parsed <= 0:
        raise AccountBlockValidationError("duration_days must be greater than 0")
    return parsed


def _parse_optional_account_block_duration(value: str | None) -> int | None:
    raw = (value or "").strip()
    if not raw:
        return None
    try:
        parsed = int(raw)
    except ValueError as exc:
        raise AccountBlockValidationError("duration_days must be an integer") from exc
    if parsed <= 0:
        raise AccountBlockValidationError("duration_days must be greater than 0")
    return parsed


def _resolve_create_duration_days(form) -> int:
    return _parse_account_block_duration(
        form.get("duration_days"),
        default=ACCOUNT_BLOCK_CREATE_DEFAULT_DURATION_DAYS,
    )


def _format_price(amount_minor: int | None, currency: str | None) -> str:
    if amount_minor is None:
        return "Цена не указана"

    amount = Decimal(int(amount_minor)) / Decimal(100)
    if amount == amount.to_integral():
        amount_text = f"{int(amount):,}".replace(",", " ")
    else:
        amount_text = f"{amount:,.2f}".replace(",", " ").replace(".", ",")

    currency_code = (currency or "RUB").upper()
    currency_suffix = "₽" if currency_code == "RUB" else currency_code
    return f"{amount_text} {currency_suffix}"


def _cabinet_paid_option_sort_key(option):
    amount_minor = option.price_amount_minor
    return (
        amount_minor is None,
        -(amount_minor or 0),
        int(option.sort_order),
        option.title.casefold(),
        int(option.id),
    )


def _active_paid_options_for_cabinet(settings):
    options = [
        option
        for option in list_paid_options(settings=settings)
        if option.code != BASE_CABINET_PAID_OPTION_CODE
    ]
    options.sort(key=_cabinet_paid_option_sort_key)
    return [
        {
            "id": option.id,
            "code": option.code,
            "title": option.title,
            "description": option.description,
            "formatted_price": _format_price(option.price_amount_minor, option.currency),
            "currency": option.currency,
            "default_duration_days": option.default_duration_days,
            "resolved_duration_days": _paid_option_duration_days(option),
            "is_renewable": option.is_renewable,
            "status": option.status,
        }
        for option in options
    ]


def _template(request: Request, template_name: str, **context) -> HTMLResponse:
    payload = {
        "request": request,
        "title": context.pop("title", "Страница"),
        "current_user": get_current_user_from_cookies(request.cookies, settings=get_settings()),
    }
    payload.update(context)
    return templates.TemplateResponse(request, template_name, payload)


def _locked_response(
    request: Request,
    *,
    title: str,
    locked_title: str,
    locked_message: str,
    locked_action_label: str = "На главную",
    locked_action_url: str = "/",
    locked_secondary_label: str | None = None,
    locked_secondary_url: str | None = None,
    current_user=None,
):
    return _template(
        request,
        "access_locked.html",
        title=title,
        locked_title=locked_title,
        locked_message=locked_message,
        locked_action_label=locked_action_label,
        locked_action_url=locked_action_url,
        locked_secondary_label=locked_secondary_label,
        locked_secondary_url=locked_secondary_url,
        current_user=current_user,
        **get_homepage_tariff_context(settings=get_settings()),
    )


def _password_change_message(exc: ValidationError | UnauthorizedError | AuthError) -> str:
    message = str(exc)
    normalized = message.lower()
    if isinstance(exc, UnauthorizedError):
        return "Текущий пароль неверный."
    if "passwords do not match" in normalized:
        return "Новые пароли не совпадают."
    if (
        "password is required" in normalized
        or "at least 8 characters" in normalized
        or "at most 128 characters" in normalized
        or "must not contain spaces" in normalized
    ):
        return "Пароль должен быть не короче 8 символов и без пробелов."
    return "Не удалось сменить пароль."


def _require_authenticated_user(request: Request):
    settings = get_settings()
    user = get_current_user_from_cookies(request.cookies, settings=settings)
    if user is None:
        return settings, None, RedirectResponse(url="/login", status_code=303)
    return settings, user, None


@router.get("/cabinet", response_class=HTMLResponse)
def cabinet_page(request: Request):
    settings, user, redirect_response = _require_authenticated_user(request)
    if redirect_response is not None:
        return redirect_response
    if not user_has_materials_access(user):
        return _locked_response(
            request,
            title="Личный кабинет",
            locked_title="Личный кабинет будет доступен после оплаты",
            locked_message="После оплаты тарифа откроются личный кабинет, обучение и материалы.",
            locked_action_label="На главную",
            locked_action_url="/",
            locked_secondary_label="К обучению",
            locked_secondary_url=LEARNING_COURSE_URL,
            current_user=user,
        )
    learning_access = user_has_materials_access(user)
    active_paid_options = _active_paid_options_for_cabinet(settings)
    account_block_context = _account_block_management_context(user, settings, request)

    return _template(
        request,
        "cabinet.html",
        title="Личный кабинет",
        learning_access=learning_access,
        learning_course_url=LEARNING_COURSE_URL if learning_access else None,
        learning_download_url=LEARNING_PROJECT_DOWNLOAD_URL if learning_access else None,
        cabinet_prompts=load_cabinet_prompts(),
        active_paid_options=active_paid_options,
        active_paid_options_count=len(active_paid_options),
        account_block_type_options=[
            {"value": "chatgpt", "label": "ChatGPT"},
            {"value": "server", "label": "Сервер"},
            {"value": "mail", "label": "Почта"},
            {"value": "vpn", "label": "ВПН"},
        ],
        **account_block_context,
    )


@router.head("/cabinet")
def cabinet_head(request: Request):
    response = cabinet_page(request)
    return response


@router.get("/cabinet/settings", response_class=HTMLResponse)
def cabinet_settings_page(request: Request):
    settings, user, redirect_response = _require_authenticated_user(request)
    if redirect_response is not None:
        return redirect_response
    return _template(
        request,
        "settings.html",
        title="Настройки",
        user_email=user.email,
        user_login=user.login,
        success=request.query_params.get("success") == "1",
        notice="Пароль изменён." if request.query_params.get("success") == "1" else None,
    )


@router.head("/cabinet/settings")
def cabinet_settings_head(request: Request):
    response = cabinet_settings_page(request)
    return response


@router.get("/cabinet/learning/project-file")
def cabinet_learning_project_file(request: Request):
    settings, user, redirect_response = _require_authenticated_user(request)
    if redirect_response is not None:
        return redirect_response
    if not user_has_materials_access(user):
        raise HTTPException(status_code=403, detail="learning access required")
    if not LEARNING_PROJECT_FILE_PATH.is_file():
        raise HTTPException(status_code=404, detail="learning project file not found")
    return FileResponse(
        path=str(LEARNING_PROJECT_FILE_PATH),
        filename=LEARNING_PROJECT_FILE_NAME,
        media_type="text/markdown; charset=utf-8",
    )


@router.post("/cabinet/settings/password", response_class=HTMLResponse)
def cabinet_change_password(
    request: Request,
    current_password: str = Form(default=""),
    password: str = Form(default=""),
    repeat_password: str = Form(default=""),
) -> HTMLResponse:
    settings, user, redirect_response = _require_authenticated_user(request)
    if redirect_response is not None:
        return redirect_response
    try:
        change_password(
            user_id=user.id,
            current_password=current_password,
            new_password=password,
            repeat_password=repeat_password,
            settings=settings,
        )
    except NotFoundError:
        return RedirectResponse(url="/login", status_code=303)
    except (ValidationError, UnauthorizedError, AuthError) as exc:
        return _template(
            request,
            "settings.html",
            title="Настройки",
            user_email=user.email,
            user_login=user.login,
            error=_password_change_message(exc),
            success=False,
        )
    return RedirectResponse(url="/cabinet/settings?success=1", status_code=303)


@router.post("/cabinet/account-blocks")
def cabinet_create_account_block(
    request: Request,
    block_type: str = Form(alias="type", default=""),
    login: str = Form(default=""),
    password_secret: str = Form(default=""),
    duration_days: str = Form(default=""),
):
    settings, user, redirect_response = _require_authenticated_user(request)
    if redirect_response is not None:
        return redirect_response
    if not can_manage_account_blocks(user):
        raise HTTPException(status_code=403, detail="account block management requires moderator or admin access")
    try:
        selected_user, selected_email, _ = _resolve_account_block_selected_user(user, settings, request)
        if selected_user is None:
            raise HTTPException(status_code=400, detail="Пользователь не найден.")
        created_block = create_account_block(
            actor=user,
            data=_parse_account_block_form_fields(
                owner_user_id=int(selected_user.id),
                block_type=block_type,
                login=login,
                password_secret=password_secret,
                duration_days=_resolve_create_duration_days({"duration_days": duration_days}),
            ),
            settings=settings,
        )
    except AccountBlockPermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except (AccountBlockValidationError, AccountBlockNotFoundError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return _cabinet_account_block_redirect(notice_key="created", selected_user_email=selected_email)


@router.post("/cabinet/account-blocks/{block_id}")
def cabinet_update_account_block(
    request: Request,
    block_id: int,
    login: str = Form(default=""),
    password_secret: str = Form(default=""),
):
    settings, user, redirect_response = _require_authenticated_user(request)
    if redirect_response is not None:
        return redirect_response
    if not can_manage_account_blocks(user):
        raise HTTPException(status_code=403, detail="account block management requires moderator or admin access")
    try:
        existing_block = get_account_block_public(actor=user, block_id=block_id, settings=settings)
        selected_email = _selected_email_for_block(
            request,
            settings,
            user.email,
            existing_block.owner_user_id,
        )
        updated_block = update_account_block(
            actor=user,
            block_id=block_id,
            data=_parse_account_block_update_fields(
                login=login,
                password_secret=password_secret,
            ),
            settings=settings,
        )
    except AccountBlockPermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except AccountBlockNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AccountBlockValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return _cabinet_account_block_redirect(notice_key="updated", selected_user_email=selected_email)


@router.post("/cabinet/account-blocks/{block_id}/delete")
def cabinet_delete_account_block(request: Request, block_id: int):
    settings, user, redirect_response = _require_authenticated_user(request)
    if redirect_response is not None:
        return redirect_response
    if not can_manage_account_blocks(user):
        raise HTTPException(status_code=403, detail="account block management requires moderator or admin access")
    try:
        existing_block = get_account_block_public(actor=user, block_id=block_id, settings=settings)
        selected_email = _selected_email_for_block(
            request,
            settings,
            user.email,
            existing_block.owner_user_id,
        )
        delete_account_block(actor=user, block_id=block_id, settings=settings)
    except AccountBlockPermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except AccountBlockNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _cabinet_account_block_redirect(notice_key="deleted", selected_user_email=selected_email)


@router.post("/cabinet/account-blocks/{block_id}/activate")
def cabinet_activate_account_block(
    request: Request,
    block_id: int,
    duration_days: str = Form(default=""),
):
    settings, user, redirect_response = _require_authenticated_user(request)
    if redirect_response is not None:
        return redirect_response
    if not can_manage_account_blocks(user):
        raise HTTPException(status_code=403, detail="account block management requires moderator or admin access")
    try:
        existing_block = get_account_block_public(actor=user, block_id=block_id, settings=settings)
        selected_email = _selected_email_for_block(
            request,
            settings,
            user.email,
            existing_block.owner_user_id,
        )
        duration_days_value = _parse_optional_account_block_duration(duration_days)
        activation_result = activate_account_block(
            actor=user,
            block_id=block_id,
            duration_days=duration_days_value,
            settings=settings,
        )
        notice_key = "activated"
        if activation_result.notification is not None:
            try:
                send_account_block_activation_email(activation_result.notification, settings=settings)
                notice_key = "activated_email_sent"
            except Exception as exc:
                logger.warning(
                    "Account block activation email failed for block_id=%s owner_user_id=%s: %s",
                    block_id,
                    activation_result.block.owner_user_id,
                    exc,
                )
                notice_key = "activated_email_failed"
        else:
            notice_key = "activated_email_failed"
    except AccountBlockPermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except AccountBlockNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AccountBlockValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return _cabinet_account_block_redirect(
        notice_key=notice_key,
        selected_user_email=selected_email,
    )


@router.post("/cabinet/account-blocks/{block_id}/renew")
def cabinet_renew_account_block(
    request: Request,
    block_id: int,
    duration_days: str = Form(default=""),
):
    settings, user, redirect_response = _require_authenticated_user(request)
    if redirect_response is not None:
        return redirect_response
    if not can_manage_account_blocks(user):
        raise HTTPException(status_code=403, detail="account block management requires moderator or admin access")
    try:
        existing_block = get_account_block_public(actor=user, block_id=block_id, settings=settings)
        selected_email = _selected_email_for_block(
            request,
            settings,
            user.email,
            existing_block.owner_user_id,
        )
        duration_days_value = _parse_optional_account_block_duration(duration_days)
        renew_account_block(
            actor=user,
            block_id=block_id,
            duration_days=duration_days_value,
            settings=settings,
        )
    except AccountBlockPermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except AccountBlockNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AccountBlockValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return _cabinet_account_block_redirect(notice_key="renewed", selected_user_email=selected_email)
```

```diff
(no diff)
```


### source/app/user_cabinet/templates/cabinet.html

```html
{% extends "base.html" %}

{% block content %}
  <section class="card stack learning-card">
    <h2 class="section-title learning-card-title">Обучающий блок</h2>
    <div class="learning-grid">
      <div class="learning-column">
        <h2 class="section-title">Обучение</h2>
        {% if learning_access %}
          <a class="button button-primary learning-button" href="{{ learning_course_url }}">Перейти к обучению</a>
        {% else %}
          <button class="button button-primary learning-button" type="button" disabled>Перейти к обучению</button>
        {% endif %}
      </div>

      <div class="learning-column">
        <h2 class="section-title">Обучающий проект</h2>
        {% if learning_access %}
          <a class="button button-primary learning-button" href="{{ learning_download_url }}">Скачать файл</a>
        {% else %}
          <button class="button button-primary learning-button" type="button" disabled>Скачать файл</button>
        {% endif %}
      </div>
    </div>
    <p class="form-help learning-card-note">Пройдите обучение, затем скачайте файл, вставьте в чат ChatGPT и следуйте его инструкциям.</p>
    {% if not learning_access %}
      <p class="form-help learning-card-lock">Доступ откроется после оплаты.</p>
    {% endif %}
  </section>

  {% set vpn_account_blocks = account_block_blocks | selectattr('type', 'equalto', 'vpn') | list %}
  {% set regular_account_blocks = account_block_blocks | rejectattr('type', 'equalto', 'vpn') | list %}

  <section id="accounts" class="card stack accounts-card accounts-card--cabinet" data-local-accounts-root data-account-blocks-source="server">
    <div class="accounts-header">
      <div class="stack accounts-intro">
        <h2 class="section-title">Аккаунты</h2>
      </div>

      {% if account_blocks_manage_mode %}
        <form class="accounts-search stack" method="get" action="/cabinet">
          <label class="form-row accounts-field">
            <span>Email пользователя</span>
            <input
              class="input"
              name="account_blocks_user_email"
              type="email"
              list="account-block-user-email-list"
              value="{{ account_block_selected_user_email }}"
              placeholder="user@example.com"
              autocomplete="email"
              required
            >
          </label>
          <datalist id="account-block-user-email-list">
            {% for option in account_block_owner_options %}
              <option value="{{ option.email }}">{{ option.display_label }}</option>
            {% endfor %}
          </datalist>
          <div class="actions">
            <button class="button button-primary" type="submit">Найти пользователя</button>
          </div>
        </form>
      {% endif %}
    </div>

    <p class="accounts-notice" data-account-blocks-notice aria-live="polite" role="status">{{ account_block_notice or "" }}</p>

    {% if account_blocks_manage_mode and account_block_selected_user_summary %}
      <section class="card stack accounts-selected-user">
        <h3 class="section-title">Выбранный пользователь</h3>
        <p class="form-help">Email: <strong>{{ account_block_selected_user_summary.email }}</strong></p>
        <p class="form-help">Логин: <strong>{{ account_block_selected_user_summary.login }}</strong></p>
        <p class="form-help">Роль: <strong>{{ account_block_selected_user_summary.role_label }}</strong></p>
      </section>
    {% endif %}

    {% if account_blocks_manage_mode %}
      <div class="accounts-builder-shell">
        <form
          class="accounts-builder accounts-builder--server"
          method="post"
          action="/cabinet/account-blocks{{ account_block_query_string }}"
          data-account-block-form="create"
        >
          <label class="form-row accounts-type-field">
            <span>Тип блока</span>
            <select class="select" name="type" required>
              {% for option in account_block_type_options %}
                <option value="{{ option.value }}" {% if option.value == 'chatgpt' %}selected{% endif %}>{{ option.label }}</option>
              {% endfor %}
            </select>
          </label>
          <label class="form-row accounts-field">
            <span>Срок, дней</span>
            <input class="input" name="duration_days" type="number" min="1" value="{{ account_block_create_default_duration_days }}" data-account-block-duration-input>
          </label>
          <label class="form-row accounts-field">
            <span>Логин</span>
            <input class="input" name="login" type="text" placeholder="Логин" autocomplete="off">
          </label>
          <label class="form-row accounts-field">
            <span>Пароль</span>
            <input class="input" name="password_secret" type="text" placeholder="Пароль" autocomplete="off">
          </label>
          <button class="button button-primary" type="submit">Добавить блок</button>
        </form>
      </div>
    {% endif %}

    {% if regular_account_blocks %}
      <div class="accounts-grid">
        {% for block in regular_account_blocks %}
          <article class="account-card">
            <header class="account-card__header">
              <div class="stack account-card__headline">
                <div class="account-card__badges">
                  <span class="account-card__type-badge">{{ block.display_type_label or block.type_label }}</span>
                  {% if block.is_active %}
                    <span class="account-card__status-badge account-card__status-badge--active">Активно</span>
                  {% elif block.is_expired %}
                    <span class="account-card__status-badge account-card__status-badge--expired">{{ block.status_label }}</span>
                  {% else %}
                    <span class="account-card__status-badge account-card__status-badge--inactive">{{ block.status_label }}</span>
                  {% endif %}
                </div>
                {% if account_blocks_manage_mode %}
                  <p class="form-help account-card__owner-line">Пользователь: {{ account_block_selected_user_summary.email }} · {{ account_block_selected_user_summary.login }}</p>
                {% endif %}
              </div>
            </header>

            <div class="account-card__body">
              <div class="account-card__readonly" data-account-card-view>
                <label class="account-field">
                  <span>Логин</span>
                  <input class="input account-field__input" data-account-field="login" type="text" value="{{ block.login|e }}" readonly>
                  <div class="account-field__actions">
                    <button class="button button-secondary account-copy-button" type="button" data-account-copy>Скопировать</button>
                  </div>
                </label>
                <label class="account-field">
                  <span>Пароль</span>
                  <input class="input account-field__input" data-account-field="password" type="password" value="{{ block.password_secret|e }}" readonly>
                  <div class="account-field__actions account-field__actions--split">
                    <button
                      class="button button-secondary account-password-toggle"
                      type="button"
                      data-account-password-toggle
                      aria-label="Показать пароль"
                      aria-pressed="false"
                    >
                      Показать
                    </button>
                    <button class="button button-secondary account-copy-button" type="button" data-account-copy>Скопировать</button>
                  </div>
                </label>
                <div class="account-card__details">
                  <p class="account-card__detail">{{ block.activation_summary }}</p>
                </div>
                {% if account_blocks_manage_mode %}
                  <div class="account-actions account-actions--view">
                    <button class="button button-secondary account-card__edit-toggle" type="button" data-account-card-edit-toggle>Редактировать</button>
                    <form class="account-action-form" method="post" action="/cabinet/account-blocks/{{ block.id }}/delete{{ account_block_query_string }}" data-account-block-form="delete">
                      <button class="button button-secondary button-danger account-card__delete" type="submit">Удалить</button>
                    </form>
                    <form class="account-action-form" method="post" action="/cabinet/account-blocks/{{ block.id }}/activate{{ account_block_query_string }}" data-account-block-form="activate">
                      <label class="account-field account-field--compact">
                        <span>Срок, дней</span>
                        <input class="input" name="duration_days" type="number" min="1" value="{{ block.duration_days }}" data-account-block-duration-input>
                      </label>
                      <button class="button button-primary account-card__activate" type="submit">Активировать</button>
                    </form>
                    {% if block.is_active %}
                      <form class="account-action-form" method="post" action="/cabinet/account-blocks/{{ block.id }}/renew{{ account_block_query_string }}" data-account-block-form="renew">
                        <label class="account-field account-field--compact">
                          <span>Срок, дней</span>
                          <input class="input" name="duration_days" type="number" min="1" value="{{ block.duration_days }}" data-account-block-duration-input>
                        </label>
                        <button class="button button-primary account-card__renew" type="submit">Продлить активацию</button>
                      </form>
                    {% endif %}
                  </div>
                {% endif %}
              </div>

              {% if account_blocks_manage_mode %}
                <form class="account-card__edit-form" method="post" action="/cabinet/account-blocks/{{ block.id }}{{ account_block_query_string }}" hidden data-account-card-edit-form data-account-block-form="update">
                  <label class="account-field">
                    <span>Логин</span>
                    <input class="input account-field__input" data-account-field="login" name="login" type="text" value="{{ block.login|e }}" autocomplete="off">
                  </label>
                  <label class="account-field">
                    <span>Пароль</span>
                    <input class="input account-field__input" data-account-field="password" name="password_secret" type="password" value="{{ block.password_secret|e }}" autocomplete="off">
                    <div class="account-field__actions">
                      <button
                        class="button button-secondary account-password-toggle"
                        type="button"
                        data-account-password-toggle
                        aria-label="Показать пароль"
                        aria-pressed="false"
                      >
                        Показать
                      </button>
                    </div>
                  </label>
                  <div class="account-actions account-actions--edit">
                    <button class="button button-primary account-card__save" type="submit">Сохранить</button>
                    <button class="button button-secondary account-card__cancel" type="button" data-account-card-edit-cancel>Отмена</button>
                  </div>
                </form>
              {% endif %}
            </div>
          </article>
        {% endfor %}
      </div>
    {% else %}
      {% if not account_blocks_manage_mode or account_block_selected_user_summary %}
        <p class="form-help accounts-empty">Тут появятся блоки с данными для авторизации после того, как администратор активирует опции. Обычно это занимает не более суток после оплаты.</p>
      {% endif %}
    {% endif %}
  </section>

  {% for block in vpn_account_blocks %}
    <section class="card stack cabinet-vpn-section" data-cabinet-vpn-section>
      <details class="cabinet-vpn-disclosure">
        <summary class="cabinet-vpn-summary">
          <h2 class="section-title cabinet-vpn-summary__title">ВПН</h2>
          <p class="form-help cabinet-vpn-summary__hint">Видеоинструкция и ссылка Amnezia VPN</p>
        </summary>
        <div class="cabinet-vpn-content">
          <div class="vpn-card__video-panel">
            <video
              class="vpn-card__video"
              controls
              preload="metadata"
              src="/static/videos/amnezia-vpn-guide.mp4"
            ></video>
          </div>

          <p class="cabinet-vpn-note">После просмотра откройте сайт Amnezia VPN и используйте IP из блока «<a href="#accounts">Сервер</a>».</p>

          <a
            class="button button-primary vpn-card__link"
            href="https://m-d0d72068b914-3w5hsuiikq-ez.a.run.app/ru"
            target="_blank"
            rel="noreferrer"
          >
            Открыть сайт Amnezia VPN
          </a>

          {% if account_blocks_manage_mode %}
            <div class="account-actions account-actions--view">
              <form class="account-action-form" method="post" action="/cabinet/account-blocks/{{ block.id }}/delete{{ account_block_query_string }}" data-account-block-form="delete">
                <button class="button button-secondary button-danger account-card__delete" type="submit">Удалить</button>
              </form>
              <form class="account-action-form" method="post" action="/cabinet/account-blocks/{{ block.id }}/activate{{ account_block_query_string }}" data-account-block-form="activate">
                <label class="account-field account-field--compact">
                  <span>Срок, дней</span>
                  <input class="input" name="duration_days" type="number" min="1" value="{{ block.duration_days }}" data-account-block-duration-input>
                </label>
                <button class="button button-primary account-card__activate" type="submit">Активировать</button>
              </form>
              {% if block.is_active %}
                <form class="account-action-form" method="post" action="/cabinet/account-blocks/{{ block.id }}/renew{{ account_block_query_string }}" data-account-block-form="renew">
                  <label class="account-field account-field--compact">
                    <span>Срок, дней</span>
                    <input class="input" name="duration_days" type="number" min="1" value="{{ block.duration_days }}" data-account-block-duration-input>
                  </label>
                  <button class="button button-primary account-card__renew" type="submit">Продлить активацию</button>
                </form>
              {% endif %}
            </div>
          {% endif %}
        </div>
      </details>
    </section>
  {% endfor %}

  <section class="card stack prompts-library-card" data-prompts-library-root>
    <div class="prompts-library-header">
      <div class="stack prompts-library-intro">
        <h2 class="section-title">Промпты</h2>
        <p class="form-help">Здесь собраны промпты из курса и ваши личные промпты. Их можно редактировать, копировать и скачивать как Markdown.</p>
      </div>
      <button class="button button-primary prompts-add-button" type="button" data-prompts-add>Добавить промпт</button>
    </div>

    <section class="prompts-section">
      <div class="prompts-section__header">
        <h3 class="section-title prompts-section__title">Промпты из курса</h3>
      </div>
      <div class="prompts-grid prompts-grid--built-in" data-prompts-built-in-list>
        {% for prompt in cabinet_prompts %}
          <article
            class="prompt-card prompt-card--built-in prompt-card--collapsed"
            data-prompt-id="{{ prompt.id|e }}"
            data-prompt-filename="{{ prompt.filename|e }}"
            data-prompt-owner="{{ prompt.owner_label|e }}"
            data-prompt-source-label="{{ (prompt.source_label or '')|e }}"
            data-prompt-title="{{ prompt.title|e }}"
            data-prompt-expanded="false"
          >
            <div class="prompt-card__header">
              <div class="stack prompt-card__intro">
                <h4 class="prompt-card__title">{{ prompt.title }}</h4>
                <p class="prompt-card__meta">{{ prompt.owner_label }}{% if prompt.source_label %} · {{ prompt.source_label }}{% endif %}</p>
                <p class="prompt-card__filename">Файл: {{ prompt.filename }}</p>
              </div>
              <div class="prompt-card__header-actions">
                <span class="prompt-card__badge">Курс</span>
                <button
                  class="button button-secondary prompt-card__toggle"
                  type="button"
                  data-prompt-toggle
                  aria-controls="prompt-body-{{ prompt.id|e }}"
                  aria-expanded="false"
                >
                  Развернуть
                </button>
              </div>
            </div>
            <div class="prompt-card__body" id="prompt-body-{{ prompt.id|e }}" data-prompt-body hidden>
              <label class="prompt-field">
                <span>Промпт</span>
                <textarea class="textarea prompt-textarea" data-prompt-textarea readonly rows="12">{{ prompt.markdown }}</textarea>
              </label>
              <div class="prompt-actions prompt-actions--built-in">
                <button class="button button-secondary" type="button" data-prompt-edit>Редактировать</button>
                <button class="button button-primary" type="button" data-prompt-save hidden>Сохранить</button>
                <button class="button button-secondary" type="button" data-prompt-copy>Скопировать</button>
                <button class="button button-secondary" type="button" data-prompt-download>Скачать .md</button>
                <button class="button button-secondary" type="button" data-prompt-reset>Сбросить к версии курса</button>
              </div>
            </div>
          </article>
        {% endfor %}
      </div>
    </section>

    <section class="prompts-section">
      <div class="prompts-section__header">
        <h3 class="section-title prompts-section__title">Мои промпты</h3>
      </div>
      <p class="form-help prompts-empty" data-prompts-empty>Пока нет ни одного личного промпта. Добавьте первый выше.</p>
      <div class="prompts-grid prompts-grid--custom" data-prompts-custom-list></div>
      <template data-prompts-custom-template>
        <article class="prompt-card prompt-card--custom prompt-card--collapsed" data-prompt-custom data-prompt-expanded="false">
          <div class="prompt-card__header">
            <div class="stack prompt-card__intro">
              <h4 class="prompt-card__title" data-prompt-summary-title>Новый промпт</h4>
              <p class="prompt-card__meta">Личный промпт</p>
              <p class="prompt-card__filename">Файл: custom-prompt.md</p>
            </div>
            <div class="prompt-card__header-actions">
              <span class="prompt-card__badge">Личный</span>
              <button
                class="button button-secondary prompt-card__toggle"
                type="button"
                data-prompt-toggle
                aria-controls="prompt-body-custom"
                aria-expanded="false"
              >
                Развернуть
              </button>
            </div>
          </div>
          <div class="prompt-card__body" id="prompt-body-custom" data-prompt-body hidden>
            <label class="prompt-title-field">
              <span>Название</span>
              <input class="input prompt-title-input" type="text" data-prompt-title placeholder="Название промпта" autocomplete="off">
            </label>
            <label class="prompt-field">
              <span>Промпт</span>
              <textarea class="textarea prompt-textarea" data-prompt-textarea rows="12" placeholder="Введите текст промпта"></textarea>
            </label>
            <div class="prompt-actions prompt-actions--custom">
              <button class="button button-secondary" type="button" data-prompt-edit>Редактировать</button>
              <button class="button button-primary" type="button" data-prompt-save>Сохранить</button>
              <button class="button button-secondary" type="button" data-prompt-copy>Скопировать</button>
              <button class="button button-secondary" type="button" data-prompt-download>Скачать .md</button>
              <button class="button button-secondary" type="button" data-prompt-delete>Удалить</button>
            </div>
          </div>
        </article>
      </template>
    </section>

    <p class="prompts-notice" data-prompts-notice aria-live="polite" role="status"></p>
  </section>

  <section class="card stack paid-options-card" data-paid-options-root>
    <div class="paid-options-header">
      <div class="stack paid-options-intro">
        <h2 class="section-title">Активация опций</h2>
        <p class="form-help">Здесь показаны активные платные опции, которые можно будет подключать к аккаунту.</p>
        {% if active_paid_options_count %}
          <p class="paid-options-count">Доступно для подключения: {{ active_paid_options_count }}</p>
        {% endif %}
      </div>
    </div>

    {% if active_paid_options %}
      <div class="paid-options-grid" data-paid-options-list>
        {% for option in active_paid_options %}
          <article class="paid-option-card" data-paid-option-card data-paid-option-id="{{ option.id|e }}">
            <div class="stack paid-option__intro">
              <div class="paid-option__headline">
                <h3 class="paid-option__title">{{ option.title }}</h3>
                <span class="paid-option__badge">Активно</span>
              </div>
              {% if option.description %}
                <p class="paid-option__description">{{ option.description }}</p>
              {% endif %}
            </div>

            <div class="stack paid-option__meta">
              <p class="paid-option__price">{{ option.formatted_price }}</p>
              {% if option.default_duration_days %}
                <p class="paid-option__duration">Срок: {{ option.default_duration_days }} дней</p>
              {% endif %}
              {% if option.is_renewable %}
                <p class="paid-option__renewable">Можно продлевать</p>
              {% endif %}
            </div>

            <div class="paid-option__actions">
              <button class="button button-primary paid-option__buy" type="button" data-paid-option-buy>Купить</button>
            </div>
          </article>
        {% endfor %}
      </div>
    {% else %}
      <p class="form-help paid-options-empty">Пока нет активных опций для подключения.</p>
    {% endif %}

    <p class="paid-options-notice" data-paid-options-notice aria-live="polite" role="status"></p>
  </section>
  <script>
    (() => {
      const getAccountsRoot = () => document.querySelector("[data-local-accounts-root][data-account-blocks-source='server']");
      if (!getAccountsRoot()) {
        return;
      }

      const setNotice = (message) => {
        const root = getAccountsRoot();
        const notice = root ? root.querySelector("[data-account-blocks-notice]") : null;
        if (!notice) {
          return;
        }
        notice.textContent = message;
      };

      const copyText = async (value) => {
        if (navigator.clipboard && typeof navigator.clipboard.writeText === "function") {
          await navigator.clipboard.writeText(value);
          return true;
        }

        const textarea = document.createElement("textarea");
        textarea.value = value;
        textarea.setAttribute("readonly", "true");
        textarea.style.position = "fixed";
        textarea.style.opacity = "0";
        textarea.style.left = "-9999px";
        document.body.appendChild(textarea);
        textarea.select();

        let copied = false;
        try {
          copied = document.execCommand("copy");
        } catch (_error) {
          copied = false;
        }

        document.body.removeChild(textarea);
        return copied;
      };

      const resetPasswordVisibility = (container) => {
        if (!(container instanceof HTMLElement)) {
          return;
        }

        container.querySelectorAll("[data-account-password-toggle]").forEach((button) => {
          if (!(button instanceof HTMLButtonElement)) {
            return;
          }

          const field = button.closest(".account-field");
          const input = field ? field.querySelector('input[data-account-field="password"]') : null;
          if (!(input instanceof HTMLInputElement)) {
            return;
          }

          input.type = "password";
          button.textContent = "Показать";
          button.setAttribute("aria-label", "Показать пароль");
          button.setAttribute("aria-pressed", "false");
        });
      };

      document.addEventListener("click", async (event) => {
        const editToggle = event.target.closest("[data-account-card-edit-toggle]");
        if (editToggle) {
          const root = editToggle.closest("[data-local-accounts-root][data-account-blocks-source='server']");
          const card = editToggle.closest(".account-card");
          const view = card ? card.querySelector("[data-account-card-view]") : null;
          const form = card ? card.querySelector("[data-account-card-edit-form]") : null;
          if (root instanceof HTMLElement && view instanceof HTMLElement && form instanceof HTMLFormElement) {
            view.hidden = true;
            form.hidden = false;
            card.classList.add("account-card--editing");
            resetPasswordVisibility(card);
            const firstInput = form.querySelector("input[name='login']");
            if (firstInput instanceof HTMLInputElement) {
              firstInput.focus();
              if (typeof firstInput.select === "function") {
                firstInput.select();
              }
            }
          }
          return;
        }

        const editCancel = event.target.closest("[data-account-card-edit-cancel]");
        if (editCancel) {
          const root = editCancel.closest("[data-local-accounts-root][data-account-blocks-source='server']");
          const card = editCancel.closest(".account-card");
          const view = card ? card.querySelector("[data-account-card-view]") : null;
          const form = card ? card.querySelector("[data-account-card-edit-form]") : null;
          if (root instanceof HTMLElement && view instanceof HTMLElement && form instanceof HTMLFormElement) {
            form.reset();
            resetPasswordVisibility(card);
            form.hidden = true;
            view.hidden = false;
            card.classList.remove("account-card--editing");
          }
          return;
        }

        const passwordToggle = event.target.closest("[data-account-password-toggle]");
        if (passwordToggle) {
          const root = passwordToggle.closest("[data-local-accounts-root][data-account-blocks-source='server']");
          if (!root) {
            return;
          }

          const field = passwordToggle.closest(".account-field");
          const input = field ? field.querySelector('input[data-account-field="password"]') : null;
          if (!(input instanceof HTMLInputElement)) {
            return;
          }

          const isHidden = input.type === "password";
          input.type = isHidden ? "text" : "password";
          const isVisible = input.type === "text";
          passwordToggle.textContent = isVisible ? "Скрыть" : "Показать";
          passwordToggle.setAttribute("aria-label", isVisible ? "Скрыть пароль" : "Показать пароль");
          passwordToggle.setAttribute("aria-pressed", String(isVisible));
          return;
        }

        const button = event.target.closest("[data-account-copy]");
        if (!button) {
          return;
        }

        const root = button.closest("[data-local-accounts-root][data-account-blocks-source='server']");
        if (!root) {
          return;
        }

        const field = button.closest(".account-field");
        const input = field ? field.querySelector("input") : null;
        const value = input instanceof HTMLInputElement ? input.value : "";
        if (!value) {
          setNotice("Нечего копировать.");
          return;
        }

        try {
          const copied = await copyText(value);
          setNotice(copied ? "Скопировано." : "Не удалось скопировать.");
        } catch (_error) {
          setNotice("Не удалось скопировать.");
        }
      });

      document.addEventListener(
        "submit",
        async (event) => {
          const form = event.target;
          if (!(form instanceof HTMLFormElement)) {
            return;
          }
          if (!form.matches("[data-account-block-form]")) {
            return;
          }

          const root = form.closest("[data-local-accounts-root][data-account-blocks-source='server']");
          if (!root) {
            return;
          }

          event.preventDefault();

          if (form.dataset.accountBlockSubmitting === "true") {
            return;
          }

          const submitButton = form.querySelector('button[type="submit"]');
          const scrollX = window.scrollX;
          const scrollY = window.scrollY;
          form.dataset.accountBlockSubmitting = "true";
          if (submitButton instanceof HTMLButtonElement) {
            submitButton.disabled = true;
          }

          try {
            const response = await fetch(form.action, {
              method: form.method || "POST",
              body: new FormData(form),
              credentials: "same-origin",
              headers: {
                "X-Requested-With": "XMLHttpRequest",
              },
            });

            const bodyText = await response.text();
            if (!response.ok) {
              setNotice("Не удалось выполнить действие.");
              return;
            }

            const parsed = new DOMParser().parseFromString(bodyText, "text/html");
            const nextRoot = parsed.querySelector("[data-local-accounts-root][data-account-blocks-source='server']");
            const currentRoot = getAccountsRoot();
            if (!(nextRoot instanceof HTMLElement) || !(currentRoot instanceof HTMLElement)) {
              if (response.url) {
                window.history.replaceState({}, "", response.url);
              }
              return;
            }

            currentRoot.replaceWith(nextRoot);
            if (response.url) {
              window.history.replaceState({}, "", response.url);
            }
            requestAnimationFrame(() => {
              window.scrollTo(scrollX, scrollY);
            });
          } catch (_error) {
            setNotice("Не удалось выполнить действие.");
          } finally {
            if (submitButton instanceof HTMLButtonElement) {
              submitButton.disabled = false;
            }
            form.dataset.accountBlockSubmitting = "false";
          }
        },
        true,
      );

    })();
  </script>
  <script src="/static/cabinet-local-accounts.js"></script>
  <script src="/static/cabinet-prompts-library.js"></script>
  <script>
    (() => {
      const root = document.querySelector("[data-paid-options-root]");
      if (!root) {
        return;
      }

      const notice = root.querySelector("[data-paid-options-notice]");
      root.addEventListener("click", (event) => {
        const button = event.target.closest("[data-paid-option-buy]");
        if (!button) {
          return;
        }

        if (notice) {
          notice.textContent = "Оплата пока не подключена. Эта кнопка подготовлена для следующего этапа.";
        }
      });
    })();
  </script>
{% endblock %}
```

```diff
(no diff)
```


### source/app/user_cabinet/templates/access_locked.html

```html
{% extends "base.html" %}

{% block content %}
  <section class="stack">
    <div class="card stack">
      <p class="muted">Доступ ограничен</p>
      <h1 class="section-title">{{ locked_title }}</h1>
      <p class="form-help">{{ locked_message }}</p>
      {% if current_user %}
        <p class="form-help">Вы вошли как {{ current_user.email }}{% if current_user.login %} · {{ current_user.login }}{% endif %}.</p>
      {% endif %}
      <div class="actions">
        <a class="button button-primary" href="{{ locked_action_url }}">{{ locked_action_label }}</a>
        {% if locked_secondary_label and locked_secondary_url %}
          <a class="button button-secondary" href="{{ locked_secondary_url }}">{{ locked_secondary_label }}</a>
        {% endif %}
      </div>
    </div>
  </section>
{% endblock %}
```


### source/app/user_cabinet/prompts_library.py

```py
"""Prompt library helpers for the personal cabinet."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

COURSE_DRAFT_ID = "dair_smoke_20260529"
COURSE_SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "materials"
    / "course_content"
    / "drafts"
    / COURSE_DRAFT_ID
    / "script.js"
)

STARTER_PROMPT_FILENAME_RE = re.compile(r'starterPromptFilename:\s*"(?P<filename>[^"]+)"')
STARTER_PROMPT_LABEL_RE = re.compile(r'starterPromptLabel:\s*"(?P<label>[^"]+)"')
PROMPT_FORM_RE = re.compile(
    r'promptForm:\s*\{\s*id:\s*"(?P<id>[^"]+)"\s*,\s*label:\s*"(?P<label>[^"]+)"\s*,\s*description:\s*"(?P<description>[^"]+)"\s*,\s*actionsLabel:\s*"(?P<actions_label>[^"]+)"\s*,\s*filename:\s*"(?P<filename>[^"]+)"\s*,\s*markdown:\s*',
    re.S,
)


def _read_course_script() -> str:
    return COURSE_SCRIPT_PATH.read_text(encoding="utf-8")


def _skip_whitespace(text: str, index: int) -> int:
    while index < len(text) and text[index].isspace():
        index += 1
    return index


def _extract_template_literal(text: str, index: int) -> tuple[str, int]:
    position = _skip_whitespace(text, index)
    if position >= len(text):
        raise ValueError("Expected a template literal")

    quote = text[position]
    if quote not in {"`", '"', "'"}:
        raise ValueError("Expected a template literal")

    chars: list[str] = []
    cursor = position + 1
    while cursor < len(text):
        char = text[cursor]
        if char == "\\":
            if cursor + 1 >= len(text):
                raise ValueError("Unterminated escape in template literal")
            escaped = text[cursor + 1]
            if quote == "`" and escaped == "$" and cursor + 2 < len(text) and text[cursor + 2] == "{":
                chars.append("${")
                cursor += 3
                continue
            if escaped == quote or escaped == "\\":
                chars.append("`")
                if escaped != "`":
                    chars[-1] = escaped
                cursor += 2
                continue
            escape_map = {
                "n": "\n",
                "r": "\r",
                "t": "\t",
                "b": "\b",
                "f": "\f",
                "v": "\v",
                "0": "\0",
            }
            chars.append(escape_map.get(escaped, escaped))
            cursor += 2
            continue
        if char == quote:
            return "".join(chars), cursor + 1
        chars.append(char)
        cursor += 1

    raise ValueError("Unterminated template literal")


def _extract_section(script_text: str, lesson_id: str, next_lesson_id: str) -> str:
    start = script_text.index(f'id: "{lesson_id}"')
    end = script_text.index(f'id: "{next_lesson_id}"', start)
    return script_text[start:end]


def _normalize_title(markdown: str) -> str:
    match = re.search(r"^\s*#\s+(.+?)\s*$", markdown, re.M)
    if match:
        return match.group(1).strip()

    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return "Prompt"


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower())
    return slug.strip("-") or "prompt"


def _lesson_owner_label(lesson_number: int) -> str:
    return f"Урок {lesson_number}"


def _build_starter_prompt(section: str, lesson_number: int) -> dict[str, Any]:
    filename_match = STARTER_PROMPT_FILENAME_RE.search(section)
    if filename_match is None:
        raise ValueError(f"Missing starterPromptFilename for lesson {lesson_number}")

    markdown_marker = section.index("starterPromptMarkdown:")
    markdown, _ = _extract_template_literal(section, markdown_marker + len("starterPromptMarkdown:"))
    label_match = STARTER_PROMPT_LABEL_RE.search(section)
    filename = filename_match.group("filename")
    title = _normalize_title(markdown)
    prompt_id = f"lesson-{lesson_number}-{_slugify(Path(filename).stem)}"

    return {
        "id": prompt_id,
        "lesson_number": lesson_number,
        "owner_label": _lesson_owner_label(lesson_number),
        "source_label": label_match.group("label") if label_match else None,
        "title": title,
        "filename": filename,
        "markdown": markdown,
    }


def load_cabinet_prompts() -> list[dict[str, Any]]:
    """Return the current built-in course prompts from the canonical course source."""

    script_text = _read_course_script()
    lesson6 = _extract_section(script_text, "lesson-6", "lesson-7")
    lesson7 = _extract_section(script_text, "lesson-7", "lesson-8")
    lesson8 = _extract_section(script_text, "lesson-8", "lesson-9")

    prompts = [
        _build_starter_prompt(lesson6, 6),
        _build_starter_prompt(lesson7, 7),
    ]

    prompt_form_matches = list(PROMPT_FORM_RE.finditer(lesson8))
    for match in prompt_form_matches:
        markdown, _ = _extract_template_literal(lesson8, match.end())
        filename = match.group("filename")
        prompts.append(
            {
                "id": match.group("id"),
                "lesson_number": 8,
                "owner_label": _lesson_owner_label(8),
                "source_label": match.group("label"),
                "title": _normalize_title(markdown),
                "filename": filename,
                "markdown": markdown,
            }
        )

    return prompts
```

```diff
(no diff)
```


### source/app/account_blocks/__init__.py

```py
"""Server-backed cabinet account blocks."""

from .schemas import (
    AccountBlockActivationNotification,
    AccountBlockActivationResult,
    AccountBlockCopyData,
    AccountBlockCreateInput,
    AccountBlockPublic,
    AccountBlockUpdateInput,
)
from .service import (
    ACCOUNT_BLOCK_TYPES,
    DEFAULT_ACCOUNT_BLOCK_DURATION_DAYS,
    AccountBlockError,
    AccountBlockPermissionError,
    AccountBlockValidationError,
    activate_account_block,
    create_account_block,
    delete_account_block,
    get_account_block_copy_data,
    get_account_block_public,
    list_account_blocks_for_viewer,
    renew_account_block,
    update_account_block,
)
```


### source/app/account_blocks/schemas.py

```py
"""Account-block schemas for server-side cabinet credential blocks."""

from __future__ import annotations

from dataclasses import dataclass


_UNSET = object()


@dataclass(frozen=True, slots=True)
class AccountBlockPublic:
    id: int
    owner_user_id: int
    type: str
    title: str
    login: str
    email: str | None
    status: str
    duration_days: int
    activated_at: str | None
    expires_at: str | None
    remaining_days: int | None
    activation_day: int | None
    activation_summary: str
    is_active: bool
    is_expired: bool
    created_by_user_id: int | None
    updated_by_user_id: int | None
    activated_by_user_id: int | None
    created_at: str
    updated_at: str

    @property
    def can_copy_email(self) -> bool:
        return self.type == "mail" and bool(self.email)


@dataclass(frozen=True, slots=True)
class AccountBlockCreateInput:
    owner_user_id: int
    type: str
    title: str = ""
    login: str = ""
    password_secret: str = ""
    email: str | None = None
    duration_days: int = 60


@dataclass(frozen=True, slots=True)
class AccountBlockUpdateInput:
    owner_user_id: int | None | object = _UNSET
    type: str | None | object = _UNSET
    title: str | None | object = _UNSET
    login: str | None | object = _UNSET
    password_secret: str | None | object = _UNSET
    email: str | None | object = _UNSET
    duration_days: int | None | object = _UNSET


@dataclass(frozen=True, slots=True, repr=False)
class AccountBlockCopyData:
    login: str
    password_secret: str
    email: str | None


@dataclass(frozen=True, slots=True)
class AccountBlockActivationNotification:
    recipient_email: str
    subject: str
    body_text: str
    template_key: str
    block_id: int
    owner_user_id: int
    owner_login: str
    owner_email: str
    block_title: str
    block_type: str
    activated_at: str
    expires_at: str


@dataclass(frozen=True, slots=True)
class AccountBlockActivationResult:
    block: AccountBlockPublic
    notification: AccountBlockActivationNotification | None
```


### source/app/account_blocks/service.py

```py
"""Backend service for server-side cabinet account blocks."""

from __future__ import annotations

import re
from dataclasses import asdict, fields
from datetime import timedelta
from math import ceil

from app.auth.schemas import UserPublic
from app.auth.service import can_manage_account_blocks
from app.core.config import Settings, get_settings
from app.shared.db import get_connection, get_database_path, initialize_database
from app.shared.utils import utc_now, utc_now_iso

from .schemas import (
    AccountBlockActivationNotification,
    AccountBlockActivationResult,
    AccountBlockCopyData,
    AccountBlockCreateInput,
    AccountBlockPublic,
    AccountBlockUpdateInput,
    _UNSET,
)


ACCOUNT_BLOCK_TYPES = ("chatgpt", "server", "mail", "vpn")
ACCOUNT_BLOCK_ACTIVE_STATUS = "active"
ACCOUNT_BLOCK_INACTIVE_STATUS = "inactive"
ACCOUNT_BLOCK_EXPIRED_STATUS = "expired"
ACCOUNT_BLOCK_STATUSES = (
    ACCOUNT_BLOCK_INACTIVE_STATUS,
    ACCOUNT_BLOCK_ACTIVE_STATUS,
    ACCOUNT_BLOCK_EXPIRED_STATUS,
)
DEFAULT_ACCOUNT_BLOCK_DURATION_DAYS = 60
TITLE_MAX_LENGTH = 200
TEXT_MAX_LENGTH = 4000
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
ACCOUNT_BLOCK_TYPE_LABELS = {
    "chatgpt": "ChatGPT",
    "server": "Сервер",
    "mail": "Почта",
    "vpn": "ВПН",
}


class AccountBlockError(Exception):
    """Base class for account-block service errors."""


class AccountBlockValidationError(AccountBlockError):
    pass


class AccountBlockPermissionError(AccountBlockError):
    pass


class AccountBlockNotFoundError(AccountBlockError):
    pass


def _settings(settings: Settings | None = None) -> Settings:
    return settings or get_settings()


def _database_path(settings: Settings | None = None):
    return get_database_path(_settings(settings))


def _connection(settings: Settings | None = None):
    resolved = _settings(settings)
    path = _database_path(resolved)
    initialize_database(path)
    return get_connection(path)


def _normalize_text(value: str | None, field_name: str, *, allow_empty: bool = False, limit: int = TEXT_MAX_LENGTH) -> str:
    normalized = "" if value is None else str(value).strip()
    if not normalized and not allow_empty:
        raise AccountBlockValidationError(f"{field_name} is required")
    if len(normalized) > limit:
        raise AccountBlockValidationError(f"{field_name} must be at most {limit} characters")
    return normalized


def _normalize_optional_text(value: str | None, *, limit: int = TEXT_MAX_LENGTH) -> str | None:
    if value is None:
        return None
    normalized = str(value).strip()
    if not normalized:
        return None
    if len(normalized) > limit:
        raise AccountBlockValidationError(f"value must be at most {limit} characters")
    return normalized


def _normalize_block_type(value: str | None) -> str:
    normalized = _normalize_text(value, "type").lower()
    if normalized not in ACCOUNT_BLOCK_TYPES:
        raise AccountBlockValidationError("unsupported account block type")
    return normalized


def _normalize_duration_days(value: int | str | None, *, default: int = DEFAULT_ACCOUNT_BLOCK_DURATION_DAYS) -> int:
    if value is None:
        return default
    if isinstance(value, bool):
        raise AccountBlockValidationError("duration_days must be an integer")
    if isinstance(value, int):
        normalized = value
    else:
        raw = str(value).strip()
        if not raw:
            return default
        try:
            normalized = int(raw)
        except ValueError as exc:
            raise AccountBlockValidationError("duration_days must be an integer") from exc
    if normalized <= 0:
        raise AccountBlockValidationError("duration_days must be greater than 0")
    return normalized


def _remaining_days_label(remaining_days: int) -> str:
    if remaining_days == 1:
        suffix = "день"
    elif 2 <= remaining_days % 10 <= 4 and not 12 <= remaining_days % 100 <= 14:
        suffix = "дня"
    else:
        suffix = "дней"
    return f"Осталось {remaining_days} {suffix}"


def _normalize_owner_user_id(value: int | str | None, field_name: str = "owner_user_id") -> int:
    if value is None:
        raise AccountBlockValidationError(f"{field_name} is required")
    if isinstance(value, bool):
        raise AccountBlockValidationError(f"{field_name} must be an integer")
    if isinstance(value, int):
        normalized = value
    else:
        raw = str(value).strip()
        if not raw:
            raise AccountBlockValidationError(f"{field_name} is required")
        try:
            normalized = int(raw)
        except ValueError as exc:
            raise AccountBlockValidationError(f"{field_name} must be an integer") from exc
    if normalized <= 0:
        raise AccountBlockValidationError(f"{field_name} must be greater than 0")
    return normalized


def _normalize_email(value: str | None) -> str | None:
    normalized = _normalize_optional_text(value)
    if normalized is None:
        return None
    if not EMAIL_RE.fullmatch(normalized):
        raise AccountBlockValidationError("email must be a valid email address")
    return normalized.lower()


def _normalize_password_secret(value: str | None) -> str:
    # Password values are kept behind the service boundary. App-level encryption is not yet implemented.
    return _normalize_text(value, "password_secret", allow_empty=True)


def _account_block_type_label(block_type: str) -> str:
    return ACCOUNT_BLOCK_TYPE_LABELS.get(block_type, block_type)


def _account_block_title_for_type(block_type: str) -> str:
    return _account_block_type_label(block_type)


def _normalize_account_block_input(data: AccountBlockCreateInput | AccountBlockUpdateInput | None = None, *, create: bool) -> dict[str, object]:
    if data is None:
        raise AccountBlockValidationError("data is required")
    if create:
        payload = asdict(data)
        owner_user_id = _normalize_owner_user_id(payload["owner_user_id"])
        block_type = _normalize_block_type(payload["type"])
        login = _normalize_text(payload.get("login"), "login", allow_empty=True)
        password_secret = _normalize_password_secret(payload.get("password_secret"))
        _normalize_duration_days(payload.get("duration_days"))
        return {
            "owner_user_id": owner_user_id,
            "type": block_type,
            "title": _account_block_title_for_type(block_type),
            "login": login,
            "password_secret": password_secret,
            "duration_days": _normalize_duration_days(payload.get("duration_days")),
        }

    payload = {field.name: getattr(data, field.name) for field in fields(data)}
    cleaned: dict[str, object] = {}
    if payload.get("login") is not _UNSET:
        cleaned["login"] = _normalize_text(payload["login"], "login", allow_empty=True)
    if payload.get("password_secret") is not _UNSET:
        cleaned["password_secret"] = _normalize_password_secret(payload["password_secret"])
    if not cleaned:
        raise AccountBlockValidationError("no account block fields provided")
    return cleaned


def _fetch_user_row(user_id: int, settings: Settings | None = None):
    with _connection(settings) as connection:
        return connection.execute("SELECT * FROM users WHERE id = ?", (int(user_id),)).fetchone()


def _assert_actor_can_manage(actor: UserPublic | None) -> None:
    if actor is None or not can_manage_account_blocks(actor):
        raise AccountBlockPermissionError("account block management requires admin or moderator access")


def _assert_viewer_can_access_block(actor: UserPublic | None, block_owner_user_id: int) -> None:
    if actor is None:
        raise AccountBlockPermissionError("authentication required")
    if can_manage_account_blocks(actor):
        return
    if int(actor.id) != int(block_owner_user_id):
        raise AccountBlockPermissionError("access denied")


def _effective_status(stored_status: str, expires_at: str | None) -> tuple[str, bool, bool, int | None]:
    now = utc_now()
    normalized_status = stored_status if stored_status in ACCOUNT_BLOCK_STATUSES else ACCOUNT_BLOCK_INACTIVE_STATUS
    if normalized_status == ACCOUNT_BLOCK_ACTIVE_STATUS:
        if expires_at is None:
            return ACCOUNT_BLOCK_INACTIVE_STATUS, False, False, None
        expires_dt = _parse_iso_datetime(expires_at)
        if expires_dt is None:
            return ACCOUNT_BLOCK_INACTIVE_STATUS, False, False, None
        if now >= expires_dt:
            return ACCOUNT_BLOCK_EXPIRED_STATUS, False, True, 0
        remaining_seconds = max(0, (expires_dt - now).total_seconds())
        remaining_days = max(0, int(ceil(remaining_seconds / 86400)))
        return ACCOUNT_BLOCK_ACTIVE_STATUS, True, False, remaining_days
    if normalized_status == ACCOUNT_BLOCK_EXPIRED_STATUS:
        return ACCOUNT_BLOCK_EXPIRED_STATUS, False, True, 0 if expires_at else None
    return ACCOUNT_BLOCK_INACTIVE_STATUS, False, False, None


def _parse_iso_datetime(value: str | None):
    if value is None:
        return None
    from datetime import datetime

    return datetime.fromisoformat(value)


def _activation_progress_for_row(row) -> tuple[int | None, str]:
    activated_at = _parse_iso_datetime(row["activated_at"])
    expires_at = _parse_iso_datetime(row["expires_at"])
    if activated_at is None:
        return None, "Не активирован"

    status, is_active, is_expired, remaining_days = _effective_status(str(row["status"]), row["expires_at"])
    if is_active and remaining_days is not None:
        return remaining_days, _remaining_days_label(remaining_days)
    if is_expired:
        return 0, "Срок завершён"
    return None, "Не активирован"


def _account_block_from_row(row) -> AccountBlockPublic:
    status, is_active, is_expired, remaining_days = _effective_status(str(row["status"]), row["expires_at"])
    activation_day, activation_summary = _activation_progress_for_row(row)
    title = _account_block_title_for_type(str(row["type"]))
    owner_row = _fetch_user_row(int(row["owner_user_id"]))
    owner_email = owner_row["email"] if owner_row is not None else None
    email = owner_email if str(row["type"]) == "mail" else row["email"]
    return AccountBlockPublic(
        id=int(row["id"]),
        owner_user_id=int(row["owner_user_id"]),
        type=str(row["type"]),
        title=title,
        login=str(row["login"]),
        email=email,
        status=status,
        duration_days=int(row["duration_days"]),
        activated_at=row["activated_at"],
        expires_at=row["expires_at"],
        remaining_days=remaining_days,
        activation_day=activation_day,
        activation_summary=activation_summary,
        is_active=is_active,
        is_expired=is_expired,
        created_by_user_id=row["created_by_user_id"],
        updated_by_user_id=row["updated_by_user_id"],
        activated_by_user_id=row["activated_by_user_id"],
        created_at=str(row["created_at"]),
        updated_at=str(row["updated_at"]),
    )


def _fetch_account_block_row(block_id: int, settings: Settings | None = None):
    with _connection(settings) as connection:
        return connection.execute("SELECT * FROM account_blocks WHERE id = ?", (int(block_id),)).fetchone()


def _assert_owner_exists(owner_user_id: int, settings: Settings | None = None) -> None:
    if _fetch_user_row(owner_user_id, settings=settings) is None:
        raise AccountBlockNotFoundError("owner user not found")


def _public_view_for_block(block_row) -> AccountBlockPublic:
    return _account_block_from_row(block_row)


def list_account_blocks_for_viewer(
    viewer: UserPublic,
    *,
    owner_user_id: int | None = None,
    settings: Settings | None = None,
) -> list[AccountBlockPublic]:
    with _connection(settings) as connection:
        if can_manage_account_blocks(viewer):
            if owner_user_id is None:
                rows = connection.execute(
                    """
                    SELECT *
                    FROM account_blocks
                    ORDER BY owner_user_id ASC, updated_at DESC, id DESC
                    """,
                ).fetchall()
            else:
                rows = connection.execute(
                    """
                    SELECT *
                    FROM account_blocks
                    WHERE owner_user_id = ?
                    ORDER BY updated_at DESC, id DESC
                    """,
                    (int(owner_user_id),),
                ).fetchall()
        else:
            resolved_owner_user_id = int(owner_user_id) if owner_user_id is not None else int(viewer.id)
            if resolved_owner_user_id != int(viewer.id):
                raise AccountBlockPermissionError("access denied")
            rows = connection.execute(
                """
                SELECT *
                FROM account_blocks
                WHERE owner_user_id = ?
                ORDER BY updated_at DESC, id DESC
                """,
                (resolved_owner_user_id,),
            ).fetchall()
    return [_public_view_for_block(row) for row in rows]


def get_account_block_public(
    *,
    actor: UserPublic,
    block_id: int,
    settings: Settings | None = None,
) -> AccountBlockPublic:
    row = _fetch_account_block_row(block_id, settings=settings)
    if row is None:
        raise AccountBlockNotFoundError("account block not found")
    _assert_viewer_can_access_block(actor, int(row["owner_user_id"]))
    return _public_view_for_block(row)


def get_account_block_copy_data(
    *,
    actor: UserPublic,
    block_id: int,
    settings: Settings | None = None,
) -> AccountBlockCopyData:
    row = _fetch_account_block_row(block_id, settings=settings)
    if row is None:
        raise AccountBlockNotFoundError("account block not found")
    _assert_viewer_can_access_block(actor, int(row["owner_user_id"]))
    owner_row = _fetch_user_row(int(row["owner_user_id"]), settings=settings)
    owner_email = owner_row["email"] if owner_row is not None else None
    email = row["email"]
    if row["type"] == "mail":
        email = owner_email
    return AccountBlockCopyData(
        login=str(row["login"]),
        password_secret=str(row["password_secret"]),
        email=email,
    )


def create_account_block(
    *,
    actor: UserPublic,
    data: AccountBlockCreateInput,
    settings: Settings | None = None,
) -> AccountBlockPublic:
    _assert_actor_can_manage(actor)
    payload = _normalize_account_block_input(data, create=True)
    owner_user_id = int(payload["owner_user_id"])
    _assert_owner_exists(owner_user_id, settings=settings)
    owner_row = _fetch_user_row(owner_user_id, settings=settings)
    owner_email = str(owner_row["email"]) if owner_row is not None else None
    stored_email = owner_email if str(payload["type"]) == "mail" else None
    now_iso = utc_now_iso()
    with _connection(settings) as connection:
        cursor = connection.execute(
            """
            INSERT INTO account_blocks (
                owner_user_id, type, title, login, password_secret, email,
                status, duration_days, activated_at, expires_at,
                created_by_user_id, updated_by_user_id, activated_by_user_id,
                created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, NULL, NULL, ?, ?, NULL, ?, ?)
            """,
            (
                owner_user_id,
                str(payload["type"]),
                str(payload["title"]),
                str(payload["login"]),
                str(payload["password_secret"]),
                stored_email,
                ACCOUNT_BLOCK_INACTIVE_STATUS,
                int(payload["duration_days"]),
                int(actor.id),
                int(actor.id),
                now_iso,
                now_iso,
            ),
        )
        block_id = int(cursor.lastrowid)
        row = connection.execute("SELECT * FROM account_blocks WHERE id = ?", (block_id,)).fetchone()
        if row is None:
            raise AccountBlockError("account block insert failed")
        return _public_view_for_block(row)


def update_account_block(
    *,
    actor: UserPublic,
    block_id: int,
    data: AccountBlockUpdateInput,
    settings: Settings | None = None,
) -> AccountBlockPublic:
    _assert_actor_can_manage(actor)
    payload = _normalize_account_block_input(data, create=False)
    with _connection(settings) as connection:
        row = connection.execute("SELECT * FROM account_blocks WHERE id = ?", (int(block_id),)).fetchone()
        if row is None:
            raise AccountBlockNotFoundError("account block not found")
        updates: list[str] = []
        params: list[object] = []
        if "login" in payload:
            updates.append("login = ?")
            params.append(str(payload["login"]))
        if "password_secret" in payload:
            updates.append("password_secret = ?")
            params.append(str(payload["password_secret"]))
        updates.append("updated_by_user_id = ?")
        params.append(int(actor.id))
        updates.append("updated_at = ?")
        params.append(utc_now_iso())
        params.append(int(block_id))
        connection.execute(
            f"UPDATE account_blocks SET {', '.join(updates)} WHERE id = ?",
            params,
        )
        updated = connection.execute("SELECT * FROM account_blocks WHERE id = ?", (int(block_id),)).fetchone()
        if updated is None:
            raise AccountBlockError("account block update failed")
        return _public_view_for_block(updated)


def delete_account_block(
    *,
    actor: UserPublic,
    block_id: int,
    settings: Settings | None = None,
) -> None:
    _assert_actor_can_manage(actor)
    with _connection(settings) as connection:
        row = connection.execute("SELECT * FROM account_blocks WHERE id = ?", (int(block_id),)).fetchone()
        if row is None:
            raise AccountBlockNotFoundError("account block not found")
        connection.execute("DELETE FROM account_blocks WHERE id = ?", (int(block_id),))


def _activation_notification_for_row(row, *, settings: Settings | None = None) -> AccountBlockActivationNotification | None:
    owner_row = _fetch_user_row(int(row["owner_user_id"]), settings=settings)
    if owner_row is None:
        return None
    recipient_email = str(owner_row["email"])
    if not recipient_email:
        return None
    title = _account_block_title_for_type(str(row["type"]))
    activated_at = str(row["activated_at"])
    expires_at = str(row["expires_at"])
    subject = "Активирована опция OpenScript"
    body_text = (
        "Здравствуйте.\n\n"
        f"У вас активирована опция: {title}.\n\n"
        "Опция активирована на сайте OpenScript:\n"
        "https://openscript.ru/\n\n"
        "Перейти в личный кабинет:\n"
        "https://openscript.ru/cabinet\n\n"
        "Если вы не ожидали это сообщение, просто проигнорируйте его."
    )
    return AccountBlockActivationNotification(
        recipient_email=recipient_email,
        subject=subject,
        body_text=body_text,
        template_key="account_block_activation",
        block_id=int(row["id"]),
        owner_user_id=int(row["owner_user_id"]),
        owner_login=str(owner_row["login"]),
        owner_email=recipient_email,
        block_title=title,
        block_type=str(row["type"]),
        activated_at=activated_at,
        expires_at=expires_at,
    )


def activate_account_block(
    *,
    actor: UserPublic,
    block_id: int,
    duration_days: int | None = None,
    settings: Settings | None = None,
) -> AccountBlockActivationResult:
    _assert_actor_can_manage(actor)
    now = utc_now()
    now_iso = now.isoformat()
    with _connection(settings) as connection:
        row = connection.execute("SELECT * FROM account_blocks WHERE id = ?", (int(block_id),)).fetchone()
        if row is None:
            raise AccountBlockNotFoundError("account block not found")
        resolved_duration_days = _normalize_duration_days(
            duration_days,
            default=int(row["duration_days"] or DEFAULT_ACCOUNT_BLOCK_DURATION_DAYS),
        )
        expires_at = (now + timedelta(days=resolved_duration_days)).isoformat()
        connection.execute(
            """
            UPDATE account_blocks
            SET status = ?,
                duration_days = ?,
                activated_at = ?,
                expires_at = ?,
                activated_by_user_id = ?,
                updated_by_user_id = ?,
                updated_at = ?
            WHERE id = ?
            """,
            (
                ACCOUNT_BLOCK_ACTIVE_STATUS,
                resolved_duration_days,
                now_iso,
                expires_at,
                int(actor.id),
                int(actor.id),
                now_iso,
                int(block_id),
            ),
        )
        updated = connection.execute("SELECT * FROM account_blocks WHERE id = ?", (int(block_id),)).fetchone()
        if updated is None:
            raise AccountBlockError("account block activation failed")
    notification = _activation_notification_for_row(updated, settings=settings)
    return AccountBlockActivationResult(
        block=_public_view_for_block(updated),
        notification=notification,
    )


def renew_account_block(
    *,
    actor: UserPublic,
    block_id: int,
    duration_days: int | None = None,
    settings: Settings | None = None,
) -> AccountBlockPublic:
    _assert_actor_can_manage(actor)
    now = utc_now()
    with _connection(settings) as connection:
        row = connection.execute("SELECT * FROM account_blocks WHERE id = ?", (int(block_id),)).fetchone()
        if row is None:
            raise AccountBlockNotFoundError("account block not found")
        if str(row["status"]) != ACCOUNT_BLOCK_ACTIVE_STATUS:
            raise AccountBlockValidationError("renewal requires an active account block")
        expires_at = _parse_iso_datetime(row["expires_at"])
        if expires_at is None or now >= expires_at:
            raise AccountBlockValidationError("renewal requires an active account block")
        resolved_duration_days = _normalize_duration_days(
            duration_days,
            default=int(row["duration_days"] or DEFAULT_ACCOUNT_BLOCK_DURATION_DAYS),
        )
        new_expires_at = (expires_at + timedelta(days=resolved_duration_days)).isoformat()
        now_iso = utc_now_iso()
        connection.execute(
            """
            UPDATE account_blocks
            SET duration_days = ?,
                expires_at = ?,
                updated_by_user_id = ?,
                updated_at = ?
            WHERE id = ?
            """,
            (
                resolved_duration_days,
                new_expires_at,
                int(actor.id),
                now_iso,
                int(block_id),
            ),
        )
        updated = connection.execute("SELECT * FROM account_blocks WHERE id = ?", (int(block_id),)).fetchone()
        if updated is None:
            raise AccountBlockError("account block renewal failed")
        return _public_view_for_block(updated)
```


### source/app/static/cabinet-prompts-library.js

```js
(() => {
  const STORAGE_KEY = "openscript:cabinet:prompts-library:v1";

  const root = document.querySelector("[data-prompts-library-root]");
  if (!root) {
    return;
  }

  const builtInList = root.querySelector("[data-prompts-built-in-list]");
  const customList = root.querySelector("[data-prompts-custom-list]");
  const emptyElement = root.querySelector("[data-prompts-empty]");
  const noticeElement = root.querySelector("[data-prompts-notice]");
  const addButton = root.querySelector("[data-prompts-add]");
  const customTemplate = root.querySelector("[data-prompts-custom-template]");

  let state = loadState();
  let noticeTimer = null;
  const builtInPrompts = collectBuiltInPrompts();

  function createId() {
    return `prompt_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 10)}`;
  }

  function slugify(value) {
    const slug = String(value || "")
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-+|-+$/g, "");
    return slug || "custom-prompt";
  }

  function normalizeCustomTitle(value) {
    const title = typeof value === "string" ? value.trim() : "";
    return title || "Новый промпт";
  }

  function normalizeState(raw) {
    const source = raw && typeof raw === "object" ? raw : {};
    const overridesSource = source.overrides && typeof source.overrides === "object" ? source.overrides : {};
    const customSource = Array.isArray(source.custom) ? source.custom : [];

    const overrides = {};
    Object.entries(overridesSource).forEach(([id, value]) => {
      const markdown = typeof value?.markdown === "string" ? value.markdown : "";
      if (!markdown) {
        return;
      }
      overrides[id] = {
        title: typeof value?.title === "string" && value.title.trim() ? value.title.trim() : "Промпт",
        markdown,
        updatedAt: typeof value?.updatedAt === "string" ? value.updatedAt : "",
      };
    });

    const custom = customSource.map((rawPrompt) => ({
      id: typeof rawPrompt?.id === "string" && rawPrompt.id ? rawPrompt.id : createId(),
      title: normalizeCustomTitle(rawPrompt?.title),
      markdown: typeof rawPrompt?.markdown === "string" ? rawPrompt.markdown : "",
      updatedAt: typeof rawPrompt?.updatedAt === "string" ? rawPrompt.updatedAt : "",
      isEditing: false,
      isExpanded: false,
    }));

    return { overrides, custom };
  }

  function loadState() {
    try {
      const raw = window.localStorage.getItem(STORAGE_KEY);
      if (!raw) {
        return normalizeState(null);
      }
      return normalizeState(JSON.parse(raw));
    } catch (_error) {
      return normalizeState(null);
    }
  }

  function persistState() {
    try {
      const payload = {
        overrides: state.overrides,
        custom: state.custom.map(({ id, title, markdown, updatedAt }) => ({
          id,
          title,
          markdown,
          updatedAt,
        })),
      };
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
      return true;
    } catch (_error) {
      return false;
    }
  }

  function setNotice(message) {
    if (!noticeElement) {
      return;
    }

    noticeElement.textContent = message;
    if (noticeTimer !== null) {
      window.clearTimeout(noticeTimer);
    }

    if (message) {
      noticeTimer = window.setTimeout(() => {
        noticeElement.textContent = "";
        noticeTimer = null;
      }, 2200);
    }
  }

  async function copyText(text) {
    if (navigator.clipboard && typeof navigator.clipboard.writeText === "function") {
      await navigator.clipboard.writeText(text);
      return true;
    }

    const textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.setAttribute("readonly", "true");
    textarea.style.position = "fixed";
    textarea.style.left = "-9999px";
    textarea.style.top = "0";
    textarea.style.opacity = "0";
    document.body.appendChild(textarea);
    textarea.focus();
    textarea.select();

    let success = false;
    try {
      success = document.execCommand("copy");
    } catch (_error) {
      success = false;
    }

    document.body.removeChild(textarea);
    return success;
  }

  function copyValue(value, successMessage) {
    void (async () => {
      try {
        const copied = await copyText(value);
        setNotice(copied ? successMessage : "Не удалось скопировать");
      } catch (_error) {
        setNotice("Не удалось скопировать");
      }
    })();
  }

  function downloadMarkdown(markdown, filename) {
    const blob = new Blob([markdown], { type: "text/markdown;charset=utf-8" });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    link.rel = "noopener";
    document.body.appendChild(link);
    link.click();
    window.setTimeout(() => {
      window.URL.revokeObjectURL(url);
      link.remove();
    }, 0);
  }

  function setPromptCardExpanded(card, expanded) {
    const body = card.querySelector("[data-prompt-body]");
    const toggleButton = card.querySelector("[data-prompt-toggle]");

    card.dataset.promptExpanded = String(expanded);
    card.classList.toggle("prompt-card--collapsed", !expanded);
    card.classList.toggle("prompt-card--expanded", expanded);

    if (body) {
      body.hidden = !expanded;
    }

    if (toggleButton) {
      toggleButton.setAttribute("aria-expanded", String(expanded));
      toggleButton.textContent = expanded ? "Свернуть" : "Развернуть";
    }
  }

  function collectBuiltInPrompts() {
    if (!builtInList) {
      return [];
    }

    return Array.from(builtInList.querySelectorAll(".prompt-card--built-in")).map((card) => {
      const textarea = card.querySelector("[data-prompt-textarea]");
      return {
        id: card.dataset.promptId || createId(),
        card,
        title: card.dataset.promptTitle || card.querySelector(".prompt-card__title")?.textContent?.trim() || "Промпт",
        ownerLabel: card.dataset.promptOwner || "",
        sourceLabel: card.dataset.promptSourceLabel || "",
        filename: card.dataset.promptFilename || "",
        textarea,
        editButton: card.querySelector("[data-prompt-edit]"),
        saveButton: card.querySelector("[data-prompt-save]"),
        copyButton: card.querySelector("[data-prompt-copy]"),
        downloadButton: card.querySelector("[data-prompt-download]"),
        resetButton: card.querySelector("[data-prompt-reset]"),
        toggleButton: card.querySelector("[data-prompt-toggle]"),
        body: card.querySelector("[data-prompt-body]"),
        originalMarkdown: textarea?.defaultValue || textarea?.value || "",
        isEditing: false,
        isExpanded: false,
      };
    });
  }

  function findBuiltInPrompt(id) {
    return builtInPrompts.find((prompt) => prompt.id === id) || null;
  }

  function applyBuiltInPrompt(prompt) {
    const override = state.overrides[prompt.id];
    const markdown = override ? override.markdown : prompt.originalMarkdown;
    prompt.textarea.value = markdown;
    prompt.textarea.readOnly = !prompt.isEditing;
    prompt.textarea.setAttribute("aria-readonly", String(!prompt.isEditing));
    prompt.card.classList.toggle("prompt-card--editing", prompt.isEditing);
    setPromptCardExpanded(prompt.card, prompt.isEditing || prompt.isExpanded);
    if (prompt.toggleButton) {
      prompt.toggleButton.disabled = prompt.isEditing;
    }
    if (prompt.saveButton) {
      prompt.saveButton.hidden = !prompt.isEditing;
      prompt.saveButton.disabled = !prompt.isEditing;
    }
    if (prompt.editButton) {
      prompt.editButton.disabled = prompt.isEditing;
    }
  }

  function persistBuiltInOverride(prompt) {
    state.overrides[prompt.id] = {
      title: prompt.title,
      markdown: prompt.textarea.value,
      updatedAt: new Date().toISOString(),
    };
    persistState();
  }

  function resetBuiltInOverride(prompt) {
    delete state.overrides[prompt.id];
    prompt.textarea.value = prompt.originalMarkdown;
    persistState();
  }

  function renderBuiltInPrompts() {
    builtInPrompts.forEach((prompt) => {
      applyBuiltInPrompt(prompt);

      if (prompt.toggleButton) {
        prompt.toggleButton.addEventListener("click", () => {
          if (prompt.isEditing) {
            return;
          }
          prompt.isExpanded = !prompt.isExpanded;
          applyBuiltInPrompt(prompt);
        });
      }

      if (prompt.editButton) {
        prompt.editButton.addEventListener("click", () => {
          prompt.isEditing = true;
          prompt.isExpanded = true;
          applyBuiltInPrompt(prompt);
          prompt.textarea.focus();
          prompt.textarea.select();
        });
      }

      if (prompt.saveButton) {
        prompt.saveButton.addEventListener("click", () => {
          persistBuiltInOverride(prompt);
          prompt.isEditing = false;
          prompt.isExpanded = true;
          applyBuiltInPrompt(prompt);
          setNotice("Промпт сохранён");
        });
      }

      if (prompt.copyButton) {
        prompt.copyButton.addEventListener("click", () => {
          copyValue(prompt.textarea.value, "Промпт скопирован");
        });
      }

      if (prompt.downloadButton) {
        prompt.downloadButton.addEventListener("click", () => {
          const filename = prompt.filename || `${slugify(prompt.title)}.md`;
          downloadMarkdown(prompt.textarea.value, filename);
          setNotice("Промпт скачан");
        });
      }

      if (prompt.resetButton) {
        prompt.resetButton.addEventListener("click", () => {
          prompt.isEditing = false;
          prompt.isExpanded = true;
          resetBuiltInOverride(prompt);
          applyBuiltInPrompt(prompt);
          setNotice("Версия курса восстановлена");
        });
      }
    });
  }

  function createCustomPromptCard(prompt) {
    if (!customTemplate) {
      return null;
    }

    const fragment = customTemplate.content.cloneNode(true);
    const card = fragment.querySelector("[data-prompt-custom]");
    const titleInput = card.querySelector("[data-prompt-title]");
    const textarea = card.querySelector("[data-prompt-textarea]");
    const editButton = card.querySelector("[data-prompt-edit]");
    const saveButton = card.querySelector("[data-prompt-save]");
    const copyButton = card.querySelector("[data-prompt-copy]");
    const downloadButton = card.querySelector("[data-prompt-download]");
    const deleteButton = card.querySelector("[data-prompt-delete]");
    const toggleButton = card.querySelector("[data-prompt-toggle]");
    const body = card.querySelector("[data-prompt-body]");
    const summaryTitle = card.querySelector("[data-prompt-summary-title]");

    card.dataset.promptId = prompt.id;
    titleInput.value = prompt.title;
    textarea.value = prompt.markdown;
    card.classList.toggle("prompt-card--editing", prompt.isEditing);
    titleInput.readOnly = !prompt.isEditing;
    textarea.readOnly = !prompt.isEditing;
    if (summaryTitle) {
      summaryTitle.textContent = prompt.title;
    }
    if (editButton) {
      editButton.hidden = prompt.isEditing;
      editButton.disabled = prompt.isEditing;
    }
    if (saveButton) {
      saveButton.hidden = !prompt.isEditing;
      saveButton.disabled = !prompt.isEditing;
    }
    if (toggleButton) {
      toggleButton.disabled = prompt.isEditing;
    }
    setPromptCardExpanded(card, prompt.isEditing || prompt.isExpanded);

    if (editButton) {
      editButton.addEventListener("click", () => {
        prompt.isEditing = true;
        prompt.isExpanded = true;
        renderCustomPrompts();
      });
    }

    if (saveButton) {
      saveButton.addEventListener("click", () => {
        prompt.title = normalizeCustomTitle(titleInput.value);
        prompt.markdown = textarea.value;
        prompt.updatedAt = new Date().toISOString();
        prompt.isEditing = false;
        prompt.isExpanded = true;
        persistState();
        renderCustomPrompts();
        setNotice("Промпт сохранён");
      });
    }

    if (copyButton) {
      copyButton.addEventListener("click", () => {
        copyValue(textarea.value, "Промпт скопирован");
      });
    }

    if (downloadButton) {
      downloadButton.addEventListener("click", () => {
        const filename = `${slugify(titleInput.value || prompt.title)}.md`;
        downloadMarkdown(textarea.value, filename);
        setNotice("Промпт скачан");
      });
    }

    if (deleteButton) {
      deleteButton.addEventListener("click", () => {
        state.custom = state.custom.filter((item) => item.id !== prompt.id);
        persistState();
        renderCustomPrompts();
        setNotice("Промпт удалён");
      });
    }

    if (toggleButton) {
      toggleButton.addEventListener("click", () => {
        if (prompt.isEditing) {
          return;
        }
        prompt.isExpanded = !prompt.isExpanded;
        renderCustomPrompts();
      });
    }

    titleInput.addEventListener("input", () => {
      if (prompt.isEditing) {
        prompt.title = normalizeCustomTitle(titleInput.value);
        if (summaryTitle) {
          summaryTitle.textContent = prompt.title;
        }
      }
    });

    textarea.addEventListener("input", () => {
      if (prompt.isEditing) {
        prompt.markdown = textarea.value;
      }
    });

    return card;
  }

  function renderCustomPrompts() {
    if (!customList) {
      return;
    }

    customList.textContent = "";
    state.custom.forEach((prompt) => {
      const card = createCustomPromptCard(prompt);
      if (card) {
        customList.append(card);
      }
    });

    if (emptyElement) {
      emptyElement.hidden = state.custom.length > 0;
    }
  }

  function addCustomPrompt() {
    state.custom = state.custom.concat({
      id: createId(),
      title: "Новый промпт",
      markdown: "",
      updatedAt: "",
      isEditing: true,
    });
    persistState();
    renderCustomPrompts();

    const lastCard = customList?.querySelector(".prompt-card:last-child");
    const titleInput = lastCard?.querySelector("[data-prompt-title]");
    if (titleInput instanceof HTMLInputElement) {
      titleInput.focus();
      titleInput.select();
    }
  }

  if (addButton) {
    addButton.addEventListener("click", addCustomPrompt);
  }

  renderBuiltInPrompts();
  renderCustomPrompts();
})();
```

```diff
(no diff)
```


### source/app/shared/db.py

```py
"""SQLite persistence helpers for the AI Starter Community MVP."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from app.core.config import Settings, database_path_from_settings

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    login TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user',
    is_active INTEGER NOT NULL DEFAULT 1,
    email_verified_at TEXT NULL,
    materials_access_granted_at TEXT NULL,
    access_status TEXT NOT NULL DEFAULT 'not_activated',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash TEXT UNIQUE NOT NULL,
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    revoked_at TEXT NULL
);

CREATE TABLE IF NOT EXISTS auth_tokens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash TEXT UNIQUE NOT NULL,
    token_type TEXT NOT NULL,
    target_email TEXT NULL,
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    used_at TEXT NULL,
    revoked_at TEXT NULL
);

CREATE TABLE IF NOT EXISTS email_outbox (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipient_email TEXT NOT NULL,
    subject TEXT NOT NULL,
    body_text TEXT NOT NULL,
    template_key TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'queued',
    created_at TEXT NOT NULL,
    sent_at TEXT NULL,
    error TEXT NULL
);

CREATE TABLE IF NOT EXISTS account_blocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type TEXT NOT NULL,
    title TEXT NOT NULL,
    login TEXT NOT NULL DEFAULT '',
    password_secret TEXT NOT NULL DEFAULT '',
    email TEXT NULL,
    status TEXT NOT NULL DEFAULT 'inactive',
    duration_days INTEGER NOT NULL DEFAULT 60,
    activated_at TEXT NULL,
    expires_at TEXT NULL,
    created_by_user_id INTEGER NULL REFERENCES users(id) ON DELETE SET NULL,
    updated_by_user_id INTEGER NULL REFERENCES users(id) ON DELETE SET NULL,
    activated_by_user_id INTEGER NULL REFERENCES users(id) ON DELETE SET NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    CHECK (type IN ('chatgpt', 'server', 'mail')),
    CHECK (status IN ('inactive', 'active', 'expired'))
);

CREATE INDEX IF NOT EXISTS idx_account_blocks_owner_user_id ON account_blocks(owner_user_id);
CREATE INDEX IF NOT EXISTS idx_account_blocks_owner_user_type ON account_blocks(owner_user_id, type);
CREATE INDEX IF NOT EXISTS idx_account_blocks_status ON account_blocks(status);

CREATE TABLE IF NOT EXISTS tariffs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    description TEXT NULL,
    price_amount_minor INTEGER NOT NULL,
    currency TEXT NOT NULL DEFAULT 'RUB',
    status TEXT NOT NULL DEFAULT 'active',
    show_on_homepage INTEGER NOT NULL DEFAULT 0,
    sort_order INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS paid_options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    description TEXT NULL,
    price_amount_minor INTEGER NULL,
    currency TEXT NOT NULL DEFAULT 'RUB',
    default_duration_days INTEGER NULL,
    status TEXT NOT NULL DEFAULT 'active',
    is_renewable INTEGER NOT NULL DEFAULT 1,
    sort_order INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tariff_options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tariff_id INTEGER NOT NULL REFERENCES tariffs(id) ON DELETE CASCADE,
    option_id INTEGER NOT NULL REFERENCES paid_options(id) ON DELETE CASCADE,
    included_duration_days INTEGER NULL,
    included_quantity INTEGER NULL,
    created_at TEXT NOT NULL,
    UNIQUE(tariff_id, option_id)
);
"""


def get_database_path(settings: Settings | None = None) -> Path:
    return database_path_from_settings(settings)


def ensure_database_parent_exists(path: Path | str) -> Path:
    db_path = Path(path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return db_path


def get_connection(path: Path | str) -> sqlite3.Connection:
    db_path = Path(path)
    connection = sqlite3.connect(str(db_path))
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(path: Path | str) -> None:
    db_path = ensure_database_parent_exists(path)
    with sqlite3.connect(str(db_path)) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(SCHEMA_SQL)
        _ensure_users_materials_access_granted_at_column(connection)
        _ensure_tariffs_show_on_homepage_column(connection)


def _ensure_users_materials_access_granted_at_column(connection: sqlite3.Connection) -> None:
    columns = {
        row[1]
        for row in connection.execute("PRAGMA table_info(users)").fetchall()
    }
    if "materials_access_granted_at" not in columns:
        connection.execute("ALTER TABLE users ADD COLUMN materials_access_granted_at TEXT NULL")


def _ensure_tariffs_show_on_homepage_column(connection: sqlite3.Connection) -> None:
    columns = {
        row[1]
        for row in connection.execute("PRAGMA table_info(tariffs)").fetchall()
    }
    if "show_on_homepage" not in columns:
        connection.execute("ALTER TABLE tariffs ADD COLUMN show_on_homepage INTEGER NOT NULL DEFAULT 0")
```

```diff
diff --git a/source/app/shared/db.py b/source/app/shared/db.py
index ad4ecfe..c3de955 100644
--- a/source/app/shared/db.py
+++ b/source/app/shared/db.py
@@ -57,6 +57,31 @@ CREATE TABLE IF NOT EXISTS email_outbox (
     error TEXT NULL
 );
 
+CREATE TABLE IF NOT EXISTS account_blocks (
+    id INTEGER PRIMARY KEY AUTOINCREMENT,
+    owner_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
+    type TEXT NOT NULL,
+    title TEXT NOT NULL,
+    login TEXT NOT NULL DEFAULT '',
+    password_secret TEXT NOT NULL DEFAULT '',
+    email TEXT NULL,
+    status TEXT NOT NULL DEFAULT 'inactive',
+    duration_days INTEGER NOT NULL DEFAULT 60,
+    activated_at TEXT NULL,
+    expires_at TEXT NULL,
+    created_by_user_id INTEGER NULL REFERENCES users(id) ON DELETE SET NULL,
+    updated_by_user_id INTEGER NULL REFERENCES users(id) ON DELETE SET NULL,
+    activated_by_user_id INTEGER NULL REFERENCES users(id) ON DELETE SET NULL,
+    created_at TEXT NOT NULL,
+    updated_at TEXT NOT NULL,
+    CHECK (type IN ('chatgpt', 'server', 'mail')),
+    CHECK (status IN ('inactive', 'active', 'expired'))
+);
+
+CREATE INDEX IF NOT EXISTS idx_account_blocks_owner_user_id ON account_blocks(owner_user_id);
+CREATE INDEX IF NOT EXISTS idx_account_blocks_owner_user_type ON account_blocks(owner_user_id, type);
+CREATE INDEX IF NOT EXISTS idx_account_blocks_status ON account_blocks(status);
+
 CREATE TABLE IF NOT EXISTS tariffs (
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     code TEXT UNIQUE NOT NULL,
@@ -65,6 +90,7 @@ CREATE TABLE IF NOT EXISTS tariffs (
     price_amount_minor INTEGER NOT NULL,
     currency TEXT NOT NULL DEFAULT 'RUB',
     status TEXT NOT NULL DEFAULT 'active',
+    show_on_homepage INTEGER NOT NULL DEFAULT 0,
     sort_order INTEGER NOT NULL DEFAULT 0,
     created_at TEXT NOT NULL,
     updated_at TEXT NOT NULL
@@ -121,6 +147,7 @@ def initialize_database(path: Path | str) -> None:
         connection.execute("PRAGMA foreign_keys = ON")
         connection.executescript(SCHEMA_SQL)
         _ensure_users_materials_access_granted_at_column(connection)
+        _ensure_tariffs_show_on_homepage_column(connection)
 
 
 def _ensure_users_materials_access_granted_at_column(connection: sqlite3.Connection) -> None:
@@ -130,3 +157,12 @@ def _ensure_users_materials_access_granted_at_column(connection: sqlite3.Connect
     }
     if "materials_access_granted_at" not in columns:
         connection.execute("ALTER TABLE users ADD COLUMN materials_access_granted_at TEXT NULL")
+
+
+def _ensure_tariffs_show_on_homepage_column(connection: sqlite3.Connection) -> None:
+    columns = {
+        row[1]
+        for row in connection.execute("PRAGMA table_info(tariffs)").fetchall()
+    }
+    if "show_on_homepage" not in columns:
+        connection.execute("ALTER TABLE tariffs ADD COLUMN show_on_homepage INTEGER NOT NULL DEFAULT 0")
```


### source/tests/test_cabinet_paid_options.py

```py
from __future__ import annotations

import re
import sqlite3

from app.auth.service import register_user, verify_email
from app.paid_options.service import create_paid_option, list_paid_options


def _verify_registered_user(client, test_settings, email: str, login: str):
    register_user(
        email=email,
        login=login,
        password="Secret123",
        repeat_password="Secret123",
        settings=test_settings,
    )
    outbox = client.get("/check-email?registered=1")
    assert outbox.status_code == 200


def _extract_token_from_db(test_settings, email: str):
    with sqlite3.connect(test_settings.database_path) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT body_text FROM email_outbox WHERE recipient_email = ? AND template_key = ? ORDER BY id DESC LIMIT 1",
            (email, "email_verification"),
        ).fetchone()
    assert row is not None
    match = re.search(r"/verify-email/([A-Za-z0-9_-]+)", row["body_text"])
    assert match
    return match.group(1)


def _login_registered_user(client, test_settings, email: str, login: str):
    _verify_registered_user(client, test_settings, email, login)
    token = _extract_token_from_db(test_settings, email)
    verify_email(token, settings=test_settings)

    with sqlite3.connect(test_settings.database_path) as conn:
        conn.execute(
            "UPDATE users SET materials_access_granted_at = CURRENT_TIMESTAMP WHERE email = ?",
            (email,),
        )
        conn.commit()

    login_response = client.post(
        "/login",
        data={"email_or_login": email, "password": "Secret123"},
        follow_redirects=False,
    )
    assert login_response.status_code == 303


def _create_paid_option(test_settings, **kwargs):
    return create_paid_option(settings=test_settings, **kwargs)


def _extract_paid_option_titles(body: str) -> list[str]:
    return re.findall(r'<h3 class="paid-option__title">([^<]+)</h3>', body)


def test_cabinet_paid_options_block_hides_base_option_and_sorts_visible_addons(client, test_settings):
    _create_paid_option(
        test_settings,
        code="ai_gpt_tool",
        title="AI / GPT-инструмент",
        description="Базовый AI-инструмент для старта.",
        price_amount_minor=699000,
        currency="RUB",
        default_duration_days=None,
        status="active",
        is_renewable=True,
        sort_order=0,
    )
    _create_paid_option(
        test_settings,
        code="cabinet_addon_two_thousand_chatgpt_plus",
        title="Chat GPT Plus",
        description="Оплаченный на месяц аккаунт Chat GPT Plus",
        price_amount_minor=200000,
        currency="RUB",
        default_duration_days=30,
        status="active",
        is_renewable=True,
        sort_order=0,
    )
    _create_paid_option(
        test_settings,
        code="cabinet_addon_four_thousand_server_plus_chatgpt",
        title="Сервер + ChatGPT Plus",
        description="Аренда сервера, плюс оплаченный аккаунт ChatGPT Plus.",
        price_amount_minor=400000,
        currency="RUB",
        default_duration_days=30,
        status="active",
        is_renewable=True,
        sort_order=0,
    )
    _create_paid_option(
        test_settings,
        code="cabinet_addon_two_thousand_server",
        title="Сервер",
        description="Аренда сервера.",
        price_amount_minor=200000,
        currency="RUB",
        default_duration_days=30,
        status="active",
        is_renewable=True,
        sort_order=1,
    )
    _create_paid_option(
        test_settings,
        code="cabinet_archived_option",
        title="Архивная опция",
        description="Не должна отображаться в кабинете.",
        price_amount_minor=500000,
        currency="RUB",
        default_duration_days=30,
        status="archived",
        is_renewable=True,
        sort_order=99,
    )
    _create_paid_option(
        test_settings,
        code="cabinet_hidden_option",
        title="Скрытая опция",
        description="Не должна отображаться в кабинете.",
        price_amount_minor=100000,
        currency="RUB",
        default_duration_days=30,
        status="hidden",
        is_renewable=True,
        sort_order=99,
    )

    active_option_codes = {item.code for item in list_paid_options(settings=test_settings)}
    assert active_option_codes == {
        "ai_gpt_tool",
        "cabinet_addon_two_thousand_chatgpt_plus",
        "cabinet_addon_four_thousand_server_plus_chatgpt",
        "cabinet_addon_two_thousand_server",
    }
    assert "cabinet_archived_option" not in active_option_codes
    assert "cabinet_hidden_option" not in active_option_codes

    _login_registered_user(client, test_settings, "cabinet-paid-options@example.com", "cabinetpaidoptions")

    response = client.get("/cabinet")
    assert response.status_code == 200
    body = response.text

    assert body.index('data-local-accounts-root') < body.index('data-prompts-library-root') < body.index('data-paid-options-root')
    assert "Активация опций" in body
    assert "Доступно для подключения: 3" in body
    assert "Сейчас активных опций" not in body
    assert "Здесь показаны активные платные опции, которые можно будет подключать к аккаунту." in body
    assert "AI / GPT-инструмент" not in body
    assert "ai_gpt_tool" not in body
    assert "Архивная опция" not in body
    assert "Скрытая опция" not in body
    assert "Сервер + ChatGPT Plus" in body
    assert "Chat GPT Plus" in body
    assert "Сервер" in body
    assert _extract_paid_option_titles(body) == [
        "Сервер + ChatGPT Plus",
        "Chat GPT Plus",
        "Сервер",
    ]
    assert "4 000 ₽" in body
    assert body.index("4 000 ₽") < body.index("2 000 ₽")
    assert body.count('type="button" data-paid-option-buy>Купить</button>') == 3
    assert body.count('data-paid-option-card') == 3
    assert 'data-paid-options-list' in body
    assert 'data-paid-options-notice' in body
    assert 'Оплата пока не подключена. Эта кнопка подготовлена для следующего этапа.' in body
    assert '/cabinet/payments' not in body
    assert '/admin/payments' not in body
    assert '/cabinet/paid-options' not in body
    assert "Аккаунты" in body
    assert "Промпты" in body
    assert "Промпты из курса" in body


def test_cabinet_paid_options_block_places_null_price_last_when_present(client, test_settings):
    _create_paid_option(
        test_settings,
        code="cabinet_active_null_price",
        title="Опция без цены",
        description="Опция без указанной цены.",
        price_amount_minor=None,
        currency="RUB",
        default_duration_days=None,
        status="active",
        is_renewable=True,
        sort_order=2,
    )
    _create_paid_option(
        test_settings,
        code="cabinet_active_two_thousand_a",
        title="Опция на 2 000 ₽",
        description="Опция с указанной стоимостью.",
        price_amount_minor=200000,
        currency="RUB",
        default_duration_days=30,
        status="active",
        is_renewable=True,
        sort_order=1,
    )
    _create_paid_option(
        test_settings,
        code="cabinet_active_four_thousand",
        title="Опция на 4 000 ₽",
        description="Активная опция с сроком.",
        price_amount_minor=400000,
        currency="RUB",
        default_duration_days=30,
        status="active",
        is_renewable=True,
        sort_order=0,
    )
    _create_paid_option(
        test_settings,
        code="cabinet_active_two_thousand_b",
        title="Опция на 2 000 ₽, вторая",
        description="Еще одна активная опция.",
        price_amount_minor=200000,
        currency="RUB",
        default_duration_days=30,
        status="active",
        is_renewable=True,
        sort_order=3,
    )

    _login_registered_user(client, test_settings, "cabinet-paid-options-null-price@example.com", "cabinetpaidoptionsnullprice")

    response = client.get("/cabinet")
    assert response.status_code == 200
    body = response.text

    assert "Доступно для подключения: 4" in body
    assert _extract_paid_option_titles(body) == [
        "Опция на 4 000 ₽",
        "Опция на 2 000 ₽",
        "Опция на 2 000 ₽, вторая",
        "Опция без цены",
    ]
    assert body.index("4 000 ₽") < body.index("2 000 ₽")
    assert body.rindex("2 000 ₽") < body.index("Цена не указана")
    assert body.count('type="button" data-paid-option-buy>Купить</button>') == 4
    assert 'Оплата пока не подключена. Эта кнопка подготовлена для следующего этапа.' in body
```


### source/tests/test_cabinet_prompts_library.py

```py
from __future__ import annotations

import html
import re
import sqlite3
from pathlib import Path

from app.auth.service import register_user, verify_email
from app.user_cabinet.prompts_library import load_cabinet_prompts


def _verify_registered_user(client, test_settings, email: str, login: str):
    register_user(
        email=email,
        login=login,
        password="Secret123",
        repeat_password="Secret123",
        settings=test_settings,
    )
    outbox = client.get("/check-email?registered=1")
    assert outbox.status_code == 200


def _extract_token_from_db(test_settings, email: str):
    with sqlite3.connect(test_settings.database_path) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT body_text FROM email_outbox WHERE recipient_email = ? AND template_key = ? ORDER BY id DESC LIMIT 1",
            (email, "email_verification"),
        ).fetchone()
    assert row is not None
    match = re.search(r"/verify-email/([A-Za-z0-9_-]+)", row["body_text"])
    assert match
    return match.group(1)


def _extract_built_in_prompt_markdowns(body_text: str) -> dict[str, str]:
    pattern = re.compile(
        r'<article\s+class="prompt-card prompt-card--built-in prompt-card--collapsed"[^>]*data-prompt-id="(?P<id>[^"]+)".*?'
        r'<div class="prompt-card__body"[^>]*hidden[^>]*>.*?'
        r'<textarea class="textarea prompt-textarea" data-prompt-textarea readonly rows="12">(?P<markdown>.*?)</textarea>',
        re.S,
    )
    return {match.group("id"): html.unescape(match.group("markdown")) for match in pattern.finditer(body_text)}


def test_cabinet_prompt_library_renders_course_prompts_and_custom_prompt_template(client, test_settings):
    _verify_registered_user(client, test_settings, "cabinet-prompts@example.com", "cabinetprompts")
    token = _extract_token_from_db(test_settings, "cabinet-prompts@example.com")
    verify_email(token, settings=test_settings)

    login_response = client.post(
        "/login",
        data={"email_or_login": "cabinet-prompts@example.com", "password": "Secret123"},
        follow_redirects=False,
    )
    assert login_response.status_code == 303

    cabinet_response = client.get("/cabinet")
    assert cabinet_response.status_code == 200
    assert cabinet_response.text.index('data-local-accounts-root') < cabinet_response.text.index('data-prompts-library-root')
    assert "Промпты" in cabinet_response.text
    assert "Промпты из курса" in cabinet_response.text
    assert cabinet_response.text.count('class="prompt-card prompt-card--built-in prompt-card--collapsed"') == 4
    assert "Мои промпты" in cabinet_response.text
    assert "Добавить промпт" in cabinet_response.text
    assert "Редактировать" in cabinet_response.text
    assert "Сохранить" in cabinet_response.text
    assert "Скопировать" in cabinet_response.text
    assert "Скачать .md" in cabinet_response.text
    assert "Сбросить к версии курса" in cabinet_response.text
    assert "Удалить" in cabinet_response.text
    assert "data-prompts-custom-template" in cabinet_response.text
    assert 'class="prompt-card prompt-card--custom prompt-card--collapsed"' in cabinet_response.text
    assert 'data-prompt-custom data-prompt-expanded="false"' in cabinet_response.text
    assert 'aria-controls="prompt-body-custom"' in cabinet_response.text
    assert "Файл: custom-prompt.md" in cabinet_response.text
    assert "openscript:cabinet:prompts-library:v1" in client.get("/static/cabinet-prompts-library.js").text
    assert cabinet_response.text.count('aria-expanded="false"') >= 4
    assert cabinet_response.text.count("data-prompt-body") >= 5
    assert cabinet_response.text.count("Развернуть") >= 5

    collapsed_cards = re.findall(
        r'<article\s+class="prompt-card prompt-card--built-in prompt-card--collapsed"[^>]*>.*?</article>',
        cabinet_response.text,
        re.S,
    )
    assert len(collapsed_cards) == 4
    for card_html in collapsed_cards:
        assert 'data-prompt-expanded="false"' in card_html
        assert "prompt-card__filename" in card_html
        assert "data-prompt-body" in card_html
        assert "hidden" in card_html
        assert 'data-prompt-toggle' in card_html
        assert 'aria-expanded="false"' in card_html
        assert "Развернуть" in card_html

    prompts = load_cabinet_prompts()
    assert len(prompts) == 4
    assert [prompt["lesson_number"] for prompt in prompts] == [6, 7, 8, 8]
    assert [prompt["owner_label"] for prompt in prompts] == ["Урок 6", "Урок 7", "Урок 8", "Урок 8"]
    assert [prompt["filename"] for prompt in prompts] == [
        "start_project_documentation_prompt.md",
        "prefix_extension_for_chatgpt_prompt.md",
        "project_docs_update_prompt.md",
        "new_project_dialogue_prompt.md",
    ]
    assert [prompt["id"] for prompt in prompts] == [
        "lesson-6-start-project-documentation-prompt",
        "lesson-7-prefix-extension-for-chatgpt-prompt",
        "lesson-8-project-docs-update-prompt",
        "lesson-8-new-project-dialogue-prompt",
    ]

    expected_source = {
        prompt["id"]: prompt
        for prompt in prompts
    }
    rendered_markdowns = _extract_built_in_prompt_markdowns(cabinet_response.text)
    assert set(rendered_markdowns) == set(expected_source)
    assert "Старт проекта с разработки документации" in cabinet_response.text
    assert "Prompt для создания расширения" in cabinet_response.text
    assert "Prompt для обновления документов проекта" in cabinet_response.text
    assert "Prompt для нового диалога по проекту" in cabinet_response.text
    assert "start_project_documentation_prompt.md" in cabinet_response.text
    assert "prefix_extension_for_chatgpt_prompt.md" in cabinet_response.text
    assert "project_docs_update_prompt.md" in cabinet_response.text
    assert "new_project_dialogue_prompt.md" in cabinet_response.text

    for prompt in prompts:
        rendered = rendered_markdowns[prompt["id"]]
        assert rendered == prompt["markdown"]
        assert prompt["title"] in cabinet_response.text
        assert prompt["owner_label"] in cabinet_response.text
        assert prompt["filename"] in cabinet_response.text

    assert "Ты — ChatGPT, ведущий технический специалист проекта." in cabinet_response.text
    assert "Сначала ответь только одной фразой:" in cabinet_response.text
    assert "Опишите свою идею проекта простыми словами" in cabinet_response.text
    assert "Мне нужно сделать простое browser-расширение для ChatGPT." in cabinet_response.text
    assert "Сделай расширение для Chrome и Edge." in cabinet_response.text
    assert "https://chatgpt.com/*" in cabinet_response.text
    assert "Мне нужно обновить документы проекта после текущего этапа работы." in cabinet_response.text
    assert "Public docs repo: [ССЫЛКА НА ПУБЛИЧНЫЙ РЕПОЗИТОРИЙ ДОКУМЕНТОВ]" in cabinet_response.text
    assert "Prompt для обновления документов проекта" in cabinet_response.text
    assert "Начни работу по проекту строго по документам проекта." in cabinet_response.text
    assert "Не продолжай по памяти." in cabinet_response.text
    assert "Prompt для нового диалога по проекту" in cabinet_response.text

    course_script = Path(
        "/opt/ai-starter-community/source/app/materials/course_content/drafts/dair_smoke_20260529/script.js"
    ).read_text(encoding="utf-8")
    assert "starterPromptMarkdown:" in course_script
    assert 'starterPromptFilename: "start_project_documentation_prompt.md"' in course_script
    assert 'starterPromptLabel: "Prompt для создания расширения"' in course_script
    assert 'label: "Prompt для обновления документов"' in course_script
    assert 'label: "Prompt для нового диалога"' in course_script
    assert 'id: "lesson-8-project-docs-update-prompt"' in course_script
    assert 'id: "lesson-8-new-project-dialogue-prompt"' in course_script
    routes_text = Path("/opt/ai-starter-community/source/app/user_cabinet/routes.py").read_text(encoding="utf-8")
    assert '"/cabinet/prompts"' not in routes_text
    assert "openscript:cabinet:local-accounts:v1" in client.get("/static/cabinet-local-accounts.js").text
    assert "Личный кабинет" in cabinet_response.text
```

```diff
(no diff)
```


### source/tests/test_account_blocks_cabinet_ui.py

```py
from __future__ import annotations

import re
import sqlite3
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode
from unittest.mock import patch

from app.account_blocks.schemas import AccountBlockCreateInput
from app.account_blocks.service import activate_account_block, create_account_block
from app.auth.service import authenticate_user, create_session, register_user, verify_email


def _connect(settings):
    conn = sqlite3.connect(str(settings.database_path))
    conn.row_factory = sqlite3.Row
    return conn


def _extract_verify_token(settings, email: str) -> str:
    with _connect(settings) as conn:
        row = conn.execute(
            "SELECT body_text FROM email_outbox WHERE recipient_email = ? AND template_key = ? ORDER BY id DESC LIMIT 1",
            (email, "email_verification"),
        ).fetchone()
    assert row is not None
    match = re.search(r"/verify-email/([A-Za-z0-9_-]+)", row["body_text"])
    assert match
    return match.group(1)


def _create_verified_user(test_settings, email: str, login: str, role: str = "user"):
    register_user(
        email=email,
        login=login,
        password="Secret123",
        repeat_password="Secret123",
        settings=test_settings,
    )
    verify_email(_extract_verify_token(test_settings, email), settings=test_settings)
    if role != "user":
        with _connect(test_settings) as conn:
            conn.execute("UPDATE users SET role = ? WHERE email = ?", (role, email))
            conn.commit()
    return authenticate_user(email, "Secret123", settings=test_settings)


def _login_as(client, test_settings, email: str):
    user = authenticate_user(email, "Secret123", settings=test_settings)
    client.cookies.set(test_settings.session_cookie_name, create_session(user.id, settings=test_settings))
    return user


def _grant_materials_access(test_settings, email: str) -> None:
    with _connect(test_settings) as conn:
        conn.execute(
            "UPDATE users SET materials_access_granted_at = CURRENT_TIMESTAMP WHERE email = ?",
            (email,),
        )
        conn.commit()


def _extract_accounts_section(body_text: str) -> str:
    start_marker = '<section id="accounts" class="card stack accounts-card'
    start = body_text.find(start_marker)
    assert start != -1
    vpn_marker = '<section class="card stack cabinet-vpn-section" data-cabinet-vpn-section>'
    end = body_text.find(vpn_marker, start)
    if end == -1:
        end_marker = '<section class="card stack prompts-library-card" data-prompts-library-root>'
        end = body_text.find(end_marker, start)
    assert end != -1
    return body_text[start:end]


def _extract_builder_shell(accounts_section: str) -> str:
    start_marker = '<div class="accounts-builder-shell">'
    end_marker = '<div class="accounts-grid">'
    start = accounts_section.find(start_marker)
    end = accounts_section.find(end_marker, start)
    assert start != -1
    if end == -1:
        end = len(accounts_section)
    return accounts_section[start:end]


def _extract_first_edit_form(accounts_section: str) -> str:
    start_marker = '<form class="account-card__edit-form"'
    start = accounts_section.find(start_marker)
    assert start != -1
    end = accounts_section.find("</form>", start)
    assert end != -1
    return accounts_section[start:end]


def _extract_vpn_section(accounts_section: str) -> str:
    start_marker = '<section class="card stack cabinet-vpn-section" data-cabinet-vpn-section>'
    start = accounts_section.find(start_marker)
    assert start != -1
    end = accounts_section.find("</section>", start)
    assert end != -1
    return accounts_section[start:end]


def test_user_sees_compact_server_backed_account_blocks_and_copy_only_controls(client, test_settings):
    admin = _create_verified_user(test_settings, "cab-ui-admin@example.com", "cabuiadmin", role="admin")
    owner = _create_verified_user(test_settings, "cab-ui-owner@example.com", "cabuiowner")
    _grant_materials_access(test_settings, owner.email)

    active_block = create_account_block(
        actor=admin,
        data=AccountBlockCreateInput(
            owner_user_id=owner.id,
            type="chatgpt",
            login="owner-chat-login",
            password_secret="owner-chat-password",
        ),
        settings=test_settings,
    )
    create_account_block(
        actor=admin,
        data=AccountBlockCreateInput(
            owner_user_id=owner.id,
            type="mail",
            login="owner-mail-login",
            password_secret="owner-mail-password",
        ),
        settings=test_settings,
    )
    vpn_block = create_account_block(
        actor=admin,
        data=AccountBlockCreateInput(
            owner_user_id=owner.id,
            type="vpn",
        ),
        settings=test_settings,
    )

    fixed_now = datetime(2026, 6, 8, 12, 0, 0, tzinfo=timezone.utc)
    with patch("app.account_blocks.service.utc_now", return_value=fixed_now):
        activate_account_block(actor=admin, block_id=active_block.id, settings=test_settings)
    with patch("app.account_blocks.service.utc_now", return_value=fixed_now):
        activate_account_block(actor=admin, block_id=vpn_block.id, settings=test_settings)

    _login_as(client, test_settings, owner.email)
    with patch("app.account_blocks.service.utc_now", return_value=fixed_now):
        response = client.get("/cabinet")

    assert response.status_code == 200
    assert "/static/cabinet-local-accounts.js" in response.text
    assert "data-account-blocks-source=\"server\"" in response.text
    assert 'id="accounts"' in response.text

    accounts_section = _extract_accounts_section(response.text)
    assert '<h2 class="section-title">Аккаунты</h2>' in accounts_section
    assert "Тут появятся блоки с данными для авторизации после того, как администратор активирует опции. Обычно это занимает не более суток после оплаты." not in accounts_section
    assert "Данные хранятся на сервере и доступны после входа в кабинет с любого устройства." not in accounts_section
    assert "Вы видите только свои блоки" not in accounts_section
    assert "Администратор или модератор добавит их позже" not in accounts_section
    assert "Добавить блок" not in accounts_section
    assert "Редактировать" not in accounts_section
    assert "Удалить" not in accounts_section
    assert "Активировать" not in accounts_section
    assert 'name="title"' not in accounts_section
    assert 'name="email"' not in accounts_section
    assert "data-account-card-edit-form" not in accounts_section
    assert "Скопировать" in accounts_section
    assert '<span class="account-card__type-badge">GPT</span>' in accounts_section
    assert '<span class="account-card__status-badge account-card__status-badge--active">Активно</span>' in accounts_section
    assert "account-card__title" not in accounts_section
    assert "ChatGPT" not in accounts_section
    assert "Почта" not in accounts_section
    assert "Осталось 60 дней" in accounts_section
    assert "Не активирован" not in accounts_section
    assert "Срок завершён" not in accounts_section
    assert "Осталось после активации" not in accounts_section
    assert "Владелец:" not in accounts_section
    assert "account-owner-group__title" not in accounts_section
    assert "account-owner-group__meta" not in accounts_section
    assert "account-card__owner-line" not in accounts_section
    assert "owner-mail-login" not in accounts_section
    assert "owner-mail-password" not in accounts_section
    assert "Срок действия" not in accounts_section
    assert "из 60" not in accounts_section
    assert "После активации блок работает 60 дней" not in accounts_section
    assert 'data-account-block-form="create"' not in accounts_section
    assert "Платная опция" not in accounts_section
    assert "Без привязки" not in accounts_section
    assert "Продлить активацию" not in accounts_section
    assert "ВПН" not in accounts_section
    assert "account-card--vpn" not in accounts_section
    assert "account-card__vpn" not in accounts_section
    assert "account-vpn-panel" not in accounts_section
    assert "cabinet-vpn-section" not in accounts_section
    assert "amnezia-vpn-guide.mp4" not in accounts_section
    assert "Открыть сайт Amnezia VPN" not in accounts_section
    assert '<input class="input account-field__input" data-account-field="login"' in accounts_section
    assert '<input class="input account-field__input" data-account-field="password" type="password"' in accounts_section
    assert '<div class="account-field__actions">' in accounts_section
    assert '<div class="account-field__actions account-field__actions--split">' in accounts_section
    assert accounts_section.count("data-account-copy") == 2
    assert accounts_section.count("data-account-password-toggle") == 1
    assert accounts_section.count('account-field__actions--split') == 1
    assert re.search(r'<button[^>]*data-account-password-toggle[^>]*>\s*Показать\s*</button>', accounts_section)

    assert "Просмотрите ролик. IP сервера возьмите из блока «Сервер»." not in response.text

    vpn_section = _extract_vpn_section(response.text)
    assert '<section class="card stack cabinet-vpn-section" data-cabinet-vpn-section>' in vpn_section
    assert '<details class="cabinet-vpn-disclosure">' in vpn_section
    assert '<summary class="cabinet-vpn-summary">' in vpn_section
    assert '<h2 class="section-title cabinet-vpn-summary__title">ВПН</h2>' in vpn_section
    assert '<p class="form-help cabinet-vpn-summary__hint">Видеоинструкция и ссылка Amnezia VPN</p>' in vpn_section
    assert '<span class="cabinet-vpn-summary__title">' not in vpn_section
    assert "Видеоинструкция и ссылка Amnezia VPN" in vpn_section
    assert 'После просмотра откройте сайт Amnezia VPN и используйте IP из блока «<a href="#accounts">Сервер</a>».' in vpn_section
    assert "cabinet-vpn-note" in vpn_section
    assert 'href="#accounts">Сервер</a>' in vpn_section
    assert "Видео взято с канала" not in vpn_section
    assert 'href="https://www.youtube.com/@TechTalk_NotDead"' not in vpn_section
    assert "Tech Talk" not in vpn_section
    assert "Благодарим канал" not in vpn_section
    assert "Лайк и подписка приветствуются" not in vpn_section
    assert "Открыть сайт Amnezia VPN" in vpn_section
    assert "account-card__type-badge" not in vpn_section
    assert "account-card__status-badge" not in vpn_section
    assert "Осталось" not in vpn_section
    assert "АКТИВНО" not in vpn_section
    assert "amnezia-vpn-guide.mp4" in vpn_section
    assert "<video" in vpn_section


def test_user_sees_three_active_account_cards_with_consistent_header_labels(client, test_settings):
    admin = _create_verified_user(test_settings, "cab-ui-grid-admin@example.com", "cabuigridadmin", role="admin")
    owner = _create_verified_user(test_settings, "cab-ui-grid-owner@example.com", "cabuigridowner")
    _grant_materials_access(test_settings, owner.email)

    fixed_now = datetime(2026, 6, 8, 12, 0, 0, tzinfo=timezone.utc)
    for block_type, login, password in (
        ("chatgpt", "grid-chat-login", "grid-chat-password"),
        ("server", "grid-server-login", "grid-server-password"),
        ("mail", "grid-mail-login", "grid-mail-password"),
    ):
        block = create_account_block(
            actor=admin,
            data=AccountBlockCreateInput(
                owner_user_id=owner.id,
                type=block_type,
                login=login,
                password_secret=password,
            ),
            settings=test_settings,
        )
        with patch("app.account_blocks.service.utc_now", return_value=fixed_now):
            activate_account_block(actor=admin, block_id=block.id, settings=test_settings)

    _login_as(client, test_settings, owner.email)
    with patch("app.account_blocks.service.utc_now", return_value=fixed_now):
        response = client.get("/cabinet")

    assert response.status_code == 200
    accounts_section = _extract_accounts_section(response.text)
    assert accounts_section.count('<article class="account-card">') == 3
    assert accounts_section.count('account-card__status-badge--active">Активно</span>') == 3
    assert '<span class="account-card__type-badge">GPT</span>' in accounts_section
    assert '<span class="account-card__type-badge">Сервер</span>' in accounts_section
    assert '<span class="account-card__type-badge">Почта</span>' in accounts_section
    assert "ChatGPT" not in accounts_section
    assert "account-card__title" not in accounts_section
    assert accounts_section.count('input class="input account-field__input" data-account-field="login"') == 3
    assert accounts_section.count('input class="input account-field__input" data-account-field="password" type="password"') == 3
    assert accounts_section.count("data-account-copy") == 6
    assert accounts_section.count("data-account-password-toggle") == 3
    assert accounts_section.count('account-field__actions--split') == 3
    assert accounts_section.count('aria-label="Показать пароль"') == 3
    assert len(re.findall(r'<button[^>]*data-account-password-toggle[^>]*>\s*Показать\s*</button>', accounts_section)) == 3


def test_user_with_no_active_account_blocks_sees_new_empty_state(client, test_settings):
    admin = _create_verified_user(test_settings, "cab-ui-empty-admin@example.com", "cabuiemptyadmin", role="admin")
    owner = _create_verified_user(test_settings, "cab-ui-empty-owner@example.com", "cabuiemptyowner")
    _grant_materials_access(test_settings, owner.email)

    create_account_block(
        actor=admin,
        data=AccountBlockCreateInput(
            owner_user_id=owner.id,
            type="mail",
            login="inactive-mail-login",
            password_secret="inactive-mail-password",
        ),
        settings=test_settings,
    )

    _login_as(client, test_settings, owner.email)
    response = client.get("/cabinet")

    assert response.status_code == 200
    accounts_section = _extract_accounts_section(response.text)
    assert '<h2 class="section-title">Аккаунты</h2>' in accounts_section
    assert "Тут появятся блоки с данными для авторизации после того, как администратор активирует опции. Обычно это занимает не более суток после оплаты." in accounts_section
    assert "Данные хранятся на сервере" not in accounts_section
    assert "Вы видите только свои блоки" not in accounts_section
    assert "Администратор или модератор добавит их позже" not in accounts_section
    assert "Пока нет ни одного блока" not in accounts_section
    assert "У этого пользователя пока нет блоков" not in accounts_section
    assert "Найдите пользователя по email" not in accounts_section
    assert "Скопировать" not in accounts_section
    assert "account-card__title" not in accounts_section
    assert "inactive-mail-login" not in accounts_section
    assert "Неактивно" not in accounts_section
    assert "Активно" not in accounts_section


def test_moderator_can_search_user_by_email_and_manage_selected_user_blocks(client, test_settings):
    admin = _create_verified_user(test_settings, "cab-ui-admin-2@example.com", "cabuiadmin2", role="admin")
    moderator = _create_verified_user(test_settings, "cab-ui-moderator@example.com", "cabuimoderator", role="moderator")
    owner_a = _create_verified_user(test_settings, "cab-ui-owner-a@example.com", "cabuiownera")
    _login_as(client, test_settings, moderator.email)

    cabinet_response = client.get(f"/cabinet?account_blocks_user_email={owner_a.email}")
    assert cabinet_response.status_code == 200
    assert '<h2 class="section-title">Аккаунты</h2>' in cabinet_response.text
    assert "Администратор и модератор выбирают пользователя по email и управляют только его блоками." not in cabinet_response.text
    assert "Email пользователя" in cabinet_response.text
    assert owner_a.email in cabinet_response.text
    accounts_section = _extract_accounts_section(cabinet_response.text)
    builder_shell = _extract_builder_shell(accounts_section)
    assert "Добавить блок" in builder_shell
    assert 'name="duration_days"' in builder_shell
    assert 'data-account-block-duration-input' in builder_shell
    assert 'name="duration_days" type="number" min="1" value="30"' in builder_shell
    assert 'name="owner_user_id"' not in builder_shell
    assert 'name="title"' not in builder_shell
    assert f'action="/cabinet/account-blocks?{urlencode({"account_blocks_user_email": owner_a.email})}' in builder_shell
    with _connect(test_settings) as conn:
        assert (
            conn.execute(
                "SELECT COUNT(*) AS c FROM email_outbox WHERE template_key = ?",
                ("account_block_activation",),
            ).fetchone()["c"]
            == 0
        )

    create_response = client.post(
        f"/cabinet/account-blocks?{urlencode({'account_blocks_user_email': owner_a.email})}",
        data={
            "type": "server",
            "duration_days": "",
            "login": "mod-block-login",
            "password_secret": "mod-block-password",
        },
        follow_redirects=False,
    )
    assert create_response.status_code == 303
    assert create_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'created', 'account_blocks_user_email': owner_a.email})}"

    with _connect(test_settings) as conn:
        row = conn.execute("SELECT * FROM account_blocks WHERE login = ?", ("mod-block-login",)).fetchone()
    assert row is not None
    block_id = int(row["id"])
    assert int(row["owner_user_id"]) == owner_a.id
    assert row["type"] == "server"
    assert row["title"] == "Сервер"
    assert row["email"] is None
    assert int(row["duration_days"]) == 30

    update_response = client.post(
        f"/cabinet/account-blocks/{block_id}",
        data={
            "type": "mail",
            "title": "Should be ignored",
            "login": "updated-login",
            "password_secret": "updated-password",
            "email": "updated@example.com",
        },
        follow_redirects=False,
    )
    assert update_response.status_code == 303
    assert update_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'updated', 'account_blocks_user_email': owner_a.email})}"
    with _connect(test_settings) as conn:
        assert (
            conn.execute(
                "SELECT COUNT(*) AS c FROM email_outbox WHERE template_key = ?",
                ("account_block_activation",),
            ).fetchone()["c"]
            == 0
        )

    activation_now = datetime(2026, 6, 8, 12, 0, 0, tzinfo=timezone.utc)
    with patch("app.account_blocks.service.utc_now", return_value=activation_now):
        activate_response = client.post(
            f"/cabinet/account-blocks/{block_id}/activate?{urlencode({'account_blocks_user_email': owner_a.email})}",
            data={
                "duration_days": "",
            },
            follow_redirects=False,
        )
    assert activate_response.status_code == 303
    assert activate_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'activated_email_sent', 'account_blocks_user_email': owner_a.email})}"

    with _connect(test_settings) as conn:
        updated_row = conn.execute("SELECT * FROM account_blocks WHERE id = ?", (block_id,)).fetchone()
    assert updated_row is not None
    assert int(updated_row["owner_user_id"]) == owner_a.id
    assert updated_row["type"] == "server"
    assert updated_row["title"] == "Сервер"
    assert updated_row["login"] == "updated-login"
    assert updated_row["password_secret"] == "updated-password"
    assert updated_row["email"] is None
    assert updated_row["status"] == "active"
    assert updated_row["activated_at"] == activation_now.isoformat()
    assert updated_row["expires_at"] == (activation_now + timedelta(days=30)).isoformat()

    with _connect(test_settings) as conn:
        email_row = conn.execute(
            """
            SELECT *
            FROM email_outbox
            WHERE recipient_email = ? AND template_key = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (owner_a.email, "account_block_activation"),
        ).fetchone()
    assert email_row is not None
    assert email_row["subject"] == "Активирована опция OpenScript"
    assert "updated-login" not in email_row["body_text"]
    assert "updated-password" not in email_row["body_text"]

    renewal_now = activation_now + timedelta(days=22)
    with patch("app.account_blocks.service.utc_now", return_value=renewal_now):
        active_page = client.get(f"/cabinet?{urlencode({'account_blocks_user_email': owner_a.email})}")
    accounts_section = _extract_accounts_section(active_page.text)
    assert "Редактировать" in accounts_section
    assert "Удалить" in accounts_section
    assert "Активировать" in accounts_section
    assert "Продлить активацию" in accounts_section
    assert "Сервер" in accounts_section
    assert "account-card__owner-line" in accounts_section
    assert "Пользователь:" in accounts_section
    assert "Осталось 8 дней" in accounts_section
    assert f'/cabinet/account-blocks/{block_id}/delete?{urlencode({"account_blocks_user_email": owner_a.email})}' in accounts_section
    assert f'/cabinet/account-blocks/{block_id}/activate?{urlencode({"account_blocks_user_email": owner_a.email})}' in accounts_section
    assert f'/cabinet/account-blocks/{block_id}/renew?{urlencode({"account_blocks_user_email": owner_a.email})}' in accounts_section
    assert 'name="duration_days"' in accounts_section
    edit_form = _extract_first_edit_form(accounts_section)
    assert 'name="login"' in edit_form
    assert 'name="password_secret"' in edit_form
    assert "data-account-card-edit-form" in edit_form
    assert 'hidden' in edit_form
    assert "Платная опция" not in builder_shell
    assert "Без привязки" not in builder_shell

    with patch("app.account_blocks.service.utc_now", return_value=renewal_now):
        renew_response = client.post(
            f"/cabinet/account-blocks/{block_id}/renew?{urlencode({'account_blocks_user_email': owner_a.email})}",
            data={
                "duration_days": "30",
            },
            follow_redirects=False,
        )
    assert renew_response.status_code == 303
    assert renew_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'renewed', 'account_blocks_user_email': owner_a.email})}"

    with _connect(test_settings) as conn:
        renewed_row = conn.execute("SELECT * FROM account_blocks WHERE id = ?", (block_id,)).fetchone()
    assert renewed_row is not None
    assert renewed_row["expires_at"] == (renewal_now + timedelta(days=38)).isoformat()

    delete_response = client.post(
        f"/cabinet/account-blocks/{block_id}/delete?{urlencode({'account_blocks_user_email': owner_a.email})}",
        follow_redirects=False,
    )
    assert delete_response.status_code == 303
    assert delete_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'deleted', 'account_blocks_user_email': owner_a.email})}"

    with _connect(test_settings) as conn:
        deleted_row = conn.execute("SELECT 1 FROM account_blocks WHERE id = ?", (block_id,)).fetchone()
    assert deleted_row is None
    with _connect(test_settings) as conn:
        email_row = conn.execute(
            """
            SELECT *
            FROM email_outbox
            WHERE recipient_email = ? AND template_key = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (owner_a.email, "account_block_activation"),
        ).fetchone()
    assert email_row is not None
    assert email_row["subject"] == "Активирована опция OpenScript"
    assert "У вас активирована опция: Сервер." in email_row["body_text"]
    assert "https://openscript.ru/" in email_row["body_text"]
    assert "https://openscript.ru/cabinet" in email_row["body_text"]
    assert "updated-login" not in email_row["body_text"]
    assert "updated-password" not in email_row["body_text"]


def test_moderator_can_manage_account_blocks_but_cannot_access_admin_dashboard(client, test_settings):
    moderator = _create_verified_user(test_settings, "cab-ui-moderator@example.com", "cabuimoderator", role="moderator")
    owner = _create_verified_user(test_settings, "cab-ui-moderator-owner@example.com", "cabuimoderatorowner")
    _login_as(client, test_settings, moderator.email)

    admin_response = client.get("/admin")
    assert admin_response.status_code == 403
    admin_blocks_response = client.get("/admin/account-blocks?account_blocks_user_email=test@example.com")
    assert admin_blocks_response.status_code == 403

    create_response = client.post(
        f"/cabinet/account-blocks?{urlencode({'account_blocks_user_email': owner.email})}",
        data={
            "type": "chatgpt",
            "login": "moderator-login",
            "password_secret": "moderator-password",
        },
        follow_redirects=False,
    )
    assert create_response.status_code == 303
    assert create_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'created', 'account_blocks_user_email': owner.email})}"

    with _connect(test_settings) as conn:
        row = conn.execute("SELECT * FROM account_blocks WHERE login = ?", ("moderator-login",)).fetchone()
    assert row is not None
    block_id = int(row["id"])

    update_response = client.post(
        f"/cabinet/account-blocks/{block_id}",
        data={
            "type": "server",
            "title": "Ignored title",
            "login": "moderator-login-updated",
            "password_secret": "moderator-password-updated",
            "email": "ignored@example.com",
        },
        follow_redirects=False,
    )
    assert update_response.status_code == 303
    assert update_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'updated', 'account_blocks_user_email': owner.email})}"

    activation_now = datetime(2026, 6, 8, 12, 0, 0, tzinfo=timezone.utc)
    with patch("app.account_blocks.service.utc_now", return_value=activation_now):
        activate_response = client.post(
            f"/cabinet/account-blocks/{block_id}/activate?{urlencode({'account_blocks_user_email': owner.email})}",
            data={"duration_days": "45"},
            follow_redirects=False,
        )
    assert activate_response.status_code == 303
    assert activate_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'activated_email_sent', 'account_blocks_user_email': owner.email})}"

    with _connect(test_settings) as conn:
        activated_row = conn.execute("SELECT * FROM account_blocks WHERE id = ?", (block_id,)).fetchone()
    assert activated_row is not None
    assert activated_row["expires_at"] == (activation_now + timedelta(days=45)).isoformat()

    with patch("app.account_blocks.service.utc_now", return_value=activation_now + timedelta(days=1)):
        active_page = client.get(f"/cabinet?{urlencode({'account_blocks_user_email': owner.email})}")
    accounts_section = _extract_accounts_section(active_page.text)
    assert "Продлить активацию" in accounts_section
    assert "Осталось 44 дня" in accounts_section

    renew_response = client.post(
        f"/cabinet/account-blocks/{block_id}/renew?{urlencode({'account_blocks_user_email': owner.email})}",
        data={"duration_days": "30"},
        follow_redirects=False,
    )
    assert renew_response.status_code == 303
    assert renew_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'renewed', 'account_blocks_user_email': owner.email})}"

    delete_response = client.post(
        f"/cabinet/account-blocks/{block_id}/delete?{urlencode({'account_blocks_user_email': owner.email})}",
        follow_redirects=False,
    )
    assert delete_response.status_code == 303
    assert delete_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'deleted', 'account_blocks_user_email': owner.email})}"


def test_regular_user_cannot_post_account_block_management_actions(client, test_settings):
    admin = _create_verified_user(test_settings, "cab-ui-deny-admin@example.com", "cabuidenyadmin", role="admin")
    owner = _create_verified_user(test_settings, "cab-ui-deny-owner@example.com", "cabuidenyowner")
    block = create_account_block(
        actor=admin,
        data=AccountBlockCreateInput(
            owner_user_id=owner.id,
            type="server",
            login="denied-login",
            password_secret="denied-password",
        ),
        settings=test_settings,
    )

    _login_as(client, test_settings, owner.email)

    create_response = client.post(
        "/cabinet/account-blocks",
        data={
            "type": "chatgpt",
            "login": "nope",
            "password_secret": "nope",
        },
    )
    assert create_response.status_code == 403

    update_response = client.post(
        f"/cabinet/account-blocks/{block.id}",
        data={
            "type": "server",
            "title": "Should not update",
            "login": "nope",
            "password_secret": "nope",
            "email": "nope@example.com",
        },
    )
    assert update_response.status_code == 403

    delete_response = client.post(f"/cabinet/account-blocks/{block.id}/delete")
    assert delete_response.status_code == 403

    activate_response = client.post(f"/cabinet/account-blocks/{block.id}/activate")
    assert activate_response.status_code == 403
    renew_response = client.post(f"/cabinet/account-blocks/{block.id}/renew")
    assert renew_response.status_code == 403


def test_expired_account_block_shows_finished_day_counter_without_active_label(client, test_settings):
    admin = _create_verified_user(test_settings, "cab-ui-expire-admin@example.com", "cabuiexpireadmin", role="admin")
    owner = _create_verified_user(test_settings, "cab-ui-expire-owner@example.com", "cabuiexpireowner")
    _grant_materials_access(test_settings, owner.email)
    block = create_account_block(
        actor=admin,
        data=AccountBlockCreateInput(
            owner_user_id=owner.id,
            type="mail",
            login="expire-login",
            password_secret="expire-password",
        ),
        settings=test_settings,
    )

    activation_now = datetime(2026, 6, 8, 12, 0, 0, tzinfo=timezone.utc)
    expired_now = activation_now + timedelta(days=61)
    with patch("app.account_blocks.service.utc_now", return_value=activation_now):
        activate_account_block(actor=admin, block_id=block.id, settings=test_settings)

    _login_as(client, test_settings, owner.email)
    with patch("app.account_blocks.service.utc_now", return_value=expired_now):
        response = client.get("/cabinet")

    accounts_section = _extract_accounts_section(response.text)
    assert "Тут появятся блоки с данными для авторизации после того, как администратор активирует опции. Обычно это занимает не более суток после оплаты." in accounts_section
    assert "Почта" not in accounts_section
    assert "Срок завершён" not in accounts_section
    assert "Осталось" not in accounts_section
    assert "Активно" not in accounts_section
    assert "Активен:" not in accounts_section
    assert "Осталось после активации" not in accounts_section
    assert "Срок действия" not in accounts_section
    assert "из 60" not in accounts_section
    assert "60 дней" not in accounts_section
    assert "Продлить активацию" not in accounts_section
```

```diff
(no diff)
```


### source/app/admin/templates/account_blocks.html

```html
{% extends "base.html" %}

{% block content %}
  <section class="card stack">
    <div class="stack">
      <p class="muted">Административный раздел</p>
      <h1 class="section-title">Блоки аккаунтов</h1>
      <p>Логин администратора: <strong>{{ admin_login }}</strong></p>
      <p>Электронная почта: {{ admin_email }}</p>
      <p class="form-help">Выберите пользователя по email, посмотрите его текущие блоки и при необходимости добавьте, активируйте или продлите доступ.</p>
    </div>
  </section>

  <section id="accounts" class="card stack accounts-card" data-local-accounts-root data-account-blocks-source="server">
    <div class="accounts-header">
      <div class="stack accounts-intro">
        <h2 class="section-title accounts-title">Аккаунты</h2>
        <p class="form-help">Администратор видит только безопасные поля и управляет выбранным пользователем по email.</p>
      </div>

      <form class="accounts-search stack" method="get" action="/admin/account-blocks">
        <label class="form-row accounts-field">
          <span>Email пользователя</span>
          <input
            class="input"
            name="account_blocks_user_email"
            type="email"
            list="admin-account-block-user-email-list"
            value="{{ account_block_selected_user_email }}"
            placeholder="user@example.com"
            autocomplete="email"
            required
          >
        </label>
        <datalist id="admin-account-block-user-email-list">
          {% for option in account_block_owner_options %}
            <option value="{{ option.email }}">{{ option.display_label }}</option>
          {% endfor %}
        </datalist>
        <div class="actions">
          <button class="button button-primary" type="submit">Найти пользователя</button>
        </div>
      </form>
    </div>

    <p class="accounts-notice" data-account-blocks-notice aria-live="polite" role="status">{{ account_block_notice or "" }}</p>

    {% if account_block_selected_user_summary %}
      <section class="card stack accounts-selected-user">
        <h3 class="section-title">Выбранный пользователь</h3>
        <p class="form-help">Email: <strong>{{ account_block_selected_user_summary.email }}</strong></p>
        <p class="form-help">Логин: <strong>{{ account_block_selected_user_summary.login }}</strong></p>
        <p class="form-help">Роль: <strong>{{ account_block_selected_user_summary.role_label }}</strong></p>
      </section>
    {% else %}
      <p class="form-help accounts-empty">Введите email пользователя, чтобы загрузить его блоки.</p>
    {% endif %}

    {% if account_block_selected_user_summary %}
      <div class="accounts-builder-shell">
        <form
          class="accounts-builder accounts-builder--server"
          method="post"
          action="/admin/account-blocks{{ account_block_query_string }}"
          data-account-block-form="create"
        >
          <label class="form-row accounts-type-field">
            <span>Тип блока</span>
            <select class="select" name="type" required>
              {% for option in account_block_type_options %}
                <option value="{{ option.value }}" {% if option.value == 'chatgpt' %}selected{% endif %}>{{ option.label }}</option>
              {% endfor %}
            </select>
          </label>
          <label class="form-row accounts-field">
            <span>Срок, дней</span>
            <input class="input" name="duration_days" type="number" min="1" value="{{ account_block_create_default_duration_days }}" data-account-block-duration-input>
          </label>
          <label class="form-row accounts-field">
            <span>Логин</span>
            <input class="input" name="login" type="text" placeholder="Логин" autocomplete="off">
          </label>
          <label class="form-row accounts-field">
            <span>Пароль</span>
            <input class="input" name="password_secret" type="text" placeholder="Пароль" autocomplete="off">
          </label>
          <button class="button button-primary" type="submit">Добавить блок</button>
        </form>
      </div>
    {% endif %}

    {% if account_block_blocks %}
      <div class="accounts-grid">
        {% for block in account_block_blocks %}
          <article class="account-card">
            <header class="account-card__header">
              <div class="stack account-card__headline">
                <div class="account-card__title-row">
                  <h3 class="account-card__title">{{ block.title }}</h3>
                  <div class="account-card__badges">
                    <span class="account-card__type-badge">{{ block.type_label }}</span>
                    {% if block.is_active %}
                      <span class="account-card__status-badge account-card__status-badge--active">Активно</span>
                    {% elif block.is_expired %}
                      <span class="account-card__status-badge account-card__status-badge--expired">{{ block.status_label }}</span>
                    {% else %}
                      <span class="account-card__status-badge account-card__status-badge--inactive">{{ block.status_label }}</span>
                    {% endif %}
                  </div>
                </div>
                <p class="form-help account-card__owner-line">Пользователь: {{ account_block_selected_user_summary.email }} · {{ account_block_selected_user_summary.login }}</p>
              </div>
            </header>

            <div class="account-card__body">
              <div class="account-card__readonly" data-account-card-view>
                <label class="account-field">
                  <span>Логин</span>
                  <div class="account-field__control">
                    <input class="input" type="text" value="{{ block.login|e }}" readonly>
                    <button class="button button-secondary account-copy-button" type="button" data-account-copy>Скопировать</button>
                  </div>
                </label>
                <label class="account-field">
                  <span>Пароль</span>
                  <div class="account-field__control">
                    <input class="input" type="password" value="{{ block.password_secret|e }}" readonly>
                    <button class="button button-secondary account-copy-button" type="button" data-account-copy>Скопировать</button>
                  </div>
                </label>
                <div class="account-card__details">
                  <p class="account-card__detail">{{ block.activation_summary }}</p>
                </div>
                <div class="account-actions account-actions--view">
                  <button class="button button-secondary account-card__edit-toggle" type="button" data-account-card-edit-toggle>Редактировать</button>
                  <form class="account-action-form" method="post" action="/admin/account-blocks/{{ block.id }}/delete{{ account_block_query_string }}" data-account-block-form="delete">
                    <button class="button button-secondary button-danger account-card__delete" type="submit">Удалить</button>
                  </form>
                  <form class="account-action-form" method="post" action="/admin/account-blocks/{{ block.id }}/activate{{ account_block_query_string }}" data-account-block-form="activate">
                    <label class="account-field account-field--compact">
                      <span>Срок, дней</span>
                      <input class="input" name="duration_days" type="number" min="1" value="{{ block.duration_days }}" data-account-block-duration-input>
                    </label>
                    <button class="button button-primary account-card__activate" type="submit">Активировать</button>
                  </form>
                  {% if block.is_active %}
                    <form class="account-action-form" method="post" action="/admin/account-blocks/{{ block.id }}/renew{{ account_block_query_string }}" data-account-block-form="renew">
                      <label class="account-field account-field--compact">
                        <span>Срок, дней</span>
                        <input class="input" name="duration_days" type="number" min="1" value="{{ block.duration_days }}" data-account-block-duration-input>
                      </label>
                      <button class="button button-primary account-card__renew" type="submit">Продлить активацию</button>
                    </form>
                  {% endif %}
                </div>
              </div>

              <form class="account-card__edit-form" method="post" action="/admin/account-blocks/{{ block.id }}{{ account_block_query_string }}" hidden data-account-card-edit-form data-account-block-form="update">
                <label class="account-field">
                  <span>Логин</span>
                  <input class="input" name="login" type="text" value="{{ block.login|e }}" autocomplete="off">
                </label>
                <label class="account-field">
                  <span>Пароль</span>
                  <input class="input" name="password_secret" type="text" value="{{ block.password_secret|e }}" autocomplete="off">
                </label>
                <div class="account-actions account-actions--edit">
                  <button class="button button-primary account-card__save" type="submit">Сохранить</button>
                  <button class="button button-secondary account-card__cancel" type="button" data-account-card-edit-cancel>Отмена</button>
                </div>
              </form>
            </div>
          </article>
        {% endfor %}
      </div>
    {% else %}
      {% if account_block_selected_user_summary %}
        <p class="form-help accounts-empty">У этого пользователя пока нет блоков. Добавьте первый выше.</p>
      {% endif %}
    {% endif %}
  </section>

  <script>
    (() => {
      const getAccountsRoot = () => document.querySelector("[data-local-accounts-root][data-account-blocks-source='server']");
      if (!getAccountsRoot()) {
        return;
      }

      const setNotice = (message) => {
        const root = getAccountsRoot();
        const notice = root ? root.querySelector("[data-account-blocks-notice]") : null;
        if (!notice) {
          return;
        }
        notice.textContent = message;
      };

      const copyText = async (value) => {
        if (navigator.clipboard && typeof navigator.clipboard.writeText === "function") {
          await navigator.clipboard.writeText(value);
          return true;
        }

        const textarea = document.createElement("textarea");
        textarea.value = value;
        textarea.setAttribute("readonly", "true");
        textarea.style.position = "fixed";
        textarea.style.opacity = "0";
        textarea.style.left = "-9999px";
        document.body.appendChild(textarea);
        textarea.select();

        let copied = false;
        try {
          copied = document.execCommand("copy");
        } catch (_error) {
          copied = false;
        }

        document.body.removeChild(textarea);
        return copied;
      };

      document.addEventListener("click", async (event) => {
        const editToggle = event.target.closest("[data-account-card-edit-toggle]");
        if (editToggle) {
          const card = editToggle.closest(".account-card");
          const view = card ? card.querySelector("[data-account-card-view]") : null;
          const form = card ? card.querySelector("[data-account-card-edit-form]") : null;
          if (view instanceof HTMLElement && form instanceof HTMLFormElement) {
            view.hidden = true;
            form.hidden = false;
            card.classList.add("account-card--editing");
            const firstInput = form.querySelector("input[name='login']");
            if (firstInput instanceof HTMLInputElement) {
              firstInput.focus();
              if (typeof firstInput.select === "function") {
                firstInput.select();
              }
            }
          }
          return;
        }

        const editCancel = event.target.closest("[data-account-card-edit-cancel]");
        if (editCancel) {
          const card = editCancel.closest(".account-card");
          const view = card ? card.querySelector("[data-account-card-view]") : null;
          const form = card ? card.querySelector("[data-account-card-edit-form]") : null;
          if (view instanceof HTMLElement && form instanceof HTMLFormElement) {
            form.reset();
            form.hidden = true;
            view.hidden = false;
            card.classList.remove("account-card--editing");
          }
          return;
        }

        const button = event.target.closest("[data-account-copy]");
        if (!button) {
          return;
        }

        const field = button.closest(".account-field");
        const input = field ? field.querySelector("input") : null;
        const value = input instanceof HTMLInputElement ? input.value : "";
        if (!value) {
          setNotice("Нечего копировать.");
          return;
        }

        try {
          const copied = await copyText(value);
          setNotice(copied ? "Скопировано." : "Не удалось скопировать.");
        } catch (_error) {
          setNotice("Не удалось скопировать.");
        }
      });

      document.addEventListener(
        "submit",
        async (event) => {
          const form = event.target;
          if (!(form instanceof HTMLFormElement)) {
            return;
          }
          if (!form.matches("[data-account-block-form]")) {
            return;
          }

          event.preventDefault();

          if (form.dataset.accountBlockSubmitting === "true") {
            return;
          }

          const submitButton = form.querySelector('button[type="submit"]');
          const scrollX = window.scrollX;
          const scrollY = window.scrollY;
          form.dataset.accountBlockSubmitting = "true";
          if (submitButton instanceof HTMLButtonElement) {
            submitButton.disabled = true;
          }

          try {
            const response = await fetch(form.action, {
              method: form.method || "POST",
              body: new FormData(form),
              credentials: "same-origin",
              headers: {
                "X-Requested-With": "XMLHttpRequest",
              },
            });

            const bodyText = await response.text();
            if (!response.ok) {
              setNotice("Не удалось выполнить действие.");
              return;
            }

            const parsed = new DOMParser().parseFromString(bodyText, "text/html");
            const nextRoot = parsed.querySelector("[data-local-accounts-root][data-account-blocks-source='server']");
            const currentRoot = getAccountsRoot();
            if (!(nextRoot instanceof HTMLElement) || !(currentRoot instanceof HTMLElement)) {
              if (response.url) {
                window.history.replaceState({}, "", response.url);
              }
              return;
            }

            currentRoot.replaceWith(nextRoot);
            if (response.url) {
              window.history.replaceState({}, "", response.url);
            }
            requestAnimationFrame(() => {
              window.scrollTo(scrollX, scrollY);
            });
          } catch (_error) {
            setNotice("Не удалось выполнить действие.");
          } finally {
            if (submitButton instanceof HTMLButtonElement) {
              submitButton.disabled = false;
            }
            form.dataset.accountBlockSubmitting = "false";
          }
        },
        true,
      );

    })();
  </script>

  <script src="/static/cabinet-local-accounts.js"></script>
  <script src="/static/cabinet-prompts-library.js"></script>
{% endblock %}
```


## 10. TESTS_CURRENT_EXPECTATIONS

```text
source/tests/test_admin_paid_option_crud_ui.py:16:from app.tariffs.service import seed_initial_catalog
source/tests/test_admin_paid_option_crud_ui.py:450:def test_admin_paid_option_list_shows_controls_without_tariff_linking_ui(client, test_settings):
source/tests/test_admin_paid_option_crud_ui.py:469:    assert "/admin/tariffs/" not in body
source/tests/test_cabinet_prompts_library.py:61:    assert cabinet_response.text.index('data-local-accounts-root') < cabinet_response.text.index('data-prompts-library-root')
source/tests/test_cabinet_prompts_library.py:78:    assert "openscript:cabinet:prompts-library:v1" in client.get("/static/cabinet-prompts-library.js").text
source/tests/test_cabinet_prompts_library.py:163:    assert "Личный кабинет" in cabinet_response.text
source/tests/test_landing_tariff_binding.py:3:from app.tariffs.service import (
source/tests/test_landing_tariff_binding.py:5:    create_tariff,
source/tests/test_landing_tariff_binding.py:6:    get_homepage_tariff,
source/tests/test_landing_tariff_binding.py:8:    update_tariff,
source/tests/test_landing_tariff_binding.py:12:def test_homepage_tariff_selection_prefers_selected_tariff_over_first_active(test_settings):
source/tests/test_landing_tariff_binding.py:14:    update_tariff(
source/tests/test_landing_tariff_binding.py:16:        show_on_homepage=False,
source/tests/test_landing_tariff_binding.py:19:    create_tariff(
source/tests/test_landing_tariff_binding.py:25:        show_on_homepage=False,
source/tests/test_landing_tariff_binding.py:29:    create_tariff(
source/tests/test_landing_tariff_binding.py:35:        show_on_homepage=True,
source/tests/test_landing_tariff_binding.py:40:    homepage_tariff = get_homepage_tariff(settings=test_settings)
source/tests/test_landing_tariff_binding.py:41:    assert homepage_tariff is not None
source/tests/test_landing_tariff_binding.py:42:    assert homepage_tariff.code == "homepage_selected"
source/tests/test_landing_tariff_binding.py:43:    assert homepage_tariff.show_on_homepage is True
source/tests/test_landing_tariff_binding.py:46:def test_homepage_tariff_selection_skips_inactive_tariffs(test_settings):
source/tests/test_landing_tariff_binding.py:47:    create_tariff(
source/tests/test_landing_tariff_binding.py:53:        show_on_homepage=True,
source/tests/test_landing_tariff_binding.py:57:    create_tariff(
source/tests/test_landing_tariff_binding.py:63:        show_on_homepage=True,
source/tests/test_landing_tariff_binding.py:68:    homepage_tariff = get_homepage_tariff(settings=test_settings)
source/tests/test_landing_tariff_binding.py:69:    assert homepage_tariff is not None
source/tests/test_landing_tariff_binding.py:70:    assert homepage_tariff.code == "homepage_active"
source/tests/test_landing_tariff_binding.py:71:    assert homepage_tariff.status == "active"
source/tests/test_landing_tariff_binding.py:74:def test_landing_page_uses_homepage_tariff_price(client, test_settings):
source/tests/test_landing_tariff_binding.py:76:    update_tariff(
source/tests/test_landing_tariff_binding.py:78:        show_on_homepage=False,
source/tests/test_landing_tariff_binding.py:81:    create_tariff(
source/tests/test_landing_tariff_binding.py:82:        code="homepage_tariff_selected",
source/tests/test_landing_tariff_binding.py:83:        title="Homepage tariff selected",
source/tests/test_landing_tariff_binding.py:87:        show_on_homepage=True,
source/tests/test_landing_tariff_binding.py:91:    update_tariff(
source/tests/test_landing_tariff_binding.py:99:    assert "Стартовый месяц OpenScript — 6 990 ₽" in response.text
source/tests/test_admin_tariff_crud_ui.py:10:from app.tariffs.service import (
source/tests/test_admin_tariff_crud_ui.py:12:    create_tariff,
source/tests/test_admin_tariff_crud_ui.py:13:    get_tariff_by_code,
source/tests/test_admin_tariff_crud_ui.py:14:    list_tariffs,
source/tests/test_admin_tariff_crud_ui.py:15:    list_tariffs_for_admin,
source/tests/test_admin_tariff_crud_ui.py:59:        ("/admin/tariffs/new",),
source/tests/test_admin_tariff_crud_ui.py:62:def test_anonymous_tariff_create_redirects_to_login(client, path):
source/tests/test_admin_tariff_crud_ui.py:68:def test_normal_user_cannot_open_tariff_create_page(client, test_settings):
source/tests/test_admin_tariff_crud_ui.py:74:    response = client.get("/admin/tariffs/new")
source/tests/test_admin_tariff_crud_ui.py:81:def test_admin_can_open_tariff_create_page(client, test_settings):
source/tests/test_admin_tariff_crud_ui.py:83:    response = client.get("/admin/tariffs/new")
source/tests/test_admin_tariff_crud_ui.py:108:    assert 'name="show_on_homepage"' in body
source/tests/test_admin_tariff_crud_ui.py:112:def test_admin_can_create_tariff_via_ui(client, test_settings):
source/tests/test_admin_tariff_crud_ui.py:116:        "/admin/tariffs/new",
source/tests/test_admin_tariff_crud_ui.py:118:            "code": "ui_tariff_create",
source/tests/test_admin_tariff_crud_ui.py:124:            "show_on_homepage": "1",
source/tests/test_admin_tariff_crud_ui.py:131:    assert response.headers["location"] == "/admin/tariffs"
source/tests/test_admin_tariff_crud_ui.py:133:    tariff = get_tariff_by_code("ui_tariff_create", settings=test_settings)
source/tests/test_admin_tariff_crud_ui.py:134:    assert tariff is not None
source/tests/test_admin_tariff_crud_ui.py:135:    assert tariff.title == "UI Tariff"
source/tests/test_admin_tariff_crud_ui.py:136:    assert tariff.description == "Tariff created from admin UI"
source/tests/test_admin_tariff_crud_ui.py:137:    assert tariff.price_amount_minor == 1234
source/tests/test_admin_tariff_crud_ui.py:138:    assert tariff.currency == "RUB"
source/tests/test_admin_tariff_crud_ui.py:139:    assert tariff.status == "active"
source/tests/test_admin_tariff_crud_ui.py:140:    assert tariff.show_on_homepage is True
source/tests/test_admin_tariff_crud_ui.py:141:    assert tariff.sort_order == 7
source/tests/test_admin_tariff_crud_ui.py:144:def test_admin_can_create_tariff_without_code_via_ui(client, test_settings):
source/tests/test_admin_tariff_crud_ui.py:148:        "/admin/tariffs/new",
source/tests/test_admin_tariff_crud_ui.py:162:    created = next(item for item in list_tariffs_for_admin(settings=test_settings) if item.title == "UI Tariff Without Code")
source/tests/test_admin_tariff_crud_ui.py:163:    assert created.code.startswith("tariff_")
source/tests/test_admin_tariff_crud_ui.py:167:def test_admin_tariff_create_rejects_duplicate_code_safely(client, test_settings):
source/tests/test_admin_tariff_crud_ui.py:170:        "code": "ui_tariff_duplicate",
source/tests/test_admin_tariff_crud_ui.py:179:    first = client.post("/admin/tariffs/new", data=payload, follow_redirects=False)
source/tests/test_admin_tariff_crud_ui.py:181:    second = client.post("/admin/tariffs/new", data=payload)
source/tests/test_admin_tariff_crud_ui.py:184:    assert get_tariff_by_code("ui_tariff_duplicate", settings=test_settings) is not None
source/tests/test_admin_tariff_crud_ui.py:204:                "code": "ui_tariff_negative",
source/tests/test_admin_tariff_crud_ui.py:216:def test_admin_tariff_create_rejects_invalid_input_safely(client, test_settings, payload, needle):
source/tests/test_admin_tariff_crud_ui.py:218:    response = client.post("/admin/tariffs/new", data=payload)
source/tests/test_admin_tariff_crud_ui.py:221:    assert get_tariff_by_code(payload["code"].lower().replace(" ", "_"), settings=test_settings) is None
source/tests/test_admin_tariff_crud_ui.py:226:    create_tariff(
source/tests/test_admin_tariff_crud_ui.py:227:        code="ui_tariff_edit",
source/tests/test_admin_tariff_crud_ui.py:231:        show_on_homepage=True,
source/tests/test_admin_tariff_crud_ui.py:236:    response = client.get("/admin/tariffs/ui_tariff_edit/edit")
source/tests/test_admin_tariff_crud_ui.py:258:    assert 'name="show_on_homepage"' in body
source/tests/test_admin_tariff_crud_ui.py:261:    assert "ui_tariff_edit" in body
source/tests/test_admin_tariff_crud_ui.py:267:    create_tariff(
source/tests/test_admin_tariff_crud_ui.py:268:        code="ui_tariff_update",
source/tests/test_admin_tariff_crud_ui.py:279:        "/admin/tariffs/ui_tariff_update/edit",
source/tests/test_admin_tariff_crud_ui.py:281:            "code": "ui_tariff_update",
source/tests/test_admin_tariff_crud_ui.py:287:            "show_on_homepage": "",
source/tests/test_admin_tariff_crud_ui.py:293:    assert response.headers["location"] == "/admin/tariffs"
source/tests/test_admin_tariff_crud_ui.py:295:    tariff = get_tariff_by_code("ui_tariff_update", settings=test_settings)
source/tests/test_admin_tariff_crud_ui.py:296:    assert tariff is not None
source/tests/test_admin_tariff_crud_ui.py:297:    assert tariff.code == "ui_tariff_update"
source/tests/test_admin_tariff_crud_ui.py:298:    assert tariff.title == "UI Tariff Updated"
source/tests/test_admin_tariff_crud_ui.py:299:    assert tariff.description == "Updated description"
source/tests/test_admin_tariff_crud_ui.py:300:    assert tariff.price_amount_minor == 5550
source/tests/test_admin_tariff_crud_ui.py:301:    assert tariff.status == "hidden"
source/tests/test_admin_tariff_crud_ui.py:302:    assert tariff.show_on_homepage is False
source/tests/test_admin_tariff_crud_ui.py:303:    assert tariff.sort_order == 9
source/tests/test_admin_tariff_crud_ui.py:308:    create_tariff(
source/tests/test_admin_tariff_crud_ui.py:309:        code="ui_tariff_code_lock",
source/tests/test_admin_tariff_crud_ui.py:320:        "/admin/tariffs/ui_tariff_code_lock/edit",
source/tests/test_admin_tariff_crud_ui.py:322:            "code": "ui_tariff_code_changed",
source/tests/test_admin_tariff_crud_ui.py:335:    tariff = get_tariff_by_code("ui_tariff_code_lock", settings=test_settings)
source/tests/test_admin_tariff_crud_ui.py:336:    assert tariff is not None
source/tests/test_admin_tariff_crud_ui.py:337:    assert tariff.title == "UI Tariff"
source/tests/test_admin_tariff_crud_ui.py:338:    assert get_tariff_by_code("ui_tariff_code_changed", settings=test_settings) is None
source/tests/test_admin_tariff_crud_ui.py:341:def test_admin_post_archive_sets_tariff_status_archived(client, test_settings):
source/tests/test_admin_tariff_crud_ui.py:343:    create_tariff(
source/tests/test_admin_tariff_crud_ui.py:344:        code="ui_tariff_archive",
source/tests/test_admin_tariff_crud_ui.py:354:    response = client.post("/admin/tariffs/ui_tariff_archive/archive", follow_redirects=False)
source/tests/test_admin_tariff_crud_ui.py:356:    assert response.headers["location"] == "/admin/tariffs"
source/tests/test_admin_tariff_crud_ui.py:358:    tariff = get_tariff_by_code("ui_tariff_archive", settings=test_settings)
source/tests/test_admin_tariff_crud_ui.py:359:    assert tariff is not None
source/tests/test_admin_tariff_crud_ui.py:360:    assert tariff.status == "archived"
source/tests/test_admin_tariff_crud_ui.py:361:    assert "ui_tariff_archive" not in {item.code for item in list_tariffs(settings=test_settings)}
source/tests/test_admin_tariff_crud_ui.py:362:    assert "ui_tariff_archive" in {item.code for item in list_tariffs_for_admin(settings=test_settings)}
source/tests/test_admin_tariff_crud_ui.py:365:def test_admin_tariff_list_shows_controls_without_paid_option_crud_ui(client, test_settings):
source/tests/test_admin_tariff_crud_ui.py:369:    response = client.get("/admin/tariffs")
source/tests/test_admin_tariff_crud_ui.py:372:    assert "/admin/tariffs/new" in body
source/tests/test_admin_tariff_crud_ui.py:373:    assert f"/admin/tariffs/{STARTER_TARIFF_CODE}/options" in body
source/tests/test_admin_tariff_crud_ui.py:375:    assert f"/admin/tariffs/{STARTER_TARIFF_CODE}/edit" in body
source/tests/test_admin_tariff_crud_ui.py:376:    assert f"/admin/tariffs/{STARTER_TARIFF_CODE}/archive" in body
source/tests/test_admin_tariff_crud_ui.py:382:def test_admin_tariff_form_does_not_expose_payment_ui(client, test_settings):
source/tests/test_admin_tariff_crud_ui.py:384:    response = client.get("/admin/tariffs/new")
source/tests/test_admin_access.py:86:    assert "Личный кабинет" in response.text
source/tests/test_admin_access.py:90:    assert '/admin/tariffs' in response.text
source/tests/test_materials_flow.py:139:    assert "Личный кабинет" in response.text
source/tests/test_materials_flow.py:152:    assert "Личный кабинет будет доступен после оплаты" in response.text
source/tests/test_materials_flow.py:154:    assert "Обучающий блок" not in response.text
source/tests/test_admin_catalog_services.py:11:from app.tariffs import service as tariff_service
source/tests/test_admin_catalog_services.py:12:from app.tariffs.schemas import TariffCreateInput, TariffOptionLinkInput, TariffUpdateInput
source/tests/test_admin_catalog_services.py:26:def _tariff_link_row(settings, tariff_code: str, option_code: str):
source/tests/test_admin_catalog_services.py:34:            FROM tariff_options AS topt
source/tests/test_admin_catalog_services.py:35:            JOIN tariffs AS t ON t.id = topt.tariff_id
source/tests/test_admin_catalog_services.py:39:            (tariff_code, option_code),
source/tests/test_admin_catalog_services.py:43:def test_create_tariff_accepts_dataclass_input_and_persists(test_settings):
source/tests/test_admin_catalog_services.py:44:    tariff = tariff_service.create_tariff(
source/tests/test_admin_catalog_services.py:57:    assert tariff.code == "pro_plan"
source/tests/test_admin_catalog_services.py:58:    assert tariff.title == "Pro plan"
source/tests/test_admin_catalog_services.py:59:    assert tariff.description == "Advanced access"
source/tests/test_admin_catalog_services.py:60:    assert tariff.price_amount_minor == 123456
source/tests/test_admin_catalog_services.py:61:    assert tariff.currency == "RUB"
source/tests/test_admin_catalog_services.py:62:    assert tariff.status == "hidden"
source/tests/test_admin_catalog_services.py:63:    assert tariff.sort_order == 5
source/tests/test_admin_catalog_services.py:66:def test_create_tariff_generates_safe_unique_code_when_blank(test_settings):
source/tests/test_admin_catalog_services.py:67:    first = tariff_service.create_tariff(
source/tests/test_admin_catalog_services.py:68:        title="Auto tariff one",
source/tests/test_admin_catalog_services.py:73:    second = tariff_service.create_tariff(
source/tests/test_admin_catalog_services.py:74:        title="Auto tariff two",
source/tests/test_admin_catalog_services.py:80:    assert first.code.startswith("tariff_")
source/tests/test_admin_catalog_services.py:81:    assert second.code.startswith("tariff_")
source/tests/test_admin_catalog_services.py:90:        ({"code": "ab", "title": "Valid title", "price_amount_minor": 100}, tariff_service.ValidationError),
source/tests/test_admin_catalog_services.py:91:        ({"code": "bad code", "title": "Valid title", "price_amount_minor": 100}, tariff_service.ValidationError),
source/tests/test_admin_catalog_services.py:92:        ({"code": "valid_code", "title": "   ", "price_amount_minor": 100}, tariff_service.ValidationError),
source/tests/test_admin_catalog_services.py:93:        ({"code": "valid_code", "title": "Valid title", "price_amount_minor": -1}, tariff_service.ValidationError),
source/tests/test_admin_catalog_services.py:94:        ({"code": "valid_code", "title": "Valid title", "price_amount_minor": 100, "status": "broken"}, tariff_service.ValidationError),
source/tests/test_admin_catalog_services.py:97:def test_create_tariff_rejects_invalid_inputs(test_settings, kwargs, error):
source/tests/test_admin_catalog_services.py:99:        tariff_service.create_tariff(settings=test_settings, **kwargs)
source/tests/test_admin_catalog_services.py:102:def test_create_tariff_rejects_duplicate_code(test_settings):
source/tests/test_admin_catalog_services.py:103:    tariff_service.create_tariff(
source/tests/test_admin_catalog_services.py:109:    with pytest.raises(tariff_service.ConflictError):
source/tests/test_admin_catalog_services.py:110:        tariff_service.create_tariff(
source/tests/test_admin_catalog_services.py:118:def test_update_tariff_edits_allowed_fields_and_keeps_code(test_settings):
source/tests/test_admin_catalog_services.py:119:    created = tariff_service.create_tariff(
source/tests/test_admin_catalog_services.py:125:    updated = tariff_service.update_tariff(
source/tests/test_admin_catalog_services.py:147:def test_archive_tariff_hides_it_from_public_listing_and_admin_listing_keeps_it(test_settings):
source/tests/test_admin_catalog_services.py:148:    created = tariff_service.create_tariff(
source/tests/test_admin_catalog_services.py:155:    assert tariff_service.archive_tariff(created.code, settings=test_settings) is True
source/tests/test_admin_catalog_services.py:156:    assert tariff_service.archive_tariff(created.code, settings=test_settings) is False
source/tests/test_admin_catalog_services.py:158:    public_codes = {item.code for item in tariff_service.list_tariffs(settings=test_settings)}
source/tests/test_admin_catalog_services.py:159:    admin_codes = {item.code for item in tariff_service.list_tariffs_for_admin(settings=test_settings)}
source/tests/test_admin_catalog_services.py:163:    archived = tariff_service.get_tariff_by_code(created.code, settings=test_settings)
source/tests/test_admin_catalog_services.py:167:def test_get_tariff_with_options_returns_tariff_and_linked_options(test_settings):
source/tests/test_admin_catalog_services.py:168:    tariff_service.create_tariff(
source/tests/test_admin_catalog_services.py:186:    tariff_service.attach_option_to_tariff(
source/tests/test_admin_catalog_services.py:192:    tariff_service.attach_option_to_tariff(
source/tests/test_admin_catalog_services.py:200:    payload = tariff_service.get_tariff_with_options("bundle_plan", include_hidden=True, include_archived=True, settings=test_settings)
source/tests/test_admin_catalog_services.py:201:    assert payload["tariff"].code == "bundle_plan"
source/tests/test_admin_catalog_services.py:207:def test_attach_option_to_tariff_is_idempotent_and_updates_metadata(test_settings):
source/tests/test_admin_catalog_services.py:208:    tariff_service.create_tariff(
source/tests/test_admin_catalog_services.py:221:    first = tariff_service.attach_option_to_tariff(
source/tests/test_admin_catalog_services.py:228:    second = tariff_service.attach_option_to_tariff(
source/tests/test_admin_catalog_services.py:238:    assert _count(test_settings, "tariff_options") == 1
source/tests/test_admin_catalog_services.py:239:    row = _tariff_link_row(test_settings, "attach_plan", "attach_option")
source/tests/test_admin_catalog_services.py:244:def test_update_tariff_option_link_and_detach_work(test_settings):
source/tests/test_admin_catalog_services.py:245:    tariff_service.create_tariff(
source/tests/test_admin_catalog_services.py:257:    tariff_service.attach_option_to_tariff("detach_plan", "detach_option", included_duration_days=7, included_quantity=1, settings=test_settings)
source/tests/test_admin_catalog_services.py:259:    updated = tariff_service.update_tariff_option_link(
source/tests/test_admin_catalog_services.py:268:    assert tariff_service.detach_option_from_tariff("detach_plan", "detach_option", settings=test_settings) is True
source/tests/test_admin_catalog_services.py:269:    assert tariff_service.detach_option_from_tariff("detach_plan", "detach_option", settings=test_settings) is False
source/tests/test_admin_catalog_services.py:270:    assert _count(test_settings, "tariff_options") == 0
source/tests/test_admin_catalog_services.py:273:def test_missing_tariff_option_and_link_errors_are_safe(test_settings):
source/tests/test_admin_catalog_services.py:274:    tariff_service.create_tariff(
source/tests/test_admin_catalog_services.py:287:    with pytest.raises(tariff_service.NotFoundError):
source/tests/test_admin_catalog_services.py:288:        tariff_service.update_tariff("missing_plan", title="x", settings=test_settings)
source/tests/test_admin_catalog_services.py:289:    with pytest.raises(tariff_service.NotFoundError):
source/tests/test_admin_catalog_services.py:290:        tariff_service.attach_option_to_tariff("missing_plan", "safe_option", settings=test_settings)
source/tests/test_admin_catalog_services.py:291:    with pytest.raises(tariff_service.NotFoundError):
source/tests/test_admin_catalog_services.py:292:        tariff_service.attach_option_to_tariff("safe_plan", "missing_option", settings=test_settings)
source/tests/test_admin_catalog_services.py:293:    with pytest.raises(tariff_service.NotFoundError):
source/tests/test_admin_catalog_services.py:294:        tariff_service.update_tariff_option_link("safe_plan", "safe_option", included_quantity=1, settings=test_settings)
source/tests/test_admin_catalog_services.py:295:    assert tariff_service.detach_option_from_tariff("safe_plan", "safe_option", settings=test_settings) is False
source/tests/test_admin_catalog_services.py:299:    tariff_service.create_tariff(
source/tests/test_admin_catalog_services.py:313:    with pytest.raises(tariff_service.ValidationError):
source/tests/test_admin_catalog_services.py:314:        tariff_service.attach_option_to_tariff("active_plan", "archived_option", settings=test_settings)
source/tests/test_admin_catalog_services.py:318:    tariff_service.seed_initial_catalog(settings=test_settings)
source/tests/test_admin_catalog_services.py:319:    tariff_service.create_tariff(
source/tests/test_admin_catalog_services.py:326:    tariff_service.create_tariff(
source/tests/test_admin_catalog_services.py:348:    public_tariff_codes = {item.code for item in tariff_service.list_tariffs(settings=test_settings)}
source/tests/test_admin_catalog_services.py:350:    admin_tariff_codes = {item.code for item in tariff_service.list_tariffs_for_admin(settings=test_settings)}
source/tests/test_admin_catalog_services.py:353:    assert "hidden_plan" not in public_tariff_codes
source/tests/test_admin_catalog_services.py:354:    assert "archived_plan" not in public_tariff_codes
source/tests/test_admin_catalog_services.py:357:    assert {"hidden_plan", "archived_plan"}.issubset(admin_tariff_codes)
source/tests/test_cabinet_catalog_display.py:40:        r'<section class="card stack accounts-card" data-local-accounts-root>(.*?)</section>',
source/tests/test_cabinet_catalog_display.py:48:def test_cabinet_displays_course_shell_without_tariffs_or_payment_noise(client, test_settings):
source/tests/test_cabinet_catalog_display.py:68:    assert "Обучающий блок" in cabinet_response.text
source/tests/test_cabinet_catalog_display.py:81:    assert cabinet_response.text.index("Обучающий блок") < cabinet_response.text.index("Аккаунты")
source/tests/test_cabinet_catalog_display.py:82:    assert cabinet_response.text.index('data-local-accounts-root') < cabinet_response.text.index('data-prompts-library-root')
source/tests/test_cabinet_catalog_display.py:89:    assert "Личный кабинет" not in accounts_section
source/tests/test_cabinet_catalog_display.py:125:    assert "Обучающий блок" in cabinet_response.text
source/tests/test_cabinet_catalog_display.py:155:    assert "Обучающий блок" in admin_response.text
source/tests/test_auth_flow.py:300:    assert 'class="button button-secondary nav-pill" href="/"' in register_response.text
source/tests/test_auth_flow.py:301:    assert 'class="button button-secondary nav-pill" href="/login"' in register_response.text
source/tests/test_auth_flow.py:302:    assert 'class="button button-secondary nav-pill" href="/register"' in register_response.text
source/tests/test_auth_flow.py:307:    assert 'class="button button-secondary nav-pill" href="/"' in register_response.text
source/tests/test_auth_flow.py:358:    assert "Личный кабинет будет доступен после оплаты" in cabinet_response.text
source/tests/test_auth_flow.py:363:    assert "Обучающий блок" not in cabinet_response.text
source/tests/test_auth_flow.py:639:    assert 'class="button button-secondary nav-pill" href="/"' in login_response.text
source/tests/test_auth_flow.py:640:    assert 'class="button button-secondary nav-pill" href="/login"' in login_response.text
source/tests/test_auth_flow.py:641:    assert 'class="button button-secondary nav-pill" href="/register"' in login_response.text
source/tests/test_auth_flow.py:657:    assert 'data-password-field' in login_response.text
source/tests/test_auth_flow.py:659:    assert 'auth-password-toggle.js' in login_response.text
source/tests/test_auth_flow.py:676:    assert 'data-password-field' in body
source/tests/test_auth_flow.py:678:    assert 'auth-password-toggle.js' in body
source/tests/test_auth_flow.py:708:    assert "Личный кабинет будет доступен после оплаты" in cabinet_response.text
source/tests/test_auth_flow.py:713:    assert "Обучающий блок" not in cabinet_response.text
source/tests/test_account_blocks_activation.py:10:from app.account_blocks.schemas import AccountBlockCreateInput
source/tests/test_account_blocks_activation.py:11:from app.account_blocks.service import (
source/tests/test_account_blocks_activation.py:73:    with patch("app.account_blocks.service.utc_now", return_value=fixed_now):
source/tests/test_account_blocks_activation.py:123:    with patch("app.account_blocks.service.utc_now", return_value=activation_now):
source/tests/test_account_blocks_activation.py:126:    with patch("app.account_blocks.service.utc_now", return_value=day_17_now):
source/tests/test_account_blocks_activation.py:134:    with patch("app.account_blocks.service.utc_now", return_value=day_60_now):
source/tests/test_account_blocks_activation.py:142:    with patch("app.account_blocks.service.utc_now", return_value=expired_now):
source/tests/test_account_blocks_activation.py:151:    with patch("app.account_blocks.service.utc_now", return_value=expired_now):
source/tests/test_account_blocks_activation.py:159:def test_user_cannot_activate_account_blocks(test_settings):
source/tests/test_account_blocks_activation.py:194:    with patch("app.account_blocks.service.utc_now", return_value=activation_now):
source/tests/test_account_blocks_activation.py:197:    with patch("app.account_blocks.service.utc_now", return_value=renewal_now):
source/tests/test_account_blocks_activation.py:216:    with patch("app.account_blocks.service.utc_now", return_value=renewal_now):
source/tests/test_catalog.py:7:from app.tariffs.service import (
source/tests/test_catalog.py:9:    archive_tariff,
source/tests/test_catalog.py:10:    get_tariff_by_code,
source/tests/test_catalog.py:11:    list_active_tariffs_with_options,
source/tests/test_catalog.py:12:    list_tariff_options,
source/tests/test_catalog.py:13:    list_tariffs,
source/tests/test_catalog.py:15:    upsert_tariff,
source/tests/test_catalog.py:41:    assert "tariffs" in names
source/tests/test_catalog.py:43:    assert "tariff_options" in names
source/tests/test_catalog.py:49:    tariff = get_tariff_by_code(STARTER_TARIFF_CODE, settings=test_settings)
source/tests/test_catalog.py:50:    assert tariff is not None
source/tests/test_catalog.py:51:    assert tariff.title == "Стартовый доступ"
source/tests/test_catalog.py:52:    assert tariff.price_amount_minor == 499000
source/tests/test_catalog.py:53:    assert tariff.currency == "RUB"
source/tests/test_catalog.py:54:    assert tariff.status == "active"
source/tests/test_catalog.py:59:    tariff_option_codes = {row["code"] for row in list_tariff_options(STARTER_TARIFF_CODE, settings=test_settings)}
source/tests/test_catalog.py:60:    assert tariff_option_codes == {"ai_gpt_tool", "server", "vpn"}
source/tests/test_catalog.py:66:        "tariffs": _count(test_settings, "tariffs"),
source/tests/test_catalog.py:68:        "tariff_options": _count(test_settings, "tariff_options"),
source/tests/test_catalog.py:73:        "tariffs": _count(test_settings, "tariffs"),
source/tests/test_catalog.py:75:        "tariff_options": _count(test_settings, "tariff_options"),
source/tests/test_catalog.py:79:    assert counts_after["tariffs"] == 1
source/tests/test_catalog.py:81:    assert counts_after["tariff_options"] == 3
source/tests/test_catalog.py:88:            "UPDATE tariffs SET title = ?, price_amount_minor = ?, status = ? WHERE code = ?",
source/tests/test_catalog.py:99:    tariff_row = _fetch_one(test_settings, "SELECT * FROM tariffs WHERE code = ?", (STARTER_TARIFF_CODE,))
source/tests/test_catalog.py:101:    assert tariff_row["title"] == "Custom Tariff"
source/tests/test_catalog.py:102:    assert tariff_row["price_amount_minor"] == 777000
source/tests/test_catalog.py:103:    assert tariff_row["status"] == "hidden"
source/tests/test_catalog.py:109:def test_list_tariffs_and_options_hide_non_active_by_default(test_settings):
source/tests/test_catalog.py:111:    upsert_tariff(
source/tests/test_catalog.py:112:        code="hidden_tariff",
source/tests/test_catalog.py:113:        title="Hidden tariff",
source/tests/test_catalog.py:126:    tariffs = list_tariffs(settings=test_settings)
source/tests/test_catalog.py:128:    assert all(tariff.status == "active" for tariff in tariffs)
source/tests/test_catalog.py:130:    assert "hidden_tariff" not in {tariff.code for tariff in tariffs}
source/tests/test_catalog.py:136:    upsert_tariff(
source/tests/test_catalog.py:137:        code="custom_tariff",
source/tests/test_catalog.py:138:        title="Custom tariff",
source/tests/test_catalog.py:151:    tariff = get_tariff_by_code("custom_tariff", settings=test_settings)
source/tests/test_catalog.py:153:    assert tariff is not None and tariff.title == "Custom tariff"
source/tests/test_catalog.py:159:    assert archive_tariff(STARTER_TARIFF_CODE, settings=test_settings) is True
source/tests/test_catalog.py:162:    tariff = get_tariff_by_code(STARTER_TARIFF_CODE, settings=test_settings)
source/tests/test_catalog.py:164:    assert tariff is not None and tariff.status == "archived"
source/tests/test_catalog.py:167:    tariffs = list_tariffs(settings=test_settings)
source/tests/test_catalog.py:169:    assert STARTER_TARIFF_CODE not in {item.code for item in tariffs}
source/tests/test_catalog.py:179:def test_active_tariff_helper_returns_included_active_options(test_settings):
source/tests/test_catalog.py:181:    tariffs = list_active_tariffs_with_options(settings=test_settings)
source/tests/test_catalog.py:182:    assert len(tariffs) == 1
source/tests/test_catalog.py:183:    tariff = tariffs[0]
source/tests/test_catalog.py:184:    assert tariff["code"] == STARTER_TARIFF_CODE
source/tests/test_catalog.py:185:    option_titles = [option["title"] for option in tariff["options"]]
source/tests/test_catalog.py:191:    upsert_tariff(
source/tests/test_catalog.py:192:        code="display_hidden_tariff",
source/tests/test_catalog.py:193:        title="Hidden tariff",
source/tests/test_catalog.py:205:    upsert_tariff(
source/tests/test_catalog.py:206:        code="display_archived_tariff",
source/tests/test_catalog.py:207:        title="Archived tariff",
source/tests/test_catalog.py:220:    tariffs = list_active_tariffs_with_options(settings=test_settings)
source/tests/test_catalog.py:221:    assert {item["code"] for item in tariffs} == {STARTER_TARIFF_CODE}
source/tests/test_catalog.py:222:    assert "display_hidden_tariff" not in {item.code for item in list_tariffs(settings=test_settings)}
source/tests/test_account_blocks_cabinet_ui.py:9:from app.account_blocks.schemas import AccountBlockCreateInput
source/tests/test_account_blocks_cabinet_ui.py:10:from app.account_blocks.service import activate_account_block, create_account_block
source/tests/test_account_blocks_cabinet_ui.py:105:def test_user_sees_compact_server_backed_account_blocks_and_copy_only_controls(client, test_settings):
source/tests/test_account_blocks_cabinet_ui.py:140:    with patch("app.account_blocks.service.utc_now", return_value=fixed_now):
source/tests/test_account_blocks_cabinet_ui.py:142:    with patch("app.account_blocks.service.utc_now", return_value=fixed_now):
source/tests/test_account_blocks_cabinet_ui.py:146:    with patch("app.account_blocks.service.utc_now", return_value=fixed_now):
source/tests/test_account_blocks_cabinet_ui.py:254:        with patch("app.account_blocks.service.utc_now", return_value=fixed_now):
source/tests/test_account_blocks_cabinet_ui.py:258:    with patch("app.account_blocks.service.utc_now", return_value=fixed_now):
source/tests/test_account_blocks_cabinet_ui.py:279:def test_user_with_no_active_account_blocks_sees_new_empty_state(client, test_settings):
source/tests/test_account_blocks_cabinet_ui.py:321:    cabinet_response = client.get(f"/cabinet?account_blocks_user_email={owner_a.email}")
source/tests/test_account_blocks_cabinet_ui.py:335:    assert f'action="/cabinet/account-blocks?{urlencode({"account_blocks_user_email": owner_a.email})}' in builder_shell
source/tests/test_account_blocks_cabinet_ui.py:346:        f"/cabinet/account-blocks?{urlencode({'account_blocks_user_email': owner_a.email})}",
source/tests/test_account_blocks_cabinet_ui.py:356:    assert create_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'created', 'account_blocks_user_email': owner_a.email})}"
source/tests/test_account_blocks_cabinet_ui.py:359:        row = conn.execute("SELECT * FROM account_blocks WHERE login = ?", ("mod-block-login",)).fetchone()
source/tests/test_account_blocks_cabinet_ui.py:380:    assert update_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'updated', 'account_blocks_user_email': owner_a.email})}"
source/tests/test_account_blocks_cabinet_ui.py:391:    with patch("app.account_blocks.service.utc_now", return_value=activation_now):
source/tests/test_account_blocks_cabinet_ui.py:393:            f"/cabinet/account-blocks/{block_id}/activate?{urlencode({'account_blocks_user_email': owner_a.email})}",
source/tests/test_account_blocks_cabinet_ui.py:400:    assert activate_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'activated_email_sent', 'account_blocks_user_email': owner_a.email})}"
source/tests/test_account_blocks_cabinet_ui.py:403:        updated_row = conn.execute("SELECT * FROM account_blocks WHERE id = ?", (block_id,)).fetchone()
source/tests/test_account_blocks_cabinet_ui.py:432:    with patch("app.account_blocks.service.utc_now", return_value=renewal_now):
source/tests/test_account_blocks_cabinet_ui.py:433:        active_page = client.get(f"/cabinet?{urlencode({'account_blocks_user_email': owner_a.email})}")
source/tests/test_account_blocks_cabinet_ui.py:443:    assert f'/cabinet/account-blocks/{block_id}/delete?{urlencode({"account_blocks_user_email": owner_a.email})}' in accounts_section
source/tests/test_account_blocks_cabinet_ui.py:444:    assert f'/cabinet/account-blocks/{block_id}/activate?{urlencode({"account_blocks_user_email": owner_a.email})}' in accounts_section
source/tests/test_account_blocks_cabinet_ui.py:445:    assert f'/cabinet/account-blocks/{block_id}/renew?{urlencode({"account_blocks_user_email": owner_a.email})}' in accounts_section
source/tests/test_account_blocks_cabinet_ui.py:455:    with patch("app.account_blocks.service.utc_now", return_value=renewal_now):
source/tests/test_account_blocks_cabinet_ui.py:457:            f"/cabinet/account-blocks/{block_id}/renew?{urlencode({'account_blocks_user_email': owner_a.email})}",
source/tests/test_account_blocks_cabinet_ui.py:464:    assert renew_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'renewed', 'account_blocks_user_email': owner_a.email})}"
source/tests/test_account_blocks_cabinet_ui.py:467:        renewed_row = conn.execute("SELECT * FROM account_blocks WHERE id = ?", (block_id,)).fetchone()
source/tests/test_account_blocks_cabinet_ui.py:472:        f"/cabinet/account-blocks/{block_id}/delete?{urlencode({'account_blocks_user_email': owner_a.email})}",
source/tests/test_account_blocks_cabinet_ui.py:476:    assert delete_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'deleted', 'account_blocks_user_email': owner_a.email})}"
source/tests/test_account_blocks_cabinet_ui.py:479:        deleted_row = conn.execute("SELECT 1 FROM account_blocks WHERE id = ?", (block_id,)).fetchone()
source/tests/test_account_blocks_cabinet_ui.py:501:def test_moderator_can_manage_account_blocks_but_cannot_access_admin_dashboard(client, test_settings):
source/tests/test_account_blocks_cabinet_ui.py:508:    admin_blocks_response = client.get("/admin/account-blocks?account_blocks_user_email=test@example.com")
source/tests/test_account_blocks_cabinet_ui.py:512:        f"/cabinet/account-blocks?{urlencode({'account_blocks_user_email': owner.email})}",
source/tests/test_account_blocks_cabinet_ui.py:521:    assert create_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'created', 'account_blocks_user_email': owner.email})}"
source/tests/test_account_blocks_cabinet_ui.py:524:        row = conn.execute("SELECT * FROM account_blocks WHERE login = ?", ("moderator-login",)).fetchone()
source/tests/test_account_blocks_cabinet_ui.py:540:    assert update_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'updated', 'account_blocks_user_email': owner.email})}"
source/tests/test_account_blocks_cabinet_ui.py:543:    with patch("app.account_blocks.service.utc_now", return_value=activation_now):
source/tests/test_account_blocks_cabinet_ui.py:545:            f"/cabinet/account-blocks/{block_id}/activate?{urlencode({'account_blocks_user_email': owner.email})}",
source/tests/test_account_blocks_cabinet_ui.py:550:    assert activate_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'activated_email_sent', 'account_blocks_user_email': owner.email})}"
source/tests/test_account_blocks_cabinet_ui.py:553:        activated_row = conn.execute("SELECT * FROM account_blocks WHERE id = ?", (block_id,)).fetchone()
source/tests/test_account_blocks_cabinet_ui.py:557:    with patch("app.account_blocks.service.utc_now", return_value=activation_now + timedelta(days=1)):
source/tests/test_account_blocks_cabinet_ui.py:558:        active_page = client.get(f"/cabinet?{urlencode({'account_blocks_user_email': owner.email})}")
source/tests/test_account_blocks_cabinet_ui.py:564:        f"/cabinet/account-blocks/{block_id}/renew?{urlencode({'account_blocks_user_email': owner.email})}",
source/tests/test_account_blocks_cabinet_ui.py:569:    assert renew_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'renewed', 'account_blocks_user_email': owner.email})}"
source/tests/test_account_blocks_cabinet_ui.py:572:        f"/cabinet/account-blocks/{block_id}/delete?{urlencode({'account_blocks_user_email': owner.email})}",
source/tests/test_account_blocks_cabinet_ui.py:576:    assert delete_response.headers["location"] == f"/cabinet?{urlencode({'account_blocks_notice': 'deleted', 'account_blocks_user_email': owner.email})}"
source/tests/test_account_blocks_cabinet_ui.py:643:    with patch("app.account_blocks.service.utc_now", return_value=activation_now):
source/tests/test_account_blocks_cabinet_ui.py:647:    with patch("app.account_blocks.service.utc_now", return_value=expired_now):
source/tests/test_context_navigation.py:57:    assert 'class="nav-link"' in nav
source/tests/test_context_navigation.py:63:    assert 'class="nav-link" href="#what-you-get"' in nav
source/tests/test_context_navigation.py:64:    assert 'class="nav-link" href="/login"' in nav
source/tests/test_context_navigation.py:66:    assert "Личный кабинет" not in nav
source/tests/test_context_navigation.py:106:        assert "Личный кабинет" in nav
source/tests/test_context_navigation.py:117:    assert cabinet_nav.index("Главная") < cabinet_nav.index("Обучение") < cabinet_nav.index("Личный кабинет") < cabinet_nav.index("Настройки") < cabinet_nav.index("Выйти")
source/tests/test_context_navigation.py:138:        assert "Личный кабинет" in nav
source/tests/test_context_navigation.py:168:        assert "Личный кабинет" in nav
source/tests/test_context_navigation.py:180:    assert cabinet_nav.index("Главная") < cabinet_nav.index("Обучение") < cabinet_nav.index("Личный кабинет") < cabinet_nav.index("Админ-панель") < cabinet_nav.index("Настройки") < cabinet_nav.index("Выйти")
source/tests/test_admin_readonly_lists.py:10:from app.tariffs.service import STARTER_TARIFF_CODE, seed_initial_catalog
source/tests/test_admin_readonly_lists.py:53:        ("/admin/tariffs",),
source/tests/test_admin_readonly_lists.py:67:        ("/admin/tariffs",),
source/tests/test_admin_readonly_lists.py:84:        ("/admin/tariffs",),
source/tests/test_admin_readonly_lists.py:100:        ("/admin/tariffs",),
source/tests/test_admin_readonly_lists.py:171:def test_admin_tariffs_shows_starter_tariff_and_admin_controls(client, test_settings):
source/tests/test_admin_readonly_lists.py:175:    response = client.get("/admin/tariffs")
source/tests/test_admin_readonly_lists.py:196:    assert "/admin/tariffs/new" in body
source/tests/test_admin_readonly_lists.py:197:    assert f"/admin/tariffs/{STARTER_TARIFF_CODE}/options" in body
source/tests/test_admin_readonly_lists.py:198:    assert f"/admin/tariffs/{STARTER_TARIFF_CODE}/edit" in body
source/tests/test_admin_readonly_lists.py:199:    assert f"/admin/tariffs/{STARTER_TARIFF_CODE}/archive" in body
source/tests/test_admin_readonly_lists.py:234:    assert "/admin/tariffs/" not in body
source/tests/test_admin_readonly_lists.py:249:    assert "Личный кабинет" in body
source/tests/test_admin_readonly_lists.py:253:    assert '/admin/tariffs' in body
source/tests/test_module_registration.py:16:    assert "/admin/tariffs" in paths
source/tests/test_account_blocks_service.py:8:from app.account_blocks.schemas import AccountBlockCreateInput, AccountBlockUpdateInput
source/tests/test_account_blocks_service.py:9:from app.account_blocks.service import (
source/tests/test_account_blocks_service.py:17:    list_account_blocks_for_viewer,
source/tests/test_account_blocks_service.py:59:def test_account_blocks_table_and_supported_types_exist(test_settings):
source/tests/test_account_blocks_service.py:66:        assert "account_blocks" in tables
source/tests/test_account_blocks_service.py:69:            for row in conn.execute("PRAGMA table_info(account_blocks)").fetchall()
source/tests/test_account_blocks_service.py:151:    all_blocks = list_account_blocks_for_viewer(admin, settings=test_settings)
source/tests/test_account_blocks_service.py:154:    owner_blocks = list_account_blocks_for_viewer(owner, settings=test_settings)
source/tests/test_account_blocks_service.py:166:        deleted = conn.execute("SELECT 1 FROM account_blocks WHERE id = ?", (moderator_block.id,)).fetchone()
source/tests/test_account_blocks_service.py:197:    own_blocks = list_account_blocks_for_viewer(owner, settings=test_settings)
source/tests/test_cabinet_paid_options.py:153:    assert body.index('data-local-accounts-root') < body.index('data-prompts-library-root') < body.index('data-paid-options-root')
source/tests/test_static_assets.py:102:    response = client.get("/static/cabinet-prompts-library.js")
source/tests/test_routes.py:51:    assert "Стартовый месяц OpenScript — 4 990 ₽" in response.text
source/tests/test_routes.py:72:    assert "Личный кабинет" in response.text
source/tests/test_routes.py:93:    assert ".top-nav .nav-links {" in response.text
source/tests/test_routes.py:95:    assert ".top-nav .nav-links .nav-pill," in response.text
source/tests/test_routes.py:170:        assert "Личный кабинет" not in response.text
source/tests/test_admin_paid_access_grant.py:81:    assert "/materials-access/grant" in body
source/tests/test_admin_paid_access_grant.py:82:    assert "/materials-access/revoke" in body
source/tests/test_admin_paid_access_grant.py:95:    grant_response = client.post(f"/admin/users/{target_user.id}/materials-access/grant", follow_redirects=False)
source/tests/test_admin_paid_access_grant.py:117:    revoke_response = client.post(f"/admin/users/{target_user.id}/materials-access/revoke", follow_redirects=False)
source/tests/test_admin_paid_access_grant.py:129:    assert "Личный кабинет будет доступен после оплаты" in locked_cabinet.text
source/tests/test_admin_paid_access_grant.py:144:    anonymous_response = client.post(f"/admin/users/{target_user.id}/materials-access/grant", follow_redirects=False)
source/tests/test_admin_paid_access_grant.py:150:    user_grant_response = client.post(f"/admin/users/{target_again.id}/materials-access/grant")
source/tests/test_admin_paid_access_grant.py:152:    user_revoke_response = client.post(f"/admin/users/{target_again.id}/materials-access/revoke")
source/tests/test_admin_paid_access_grant.py:158:    moderator_grant_response = client.post(f"/admin/users/{target_again.id}/materials-access/grant")
source/tests/test_admin_paid_access_grant.py:160:    moderator_revoke_response = client.post(f"/admin/users/{target_again.id}/materials-access/revoke")
source/tests/test_admin_paid_access_grant.py:182:    assert "Личный кабинет будет доступен после оплаты" in cabinet_response.text
source/tests/test_account_blocks_permissions.py:4:from app.auth.service import can_manage_account_blocks, is_admin_role
source/tests/test_account_blocks_permissions.py:11:    assert can_manage_account_blocks("admin")
source/tests/test_account_blocks_permissions.py:12:    assert can_manage_account_blocks("moderator")
source/tests/test_account_blocks_permissions.py:13:    assert not can_manage_account_blocks("user")
source/tests/test_account_blocks_permissions.py:14:    assert not can_manage_account_blocks(None)
source/tests/test_account_blocks_permissions.py:49:    assert can_manage_account_blocks(admin)
source/tests/test_account_blocks_permissions.py:50:    assert can_manage_account_blocks(moderator)
source/tests/test_account_blocks_permissions.py:51:    assert not can_manage_account_blocks(user)
source/tests/test_account_blocks_permissions.py:55:    assert can_manage_account_blocks("ADMIN")
source/tests/test_account_blocks_permissions.py:56:    assert can_manage_account_blocks(" moderator ")
source/tests/test_account_blocks_permissions.py:57:    assert not can_manage_account_blocks("guest")
source/tests/test_admin_tariff_option_linking_ui.py:11:from app.tariffs.service import STARTER_TARIFF_CODE, get_tariff_by_code, list_tariff_options, seed_initial_catalog
source/tests/test_admin_tariff_option_linking_ui.py:55:        description="Active option for tariff linking",
source/tests/test_admin_tariff_option_linking_ui.py:65:        description="Archived option for tariff linking",
source/tests/test_admin_tariff_option_linking_ui.py:78:        (f"/admin/tariffs/{STARTER_TARIFF_CODE}/options",),
source/tests/test_admin_tariff_option_linking_ui.py:81:def test_anonymous_tariff_options_redirects_to_login(client, path):
source/tests/test_admin_tariff_option_linking_ui.py:87:def test_normal_user_gets_forbidden_on_tariff_options_page(client, test_settings):
source/tests/test_admin_tariff_option_linking_ui.py:93:    response = client.get(f"/admin/tariffs/{STARTER_TARIFF_CODE}/options")
source/tests/test_admin_tariff_option_linking_ui.py:100:def test_admin_tariff_options_page_returns_404_for_missing_tariff(client, test_settings):
source/tests/test_admin_tariff_option_linking_ui.py:102:    response = client.get("/admin/tariffs/missing_tariff/options")
source/tests/test_admin_tariff_option_linking_ui.py:106:def test_admin_tariff_options_page_shows_linked_and_attachable_options(client, test_settings):
source/tests/test_admin_tariff_option_linking_ui.py:110:    response = client.get(f"/admin/tariffs/{STARTER_TARIFF_CODE}/options")
source/tests/test_admin_tariff_option_linking_ui.py:126:    assert "Настроить опции" not in body  # link lives on tariffs list, not page header
source/tests/test_admin_tariff_option_linking_ui.py:141:def test_admin_tariff_options_page_has_tariffs_list_link(client, test_settings):
source/tests/test_admin_tariff_option_linking_ui.py:145:    response = client.get("/admin/tariffs")
source/tests/test_admin_tariff_option_linking_ui.py:148:    assert f"/admin/tariffs/{STARTER_TARIFF_CODE}/options" in body
source/tests/test_admin_tariff_option_linking_ui.py:157:        f"/admin/tariffs/{STARTER_TARIFF_CODE}/options/attach",
source/tests/test_admin_tariff_option_linking_ui.py:166:    assert first.headers["location"] == f"/admin/tariffs/{STARTER_TARIFF_CODE}/options"
source/tests/test_admin_tariff_option_linking_ui.py:169:        f"/admin/tariffs/{STARTER_TARIFF_CODE}/options/attach",
source/tests/test_admin_tariff_option_linking_ui.py:179:    links = [row for row in list_tariff_options(STARTER_TARIFF_CODE, include_hidden=True, include_archived=True, settings=test_settings) if row["code"] == active_code]
source/tests/test_admin_tariff_option_linking_ui.py:190:        f"/admin/tariffs/{STARTER_TARIFF_CODE}/options/attach",
source/tests/test_admin_tariff_option_linking_ui.py:205:        f"/admin/tariffs/{STARTER_TARIFF_CODE}/options/attach",
source/tests/test_admin_tariff_option_linking_ui.py:215:        f"/admin/tariffs/{STARTER_TARIFF_CODE}/options/{active_code}/update",
source/tests/test_admin_tariff_option_linking_ui.py:223:    links = [row for row in list_tariff_options(STARTER_TARIFF_CODE, include_hidden=True, include_archived=True, settings=test_settings) if row["code"] == active_code]
source/tests/test_admin_tariff_option_linking_ui.py:233:        f"/admin/tariffs/{STARTER_TARIFF_CODE}/options/attach",
source/tests/test_admin_tariff_option_linking_ui.py:243:        f"/admin/tariffs/{STARTER_TARIFF_CODE}/options/{active_code}/detach",
source/tests/test_admin_tariff_option_linking_ui.py:247:    assert response.headers["location"] == f"/admin/tariffs/{STARTER_TARIFF_CODE}/options"
source/tests/test_admin_tariff_option_linking_ui.py:248:    assert get_tariff_by_code(STARTER_TARIFF_CODE, settings=test_settings) is not None
source/tests/test_admin_tariff_option_linking_ui.py:250:    assert active_code not in {row["code"] for row in list_tariff_options(STARTER_TARIFF_CODE, include_hidden=True, include_archived=True, settings=test_settings)}
source/tests/test_admin_tariff_option_linking_ui.py:258:        f"/admin/tariffs/{STARTER_TARIFF_CODE}/options/ui_link_active/update",
source/tests/test_admin_tariff_option_linking_ui.py:267:        f"/admin/tariffs/{STARTER_TARIFF_CODE}/options/ui_link_active/detach",
source/tests/test_admin_tariff_option_linking_ui.py:272:        f"/admin/tariffs/{STARTER_TARIFF_CODE}/options/missing_option/attach",
source/tests/test_admin_tariff_option_linking_ui.py:281:def test_admin_tariff_options_page_shows_empty_state_when_no_active_unlinked_options(client, test_settings):
source/tests/test_admin_tariff_option_linking_ui.py:285:        f"/admin/tariffs/{STARTER_TARIFF_CODE}/options/attach",
source/tests/test_admin_tariff_option_linking_ui.py:294:    response = client.get(f"/admin/tariffs/{STARTER_TARIFF_CODE}/options")
source/tests/test_admin_tariff_option_linking_ui.py:306:def test_admin_tariff_options_page_is_read_safe(client, test_settings):
source/tests/test_admin_tariff_option_linking_ui.py:310:    response = client.get(f"/admin/tariffs/{STARTER_TARIFF_CODE}/options")
source/tests/test_account_blocks_admin_ui.py:9:from app.account_blocks.schemas import AccountBlockCreateInput
source/tests/test_account_blocks_admin_ui.py:10:from app.account_blocks.service import create_account_block
source/tests/test_account_blocks_admin_ui.py:87:    response = client.get(f"/admin/account-blocks?{urlencode({'account_blocks_user_email': owner.email})}")
source/tests/test_account_blocks_admin_ui.py:95:    assert 'name="account_blocks_user_email"' in body
source/tests/test_account_blocks_admin_ui.py:99:    assert f'action="/admin/account-blocks?{urlencode({"account_blocks_user_email": owner.email})}' in body
source/tests/test_account_blocks_admin_ui.py:105:        f"/admin/account-blocks?{urlencode({'account_blocks_user_email': owner.email})}",
source/tests/test_account_blocks_admin_ui.py:116:    assert create_response.headers["location"] == f"/admin/account-blocks?{urlencode({'account_blocks_notice': 'created', 'account_blocks_user_email': owner.email})}"
source/tests/test_account_blocks_admin_ui.py:119:        row = conn.execute("SELECT * FROM account_blocks WHERE login = ?", ("admin-ui-login",)).fetchone()
source/tests/test_account_blocks_admin_ui.py:127:    with patch("app.account_blocks.service.utc_now", return_value=activation_now):
source/tests/test_account_blocks_admin_ui.py:129:            f"/admin/account-blocks/{block_id}/activate?{urlencode({'account_blocks_user_email': owner.email})}",
source/tests/test_account_blocks_admin_ui.py:134:    assert activate_response.headers["location"] == f"/admin/account-blocks?{urlencode({'account_blocks_notice': 'activated_email_sent', 'account_blocks_user_email': owner.email})}"
source/tests/test_account_blocks_admin_ui.py:137:        activated_row = conn.execute("SELECT * FROM account_blocks WHERE id = ?", (block_id,)).fetchone()
source/tests/test_account_blocks_admin_ui.py:157:    with patch("app.account_blocks.service.utc_now", return_value=activation_now):
source/tests/test_account_blocks_admin_ui.py:158:        active_page = client.get(f"/admin/account-blocks?{urlencode({'account_blocks_user_email': owner.email})}")
source/tests/test_account_blocks_admin_ui.py:165:    with patch("app.account_blocks.service.utc_now", return_value=renewal_now):
source/tests/test_account_blocks_admin_ui.py:167:            f"/admin/account-blocks/{block_id}/renew?{urlencode({'account_blocks_user_email': owner.email})}",
source/tests/test_account_blocks_admin_ui.py:172:    assert renew_response.headers["location"] == f"/admin/account-blocks?{urlencode({'account_blocks_notice': 'renewed', 'account_blocks_user_email': owner.email})}"
source/tests/test_account_blocks_admin_ui.py:175:        renewed_row = conn.execute("SELECT * FROM account_blocks WHERE id = ?", (block_id,)).fetchone()
source/tests/test_account_blocks_admin_ui.py:179:    with patch("app.account_blocks.service.utc_now", return_value=renewal_now):
source/tests/test_account_blocks_admin_ui.py:180:        renewed_page = client.get(f"/admin/account-blocks?{urlencode({'account_blocks_user_email': owner.email})}")
```


```diff
diff --git a/source/tests/test_admin_tariff_crud_ui.py b/source/tests/test_admin_tariff_crud_ui.py
index 4eaa674..5c95187 100644
--- a/source/tests/test_admin_tariff_crud_ui.py
+++ b/source/tests/test_admin_tariff_crud_ui.py
@@ -105,6 +105,7 @@ def test_admin_can_open_tariff_create_page(client, test_settings):
     assert "Description" not in body
     assert "Price, RUB" not in body
     assert 'name="code"' in body
+    assert 'name="show_on_homepage"' in body
     assert "Нужен программе. Можно оставить пустым — система создаст код автоматически." in body
 
 
@@ -120,6 +121,7 @@ def test_admin_can_create_tariff_via_ui(client, test_settings):
             "price_rub": "12.34",
             "currency": "RUB",
             "status": "active",
+            "show_on_homepage": "1",
             "sort_order": "7",
         },
         follow_redirects=False,
@@ -135,6 +137,7 @@ def test_admin_can_create_tariff_via_ui(client, test_settings):
     assert tariff.price_amount_minor == 1234
     assert tariff.currency == "RUB"
     assert tariff.status == "active"
+    assert tariff.show_on_homepage is True
     assert tariff.sort_order == 7
 
 
@@ -225,6 +228,7 @@ def test_admin_edit_page_shows_code_as_read_only(client, test_settings):
         title="UI Tariff",
         description="Initial description",
         price_amount_minor=1000,
+        show_on_homepage=True,
         status="active",
         settings=test_settings,
     )
@@ -251,7 +255,9 @@ def test_admin_edit_page_shows_code_as_read_only(client, test_settings):
     assert "Code" not in body
     assert "Title" not in body
     assert 'name="code"' in body
+    assert 'name="show_on_homepage"' in body
     assert "readonly" in body
+    assert "checked" in body
     assert "ui_tariff_edit" in body
     assert "Системный код нельзя изменить после создания." in body
 
@@ -278,6 +284,7 @@ def test_admin_post_edit_updates_allowed_fields_and_keeps_code(client, test_sett
             "price_rub": "55.50",
             "currency": "RUB",
             "status": "hidden",
+            "show_on_homepage": "",
             "sort_order": "9",
         },
         follow_redirects=False,
@@ -292,6 +299,7 @@ def test_admin_post_edit_updates_allowed_fields_and_keeps_code(client, test_sett
     assert tariff.description == "Updated description"
     assert tariff.price_amount_minor == 5550
     assert tariff.status == "hidden"
+    assert tariff.show_on_homepage is False
     assert tariff.sort_order == 9
 
 
diff --git a/source/tests/test_context_navigation.py b/source/tests/test_context_navigation.py
index 1636708..5ab31e6 100644
--- a/source/tests/test_context_navigation.py
+++ b/source/tests/test_context_navigation.py
@@ -54,11 +54,14 @@ def test_anonymous_navigation_shows_public_links_and_login(client):
     response = client.get("/login")
     assert response.status_code == 200
     nav = _nav_block(response.text)
+    assert 'class="nav-link"' in nav
     assert "Что вы получите" in nav
     assert "Первый проект" in nav
     assert "Как проходит работа" in nav
     assert "Цена" in nav
     assert "Войти" in nav
+    assert 'class="nav-link" href="#what-you-get"' in nav
+    assert 'class="nav-link" href="/login"' in nav
     assert "Начать первый проект" not in nav
     assert "Личный кабинет" not in nav
     assert "Работа с ИИ" not in nav
diff --git a/source/tests/test_landing_tariff_binding.py b/source/tests/test_landing_tariff_binding.py
index b710bef..690989f 100644
--- a/source/tests/test_landing_tariff_binding.py
+++ b/source/tests/test_landing_tariff_binding.py
@@ -9,30 +9,38 @@ from app.tariffs.service import (
 )
 
 
-def test_homepage_tariff_selection_prefers_lowest_sort_order_active_tariff(test_settings):
+def test_homepage_tariff_selection_prefers_selected_tariff_over_first_active(test_settings):
+    seed_initial_catalog(settings=test_settings)
+    update_tariff(
+        STARTER_TARIFF_CODE,
+        show_on_homepage=False,
+        settings=test_settings,
+    )
     create_tariff(
-        code="homepage_later",
-        title="Homepage later",
+        code="homepage_first",
+        title="Homepage first",
         price_amount_minor=1000,
         currency="RUB",
         status="active",
-        sort_order=10,
+        show_on_homepage=False,
+        sort_order=1,
         settings=test_settings,
     )
     create_tariff(
-        code="homepage_first",
-        title="Homepage first",
+        code="homepage_selected",
+        title="Homepage selected",
         price_amount_minor=2000,
         currency="RUB",
         status="active",
-        sort_order=1,
+        show_on_homepage=True,
+        sort_order=10,
         settings=test_settings,
     )
 
     homepage_tariff = get_homepage_tariff(settings=test_settings)
     assert homepage_tariff is not None
-    assert homepage_tariff.code == "homepage_first"
-    assert homepage_tariff.status == "active"
+    assert homepage_tariff.code == "homepage_selected"
+    assert homepage_tariff.show_on_homepage is True
 
 
 def test_homepage_tariff_selection_skips_inactive_tariffs(test_settings):
@@ -42,6 +50,7 @@ def test_homepage_tariff_selection_skips_inactive_tariffs(test_settings):
         price_amount_minor=3000,
         currency="RUB",
         status="hidden",
+        show_on_homepage=True,
         sort_order=0,
         settings=test_settings,
     )
@@ -51,6 +60,7 @@ def test_homepage_tariff_selection_skips_inactive_tariffs(test_settings):
         price_amount_minor=4000,
         currency="RUB",
         status="active",
+        show_on_homepage=True,
         sort_order=2,
         settings=test_settings,
     )
@@ -65,7 +75,22 @@ def test_landing_page_uses_homepage_tariff_price(client, test_settings):
     seed_initial_catalog(settings=test_settings)
     update_tariff(
         STARTER_TARIFF_CODE,
+        show_on_homepage=False,
+        settings=test_settings,
+    )
+    create_tariff(
+        code="homepage_tariff_selected",
+        title="Homepage tariff selected",
         price_amount_minor=699000,
+        currency="RUB",
+        status="active",
+        show_on_homepage=True,
+        sort_order=10,
+        settings=test_settings,
+    )
+    update_tariff(
+        STARTER_TARIFF_CODE,
+        price_amount_minor=499000,
         settings=test_settings,
     )
 
diff --git a/source/tests/test_materials_flow.py b/source/tests/test_materials_flow.py
index 10e2f76..a5d83d0 100644
--- a/source/tests/test_materials_flow.py
+++ b/source/tests/test_materials_flow.py
@@ -107,25 +107,24 @@ def test_materials_shows_locked_state_without_access(client, test_settings):
     response = client.get("/materials")
     assert response.status_code == 200
     assert "/static/styles.css" in response.text
-    assert "Работа с ИИ" in response.text
-    assert "Курс для новичков без опыта программирования." in response.text
-    assert "Уроки курса" in response.text
-    assert "Как мы работаем: ChatGPT проектирует, Codex выполняет, пользователь проверяет" in response.text
-    assert "/materials/lessons/kak-my-rabotaem-chatgpt-codex-user" in response.text
-    assert "Вернуться в личный кабинет" in response.text
+    assert "Доступ ограничен" in response.text
+    assert "Раздел «Работа с ИИ» закрыт" in response.text
+    assert "Доступ к материалам и урокам откроется после оплаты тарифа." in response.text
+    assert "В личный кабинет" in response.text
+    assert "Курс для новичков без опыта программирования." not in response.text
+    assert "Уроки курса" not in response.text
+    assert "Как мы работаем: ChatGPT проектирует, Codex выполняет, пользователь проверяет" not in response.text
+    assert "/materials/lessons/kak-my-rabotaem-chatgpt-codex-user" not in response.text
     assert "/cabinet" in response.text
-    assert "Доступные тарифы" not in response.text
-    assert "Оплата" not in response.text
-    assert "Что дальше" not in response.text
-    assert "Раздел «Работа с ИИ» будет доступен после оплаты." not in response.text
-    assert "После первой оплаты доступ к разделу останется навсегда." not in response.text
-    assert "Быстрый старт" not in response.text
-    assert "Как работать с AI-агентом" not in response.text
-    assert "Команды для копирования" not in response.text
     assert "/admin" not in response.text
     assert "Payment" not in response.text
     assert "Locked" not in response.text
 
+    lesson_response = client.get("/materials/lessons/kak-my-rabotaem-chatgpt-codex-user")
+    assert lesson_response.status_code == 200
+    assert "Доступ ограничен" in lesson_response.text
+    assert "Урок и его материалы откроются после оплаты тарифа." in lesson_response.text
+    assert "lesson-content" not in lesson_response.text
 
 def test_materials_shows_placeholder_sections_when_access_granted(client, test_settings):
     _prepare_and_login_verified_user(client, test_settings, "materials-open@example.com", "materialsopen", grant_access=True)
@@ -150,18 +149,20 @@ def test_cabinet_contains_materials_link_and_locked_hint(client, test_settings):
     response = client.get("/cabinet")
     assert response.status_code == 200
     assert "Главная" in response.text
-    assert "Обучающий блок" in response.text
-    assert "Обучение" in response.text
-    assert "Перейти к обучению" in response.text
-    assert "Обучающий проект" in response.text
-    assert "Скачать файл" in response.text
-    assert "Доступ откроется после оплаты." in response.text
-    assert response.text.count('class="button button-primary learning-button"') == 2
-    assert 'href="/materials/drafts/dair-smoke-20260529/"' not in response.text
+    assert "Личный кабинет будет доступен после оплаты" in response.text
+    assert "После оплаты тарифа откроются личный кабинет, обучение и материалы." in response.text
+    assert "Обучающий блок" not in response.text
+    assert "Перейти к обучению" not in response.text
+    assert "Обучающий проект" not in response.text
+    assert "Скачать файл" not in response.text
+    assert "Доступ откроется после оплаты." not in response.text
+    assert response.text.count('class="button button-primary learning-button"') == 0
+    assert "К обучению" in response.text
+    assert 'href="/materials/drafts/dair-smoke-20260529/"' in response.text
     assert 'href="/cabinet/learning/project-file"' not in response.text
-    assert "Аккаунты" in response.text
-    assert "/static/cabinet-local-accounts.js" in response.text
-    assert "Пройдите обучение, затем скачайте файл, вставьте в чат ChatGPT и следуйте его инструкциям." in response.text
+    assert "Аккаунты" not in response.text
+    assert "/static/cabinet-local-accounts.js" not in response.text
+    assert "Пройдите обучение, затем скачайте файл, вставьте в чат ChatGPT и следуйте его инструкциям." not in response.text
     assert "Раздел «Работа с ИИ» будет доступен после оплаты." not in response.text
 
 
diff --git a/source/tests/test_routes.py b/source/tests/test_routes.py
index b5131aa..9873a44 100644
--- a/source/tests/test_routes.py
+++ b/source/tests/test_routes.py
@@ -117,10 +117,9 @@ def test_login_and_register_pages(client):
     assert cabinet_response.headers["location"] == "/login"
     assert "Вход в аккаунт" in login_response.text
     assert "Регистрация" in register_response.text
-    assert "Регистрация временно закрыта" in register_response.text
-    assert "Перейти ко входу" in register_response.text
+    assert "Создать аккаунт" in register_response.text
     assert "/login" in register_response.text
-    assert "Создать аккаунт" not in register_response.text
+    assert "Регистрация временно закрыта" not in register_response.text
     assert "Нет аккаунта?" in login_response.text
     assert "Зарегистрироваться" in login_response.text
     assert "Забыли пароль?" in login_response.text
@@ -133,9 +132,8 @@ def test_login_and_register_pages(client):
     assert "/static/styles.css" in login_response.text
     assert "/static/styles.css" in register_response.text
     assert "Электронная почта или логин" in login_response.text
-    assert "Регистрация временно закрыта" in register_response.text
-    assert "Перейти ко входу" in register_response.text
-    assert "Создать аккаунт" not in register_response.text
+    assert "Создать аккаунт" in register_response.text
+    assert "Регистрация временно закрыта" not in register_response.text
     assert "Подтверждение почты" not in login_response.text
     assert "Не пришло письмо подтверждения?" not in login_response.text
     assert "Отправить письмо подтверждения" not in login_response.text
diff --git a/source/tests/test_static_assets.py b/source/tests/test_static_assets.py
index d5a5d3d..5b21d31 100644
--- a/source/tests/test_static_assets.py
+++ b/source/tests/test_static_assets.py
@@ -43,8 +43,7 @@ def test_stylesheet_is_served(client):
     assert ".accounts-grid" in response.text
     assert ".account-card" in response.text
     assert ".account-password-row" in response.text
-    assert "width: min(100%, 320px);" in response.text
-    assert "max-width: 340px;" in response.text
+    assert "width: min(100%, 34rem);" in response.text
     assert ".accounts-builder .select {" in response.text
     assert "min-height: 38px;" in response.text
     assert ".accounts-builder .button {" in response.text
```


## 11. CLEAN_CHECKOUT_RISK_CURRENT

| path | tracked yes/no | exists yes/no | referenced by tracked source/tests yes/no | clean checkout risk yes/no | current content included yes/no |
|---|---|---|---|---|---|
| `source/app/static/auth-password-toggle.js` | no | yes | yes | yes | yes |
| `source/app/shared/tariff_display.py` | no | yes | yes | yes | yes |
| `source/app/shared/templates/tariff_pricing_section.html` | no | yes | no | no | yes |
| `source/app/materials/templates/learning_locked.html` | no | yes | no | no | yes |
| `source/app/user_cabinet/templates/access_locked.html` | no | yes | yes | yes | yes |
| `source/app/user_cabinet/prompts_library.py` | yes | yes | yes | no | yes |
| `source/app/static/cabinet-prompts-library.js` | yes | yes | yes | no | yes |
| `source/app/account_blocks/__init__.py` | no | yes | yes | yes | yes |
| `source/app/account_blocks/schemas.py` | no | yes | yes | yes | yes |
| `source/app/account_blocks/service.py` | no | yes | yes | yes | yes |
| `source/app/admin/templates/account_blocks.html` | no | yes | yes | yes | no |


## 12. SUMMARY_OF_CURRENT_CODE_ONLY

- current code currently renders auth password toggle buttons on login/register and loads the toggle script
- current code currently routes authenticated users through nav pills and anonymous users through hash links in the header
- current code currently selects the public tariff from active tariffs with `show_on_homepage` and falls back to the first active tariff
- current code currently gates materials and cabinet access on materials access or staff role
- current code currently renders cabinet account blocks, prompts, and paid options from tracked routes/templates plus untracked helpers
- current dependencies that are untracked are listed in the clean-checkout risk section


## 13. FINAL_CONFIRMATION

```text
files edited: no
tests edited: no
report file created: yes
commit created: no
push done: no
deploy done: no
reset/revert/checkout done: no
secrets read/printed: no
runtime mutated: no
```
