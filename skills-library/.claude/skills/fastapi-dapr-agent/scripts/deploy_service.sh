#!/bin/bash
# Deploy FastAPI service with Dapr integration to Kubernetes

if [ $# -ne 1 ]; then
    echo "Usage: $0 <service-name>"
    exit 1
fi

SERVICE_NAME=$1

echo "Deploying FastAPI service with Dapr: $SERVICE_NAME"

# Create namespace for the service
kubectl create namespace $SERVICE_NAME --dry-run=client -o yaml | kubectl apply -f -

# Create a basic deployment YAML for the service
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: $SERVICE_NAME
  namespace: $SERVICE_NAME
  labels:
    app: $SERVICE_NAME
spec:
  replicas: 1
  selector:
    matchLabels:
      app: $SERVICE_NAME
  template:
    metadata:
      labels:
        app: $SERVICE_NAME
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "$SERVICE_NAME"
        dapr.io/app-port: "8000"
        dapr.io/log-level: "debug"
    spec:
      containers:
      - name: $SERVICE_NAME
        image: $SERVICE_NAME:latest
        ports:
        - containerPort: 8000
        env:
        - name: DAPR_HTTP_PORT
          value: "3500"
        - name: DAPR_GRPC_PORT
          value: "50001"
---
apiVersion: v1
kind: Service
metadata:
  name: $SERVICE_NAME-service
  namespace: $SERVICE_NAME
spec:
  selector:
    app: $SERVICE_NAME
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: LoadBalancer
EOF

echo "✓ FastAPI service $SERVICE_NAME deployed with Dapr integration"