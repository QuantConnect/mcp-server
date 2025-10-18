from __future__ import annotations

from api_connection import post
from models import ProjectNodesResponse, ReadProjectNodesRequest, UpdateProjectNodesRequest
from mcp.server.fastmcp import FastMCP


def register_project_node_tools(mcp: FastMCP) -> None:
    """Expose endpoints for managing project compute nodes."""

    @mcp.tool(annotations={"title": "Read project nodes", "readOnlyHint": True})
    async def read_project_nodes(
        model: ReadProjectNodesRequest,
    ) -> ProjectNodesResponse:
        """Read the available and selected nodes of a project."""

        return await post("/projects/nodes/read", model)

    @mcp.tool(
        annotations={
            "title": "Update project nodes",
            "destructiveHint": False,
            "idempotentHint": True,
        }
    )
    async def update_project_nodes(
        model: UpdateProjectNodesRequest,
    ) -> ProjectNodesResponse:
        """Activate specific project nodes or fall back to auto-selection."""

        return await post("/projects/nodes/update", model)
