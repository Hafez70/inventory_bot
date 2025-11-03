#!/bin/bash
# Stop FastAPI
# Usage: ./stop_api.sh

echo "Stopping FastAPI..."

pkill -f "uvicorn api.main:app"

sleep 2

if ! pgrep -f "uvicorn api.main:app" > /dev/null; then
    echo "✅ API stopped successfully"
else
    echo "⚠️  Force stopping..."
    pkill -9 -f "uvicorn api.main:app"
    sleep 1
    if ! pgrep -f "uvicorn api.main:app" > /dev/null; then
        echo "✅ API stopped (force)"
    else
        echo "❌ Failed to stop API"
        exit 1
    fi
fi

