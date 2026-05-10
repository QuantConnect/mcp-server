from __future__ import annotations

from api_connection import post
from models import AccountResponse
from mcp.server.fastmcp import FastMCP


def register_account_tools(mcp: FastMCP) -> None:
    """Expose account-related MCP tooling."""

    @mcp.tool(
        annotations={
            "title": "Read account",
            "readOnlyHint": True,
            "openWorldHint": True,
        }
    )
    async def read_account() -> AccountResponse:
        """Read the organization account status."""

        return await post("/account/read")
