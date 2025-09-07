#!/bin/bash
set -e

# Create backups directory if it doesn't exist
mkdir -p ./backups

# Generate backup filename with timestamp
BACKUP_FILE="./backups/telegram_ai_$(date +%Y%m%d_%H%M%S).sql"

echo "Creating database backup..."

# Create backup using docker compose
docker compose exec -T db pg_dump -U app -d jobwatch > "$BACKUP_FILE"

# Compress the backup
gzip "$BACKUP_FILE"

echo "✅ Backup created: ${BACKUP_FILE}.gz"

# Keep only the last 7 backups
find ./backups -name "telegram_ai_*.sql.gz" -type f -mtime +7 -delete

echo "🧹 Old backups cleaned up (keeping last 7 days)"
