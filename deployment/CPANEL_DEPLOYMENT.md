# Complete cPanel Deployment Guide
## For Restructured Warehouse Management System

---

## 📋 Prerequisites

- ✅ cPanel account with Python support
- ✅ SSH access (recommended)
- ✅ Telegram bot token from @BotFather
- ✅ This project files

---

## 🚀 Step-by-Step Deployment

### Step 1: Upload Project to cPanel

#### Option A: Via SSH (Recommended)
```bash
# On your local machine
cd d:/projects/ci-farco/warehousing

# Create a zip file (exclude unnecessary files)
# Then upload via SCP or use git

# Or use git directly on cPanel:
ssh username@your-server.com
cd ~/repositories
git clone https://github.com/Hafez70/inventory_bot.git
cd inventory_bot
```

#### Option B: Via File Manager
1. Login to cPanel
2. Go to **File Manager**
3. Navigate to `/home/username/repositories/`
4. Create folder `inventory_bot`
5. Upload all project files
6. Extract if zipped

**Final structure on cPanel:**
```
~/repositories/inventory_bot/
├── bot/
├── database/
├── api/
├── webApp/
├── deployment/
├── docs/
├── requirements.txt
├── start_bot.sh
├── start_api.sh
└── .env (create this!)
```

---

### Step 2: Create Environment File

SSH into your server or use File Manager:

```bash
cd ~/repositories/inventory_bot
nano .env
```

**Add this content:**
```env
TELEGRAM_BOT_TOKEN=8230888056:AAECbaqgYKRcDHpkAVpAfELsMgYOC5QO3iM
BOT_PASSWORD=ciFarco@1213#3221
```

Save and exit (Ctrl+X, Y, Enter)

Set permissions:
```bash
chmod 600 .env
```

---

### Step 3: Setup Python Application in cPanel

#### 3.1 Create Python App for Bot

1. Login to **cPanel**
2. Go to **"Setup Python App"**
3. Click **"Create Application"**

