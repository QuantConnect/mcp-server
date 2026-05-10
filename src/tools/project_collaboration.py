from __future__ import annotations

from api_connection import post
from code_source_id import add_code_source_id
from models import (
    CreateCollaboratorRequest,
    CreateCollaboratorResponse,
    DeleteCollaboratorRequest,
    DeleteCollaboratorResponse,
    LockCollaboratorRequest,
    ReadCollaboratorsRequest,
    ReadCollaboratorsResponse,
    RestResponse,
    UpdateCollaboratorRequest,
    UpdateCollaboratorResponse,
)
from mcp.server.fastmcp import FastMCP


def register_project_collaboration_tools(mcp: FastMCP) -> None:
    """Expose collaboration management helpers."""

    @mcp.tool(
        annotations={
            "title": "Create project collaborator",
            "destructiveHint": False,
            "idempotentHint": True,
        }
    )
    async def create_project_collaborator(
        model: CreateCollaboratorRequest,
    ) -> CreateCollaboratorResponse:
        """Add a collaborator to a project."""

        return await post("/projects/collaboration/create", model)

    @mcp.tool(
        annotations={
            "title": "Read project collaborators",
            "readOnlyHint": True,
        }
    )
    async def read_project_collaborators(
        model: ReadCollaboratorsRequest,
    ) -> ReadCollaboratorsResponse:
        """List collaborators for a given project."""

        return await post("/projects/collaboration/read", model)

    @mcp.tool(
        annotations={
            "title": "Update project collaborator",
            "idempotentHint": True,
        }
    )
    async def update_project_collaborator(
        model: UpdateCollaboratorRequest,
    ) -> UpdateCollaboratorResponse:
        """Update project collaborator permissions."""

        return await post("/projects/collaboration/update", model)

    @mcp.tool(
        annotations={
            "title": "Delete project collaborator",
            "idempotentHint": True,
        }
    )
    async def delete_project_collaborator(
        model: DeleteCollaboratorRequest,
    ) -> DeleteCollaboratorResponse:
        """Remove a collaborator from a project."""

        return await post("/projects/collaboration/delete", model)

    @mcp.tool(
        annotations={
            "title": "Lock project with collaborators",
            "idempotentHint": True,
        }
    )
    async def lock_project_with_collaborators(
        model: LockCollaboratorRequest,
    ) -> RestResponse:
        """Acquire a collaboration lock before editing project files."""

        return await post(
            "/projects/collaboration/lock/acquire", add_code_source_id(model)
        )
