---
sidebar_position: 1
---

# Reusable Intelligence Portal

Welcome to the **LearnFlow Skills Library Documentation**. This portal serves as the definitive guide for using and developing "Reusable Intelligence" units (Skills) that power the LearnFlow platform.

## What are Skills?

In the context of this project, a **Skill** is an emerging industry-standard format for teaching AI agents capabilities. Unlike static documentation, a Skill is an executable unit of intelligence that works across **Claude Code**, **Goose**, and **OpenAI Codex**.

### The MCP Code Execution Pattern

Our skills utilize the **Model Context Protocol (MCP)** with Code Execution. This strategy allows agents to:
1.  **Reduce Token Bloat**: By executing scripts instead of loading boilerplate into context.
2.  **Ensure Consistency**: Standardized logic for Kubernetes, Kafka, and Dapr operations.
3.  **Enhance Autonomy**: Single-prompt deployments with automated verification.

## Core Infrastructure Skills

Our library currently includes the following critical skills:

- **k8s-foundation**: Cluster health and Helm orchestration.
- **kafka-k8s-setup**: Cloud-native event mesh deployment.
- **postgres-k8s-setup**: Stateful data layer setup with automated migrations.
- **fastapi-dapr-agent**: Microservice architecture with sidecar integration.
- **nextjs-k8s-deploy**: High-performance frontend orchestration.

## Getting Started

1.  Read the [Skill Development Guide](./skill-development-guide.md) to understand how to contribute.
2.  Explore the `.claude/skills` directory in the root of the repository.
3.  Teach your agents to build the systems of the future.

---
*Powered by Agentic AI Foundation (AAIF) Standards*
