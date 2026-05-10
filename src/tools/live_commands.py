from __future__ import annotations

from api_connection import post
from models import BroadcastLiveCommandRequest, CreateLiveCommandRequest, RestResponse
from mcp.server.fastmcp import FastMCP


def register_live_trading_command_tools(mcp: FastMCP) -> None:
    """Expose live command broadcast helpers."""

    @mcp.tool(annotations={"title": "Create live command"})
    async def create_live_command(model: CreateLiveCommandRequest) -> RestResponse:
        """Send a command to a specific live deployment."""

        return await post("/live/commands/create", model)

    @mcp.tool(annotations={"title": "Broadcast live command"})
    async def broadcast_live_command(
        model: BroadcastLiveCommandRequest,
    ) -> RestResponse:
        """Broadcast a live command to every deployment in the organization."""

        return await post("/live/commands/broadcast", model)
