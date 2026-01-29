# Docusaurus Deployment - Reference

## Purpose
The docusaurus-deploy skill deploys Docusaurus documentation sites to Kubernetes, enabling teams to publish technical documentation with proper infrastructure.

## Commands
- `build_site.sh <site-path>`: Builds the Docusaurus site for production
- `configure_deploy.py <config-file>`: Updates deployment configuration
- `deploy_site.sh <site-name>`: Deploys the site to Kubernetes

## Best Practices
- Always verify the site builds locally before deploying
- Configure proper base URL for the deployment environment
- Set up proper caching headers for static assets
- Use CDN for improved global performance

## Common Issues
- Build failures due to missing dependencies
- Incorrect base URL configuration
- Static asset loading problems
- Ingress configuration issues