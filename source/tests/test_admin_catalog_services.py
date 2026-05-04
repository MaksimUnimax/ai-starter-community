from __future__ import annotations

import re
import sqlite3

import pytest

from app.paid_options import service as paid_option_service
from app.paid_options.schemas import PaidOptionCreateInput, PaidOptionUpdateInput
from app.shared.db import get_database_path
from app.tariffs import service as tariff_service
from app.tariffs.schemas import TariffCreateInput, TariffOptionLinkInput, TariffUpdateInput


def _connect(settings):
    conn = sqlite3.connect(str(get_database_path(settings)))
    conn.row_factory = sqlite3.Row
    return conn


def _count(settings, table: str) -> int:
    with _connect(settings) as conn:
        return int(conn.execute(f"SELECT COUNT(*) AS c FROM {table}").fetchone()["c"])


def _tariff_link_row(settings, tariff_code: str, option_code: str):
    with _connect(settings) as conn:
        return conn.execute(
            """
            SELECT
                topt.included_duration_days,
                topt.included_quantity,
                po.code AS option_code
            FROM tariff_options AS topt
            JOIN tariffs AS t ON t.id = topt.tariff_id
            JOIN paid_options AS po ON po.id = topt.option_id
            WHERE t.code = ? AND po.code = ?
            """,
            (tariff_code, option_code),
        ).fetchone()


def test_create_tariff_accepts_dataclass_input_and_persists(test_settings):
    tariff = tariff_service.create_tariff(
        data=TariffCreateInput(
            code="pro_plan",
            title="Pro plan",
            description="Advanced access",
            price_amount_minor=123456,
            currency="rub",
            status="hidden",
            sort_order=5,
        ),
        settings=test_settings,
    )

    assert tariff.code == "pro_plan"
    assert tariff.title == "Pro plan"
    assert tariff.description == "Advanced access"
    assert tariff.price_amount_minor == 123456
    assert tariff.currency == "RUB"
    assert tariff.status == "hidden"
    assert tariff.sort_order == 5


def test_create_tariff_generates_safe_unique_code_when_blank(test_settings):
    first = tariff_service.create_tariff(
        title="Auto tariff one",
        price_amount_minor=1000,
        code=None,
        settings=test_settings,
    )
    second = tariff_service.create_tariff(
        title="Auto tariff two",
        price_amount_minor=2000,
        code="",
        settings=test_settings,
    )

    assert first.code.startswith("tariff_")
    assert second.code.startswith("tariff_")
    assert re.fullmatch(r"[a-z0-9_-]{3,64}", first.code)
    assert re.fullmatch(r"[a-z0-9_-]{3,64}", second.code)
    assert first.code != second.code


@pytest.mark.parametrize(
    ("kwargs", "error"),
    [
        ({"code": "ab", "title": "Valid title", "price_amount_minor": 100}, tariff_service.ValidationError),
        ({"code": "bad code", "title": "Valid title", "price_amount_minor": 100}, tariff_service.ValidationError),
        ({"code": "valid_code", "title": "   ", "price_amount_minor": 100}, tariff_service.ValidationError),
        ({"code": "valid_code", "title": "Valid title", "price_amount_minor": -1}, tariff_service.ValidationError),
        ({"code": "valid_code", "title": "Valid title", "price_amount_minor": 100, "status": "broken"}, tariff_service.ValidationError),
    ],
)
def test_create_tariff_rejects_invalid_inputs(test_settings, kwargs, error):
    with pytest.raises(error):
        tariff_service.create_tariff(settings=test_settings, **kwargs)


def test_create_tariff_rejects_duplicate_code(test_settings):
    tariff_service.create_tariff(
        code="dup_plan",
        title="Duplicate plan",
        price_amount_minor=1000,
        settings=test_settings,
    )
    with pytest.raises(tariff_service.ConflictError):
        tariff_service.create_tariff(
            code="dup_plan",
            title="Duplicate plan again",
            price_amount_minor=2000,
            settings=test_settings,
        )


