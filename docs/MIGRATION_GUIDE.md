# Project Restructure - Migration Guide

## 🎉 What's New?

Your project has been restructured into a clean, modular architecture:

```
warehousing/
├── bot/              # Telegram Bot
├── database/         # Database Layer
├── api/              # REST API Backend
└── webApp/           # Future Web App
```

---

## 📦 New Project Structure

### Before (Old Structure):
```
warehousing/
├── bot.py
├── database.py
├── handlers_*.py
├── messages.py
├── utils.py
└── warehouse.db
```

### After (New Structure):
```
warehousing/
├── bot/
│   ├── bot.py
│   ├── handlers_*.py
│   ├── messages.py
│   └── README.md
│
├── database/
│   ├── database.py
│   ├── utils.py
│   ├── warehouse.db (will be created at runtime)
│   └── README.md
│
├── api/
│   ├── main.py (NEW!)
│   ├── requirements.txt
│   └── README.md
│
├── webApp/
│   └── README.md (placeholder for future)
│
├── requirements.txt (updated)
├── start_bot.bat/sh (updated)
├── start_api.bat/sh (NEW!)
└── README.md (completely rewritten)
```

---

## 🚀 How to Use

### 1. Running the Telegram Bot

**Windows:**
```cmd
start_bot.bat
```

**Linux/cPanel:**
```bash
./start_bot.sh
```

**Manual:**
```bash
python bot/bot.py
```

### 2. Running the API (NEW!)

**Windows:**
```cmd
start_api.bat
```

**Linux/cPanel:**
```bash
./start_api.sh
```

**Manual:**
```bash
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

Then visit:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

---

## 📝 What Changed?

### 1. Import Statements
All files now use the new module structure:

**Before:**
```python
import database as db
import messages as msg
import utils
```

**After:**
```python
from database import database as db
from bot import messages as msg
from database import utils
```

### 2. File Locations
- All bot files moved to `/bot/`
- Database files moved to `/database/`
- New API created in `/api/`

### 3. New API Backend
A complete REST API has been created with 15+ endpoints:

#### Key Endpoints:
- `GET /api/items` - Get all items
- `GET /api/items/search?q=keyword` - Search items
- `GET /api/items/{id}` - Get item details
- `PATCH /api/items/{id}/stock` - Update stock
- `GET /api/categories` - Get categories
- `GET /api/brands` - Get brands
- `GET /api/low-stock` - Get low stock items
- `GET /api/stats` - Get statistics

### 4. Documentation
Each module now has its own README:
- `/bot/README.md` - Bot documentation
- `/database/README.md` - Database documentation
- `/api/README.md` - API documentation
- `/webApp/README.md` - Future web app docs
- `/README.md` - Main project documentation

---

## 🔧 Dependencies

Updated `requirements.txt` includes:
```txt
python-telegram-bot>=21.0
Pillow>=10.2.0
jdatetime==4.1.1
python-dotenv==1.0.0
fastapi==0.104.1          # NEW
uvicorn[standard]==0.24.0  # NEW
pydantic==2.5.0           # NEW
```

Install/update:
```bash
pip install -r requirements.txt
```

---

## 🚢 Deployment Changes

### Local Development
No changes needed - just use the new start scripts.

### cPanel Deployment

#### For the Bot (existing):
1. Update paths in existing shell scripts if needed
2. Bot continues to run as before

#### For the API (new):
Create a **second Python app** in cPanel:

1. **Setup Python App**
   - Application Root: `/home/username/repositories/inventory_bot`
   - Application Startup File: Create `passenger_wsgi_api.py` (see below)
   - Application URL: `api.yourdomain.com` or `/api`

2. **Create `passenger_wsgi_api.py`:**
```python
import sys
import os

INTERP = os.path.expanduser("~/virtualenv/repositories/inventory_bot/3.11/bin/python3")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0, os.getcwd())

from api.main import app
application = app
```

---

## 🎯 Benefits of New Structure

### 1. **Modularity**
- Each component is independent
- Easy to maintain and update
- Clear separation of concerns

### 2. **Scalability**
- Easy to add new features
- Bot and API can run independently
- Ready for web app integration

### 3. **Documentation**
- Each module has its own README
- Clear API documentation (auto-generated)
- Easy onboarding for new developers

### 4. **Web App Ready**
- API is ready to be consumed by Angular/React/Vue
- CORS enabled
- RESTful design

### 5. **Better Organization**
```
bot/        → Everything about Telegram bot
database/   → All database operations
api/        → REST API for web apps
webApp/     → Future frontend
```

---

## 📊 API Features

Your new API includes:

✅ **15+ RESTful Endpoints**
✅ **Auto-generated documentation** (Swagger/OpenAPI)
✅ **Search & filtering**
✅ **Pagination support**
✅ **CORS enabled**
✅ **JSON responses**
✅ **Error handling**
✅ **Type validation** (Pydantic)

---

## 🧪 Testing the New Structure

### Test the Bot:
```bash
python bot/bot.py
```

### Test the API:
```bash
# Start the API
python -m uvicorn api.main:app --reload

# In another terminal, test:
curl http://localhost:8000/api/items
curl http://localhost:8000/api/stats
curl "http://localhost:8000/api/items/search?q=test"
```

### Test API in Browser:
Visit: http://localhost:8000/docs

---

## 🔄 Migration Checklist

- [x] Create new folder structure
- [x] Move files to appropriate folders
- [x] Update all import statements
- [x] Create FastAPI backend
- [x] Update startup scripts
- [x] Create module READMEs
- [x] Update main README
- [x] Add API documentation
- [ ] Test bot functionality
- [ ] Test API endpoints
- [ ] Commit changes to git
- [ ] Deploy to cPanel (if needed)

---

## 🎓 Next Steps

1. **Test Locally:**
   - Run bot: `python bot/bot.py`
   - Run API: `python -m uvicorn api.main:app --reload`
   - Test API: http://localhost:8000/docs

2. **Commit Changes:**
   ```bash
   git add .
   git commit -m "Restructure project: separate bot, database, api modules"
   git push origin main
   ```

3. **Deploy API to cPanel** (optional):
   - See "Deployment Changes" section above
   - Create passenger_wsgi_api.py
   - Setup second Python app

4. **Develop Web App** (future):
   - Choose framework (Angular/React/Vue)
   - Create app in `/webApp/` folder
   - Consume API from `/api/`

---

## 🆘 Troubleshooting

### Import Errors
If you get import errors, make sure:
1. You're running from project root
2. All `__init__.py` files exist
3. Python path includes parent directory

### API Won't Start
```bash
# Check if port 8000 is available
pip install uvicorn[standard]
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
```

### Bot Won't Start
```bash
# Check .env file exists
# Check imports are correct
python bot/bot.py
```

---

## 📞 Support

For issues:
1. Check module README in respective folder
2. Check main project README
3. Review API documentation: http://localhost:8000/docs
4. Contact development team

---

**Happy coding! 🚀**

Your warehouse management system is now modular, scalable, and web-app ready!

