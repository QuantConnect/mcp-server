from mcp.server.fastmcp import FastMCP

from tools.account import register_account_tools

# Initialize the FastMCP server.
mcp = FastMCP('quantconnect', version='0.1.0')

# Register all the tools.
registration_functions = [
    register_account_tools,
]
for registration_function in registration_functions:
    registration_function(mcp)

if __name__ == "__main__":
    # Initialize and run the server.
    mcp.run(transport='stdio')
