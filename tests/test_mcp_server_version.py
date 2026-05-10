import os
import pytest

from main import mcp

requires_quantconnect_api_tests = pytest.mark.skipif(
    os.getenv("RUN_QUANTCONNECT_API_TESTS") != "1",
    reason="Requires access to QuantConnect/Docker Hub APIs. "
    "Set RUN_QUANTCONNECT_API_TESTS=1 to run integration tests.",
)


class TestMCPServerVersion:

    async def _ensure_response_has_two_periods(self, tool_name):
        _, structured_response = await mcp.call_tool(tool_name, {})
        assert structured_response['result'].count('.') == 2

    @pytest.mark.asyncio
    async def test_read_verion(self):
        await self._ensure_response_has_two_periods('read_mcp_server_version')

    @pytest.mark.asyncio
    @requires_quantconnect_api_tests
    async def test_read_latest_verion(self):
        await self._ensure_response_has_two_periods(
            'read_latest_mcp_server_version'
        )
        
