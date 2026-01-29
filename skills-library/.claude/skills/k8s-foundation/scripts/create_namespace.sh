#!/bin/bash
# Create a Kubernetes namespace

if [ $# -ne 1 ]; then
    echo "Usage: $0 <namespace>"
    exit 1
fi

NAMESPACE=$1

echo "Creating namespace: $NAMESPACE"

# Check if namespace already exists
if kubectl get namespace $NAMESPACE &> /dev/null; then
    echo "Namespace $NAMESPACE already exists"
    exit 0
fi

# Create the namespace
kubectl create namespace $NAMESPACE || {
    echo "✗ Failed to create namespace $NAMESPACE"
    exit 1
}

# Add labels to the namespace
kubectl label namespace $NAMESPACE purpose=hackathon-project || {
    echo "Warning: Failed to add labels to namespace $NAMESPACE"
}

echo "✓ Namespace $NAMESPACE created successfully"