# Kafka Kubernetes Setup - Reference

## Purpose
The kafka-k8s-setup skill deploys Apache Kafka on Kubernetes, providing distributed messaging capabilities for event-driven architectures.

## Commands
- `deploy.sh`: Deploys Kafka using Helm charts
- `verify.py`: Checks if Kafka is properly running and accessible

## Best Practices
- Use persistent storage for Kafka logs in production
- Configure appropriate replication factors
- Set up proper network policies
- Monitor broker health and partition distribution

## Common Issues
- Insufficient disk space for Kafka logs
- Network connectivity between brokers
- Zookeeper configuration issues
- Topic creation and partitioning problems