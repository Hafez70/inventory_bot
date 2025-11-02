# 🚀 Deployment Guide for cPanel

This guide explains how to deploy and run the Telegram Warehouse Bot on cPanel using the Passenger + Cron approach.

## 📋 Prerequisites

- cPanel access
- Telegram Bot Token from @BotFather
- Git installed on cPanel (usually pre-installed)

## 🔧 Initial Setup (One-Time)

### Step 1: Clone Repository

In cPanel Terminal:

```bash
cd ~/repositories
git clone https://github.com/Hafez70/inventory_bot.git
cd inventory_bot
```

### Step 2: Create .env File

```bash
cd ~/repositories/inventory_bot
nano .env
```

Add your bot token:
```
TELEGRAM_BOT_TOKEN=your_actual_bot_token_here
```

Save: `Ctrl+X` → `Y` → `Enter`

**⚠️ Important:** Never commit `.env` to git (it's already in .gitignore)

### Step 3: Setup Python App in cPanel

1. Open **cPanel Dashboard**
2. Go to **Software** → **Setup Python App**
3. Click **"CREATE APPLICATION"**
4. Configure:
   - Python version: `3.9` or higher
   - Application root: `repositories/inventory_bot`
   - Application URL: Leave empty (optional)
   - Application startup file: `passenger_wsgi.py`
   - Application entry point: `application`
5. Click **CREATE**

### Step 4: Install Dependencies

After creating the app, cPanel shows a command like:
```bash
source /home/USERNAME/virtualenv/repositories/inventory_bot/3.9/bin/activate
```

Copy and run it, then:

```bash
cd ~/repositories/inventory_bot
pip install -r requirements.txt
```

### Step 5: Initialize Database

```bash
cd ~/repositories/inventory_bot
python migrate.py
```

### Step 6: Make Scripts Executable

```bash
cd ~/repositories/inventory_bot
chmod +x keep_alive.sh start_bot.sh check_status.sh
```

### Step 7: Update keep_alive.sh Paths

Edit `keep_alive.sh` if your paths are different:

```bash
nano keep_alive.sh
```

Update the `VENV_ACTIVATE` path to match what cPanel showed you in Step 4.

Save: `Ctrl+X` → `Y` → `Enter`

### Step 8: Start Bot Manually (First Time)

```bash
cd ~/repositories/inventory_bot
./start_bot.sh
```

Verify it's working:
```bash
./check_status.sh
```

Test in Telegram by sending `/start` to your bot.

### Step 9: Setup Cron Job (Auto-Restart)

1. Go to **cPanel** → **Cron Jobs**
2. Add new cron job:
   - **Minute**: `*/5` (every 5 minutes)
   - **Hour**: `*`
   - **Day**: `*`
   - **Month**: `*`
   - **Weekday**: `*`
   - **Command**: `/home/YOUR_USERNAME/repositories/inventory_bot/keep_alive.sh`

Replace `YOUR_USERNAME` with your actual cPanel username.

**What this does:** Checks every 5 minutes if bot is running, restarts it if not.

### Step 10: Verify Status Page (Optional)

If you set an Application URL in Step 3, visit it in your browser to see a beautiful status page.

If you didn't set a URL, you can still access it via:
- Your domain + port (cPanel will show you)
- Or skip this - the bot works without it

---

## 🔄 Updating the Bot

When you make changes and push to GitHub:

```bash
cd ~/repositories/inventory_bot

# Pull latest changes
git pull origin main

# If requirements.txt changed, reinstall dependencies
source /home/YOUR_USERNAME/virtualenv/repositories/inventory_bot/3.9/bin/activate
pip install -r requirements.txt

# Restart bot
pkill -f bot.py
./start_bot.sh

# Or let cron restart it automatically within 5 minutes
```

---

## 📊 Management Commands

### Check Bot Status
```bash
cd ~/repositories/inventory_bot
./check_status.sh
```

### Start Bot
```bash
cd ~/repositories/inventory_bot
./start_bot.sh
```

### Stop Bot
```bash
pkill -f bot.py
# Or using PID:
kill $(cat ~/repositories/inventory_bot/bot.pid)
```

### View Logs (Live)
```bash
tail -f ~/repositories/inventory_bot/bot.log
```

### View Last 50 Log Lines
```bash
tail -50 ~/repositories/inventory_bot/bot.log
```

### Restart Bot
```bash
pkill -f bot.py
cd ~/repositories/inventory_bot
./start_bot.sh
```

---

## 🐛 Troubleshooting

### Bot Not Starting

**Check logs:**
```bash
tail -50 ~/repositories/inventory_bot/bot.log
```

**Common issues:**
- ❌ `.env` file missing → Create it with your bot token
- ❌ Dependencies not installed → Run pip install again
- ❌ Wrong virtual environment path → Update keep_alive.sh
- ❌ Database not initialized → Run migrate.py

### Bot Keeps Stopping

**Check if cron is running:**
```bash
crontab -l | grep keep_alive
```

Should show your cron job. If not, add it again in cPanel.

### Can't Find Virtual Environment

**Find the correct path:**
```bash
find /home -name "activate" -path "*/inventory_bot*/bin/activate" 2>/dev/null
```

Use this path in `keep_alive.sh` and `start_bot.sh`.

### Bot Token Issues

**Verify token:**
```bash
cd ~/repositories/inventory_bot
cat .env
```

Make sure token is correct (no spaces, quotes, or extra characters).

**Test token:**
```bash
curl https://api.telegram.org/bot<YOUR_TOKEN>/getMe
```

Should return bot information.

---

## 🎯 Architecture

This setup uses:

1. **Passenger (passenger_wsgi.py)**: Provides status page and monitoring
2. **Cron (keep_alive.sh)**: Ensures bot stays running
3. **nohup**: Runs bot in background
4. **PID file**: Tracks bot process

**Benefits:**
- ✅ Auto-restart on crash
- ✅ Auto-start on server reboot
- ✅ Status page for monitoring
- ✅ Works within cPanel shared hosting limits
- ✅ Reliable and production-ready

---

## 📝 Notes

- Bot logs are in `~/repositories/inventory_bot/bot.log`
- Database is in `~/repositories/inventory_bot/warehouse.db`
- Images are stored in `~/repositories/inventory_bot/images/`
- PID file is in `~/repositories/inventory_bot/bot.pid`

---

## 🆘 Support

If you encounter issues:

1. Check logs: `tail -50 ~/repositories/inventory_bot/bot.log`
2. Check status: `./check_status.sh`
3. Try manual start: `./start_bot.sh`
4. Check cron: `crontab -l`

---

## ✅ Verification Checklist

After setup, verify:
- [ ] Bot responds to `/start` in Telegram
- [ ] `./check_status.sh` shows bot is running
- [ ] Cron job is set up (`crontab -l`)
- [ ] Status page loads (if URL configured)
- [ ] Bot auto-restarts after kill test: `pkill -f bot.py` then wait 5 minutes

---

**Your bot is now production-ready on cPanel!** 🎉

