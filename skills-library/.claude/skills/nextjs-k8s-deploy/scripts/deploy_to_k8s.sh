#!/bin/bash
# Deploy a Next.js application to Kubernetes

if [ $# -ne 1 ]; then
    echo "Usage: $0 <deployment-name>"
    exit 1
fi

DEPLOYMENT_NAME=$1

echo "Deploying Next.js application: $DEPLOYMENT_NAME"

# Create a namespace for the application
kubectl create namespace $DEPLOYMENT_NAME --dry-run=client -o yaml | kubectl apply -f -

# Create Kubernetes deployment and service YAML
cat << EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: $DEPLOYMENT_NAME
  namespace: $DEPLOYMENT_NAME
  labels:
    app: $DEPLOYMENT_NAME
spec:
  replicas: 2
  selector:
    matchLabels:
      app: $DEPLOYMENT_NAME
  template:
    metadata:
      labels:
        app: $DEPLOYMENT_NAME
    spec:
      containers:
      - name: $DEPLOYMENT_NAME
        image: $DEPLOYMENT_NAME:latest
        ports:
        - containerPort: 3000
        env:
        - name: NODE_ENV
          value: "production"
        livenessProbe:
          httpGet:
            path: /
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: $DEPLOYMENT_NAME-service
  namespace: $DEPLOYMENT_NAME
spec:
  selector:
    app: $DEPLOYMENT_NAME
  ports:
    - protocol: TCP
      port: 80
      targetPort: 3000
  type: LoadBalancer
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: $DEPLOYMENT_NAME-ingress
  namespace: $DEPLOYMENT_NAME
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: $DEPLOYMENT_NAME-service
            port:
              number: 80
EOF

echo "✓ Next.js application $DEPLOYMENT_NAME deployed to Kubernetes"
echo "✓ Waiting for deployment to be ready..."

# Wait for the deployment to be ready
kubectl rollout status deployment/$DEPLOYMENT_NAME -n $DEPLOYMENT_NAME --timeout=300s || {
    echo "✗ Deployment failed to become ready within 5 minutes"
    exit 1
}

echo "✓ Deployment is ready"