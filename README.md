<img width="1575" height="280" alt="github-header" src="https://github.com/user-attachments/assets/6cec1ef7-0340-416e-ab81-c73fbc8ff847" />

# QuantConnect Remote MCP Server

The **QuantConnect Remote MCP Server** is the preferred way to connect AI assistants such as Claude to the QuantConnect platform.

There is nothing to install, build, or run. Point your MCP client at the hosted endpoint, authorize it against your QuantConnect organization, and the tools are available immediately.

- **Documentation:** https://www.quantconnect.com/docs/v2/ai-assistance/mcp-server/key-concepts
- **Remote MCP endpoint:** `https://www.quantconnect.com/api/v2/mcp`

> **Note:** The remote MCP server requires a paid agent node (A1-1, A4-8, or A16-32) in your organization. The free A-MICRO node cannot connect. See [Agent Nodes](https://www.quantconnect.com/docs/v2/cloud-platform/organizations/resources#05-Agent-Nodes) and [Add Nodes](https://www.quantconnect.com/docs/v2/cloud-platform/organizations/resources#15-Add-Nodes).

## Quick Start with Claude

The remote server speaks the standard MCP HTTP transport, so any MCP-capable Claude surface can use it. Pick the one you use.

### Claude Desktop and claude.ai

1. Open **Settings > Connectors** (on the desktop app, **File > Settings > Connectors**).
2. Click **Add custom connector**, give it a name such as `QuantConnect`, and enter the server URL:
   ```
   https://www.quantconnect.com/api/v2/mcp
   ```
3. Click **Connect**. Your default browser opens.
4. Click **Continue connecting**, select your QuantConnect organization in the **Authorize MCP Server** form, and click **Authorize**.
5. Start a new chat. The QuantConnect tools are listed under the connector and can be enabled per conversation.

### Claude Code (terminal)

Register the server once from any terminal:

```bash
claude mcp add --transport http quantconnect https://www.quantconnect.com/api/v2/mcp
```

Then start Claude Code, run `/mcp`, select **quantconnect**, and follow the browser authorization flow (**Continue connecting > Authorize**). Running `/mcp` again should show the server as connected with its tools listed.

### Claude Code in Local Platform (VS Code extension)

1. Install the Claude Code extension in VS Code.
2. Create or open a QuantConnect project in Local Platform.
3. Open the Claude Code panel from the top navigation bar.
4. Enter `/mcp` to confirm the QuantConnect MCP Server is connected.

### Try it

Once connected, send a simple prompt to verify the tools are working:

```
Read the open project.
```

Claude should call the `read_open_project` tool and describe the project. From there you can ask it to create projects, write and edit strategy files, run backtests, optimize parameters, or deploy to paper trading, all in plain language. For example:

```
Create a new Python project that buys SPY on the first trading day of each month,
backtest it from 2020 to today, and summarize the results.
```

Tip for Claude Code users: a `CLAUDE.md` file in your project or home directory lets you set conventions (Python-first, compile after every edit, position-sizing rules, and so on). The [Claude Code docs page](https://www.quantconnect.com/docs/v2/ai-assistance/mcp-server/claude-code) includes an example you can copy.

## Available Tools

The full, up-to-date list lives in the [Key Concepts](https://www.quantconnect.com/docs/v2/ai-assistance/mcp-server/key-concepts) documentation.

## Other Clients

The remote server also works with Copilot, Cursor, Devin Desktop, and any other client that supports the MCP HTTP transport. Setup guides for each are in the [MCP Server documentation](https://www.quantconnect.com/docs/v2/ai-assistance/mcp-server).
