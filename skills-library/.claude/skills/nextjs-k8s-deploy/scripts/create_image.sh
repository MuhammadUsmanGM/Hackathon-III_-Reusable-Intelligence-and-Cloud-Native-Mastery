#!/bin/bash
# Create a Docker image for a Next.js application

if [ $# -ne 1 ]; then
    echo "Usage: $0 <image-name>"
    exit 1
fi

IMAGE_NAME=$1

echo "Creating Docker image: $IMAGE_NAME"

# Create a temporary Dockerfile if not present
if [ ! -f "Dockerfile" ]; then
    cat > Dockerfile << 'EOF'
# Use the official Node.js 18 image
# https://hub.docker.com/_/node
FROM node:18-alpine AS builder

# Create and change to the app directory
WORKDIR /usr/src/app

# Copy application dependency manifests to the container image.
# A wildcard is used to ensure copying both package.json AND package-lock.json (when available).
# This is important for production image generation.
COPY package*.json ./

# Install all dependencies
RUN npm ci --only=production

# Copy local code to the container image
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM node:18-alpine AS runner

WORKDIR /usr/src/app

# Don't run production as root
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy pruned dependencies
COPY --from=builder /usr/src/app/node_modules ./node_modules
COPY --from=builder --chown=nextjs:nodejs /usr/src/app/.next ./.next
COPY --from=builder --chown=nextjs:nodejs /usr/src/app/public ./public
COPY --from=builder --chown=nextjs:nodejs /usr/src/app/package.json ./package.json

USER nextjs

EXPOSE 3000

ENV PORT 3000

# Start the nextjs application
CMD ["npm", "start"]
EOF
    echo "✓ Temporary Dockerfile created"
fi

# Build the Docker image
docker build -t $IMAGE_NAME . || {
    echo "✗ Docker build failed"
    exit 1
}

echo "✓ Docker image $IMAGE_NAME created successfully"