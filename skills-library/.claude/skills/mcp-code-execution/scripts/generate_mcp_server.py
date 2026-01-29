#!/usr/bin/env python3
"""
Generate an MCP server with code execution pattern
"""
import os
import sys
import argparse
from pathlib import Path

def create_mcp_server(server_name, output_dir):
    """Create an MCP server with code execution pattern"""

    # Create the server directory
    server_dir = Path(output_dir) / server_name
    server_dir.mkdir(parents=True, exist_ok=True)

    # Create main server file
    server_content = f'''import asyncio
import json
import logging
from typing import Dict, Any, List
from pydantic import BaseModel
import aiohttp
from aiohttp import web

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ToolCall(BaseModel):
    """Represents a tool call from the model"""
    id: str
    name: str
    arguments: Dict[str, Any]

class ToolResult(BaseModel):
    """Represents the result of a tool call"""
    tool_call_id: str
    content: str
    is_error: bool = False

class MCPHandler:
    def __init__(self):
        self.tools = {{
            "execute_bash_command": self.execute_bash_command,
            "read_file": self.read_file,
            "write_file": self.write_file,
            "list_directory": self.list_directory,
        }}

    async def execute_bash_command(self, command: str) -> str:
        """Execute a bash command and return the result"""
        try:
            proc = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()

            result = {{
                "stdout": stdout.decode(),
                "stderr": stderr.decode(),
                "return_code": proc.returncode
            }}
            return json.dumps(result, indent=2)
        except Exception as e:
            return json.dumps({{"error": str(e)}})

    async def read_file(self, filepath: str) -> str:
        """Read a file and return its content"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except Exception as e:
            return json.dumps({{"error": str(e)}})

    async def write_file(self, filepath: str, content: str) -> str:
        """Write content to a file"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Successfully wrote to {{filepath}}"
        except Exception as e:
            return json.dumps({{"error": str(e)}})

    async def list_directory(self, dirpath: str = ".") -> str:
        """List the contents of a directory"""
        try:
            import os
            items = os.listdir(dirpath)
            return json.dumps(items, indent=2)
        except Exception as e:
            return json.dumps({{"error": str(e)}})

    async def handle_request(self, tools: List[Dict[str, Any]]) -> List[ToolResult]:
        """Handle a request with multiple tool calls"""
        results = []

        for tool_call in tools:
            tool_name = tool_call.get("name")
            arguments = tool_call.get("arguments", {{}})
            tool_call_id = tool_call.get("id", "unknown")

            logger.info(f"Executing tool: {{tool_name}} with args: {{arguments}}")

            if tool_name in self.tools:
                try:
                    result = await self.tools[tool_name](**arguments)
                    results.append(ToolResult(tool_call_id=tool_call_id, content=result))
                except Exception as e:
                    error_result = json.dumps({{"error": str(e)}})
                    results.append(ToolResult(tool_call_id=tool_call_id, content=error_result, is_error=True))
            else:
                error_result = json.dumps({{"error": f"Unknown tool: {{tool_name}}"}})
                results.append(ToolResult(tool_call_id=tool_call_id, content=error_result, is_error=True))

        return results

# Global handler instance
handler = MCPHandler()

async def mcp_handler(request):
    """HTTP handler for MCP requests"""
    try:
        data = await request.json()
        tools = data.get("tools", [])

        results = await handler.handle_request(tools)

        return web.json_response([{{"tool_call_id": r.tool_call_id, "content": r.content, "is_error": r.is_error}} for r in results])
    except Exception as e:
        logger.error(f"Error processing request: {{e}}")
        return web.json_response({{"error": str(e)}}, status=500)

def create_app():
    """Create the aiohttp application"""
    app = web.Application()
    app.router.add_post('/execute', mcp_handler)
    return app

if __name__ == "__main__":
    app = create_app()
    web.run_app(app, host='localhost', port=8080)
'''

    with open(server_dir / "mcp_server.py", 'w') as f:
        f.write(server_content)

    # Create requirements.txt
    requirements_content = '''aiohttp==3.9.0
pydantic==2.5.0
python-dotenv==1.0.0
asyncio-mqtt==0.13.0
websockets==12.0
'''

    with open(server_dir / "requirements.txt", 'w') as f:
        f.write(requirements_content)

    # Create client script
    client_content = f'''#!/usr/bin/env python3
"""
Client script for interacting with the MCP server
"""
import asyncio
import aiohttp
import json

async def call_mcp_server(url, tools):
    """Call the MCP server with a list of tools to execute"""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json={{"tools": tools}}) as response:
                result = await response.text()
                return json.loads(result)
        except Exception as e:
            return {{"error": str(e)}}

# Example usage
async def main():
    # Example tool call to execute bash command
    tools = [
        {{
            "id": "1",
            "name": "execute_bash_command",
            "arguments": {{"command": "echo 'Hello from MCP server!'"}}
        }},
        {{
            "id": "2",
            "name": "list_directory",
            "arguments": {{"dirpath": "."}}
        }}
    ]

    result = await call_mcp_server("http://localhost:8080/execute", tools)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
'''

    with open(server_dir / "client.py", 'w') as f:
        f.write(client_content)

    # Create Dockerfile
    dockerfile_content = f'''FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "mcp_server.py"]
'''

    with open(server_dir / "Dockerfile", 'w') as f:
        f.write(dockerfile_content)

    print(f"✓ MCP server with code execution pattern created at {server_dir}")

def main():
    parser = argparse.ArgumentParser(description='Generate MCP server with code execution pattern')
    parser.add_argument('server_name', help='Name of the server')
    parser.add_argument('--output', '-o', default='.', help='Output directory (default: current directory)')

    args = parser.parse_args()

    create_mcp_server(args.server_name, args.output)

if __name__ == "__main__":
    main()