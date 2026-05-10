from __future__ import annotations

import webbrowser
from typing import Any

from api_connection import post, post_raw
from models import (
    AuthorizeExternalConnectionRequest,
    AuthorizeExternalConnectionResponse,
    CreateLiveAlgorithmRequest,
    CreateLiveAlgorithmResponse,
    LiquidateLiveAlgorithmRequest,
    ListLiveAlgorithmsRequest,
    LiveAlgorithmListResponse,
    LiveAlgorithmResults,
    LiveInsightsResponse,
    LiveOrdersResponse,
    LivePortfolioResponse,
    ReadChartResponse,
    ReadLiveAlgorithmRequest,
    ReadLiveChartRequest,
    ReadLiveInsightsRequest,
    ReadLiveLogsRequest,
    ReadLiveLogsResponse,
    ReadLiveOrdersRequest,
    ReadLivePortfolioRequest,
    RestResponse,
    StopLiveAlgorithmRequest,
)
from mcp.server.fastmcp import FastMCP


async def handle_loading_response(response: dict[str, Any], text: str):
    """Surface streaming-progress metadata returned by some live endpoints."""

    if "progress" in response:
        progress = response["progress"]
        return {"errors": [f"{text} Progress: {progress}"]}
    return response


def register_live_trading_tools(mcp: FastMCP) -> None:
    """Expose live trading management tools."""

    @mcp.tool(
        annotations={
            "title": "Authorize external connection",
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": True,
        }
    )
    async def authorize_connection(
        model: AuthorizeExternalConnectionRequest,
    ) -> AuthorizeExternalConnectionResponse:
        """Authorize a live brokerage or data provider connection."""

        response = await post_raw(
            "/live/auth0/authorize",
            model=model,
            timeout=300.0,
            follow_redirects=False,
        )
        redirect_url = response.headers.get("Location")
        if redirect_url:
            webbrowser.open(redirect_url)
        return await post("/live/auth0/read", model, 800.0)

    @mcp.tool(annotations={"title": "Create live algorithm", "destructiveHint": False})
    async def create_live_algorithm(
        model: CreateLiveAlgorithmRequest,
    ) -> CreateLiveAlgorithmResponse:
        """Deploy a project to live trading."""

        return await post("/live/create", model)

    @mcp.tool(annotations={"title": "Read live algorithm", "readOnlyHint": True})
    async def read_live_algorithm(
        model: ReadLiveAlgorithmRequest,
    ) -> LiveAlgorithmResults:
        """Retrieve the status of a live deployment."""

        return await post("/live/read", model)

    @mcp.tool(annotations={"title": "List live algorithms", "readOnlyHint": True})
    async def list_live_algorithms(
        model: ListLiveAlgorithmsRequest,
    ) -> LiveAlgorithmListResponse:
        """List current and historical live deployments."""

        return await post("/live/list", model)

    @mcp.tool(annotations={"title": "Read live chart", "readOnlyHint": True})
    async def read_live_chart(model: ReadLiveChartRequest) -> ReadChartResponse:
        """Retrieve chart data for a live deployment."""

        return await handle_loading_response(
            await post("/live/chart/read", model), "Chart is loading."
        )

    @mcp.tool(annotations={"title": "Read live logs", "readOnlyHint": True})
    async def read_live_logs(model: ReadLiveLogsRequest) -> ReadLiveLogsResponse:
        """Fetch recent logs for a live deployment."""

        return await post("/live/logs/read", model)

    @mcp.tool(annotations={"title": "Read live portfolio", "readOnlyHint": True})
    async def read_live_portfolio(
        model: ReadLivePortfolioRequest,
    ) -> LivePortfolioResponse:
        """Retrieve the latest live portfolio snapshot."""

        return await post("/live/portfolio/read", model)

    @mcp.tool(annotations={"title": "Read live orders", "readOnlyHint": True})
    async def read_live_orders(model: ReadLiveOrdersRequest) -> LiveOrdersResponse:
        """Fetch orders for a live deployment."""

        return await handle_loading_response(
            await post("/live/orders/read", model), "Orders are loading."
        )

    @mcp.tool(annotations={"title": "Read live insights", "readOnlyHint": True})
    async def read_live_insights(
        model: ReadLiveInsightsRequest,
    ) -> LiveInsightsResponse:
        """Fetch alpha insights for a live deployment."""

        return await post("/live/insights/read", model)

    @mcp.tool(annotations={"title": "Stop live algorithm", "idempotentHint": True})
    async def stop_live_algorithm(model: StopLiveAlgorithmRequest) -> RestResponse:
        """Stop a live deployment without liquidating."""

        return await post("/live/update/stop", model)

    @mcp.tool(
        annotations={"title": "Liquidate live algorithm", "idempotentHint": True}
    )
    async def liquidate_live_algorithm(
        model: LiquidateLiveAlgorithmRequest,
    ) -> RestResponse:
        """Liquidate and stop a live deployment."""

        return await post("/live/update/liquidate", model)
