---
name: k8s-foundation
description: Check cluster health and apply basic Helm charts for Kubernetes
---

# Kubernetes Foundation

## When to Use
- Checking cluster health and readiness
- Applying basic Helm charts
- Verifying Kubernetes connectivity
- Setting up namespaces and basic resources

## Instructions
1. Check cluster status: `./scripts/check_cluster_health.sh`
2. Create namespace: `./scripts/create_namespace.sh <namespace>`
3. Apply basic resources: `./scripts/apply_resources.sh <resource-file>`

## Validation
- [ ] Cluster is accessible and healthy
- [ ] Required namespaces exist
- [ ] Basic resources deployed successfully

See [REFERENCE.md](./REFERENCE.md) for configuration options.