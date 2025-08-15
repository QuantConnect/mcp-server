from pydantic_core import to_jsonable_python
import webbrowser

from api_connection import post, httpx, get_headers, BASE_URL
from models import (
    AuthorizeExternalConnectionRequest,
    CreateLiveAlgorithmRequest,
    ReadLiveAlgorithmRequest,
    ListLiveAlgorithmsRequest,
    ReadLivePortfolioRequest,
    ReadLiveChartRequest,
    ReadLiveOrdersRequest,
    ReadLiveInsightsRequest,
    ReadLiveLogsRequest,
    LiquidateLiveAlgorithmRequest,
    StopLiveAlgorithmRequest,
    AuthorizeExternalConnectionResponse,
    CreateLiveAlgorithmResponse,
    LiveAlgorithmResults,
    LiveAlgorithmListResponse,
    LivePortfolioResponse,
    ReadChartResponse,
    LiveOrdersResponse,
    LiveInsightsResponse,
    ReadLiveLogsResponse,
    RestResponse
)
from tool_args import tool_with_args

async def handle_loading_response(response, text):
    if 'progress' in response:
        progress = response["progress"]
        return {'errors': [f'{text} Progress: {progress}']}
    return response

def register_live_trading_tools(mcp):
    # Authenticate
    @tool_with_args(
        mcp,
        AuthorizeExternalConnectionRequest,
        annotations={
            'title': 'Authorize external connection',
            'readOnlyHint': False,
            'destructiveHint': False,
            'idempotentHint': True
        }
    )
    async def authorize_connection(
            model: AuthorizeExternalConnectionRequest
            ) -> AuthorizeExternalConnectionResponse:
        """Authorize an external connection with a live brokerage or 
        data provider.

        This tool automatically opens your browser for you to complete
        the authentication flow. For the flow to work, you must be 
        logged into your QuantConnect account on the browser that opens.
        """
        # This endpoint is unique because post we need to extract and 
        # return the redirect URL and open it in a browser.        
        async with httpx.AsyncClient(follow_redirects=False) as client:
            response = await client.post(
                f'{BASE_URL}/live/auth0/authorize', 
                headers=get_headers(), 
                json=to_jsonable_python(model, exclude_none=True),
                timeout=300.0 # 5 minutes
            )
            # Extract the redirect URL from the 'Location' header
            redirect_url = response.headers.get("Location")
            # Open the URL in the user's default browser.
            webbrowser.open(redirect_url)
        # Read the authentication.
        return await post('/live/auth0/read', model, 800.0)

    # Create
    @tool_with_args(
        mcp,
        CreateLiveAlgorithmRequest,
        annotations={
            'title': 'Create live algorithm', 'destructiveHint': False
        }
    )
    async def create_live_algorithm(
            model: CreateLiveAlgorithmRequest) -> CreateLiveAlgorithmResponse:
        """Create a live algorithm."""
        return await post('/live/create', model)

    # Read (singular)
    @tool_with_args(
        mcp,
        ReadLiveAlgorithmRequest,
        annotations={'title': 'Read live algorithm', 'readOnly': True}
    )
    async def read_live_algorithm(
            model: ReadLiveAlgorithmRequest) -> LiveAlgorithmResults:
        """Read details of a live algorithm."""
        return await post('/live/read', model)

    # Read (all).
    @tool_with_args(
        mcp,
        ListLiveAlgorithmsRequest,
        annotations={'title': 'List live algorithms', 'readOnly': True}
    )
    async def list_live_algorithms(
            model: ListLiveAlgorithmsRequest) -> LiveAlgorithmListResponse:
        """List all your past and current live trading deployments."""
        return await post('/live/list', model)

    # Read a chart.
    @tool_with_args(
        mcp,
        ReadLiveChartRequest,
        annotations={'title': 'Read live chart', 'readOnly': True}
    )
    async def read_live_chart(
            model: ReadLiveChartRequest) -> ReadChartResponse:
        """Read a chart from a live algorithm."""
        return await handle_loading_response(
            await post('/live/chart/read', model), 'Chart is loading.'
        )

    # Read the logs.
    @tool_with_args(
        mcp,
        ReadLiveLogsRequest,
        annotations={'title': 'Read live logs', 'readOnly': True}
    )
    async def read_live_logs(
            model: ReadLiveLogsRequest) -> ReadLiveLogsResponse:
        """Get the logs of a live algorithm.

        The snapshot updates about every 5 minutes."""
        return await post('/live/logs/read', model)

    # Read the portfolio state.
    @tool_with_args(
        mcp,
        ReadLivePortfolioRequest,
        annotations={'title': 'Read live portfolio', 'readOnly': True}
    )
    async def read_live_portfolio(
            model: ReadLivePortfolioRequest) -> LivePortfolioResponse:
        """Read out the portfolio state of a live algorithm.

        The snapshot updates about every 10 minutes."""
        return await post('/live/portfolio/read', model)

    # Read the orders.
    @tool_with_args(
        mcp,
        ReadLiveOrdersRequest,
        annotations={'title': 'Read live orders', 'readOnly': True}
    )
    async def read_live_orders(
            model: ReadLiveOrdersRequest) -> LiveOrdersResponse:
        """Read out the orders of a live algorithm.

        The snapshot updates about every 10 minutes."""
        return await handle_loading_response(
            await post('/live/orders/read', model), 'Orders are loading.'
        )

    # Read the insights.
    @tool_with_args(
        mcp,
        ReadLiveInsightsRequest,
        annotations={'title': 'Read live insights', 'readOnly': True}
    )
    async def read_live_insights(
            model: ReadLiveInsightsRequest) -> LiveInsightsResponse:
        """Read out the insights of a live algorithm.

        The snapshot updates about every 10 minutes."""
        return await post('/live/insights/read', model)

    # Update (stop)
    @tool_with_args(
        mcp,
        StopLiveAlgorithmRequest,
        annotations={'title': 'Stop live algorithm', 'idempotentHint': True}
    )
    async def stop_live_algorithm(
            model: StopLiveAlgorithmRequest) -> RestResponse:
        """Stop a live algorithm."""
        return await post('/live/update/stop', model)

    # Update (liquidate)
    @tool_with_args(
        mcp,
        LiquidateLiveAlgorithmRequest,
        annotations={
            'title': 'Liquidate live algorithm', 'idempotentHint': True
        }
    )
    async def liquidate_live_algorithm(
            model: LiquidateLiveAlgorithmRequest) -> RestResponse:
        """Liquidate and stop a live algorithm."""
        return await post('/live/update/liquidate', model)
