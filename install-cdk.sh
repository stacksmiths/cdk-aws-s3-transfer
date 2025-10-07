#!/bin/bash

# CDK CLI Installation Script
# This script installs CDK CLI using the best available method

set -e

echo "Installing AWS CDK CLI..."

# Check if CDK is already installed
if command -v cdk >/dev/null 2>&1; then
    echo "CDK CLI already installed: $(cdk --version)"
    exit 0
fi

# Check if Node.js is available
if ! command -v node >/dev/null 2>&1; then
    echo "Error: Node.js is not installed. Please install Node.js first."
    echo "Visit: https://nodejs.org/"
    exit 1
fi

# Check if npm is available
if ! command -v npm >/dev/null 2>&1; then
    echo "Error: npm is not installed. Please install npm first."
    exit 1
fi

echo "Node.js version: $(node --version)"
echo "npm version: $(npm --version)"

# Try to install CDK CLI
echo "Installing CDK CLI globally..."

if sudo npm install -g aws-cdk 2>/dev/null; then
    echo "✅ CDK CLI installed successfully!"
    cdk --version
elif npm install -g aws-cdk 2>/dev/null; then
    echo "✅ CDK CLI installed successfully (user install)!"
    cdk --version
else
    echo "❌ Failed to install CDK CLI with npm"
    echo ""
    echo "Please try one of these alternatives:"
    echo "1. Install with sudo: sudo npm install -g aws-cdk"
    echo "2. Install locally: npm install aws-cdk (then use npx cdk)"
    echo "3. Use package manager:"
    echo "   - Ubuntu/Debian: sudo apt install aws-cdk"
    echo "   - macOS: brew install aws-cdk"
    echo "   - Windows: choco install aws-cdk"
    exit 1
fi
