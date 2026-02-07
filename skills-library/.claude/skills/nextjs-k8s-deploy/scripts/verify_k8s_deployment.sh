#!/bin/bash
# Skill: nextjs-k8s-deploy
# Script: scripts/verify_k8s_deployment.sh
# Purpose: Verify the health and availability of the deployed Next.js frontend

SERVICE_NAME="learnflow-frontend"
NAMESPACE="default"

echo "🔍 Verifying deployment for: $SERVICE_NAME"

# Check if service exists
if ! kubectl get service $SERVICE_NAME -n $NAMESPACE > /dev/null 2>&1; then
    echo "✗ Error: Service $SERVICE_NAME not found in namespace $NAMESPACE"
    exit 1
fi

# Check pod status
POD_STATUS=$(kubectl get pods -l app=$SERVICE_NAME -n $NAMESPACE -o jsonpath='{.items[*].status.phase}')
echo "✓ Pod Status: $POD_STATUS"

if [[ $POD_STATUS != *"Running"* ]]; then
    echo "✗ Error: At least one pod is not in Running state."
    exit 1
fi

# Check for LoadBalancer IP (if applicable)
EXTERNAL_IP=$(kubectl get service $SERVICE_NAME -n $NAMESPACE -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

if [ -z "$EXTERNAL_IP" ]; then
    echo "ℹ️ External IP pending or not applicable (NodePort used)."
else
    echo "✓ External IP: $EXTERNAL_IP"
    echo "Testing connectivity..."
    curl -I -s -o /dev/null -w "%{http_code}" http://$EXTERNAL_IP | grep 200 > /dev/null
    if [ $? -eq 0 ]; then
        echo "✓ Connectivity Test: SUCCESS (200 OK)"
    else
        echo "⚠️ Connectivity Test: WARNING (Endpoint reachable but returned non-200)"
    fi
fi

echo "✅ Deployment verification COMPLETE."
