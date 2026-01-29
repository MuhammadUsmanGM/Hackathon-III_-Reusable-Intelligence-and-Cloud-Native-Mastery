---
name: kafka-k8s-setup
description: Deploy Apache Kafka on Kubernetes
---

# Kafka Kubernetes Setup

## When to Use
- User asks to deploy Kafka
- Setting up event-driven microservices
- Creating message queues for asynchronous communication

## Instructions
1. Run deployment: `./scripts/deploy.sh`
2. Verify status: `python scripts/verify.py`
3. Confirm all pods Running before proceeding.

## Validation
- [ ] All pods in Running state
- [ ] Can create test topic

See [REFERENCE.md](./REFERENCE.md) for configuration options.