# Kubernetes Foundation - Reference

## Purpose
The k8s-foundation skill provides basic Kubernetes operations for checking cluster health and deploying foundational resources.

## Commands
- `check_cluster_health.sh`: Verifies cluster connectivity and node status
- `create_namespace.sh <namespace>`: Creates a namespace with appropriate labels
- `apply_resources.sh <resource-file>`: Applies YAML resource files to the cluster

## Best Practices
- Always verify cluster health before deploying resources
- Use descriptive namespace names that follow organization standards
- Validate resource files before applying to prevent configuration errors
- Monitor resource creation for successful completion

## Common Issues
- Insufficient cluster resources
- Network policy conflicts
- RBAC permission issues