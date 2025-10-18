from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from mcp.server.fastmcp import FastMCP

from organization_workspace import OrganizationWorkspace
from settings import NETWORK_TRANSPORTS, Transport, get_settings
from tools import register_all_tools

__all__ = ["create_server", "run_server", "cli", "main", "mcp"]


def _load_instructions() -> str:
    """Read the user-facing instructions bundled with the server."""

    instructions_path = Path(__file__).with_name("instructions.md")
    return instructions_path.read_text(encoding="utf-8")


def create_server() -> FastMCP:
    """Instantiate the FastMCP server with all registered tools."""

    mcp = FastMCP(name="quantconnect", instructions=_load_instructions())
    register_all_tools(mcp)
    return mcp


mcp = create_server()


AVAILABLE_TRANSPORTS = tuple(
    sorted({Transport.AUTO.value, Transport.STDIO.value, *NETWORK_TRANSPORTS})
)


def run_server(
    *,
    transport: str | None = None,
    host: str | None = None,
    port: int | None = None,
    log_level: str | None = None,
) -> None:
    """Run the MCP server with the provided transport configuration."""

    settings = get_settings()
    OrganizationWorkspace.load(settings)
    selected_transport_enum = settings._normalize_transport(transport) or settings.transport
    selected_transport_value = selected_transport_enum.value
    run_kwargs = settings.transport_kwargs(selected_transport_value)
    if selected_transport_value not in NETWORK_TRANSPORTS:
        run_kwargs.pop("host", None)
        run_kwargs.pop("port", None)
    if host is not None:
        run_kwargs["host"] = host
    if port is not None:
        run_kwargs["port"] = port
    if log_level is not None:
        run_kwargs["log_level"] = log_level

    mcp.run(transport=selected_transport_value, **run_kwargs)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="QuantConnect MCP server powered by FastMCP."
    )
    parser.add_argument(
        "--transport",
        choices=AVAILABLE_TRANSPORTS,
        help="Transport to use when serving MCP (default: value from MCP_TRANSPORT).",
    )
    parser.add_argument(
        "--host",
        help="Host/interface to bind for network transports.",
    )
    parser.add_argument(
        "--port",
        type=int,
        help="Port to bind for network transports.",
    )
    parser.add_argument(
        "--log-level",
        help="Override FastMCP log level for this run.",
    )
    parser.add_argument(
        "--list-transports",
        action="store_true",
        help="List supported transports and exit.",
    )
    return parser


def cli(argv: Sequence[str] | None = None) -> None:
    """Command-line interface for running the MCP server."""

    parser = _build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.list_transports:
        print("Available transports:", ", ".join(AVAILABLE_TRANSPORTS))
        return

    run_server(
        transport=args.transport,
        host=args.host,
        port=args.port,
        log_level=args.log_level,
    )


def main() -> None:
    """Default entry-point used by legacy invocations."""

    run_server()


if __name__ == "__main__":
    cli(sys.argv[1:])
