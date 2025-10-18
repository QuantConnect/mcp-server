from __future__ import annotations

import os
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator


class Transport(str, Enum):
    """Supported transport identifiers for FastMCP."""

    AUTO = "auto"
    STDIO = "stdio"
    HTTP = "streamable-http"
    SSE = "sse"
    WEBSOCKET = "websocket"
    WS = "ws"
    TCP = "tcp"


NETWORK_TRANSPORTS = {
    Transport.HTTP.value,
    Transport.SSE.value,
    Transport.WEBSOCKET.value,
    Transport.WS.value,
    Transport.TCP.value,
}

DEFAULT_TRANSPORT_PORTS: dict[str, int] = {
    Transport.HTTP.value: 8000,
    Transport.SSE.value: 8000,
    Transport.WEBSOCKET.value: 8765,
    Transport.WS.value: 8765,
    Transport.TCP.value: 8020,
}
DEFAULT_TRANSPORT_HOST = "127.0.0.1"


class ServerSettings(BaseModel):
    """Configuration loaded from environment variables."""

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    quantconnect_user_id: str | None = Field(
        default=None,
        alias="QUANTCONNECT_USER_ID",
        description="QuantConnect account identifier used for API requests.",
    )
    quantconnect_api_token: str | None = Field(
        default=None,
        alias="QUANTCONNECT_API_TOKEN",
        description="QuantConnect API token used for authentication.",
    )
    agent_name: str = Field(
        default="QuantConnect MCP Server",
        alias="AGENT_NAME",
        description="Identifier attached to code modifications made via the MCP.",
    )
    api_base_url: str = Field(
        default="https://www.quantconnect.com/api/v2",
        alias="QUANTCONNECT_API_BASE_URL",
        description="Base URL for the QuantConnect REST API.",
    )
    mount_source_path: str | None = Field(
        default=None,
        alias="MOUNT_SOURCE_PATH",
        description="Host path containing locally synchronized Lean projects.",
    )
    mount_destination_path: str | None = Field(
        default=None,
        alias="MOUNT_DST_PATH",
        description="Container path where Lean projects are mounted.",
    )
    transport: Transport = Field(
        default=Transport.STDIO,
        alias="MCP_TRANSPORT",
        description="FastMCP transport. Supports stdio, http, websocket, tcp, or auto.",
    )
    api_timeout: float = Field(
        default=30.0,
        alias="QUANTCONNECT_API_TIMEOUT",
        ge=0.0,
        description="Default timeout (seconds) for QuantConnect API requests.",
    )
    transport_host: str | None = Field(
        default=None,
        alias="MCP_HOST",
        description="Host/interface binding for network transports.",
    )
    transport_port: int | None = Field(
        default=None,
        alias="MCP_PORT",
        description="Port binding for network transports.",
    )
    log_level: str | None = Field(
        default=None,
        alias="MCP_LOG_LEVEL",
        description="Optional log level override for FastMCP run() helpers.",
    )

    def ensure_credentials(self) -> tuple[str, str]:
        """Ensure that the credentials required for API calls are available."""

        missing = [
            name
            for name, value in (
                ("QUANTCONNECT_USER_ID", self.quantconnect_user_id),
                ("QUANTCONNECT_API_TOKEN", self.quantconnect_api_token),
            )
            if not value
        ]
        if missing:
            message = (
                "Missing required QuantConnect credentials. "
                f"Set the environment variable(s): {', '.join(missing)}."
            )
            raise RuntimeError(message)
        # The casts are safe because the missing list is empty.
        return self.quantconnect_user_id, self.quantconnect_api_token  # type: ignore[return-value]

    @staticmethod
    def _safe_path(path_value: str | None) -> Path | None:
        if not path_value:
            return None
        candidate = Path(path_value).expanduser()
        try:
            return candidate.resolve()
        except (OSError, RuntimeError) as exc:
            raise RuntimeError(f"Failed to resolve path '{path_value}': {exc}") from exc

    @property
    def mount_source(self) -> Path | None:
        """Return the resolved mount source path if configured."""

        return self._safe_path(self.mount_source_path)

    @property
    def mount_destination(self) -> Path | None:
        """Return the resolved mount destination path if configured."""

        return self._safe_path(self.mount_destination_path)

    @staticmethod
    def _normalize_transport(value: Transport | str | None) -> Transport | None:
        if value is None or value == "":
            return None
        if isinstance(value, Transport):
            return value
        normalized_value = value.lower()
        alias_map = {
            "http": Transport.HTTP,
            "streamable-http": Transport.HTTP,
            "streamablehttp": Transport.HTTP,
        }
        if normalized_value in alias_map:
            return alias_map[normalized_value]
        try:
            return Transport(normalized_value)
        except ValueError as exc:
            valid = ", ".join(t.value for t in Transport)
            raise RuntimeError(f"Unsupported transport '{value}'. Expected one of {valid}.") from exc

    @field_validator("transport", mode="before")
    @classmethod
    def _coerce_transport(cls, value: Transport | str | None) -> Transport:
        normalized = cls._normalize_transport(value)
        return normalized or Transport.STDIO

    def transport_kwargs(self, transport: str | None = None) -> dict[str, Any]:
        """Return keyword arguments to forward to FastMCP.run based on transport."""

        selected_transport = self._normalize_transport(transport) or self.transport
        kwargs: dict[str, Any] = {}
        if selected_transport.value in NETWORK_TRANSPORTS:
            kwargs["host"] = self.transport_host or DEFAULT_TRANSPORT_HOST
            kwargs["port"] = self.transport_port or DEFAULT_TRANSPORT_PORTS.get(
                selected_transport.value, DEFAULT_TRANSPORT_PORTS[Transport.HTTP.value]
            )
        if self.log_level:
            kwargs["log_level"] = self.log_level
        return kwargs


def _load_raw_environment(env: Mapping[str, str] | None = None) -> Mapping[str, str]:
    if env is not None:
        return env
    # Casting to Mapping ensures type checkers do not treat os._Environ as mutable.
    return os.environ


def resolve_settings(
    *, env: Mapping[str, str] | None = None, require_credentials: bool = False
) -> ServerSettings:
    """Instantiate ServerSettings from environment variables."""

    raw_env = _load_raw_environment(env)
    try:
        settings = ServerSettings.model_validate(raw_env)
    except ValidationError as exc:
        raise RuntimeError(f"Failed to parse server settings: {exc}") from exc

    if require_credentials:
        settings.ensure_credentials()
    return settings


@lru_cache(maxsize=1)
def _cached_settings(require_credentials: bool) -> ServerSettings:
    return resolve_settings(require_credentials=require_credentials)


def get_settings(
    *, require_credentials: bool = False, refresh: bool = False
) -> ServerSettings:
    """Cached accessor for server settings.

    Use `refresh=True` or :func:`clear_settings_cache` to reload configuration.
    """

    if refresh:
        clear_settings_cache()
    return _cached_settings(require_credentials)


def clear_settings_cache() -> None:
    """Reset the cached ServerSettings instance."""

    _cached_settings.cache_clear()
