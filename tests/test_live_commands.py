import pytest
from time import sleep

from main import mcp
from test_project import Project
from test_files import Files
from test_live import Live
from test_live_logs import LiveLogs
from utils import validate_models
from models import (
    CreateLiveCommandRequest,
    BroadcastLiveCommandRequest,
    RestResponse
)


# Static helpers for common operations:
class LiveCommands:

    @staticmethod
    async def create(project_id, command):
        return await validate_models(
            mcp, 'create_live_command', 
            {'projectId': project_id, 'command': command}, RestResponse
        )

    @staticmethod
    async def broadcast(organization_id, command, **kwargs):
        return await validate_models(
            mcp, 'broadcast_live_command', 
            {'organizationId': organization_id, 'command': command} | kwargs, 
            RestResponse
        )    


TEST_CASES = [
    ('Py', 'live_command.py'),
    #('C#', 'LiveCommand.cs')
]
# Test suite:
class TestLiveCommands:

    @pytest.mark.asyncio
    @pytest.mark.parametrize('language, algo', TEST_CASES)
    async def test_create_live_command(self, language, algo):
        # Create and compile the project.
        project_id, compile_id = await Files.setup_project(language, algo)
        # Deploy the algorithm and wait for it to start.
        node_id = await Live.get_node_id(project_id)
        live = await Live.create(project_id, compile_id, node_id)
        await Live.wait_for_algorithm_to_start(project_id)
        # Wait for logs to load. If you send the command
        # too early, it doesn't reach the algorithm.
        await LiveLogs.wait_for_logs_to_load(
            project_id, live.deployId, threshold=3
        )
        # Try to send a generic command.
        await LiveCommands.create(project_id, {'text': 'foo'})
        # Try to send an encapsulated command.
        encapsulated_command = {
            '$type': 'MyCommand', 
            'text': 'boo', 
            'number': 1, 
            'parameters': {'hello': 'world'}
        }
        await LiveCommands.create(project_id, encapsulated_command)
        # Give the algorithm time to print the logs and then stop it so
        # it flushes all the logs to the log file. Without stopping it, 
        # we'll have to wait ~10 minutes for the log file to populate.
        sleep(15)
        await Live.stop(project_id)
        # Check the logs to see if the commands ran.
        response = await LiveLogs.wait_for_logs_to_load(
            project_id, live.deployId, threshold=5
        )
        assert response.logs
        assert any([
            'Generic command. data.text: foo' in log 
            for log in response.logs
        ])
        assert any([
            f"Encapsulated command. text: {encapsulated_command['text']}; "
            f"number: {encapsulated_command['number']}; "
            f"parameters: {encapsulated_command['parameters']}" in log
            for log in response.logs
        ])
        # Delete the project to clean up.
        await Project.delete(project_id)
