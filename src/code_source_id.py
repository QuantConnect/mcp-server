import os

# Load the agent name from the environment variables.
AGENT_NAME = os.getenv('AGENT_NAME', 'MCP Server')

def add_code_source_id(model):
    model.codeSourceId = AGENT_NAME
    return model