#!/bin/bash
# All-in-one deployment script for cPanel
# Run this on your cPanel server after uploading files

echo "======================================"
echo "  Warehouse Bot Deployment Script"
echo "======================================"
echo ""

# Get username
USERNAME=$(whoami)
PROJECT_DIR="$HOME/repositories/inventory_bot"

echo "👤 Username: $USERNAME"
echo "📁 Project Directory: $PROJECT_DIR"
echo ""

# Step 1: Check if project exists
if [ ! -d "$PROJECT_DIR" ]; then
    echo "❌ Project directory not found: $PROJECT_DIR"
    echo "Please upload the project first!"
    exit 1
fi

cd "$PROJECT_DIR"
echo "✅ Project directory found"
echo ""

# Step 2: Check .env file
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "Creating .env file..."
    cat > .env << EOF
TELEGRAM_BOT_TOKEN=your_bot_token_here
BOT_PASSWORD=ciFarco@1213#3221
EOF
    chmod 600 .env
    echo "❌ Please edit .env file and add your bot token:"
    echo "   nano $PROJECT_DIR/.env"
    exit 1
fi

echo "✅ .env file exists"
echo ""

# Step 3: Find and activate virtual environment
echo "🔍 Looking for virtual environment..."

if [ -d "$HOME/virtualenv/repositories/inventory_bot/3.11" ]; then
    VENV_PATH="$HOME/virtualenv/repositories/inventory_bot/3.11"
    PYTHON_VERSION="3.11"
elif [ -d "$HOME/virtualenv/repositories/inventory_bot/3.9" ]; then
    VENV_PATH="$HOME/virtualenv/repositories/inventory_bot/3.9"
    PYTHON_VERSION="3.9"
elif [ -d "$HOME/virtualenv/repositories/inventory_bot/3.10" ]; then
    VENV_PATH="$HOME/virtualenv/repositories/inventory_bot/3.10"
    PYTHON_VERSION="3.10"
else
    echo "❌ Virtual environment not found!"
    echo "Please create a Python App in cPanel first:"
    echo "1. Go to cPanel > Setup Python App"
    echo "2. Create application with root: /home/$USERNAME/repositories/inventory_bot"
    echo "3. Run this script again"
    exit 1
fi

echo "✅ Found Python $PYTHON_VERSION virtual environment"
echo "   Path: $VENV_PATH"
echo ""

# Step 4: Install dependencies
echo "📦 Installing dependencies..."
source "$VENV_PATH/bin/activate"
pip install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo ""

# Step 5: Initialize database
echo "🗄️  Initializing database..."
python database/migrate.py

if [ $? -eq 0 ]; then
    echo "✅ Database initialized"
else
    echo "❌ Failed to initialize database"
    exit 1
fi
echo ""

# Step 6: Update deployment scripts
echo "🔧 Updating deployment scripts..."

# Update keep_alive.sh
sed -i "s|VENV_ACTIVATE=.*|VENV_ACTIVATE=\"$VENV_PATH/bin/activate\"|g" deployment/keep_alive.sh
sed -i "s|BOT_DIR=.*|BOT_DIR=\"$PROJECT_DIR\"|g" deployment/keep_alive.sh

# Update check_status.sh
sed -i "s|VENV_ACTIVATE=.*|VENV_ACTIVATE=\"$VENV_PATH/bin/activate\"|g" deployment/check_status.sh
sed -i "s|BOT_DIR=.*|BOT_DIR=\"$PROJECT_DIR\"|g" deployment/check_status.sh

# Update backup_db.sh
sed -i "s|DB_DIR=.*|DB_DIR=\"$PROJECT_DIR/database\"|g" deployment/backup_db.sh
sed -i "s|BACKUP_DIR=.*|BACKUP_DIR=\"$PROJECT_DIR/backups\"|g" deployment/backup_db.sh

# Make executable
chmod +x deployment/*.sh

echo "✅ Deployment scripts updated"
echo ""

# Step 7: Stop any running bot
echo "🛑 Stopping any running bot..."
pkill -f "bot/bot.py"
sleep 2
echo "✅ Done"
echo ""

# Step 8: Start bot
echo "🚀 Starting bot..."
nohup python bot/bot.py > bot.log 2>&1 &
sleep 3

# Check if bot started
if ps aux | grep -q "[b]ot/bot.py"; then
    echo "✅ Bot started successfully!"
    echo ""
    echo "📊 Bot Status:"
    ps aux | grep "[b]ot/bot.py" | awk '{print "   PID: "$2" | Memory: "$4"% | Started: "$9}'
else
    echo "❌ Failed to start bot"
    echo "Check logs: tail -50 $PROJECT_DIR/bot.log"
    exit 1
fi
echo ""

# Step 9: Show cron job commands
echo "⏰ To setup automatic restart and backup:"
echo ""
echo "1. Go to cPanel > Cron Jobs"
echo ""
echo "2. Add this cron job (Keep bot alive - every 5 minutes):"
echo "   */5 * * * * /bin/bash $PROJECT_DIR/deployment/keep_alive.sh >> $PROJECT_DIR/cron.log 2>&1"
echo ""
echo "3. Add this cron job (Daily backup - at 2 AM):"
echo "   0 2 * * * /bin/bash $PROJECT_DIR/deployment/backup_db.sh >> $PROJECT_DIR/backup.log 2>&1"
echo ""

# Step 10: Test bot
echo "======================================"
echo "  ✅ Deployment Complete!"
echo "======================================"
echo ""
echo "📱 Test your bot:"
echo "   1. Open Telegram"
echo "   2. Find your bot"
echo "   3. Send: /start"
echo "   4. Enter password: ciFarco@1213#3221"
echo ""
echo "📊 Useful commands:"
echo "   View logs:    tail -50 $PROJECT_DIR/bot.log"
echo "   Check status: $PROJECT_DIR/deployment/check_status.sh"
echo "   Stop bot:     pkill -f 'bot/bot.py'"
echo "   Restart bot:  nohup python $PROJECT_DIR/bot/bot.py > $PROJECT_DIR/bot.log 2>&1 &"
echo ""
echo "📁 Important paths:"
echo "   Database:     $PROJECT_DIR/database/warehouse.db"
echo "   Images:       $PROJECT_DIR/database/images/"
echo "   Backups:      $PROJECT_DIR/backups/"
echo "   Logs:         $PROJECT_DIR/bot.log"
echo ""
echo "🎉 Your warehouse bot is ready!"
echo ""

