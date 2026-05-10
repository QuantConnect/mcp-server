from api_connection import post
from models import (
    CreateBacktestRequest,
    ReadBacktestRequest,
    ReadBacktestChartRequest,
    ReadBacktestOrdersRequest,
    ReadBacktestInsightsRequest,
    BacktestReportRequest,
    ListBacktestRequest,
    UpdateBacktestRequest,
    DeleteBacktestRequest,
    BacktestResponse,
    #LoadingChartResponse,
    ReadChartResponse,
    BacktestOrdersResponse,
    BacktestInsightsResponse,
    BacktestSummaryResponse,
    BacktestReport,
    BacktestReportGeneratingResponse,
    RestResponse
)
from tool_args import tool_with_args

def register_backtest_tools(mcp):
    # Create
    @tool_with_args(
        mcp,
        CreateBacktestRequest,
        annotations={
            'title': 'Create backtest',
            'destructiveHint': False
        }
    )
    async def create_backtest(
            model: CreateBacktestRequest) -> BacktestResponse:
        """Create a new backtest request and get the backtest Id."""
        return await post('/backtests/create', model)

    # Read statistics for a single backtest.
    @tool_with_args(
        mcp,
        ReadBacktestRequest,
        annotations={'title': 'Read backtest', 'readOnlyHint': True}
    )
    async def read_backtest(model: ReadBacktestRequest) -> BacktestResponse:
        """Read the results of a backtest."""
        return await post('/backtests/read', model)

    # Read a summary of all the backtests.
    @tool_with_args(
        mcp,
        ListBacktestRequest,
        annotations={'title': 'List backtests', 'readOnlyHint': True}
    )
    async def list_backtests(
            model: ListBacktestRequest) -> BacktestSummaryResponse:
        """List all the backtests for the project."""
        return await post('/backtests/list', model)

    # Read the chart of a single backtest.
    @tool_with_args(
        mcp,
        ReadBacktestChartRequest,
        annotations={'title': 'Read backtest chart', 'readOnlyHint': True}
    )
    async def read_backtest_chart(
            model: ReadBacktestChartRequest) -> ReadChartResponse:
        """Read a chart from a backtest."""
        return await post('/backtests/chart/read', model)
    
    # Read the orders of a single backtest.
    @tool_with_args(
        mcp,
        ReadBacktestOrdersRequest,
        annotations={'title': 'Read backtest orders', 'readOnlyHint': True}
    )
    async def read_backtest_orders(
            model: ReadBacktestOrdersRequest) -> BacktestOrdersResponse:
        """Read out the orders of a backtest."""
        return await post('/backtests/orders/read', model)
    
    # Read the insights of a single backtest.
    @tool_with_args(
        mcp,
        ReadBacktestInsightsRequest,
        annotations={'title': 'Read backtest insights', 'readOnlyHint': True}
    )
    async def read_backtest_insights(
            model: ReadBacktestInsightsRequest) -> BacktestInsightsResponse:
        """Read out the insights of a backtest."""
        return await post('/backtests/read/insights', model)
    
    ## Read the report of a single backtest.
    #@mcp.tool(
    #    annotations={'title': 'Read backtest report', 'readOnlyHint': True}
    #)
    #async def read_backtest_report(
    #        model: BacktestReportRequest
    #    ) -> BacktestReport | BacktestReportGeneratingResponse:
    #    """Read out the report of a backtest."""
    #    return await post('/backtests/read/report', model)

    # Update
    @tool_with_args(
        mcp,
        UpdateBacktestRequest,
        annotations={'title': 'Update backtest', 'idempotentHint': True}
    )
    async def update_backtest(model: UpdateBacktestRequest) -> RestResponse:
        """Update the name or note of a backtest."""
        return await post('/backtests/update', model)
    
    # Delete
    @tool_with_args(
        mcp,
        DeleteBacktestRequest,
        annotations={'title': 'Delete backtest', 'idempotentHint': True}
    )
    async def delete_backtest(model: DeleteBacktestRequest) -> RestResponse:
        """Delete a backtest from a project."""
        return await post('/backtests/delete', model)
