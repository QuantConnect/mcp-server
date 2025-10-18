import main
import pytest

from settings import get_settings


@pytest.fixture(autouse=True)
def _reset_settings(monkeypatch):
    """Ensure cached settings do not leak between tests."""

    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def test_run_server_overrides_transport(monkeypatch):
    monkeypatch.setenv("MCP_TRANSPORT", "auto")
    recorded = {}

    class DummyServer:
        def run(self, *, transport, **kwargs):
            recorded["transport"] = transport
            recorded["kwargs"] = kwargs

    monkeypatch.setattr(main, "mcp", DummyServer())

    main.run_server(
        transport="http",
        host="1.2.3.4",
        port=9000,
        log_level="DEBUG",
    )

    assert recorded["transport"] == "http"
    assert recorded["kwargs"]["host"] == "1.2.3.4"
    assert recorded["kwargs"]["port"] == 9000
    assert recorded["kwargs"]["log_level"] == "DEBUG"


def test_cli_lists_transports(monkeypatch, capsys):
    monkeypatch.setenv("MCP_TRANSPORT", "stdio")
    main.cli(["--list-transports"])
    captured = capsys.readouterr()
    assert "Available transports" in captured.out


def test_cli_invokes_run_server(monkeypatch):
    recorded = {}

    def fake_run_server(**kwargs):
        recorded.update(kwargs)

    monkeypatch.setenv("MCP_TRANSPORT", "stdio")
    monkeypatch.setattr(main, "run_server", fake_run_server)

    main.cli(["--transport", "stdio", "--log-level", "ERROR"])

    assert recorded["transport"] == "stdio"
    assert recorded["log_level"] == "ERROR"
