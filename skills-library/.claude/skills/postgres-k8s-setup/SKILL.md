---
name: postgres-k8s-setup
description: Deploy PostgreSQL on Kubernetes
---

# PostgreSQL Kubernetes Setup

## When to Use
- User asks to deploy PostgreSQL
- Setting up persistent storage for applications
- Creating database for microservices

## Instructions
1. Run deployment: `./scripts/deploy_postgres.sh`
2. Verify status: `python scripts/verify_postgres.py`
3. Run migrations: `./scripts/run_migrations.sh`

## Validation
- [ ] PostgreSQL pod is Running
- [ ] Database is accessible
- [ ] Schema migrations completed

See [REFERENCE.md](./REFERENCE.md) for configuration options.