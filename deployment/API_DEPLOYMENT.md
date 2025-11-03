# FastAPI Deployment on cPanel - Quick Guide

## Method 1: Using Passenger (Recommended)

### Prerequisites
- File `deployment/passenger_wsgi_api.py` exists
- Python app created in cPanel

### Steps:
1. Go to cPanel → **Setup Python App**
2. Click **Create Application**
3. Configure:
   - Python Version: `3.11`
   - Application Root: `/home/username/app`
   - Application URL: `api.yourdomain.com` or `/api`
   - Startup File: `deployment/passenger_wsgi_api.py` ⬅️ **Important!**
   - Entry Point: `application`
4. Click **Create**
5. Restart the application

### Test:
```
https://api.yourdomain.com/health
https://api.yourdomain.com/docs
```

---

## Method 2: Background Process with Uvicorn

### Start API:
```bash
cd ~/app/deployment
chmod +x start_api.sh stop_api.sh check_api_status.sh
./start_api.sh
```

### Check Status:
```bash
./check_api_status.sh
```

### Stop API:
```bash
./stop_api.sh
```

### Keep Alive (Cron Job):
Add to cPanel → Cron Jobs:
```
*/5 * * * * /bin/bash /home/username/app/deployment/keep_api_alive.sh >> /home/username/app/api_cron.log 2>&1
```

---

## Reverse Proxy Setup (for Method 2)

If using background process, create `.htaccess`:

```apache
# ~/public_html/api/.htaccess
RewriteEngine On
RewriteRule ^(.*)$ http://localhost:8000/$1 [P,L]
```

---

## Restart Everything

```bash
cd ~/app/deployment
chmod +x restart_all.sh
./restart_all.sh
```

This will:
- Stop bot and API
- Pull latest changes
- Update dependencies
- Restart both services
- Show status

---

## Troubleshooting

### Check logs:
```bash
tail -50 ~/app/api.log
```

### Check if running:
```bash
ps aux | grep uvicorn
```

### Reinstall dependencies:
```bash
cd ~/app
source ~/virtualenv/app/3.11/bin/activate
pip install -r requirements.txt --force-reinstall
```

---

## Quick Commands

```bash
# Status
./deployment/check_api_status.sh

# Start
./deployment/start_api.sh

# Stop
./deployment/stop_api.sh

# Restart all
./deployment/restart_all.sh

# View logs
tail -f ~/app/api.log
```

