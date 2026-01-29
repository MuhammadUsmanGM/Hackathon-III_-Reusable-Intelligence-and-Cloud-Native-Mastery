#!/bin/bash
# Build a Next.js application for Kubernetes deployment

if [ $# -ne 1 ]; then
    echo "Usage: $0 <app-path>"
    exit 1
fi

APP_PATH=$1

echo "Building Next.js application at $APP_PATH"

# Navigate to the app directory
cd $APP_PATH || exit 1

# Check if package.json exists
if [ ! -f "package.json" ]; then
    echo "✗ No package.json found in $APP_PATH"
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
npm install || exit 1

# Build the Next.js application
echo "Building Next.js application..."
npm run build || {
    echo "✗ Build failed. Trying with legacy peer deps..."
    npm install --legacy-peer-deps && npm run build || exit 1
}

echo "✓ Next.js application built successfully"
echo "Build output located at $APP_PATH/.next"