**Configuration:**
- **Python Version**: `3.11` (or latest available)
- **Application Root**: `/home/username/repositories/inventory_bot`
- **Application URL**: Leave empty (bot doesn't need URL)
- **Application Startup File**: Leave default
- **Application Entry Point**: Leave default

4. Click **"Create"**

5. Wait for virtual environment to be created

#### 3.2 Install Dependencies

After the app is created, you'll see a command to activate the virtual environment.

**Copy the activation command**, then SSH to your server:

```bash
# Example (adjust path based on your username and Python version)
source ~/virtualenv/repositories/inventory_bot/3.11/bin/activate

# Navigate to project
cd ~/repositories/inventory_bot

# Install dependencies
pip install -r requirements.txt

# This will install:
# - python-telegram-bot>=21.0
# - Pillow>=10.2.0
# - jdatetime==4.1.1
# - python-dotenv==1.0.0
# - fastapi==0.104.1
# - uvicorn[standard]==0.24.0
# - pydantic==2.5.0
```

---

### Step 4: Initialize Database

```bash
# Make sure you're in the virtual environment
cd ~/repositories/inventory_bot
python database/migrate.py
```

This will create:
- `database/warehouse.db` (SQLite database)
- `database/images/` (images folder)

---

### Step 5: Test Bot Locally

```bash
# Still in virtual environment
python bot/bot.py
```

If you see:
```
✅ ربات با موفقیت راه‌اندازی شد!
📱 منتظر دریافت پیام...
```

**Success!** Press Ctrl+C to stop.

---

### Step 6: Setup Bot to Run in Background

#### 6.1 Make Scripts Executable

```bash
cd ~/repositories/inventory_bot/deployment
chmod +x backup_db.sh check_status.sh keep_alive.sh
```

#### 6.2 Update Script Paths

**Edit `keep_alive.sh`:**
```bash
nano ~/repositories/inventory_bot/deployment/keep_alive.sh
```

**Make sure these lines are correct:**
```bash
BOT_DIR="$HOME/repositories/inventory_bot"
VENV_ACTIVATE="$HOME/virtualenv/repositories/inventory_bot/3.11/bin/activate"
```

**Save and exit.**

#### 6.3 Start Bot Manually (First Time)

```bash
cd ~/repositories/inventory_bot
source ~/virtualenv/repositories/inventory_bot/3.11/bin/activate

# Start bot in background
nohup python bot/bot.py > bot.log 2>&1 &

# Check if running
ps aux | grep bot.py
```

You should see the bot process running.

#### 6.4 Test Bot on Telegram

1. Open Telegram
2. Find your bot
3. Send `/start`
4. Enter password: `ciFarco@1213#3221`
5. You should see the main menu!

---

### Step 7: Setup Cron Jobs

#### 7.1 Keep Bot Alive (Check Every 5 Minutes)

1. Go to cPanel **"Cron Jobs"**
2. Add new cron job:

**Minute**: `*/5`  
**Hour**: `*`  
**Day**: `*`  
**Month**: `*`  
**Weekday**: `*`  
**Command**:
```bash
/bin/bash /home/username/repositories/inventory_bot/deployment/keep_alive.sh >> /home/username/repositories/inventory_bot/cron.log 2>&1
```

*(Replace `username` with your actual cPanel username)*

#### 7.2 Daily Database Backup (Run at 2 AM)

1. Add another cron job:

**Minute**: `0`  
**Hour**: `2`  
**Day**: `*`  
**Month**: `*`  
**Weekday**: `*`  
**Command**:
```bash
/bin/bash /home/username/repositories/inventory_bot/deployment/backup_db.sh >> /home/username/repositories/inventory_bot/backup.log 2>&1
```

---

### Step 8: Setup FastAPI (Optional)

If you want to run the API as well:

#### Option A: As Separate Python App in cPanel

1. Go to **"Setup Python App"**
2. Click **"Create Application"**

**Configuration:**
- **Python Version**: `3.11`
- **Application Root**: `/home/username/repositories/inventory_bot`
- **Application URL**: `api.yourdomain.com` (or `/api`)
- **Application Startup File**: Create `passenger_wsgi_api.py` (see below)
- **Application Entry Point**: `app`

**Create `passenger_wsgi_api.py` in project root:**
```python
import sys
import os

# Path to virtual environment
INTERP = os.path.expanduser("~/virtualenv/repositories/inventory_bot/3.11/bin/python3")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Add project to path
sys.path.insert(0, os.getcwd())

# Import FastAPI app
from api.main import app

# Passenger needs 'application' variable
application = app
```

#### Option B: Run API in Background

```bash
cd ~/repositories/inventory_bot
source ~/virtualenv/repositories/inventory_bot/3.11/bin/activate

# Start API in background
nohup python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 >> api.log 2>&1 &
```

---

## 🔍 Verification Checklist

After deployment, verify everything works:

### ✅ Bot Status
```bash
cd ~/repositories/inventory_bot/deployment
./check_status.sh
```

Should show: **Bot is running**

### ✅ Bot Logs
```bash
tail -50 ~/repositories/inventory_bot/bot.log
```

Should show recent activity.

### ✅ Telegram Test
1. Open bot in Telegram
2. Send `/start`
3. Enter password
4. Try creating a category
5. Try adding an item
6. Upload an image
7. Check item details

### ✅ Database Check
```bash
ls -lh ~/repositories/inventory_bot/database/
```

Should show:
- `warehouse.db` (database file)
- `images/` (folder with uploaded images)

### ✅ Cron Jobs Check
```bash
crontab -l
```

Should show both cron jobs.

### ✅ API Check (if setup)
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy","database":"connected"}
```

---

## 🐛 Troubleshooting

### Bot Not Starting

**Check logs:**
```bash
tail -100 ~/repositories/inventory_bot/bot.log
```

**Common issues:**
1. **.env file missing**
   ```bash
   cd ~/repositories/inventory_bot
   ls -la .env
   # If missing, create it with bot token
   ```

2. **Dependencies not installed**
   ```bash
   source ~/virtualenv/repositories/inventory_bot/3.11/bin/activate
   pip list | grep telegram
   # If empty, run: pip install -r requirements.txt
   ```

3. **Wrong Python version**
   ```bash
   python --version
   # Should be 3.11 or higher
   ```

### Bot Keeps Stopping

**Check keep_alive.sh:**
```bash
cat ~/repositories/inventory_bot/deployment/keep_alive.sh
```

Make sure paths are correct.

**Test manually:**
```bash
bash ~/repositories/inventory_bot/deployment/keep_alive.sh
```

### Images Not Uploading

**Check images folder:**
```bash
ls -la ~/repositories/inventory_bot/database/images/
```

**Check permissions:**
```bash
chmod 755 ~/repositories/inventory_bot/database/images/
```

### Database Errors

**Check database file:**
```bash
ls -la ~/repositories/inventory_bot/database/warehouse.db
```

**Reinitialize if needed:**
```bash
cd ~/repositories/inventory_bot
python database/migrate.py
```

---

## 📊 Monitoring

### View Bot Logs (Real-time)
```bash
tail -f ~/repositories/inventory_bot/bot.log
```

### View Cron Logs
```bash
tail -50 ~/repositories/inventory_bot/cron.log
```

### View Backup Logs
```bash
tail -50 ~/repositories/inventory_bot/backup.log
```

### Check Running Processes
```bash
ps aux | grep python
```

### Stop Bot (if needed)
```bash
pkill -f "bot/bot.py"
```

### Restart Bot
```bash
cd ~/repositories/inventory_bot
source ~/virtualenv/repositories/inventory_bot/3.11/bin/activate
nohup python bot/bot.py > bot.log 2>&1 &
```

---

## 📁 Important Paths Reference

```
Project Root:       ~/repositories/inventory_bot/
Virtual Env:        ~/virtualenv/repositories/inventory_bot/3.11/
Python Executable:  ~/virtualenv/repositories/inventory_bot/3.11/bin/python
Database File:      ~/repositories/inventory_bot/database/warehouse.db
Images Folder:      ~/repositories/inventory_bot/database/images/
Bot Log:            ~/repositories/inventory_bot/bot.log
Cron Log:           ~/repositories/inventory_bot/cron.log
Backup Folder:      ~/repositories/inventory_bot/backups/
```

---

## 🔄 Updating the Bot

When you push changes to GitHub:

```bash
# SSH to server
ssh username@your-server.com

# Navigate to project
cd ~/repositories/inventory_bot

# Stop bot
pkill -f "bot/bot.py"

# Pull latest changes
git pull origin main

# Activate virtual env
source ~/virtualenv/repositories/inventory_bot/3.11/bin/activate

# Update dependencies (if needed)
pip install -r requirements.txt

# Run migrations (if any)
python database/migrate.py

# Restart bot
nohup python bot/bot.py > bot.log 2>&1 &

# Verify
ps aux | grep bot.py
```

---

## 📝 Quick Commands Cheat Sheet

```bash
# Activate virtual environment
source ~/virtualenv/repositories/inventory_bot/3.11/bin/activate

# Check bot status
ps aux | grep bot.py

# View logs
tail -50 ~/repositories/inventory_bot/bot.log

# Stop bot
pkill -f "bot/bot.py"

# Start bot
cd ~/repositories/inventory_bot && nohup python bot/bot.py > bot.log 2>&1 &

# Check database
ls -lh ~/repositories/inventory_bot/database/

# Check images
ls -lh ~/repositories/inventory_bot/database/images/

# View backups
ls -lh ~/repositories/inventory_bot/backups/

# Update from git
cd ~/repositories/inventory_bot && git pull origin main

# Restart everything
pkill -f "bot/bot.py" && sleep 2 && cd ~/repositories/inventory_bot && source ~/virtualenv/repositories/inventory_bot/3.11/bin/activate && nohup python bot/bot.py > bot.log 2>&1 &
```

---

## ✅ Deployment Complete!

Your warehouse management bot is now running on cPanel with:

- ✅ Telegram Bot (running in background)
- ✅ SQLite Database (in `database/` folder)
- ✅ Image Storage (in `database/images/`)
- ✅ Auto-restart (via cron job every 5 minutes)
- ✅ Daily Backups (at 2 AM daily)
- ✅ Error Logging (in `bot.log`)

**Test your bot on Telegram and enjoy!** 🎉

---

## 📞 Need Help?

- Check logs: `tail -50 ~/repositories/inventory_bot/bot.log`
- Check status: `ps aux | grep bot.py`
- View this guide: `/deployment/DEPLOYMENT.md`
- Check docs: `/docs/` folder

**Your bot is ready to manage your warehouse!** 🏪


cd ~/repositories/inventory_bot && \
pkill -f bot.py && \
sleep 2 && \
git pull origin main && \
sleep 2 && \
chmod +x backup_db.sh start_bot.sh keep_alive.sh check_status.sh && \
./start_bot.sh && \
sleep 2 && \
./check_status.sh