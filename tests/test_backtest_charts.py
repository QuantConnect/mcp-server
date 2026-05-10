import pytest

from main import mcp
from test_project import Project
from test_backtests import Backtest
from utils import (
    validate_models, 
    ensure_request_raises_validation_error_when_omitting_an_arg,
    ensure_request_fails_when_including_an_invalid_arg
)
from models import (
    ReadBacktestChartRequest,
    #LoadingChartResponse,
    ReadChartResponse
)


# Static helpers for common operations:
class BacktestCharts:

    default_charts = [
        'Strategy Equity', 'Capacity', 'Drawdown', 'Benchmark', 'Exposure',
        'Assets Sales Volume', 'Portfolio Turnover', 'Portfolio Margin'
    ]

    @staticmethod
    async def read(project_id, backtest_id, name, start, end, count=100):
        output_model = await validate_models(
            mcp, 'read_backtest_chart', 
            {
                'projectId': project_id, 
                'backtestId': backtest_id, 
                'name': name,
                'start': start, 
                'end': end,
                'count': count
            },
            ReadChartResponse
        )
        return output_model.chart


TEST_CASES = [
    ('Py', 'charts.py'),
    ('C#', 'Charts.cs')
]
# Test suite:
class TestBacktestCharts:

    async def _run_algorithm(self, language, algo):
        # Backtest and algorithm that creates a custom chart.
        project_id, backtest_id = await Backtest.run_algorithm(language, algo)
        # Return the data we need to read the backtest charts.
        start = 1672531200  # Start Unix time of the backtest.
        end = 1680307200  # End Unix time of the backtest.
        return project_id, backtest_id, start, end

    @pytest.mark.asyncio
    @pytest.mark.parametrize('language, algo', TEST_CASES)
    async def test_read_backtest_chart(self, language, algo):
        # Run the backtest.
        project_id, backtest_id, start, end = (
            await self._run_algorithm(language, algo)
        )
        # Try to read the charts.
        for name in BacktestCharts.default_charts + ['SMA']:
            chart = await BacktestCharts.read(
                project_id, backtest_id, name, start, end
            )
            assert chart.name == name
        # Delete the project to clean up.
        await Project.delete(project_id)

    @pytest.mark.asyncio    
    @pytest.mark.parametrize('language, algo', TEST_CASES)
    async def test_read_backtest_chart_with_invalid_args(
            self, language, algo):
        # Run the backtest.
        project_id, backtest_id, start, end = (
            await self._run_algorithm(language, algo)
        )
        # Test the invalid requests.
        tool_name = 'read_backtest_chart'
        class_ = ReadBacktestChartRequest
        minimal_payload = {
            'projectId': project_id,
            'backtestId': backtest_id,
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
                # Try to read the charts of a backtest that doesn't 
                # exist.
                {'backtestId': ' '},
                # Try to read a chart that doesn't exist.
                {'name': ' '},
                # Try to read a chart when the end time is before the
                # start time.
                {'start': end, 'end': start}
            ]
        )
        # Delete the project to clean up.
        await Project.delete(project_id)
