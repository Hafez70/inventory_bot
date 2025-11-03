# 🚀 Quick Start Guide for cPanel Deployment

## For the Impatient! ⚡

---

## Step 1: Upload Files (5 minutes)

### Via Git (Easiest):
```bash
ssh username@your-server.com
cd ~/repositories
git clone https://github.com/Hafez70/inventory_bot.git
cd inventory_bot
```

### Via File Manager:
1. Login to cPanel
2. File Manager → `/home/username/repositories/`
3. Upload zip file
4. Extract

---

## Step 2: Create .env File (1 minute)

```bash
cd ~/repositories/inventory_bot
nano .env
```

**Add this:**
```
TELEGRAM_BOT_TOKEN=8230888056:AAECbaqgYKRcDHpkAVpAfELsMgYOC5QO3iM
BOT_PASSWORD=ciFarco@1213#3221
```

Save (Ctrl+X, Y, Enter)

---

## Step 3: Setup Python App (2 minutes)

1. cPanel → **Setup Python App**
2. **Create Application**
   - Python Version: `3.11`
   - App Root: `/home/username/repositories/inventory_bot`
   - Leave other fields empty
3. Click **Create**
4. Wait for it to finish

---

## Step 4: Run Auto-Deploy Script (2 minutes)

```bash
cd ~/repositories/inventory_bot
chmod +x deployment/deploy.sh
./deployment/deploy.sh
```

**This script will:**
- ✅ Check everything
- ✅ Install dependencies
- ✅ Initialize database
- ✅ Start the bot
- ✅ Show you cron job commands

---

## Step 5: Setup Cron Jobs (2 minutes)

Go to cPanel → **Cron Jobs**

**Add these 2 cron jobs:**

### Cron 1: Keep Bot Alive (every 5 min)
```
*/5 * * * * /bin/bash ~/repositories/inventory_bot/deployment/keep_alive.sh >> ~/repositories/inventory_bot/cron.log 2>&1
```

### Cron 2: Daily Backup (2 AM)
```
0 2 * * * /bin/bash ~/repositories/inventory_bot/deployment/backup_db.sh >> ~/repositories/inventory_bot/backup.log 2>&1
```

*(Replace `~` with `/home/username` if needed)*

---

## Step 6: Test Bot! 🎉

1. Open Telegram
2. Find your bot
3. Send: `/start`
4. Enter: `ciFarco@1213#3221`
5. **Done!** Main menu should appear

---

## 📊 Quick Commands

```bash
# Check if bot is running
ps aux | grep bot.py

# View logs
tail -50 ~/repositories/inventory_bot/bot.log

# Stop bot
pkill -f "bot/bot.py"

# Start bot
cd ~/repositories/inventory_bot
source ~/virtualenv/repositories/inventory_bot/3.11/bin/activate
nohup python bot/bot.py > bot.log 2>&1 &

# Check status
~/repositories/inventory_bot/deployment/check_status.sh
```

---

## 🐛 Something Wrong?

### Bot won't start?
```bash
# Check logs
tail -100 ~/repositories/inventory_bot/bot.log

# Check .env file
cat ~/repositories/inventory_bot/.env
```

### Dependencies issue?
```bash
cd ~/repositories/inventory_bot
source ~/virtualenv/repositories/inventory_bot/3.11/bin/activate
pip install -r requirements.txt
```

### Database issue?
```bash
cd ~/repositories/inventory_bot
python database/migrate.py
```

---

## ✅ That's It!

**Total time:** ~12 minutes

**Your bot is now:**
- ✅ Running 24/7
- ✅ Auto-restarting if it crashes
- ✅ Backing up daily
- ✅ Logging everything

**Enjoy your warehouse management system!** 🏪

---

## 📚 Need More Details?

See the full guide: [`deployment/CPANEL_DEPLOYMENT.md`](./CPANEL_DEPLOYMENT.md)

