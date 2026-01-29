#!/bin/bash
# Deploy Apache Kafka on Kubernetes

echo "Setting up Kafka on Kubernetes..."

# Add the Bitnami Helm repository
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Create kafka namespace
kubectl create namespace kafka --dry-run=client -o yaml | kubectl apply -f -

# Install Kafka using Helm
helm install kafka bitnami/kafka \
  --namespace kafka \
  --set replicaCount=1 \
  --set zookeeper.enabled=true \
  --set zookeeper.replicaCount=1

echo "✓ Kafka deployed to namespace 'kafka'"