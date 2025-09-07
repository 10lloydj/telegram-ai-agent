#!/bin/bash
set -e

echo "🚀 Deploying Telegram AI Agent..."

# Pull latest changes
git pull origin main

# Stop existing containers
docker compose down

# Rebuild and start
docker compose up -d --build

# Wait for services to be healthy
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
if docker compose ps | grep -q "Up"; then
    echo "✅ Deployment successful!"
    echo "📊 Service status:"
    docker compose ps
    echo ""
    echo "View logs with: docker compose logs -f"
    echo "Monitor with: docker compose ps"
else
    echo "❌ Deployment failed!"
    echo "Check logs with: docker compose logs"
    exit 1
fi
