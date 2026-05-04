from app.main import app


def test_expected_routes_registered():
    paths = {route.path for route in app.routes}
    assert "/healthz" in paths
    assert "/readyz" in paths
    assert "/" in paths
    assert "/login" in paths
    assert "/register" in paths
    assert "/logout" in paths
    assert "/cabinet" in paths


def test_app_entrypoint_is_composition_only():
    import app.main as app_main

    assert hasattr(app_main, "app")
    assert app_main.app.title == "AI Starter Community"