def test_update_tariff_edits_allowed_fields_and_keeps_code(test_settings):
    created = tariff_service.create_tariff(
        code="edit_plan",
        title="Edit plan",
        price_amount_minor=1000,
        settings=test_settings,
    )
    updated = tariff_service.update_tariff(
        created.code,
        data=TariffUpdateInput(
            title="Edited plan",
            description="Updated description",
            price_amount_minor=2500,
            currency="usd",
            status="hidden",
            sort_order=9,
        ),
        settings=test_settings,
    )

    assert updated.code == created.code
    assert updated.title == "Edited plan"
    assert updated.description == "Updated description"
    assert updated.price_amount_minor == 2500
    assert updated.currency == "USD"
    assert updated.status == "hidden"
    assert updated.sort_order == 9


def test_archive_tariff_hides_it_from_public_listing_and_admin_listing_keeps_it(test_settings):
    created = tariff_service.create_tariff(
        code="archive_plan",
        title="Archive plan",
        price_amount_minor=1000,
        settings=test_settings,
    )

    assert tariff_service.archive_tariff(created.code, settings=test_settings) is True
    assert tariff_service.archive_tariff(created.code, settings=test_settings) is False

    public_codes = {item.code for item in tariff_service.list_tariffs(settings=test_settings)}
    admin_codes = {item.code for item in tariff_service.list_tariffs_for_admin(settings=test_settings)}

    assert created.code not in public_codes
    assert created.code in admin_codes
    archived = tariff_service.get_tariff_by_code(created.code, settings=test_settings)
    assert archived is not None and archived.status == "archived"


def test_get_tariff_with_options_returns_tariff_and_linked_options(test_settings):
    tariff_service.create_tariff(
        code="bundle_plan",
        title="Bundle plan",
        price_amount_minor=1500,
        settings=test_settings,
    )
    paid_option_service.create_paid_option(
        code="bundle_ai",
        title="Bundle AI",
        price_amount_minor=None,
        settings=test_settings,
    )
    paid_option_service.create_paid_option(
        code="bundle_support",
        title="Bundle Support",
        price_amount_minor=500,
        settings=test_settings,
    )
    tariff_service.attach_option_to_tariff(
        "bundle_plan",
        "bundle_ai",
        data=TariffOptionLinkInput(included_duration_days=14, included_quantity=1),
        settings=test_settings,
    )
    tariff_service.attach_option_to_tariff(
        "bundle_plan",
        "bundle_support",
        included_duration_days=None,
        included_quantity=2,
        settings=test_settings,
    )

    payload = tariff_service.get_tariff_with_options("bundle_plan", include_hidden=True, include_archived=True, settings=test_settings)
    assert payload["tariff"].code == "bundle_plan"
    assert [option["code"] for option in payload["options"]] == ["bundle_ai", "bundle_support"]
    assert payload["options"][0]["included_duration_days"] == 14
    assert payload["options"][0]["included_quantity"] == 1


def test_attach_option_to_tariff_is_idempotent_and_updates_metadata(test_settings):
    tariff_service.create_tariff(
        code="attach_plan",
        title="Attach plan",
        price_amount_minor=1000,
        settings=test_settings,
    )
    paid_option_service.create_paid_option(
        code="attach_option",
        title="Attach option",
        price_amount_minor=100,
        settings=test_settings,
    )

    first = tariff_service.attach_option_to_tariff(
        "attach_plan",
        "attach_option",
        included_duration_days=10,
        included_quantity=1,
        settings=test_settings,
    )
    second = tariff_service.attach_option_to_tariff(
        "attach_plan",
        "attach_option",
        data=TariffOptionLinkInput(included_duration_days=30, included_quantity=3),
        settings=test_settings,
    )

    assert first["code"] == "attach_option"
    assert second["included_duration_days"] == 30
    assert second["included_quantity"] == 3
    assert _count(test_settings, "tariff_options") == 1
    row = _tariff_link_row(test_settings, "attach_plan", "attach_option")
    assert row["included_duration_days"] == 30
    assert row["included_quantity"] == 3


