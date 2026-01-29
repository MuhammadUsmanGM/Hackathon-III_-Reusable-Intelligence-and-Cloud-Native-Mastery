---
name: fastapi-dapr-agent
description: Deploy FastAPI services with Dapr integration
---

# FastAPI Dapr Agent

## When to Use
- Creating microservices with FastAPI
- Integrating Dapr for state management and pub/sub
- Building event-driven services

## Instructions
1. Create service template: `./scripts/create_template.py <service-name>`
2. Deploy service: `./scripts/deploy_service.sh <service-name>`
3. Configure Dapr: `./scripts/configure_dapr.py <service-name>`

## Validation
- [ ] FastAPI service is running
- [ ] Dapr sidecar is attached
- [ ] Service is accessible via Dapr

See [REFERENCE.md](./REFERENCE.md) for configuration options.