import os
from mcp.server.fastmcp import FastMCP

from tools.account import register_account_tools
from tools.project import register_project_tools
from tools.project_collaboration import register_project_collaboration_tools
from tools.project_nodes import register_project_node_tools
from tools.compile import register_compile_tools
from tools.files import register_file_tools
from tools.backtests import register_backtest_tools
from tools.optimizations import register_optimization_tools
from tools.live import register_live_trading_tools
from tools.live_commands import register_live_trading_command_tools
from tools.object_store import register_object_store_tools
from tools.lean_versions import register_lean_version_tools
from tools.ai import register_ai_tools
from tools.mcp_server_version import register_mcp_server_version_tools

transport = os.getenv('MCP_TRANSPORT', 'stdio')

# Load the server instructions.
with open('src/instructions.md', 'r', encoding='utf-8') as file:
    instructions = file.read()
# Initialize the FastMCP server.
mcp = FastMCP('quantconnect', instructions, host="0.0.0.0")

# Register all the tools.
registration_functions = [
    register_account_tools,
    register_project_tools,
    register_project_collaboration_tools,
    register_project_node_tools,
    register_compile_tools,
    register_file_tools,
    register_backtest_tools,
    register_optimization_tools,
    register_live_trading_tools,
    register_live_trading_command_tools,
    register_object_store_tools,
    register_lean_version_tools,
    register_ai_tools,
    register_mcp_server_version_tools,
]
for f in registration_functions:
    f(mcp)

# Temporary shim to normalize tool input schemas for Codex/Anthropic
async def _list_tools_with_shim():
    tools = await original_list_tools()
    for tool in tools:
        schema = tool.inputSchema or {"type": "object", "properties": {}}
        if schema.get("properties") and list(schema["properties"].keys()) == ["args"]:
            schema = schema["properties"]["args"]
        schema.setdefault("type", "object")
        schema.setdefault("additionalProperties", False)

        def _fix(node):
            if isinstance(node, dict):
                if node.get("type") == "integer":
                    node["type"] = "number"
                for v in node.values():
                    _fix(v)
            elif isinstance(node, list):
                for v in node:
                    _fix(v)

        _fix(schema)
        tool.inputSchema = schema
    return tools

original_list_tools = mcp.list_tools
mcp.list_tools = _list_tools_with_shim

if __name__ == "__main__":
    # Run the server.
    mcp.run(transport=transport)
