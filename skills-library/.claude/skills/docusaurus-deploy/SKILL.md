---
name: docusaurus-deploy
description: Deploy Docusaurus documentation sites
---

# Docusaurus Deployment

## When to Use
- Deploying documentation sites
- Creating knowledge bases for projects
- Publishing technical documentation

## Instructions
1. Build Docusaurus site: `./scripts/build_site.sh <site-path>`
2. Configure deployment: `./scripts/configure_deploy.py <config-file>`
3. Deploy to hosting: `./scripts/deploy_site.sh <site-name>`

## Validation
- [ ] Site is accessible at designated URL
- [ ] Navigation works correctly
- [ ] Search functionality is operational

See [REFERENCE.md](./REFERENCE.md) for configuration options.