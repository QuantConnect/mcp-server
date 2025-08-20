
<img width="1575" height="280" alt="github-header" src="https://github.com/user-attachments/assets/6cec1ef7-0340-416e-ab81-c73fbc8ff847" />


# QuantConnect MCP Server
The QuantConnect MCP Server is a bridge for AIs (such as Claude and OpenAI o3 Pro) to interact with our cloud platform. When equipped with our MCP, the AI can perform tasks on your behalf through our API such as updating projects, writing strategies, backtesting, and deploying strategies to production live-trading.

Our implementation is tested and dockerized for easy cross-platform deployment.

## Getting Started
To connect local MCP clients (like Claude Desktop) to the QC MCP Server, follow these steps:

1. Install and open [Docker Desktop](https://docs.docker.com/desktop/).
2. Install and open [Claude Desktop](https://claude.ai/download).
3. In Claude Desktop, click **File > Settings > Developer > Edit Config**.
4. Edit the `claude_desktop_config.json` file to include the following `quantconnect` configuration:

```json
{
  "mcpServers": {
    "quantconnect": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e", "QUANTCONNECT_USER_ID",
        "-e", "QUANTCONNECT_API_TOKEN",
        "-e", "AGENT_NAME",
        "--platform", "<your_platform>",
        "--name",
        "quantconnect-mcp-server",
        "quantconnect/mcp-server"
      ],
      "env": {
        "QUANTCONNECT_USER_ID": "<your_user_id>",
        "QUANTCONNECT_API_TOKEN": "<your_api_token>",
        "AGENT_NAME": "MCP Server"
      }
    }
  }
}
```

  To get your user Id and API token, see [Request API Token](https://www.quantconnect.com/docs/v2/cloud-platform/community/profile#09-Request-API-Token).

  Our MCP server is multi-platform capable. The options are `linux/amd64` for Intel/AMD chips and `linux/arm64` for ARM chips (for example, Apple's M-series chips).

  If you simultaneously run multiple agents, set a unique value for the `AGENT_NAME` environment variable for each agent to keep record of the request source. 

5. Restart Claude Desktop.

   Claude Desktop automatically pulls our MCP server from Docker Hub and connects to it.

To view all the MCP clients and the features they support, see the [Feature Support Matrix](https://modelcontextprotocol.io/clients#feature-support-matrix) in the MCP documentation.

To keep the Docker image up-to-date, pull the latest MCP server from Docker Hub in the terminal.
```
docker pull quantconnect/mcp-server
```
If you have an ARM chip, add the `--platform linux/arm64` option.

## Available Tools (60)
| Tools provided by this Server | Short Description |
| -------- | ------- |
| `read_account` | Read the organization account status. |
| `create_project` | Create a new project in your default organization. |
| `read_project` | List the details of a project. |
| `list_projects` | List the details of all projects. |
| `update_project` | Update a project's name or description. |
| `delete_project` | Delete a project. |
| `create_project_collaborator` | Add a collaborator to a project. |
| `read_project_collaborators` | List all collaborators on a project. |
| `update_project_collaborator` | Update collaborator information in a project. |
| `delete_project_collaborator` | Remove a collaborator from a project. |
| `read_project_nodes` | Read the available and selected nodes of a project. |
| `update_project_nodes` | Update the active state of the given nodes to true. |
| `create_compile` | Asynchronously create a compile job request for a project. |
| `read_compile` | Read a compile packet job result. |
| `create_file` | Add a file to a given project. |
| `read_file` | Read a file from a project, or all files in the project if no file name is provided. |
| `update_file_name` | Update the name of a file. |
| `update_file_contents` | Update the contents of a file. |
| `delete_file` | Delete a file in a project. |
| `create_backtest` | Create a new backtest request and get the backtest Id. |
| `read_backtest` | Read the results of a backtest. |
| `list_backtests` | List all the backtests for the project. |
| `read_backtest_chart` | Read a chart from a backtest. |
| `read_backtest_orders` | Read out the orders of a backtest. |
| `read_backtest_insights` | Read out the insights of a backtest. |
| `update_backtest` | Update the name or note of a backtest. |
| `delete_backtest` | Delete a backtest from a project. |
| `estimate_optimization_time` | Estimate the execution time of an optimization with the specified parameters. |
| `create_optimization` | Create an optimization with the specified parameters. |
| `read_optimization` | Read an optimization. |
| `list_optimizations` | List all the optimizations for a project. |
| `update_optimization` | Update the name of an optimization. |
| `abort_optimization` | Abort an optimization. |
| `delete_optimization` | Delete an optimization. |
| `authorize_connection` | Authorize an external connection with a live brokerage or data provider. |
| `create_live_algorithm` | Create a live algorithm. |
| `read_live_algorithm` | Read details of a live algorithm. |
| `list_live_algorithms` | List all your past and current live trading deployments. |
| `read_live_chart` | Read a chart from a live algorithm. |
| `read_live_logs` | Get the logs of a live algorithm. |
| `read_live_portfolio` | Read out the portfolio state of a live algorithm. |
| `read_live_orders` | Read out the orders of a live algorithm. |
| `read_live_insights` | Read out the insights of a live algorithm. |
| `stop_live_algorithm` | Stop a live algorithm. |
| `liquidate_live_algorithm` | Liquidate and stop a live algorithm. |
| `create_live_command` | Send a command to a live trading algorithm. |
| `broadcast_live_command` | Broadcast a live command to all live algorithms in an organization. |
| `upload_object` | Upload files to the Object Store. |
| `read_object_properties` | Get Object Store properties of a specific organization and key. |
| `read_object_store_file_job_id` | Create a job to download files from the Object Store and then read the job Id. |
| `read_object_store_file_download_url` | Get the URL for downloading files from the Object Store. |
| `list_object_store_files` | List the Object Store files under a specific directory in an organization. |
| `delete_object` | Delete the Object Store file of a specific organization and key. |
| `read_lean_versions` | Returns a list of LEAN versions with basic information for each version. |
| `check_initialization_errors` | Run a backtest for a few seconds to initialize the algorithm and get initialization errors if any. |
| `complete_code` | Show the code completion for a specific text input. |
| `enhance_error_message` | Show additional context and suggestions for error messages. |
| `update_code_to_pep8` | Update Python code to follow PEP8 style. |
| `check_syntax` | Check the syntax of a code. |
| `search_quantconnect` | Search for content in QuantConnect. |

 --- 
## Tool Details
**Tool:** `read_account`

Read the organization account status.

*This tool doesn't modify it's environment.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `create_project`

Create a new project in your default organization.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `name` | `string`  | Project name. |
| `language` | `string`  | Programming language to use. |
| `organizationId` | `string` *optional* | The organization to create project under. If you don't provide a value, it defaults to your preferred organization. |

*This tool modifies it's environment.*

*This tool doesn't perform destructive updates.*

*Calling this tool repeatedly with the same arguments has additional effects.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `read_project`

List the details of a project.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `projectId` | `integer`  | Id of the project. If not provided the API will return a details list of all projects. |

*This tool doesn't modify it's environment.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `list_projects`

List the details of all projects.

*This tool doesn't modify it's environment.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `update_project`

Update a project's name or description.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `projectId` | `integer`  | Project Id to which the file belongs. |
| `name` | `string` *optional* | The new name for the project. |
| `description` | `string` *optional* | The new description for the project. |

*This tool modifies it's environment.*

*This tool may perform destructive updates.*

*Calling this tool repeatedly with the same arguments has no additional effect.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `delete_project`

Delete a project.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `projectId` | `integer`  | Id of the project to delete. |

*This tool modifies it's environment.*

*This tool may perform destructive updates.*

*Calling this tool repeatedly with the same arguments has no additional effect.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `create_project_collaborator`

Add a collaborator to a project.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `projectId` | `integer`  | Id of the project to add the collaborator to. |
| `collaboratorUserId` | `string`  | User Id of the collaborator to add. |
| `collaborationLiveControl` | `boolean`  | Gives the right to deploy and stop live algorithms. |
| `collaborationWrite` | `boolean`  | Gives the right to edit the code. |

*This tool modifies it's environment.*

*This tool doesn't perform destructive updates.*

*Calling this tool repeatedly with the same arguments has no additional effect.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `read_project_collaborators`

List all collaborators on a project.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `projectId` | `integer`  | Id of the project from which to read the collaborators. |

*This tool doesn't modify it's environment.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `update_project_collaborator`

Update collaborator information in a project.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `projectId` | `integer`  | Id of the project the collaborator is on. |
| `collaboratorUserId` | `string`  | User Id of the collaborator to update. |
| `liveControl` | `boolean`  | Gives the right to deploy and stop live algorithms. |
| `write` | `boolean`  | Gives the right to edit the code. |

*This tool modifies it's environment.*

*This tool may perform destructive updates.*

*Calling this tool repeatedly with the same arguments has no additional effect.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `delete_project_collaborator`

Remove a collaborator from a project.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `projectId` | `integer`  | Id of the project to remove the collaborator from. |
| `collaboratorId` | `string`  | User Id of the collaborator to remove. |

*This tool modifies it's environment.*

*This tool may perform destructive updates.*

*Calling this tool repeatedly with the same arguments has no additional effect.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `read_project_nodes`

Read the available and selected nodes of a project.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `projectId` | `integer`  | Id of the project to which the nodes refer. |

*This tool doesn't modify it's environment.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `update_project_nodes`

Update the active state of the given nodes to true.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `projectId` | `integer`  | Project Id to which the nodes refer. |
| `nodes` | `array` *optional* | List of node Ids the project may use. If you omit this property or pass an empty list, the best node will be automatically selected for backtest, research, and live trading. |

*This tool modifies it's environment.*

*This tool doesn't perform destructive updates.*

*Calling this tool repeatedly with the same arguments has no additional effect.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `create_compile`

Asynchronously create a compile job request for a project.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `projectId` | `integer`  | Id of the project to compile. |

*This tool modifies it's environment.*

*This tool doesn't perform destructive updates.*

*Calling this tool repeatedly with the same arguments has additional effects.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `read_compile`

Read a compile packet job result.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `projectId` | `integer`  | Id of the project you requested to compile. |
| `compileId` | `string`  | Compile Id returned during the creation request. |

*This tool doesn't modify it's environment.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `create_file`

Add a file to a given project.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `projectId` | `integer`  | Id of the project to add the file. |
| `name` | `string`  | The name of the new file. |
| `content` | `string` *optional* | The content of the new file. |
| `codeSourceId` | `string` *optional* | Name of the environment that's creating the request. |

*This tool modifies it's environment.*

*This tool doesn't perform destructive updates.*

*Calling this tool repeatedly with the same arguments has no additional effect.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `read_file`

Read a file from a project, or all files in the project if no file name is provided.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `projectId` | `integer`  | Id of the project that contains the file. |
| `name` | `string` *optional* | The name of the file to read. |
| `codeSourceId` | `string` *optional* | Name of the environment that's creating the request. |

*This tool doesn't modify it's environment.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `update_file_name`

Update the name of a file.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `projectId` | `integer`  | Id of the project that contains the file. |
| `name` | `string`  | The current name of the file. |
| `newName` | `string`  | The new name for the file. |
| `codeSourceId` | `string` *optional* | Name of the environment that's creating the request. |

*This tool modifies it's environment.*

*This tool may perform destructive updates.*

*Calling this tool repeatedly with the same arguments has no additional effect.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `update_file_contents`

Update the contents of a file.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `projectId` | `integer`  | Id of the project that contains the file. |
| `name` | `string`  | The name of the file to update. |
| `content` | `string`  | The new contents of the file. |
| `codeSourceId` | `string` *optional* | Name of the environment that's creating the request. |

*This tool modifies it's environment.*

*This tool may perform destructive updates.*

*Calling this tool repeatedly with the same arguments has no additional effect.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `delete_file`

Delete a file in a project.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `projectId` | `integer`  | Id of the project that contains the file. |
| `name` | `string`  | The name of the file to delete. |
| `codeSourceId` | `string` *optional* | Name of the environment that's creating the request. |

*This tool modifies it's environment.*

*This tool may perform destructive updates.*

*Calling this tool repeatedly with the same arguments has no additional effect.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `create_backtest`

Create a new backtest request and get the backtest Id.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `projectId` | `integer`  | Id of the project to backtest. |
| `compileId` | `string`  | Compile Id for the project to backtest. |
| `backtestName` | `string`  | Name for the new backtest. |
| `parameters` | `object` *optional* | Parameters to use for the backtest. |

*This tool modifies it's environment.*

*This tool doesn't perform destructive updates.*

*Calling this tool repeatedly with the same arguments has additional effects.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `read_backtest`

Read the results of a backtest.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `projectId` | `integer`  | Id of the project that contains the backtest. |
| `backtestId` | `string`  | Id of the backtest to read. |

*This tool doesn't modify it's environment.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `list_backtests`

List all the backtests for the project.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `projectId` | `integer`  | Id of the project from which to read one or multiple backtests. |
| `includeStatistics` | `boolean` *optional* | If true, the backtests summaries from the response will contain the statistics with their corresponding values. |

*This tool doesn't modify it's environment.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `read_backtest_chart`

Read a chart from a backtest.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `projectId` | `integer`  | Id of the project that contains the backtest. |
| `backtestId` | `string`  | Id of the backtest for this chart request. |
| `name` | `string`  | The requested chart name. |
| `count` | `integer`  | The number of data points to request. |
| `start` | `integer`  | The start timestamp of the request in Unix time. |
| `end` | `integer`  | The end timestamp of the request in Unix time. |

*This tool doesn't modify it's environment.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `read_backtest_orders`

Read out the orders of a backtest.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `start` | `integer`  | Starting index of the orders to be fetched. |
| `end` | `integer`  | Last index of the orders to be fetched. Note that end - start must be less than 100. |
| `projectId` | `integer`  | Id of the project from which to read the backtest. |
| `backtestId` | `string`  | Id of the backtest from which to read the orders. |

*This tool doesn't modify it's environment.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `read_backtest_insights`

Read out the insights of a backtest.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `start` | `integer`  | Starting index of the insights to be fetched. |
| `end` | `integer`  | Last index of the insights to be fetched. Note that end - start must be less than 100. |
| `projectId` | `integer`  | Id of the project from which to read the backtest. |
| `backtestId` | `string`  | Id of the backtest from which to read the insights. |

*This tool doesn't modify it's environment.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `update_backtest`

Update the name or note of a backtest.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `projectId` | `integer`  | Id of the project that contains the backtest. |
| `backtestId` | `string`  | Id of the backtest to update. |
| `name` | `string` *optional* | Name to assign to the backtest. |
| `note` | `string` *optional* | Note to attach to the backtest. |

*This tool modifies it's environment.*

*This tool may perform destructive updates.*

*Calling this tool repeatedly with the same arguments has no additional effect.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `delete_backtest`

Delete a backtest from a project.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `projectId` | `integer`  | Id of the project that contains the backtest. |
| `backtestId` | `string`  | Id of the backtest to delete. |

*This tool modifies it's environment.*

*This tool may perform destructive updates.*

*Calling this tool repeatedly with the same arguments has no additional effect.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `estimate_optimization_time`

Estimate the execution time of an optimization with the specified parameters.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `projectId` | `integer`  | Id of the project to optimize. |
| `name` | `string`  | Name of the optimization. |
| `target` | `string`  | Target statistic of the optimization to minimize or maximize. |
| `targetTo` | `string`  | Target extremum of the optimization. |
| `targetValue` | `number` *optional* | Desired value for the optimization target statistic. |
| `strategy` | `string`  | Optimization strategy. |
| `compileId` | `string` *optional* | Optimization compile Id. |
| `parameters` | `array`  | Optimization parameters. |
| `constraints` | `array` *optional* | Optimization constraints. |

*This tool doesn't modify it's environment.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `create_optimization`

Create an optimization with the specified parameters.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `projectId` | `integer`  | Id of the project to optimize. |
| `name` | `string`  | Name of the optimization. |
| `target` | `string`  | Target statistic of the optimization to minimize or maximize. |
| `targetTo` | `string`  | Target extremum of the optimization. |
| `targetValue` | `number` *optional* | Desired value for the optimization target statistic. |
| `strategy` | `string`  | Optimization strategy. |
| `compileId` | `string`  | Optimization compile Id. |
| `parameters` | `array`  | Optimization parameters. |
| `constraints` | `array` *optional* | Optimization constraints. |
| `estimatedCost` | `number`  | Estimated cost for optimization. |
| `nodeType` | `string`  | Optimization node type. |
| `parallelNodes` | `integer`  | Number of parallel nodes for optimization. |

*This tool modifies it's environment.*

*This tool doesn't perform destructive updates.*

*Calling this tool repeatedly with the same arguments has additional effects.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `read_optimization`

Read an optimization.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `optimizationId` | `string`  | Id of the optimization to read. |

*This tool doesn't modify it's environment.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `list_optimizations`

List all the optimizations for a project.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `projectId` | `integer`  | Id of the Project to get a list of optimizations for. |

*This tool doesn't modify it's environment.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `update_optimization`

Update the name of an optimization.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `optimizationId` | `string`  | Id of the optimization to update. |
| `name` | `string`  | Name to assign to the optimization. |

*This tool modifies it's environment.*

*This tool may perform destructive updates.*

*Calling this tool repeatedly with the same arguments has no additional effect.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `abort_optimization`

Abort an optimization.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `optimizationId` | `string`  | Id of the optimization to abort. |

*This tool modifies it's environment.*

*This tool may perform destructive updates.*

*Calling this tool repeatedly with the same arguments has no additional effect.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `delete_optimization`

Delete an optimization.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `optimizationId` | `string`  | Id of the optimization to delete. |

*This tool modifies it's environment.*

*This tool may perform destructive updates.*

*Calling this tool repeatedly with the same arguments has no additional effect.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `authorize_connection`

Authorize an external connection with a live brokerage or data provider.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `brokerage` | `string`  | The brokerage to authenticate a connection with. |

*This tool modifies it's environment.*

*This tool doesn't perform destructive updates.*

*Calling this tool repeatedly with the same arguments has no additional effect.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `create_live_algorithm`

Create a live algorithm.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `versionId` | `string`  | The version of the Lean used to run the algorithm. -1 is master, however, sometimes this can create problems with live deployments. If you experience problems using, try specifying the version of Lean you would like to use. |
| `projectId` | `integer`  | Project Id. |
| `compileId` | `string`  | Compile Id. |
| `nodeId` | `string`  | Id of the node that will run the algorithm. |
| `brokerage` | `brokerage enum`  | Brokerage configuration for the live algorithm. |
| `dataProviders` | `dataProvider(s)` *optional* | Dictionary of data provider configurations to be used in the live algorithm. Provide at least one. The order in which you define the providers defines their order of precedence. |

*This tool modifies it's environment.*

*This tool doesn't perform destructive updates.*

*Calling this tool repeatedly with the same arguments has additional effects.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `read_live_algorithm`

Read details of a live algorithm.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `projectId` | `integer`  | Id of the project to read. |

*This tool modifies it's environment.*

*This tool may perform destructive updates.*

*Calling this tool repeatedly with the same arguments has additional effects.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `list_live_algorithms`

List all your past and current live trading deployments.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `status` | `status enum` *optional* | Status of the live algorithms to include in the response. |

*This tool modifies it's environment.*

*This tool may perform destructive updates.*

*Calling this tool repeatedly with the same arguments has additional effects.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `read_live_chart`

Read a chart from a live algorithm.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `projectId` | `integer`  | Id of the project that's live trading. |
| `name` | `string`  | Name of the chart to read. |
| `count` | `integer`  | The number of data points to request. |
| `start` | `integer`  | The unix start time of the request. |
| `end` | `integer`  | The unix end time of the request. |

*This tool modifies it's environment.*

*This tool may perform destructive updates.*

*Calling this tool repeatedly with the same arguments has additional effects.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `read_live_logs`

Get the logs of a live algorithm.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `format` | `` *optional* | Format of the log results. |
| `projectId` | `integer`  | Id of the project that contains the live running algorithm. |
| `algorithmId` | `string`  | Deploy Id (Algorithm Id) of the live running algorithm. |
| `startLine` | `integer`  | Start line (inclusive) of logs to read. The lines numbers start at 0. |
| `endLine` | `integer`  | End line (exclusive) of logs to read, where endLine - startLine <= 250. |

*This tool modifies it's environment.*

*This tool may perform destructive updates.*

*Calling this tool repeatedly with the same arguments has additional effects.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `read_live_portfolio`

Read out the portfolio state of a live algorithm.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `projectId` | `integer`  | Id of the project from which to read the live algorithm. |

*This tool modifies it's environment.*

*This tool may perform destructive updates.*

*Calling this tool repeatedly with the same arguments has additional effects.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `read_live_orders`

Read out the orders of a live algorithm.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `start` | `integer` *optional* | Starting index of the orders to be fetched. Required if end > 1,000. |
| `end` | `integer`  | Last index of the orders to be fetched. Note that end - start must be less than 1,000. |
| `projectId` | `integer`  | Id of the project from which to read the live algorithm. |

*This tool modifies it's environment.*

*This tool may perform destructive updates.*

*Calling this tool repeatedly with the same arguments has additional effects.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `read_live_insights`

Read out the insights of a live algorithm.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `start` | `integer` *optional* | Starting index of the insights to be fetched. Required if end > 100. |
| `end` | `integer`  | Last index of the insights to be fetched. Note that end - start must be less than 100. |
| `projectId` | `integer`  | Id of the project from which to read the live algorithm. |

*This tool modifies it's environment.*

*This tool may perform destructive updates.*

*Calling this tool repeatedly with the same arguments has additional effects.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `stop_live_algorithm`

Stop a live algorithm.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `projectId` | `integer`  | Id of the project to stop trading live. |

*This tool modifies it's environment.*

*This tool may perform destructive updates.*

*Calling this tool repeatedly with the same arguments has no additional effect.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `liquidate_live_algorithm`

Liquidate and stop a live algorithm.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `projectId` | `integer`  | Project Id for the live instance to liquidate. |

*This tool modifies it's environment.*

*This tool may perform destructive updates.*

*Calling this tool repeatedly with the same arguments has no additional effect.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `create_live_command`

Send a command to a live trading algorithm.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `projectId` | `integer`  | Project for the live instance we want to run the command against. |
| `command` | `object`  | The command to run. |

*This tool modifies it's environment.*

*This tool may perform destructive updates.*

*Calling this tool repeatedly with the same arguments has additional effects.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `broadcast_live_command`

Broadcast a live command to all live algorithms in an organization.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `organizationId` | `string`  | Organization Id of the projects we would like to broadcast the command to |
| `excludeProjectId` | `integer` *optional* | Project for the live instance we want to exclude from the broadcast list. If null, all projects will be included. |
| `command` | `object`  | The command to run. |

*This tool modifies it's environment.*

*This tool may perform destructive updates.*

*Calling this tool repeatedly with the same arguments has additional effects.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `upload_object`

Upload files to the Object Store.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `organizationId` | `string`  | Orgainization ID. |
| `key` | `string`  | Unique key to access the object in Object Store. |
| `objectData` | `string`  | Object data to be stored. |

*This tool modifies it's environment.*

*This tool may perform destructive updates.*

*Calling this tool repeatedly with the same arguments has no additional effect.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `read_object_properties`

Get Object Store properties of a specific organization and key.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `organizationId` | `string`  | Id of the organization that owns the Object Store. |
| `key` | `string`  | Key in the Object Store. |

*This tool doesn't modify it's environment.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `read_object_store_file_job_id`

Create a job to download files from the Object Store and then read the job Id.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `organizationId` | `string`  | Id of the organization that owns the Object Store. |
| `keys` | `array`  | Keys of the Object Store files. |

*This tool modifies it's environment.*

*This tool doesn't perform destructive updates.*

*Calling this tool repeatedly with the same arguments has additional effects.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `read_object_store_file_download_url`

Get the URL for downloading files from the Object Store.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `organizationId` | `string`  | Id of the organization that owns the Object Store. |
| `jobId` | `string`  | Id of the download job for the files. |

*This tool doesn't modify it's environment.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `list_object_store_files`

List the Object Store files under a specific directory in an organization.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `organizationId` | `string`  | Id of the organization to list the Object Store files from. |
| `path` | `string` *optional* | Path to a directory in the Object Store. |

*This tool doesn't modify it's environment.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `delete_object`

Delete the Object Store file of a specific organization and key.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `organizationId` | `string`  | Id of the organization that owns the Object Store. |
| `key` | `string`  | Key of the Object Store file to delete. |

*This tool modifies it's environment.*

*This tool may perform destructive updates.*

*Calling this tool repeatedly with the same arguments has no additional effect.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `read_lean_versions`

Returns a list of LEAN versions with basic information for each version.

*This tool doesn't modify it's environment.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `check_initialization_errors`

Run a backtest for a few seconds to initialize the algorithm and get inialization errors if any.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `language` | `string`  | Programming language. |
| `files` | `array`  | Files to process. |

*This tool doesn't modify it's environment.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `complete_code`

Show the code completion for a specific text input.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `language` | `string`  | Programming language for the code completion. |
| `sentence` | `string`  | Sentence to complete. |
| `responseSizeLimit` | `integer` *optional* | Maximum size of the responses. |

*This tool doesn't modify it's environment.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `enhance_error_message`

Show additional context and suggestions for error messages.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `language` | `string`  | Programming language for the code completion. |
| `error` | `object`  | Error message to enhance. |

*This tool doesn't modify it's environment.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `update_code_to_pep8`

Update Python code to follow PEP8 style.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `files` | `array`  | Files of the project. |

*This tool doesn't modify it's environment.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `check_syntax`

Check the syntax of a code.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `language` | `string`  | Programming language. |
| `files` | `array`  | Files to process. |

*This tool doesn't modify it's environment.*

*This tool may interact with an "open world" of external entities.*

---
**Tool:** `search_quantconnect`

Search for content in QuantConnect.

| Parameter | Type | Description |
| -------- | ------- | ------- |
| `language` | `string`  | Programming language of the content to search. |
| `criteria` | `array`  | Criteria for the search. |

*This tool doesn't modify it's environment.*

*This tool may interact with an "open world" of external entities.*

---


## Debugging

### Build
 To build the Docker image from source, clone this repository and then run `docker build -t quantconnect/mcp-server .`.

### Logs
 To log to the `mcp-server-quantconnect.log` file, `import sys` and then `print("Hello world", file=sys.stderr)`.

### Inspector
 To start the inspector, run `npx @modelcontextprotocol/inspector uv run src/main.py`.
 To pass a model to the inspector tool, use JSON (for example, `{"name":"My Project","language":"Py"}`).
