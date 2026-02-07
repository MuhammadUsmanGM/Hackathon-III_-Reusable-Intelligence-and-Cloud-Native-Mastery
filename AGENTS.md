# LearnFlow - Agent Readiness Guide

This repository is designed for agentic collaboration. Following these guidelines ensures that AI coding agents like Claude Code and Goose can interact efficiently and effectively with the codebase.

## Repository Overview
LearnFlow is an AI-powered Python tutoring platform with a multi-agent architecture.

- **Frontend**: Next.js 15, TypeScript, Tailwind CSS, Monaco Editor.
- **Backend**: FastAPI, Python, PostgreSQL, Kafka, Dapr.
- **Skills**: Reusable skills located in the `skills-library` repository.

## Coding Standards
- **Python**: Follow PEP 8. Use type hints for all function signatures.
- **TypeScript**: Use strict typing. Prefer functional components and hooks.
- **CSS**: Use Tailwind CSS for styling. Adhere to the Emerald Green core design system.

## Agentic Workflow
- **Commit Messages**: All commits made by AI agents must be prefixed with the agent's name (e.g., `Claude:`, `Goose:`).
- **Skills**: Reference and utilize skills from `.claude/skills/` whenever possible.
- **MCP Pattern**: Use the MCP Code Execution pattern (SKILL.md + scripts/) to minimize token consumption and maximize efficiency.

## Key Directories
- `learnflow-app/backend/agents`: Core AI agent implementations.
- `learnflow-app/backend/services`: Business logic and service integrations (Kafka, Dapr).
- `learnflow-app/frontend/app`: Next.js application routes and components.
- `skills-library/.claude/skills`: Reusable intelligence components.

## Development Tasks for Agents
1. **Adding Features**: Create a technical specification first, then implement logic using specialized skills.
2. **Infrastructure**: Use the `k8s-foundation` and `infra-setup` skills for deployment tasks.
3. **Refactoring**: Ensure that refactoring adheres to the modular multi-agent architecture.

## Tooling
- **Claude Code**: Primary agent for code generation and refactoring.
- **Goose**: Primary agent for local orchestration and recipe execution.
- **Minikube**: Local Kubernetes environment for testing deployments.

---
*Created as part of Hackathon III: Reusable Intelligence and Cloud-Native Mastery.*
