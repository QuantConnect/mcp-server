from __future__ import annotations

from api_connection import post
from models import (
    BacktestInsightsResponse,
    BacktestOrdersResponse,
    BacktestResponse,
    BacktestSummaryResponse,
    CreateBacktestRequest,
    DeleteBacktestRequest,
    ListBacktestRequest,
    ReadBacktestChartRequest,
    ReadBacktestInsightsRequest,
    ReadBacktestOrdersRequest,
    ReadBacktestRequest,
    ReadChartResponse,
    RestResponse,
    UpdateBacktestRequest,
)
from mcp.server.fastmcp import FastMCP


def register_backtest_tools(mcp: FastMCP) -> None:
    """Expose backtest management operations."""

    @mcp.tool(
        annotations={
            "title": "Create backtest",
            "destructiveHint": False,
        }
    )
    async def create_backtest(model: CreateBacktestRequest) -> BacktestResponse:
        """Kick off a new backtest request and return the tracking identifier."""

        return await post("/backtests/create", model)

    @mcp.tool(annotations={"title": "Read backtest", "readOnlyHint": True})
    async def read_backtest(model: ReadBacktestRequest) -> BacktestResponse:
        """Retrieve the latest result for a completed backtest."""

        return await post("/backtests/read", model)

    @mcp.tool(annotations={"title": "List backtests", "readOnlyHint": True})
    async def list_backtests(
        model: ListBacktestRequest,
    ) -> BacktestSummaryResponse:
        """Return a summary of recent backtests for a project."""

        return await post("/backtests/list", model)

    @mcp.tool(annotations={"title": "Read backtest chart", "readOnlyHint": True})
    async def read_backtest_chart(
        model: ReadBacktestChartRequest,
    ) -> ReadChartResponse:
        """Fetch chart data from a backtest result."""

        return await post("/backtests/chart/read", model)

    @mcp.tool(annotations={"title": "Read backtest orders", "readOnlyHint": True})
    async def read_backtest_orders(
        model: ReadBacktestOrdersRequest,
    ) -> BacktestOrdersResponse:
        """Retrieve orders generated during a backtest."""

        return await post("/backtests/orders/read", model)

    @mcp.tool(
        annotations={"title": "Read backtest insights", "readOnlyHint": True}
    )
    async def read_backtest_insights(
        model: ReadBacktestInsightsRequest,
    ) -> BacktestInsightsResponse:
        """Retrieve alpha insights produced by a backtest."""

        return await post("/backtests/read/insights", model)

    @mcp.tool(annotations={"title": "Update backtest", "idempotentHint": True})
    async def update_backtest(model: UpdateBacktestRequest) -> RestResponse:
        """Rename a backtest or update its notes."""

        return await post("/backtests/update", model)

    @mcp.tool(annotations={"title": "Delete backtest", "idempotentHint": True})
    async def delete_backtest(model: DeleteBacktestRequest) -> RestResponse:
        """Remove a backtest from the project history."""

        return await post("/backtests/delete", model)
