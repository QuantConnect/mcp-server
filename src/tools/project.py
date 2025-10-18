from __future__ import annotations

from api_connection import post
from models import (
    CreateProjectRequest,
    DeleteProjectRequest,
    ProjectListResponse,
    ReadProjectRequest,
    RestResponse,
    UpdateProjectRequest,
)
from mcp.server.fastmcp import FastMCP


def register_project_tools(mcp: FastMCP) -> None:
    """Expose project management helpers."""

    @mcp.tool(
        annotations={
            "title": "Create project",
            "destructiveHint": False,
            "idempotentHint": False,
        }
    )
    async def create_project(model: CreateProjectRequest) -> ProjectListResponse:
        """Create a new project in the default organization."""

        return await post("/projects/create", model)

    @mcp.tool(annotations={"title": "Read project", "readOnlyHint": True})
    async def read_project(model: ReadProjectRequest) -> ProjectListResponse:
        """Return information for a specific project or recent projects."""

        return await post("/projects/read", model)

    @mcp.tool(annotations={"title": "List projects", "readOnlyHint": True})
    async def list_projects() -> ProjectListResponse:
        """List all projects in the organization."""

        return await post("/projects/read")

    @mcp.tool(annotations={"title": "Update project", "idempotentHint": True})
    async def update_project(model: UpdateProjectRequest) -> RestResponse:
        """Update a project's name or description."""

        return await post("/projects/update", model)

    @mcp.tool(annotations={"title": "Delete project", "idempotentHint": True})
    async def delete_project(model: DeleteProjectRequest) -> RestResponse:
        """Delete a project."""

        return await post("/projects/delete", model)
