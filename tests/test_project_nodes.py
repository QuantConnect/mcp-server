import pytest

from main import mcp
from test_project import Project
from utils import (
    validate_models, 
    ensure_request_raises_validation_error,
    ensure_request_fails
)
from models import (
    ReadProjectNodesRequest,
    ProjectNodesResponse
)

# Static helpers for common operations:
class ProjectNodes:

    @staticmethod
    async def read(project_id):
        output_model = await validate_models(
            mcp, 'read_project_nodes', {'projectId': project_id}, 
            ProjectNodesResponse
        )
        return output_model

    @staticmethod
    async def update(project_id, **kwargs):
        output_model = await validate_models(
            mcp, 'update_project_nodes', {'projectId': project_id} | kwargs, 
            ProjectNodesResponse
        )
        return output_model


# Test suite:
class TestProjectNodes:

    async def _ensure_all_nodes_are_inactive(self, nodes):
        assert len([n for n in nodes.backtest if n.active]) == 0
        assert len([n for n in nodes.research if n.active]) == 0
        assert len([n for n in nodes.live if n.active]) == 0

    async def _active_nodes(self, nodes):
        return (
            [n.id for n in nodes.backtest if n.active]
            + [n.id for n in nodes.research if n.active]
            + [n.id for n in nodes.live if n.active]
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize('language', ['Py', 'C#'])
    async def test_read_project_nodes(self, language):
        # Create a project.
        project_id = (await Project.create(language=language)).projectId
        # Test if we can read the project nodes.
        nodes_response = await ProjectNodes.read(project_id)
        # Test if the default is to enable 'autoSelectNode'.
        assert nodes_response.autoSelectNode
        await self._ensure_all_nodes_are_inactive(nodes_response.nodes)
        # Delete the project to clean up.
        await Project.delete(project_id)

    @pytest.mark.asyncio
    async def test_read_project_nodes_with_invalid_args(self):
        # Try to read the project nodes without providing the project 
        # Id.
        tool_name = 'read_project_nodes'
        await ensure_request_raises_validation_error(
            tool_name, ReadProjectNodesRequest, {}
        )
        # Try to read the nodes of a project that doesn't exist.
        await ensure_request_fails(mcp, tool_name, {'projectId': -1})

    @pytest.mark.asyncio
    async def test_update_project_nodes(self):
        # Create a project.
        project_id = (await Project.create()).projectId
        
        # Select some specific nodes.
        nodes = (await ProjectNodes.read(project_id)).nodes
        node_ids = (
            [n.id for n in nodes.backtest[:2]]
            + [n.id for n in nodes.research[:2]]
            + [n.id for n in nodes.live[:2]]
        )
        # Update the project's selected nodes.
        nodes_response = await ProjectNodes.update(project_id, nodes=node_ids)
        # Test if the project's selected nodes were updated.
        assert not nodes_response.autoSelectNode
        active_nodes = await self._active_nodes(nodes_response.nodes)
        for node_id in node_ids:
            assert node_id in active_nodes
        
        # Update the project to auto-select the best node by omitting
        # the list of nodes.
        nodes_response = await ProjectNodes.update(project_id)
        # Test if the project's selected nodes were updated.
        assert nodes_response.autoSelectNode
        await self._ensure_all_nodes_are_inactive(nodes_response.nodes)

        # Update the project to auto-select the best node by passing 
        # an empty list.
        await ProjectNodes.update(project_id, nodes=node_ids)
        nodes_response = await ProjectNodes.update(project_id, nodes=[])
        # Test if the project's selected nodes were updated.
        assert nodes_response.autoSelectNode
        await self._ensure_all_nodes_are_inactive(nodes_response.nodes)

        # Delete the project to clean up.
        await Project.delete(project_id)

    @pytest.mark.asyncio
    async def test_update_project_nodes_with_invalid_args(self):
        # Create a project.
        project_id = (await Project.create()).projectId
        # Test the invalid requests.
        invalid_payloads = [
            # Try to update the nodes of a project that doesn't exist.
            {'projectId': -1},
            # Try to update the nodes of a project by providing invalid
            # node Ids.
            #{'projectId': project_id, 'nodes': ['fakeNodeId']}
        ]
        for payload in invalid_payloads:
            await ensure_request_fails(mcp, 'update_project_nodes', payload)
        # Delete the project to clean up.
        await Project.delete(project_id)
