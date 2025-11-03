#!/bin/bash
# Restart both Bot and API
# Usage: ./restart_all.sh

echo "======================================"
echo "  Restarting Bot and API"
echo "======================================"
echo ""

BOT_DIR="$HOME/app"
VENV_ACTIVATE="$HOME/virtualenv/app/3.11/bin/activate"

cd "$BOT_DIR"

# 1. Stop everything
echo "1️⃣  Stopping bot..."
pkill -f "bot/bot.py"
sleep 2

echo "2️⃣  Stopping API..."
pkill -f "uvicorn api.main:app"
sleep 2

# 2. Pull latest changes (optional - comment out if not needed)
echo "3️⃣  Pulling latest changes from git..."
git pull origin main

# 3. Activate virtual environment
echo "4️⃣  Activating virtual environment..."
source "$VENV_ACTIVATE"

# 4. Update dependencies
echo "5️⃣  Updating dependencies..."
pip install -q -r requirements.txt

# 5. Run migrations
echo "6️⃣  Running database migrations..."
python database/migrate.py

# 6. Start bot
echo "7️⃣  Starting bot..."
nohup python bot/bot.py > bot.log 2>&1 &
sleep 2

# 7. Start API (optional - comment out if using Passenger)
echo "8️⃣  Starting API..."
nohup python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 >> api.log 2>&1 &
sleep 2

# 8. Check status
echo ""
echo "======================================"
echo "  Status Check"
echo "======================================"
echo ""

if pgrep -f "bot/bot.py" > /dev/null; then
    echo "✅ Bot is running"
    ps aux | grep "[b]ot/bot.py" | awk '{print "   PID: "$2" | CPU: "$3"% | Memory: "$4"%"}'
else
    echo "❌ Bot is NOT running"
fi

echo ""

if pgrep -f "uvicorn api.main:app" > /dev/null; then
    echo "✅ API is running"
    ps aux | grep "[u]vicorn" | awk '{print "   PID: "$2" | CPU: "$3"% | Memory: "$4"%"}'
else
    echo "❌ API is NOT running"
fi

echo ""
echo "======================================"
echo "  Logs"
echo "======================================"
echo ""
echo "Bot logs: tail -f ~/app/bot.log"
echo "API logs: tail -f ~/app/api.log"
echo ""
echo "✅ Restart complete!"

