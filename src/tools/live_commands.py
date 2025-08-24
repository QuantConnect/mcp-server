from api_connection import post
from models import (
    CreateLiveCommandRequest,
    BroadcastLiveCommandRequest,
    RestResponse
)
from tool_args import tool_with_args

def register_live_trading_command_tools(mcp):
    # Create (singular algorithm)
    @tool_with_args(
        mcp,
        CreateLiveCommandRequest,
        annotations={'title': 'Create live command'}
    )
    async def create_live_command(
            model: CreateLiveCommandRequest) -> RestResponse:
        """Send a command to a live trading algorithm."""
        return await post('/live/commands/create', model)

    # Create (multiple algorithms) - Broadcast
    @tool_with_args(
        mcp,
        BroadcastLiveCommandRequest,
        annotations={'title': 'Broadcast live command'}
    )
    async def broadcast_live_command(
            model: BroadcastLiveCommandRequest) -> RestResponse:
        """Broadcast a live command to all live algorithms in an 
        organization."""
        return await post('/live/commands/broadcast', model)
