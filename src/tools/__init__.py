from __future__ import annotations

from collections.abc import Callable
from typing import Tuple

from mcp.server.fastmcp import FastMCP

from .account import register_account_tools
from .ai import register_ai_tools
from .backtests import register_backtest_tools
from .compile import register_compile_tools
from .files import register_file_tools
from .lean_versions import register_lean_version_tools
from .live import register_live_trading_tools
from .live_commands import register_live_trading_command_tools
from .mcp_server_version import register_mcp_server_version_tools
from .object_store import register_object_store_tools
from .optimizations import register_optimization_tools
from .project import register_project_tools
from .project_collaboration import register_project_collaboration_tools
from .project_nodes import register_project_node_tools

RegistrationFn = Callable[[FastMCP], None]

REGISTRATION_FUNCTIONS: Tuple[RegistrationFn, ...] = (
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
)


def register_all_tools(mcp: FastMCP) -> None:
    """Register every tool exposed by the QuantConnect MCP server."""

    for register in REGISTRATION_FUNCTIONS:
        register(mcp)
