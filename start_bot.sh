#!/bin/bash

# Manual Bot Starter Script for cPanel
# Use this to manually start the bot from terminal

BOT_DIR=~/repositories/inventory_bot
VENV_ACTIVATE=~/virtualenv/repositories/inventory_bot/3.11/bin/activate

echo "Starting Telegram Warehouse Bot..."
echo "=================================="

# Navigate to bot directory
cd "$BOT_DIR" || {
    echo "Error: Cannot find bot directory at $BOT_DIR"
    exit 1
}

# Check if .env exists
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Please create .env file with your TELEGRAM_BOT_TOKEN"
    exit 1
fi

# Activate virtual environment
if [ -f "$VENV_ACTIVATE" ]; then
    source "$VENV_ACTIVATE"
    echo "✓ Virtual environment activated"
else
    echo "Error: Virtual environment not found"
    echo "Please set up Python App in cPanel first"
    exit 1
fi

# Check if bot is already running
if [ -f bot.pid ]; then
    PID=$(cat bot.pid)
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "✓ Bot is already running (PID: $PID)"
        echo ""
        echo "To stop it, run: kill $PID"
        exit 0
    fi
fi

# Start the bot
echo "Starting bot..."
nohup python bot.py > bot.log 2>&1 &
NEW_PID=$!

echo $NEW_PID > bot.pid
echo "✓ Bot started successfully!"
echo "  PID: $NEW_PID"
echo "  Log: $BOT_DIR/bot.log"
echo ""
echo "To view logs: tail -f $BOT_DIR/bot.log"
echo "To stop bot: kill $NEW_PID"

