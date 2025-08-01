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

# Initialize the FastMCP server.
mcp = FastMCP('quantconnect', version='0.1.0')

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
]
for f in registration_functions:
    f(mcp)

if __name__ == "__main__":
    # Run the server.
    mcp.run(transport='stdio')
