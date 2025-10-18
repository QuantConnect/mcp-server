from __future__ import annotations

from api_connection import post
from code_source_id import add_code_source_id
from models import (
    CreateProjectFileRequest,
    DeleteFileRequest,
    PatchFileRequest,
    ProjectFilesResponse,
    ReadFilesRequest,
    RestResponse,
    UpdateFileContentsRequest,
    UpdateFileNameRequest,
)
from mcp.server.fastmcp import FastMCP


def register_file_tools(mcp: FastMCP) -> None:
    """Expose project file management operations."""

    @mcp.tool(
        annotations={
            "title": "Create file",
            "destructiveHint": False,
            "idempotentHint": True,
        }
    )
    async def create_file(model: CreateProjectFileRequest) -> RestResponse:
        """Add a file to a given project."""

        return await post("/files/create", add_code_source_id(model))

    @mcp.tool(annotations={"title": "Read file", "readOnlyHint": True})
    async def read_file(model: ReadFilesRequest) -> ProjectFilesResponse:
        """Read a file or enumerate all files within a project."""

        return await post("/files/read", add_code_source_id(model))

    @mcp.tool(annotations={"title": "Update file name", "idempotentHint": True})
    async def update_file_name(model: UpdateFileNameRequest) -> RestResponse:
        """Rename a project file."""

        return await post("/files/update", add_code_source_id(model))

    @mcp.tool(annotations={"title": "Update file contents", "idempotentHint": True})
    async def update_file_contents(
        model: UpdateFileContentsRequest,
    ) -> ProjectFilesResponse:
        """Replace the contents of an existing file."""

        return await post("/files/update", add_code_source_id(model))

    @mcp.tool(annotations={"title": "Patch file", "idempotentHint": True})
    async def patch_file(model: PatchFileRequest) -> RestResponse:
        """Apply a unified-diff patch to a file."""

        return await post("/files/patch", add_code_source_id(model))

    @mcp.tool(annotations={"title": "Delete file", "idempotentHint": True})
    async def delete_file(model: DeleteFileRequest) -> RestResponse:
        """Delete a file from a project."""

        return await post("/files/delete", add_code_source_id(model))
