from __future__ import annotations

from api_connection import post
from models import (
    BacktestInitResponse,
    BasicFilesRequest,
    CodeCompletionRequest,
    CodeCompletionResponse,
    ErrorEnhanceRequest,
    ErrorEnhanceResponse,
    PEP8ConvertRequest,
    PEP8ConvertResponse,
    SearchRequest,
    SearchResponse,
    SyntaxCheckResponse,
)
from mcp.server.fastmcp import FastMCP


def register_ai_tools(mcp: FastMCP) -> None:
    """Expose AI-assistive tooling such as code completion and search."""

    @mcp.tool(
        annotations={"title": "Check initialization errors", "readOnlyHint": True}
    )
    async def check_initialization_errors(
        model: BasicFilesRequest,
    ) -> BacktestInitResponse:
        """Run a short backtest to surface initialization errors."""

        return await post("/ai/tools/backtest-init", model)

    @mcp.tool(annotations={"title": "Complete code", "readOnlyHint": True})
    async def complete_code(
        model: CodeCompletionRequest,
    ) -> CodeCompletionResponse:
        """Return code completion suggestions."""

        return await post("/ai/tools/complete", model)

    @mcp.tool(annotations={"title": "Enhance error message", "readOnlyHint": True})
    async def enhance_error_message(
        model: ErrorEnhanceRequest,
    ) -> ErrorEnhanceResponse:
        """Augment runtime errors with additional guidance."""

        return await post("/ai/tools/error-enhance", model)

    @mcp.tool(annotations={"title": "Update code to PEP8", "readOnlyHint": True})
    async def update_code_to_pep8(
        model: PEP8ConvertRequest,
    ) -> PEP8ConvertResponse:
        """Convert Python code snippets to follow PEP 8 style."""

        return await post("/ai/tools/pep8-convert", model)

    @mcp.tool(annotations={"title": "Check syntax", "readOnlyHint": True})
    async def check_syntax(model: BasicFilesRequest) -> SyntaxCheckResponse:
        """Validate algorithm syntax without running the algorithm."""

        return await post("/ai/tools/syntax-check", model)

    @mcp.tool(annotations={"title": "Search QuantConnect", "readOnlyHint": True})
    async def search_quantconnect(model: SearchRequest) -> SearchResponse:
        """Search QuantConnect documentation, forums, and examples."""

        return await post("/ai/tools/search", model)
