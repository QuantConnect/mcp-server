from __future__ import annotations

from api_connection import post
from models import LeanVersionsResponse
from mcp.server.fastmcp import FastMCP


def register_lean_version_tools(mcp: FastMCP) -> None:
    """Expose Lean version discovery tooling."""

    @mcp.tool(annotations={"title": "Read LEAN versions", "readOnlyHint": True})
    async def read_lean_versions() -> LeanVersionsResponse:
        """Return the list of Lean versions with metadata."""

        return await post("/lean/versions/read")