def test_update_tariff_option_link_and_detach_work(test_settings):
    tariff_service.create_tariff(
        code="detach_plan",
        title="Detach plan",
        price_amount_minor=1000,
        settings=test_settings,
    )
    paid_option_service.create_paid_option(
        code="detach_option",
        title="Detach option",
        price_amount_minor=100,
        settings=test_settings,
    )
    tariff_service.attach_option_to_tariff("detach_plan", "detach_option", included_duration_days=7, included_quantity=1, settings=test_settings)

    updated = tariff_service.update_tariff_option_link(
        "detach_plan",
        "detach_option",
        data=TariffOptionLinkInput(included_duration_days=21, included_quantity=2),
        settings=test_settings,
    )
    assert updated["included_duration_days"] == 21
    assert updated["included_quantity"] == 2

    assert tariff_service.detach_option_from_tariff("detach_plan", "detach_option", settings=test_settings) is True
    assert tariff_service.detach_option_from_tariff("detach_plan", "detach_option", settings=test_settings) is False
    assert _count(test_settings, "tariff_options") == 0


def test_missing_tariff_option_and_link_errors_are_safe(test_settings):
    tariff_service.create_tariff(
        code="safe_plan",
        title="Safe plan",
        price_amount_minor=1000,
        settings=test_settings,
    )
    paid_option_service.create_paid_option(
        code="safe_option",
        title="Safe option",
        price_amount_minor=100,
        settings=test_settings,
    )

    with pytest.raises(tariff_service.NotFoundError):
        tariff_service.update_tariff("missing_plan", title="x", settings=test_settings)
    with pytest.raises(tariff_service.NotFoundError):
        tariff_service.attach_option_to_tariff("missing_plan", "safe_option", settings=test_settings)
    with pytest.raises(tariff_service.NotFoundError):
        tariff_service.attach_option_to_tariff("safe_plan", "missing_option", settings=test_settings)
    with pytest.raises(tariff_service.NotFoundError):
        tariff_service.update_tariff_option_link("safe_plan", "safe_option", included_quantity=1, settings=test_settings)
    assert tariff_service.detach_option_from_tariff("safe_plan", "safe_option", settings=test_settings) is False


def test_archived_option_cannot_be_attached(test_settings):
    tariff_service.create_tariff(
        code="active_plan",
        title="Active plan",
        price_amount_minor=1000,
        settings=test_settings,
    )
    paid_option_service.create_paid_option(
        code="archived_option",
        title="Archived option",
        price_amount_minor=100,
        status="archived",
        settings=test_settings,
    )

    with pytest.raises(tariff_service.ValidationError):
        tariff_service.attach_option_to_tariff("active_plan", "archived_option", settings=test_settings)


def test_admin_list_helpers_include_hidden_and_archived_rows(test_settings):
    tariff_service.seed_initial_catalog(settings=test_settings)
    tariff_service.create_tariff(
        code="hidden_plan",
        title="Hidden plan",
        price_amount_minor=2000,
        status="hidden",
        settings=test_settings,
    )
    tariff_service.create_tariff(
        code="archived_plan",
        title="Archived plan",
        price_amount_minor=3000,
        status="archived",
        settings=test_settings,
    )
    paid_option_service.create_paid_option(
        code="hidden_option",
        title="Hidden option",
        price_amount_minor=50,
        status="hidden",
        settings=test_settings,
    )
    paid_option_service.create_paid_option(
        code="archived_option_admin",
        title="Archived option admin",
        price_amount_minor=None,
        status="archived",
        settings=test_settings,
    )

    public_tariff_codes = {item.code for item in tariff_service.list_tariffs(settings=test_settings)}
    public_option_codes = {item.code for item in paid_option_service.list_paid_options(settings=test_settings)}
    admin_tariff_codes = {item.code for item in tariff_service.list_tariffs_for_admin(settings=test_settings)}
    admin_option_codes = {item.code for item in paid_option_service.list_paid_options_for_admin(settings=test_settings)}

    assert "hidden_plan" not in public_tariff_codes
    assert "archived_plan" not in public_tariff_codes
    assert "hidden_option" not in public_option_codes
    assert "archived_option_admin" not in public_option_codes
    assert {"hidden_plan", "archived_plan"}.issubset(admin_tariff_codes)
    assert {"hidden_option", "archived_option_admin"}.issubset(admin_option_codes)


