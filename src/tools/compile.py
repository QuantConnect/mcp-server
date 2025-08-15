from api_connection import post
from models import (
    CreateCompileRequest,
    ReadCompileRequest,
    CreateCompileResponse,
    ReadCompileResponse
)
from tool_args import tool_with_args

def register_compile_tools(mcp):
    # Create
    @tool_with_args(
        mcp,
        CreateCompileRequest,
        annotations={'title': 'Create compile', 'destructiveHint': False}
    )
    async def create_compile(
            model: CreateCompileRequest) -> CreateCompileResponse:
        """Asynchronously create a compile job request for a project."""
        return await post('/compile/create', model)

    # Read
    @tool_with_args(
        mcp,
        ReadCompileRequest,
        annotations={'title': 'Read compile', 'readOnlyHint': True}
    )
    async def read_compile(model: ReadCompileRequest) -> ReadCompileResponse:
        """Read a compile packet job result."""
        return await post('/compile/read', model)
