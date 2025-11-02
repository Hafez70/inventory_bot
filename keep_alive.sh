#!/bin/bash

# Telegram Bot Keep-Alive Script for cPanel
# This script ensures the bot is always running and restarts it if needed

# Configuration - Update these paths for your setup
BOT_DIR=~/repositories/inventory_bot
PID_FILE=$BOT_DIR/bot.pid
LOG_FILE=$BOT_DIR/bot.log
VENV_ACTIVATE=~/virtualenv/repositories/inventory_bot/3.9/bin/activate

# Function to check if bot is running
is_bot_running() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            return 0  # Bot is running
        fi
    fi
    return 1  # Bot is not running
}

# Check if bot is already running
if is_bot_running; then
    # Bot is running, nothing to do
    exit 0
fi

# Bot is not running, start it
cd "$BOT_DIR" || exit 1

# Activate virtual environment
if [ -f "$VENV_ACTIVATE" ]; then
    source "$VENV_ACTIVATE"
else
    echo "Error: Virtual environment not found at $VENV_ACTIVATE" >> "$LOG_FILE"
    exit 1
fi

# Start the bot in background
nohup python bot.py >> "$LOG_FILE" 2>&1 &
NEW_PID=$!

# Save the PID
echo $NEW_PID > "$PID_FILE"

# Log the restart
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Bot started with PID: $NEW_PID" >> "$LOG_FILE"

exit 0

