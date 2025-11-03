#!/bin/bash
# Start FastAPI in background (Method 2)
# Usage: ./start_api.sh

cd ~/app

echo "Starting FastAPI..."

# Activate virtual environment
source ~/virtualenv/app/3.11/bin/activate

# Check if already running
if pgrep -f "uvicorn api.main:app" > /dev/null; then
    echo "⚠️  API is already running!"
    echo "Stop it first with: pkill -f 'uvicorn api.main:app'"
    exit 1
fi

# Start API in background
nohup python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 >> api.log 2>&1 &

sleep 2

# Check if started successfully
if pgrep -f "uvicorn api.main:app" > /dev/null; then
    echo "✅ API started successfully!"
    echo "📊 Check status: ps aux | grep uvicorn"
    echo "📝 View logs: tail -f ~/app/api.log"
    echo "🌐 Access: http://localhost:8000"
else
    echo "❌ Failed to start API"
    echo "Check logs: tail -50 ~/app/api.log"
    exit 1
fi

