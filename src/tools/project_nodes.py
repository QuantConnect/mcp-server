from api_connection import post
from models import (
    ReadProjectNodesRequest,
    UpdateProjectNodesRequest,
    ProjectNodesResponse
)
from tool_args import tool_with_args

def register_project_node_tools(mcp):
    # Read
    @tool_with_args(
        mcp,
        ReadProjectNodesRequest,
        annotations={'title': 'Read project nodes', 'readOnlyHint': True}
    )
    async def read_project_nodes(
            model: ReadProjectNodesRequest) -> ProjectNodesResponse:
        """Read the available and selected nodes of a project."""
        return await post('/projects/nodes/read', model)

    # Update
    @tool_with_args(
        mcp,
        UpdateProjectNodesRequest,
        annotations={
            'title': 'Update project nodes',
            'destructiveHint': False,
            'idempotentHint': True
        }
    )
    async def update_project_nodes(
            model: UpdateProjectNodesRequest) -> ProjectNodesResponse:
        """Update the active state of the given nodes to true.
        
        If you don't provide any nodes, all the nodes become inactive 
        and autoSelectNode is true.
        """
        return await post('/projects/nodes/update', model)
