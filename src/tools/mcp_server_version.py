from src import __version__

import requests

def register_mcp_server_version_tools(mcp):
    # Read current version
    @mcp.tool(
        annotations={
            'title': 'Read QC MCP Server version', 'readOnlyHint': True
        }
    )
    async def read_mcp_server_version() -> str:
        """Returns the version of the QC MCP Server that's running."""
        return __version__

    # Read latest version
    @mcp.tool(
        annotations={
            'title': 'Read latest QC MCP Server version', 'readOnlyHint': True
        }
    )
    async def read_latest_mcp_server_version() -> str:
        """Returns the latest version of the QC MCP Server released."""
        response = requests.get(
            "https://hub.docker.com/v2/namespaces/quantconnect/repositories/mcp-server/tags", 
            params={"page_size": 2}
        )
        response.raise_for_status()
        # Get the name of the second result. The first one is 'latest'.
        return response.json()['results'][1]['name']
