# PostgreSQL Kubernetes Setup - Reference

## Purpose
The postgres-k8s-setup skill deploys PostgreSQL on Kubernetes, providing persistent storage for applications with proper configuration and security.

## Commands
- `deploy_postgres.sh`: Deploys PostgreSQL using Helm charts
- `verify_postgres.py`: Checks if PostgreSQL is properly running and accessible

## Best Practices
- Use persistent volumes for data storage
- Configure proper backup and recovery procedures
- Implement secure authentication methods
- Set up monitoring and alerting

## Common Issues
- Persistent volume provisioning failures
- Connection timeout issues
- Password and authentication configuration
- Resource allocation for database performance