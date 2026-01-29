# MCP Code Execution - Reference

## Purpose
The mcp-code-execution skill implements the MCP with code execution pattern for token efficiency, allowing AI agents to execute code while minimizing context window bloat.

## Commands
- `generate_mcp_server.py <server-name>`: Creates an MCP server with code execution capabilities
- `create_client_script.py <script-name>`: Creates a client script for MCP interaction
- `test_integration.py <server-name>`: Tests the MCP server integration

## Best Practices
- Keep execution results concise to minimize token usage
- Implement proper error handling in MCP servers
- Use scripts for complex operations instead of loading everything in context
- Validate inputs to prevent code injection

## Common Issues
- Security vulnerabilities in code execution
- Token bloat from verbose outputs
- Network connectivity to MCP servers
- Authentication and authorization challenges