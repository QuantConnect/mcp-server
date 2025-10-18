from __future__ import annotations

from base64 import b64encode
from contextlib import asynccontextmanager
from hashlib import sha256
from time import time
from typing import Any, AsyncIterator

import httpx
from pydantic_core import to_jsonable_python

from __init__ import __version__  # type: ignore import-not-found
from settings import get_settings


def _format_endpoint(endpoint: str) -> str:
    """Return a normalized API endpoint path."""

    return endpoint if endpoint.startswith("/") else f"/{endpoint}"


def _build_headers(user_id: str, api_token: str) -> dict[str, str]:
    """Create the QuantConnect authentication headers."""

    timestamp = str(int(time()))
    hashed_token = sha256(f"{api_token}:{timestamp}".encode("utf-8")).hexdigest()
    authentication = b64encode(f"{user_id}:{hashed_token}".encode("utf-8")).decode("ascii")
    return {
        "Authorization": f"Basic {authentication}",
        "Timestamp": timestamp,
        "User-Agent": f"QuantConnect MCP Server v{__version__}",
    }


def _serialize_payload(model: object | None) -> dict[str, Any]:
    """Convert request models to JSON-compatible dictionaries."""

    if model is None:
        return {}
    return to_jsonable_python(model, exclude_none=True)


@asynccontextmanager
async def authenticated_client(
    *, follow_redirects: bool = False
) -> AsyncIterator[tuple[httpx.AsyncClient, dict[str, str]]]:
    """Yield an authenticated AsyncClient instance with QuantConnect headers."""

    settings = get_settings(require_credentials=True)
    user_id, api_token = settings.ensure_credentials()
    headers = _build_headers(user_id, api_token)
    async with httpx.AsyncClient(
        base_url=settings.api_base_url.rstrip("/"),
        follow_redirects=follow_redirects,
    ) as client:
        yield client, headers


async def post_raw(
    endpoint: str,
    model: object = None,
    timeout: float = 30.0,
    *,
    follow_redirects: bool = False,
) -> httpx.Response:
    """Perform a POST request and return the raw httpx response."""

    async with authenticated_client(
        follow_redirects=follow_redirects
    ) as (client, headers):
        response = await client.post(
            _format_endpoint(endpoint),
            headers=headers,
            json=_serialize_payload(model),
            timeout=timeout,
        )
        response.raise_for_status()
        return response


async def post(endpoint: str, model: object = None, timeout: float = 30.0):
    """Make an HTTP POST request to the API with proper error handling."""

    response = await post_raw(endpoint, model=model, timeout=timeout)
    return response.json()
