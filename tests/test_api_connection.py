import httpx
import pytest

from api_connection import post
from settings import clear_settings_cache, get_settings


@pytest.fixture(autouse=True)
def _configure_env(monkeypatch):
    monkeypatch.setenv("QUANTCONNECT_USER_ID", "1")
    monkeypatch.setenv("QUANTCONNECT_API_TOKEN", "token")
    monkeypatch.setenv("QUANTCONNECT_API_TIMEOUT", "12.5")
    clear_settings_cache()
    yield
    clear_settings_cache()


@pytest.mark.asyncio
async def test_post_uses_default_timeout(monkeypatch):
    settings = get_settings(require_credentials=True)
    captured = {}

    async def fake_post(self, path, **kwargs):
        captured["timeout"] = kwargs.get("timeout")

        class DummyResponse:
            def raise_for_status(self):
                return None

            def json(self):
                return {"success": True}

        return DummyResponse()

    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post, raising=False)
    response = await post("/projects/read")
    assert response == {"success": True}
    assert captured["timeout"] == settings.api_timeout


@pytest.mark.asyncio
async def test_post_wraps_http_errors(monkeypatch):
    async def fake_post(self, path, **kwargs):
        raise httpx.ConnectError("boom", request=httpx.Request("POST", "https://example.com"))

    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post, raising=False)

    with pytest.raises(RuntimeError) as excinfo:
        await post("/broken")
    assert "QuantConnect API request failed" in str(excinfo.value)
