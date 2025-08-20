import pytest
from time import sleep

from main import mcp
from test_project import Project
from test_files import Files
from test_live import Live
from utils import validate_models
from models import LiveInsightsResponse


# Static helpers for common operations:
class LiveInsights:

    @staticmethod
    async def read(project_id, end, **kwargs):
        return await validate_models(
            mcp, 'read_live_insights', 
            {'projectId': project_id, 'end': end} | kwargs,
            LiveInsightsResponse
        )

    @staticmethod
    async def wait_for_insights_to_load(project_id, end=1_000):
        attempts = 0
        while attempts < 6*15: # 15 minutes
            attempts += 1
            response = await LiveInsights.read(project_id, end)
            if response.length:
                return response.insights
            sleep(10)
        assert False, "Insights didn't load in time."


TEST_CASES = [
    ('Py', 'live_insights.py'),
    ('C#', 'LiveInsights.cs')
]
# Test suite:
class TestLiveInsights:

    @pytest.mark.asyncio
    @pytest.mark.parametrize('language, algo', TEST_CASES)
    async def test_read_live_insights(self, language, algo):
        # Create and compile the project.
        project_id, compile_id = await Files.setup_project(language, algo)
        # Deploy the algorithm.
        await Live.create(
            project_id, compile_id, await Live.get_node_id(project_id)
        )
        await Live.wait_for_algorithm_to_start(project_id)
        # Give the algorithm time to emit the insights and then stop it 
        # so it flushes all the insights to the insight file. Without 
        # stopping it, we'll have to wait ~10 minutes for the file to 
        # populate.
        sleep(120)
        await Live.stop(project_id)
        # Try to read the insights.
        insights = await LiveInsights.wait_for_insights_to_load(project_id)
        for i, insight in enumerate(insights):
            insight.symbol == 'BTCUSD 2XR'
            insight.type == 'price'
            insight.direction == ['up', 'flat'][i%2]
            insight.period == 24*60*60 # seconds in a day
            insight.magnitude == None
            insight.confidence == None
            insight.weight == None
            insight.tag == None
        # Delete the project to clean up.
        await Project.delete(project_id)
