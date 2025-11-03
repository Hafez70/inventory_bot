# Authentication System Update Guide

## Overview
The bot now requires password authentication before users can access any features. Users must enter the correct password when they first start the bot.

## Default Password
```
ciFarco@1213#3221
```

## Changes Made

### 1. Database Changes
- Added `authenticated_users` table to store authenticated users
- Fields: `user_id`, `username`, `first_name`, `last_name`, `authenticated_at`

### 2. Bot Changes
- `/start` command now asks for password if user is not authenticated
- All operations require authentication
- Password verification with success/failure messages
- User information is saved after successful authentication

### 3. Persian Messages
- 🔐 Welcome message with password request
- ✅ Success message after authentication
- ❌ Failed authentication message
- 🔒 Access denied message for unauthenticated users

## Deployment to cPanel

### Step 1: Stop the Bot
```bash
cd ~/repositories/inventory_bot
pkill -f bot.py
```

### Step 2: Pull Latest Changes
```bash
git reset --hard origin/main
git pull origin main
```

### Step 3: Run Migration
```bash
source ~/virtualenv/repositories/inventory_bot/3.11/bin/activate
python migrate.py
```

Expected output:
```
🔄 Running database migration...
➕ Creating authenticated_users table...
✅ Migration completed successfully!
```

### Step 4: (Optional) Set Custom Password in .env
If you want to change the password from the default:

```bash
nano .env
```

Add this line:
```
BOT_PASSWORD=YOUR_CUSTOM_PASSWORD_HERE
```

Save and exit (Ctrl+X, then Y, then Enter)

### Step 5: Restart the Bot
```bash
./start_bot.sh
```

### Step 6: Verify Bot is Running
```bash
./check_status.sh
```

## Testing the Authentication

1. Open Telegram and find your bot
2. Send `/start` command
3. You should see: 🔐 **خوش آمدید!** (Welcome message asking for password)
4. Enter the password: `ciFarco@1213#3221`
5. You should see: ✅ **احراز هویت موفق!** (Authentication successful)
6. Main menu will appear automatically

## Security Notes

1. **Change Default Password**: For production, consider changing the default password in `.env` file
2. **Backup Database**: The authenticated users are stored in `warehouse.db`, make sure backups include this table
3. **Reset Authentication**: If you need to remove a user's authentication, delete them from the `authenticated_users` table:
   ```sql
   DELETE FROM authenticated_users WHERE user_id = USER_ID;
   ```

## Troubleshooting

### Problem: Bot doesn't ask for password
**Solution**: Check if user is already authenticated. Stop bot, run migration again, restart bot.

### Problem: Wrong password but bot accepts it
**Solution**: 
1. Check `.env` file for `BOT_PASSWORD` value
2. If not set, default is: `ciFarco@1213#3221`
3. Make sure there are no extra spaces

### Problem: Error "AUTH_REQUEST not found"
**Solution**: You may not have pulled the latest code. Run:
```bash
git pull origin main
./start_bot.sh
```

## View Authenticated Users

To see how many users are authenticated:
```bash
sqlite3 warehouse.db "SELECT COUNT(*) FROM authenticated_users;"
```

To see all authenticated users:
```bash
sqlite3 warehouse.db "SELECT user_id, username, first_name, authenticated_at FROM authenticated_users;"
```

## Complete Deployment Commands (All-in-One)

```bash
cd ~/repositories/inventory_bot && \
pkill -f bot.py && \
sleep 2 && \
git reset --hard origin/main && \
git pull origin main && \
source ~/virtualenv/repositories/inventory_bot/3.11/bin/activate && \
python migrate.py && \
./start_bot.sh && \
sleep 2 && \
./check_status.sh
```

This will:
1. Navigate to bot directory
2. Stop the bot
3. Pull latest changes
4. Activate virtual environment
5. Run migration
6. Start the bot
7. Check bot status

---

**Important**: After deployment, test the authentication by sending `/start` to the bot from a new Telegram account or after deleting your user from `authenticated_users` table.

