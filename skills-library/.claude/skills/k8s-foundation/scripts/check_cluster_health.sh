#!/bin/bash
# Check Kubernetes cluster health

echo "Checking Kubernetes cluster health..."

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "✗ kubectl is not installed or not in PATH"
    exit 1
fi

# Check cluster info
echo "Cluster Info:"
kubectl cluster-info 2>/dev/null || {
    echo "✗ Cannot connect to cluster - Minikube may not be running"
    exit 1
}

# Check node status
echo -e "\nNode Status:"
kubectl get nodes || {
    echo "✗ Cannot get node status"
    exit 1
}

# Check if all nodes are ready
node_status=$(kubectl get nodes --no-headers | awk '{print $2}')
for status in $node_status; do
    if [[ "$status" != "Ready" ]]; then
        echo "✗ Node not ready: $status"
        exit 1
    fi
done

echo -e "\n✓ Cluster is healthy"
exit 0