def test_create_paid_option_accepts_dataclass_input_and_null_price(test_settings):
    option = paid_option_service.create_paid_option(
        data=PaidOptionCreateInput(
            code="mentor_support",
            title="Mentor support",
            description="Human guidance",
            price_amount_minor=None,
            currency="rub",
            default_duration_days=None,
            status="active",
            is_renewable=True,
            sort_order=7,
        ),
        settings=test_settings,
    )

    assert option.code == "mentor_support"
    assert option.price_amount_minor is None
    assert option.currency == "RUB"
    assert option.default_duration_days is None
    assert option.is_renewable is True


def test_create_paid_option_generates_safe_unique_code_when_blank(test_settings):
    first = paid_option_service.create_paid_option(
        title="Auto option one",
        price_amount_minor=None,
        code=None,
        settings=test_settings,
    )
    second = paid_option_service.create_paid_option(
        title="Auto option two",
        price_amount_minor=100,
        code="",
        settings=test_settings,
    )

    assert first.code.startswith("option_")
    assert second.code.startswith("option_")
    assert re.fullmatch(r"[a-z0-9_-]{3,64}", first.code)
    assert re.fullmatch(r"[a-z0-9_-]{3,64}", second.code)
    assert first.code != second.code


@pytest.mark.parametrize(
    ("kwargs", "error"),
    [
        ({"code": "ab", "title": "Valid title"}, paid_option_service.ValidationError),
        ({"code": "bad code", "title": "Valid title"}, paid_option_service.ValidationError),
        ({"code": "valid_option", "title": "   "}, paid_option_service.ValidationError),
        ({"code": "valid_option", "title": "Valid title", "price_amount_minor": -1}, paid_option_service.ValidationError),
        ({"code": "valid_option", "title": "Valid title", "status": "broken"}, paid_option_service.ValidationError),
    ],
)
def test_create_paid_option_rejects_invalid_inputs(test_settings, kwargs, error):
    with pytest.raises(error):
        paid_option_service.create_paid_option(settings=test_settings, **kwargs)


def test_create_paid_option_rejects_duplicate_code(test_settings):
    paid_option_service.create_paid_option(
        code="dup_option",
        title="Duplicate option",
        price_amount_minor=100,
        settings=test_settings,
    )
    with pytest.raises(paid_option_service.ConflictError):
        paid_option_service.create_paid_option(
            code="dup_option",
            title="Duplicate option again",
            price_amount_minor=200,
            settings=test_settings,
        )


def test_update_paid_option_edits_allowed_fields_and_keeps_code(test_settings):
    created = paid_option_service.create_paid_option(
        code="edit_option",
        title="Edit option",
        price_amount_minor=100,
        settings=test_settings,
    )
    updated = paid_option_service.update_paid_option(
        created.code,
        data=PaidOptionUpdateInput(
            title="Edited option",
            description="Updated description",
            price_amount_minor=250,
            currency="usd",
            default_duration_days=45,
            status="hidden",
            is_renewable=False,
            sort_order=11,
        ),
        settings=test_settings,
    )

    assert updated.code == created.code
    assert updated.title == "Edited option"
    assert updated.description == "Updated description"
    assert updated.price_amount_minor == 250
    assert updated.currency == "USD"
    assert updated.default_duration_days == 45
    assert updated.status == "hidden"
    assert updated.is_renewable is False
    assert updated.sort_order == 11


def test_archive_paid_option_hides_it_from_public_listing_and_admin_listing_keeps_it(test_settings):
    created = paid_option_service.create_paid_option(
        code="archive_option",
        title="Archive option",
        price_amount_minor=100,
        settings=test_settings,
    )

    assert paid_option_service.archive_paid_option(created.code, settings=test_settings) is True
    assert paid_option_service.archive_paid_option(created.code, settings=test_settings) is False

    public_codes = {item.code for item in paid_option_service.list_paid_options(settings=test_settings)}
    admin_codes = {item.code for item in paid_option_service.list_paid_options_for_admin(settings=test_settings)}

    assert created.code not in public_codes
    assert created.code in admin_codes
    archived = paid_option_service.get_paid_option_by_code(created.code, settings=test_settings)
    assert archived is not None and archived.status == "archived"
