# Next.js Kubernetes Deployment - Reference

## Purpose
The nextjs-k8s-deploy skill deploys Next.js applications on Kubernetes, handling containerization, deployment, and service configuration.

## Commands
- `build_app.sh <app-path>`: Builds the Next.js application for production
- `create_image.sh <image-name>`: Creates a Docker image for the application
- `deploy_to_k8s.sh <deployment-name>`: Deploys the application to Kubernetes

## Best Practices
- Use multi-stage Docker builds for smaller images
- Implement proper health checks
- Configure appropriate resource limits
- Set up SSL termination at the ingress level

## Common Issues
- Build failures due to missing dependencies
- Docker image size optimization
- Environment variable configuration
- Static asset serving in production