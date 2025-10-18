from __future__ import annotations

import httpx

from mcp.server.fastmcp import FastMCP
from version import __version__

DOCKER_TAGS_URL = (
    "https://hub.docker.com/v2/namespaces/quantconnect/repositories/mcp-server/tags"
)


def register_mcp_server_version_tools(mcp: FastMCP) -> None:
    """Expose utilities for inspecting server versions."""

    @mcp.tool(
        annotations={"title": "Read QC MCP Server version", "readOnlyHint": True}
    )
    async def read_mcp_server_version() -> str:
        """Return the version of the currently running MCP server."""

        return __version__

    @mcp.tool(
        annotations={
            "title": "Read latest QC MCP Server version",
            "readOnlyHint": True,
        }
    )
    async def read_latest_mcp_server_version() -> str:
        """Return the latest published version of the MCP server."""

        async with httpx.AsyncClient() as client:
            response = await client.get(DOCKER_TAGS_URL, params={"page_size": 5})
            response.raise_for_status()
        for tag in response.json().get("results", []):
            name = tag.get("name")
            if name and name != "latest":
                return name
        raise RuntimeError("No version tags returned by Docker Hub.")
