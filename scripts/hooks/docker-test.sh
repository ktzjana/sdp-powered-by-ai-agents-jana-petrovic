#!/bin/bash

set -e

echo "🐳 Building Docker image..."
docker build -t kata-tests .

echo "🧪 Running tests in container..."
docker run --rm kata-tests

echo "✅ Docker tests passed"
