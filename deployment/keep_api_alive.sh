#!/bin/bash
# Keep FastAPI alive - for use with Method 2 (background process)
# Add to cron: */5 * * * * /bin/bash ~/app/deployment/keep_api_alive.sh >> ~/app/api_cron.log 2>&1

API_DIR="$HOME/app"
VENV_ACTIVATE="$HOME/virtualenv/app/3.11/bin/activate"
LOG_FILE="$API_DIR/api.log"

cd "$API_DIR"

# Check if API is running
if ! pgrep -f "uvicorn api.main:app" > /dev/null; then
    echo "[$(date)] API not running, starting...." >> "$LOG_FILE"
    
    # Activate virtual environment
    source "$VENV_ACTIVATE"
    
    # Start API in background
    nohup python -m uvicorn api.main:app --host 0.0.0.0 --port 8001 >> "$LOG_FILE" 2>&1 &
    
    echo "[$(date)] API started with PID: $!" >> "$LOG_FILE"
else
    echo "[$(date)] API is already running" >> "$LOG_FILE"
fi

