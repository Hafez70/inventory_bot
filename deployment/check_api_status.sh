#!/bin/bash
# Check API status
# Usage: ./check_api_status.sh

echo "Checking FastAPI status..."
echo "======================================"

if pgrep -f "uvicorn api.main:app" > /dev/null; then
    echo "✅ API is RUNNING"
    echo ""
    echo "Process details:"
    ps aux | grep "[u]vicorn api.main:app" | awk '{print "PID: "$2" | CPU: "$3"% | Memory: "$4"% | Started: "$9}'
    echo ""
    echo "Recent logs (last 10 lines):"
    tail -10 ~/app/api.log 2>/dev/null || echo "No log file found"
else
    echo "❌ API is NOT running"
    echo ""
    echo "To start: ./start_api.sh"
    echo "Or manually: cd ~/app && source ~/virtualenv/app/3.11/bin/activate && nohup python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 >> api.log 2>&1 &"
fi

echo ""
echo "======================================"

