from __future__ import annotations

from api_connection import post
from models import (
    CreateCompileRequest,
    CreateCompileResponse,
    ReadCompileRequest,
    ReadCompileResponse,
)
from mcp.server.fastmcp import FastMCP


def register_compile_tools(mcp: FastMCP) -> None:
    """Expose Lean compilation helpers."""

    @mcp.tool(annotations={"title": "Create compile", "destructiveHint": False})
    async def create_compile(
        model: CreateCompileRequest,
    ) -> CreateCompileResponse:
        """Submit an asynchronous compile request."""

        return await post("/compile/create", model)

    @mcp.tool(annotations={"title": "Read compile", "readOnlyHint": True})
    async def read_compile(model: ReadCompileRequest) -> ReadCompileResponse:
        """Retrieve the status of a compile request."""

        return await post("/compile/read", model)
