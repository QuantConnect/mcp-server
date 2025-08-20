import pytest
from time import time, sleep

from main import mcp
from test_live import Live
from test_files import Files
from test_project import Project
from utils import (
    validate_models, 
    ensure_request_raises_validation_error_when_omitting_an_arg,
    ensure_request_fails_when_including_an_invalid_arg
)
from models import (
    ReadLiveChartRequest,
    LoadingResponse,
    ReadChartResponse,
)


# Static helpers for common operations:
class LiveCharts:

    default_charts = [
        'Strategy Equity', 'Drawdown', 'Benchmark', 'Exposure',
        'Assets Sales Volume', 'Portfolio Turnover', 'Portfolio Margin'
    ]

    @staticmethod
    async def read(project_id, name, start, end, count=100):
        return await validate_models(
            mcp, 'read_live_chart', 
            {
                'projectId': project_id,
                'name': name,
                'start': start, 
                'end': end,
                'count': count
            },
            ReadChartResponse
        )

    @staticmethod
    async def wait_for_chart_to_load(project_id, name, start, count=None):
        attempts = 0
        while attempts < 12*2: # 2 mins
            attempts += 1
            end = max(start+10, int(time()))
            response = await LiveCharts.read(project_id, name, start, end)
            if response.errors is None:
                return response.chart
            sleep(5)
        assert False, f"Chart didn't load in time. {type(response)}"


TEST_CASES = [
    ('Py', 'live_charts.py'),
    ('C#', 'LiveCharts.cs')
]
# Test suite:
class TestLiveCharts:

    @pytest.mark.asyncio
    @pytest.mark.parametrize('language, algo', TEST_CASES)
    async def test_read_live_chart(self, language, algo):
        # Create and compile the project.
        project_id, compile_id = await Files.setup_project(language, algo)
        # Deploy the algorithm.
        await Live.create(
            project_id, compile_id, await Live.get_node_id(project_id)
        )
        await Live.wait_for_algorithm_to_start(project_id)
        start = int(time())
        # Give the algorithm time to plot the data and then stop it so
        # it flushes all the charts to the file. Without stopping it, 
        # we'll have to wait ~10 minutes for the chart file to populate.
        sleep(180)
        await Live.stop(project_id)        
        # Try to read the charts.
        for name in LiveCharts.default_charts + ['SMA']:
            chart = await LiveCharts.wait_for_chart_to_load(
                project_id, name, start
            )
            assert chart.name == name, chart
        # Delete the project to clean up.
        await Project.delete(project_id)

    @pytest.mark.asyncio
    async def test_read_live_chart_with_invalid_args(self):
        # Create and compile the project.
        project_id, compile_id = await Files.setup_project('Py')
        # Deploy the algorithm.
        await Live.create(
            project_id, compile_id, await Live.get_node_id(project_id)
        )
        await Live.wait_for_algorithm_to_start(project_id)
        # Test the invalid requests.
        tool_name = 'read_live_chart'
        class_ = ReadLiveChartRequest
        start = int(time())
        end = start + 100
        minimal_payload = {
            'projectId': project_id,
            'name': 'Strategy Equity',
            'start': start, 
            'end': end,
            'count': 100
        }
        # Try to read the insights without providing all the required 
        # arguments.
        await ensure_request_raises_validation_error_when_omitting_an_arg(
            tool_name, class_, minimal_payload
        )
        await ensure_request_fails_when_including_an_invalid_arg(
            mcp, tool_name, minimal_payload, [
                # Try to read the charts of a project that doesn't 
                # exist.
                {'projectId': -1},
                # Try to read a chart that doesn't exist.
                {'name': ' '},
                # Try to read a chart when the end time is before the
                # start time.
                {'start': end, 'end': start}
            ]
        )
        # Stop the algorithm and delete the project to clean up.
        await Live.stop(project_id)
        await Project.delete(project_id)
