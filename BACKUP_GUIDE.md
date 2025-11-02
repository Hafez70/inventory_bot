# Database Backup Guide for cPanel

This guide explains how to set up automatic daily backups of your warehouse database on cPanel.

## 📋 Overview

The backup system:
- Creates daily backups of `warehouse.db` with timestamps
- Automatically deletes backups older than 30 days (configurable)
- Stores backups in the `backups/` folder
- Runs automatically via cron job

## 🚀 Setup Instructions

### Step 1: Upload Backup Script

The `backup_db.sh` script is already in your repository. After pulling the latest code:

```bash
cd ~/repositories/inventory_bot
git pull origin main
chmod +x backup_db.sh
```

### Step 2: Test the Backup Script

Test the backup manually first:

```bash
./backup_db.sh
```

You should see:
```
✓ Backup created successfully: /home/xqaebsls/repositories/inventory_bot/backups/warehouse_backup_20251102_123456.db
  Size: 12K
  Cleaning up old backups (keeping last 30 days)...
  Total backups: 1
```

### Step 3: Set Up Cron Job in cPanel

1. **Login to cPanel**
2. **Go to: Advanced → Cron Jobs**
3. **Add New Cron Job:**

   - **Common Settings**: Select "Once Per Day (0 0 * * *)" or customize
   - **Minute**: `0`
   - **Hour**: `2` (2 AM - or choose your preferred time)
   - **Day**: `*`
   - **Month**: `*`
   - **Weekday**: `*`
   - **Command**: 
     ```bash
     /bin/bash /home/xqaebsls/repositories/inventory_bot/backup_db.sh >> /home/xqaebsls/repositories/inventory_bot/backup.log 2>&1
     ```

4. **Click "Add New Cron Job"**

### Alternative Cron Schedule Options

- **Every day at 2 AM**: `0 2 * * *`
- **Every day at midnight**: `0 0 * * *`
- **Every 12 hours**: `0 */12 * * *`
- **Every 6 hours**: `0 */6 * * *`

## 📁 Backup Location

Backups are stored in:
```
~/repositories/inventory_bot/backups/
```

Backup filename format:
```
warehouse_backup_YYYYMMDD_HHMMSS.db
```

Example:
```
warehouse_backup_20251102_020000.db
warehouse_backup_20251103_020000.db
```

## 🔧 Configuration

Edit `backup_db.sh` to customize:

```bash
KEEP_DAYS=30  # Change to keep backups for more/fewer days
```

## 📊 View Backup Status

Check backup logs:
```bash
tail -f ~/repositories/inventory_bot/backup.log
```

List all backups:
```bash
ls -lh ~/repositories/inventory_bot/backups/
```

Count backups:
```bash
ls -1 ~/repositories/inventory_bot/backups/ | wc -l
```

## 🔄 Restore from Backup

To restore a backup:

1. **Stop the bot**:
   ```bash
   cd ~/repositories/inventory_bot
   kill $(cat bot.pid)
   ```

2. **Backup current database** (just in case):
   ```bash
   cp warehouse.db warehouse.db.before_restore
   ```

3. **Restore from backup**:
   ```bash
   cp backups/warehouse_backup_20251102_020000.db warehouse.db
   ```

4. **Restart the bot**:
   ```bash
   ./start_bot.sh
   ```

## 💾 Download Backups to Local Computer

### Option 1: Via cPanel File Manager
1. Go to **cPanel → File Manager**
2. Navigate to: `repositories/inventory_bot/backups/`
3. Select backup file(s)
4. Click **Download**

### Option 2: Via SCP (if SSH access available)
```bash
scp xqaebsls@yourserver.com:~/repositories/inventory_bot/backups/*.db ./local_backups/
```

### Option 3: Via FTP
Use an FTP client (FileZilla, WinSCP) to download from:
```
/home/xqaebsls/repositories/inventory_bot/backups/
```

## 🔍 Verify Cron Job is Running

Check if cron job exists:
```bash
crontab -l | grep backup_db
```

Check recent backup logs:
```bash
tail -20 ~/repositories/inventory_bot/backup.log
```

## ⚠️ Important Notes

1. **Backups are NOT included in Git** (added to `.gitignore`)
2. **Old backups are auto-deleted** after 30 days (configurable)
3. **Backups are stored on the same server** - for critical data, also download backups to a separate location
4. **Database file is locked** while bot is running, but `cp` command safely copies it

## 🎯 Best Practices

1. **Test restore process** periodically to ensure backups work
2. **Download important backups** to your local computer regularly
3. **Monitor backup logs** to ensure cron job runs successfully
4. **Keep backups offsite** for disaster recovery

## 📧 Email Notifications (Optional)

To receive email notifications when backups complete, modify the cron command:

```bash
0 2 * * * /bin/bash /home/xqaebsls/repositories/inventory_bot/backup_db.sh 2>&1 | mail -s "Database Backup Report" your-email@example.com
```

## 🆘 Troubleshooting

### Backup not created?
- Check cron job syntax in cPanel
- Verify script has execute permission: `chmod +x backup_db.sh`
- Check backup.log for errors: `cat backup.log`

### Out of disk space?
- Reduce `KEEP_DAYS` in backup_db.sh
- Manually delete old backups: `rm ~/repositories/inventory_bot/backups/warehouse_backup_2024*.db`
- Check disk usage: `du -sh ~/repositories/inventory_bot/backups/`

### Backup file is 0 bytes?
- Check if warehouse.db exists and has data
- Ensure bot is running and database is initialized

