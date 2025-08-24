import asyncio
import pytest

from main import mcp


def _has_integer_type(node):
    if isinstance(node, dict):
        if node.get("type") == "integer":
            return True
        return any(_has_integer_type(v) for v in node.values())
    if isinstance(node, list):
        return any(_has_integer_type(v) for v in node)
    return False


@pytest.mark.asyncio
async def test_all_tool_schemas_are_objects():
    tools = await mcp.list_tools()
    for tool in tools:
        schema = tool.inputSchema or {}
        assert schema.get("type") == "object"
        assert schema.get("additionalProperties") is False
        assert not _has_integer_type(schema)
