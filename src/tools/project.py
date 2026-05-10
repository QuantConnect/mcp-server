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


def _normalize_parameters(payload: dict) -> dict:
    """QuantConnect returns [] for parameter sets; normalize to empty dicts."""

    projects = payload.get("projects")
    if isinstance(projects, list):
        for project in projects:
            parameters = project.get("parameters")
            if parameters == []:
                project["parameters"] = {}
    return payload


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

        payload = await post("/projects/create", model)
        return _normalize_parameters(payload)

    @mcp.tool(annotations={"title": "Read project", "readOnlyHint": True})
    async def read_project(model: ReadProjectRequest) -> ProjectListResponse:
        """Return information for a specific project or recent projects."""

        payload = await post("/projects/read", model)
        return _normalize_parameters(payload)

    @mcp.tool(annotations={"title": "List projects", "readOnlyHint": True})
    async def list_projects() -> ProjectListResponse:
        """List all projects in the organization."""

        payload = await post("/projects/read")
        return _normalize_parameters(payload)

    @mcp.tool(annotations={"title": "Update project", "idempotentHint": True})
    async def update_project(model: UpdateProjectRequest) -> RestResponse:
        """Update a project's name or description."""

        return await post("/projects/update", model)

    @mcp.tool(annotations={"title": "Delete project", "idempotentHint": True})
    async def delete_project(model: DeleteProjectRequest) -> RestResponse:
        """Delete a project."""

        return await post("/projects/delete", model)
