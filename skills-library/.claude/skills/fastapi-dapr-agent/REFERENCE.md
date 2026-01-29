# FastAPI Dapr Agent - Reference

## Purpose
The fastapi-dapr-agent skill creates and deploys FastAPI microservices with Dapr integration, enabling state management, pub/sub messaging, and service invocation.

## Commands
- `create_template.py <service-name>`: Creates a FastAPI service template with Dapr integration
- `deploy_service.sh <service-name>`: Deploys the service to Kubernetes with Dapr sidecar
- `configure_dapr.py <service-name>`: Configures Dapr components for the service

## Best Practices
- Always enable Dapr sidecar injection in Kubernetes deployments
- Use Dapr state stores for consistent state management
- Leverage Dapr pub/sub for event-driven communication
- Secure Dapr components with appropriate authentication

## Common Issues
- Dapr runtime not installed in cluster
- Sidecar injection failures
- Component configuration mismatches
- Service invocation timeouts