---
name: mcp-code-execution
description: Implement MCP with code execution pattern for token efficiency
---

# MCP Code Execution

## When to Use
- Creating MCP servers that need token-efficient communication
- Implementing scripts that interact with external APIs/data sources
- Reducing context window bloat in AI agents

## Instructions
1. Generate MCP server: `./scripts/generate_mcp_server.py <server-name>`
2. Create client script: `./scripts/create_client_script.py <server-name>`
3. Test integration: `./scripts/test_integration.py <server-name>`

## Validation
- [ ] MCP server responds correctly
- [ ] Client script executes properly
- [ ] Token usage is optimized

See [REFERENCE.md](./REFERENCE.md) for configuration options.