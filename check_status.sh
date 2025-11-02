#!/bin/bash

# Bot Status Checker Script
# Shows current status of the Telegram bot

BOT_DIR=~/repositories/inventory_bot
PID_FILE=$BOT_DIR/bot.pid

echo "========================================"
echo "  Telegram Warehouse Bot Status"
echo "========================================"
echo ""

# Check if PID file exists
if [ ! -f "$PID_FILE" ]; then
    echo "Status: ❌ STOPPED (No PID file)"
    echo ""
    echo "To start: cd ~/repositories/inventory_bot && ./start_bot.sh"
    exit 1
fi

# Read PID
PID=$(cat "$PID_FILE")

# Check if process is running
if ps -p "$PID" > /dev/null 2>&1; then
    echo "Status: ✅ RUNNING"
    echo "PID: $PID"
    
    # Show process info
    echo ""
    echo "Process Info:"
    ps -p "$PID" -o pid,etime,cmd
    
    echo ""
    echo "Last 5 log entries:"
    tail -5 "$BOT_DIR/bot.log" 2>/dev/null || echo "No logs available"
    
else
    echo "Status: ❌ STOPPED (Process not found)"
    echo "PID file exists but process $PID is not running"
    echo ""
    echo "To start: cd ~/repositories/inventory_bot && ./start_bot.sh"
    exit 1
fi

echo ""
echo "To view live logs: tail -f $BOT_DIR/bot.log"
echo "To stop bot: kill $PID"
echo "========================================"

