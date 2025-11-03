# Quick Reference Card

## 🚀 Start Commands

### Telegram Bot
```bash
# Windows
start_bot.bat

# Linux
./start_bot.sh

# Manual
python bot/bot.py
```

### FastAPI Backend
```bash
# Windows
start_api.bat

# Linux
./start_api.sh

# Manual
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 📂 Project Structure
```
warehousing/
├── bot/        → Telegram Bot
├── database/   → SQLite Database
├── api/        → REST API
└── webApp/     → Future Web App
```

---

## 🌐 API Endpoints (http://localhost:8000)

### Items
- `GET /api/items` - List all items
- `GET /api/items/search?q=keyword` - Search
- `GET /api/items/{id}` - Get item
- `PATCH /api/items/{id}/stock` - Update stock

### Categories
- `GET /api/categories` - List categories
- `GET /api/categories/{id}/subcategories` - Get subs

### Brands
- `GET /api/brands` - List brands
- `GET /api/brands/{id}/items` - Get brand items

### Other
- `GET /api/stats` - Statistics
- `GET /api/low-stock` - Low stock items
- `GET /api/measure-types` - Measurement units

### Documentation
- `GET /docs` - Swagger UI
- `GET /redoc` - ReDoc
- `GET /health` - Health check

---

## 📝 Important Files

### Configuration
- `.env` - Environment variables (BOT_TOKEN, PASSWORD)

### Database
- `database/warehouse.db` - SQLite database file

### Scripts
- `start_bot.bat/sh` - Run bot
- `start_api.bat/sh` - Run API
- `backup_db.sh` - Backup database (Linux)

### Documentation
- `README.md` - Main docs
- `MIGRATION_GUIDE.md` - Migration info
- `ARCHITECTURE.md` - System design
- `bot/README.md` - Bot docs
- `database/README.md` - Database docs
- `api/README.md` - API docs

---

## 🔐 Environment Variables

Create `.env` file:
```env
TELEGRAM_BOT_TOKEN=your_token_here
BOT_PASSWORD=ciFarco@1213#3221
```

---

## 📦 Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🧪 Test Commands

### Test Bot
```bash
python bot/bot.py
```

### Test API
```bash
# Terminal 1: Start API
python -m uvicorn api.main:app --reload

# Terminal 2: Test
curl http://localhost:8000/api/items
curl http://localhost:8000/api/stats
curl http://localhost:8000/health
```

### Test in Browser
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

---

## 🐛 Troubleshooting

### Bot won't start
- Check `.env` file exists
- Check `TELEGRAM_BOT_TOKEN` is set
- Run: `python bot/bot.py`

### API won't start
- Install uvicorn: `pip install uvicorn[standard]`
- Check port 8000 is free
- Run: `python -m uvicorn api.main:app --reload`

### Import errors
- Install dependencies: `pip install -r requirements.txt`
- Check you're in project root
- Check folder structure is correct

---

## 📊 Database Info

- **Type**: SQLite
- **File**: `database/warehouse.db`
- **Location**: `/database/` folder
- **Backup**: Daily (via `backup_db.sh`)

---

## 🎯 Module Responsibilities

| Module | Purpose |
|--------|---------|
| `/bot/` | Telegram bot interface |
| `/database/` | Database operations |
| `/api/` | REST API for web apps |
| `/webApp/` | Future web interface |

---

## 📮 Git Commands

```bash
# Status
git status

# Add all
git add .

# Commit
git commit -m "Your message"

# Push
git push origin main

# Pull
git pull origin main
```

---

## 🎓 Key Features

### Bot Features
✅ Password authentication
✅ Full CRUD operations
✅ Image upload
✅ Search & filter
✅ Low stock alerts
✅ Persian UI

### API Features
✅ RESTful endpoints
✅ Auto documentation
✅ Search & filter
✅ Pagination
✅ CORS enabled
✅ JSON responses

---

## 📞 Help

- Main docs: `README.md`
- Migration guide: `MIGRATION_GUIDE.md`
- Architecture: `ARCHITECTURE.md`
- Module docs: See `README.md` in each folder

---

**Quick Start:**
1. Install: `pip install -r requirements.txt`
2. Config: Create `.env` with bot token
3. Run bot: `start_bot.bat` or `python bot/bot.py`
4. Run API: `start_api.bat` or `uvicorn api.main:app --reload`
5. Test: http://localhost:8000/docs

✨ **You're ready to go!**

