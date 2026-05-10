from api_connection import post
from code_source_id import add_code_source_id
from models import (
    CreateProjectFileRequest,
    ReadFilesRequest,
    UpdateFileNameRequest,
    UpdateFileContentsRequest,
    PatchFileRequest,
    DeleteFileRequest,
    RestResponse,
    ProjectFilesResponse
)
from tool_args import tool_with_args


def register_file_tools(mcp):
    # Create
    @tool_with_args(
        mcp,
        CreateProjectFileRequest,
        annotations={
            'title': 'Create file',
            'destructiveHint': False,
            'idempotentHint': True
        }
    )
    async def create_file(
            model: CreateProjectFileRequest) -> RestResponse:
        """Add a file to a given project."""
        return await post('/files/create', add_code_source_id(model))

    # Read
    @tool_with_args(
        mcp,
        ReadFilesRequest,
        annotations={'title': 'Read file', 'readOnlyHint': True}
    )
    async def read_file(model: ReadFilesRequest) -> ProjectFilesResponse:
        """Read a file from a project, or all files in the project if 
        no file name is provided.
        """
        return await post('/files/read', add_code_source_id(model))
    
    # Update name
    @tool_with_args(
        mcp,
        UpdateFileNameRequest,
        annotations={'title': 'Update file name', 'idempotentHint': True}
    )
    async def update_file_name(model: UpdateFileNameRequest) -> RestResponse:
        """Update the name of a file."""
        return await post('/files/update', add_code_source_id(model))

    # Update contents
    @tool_with_args(
        mcp,
        UpdateFileContentsRequest,
        annotations={'title': 'Update file contents', 'idempotentHint': True}
    )
    async def update_file_contents(
            model: UpdateFileContentsRequest) -> ProjectFilesResponse:
        """Update the contents of a file."""
        return await post('/files/update', add_code_source_id(model))

    # Update lines (patch)
    @mcp.tool(
        annotations={'title': 'Patch file', 'idempotentHint': True}
    )
    async def patch_file(model: PatchFileRequest) -> RestResponse:
        """Apply a patch (unified diff) to a file in a project."""
        return await post('/files/patch', add_code_source_id(model))
        
    # Delete
    @tool_with_args(
        mcp,
        DeleteFileRequest,
        annotations={'title': 'Delete file', 'idempotentHint': True}
    )
    async def delete_file(model: DeleteFileRequest) -> RestResponse:
        """Delete a file in a project."""
        return await post('/files/delete', add_code_source_id(model))
