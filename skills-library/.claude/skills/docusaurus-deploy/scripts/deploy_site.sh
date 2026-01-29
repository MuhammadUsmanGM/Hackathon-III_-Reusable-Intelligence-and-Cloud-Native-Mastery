#!/bin/bash
# Deploy a Docusaurus site to Kubernetes

if [ $# -ne 1 ]; then
    echo "Usage: $0 <site-name>"
    exit 1
fi

SITE_NAME=$1

echo "Deploying Docusaurus site: $SITE_NAME"

# Create a namespace for the site
kubectl create namespace $SITE_NAME --dry-run=client -o yaml | kubectl apply -f -

# Create a ConfigMap with the nginx configuration for static files
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: $SITE_NAME-nginx-config
  namespace: $SITE_NAME
data:
  nginx.conf: |
    events {
        worker_connections 1024;
    }
    http {
        server {
            listen 80;
            root /usr/share/nginx/html;
            index index.html;

            # Serve static files
            location / {
                try_files \$uri \$uri/ /index.html;
            }

            # Set cache headers for static assets
            location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
                expires 1y;
                add_header Cache-Control "public, immutable";
            }

            # Security headers
            add_header X-Frame-Options "SAMEORIGIN" always;
            add_header X-XSS-Protection "1; mode=block" always;
            add_header X-Content-Type-Options "nosniff" always;
        }
    }
EOF

# Create Kubernetes deployment and service YAML for static site
cat << EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: $SITE_NAME
  namespace: $SITE_NAME
  labels:
    app: $SITE_NAME
spec:
  replicas: 2
  selector:
    matchLabels:
      app: $SITE_NAME
  template:
    metadata:
      labels:
        app: $SITE_NAME
    spec:
      containers:
      - name: $SITE_NAME
        image: nginx:alpine
        ports:
        - containerPort: 80
        volumeMounts:
        - name: nginx-config
          mountPath: /etc/nginx/nginx.conf
          subPath: nginx.conf
        - name: site-content
          mountPath: /usr/share/nginx/html
        # In a real deployment, you would typically copy the built site to this volume
        # or use an init container to download the build artifacts
        env:
        - name: NGINX_ENTRYPOINT_QUIET_LOGS
          value: "1"
      volumes:
      - name: nginx-config
        configMap:
          name: $SITE_NAME-nginx-config
      - name: site-content
        emptyDir: {}
---
apiVersion: v1
kind: Service
metadata:
  name: $SITE_NAME-service
  namespace: $SITE_NAME
spec:
  selector:
    app: $SITE_NAME
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: LoadBalancer
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: $SITE_NAME-ingress
  namespace: $SITE_NAME
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
            name: $SITE_NAME-service
            port:
              number: 80
EOF

echo "✓ Docusaurus site $SITE_NAME deployment created in Kubernetes"
echo "Note: In a real deployment, you would need to ensure the built site content is available in the container."

# Wait for the deployment to be ready
kubectl rollout status deployment/$SITE_NAME -n $SITE_NAME --timeout=300s || {
    echo "✗ Deployment failed to become ready within 5 minutes"
    exit 1
}

echo "✓ Docusaurus site deployment is ready"