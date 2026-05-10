from api_connection import post
from models import (
    CreateProjectRequest,
    ReadProjectRequest,
    UpdateProjectRequest,
    DeleteProjectRequest,
    ProjectListResponse,
    RestResponse
)
from tool_args import tool_with_args

def register_project_tools(mcp):
    # Create
    @tool_with_args(
        mcp,
        CreateProjectRequest,
        annotations={
            'title': 'Create project',
            'destructiveHint': False,
            'idempotentHint': False
        }
    )
    async def create_project(model: CreateProjectRequest) -> ProjectListResponse:
        """Create a new project in your default organization."""
        return await post('/projects/create', model)

    # Read (singular)
    @tool_with_args(
        mcp,
        ReadProjectRequest,
        annotations={'title': 'Read project', 'readOnlyHint': True}
    )
    async def read_project(model: ReadProjectRequest) -> ProjectListResponse:
        """List the details of a project or a set of recent projects."""
        return await post('/projects/read', model)
    
    # Read (all)
    @tool_with_args(
        mcp,
        annotations={'title': 'List projects', 'readOnlyHint': True}
    )
    async def list_projects() -> ProjectListResponse:
        """List the details of all projects."""
        return await post('/projects/read')

    # Update
    @tool_with_args(
        mcp,
        UpdateProjectRequest,
        annotations={'title': 'Update project', 'idempotentHint': True}
    )
    async def update_project(model: UpdateProjectRequest) -> RestResponse:
        """Update a project's name or description."""
        return await post('/projects/update', model)
        
    # Delete
    @tool_with_args(
        mcp,
        DeleteProjectRequest,
        annotations={'title': 'Delete project', 'idempotentHint': True}
    )
    async def delete_project(model: DeleteProjectRequest) -> RestResponse:
        """Delete a project."""
        return await post('/projects/delete', model)
