# Warehouse Management System

A comprehensive warehouse/inventory management system with Telegram Bot interface and REST API backend.

## 🏗️ Project Structure

```
warehousing/
├── bot/                    # Telegram Bot Application
│   ├── bot.py             # Main bot file
│   ├── messages.py        # Persian UI messages
│   ├── handlers_*.py      # Command handlers
│   └── README.md
│
├── database/              # Database Layer
│   ├── database.py        # SQLite operations
│   ├── utils.py           # Utility functions
│   ├── migrate.py         # Database migration script
│   ├── warehouse.db       # SQLite database (created at runtime)
│   ├── images/            # Item images storage
│   └── README.md
│
├── api/                   # REST API Backend
│   ├── main.py            # FastAPI application
│   ├── requirements.txt   # API dependencies
│   └── README.md
│
├── webApp/                # Web Application (Future)
│   └── README.md
│
├── deployment/            # Deployment Scripts & Guides
│   ├── backup_db.sh       # Database backup script
│   ├── check_status.sh    # Bot status checker
│   ├── keep_alive.sh      # Keep bot running
│   ├── passenger_wsgi.py  # cPanel WSGI wrapper
│   ├── DEPLOYMENT.md      # Deployment guide
│   ├── BACKUP_GUIDE.md    # Backup setup guide
│   ├── AUTH_UPDATE.md     # Auth update guide
│   └── UPDATE_BOT_HOST.md # Host update guide
│
├── docs/                  # Documentation
│   ├── ARCHITECTURE.md    # System architecture
│   ├── MIGRATION_GUIDE.md # Migration guide
│   ├── QUICK_REFERENCE.md # Quick reference
│   └── QUICKSTART.py      # Quick start script
│
├── requirements.txt       # Project dependencies
├── LICENSE                # License file
├── README.md              # This file
├── .env                   # Environment variables (create this)
├── .gitignore             # Git ignore rules
├── start_bot.bat/sh       # Bot launcher scripts
└── start_api.bat/sh       # API launcher scripts
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file in project root:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
BOT_PASSWORD=ciFarco@1213#3221
```

### 3. Run Telegram Bot

**Windows:**
```cmd
start_bot.bat
```

**Linux:**
```bash
chmod +x start_bot.sh
./start_bot.sh
```

### 4. Run API (Optional)

**Windows:**
```cmd
start_api.bat
```

**Linux:**
```bash
chmod +x start_api.sh
./start_api.sh
```

API will be available at: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

## 📦 Features

### Telegram Bot
- ✅ User authentication with password
- ✅ Full CRUD for items, categories, subcategories, brands
- ✅ Item image upload (multiple images per item)
- ✅ Search items (by name, code, description)
- ✅ Filter items by brand or category
- ✅ Low stock alerts
- ✅ Inventory management
- ✅ Persian (Shamsi) date system
- ✅ Inline keyboard navigation

### REST API
- ✅ RESTful endpoints for all entities
- ✅ Search and filtering
- ✅ Pagination support
- ✅ CORS enabled
- ✅ Auto-generated documentation
- ✅ JSON responses
- ✅ Stock update endpoint

### Database
- ✅ SQLite (simple, file-based)
- ✅ Automatic backups
- ✅ Persian date support
- ✅ Relational data (categories, brands, etc.)
- ✅ Image path storage

## 🔧 Module Documentation

Each module has its own README:
- [Bot Documentation](./bot/README.md)
- [Database Documentation](./database/README.md)
- [API Documentation](./api/README.md)
- [WebApp Documentation](./webApp/README.md)

## 📚 Additional Documentation

- [Architecture Diagrams](./docs/ARCHITECTURE.md)
- [Migration Guide](./docs/MIGRATION_GUIDE.md)
- [Quick Reference](./docs/QUICK_REFERENCE.md)
- [Deployment Guide](./deployment/DEPLOYMENT.md)
- [Backup Setup](./deployment/BACKUP_GUIDE.md)

## 📊 Database Schema

```
categories
  ├── subcategories
  │     └── items
  │           ├── item_images
  │           └── brands
  │           └── measure_types

user_states (for bot conversation flow)
authenticated_users (for bot access control)
```

## 🌐 API Endpoints

### Items
- `GET /api/items` - List all items
- `GET /api/items/search?q={query}` - Search items
- `GET /api/items/{id}` - Get item details
- `PATCH /api/items/{id}/stock` - Update stock

### Categories
- `GET /api/categories` - List categories
- `GET /api/categories/{id}/subcategories` - Get subcategories

### Brands
- `GET /api/brands` - List brands
- `GET /api/brands/{id}/items` - Get brand items

### Statistics
- `GET /api/stats` - Warehouse statistics
- `GET /api/low-stock` - Low stock items

Full API documentation: `http://localhost:8000/docs`

## 🛠️ Tech Stack

- **Bot Framework**: python-telegram-bot (v22+)
- **API Framework**: FastAPI
- **Database**: SQLite3
- **Date System**: jdatetime (Persian dates)
- **Image Processing**: Pillow
- **Server**: Uvicorn (ASGI)

## 📁 Data Files

- `database/warehouse.db` - Main database file
- `database/images/` - Uploaded item images
- `backups/` - Daily database backups (auto-generated)
- `.env` - Configuration (create manually)

## 🔐 Authentication

### Telegram Bot
- Password-based authentication
- Default password: `ciFarco@1213#3221`
- Set via `BOT_PASSWORD` in `.env`

### API
- Currently open (no auth)
- Add JWT/API keys in production

## 🚢 Deployment

### cPanel Hosting

See [deployment/DEPLOYMENT.md](./deployment/DEPLOYMENT.md) for detailed cPanel setup instructions.

Quick summary:
1. Upload project to cPanel
2. Setup Python App for bot
3. Setup separate Python App for API (optional)
4. Configure environment variables
5. Setup cron job for keep-alive and backups

### Local Development

1. Clone repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create `.env` file with bot token
4. Run bot: `python bot/bot.py`
5. Run API: `uvicorn api.main:app --reload`

## 🗓️ Backup System

Automatic daily backups are configured via `deployment/backup_db.sh`:
- Keeps last 7 days of backups
- Stored in `/backups/` directory (auto-generated)
- Setup via cron job on cPanel

See [deployment/BACKUP_GUIDE.md](./deployment/BACKUP_GUIDE.md) for setup instructions.

## 📝 License

This project is private and proprietary.

## 👥 Support

For issues or questions, contact the development team.

## 🎯 Roadmap

- [x] Telegram Bot with full CRUD
- [x] REST API backend
- [x] Search and filtering
- [x] Low stock alerts
- [ ] Web application UI (Angular/React)
- [ ] Advanced reporting
- [ ] Export to Excel
- [ ] Barcode/QR code support
- [ ] Multi-user roles
- [ ] API authentication

---

**Version**: 1.0.0  
**Last Updated**: November 2025  
**Status**: ✅ Production Ready (Bot + API)
