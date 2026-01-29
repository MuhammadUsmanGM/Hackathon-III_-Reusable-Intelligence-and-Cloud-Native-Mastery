# Skills Library

This repository contains reusable skills for Claude Code and Goose that implement the MCP Code Execution pattern.

## Structure

```
.claude/skills/
├── agents-md-gen/
├── kafka-k8s-setup/
├── postgres-k8s-setup/
├── fastapi-dapr-agent/
├── mcp-code-execution/
├── nextjs-k8s-deploy/
└── docusaurus-deploy/
```

Each skill follows the pattern:
- `SKILL.md` - Minimal instructions (~100 tokens)
- `REFERENCE.md` - Detailed documentation (loaded on demand)
- `scripts/` - Actual implementation code (executed, not loaded in context)

## Purpose

These skills teach AI agents how to build cloud-native applications autonomously using best practices for token efficiency and cross-agent compatibility.