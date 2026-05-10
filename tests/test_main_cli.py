import main
import pytest

from settings import clear_settings_cache


@pytest.fixture(autouse=True)
def _reset_settings():
    """Ensure cached settings do not leak between tests."""

    clear_settings_cache()
    yield
    clear_settings_cache()


def test_run_server_overrides_transport(monkeypatch):
    monkeypatch.setenv("MCP_TRANSPORT", "auto")
    recorded = {}

    class DummySettings:
        def __init__(self):
            self.host = None
            self.port = None
            self.log_level = None

    class DummyServer:
        def __init__(self):
            self.settings = DummySettings()

        def run(self, *, transport, **kwargs):
            recorded["transport"] = transport
            recorded["kwargs"] = kwargs
            recorded["settings"] = self.settings

    monkeypatch.setattr(main, "mcp", DummyServer())

    main.run_server(
        transport="http",
        host="1.2.3.4",
        port=9000,
        log_level="DEBUG",
    )

    assert recorded["transport"] == "streamable-http"
    assert recorded["kwargs"] == {}
    assert recorded["settings"].host == "1.2.3.4"
    assert recorded["settings"].port == 9000
    assert recorded["settings"].log_level == "DEBUG"


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
