#!/usr/bin/env python3
"""
Create a client script for MCP server interaction
"""
import os
import sys
import argparse
from pathlib import Path

def create_client_script(script_name, output_dir):
    """Create a client script for MCP server interaction"""

    # Create the client script
    client_content = f'''#!/usr/bin/env python3
"""
MCP Client Script: {script_name}
Interacts with an MCP server using the code execution pattern
"""
import asyncio
import aiohttp
import json
import argparse
import sys
from typing import Dict, Any, List

async def call_mcp_server(server_url: str, tools: List[Dict[str, Any]], headers: Dict[str, str] = None):
    """
    Call the MCP server with a list of tools to execute

    Args:
        server_url: URL of the MCP server
        tools: List of tool definitions to execute
        headers: Optional headers to include in the request

    Returns:
        Response from the MCP server
    """
    if headers is None:
        headers = {{"Content-Type": "application/json"}}

    async with aiohttp.ClientSession() as session:
        try:
            print(f"Sending request to MCP server: {{server_url}}")
            async with session.post(server_url, json={{"tools": tools}}, headers=headers) as response:
                result = await response.text()

                # Parse and pretty-print the result
                try:
                    parsed_result = json.loads(result)
                    print("MCP Server Response:")
                    print(json.dumps(parsed_result, indent=2))
                    return parsed_result
                except json.JSONDecodeError:
                    print("Raw response:", result)
                    return result
        except aiohttp.ClientConnectorError:
            print(f"Error: Could not connect to MCP server at {{server_url}}")
            return None
        except Exception as e:
            print(f"Error calling MCP server: {{e}}")
            return {{"error": str(e)}}

async def execute_single_tool(server_url: str, tool_name: str, arguments: Dict[str, Any]):
    """
    Execute a single tool on the MCP server

    Args:
        server_url: URL of the MCP server
        tool_name: Name of the tool to execute
        arguments: Arguments to pass to the tool
    """
    tools = [
        {{
            "id": "1",
            "name": tool_name,
            "arguments": arguments
        }}
    ]

    result = await call_mcp_server(server_url, tools)
    return result

async def main():
    parser = argparse.ArgumentParser(description='{script_name} - MCP Client Script')
    parser.add_argument("--server-url", default="http://localhost:8080/execute",
                       help="URL of the MCP server (default: http://localhost:8080/execute)")
    parser.add_argument("--tool", required=True,
                       help="Name of the tool to execute")
    parser.add_argument("--args", required=True,
                       help="Arguments for the tool as JSON string")

    args = parser.parse_args()

    try:
        tool_args = json.loads(args.args)
    except json.JSONDecodeError:
        print("Error: Invalid JSON in arguments")
        sys.exit(1)

    result = await execute_single_tool(args.server_url, args.tool, tool_args)

    if result is None:
        sys.exit(1)

    # Exit with error code if there were errors in the response
    if isinstance(result, list):
        for item in result:
            if item.get('is_error'):
                sys.exit(1)
    elif isinstance(result, dict) and result.get('error'):
        sys.exit(1)

# Example usage functions
async def example_usage():
    """Demonstrate various ways to use the MCP client"""

    server_url = "http://localhost:8080/execute"

    # Example 1: Execute a bash command
    print("Example 1: Executing bash command")
    tools = [
        {{
            "id": "cmd1",
            "name": "execute_bash_command",
            "arguments": {{"command": "pwd && ls -la"}}
        }}
    ]
    await call_mcp_server(server_url, tools)

    print("\\n" + "="*50 + "\\n")

    # Example 2: Read a file
    print("Example 2: Reading a file")
    tools = [
        {{
            "id": "read1",
            "name": "read_file",
            "arguments": {{"filepath": "./README.md"}}
        }}
    ]
    await call_mcp_server(server_url, tools)

    print("\\n" + "="*50 + "\\n")

    # Example 3: Multiple operations
    print("Example 3: Multiple operations")
    tools = [
        {{
            "id": "list1",
            "name": "list_directory",
            "arguments": {{"dirpath": "."}}
        }},
        {{
            "id": "cmd2",
            "name": "execute_bash_command",
            "arguments": {{"command": "date"}}
        }}
    ]
    await call_mcp_server(server_url, tools)

if __name__ == "__main__":
    # If called with no arguments, show help
    if len(sys.argv) == 1:
        print(f"Usage: python {sys.argv[0]} --server-url <URL> --tool <TOOL_NAME> --args '<JSON_ARGS>'")
        print("Example: python {sys.argv[0]} --server-url http://localhost:8080/execute --tool execute_bash_command --args '{\"command\":\"echo hello world\"}'")
        sys.exit(1)

    # Run the main function
    asyncio.run(main())
'''

    output_file = Path(output_dir) / f"{script_name}_client.py"
    with open(output_file, 'w') as f:
        f.write(client_content)

    # Make the script executable
    os.chmod(output_file, 0o755)

    print(f"✓ MCP client script created at {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Create MCP client script')
    parser.add_argument('script_name', help='Name of the client script')
    parser.add_argument('--output', '-o', default='.', help='Output directory (default: current directory)')

    args = parser.parse_args()

    create_client_script(args.script_name, args.output)

if __name__ == "__main__":
    main()