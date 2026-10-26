<img width="1575" height="280" alt="github-header" src="https://github.com/user-attachments/assets/6cec1ef7-0340-416e-ab81-c73fbc8ff847" />

# This repository has been replaced by the QuantConnect Remote MCP Server

The local, Docker-based MCP server that used to live in this repository has been retired. It has been completely replaced by the **QuantConnect Remote MCP Server**, which is now the preferred way to connect AI assistants such as Claude to the QuantConnect platform.

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

### Projects
| Tool | Description |
|------|-------------|
| `create_project` | Creates a project with the given files (`main.py` or `main.cs` is required). |
| `list_projects` | Lists projects, most recent first, 50 per page, with an optional text filter. |
| `read_project` | Reads a project's name, language, and files. |
| `read_open_project` | Reads the currently open project. |
| `update_project` | Updates the project name or description. |
| `read_project_templates` | Finds matching templates based on a description. |

### Files
| Tool | Description |
|------|-------------|
| `create_file` | Creates a `.py` or `.cs` file and compiles it. |
| `edit_file` | Replaces a unique text snippet in a file and compiles it. |
| `read_file` | Reads a full file or a line range. |
| `delete_file` | Deletes a file in the project root. |
| `search_file_content` | Case-insensitive search across project files, paginated. |

### Compile
| Tool | Description |
|------|-------------|
| `create_compile` | Compiles the project and checks for errors after code changes. |

### Backtests
| Tool | Description |
|------|-------------|
| `create_backtest` | Queues a backtest. Results are delivered as a new message when finished. |
| `read_backtest` | Reads results for completed backtests. |
| `read_backtest_orders` | Reads backtest orders, paginated, with filters. |
| `list_backtests` | Lists recent backtests with stats. |
| `update_backtest` | Renames a backtest or updates its note. |
| `delete_backtest` | Permanently deletes a backtest. |
| `search_backtest_logs` | Searches backtest logs. |

### Optimization
| Tool | Description |
|------|-------------|
| `create_optimization` | Queues a parameter optimization. Results are delivered as a new message when finished. |
| `read_optimization` | Reads the interpretation of a completed optimization. |
| `list_optimizations` | Lists optimizations. |
| `delete_optimization` | Permanently deletes an optimization. |

### Live Trading
| Tool | Description |
|------|-------------|
| `create_live_algorithm` | Deploys to paper trading with the QuantConnect brokerage. |
| `read_live_algorithm` | Reads live deployment status and results. |
| `read_live_holdings` | Reads current live holdings. |
| `search_live_logs` | Searches live deployment logs. |
| `stop_live_algorithm` | Stops trading without liquidating. |
| `liquidate_live_algorithm` | Closes positions at market and stops trading. |

### Research (Jupyter notebook in Cloud Research)
| Tool | Description |
|------|-------------|
| `jupyter_create_cell` | Inserts a cell. |
| `jupyter_read_cell` | Reads a cell by index. |
| `jupyter_update_cell` | Replaces a cell's source. |
| `jupyter_delete_cell` | Deletes a cell by index. |
| `jupyter_execute_cell` | Runs a cell and returns outputs. |
| `jupyter_create_notebook` | Replaces the notebook with raw JSON. |
| `jupyter_read_notebook` | Reads the notebook as raw JSON. |
| `jupyter_execute_notebook` | Runs all cells and returns combined outputs. |
| `jupyter_get_image` | Fetches a research image as base64. |

### Object Store
| Tool | Description |
|------|-------------|
| `object_store_set` | Writes content to a file, overwriting existing content. |
| `object_store_pdf_to_markdown` | Converts a PDF to markdown. |

### Datasets and Environment
| Tool | Description |
|------|-------------|
| `list_datasets` | Lists available dataset names. |
| `get_dataset_details` | Gets full details for a dataset. |
| `environment_library_support` | Lists preinstalled libraries. |

### Skills
| Tool | Description |
|------|-------------|
| `list_skills` | Lists available skills. |
| `load_skill` | Loads a skill by name. |

### Notifications
| Tool | Description |
|------|-------------|
| `send_email_notification` | Sends a live trading email notification. |
| `send_sms_notification` | Sends a live trading SMS notification. |
| `send_telegram_notification` | Sends a live trading Telegram notification. |

## Other Clients

The remote server also works with Copilot, Cursor, Devin Desktop, and any other client that supports the MCP HTTP transport. Setup guides for each are in the [MCP Server documentation](https://www.quantconnect.com/docs/v2/ai-assistance/mcp-server).

## Troubleshooting

If a tool call fails, check the [QuantConnect status page](https://status.quantconnect.com/) and the [Anthropic status page](https://status.anthropic.com/). The QuantConnect API imposes no quotas on MCP usage; Claude's own usage limits still apply.

## Looking for the old code?

The previous local server implementation remains available in this repository's git history. It is no longer maintained or supported.
