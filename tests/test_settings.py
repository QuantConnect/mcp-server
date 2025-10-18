from settings import DEFAULT_TRANSPORT_HOST, DEFAULT_TRANSPORT_PORTS, resolve_settings
import pytest


def test_transport_kwargs_default_log_level():
    settings = resolve_settings(env={"MCP_TRANSPORT": "stdio", "MCP_LOG_LEVEL": "DEBUG"})
    assert settings.transport == "stdio"
    assert settings.transport_kwargs() == {"log_level": "DEBUG"}


def test_transport_kwargs_for_network_transport():
    settings = resolve_settings(env={"MCP_TRANSPORT": "auto"})
    kwargs = settings.transport_kwargs("http")
    assert kwargs["host"] == DEFAULT_TRANSPORT_HOST
    assert kwargs["port"] == DEFAULT_TRANSPORT_PORTS["http"]


def test_ensure_credentials_raises_when_missing():
    settings = resolve_settings(env={})
    with pytest.raises(RuntimeError):
        settings.ensure_credentials()
