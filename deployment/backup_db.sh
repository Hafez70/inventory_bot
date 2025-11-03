#!/bin/bash

# Database Backup Script for cPanel
# Automatically backs up warehouse.db with timestamp

# Configuration
BOT_DIR=~/repositories/inventory_bot
BACKUP_DIR=$BOT_DIR/backups
DB_FILE=$BOT_DIR/warehouse.db
KEEP_DAYS=7  # Keep backups for 30 days

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Check if database exists
if [ ! -f "$DB_FILE" ]; then
    echo "Error: Database file not found at $DB_FILE"
    exit 1
fi

# Generate timestamp for backup filename
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/warehouse_backup_$TIMESTAMP.db"

# Create backup
cp "$DB_FILE" "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "✓ Backup created successfully: $BACKUP_FILE"
    
    # Get backup file size
    SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo "  Size: $SIZE"
    
    # Delete old backups (older than KEEP_DAYS)
    echo "  Cleaning up old backups (keeping last $KEEP_DAYS days)..."
    find "$BACKUP_DIR" -name "warehouse_backup_*.db" -type f -mtime +$KEEP_DAYS -delete
    
    # Count remaining backups
    BACKUP_COUNT=$(ls -1 "$BACKUP_DIR"/warehouse_backup_*.db 2>/dev/null | wc -l)
    echo "  Total backups: $BACKUP_COUNT"
else
    echo "✗ Backup failed!"
    exit 1
fi

