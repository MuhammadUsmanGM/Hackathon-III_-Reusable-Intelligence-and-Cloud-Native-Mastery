#!/bin/bash
# Deploy PostgreSQL on Kubernetes

echo "Setting up PostgreSQL on Kubernetes..."

# Add the Bitnami Helm repository
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Create postgresql namespace
kubectl create namespace postgresql --dry-run=client -o yaml | kubectl apply -f -

# Install PostgreSQL using Helm with basic configuration
helm install postgresql bitnami/postgresql \
  --namespace postgresql \
  --set auth.postgresPassword=secretpassword \
  --set primary.persistence.enabled=false \
  --set image.debug=true

echo "✓ PostgreSQL deployed to namespace 'postgresql'"