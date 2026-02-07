# Mastery Catalog: Core Infrastructure Skills

Our library features 8 "Reusable Intelligence" units. Each skill provides the deterministic logic required for high-stakes cloud-native operations.

## 🛰️ Event & State Mastery

### [FastAPI Dapr Agent](../.claude/skills/fastapi-dapr-agent/SKILL.md)
The backbone of our microservice mesh. Implements state persistence via Redis and service-to-service invocation.
*   **Key Scripts**: `create_template.py`, `configure_dapr.py`.

### [Kafka K8s Setup](../.claude/skills/kafka-k8s-setup/SKILL.md)
Automated deployment of the Apache Kafka cluster for the event mesh.
*   **Success Indicator**: Producer/Consumer connectivity in under 60 seconds.

## 🏗️ Orchestration Mastery

### [K8s Foundation](../.claude/skills/k8s-foundation/SKILL.md)
The base layer for all clusters. Handles namespace isolation, resource quotas, and health verification.

### [Next.js K8s Deploy](../.claude/skills/nextjs-k8s-deploy/SKILL.md)
High-fidelity frontend orchestration scripts, including zero-downtime rollouts and ingress configuration.

## 🗄️ Database Mastery

### [Postgres K8s Setup](../.claude/skills/postgres-k8s-setup/SKILL.md)
StatefulSets for Postgres with automated volume claims and health checks.
*   **Bonus**: Integrated Alembic migration scripts.

---
*Explore the full catalog in the sidebar for technical deep-dives.*
