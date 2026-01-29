#!/bin/bash
# Build a Docusaurus site

if [ $# -ne 1 ]; then
    echo "Usage: $0 <site-path>"
    exit 1
fi

SITE_PATH=$1

echo "Building Docusaurus site at $SITE_PATH"

# Navigate to the site directory
cd $SITE_PATH || exit 1

# Check if package.json exists
if [ ! -f "package.json" ]; then
    echo "✗ No package.json found in $SITE_PATH"
    exit 1
fi

# Check if docusaurus config exists
if [ ! -f "docusaurus.config.js" ] && [ ! -f "docusaurus.config.ts" ]; then
    echo "✗ No Docusaurus configuration found (docusaurus.config.js or docusaurus.config.ts)"
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
npm install || exit 1

# Build the Docusaurus site
echo "Building Docusaurus site..."
npm run build || {
    echo "✗ Build failed. Checking if Docusaurus is properly installed..."

    # Check if @docusaurus/core is in package.json
    if grep -q "@docusaurus/core" package.json; then
        echo "Docusaurus appears to be installed in package.json"
        echo "Trying to build with npx..."
        npx docusaurus build || exit 1
    else
        echo "Docusaurus does not appear to be installed in this project"
        exit 1
    fi
}

echo "✓ Docusaurus site built successfully"
echo "Build output located at $SITE_PATH/build"