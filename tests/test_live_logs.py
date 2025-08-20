import pytest
from time import time, sleep

from main import mcp
from test_live import Live
from test_files import Files
from test_project import Project
from utils import validate_models
from models import ReadLiveLogsRequest, ReadLiveLogsResponse


# Static helpers for common operations:
class LiveLogs:

    @staticmethod
    async def read(project_id, algorithm_id, start_line=0, end_line=250):
        return await validate_models(
            mcp, 'read_live_logs', 
            {
                'projectId': project_id,
                'algorithmId': algorithm_id,
                'startLine': start_line, 
                'endLine': end_line
            },
            ReadLiveLogsResponse
        )

    @staticmethod
    async def wait_for_logs_to_load(
            project_id, algorithm_id, start_line=0, end_line=250, threshold=3):
        attempts = 0
        while attempts < 6*5:  # 5 minutes
            attempts += 1
            response = await LiveLogs.read(
                project_id, algorithm_id, start_line, end_line
            )
            if (any(algorithm_id in log for log in response.logs) and 
                len(response.logs) >= threshold):
                return response
            sleep(10)
        assert False, "Logs didn't load in time."


TEST_CASES = [
    ('Py', 'live_logs.py'),
    #('C#', 'LiveLogs.cs')
]
# Test suite:
class TestLiveLogs:

    @pytest.mark.asyncio
    @pytest.mark.parametrize('language, algo', TEST_CASES)
    async def test_read_live_logs(self, language, algo):
        # Create and compile the project.
        project_id, compile_id = await Files.setup_project(language, algo)
        # Deploy the algorithm.
        live = await Live.create(
            project_id, compile_id, await Live.get_node_id(project_id)
        )
        await Live.wait_for_algorithm_to_start(project_id)
        # Give the algorithm time to print the logs and then stop it so
        # it flushes all the logs to the log file. Without stopping it, 
        # we'll have to wait ~10 minutes for the log file to populate.
        sleep(15)
        await Live.stop(project_id)
        # Try to read the logs.
        response = await LiveLogs.wait_for_logs_to_load(
            project_id, live.deployId
        )
        assert response.deploymentOffset == 0
        assert response.length >= 10        
        assert len(response.logs) >= 10
        # Delete the project to clean up.
        await Project.delete(project_id)
