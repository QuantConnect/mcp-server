from api_connection import post
from models import (
    BasicFilesRequest,
    CodeCompletionRequest,
    ErrorEnhanceRequest,
    PEP8ConvertRequest,
    BasicFilesRequest,
    SearchRequest,

    BacktestInitResponse,
    CodeCompletionResponse,
    ErrorEnhanceResponse,
    PEP8ConvertResponse,
    SyntaxCheckResponse,
    SearchResponse
)
from tool_args import tool_with_args

def register_ai_tools(mcp):
    # Get backtest initialization errors
    @tool_with_args(
        mcp,
        BasicFilesRequest,
        annotations={
            'title': 'Check initialization errors', 'readOnlyHint': True
        }
    )
    async def check_initialization_errors(
            model: BasicFilesRequest) -> BacktestInitResponse:
        """Run a backtest for a few seconds to initialize the algorithm 
        and get inialization errors if any."""
        return await post('/ai/tools/backtest-init', model)
    
    # Complete code
    @tool_with_args(
        mcp,
        CodeCompletionRequest,
        annotations={'title': 'Complete code', 'readOnlyHint': True}
    )
    async def complete_code(
            model: CodeCompletionRequest) -> CodeCompletionResponse:
        """Show the code completion for a specific text input."""
        return await post('/ai/tools/complete', model)

    # Enchance error message
    @tool_with_args(
        mcp,
        ErrorEnhanceRequest,
        annotations={'title': 'Enhance error message', 'readOnlyHint': True}
    )
    async def enhance_error_message(
            model: ErrorEnhanceRequest) -> ErrorEnhanceResponse:
        """Show additional context and suggestions for error messages."""
        return await post('/ai/tools/error-enhance', model)

    # Update code to PEP8
    @tool_with_args(
        mcp,
        PEP8ConvertRequest,
        annotations={'title': 'Update code to PEP8', 'readOnlyHint': True}
    )
    async def update_code_to_pep8(
            model: PEP8ConvertRequest) -> PEP8ConvertResponse:
        """Update Python code to follow PEP8 style."""
        return await post('/ai/tools/pep8-convert', model)

    # Check syntax
    @tool_with_args(
        mcp,
        BasicFilesRequest,
        annotations={'title': 'Check syntax', 'readOnlyHint': True}
    )
    async def check_syntax(model: BasicFilesRequest) -> SyntaxCheckResponse:
        """Check the syntax of a code."""
        return await post('/ai/tools/syntax-check', model)

    # Search
    @tool_with_args(
        mcp,
        SearchRequest,
        annotations={'title': 'Search QuantConnect', 'readOnlyHint': True}
    )
    async def search_quantconnect(model: SearchRequest) -> SearchResponse:
        """Search for content in QuantConnect."""
        return await post('/ai/tools/search', model)
