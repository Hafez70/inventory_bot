# API Deployment Files

This folder contains all files needed for API deployment on cPanel.

## Files

### For Method 1 (Passenger - Recommended):
- **`passenger_wsgi_api.py`** - WSGI wrapper for cPanel's Setup Python App
  - Use this when creating Python app in cPanel
  - In cPanel, set Startup File to: `deployment/passenger_wsgi_api.py`

### For Method 2 (Background Process):
- **`start_api.sh`** - Start API manually
- **`stop_api.sh`** - Stop API
- **`check_api_status.sh`** - Check if API is running
- **`keep_api_alive.sh`** - Cron job to keep API running
- **`api_htaccess_example.txt`** - Example .htaccess for reverse proxy

### For Both Methods:
- **`restart_all.sh`** - Restart both bot and API
- **`API_DEPLOYMENT.md`** - Complete API deployment guide

## Quick Setup

### Method 1 (cPanel Passenger):
1. Go to cPanel → Setup Python App
2. Create application:
   - Application Root: `/home/username/app`
   - Startup File: `deployment/passenger_wsgi_api.py` ⬅️ **Note the path!**
   - Entry Point: `application`
3. Restart app

### Method 2 (Background):
```bash
cd ~/app/deployment
chmod +x *.sh
./start_api.sh
```

## Documentation
See `API_DEPLOYMENT.md` for detailed instructions.

