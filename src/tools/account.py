from api_connection import post
from models import AccountResponse
from tool_args import tool_with_args

def register_account_tools(mcp):
    # Read
    @tool_with_args(
        mcp,
        annotations={
            'title': 'Read account',
            'readOnlyHint': True,
            'openWorldHint': True
        }
    )
    async def read_account() -> AccountResponse:
        """Read the organization account status."""
        return await post('/account/read')
