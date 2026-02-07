# Skill Development Guide

This guide outlines the standards and best practices for creating reusable intelligence units (Skills) for Claude Code, Goose, and other AI agents.

## The Skill Paradigm
A Skill is more than documentation; it's a piece of executable intelligence that teaches an AI agent how to perform a complex task autonomously.

## Core Components
Every skill must follow this directory structure:
```
.claude/skills/<skill-name>/
├── SKILL.md              # High-level instructions (low token cost)
├── REFERENCE.md          # Deep technical documentation (context on-demand)
└── scripts/              # Executable logic (0 token cost at rest)
    ├── deploy.sh
    ├── verify.py
    └── ...
```

## Writing the SKILL.md
- **Frontmatter**: Must include `name` and `description`.
- **When to Use**: Clear triggers for the agent.
- **Instructions**: Step-by-step actions for the agent to take.
- **Validation**: Success criteria the agent must verify.

## MCP Code Execution Pattern
To optimize for token efficiency and agent speed:
1. **Move Logic to Scripts**: Don't ask the agent to write complex boilerplate. Provide a script that generates it.
2. **Execute, Don't Read**: The agent should call `./scripts/do-something.sh` rather than reading 500 lines of code.
3. **Control Output**: Scripts should return concise, actionable status updates (e.g., "✓ Success" or "✗ Failed: [Error]") to keep the context window clear.

## Testing Skills
- **Autonomy Test**: Single prompt → Agent completes task → Output is correct.
- **Cross-Agent Test**: Verify the skill works in both Claude Code and Goose.
- **Token Check**: Verify that the context consumption remains low throughout the execution.

---
*Created as part of Hackathon III: Reusable Intelligence and Cloud-Native Mastery.*
