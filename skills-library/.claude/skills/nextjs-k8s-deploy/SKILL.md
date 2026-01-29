---
name: nextjs-k8s-deploy
description: Deploy Next.js applications on Kubernetes
---

# Next.js Kubernetes Deployment

## When to Use
- Deploying Next.js frontend applications
- Setting up ingress for web applications
- Configuring load balancing for web traffic

## Instructions
1. Build Next.js app: `./scripts/build_app.sh <app-path>`
2. Create Docker image: `./scripts/create_image.sh <image-name>`
3. Deploy to Kubernetes: `./scripts/deploy_to_k8s.sh <deployment-name>`

## Validation
- [ ] Next.js app is accessible
- [ ] Health checks are passing
- [ ] SSL/TLS configured (if applicable)

See [REFERENCE.md](./REFERENCE.md) for configuration options.