import pytest
from settings import (
    DEFAULT_TRANSPORT_HOST,
    DEFAULT_TRANSPORT_PORTS,
    Transport,
    clear_settings_cache,
    get_settings,
    resolve_settings,
)


def test_transport_kwargs_default_log_level():
    settings = resolve_settings(env={"MCP_TRANSPORT": "stdio", "MCP_LOG_LEVEL": "DEBUG"})
    assert settings.transport is Transport.STDIO
    assert settings.transport_kwargs() == {"log_level": "DEBUG"}


def test_transport_kwargs_for_network_transport():
    settings = resolve_settings(env={"MCP_TRANSPORT": "auto"})
    kwargs = settings.transport_kwargs("http")
    assert kwargs["host"] == DEFAULT_TRANSPORT_HOST
    assert kwargs["port"] == DEFAULT_TRANSPORT_PORTS[Transport.HTTP.value]


def test_ensure_credentials_raises_when_missing():
    settings = resolve_settings(env={})
    with pytest.raises(RuntimeError):
        settings.ensure_credentials()


def test_invalid_transport_raises_runtime():
    with pytest.raises(RuntimeError):
        resolve_settings(env={"MCP_TRANSPORT": "invalid"})


def test_mount_source_path_resolution_handles_errors(monkeypatch):
    class DummyPath:
        def __init__(self):
            self._called = False

        def expanduser(self):
            return self

        def resolve(self):
            raise OSError("boom")

    monkeypatch.setattr("settings.Path", lambda *_args, **_kwargs: DummyPath())
    settings = resolve_settings(env={"MOUNT_SOURCE_PATH": "/bad/path"})
    with pytest.raises(RuntimeError):
        _ = settings.mount_source


def test_clear_settings_cache():
    clear_settings_cache()
    first = get_settings()
    second = get_settings()
    assert first is second
    clear_settings_cache()
    third = get_settings()
    assert third is not first
