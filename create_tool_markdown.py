"""
This script generates the markdown for the table of available tools and
the description of each tool. To run this script, follow these steps:

 1) Start the inspector.

     `npx @modelcontextprotocol/inspector uv run src/main.py`

 2) In the inspector, connect to the server and then click List Tools.

 3) Copy the response JSON and save it on your local machine as tool_list.json.

 4) Run `python create_tool_markdown.py`.
"""

import json

def clean_description(description):
    # Split by period to get the first sentence, then strip and normalize whitespace
    first_sentence = description.split('.')[0]
    # Replace multiple whitespace characters (spaces, tabs, newlines) with a single space
    cleaned = ' '.join(first_sentence.split())
    return cleaned + '.'  # Add period back to end

def create_tools_table(tools):
    content = f"## Available Tools ({len(tools)})\n"
    content += "| Tools provided by this Server | Short Description |\n"
    content += "| -------- | ------- |\n"
    for tool in tools:
        content += f"| `{tool['name']}` | {clean_description(tool['description'])} |\n"
    content += " --- \n"
    return content

def create_tool_details(tools):
    content = "## Tool Details\n"
    for tool in tools:
        print('Tool:', tool['name'])
        content += f"**Tool:** `{tool['name']}`\n"
        content += f"\n{clean_description(tool['description'])}\n"
        properties = tool['inputSchema']['properties'].get('model', None)
        if properties:
            #print('Property: ', properties)
            content += "\n| Parameter | Type | Description |\n"
            content += "| -------- | ------- | ------- |\n"
            defs = tool['inputSchema'].get('$defs', {})
            input_model_name = properties['$ref'].split("/")[-1]
            model_name = input_model_name
            for name, meta in defs[model_name]['properties'].items():
                print(' property:', name)
                required = name in defs[input_model_name].get('required', [])
                if 'type' in meta:
                    data_type = meta['type'] 
                elif 'anyOf' in meta:
                    # Instead of listing enum values, let's just put a
                    # placeholder for these cases:
                    if name in ['brokerage', 'dataProviders']:
                        data_type = 'object'
                    elif name == 'status':
                        data_type = 'status enum'
                    elif name == 'format':
                        data_type = ''
                    else:
                        data_type = meta['anyOf'][0]['type']
                elif '$ref' in meta:
                    model_name = meta['$ref'].split("/")[-1]
                    data_type = defs[model_name]['type']
                description = meta.get('description', '')
                first_line = description.splitlines()[0] if description else ''
                optional_suffix = '' if required else '*optional*'
                content += (
                    f"| `{name}` | `{data_type}` {optional_suffix} | {first_line} |\n"
                )

        # These default values come from  https://modelcontextprotocol.io/docs/concepts/tools#available-tool-annotations
        read_only = tool['annotations'].get('readOnlyHint', False)
        if read_only:
            content += "\n*This tool doesn't modify it's environment.*\n"
        else: 
            content += "\n*This tool modifies it's environment.*\n"

            if tool['annotations'].get('destructiveHint', True):
                content += "\n*This tool may perform destructive updates.*\n"
            else:
                content += "\n*This tool doesn't perform destructive updates.*\n"
                
            if tool['annotations'].get('idempotentHint', False):
                content += "\n*Calling this tool repeatedly with the same arguments has no additional effect.*\n"
            else:
                content += "\n*Calling this tool repeatedly with the same arguments has additional effects.*\n"

        if tool['annotations'].get('openWorldHint', True):
            content += "\n*This tool may interact with an \"open world\" of external entities.*\n"
        else:
            content += "\n*This tool doesn't interact with an \"open world\" of external entities.*\n"

        content += "\n---\n"
    return content

def document(tools, output_file="README.md"):
    content = create_tools_table(tools)
    content += create_tool_details(tools)
    with open(output_file, 'w') as f:
        f.write(content)
    print(f"README generated successfully at {output_file}")

if __name__ == "__main__":
    with open('tool_list.json', 'r') as f:
        document(json.load(f)['tools'])
