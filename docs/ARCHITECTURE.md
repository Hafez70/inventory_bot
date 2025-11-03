# Project Architecture Diagram

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     WAREHOUSE MANAGEMENT SYSTEM                      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────┐         ┌─────────────────────┐
│   TELEGRAM BOT      │         │     FASTAPI         │
│    (bot/)           │         │     (api/)          │
│                     │         │                     │
│  ┌───────────────┐  │         │  ┌───────────────┐  │
│  │   bot.py      │  │         │  │   main.py     │  │
│  │   handlers    │  │         │  │   endpoints   │  │
│  │   messages    │  │         │  │   models      │  │
│  └───────────────┘  │         │  └───────────────┘  │
│         │            │         │         │           │
│         ▼            │         │         ▼           │
└─────────────────────┘         └─────────────────────┘
          │                               │
          │                               │
          └───────────┬───────────────────┘
                      │
                      ▼
          ┌───────────────────────┐
          │  DATABASE MODULE       │
          │    (database/)         │
          │                        │
          │  ┌──────────────────┐  │
          │  │  database.py     │  │
          │  │  (SQLite CRUD)   │  │
          │  └──────────────────┘  │
          │          │              │
          │          ▼              │
          │  ┌──────────────────┐  │
          │  │  warehouse.db    │  │
          │  │  (SQLite File)   │  │
          │  └──────────────────┘  │
          │                        │
          │  ┌──────────────────┐  │
          │  │    utils.py      │  │
          │  │  (Date, Codes)   │  │
          │  └──────────────────┘  │
          └───────────────────────┘
                      ▲
                      │
          ┌───────────────────────┐
          │  WEB APP (Future)      │
          │    (webApp/)           │
          │                        │
          │  Angular/React/Vue     │
          │         ▼              │
          │  Consumes API via HTTP │
          └───────────────────────┘
```

---

## 🔄 Data Flow

### Telegram Bot Flow:
```
User ──Telegram──> Bot ──Python──> Database ──SQLite──> warehouse.db
                    │                   ▲
                    └─── Handlers ──────┘
```

### API Flow:
```
Web App ──HTTP──> API ──Python──> Database ──SQLite──> warehouse.db
                   │                  ▲
                   └── FastAPI ───────┘
```

---

## 📁 Module Dependencies

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│   Bot    │────>│ Database │<────│   API    │
└──────────┘     └──────────┘     └──────────┘
     │                  │                │
     │                  │                │
     ▼                  ▼                ▼
Messages            SQLite           FastAPI
Handlers            Utils            Endpoints
```

**Legend:**
- `────>` imports/uses
- Each module can work independently
- Database is the shared layer

---

## 🌐 Network Diagram (Production)

```
                    ┌──────────────┐
                    │  Telegram    │
                    │   Server     │
                    └──────┬───────┘
                           │ HTTPS
                           ▼
                    ┌──────────────┐
                    │   cPanel     │
                    │   Server     │
                    │              │
                    │  ┌────────┐  │
                    │  │  Bot   │  │ (Python App)
                    │  │ Process│  │
                    │  └────────┘  │
                    │      │       │
                    │  ┌────────┐  │
                    │  │  API   │  │ (Python App)
                    │  │ Process│  │ Port 8000 or Subdomain
                    │  └────────┘  │
                    │      │       │
                    │  ┌────────┐  │
                    │  │  DB    │  │ warehouse.db
                    │  │  File  │  │
                    │  └────────┘  │
                    └──────────────┘
                           ▲
                           │ HTTPS
                    ┌──────┴───────┐
                    │  Web Browser │
                    │  (Future App)│
                    └──────────────┘
```

---

## 📦 Component Breakdown

### 1. Bot Module (`/bot/`)
```
bot/
├── bot.py                 # Main bot application
├── messages.py            # UI text (Persian)
├── handlers_category.py   # Category CRUD
├── handlers_subcategory.py# Subcategory CRUD
├── handlers_brand.py      # Brand CRUD
├── handlers_measure_type.py # Measure type CRUD
├── handlers_item.py       # Item CRUD + Search
├── handlers_low_stock.py  # Low stock alerts
└── README.md              # Documentation
```

**Responsibilities:**
- User interaction via Telegram
- Message handling
- Inline keyboard navigation
- Image upload
- Persian UI

### 2. Database Module (`/database/`)
```
database/
├── database.py     # SQLite operations
├── utils.py        # Helper functions
├── warehouse.db    # SQLite database file
└── README.md       # Documentation
```

**Responsibilities:**
- Database connection
- CRUD operations
- Data validation
- Code generation
- Date formatting (Shamsi)

### 3. API Module (`/api/`)
```
api/
├── main.py            # FastAPI application
├── requirements.txt   # API dependencies
└── README.md          # Documentation
```

**Responsibilities:**
- HTTP endpoints
- JSON responses
- CORS handling
- Data serialization
- API documentation

### 4. WebApp Module (`/webApp/`)
```
webApp/
└── README.md    # Placeholder
```

**Future Responsibilities:**
- Web UI
- Dashboard
- Reports
- Analytics

---

## 🔐 Authentication Flow

### Bot Authentication:
```
User ──/start──> Bot ──Check User──> Database
                  │                      │
                  │  [Not Authenticated] │
                  ▼                      │
            Request Password             │
                  │                      │
      User ──Password──> Bot ──Verify───┤
                  │                      │
                  │  [Correct]           │
                  ▼                      ▼
            Save to ──authenticated_users
                  │
                  ▼
            Show Main Menu
```

### API Authentication (Future):
```
Web App ──Credentials──> API ──JWT Token──> Database
                          │                      │
                          │  [Valid]            │
                          ▼                      ▼
                    Allow Access ──────────> Return Data
```

---

## 📊 Database Schema

```
┌─────────────┐
│ categories  │
└──────┬──────┘
       │ 1:N
       ▼
┌──────────────┐
│subcategories │
└──────┬───────┘
       │ 1:N
       ▼
┌──────────┐       ┌────────────┐
│  items   │──N:1──│   brands   │
└────┬─────┘       └────────────┘
     │ 1:N
     │             ┌──────────────┐
     │        N:1  │measure_types │
     ├─────────────┴──────────────┘
     │
     │ 1:N
     ▼
┌──────────────┐
│ item_images  │
└──────────────┘

┌──────────────────┐
│  user_states     │ (Bot state management)
└──────────────────┘

┌──────────────────┐
│authenticated_users│ (Bot auth)
└──────────────────┘
```

---

## 🚀 Deployment Architecture

### Option 1: Single Server (Current)
```
cPanel Server
├── Bot Process (background)
├── API Process (Passenger or background)
└── Database File (shared)
```

### Option 2: Separated (Future)
```
Server 1: Bot
Server 2: API + Web App
Database: PostgreSQL/MySQL (networked)
```

---

## 📈 Scalability Path

```
Current State:
SQLite ──> Bot + API (Same Server)

Future State 1:
PostgreSQL ──> Bot (Server 1)
           └──> API (Server 2) ──> Web App

Future State 2:
PostgreSQL Cluster ──> Bot Farm (Load Balanced)
                   └──> API Cluster ──> CDN ──> Web App
```

---

## 🎯 API Endpoint Structure

```
/
├── /api/
│   ├── /items
│   │   ├── GET    /           (list all)
│   │   ├── GET    /search     (search)
│   │   ├── GET    /{id}       (get one)
│   │   └── PATCH  /{id}/stock (update stock)
│   │
│   ├── /categories
│   │   ├── GET  /                        (list all)
│   │   └── GET  /{id}/subcategories      (get subs)
│   │
│   ├── /brands
│   │   ├── GET  /            (list all)
│   │   └── GET  /{id}/items  (get items)
│   │
│   ├── /measure-types
│   │   └── GET  /            (list all)
│   │
│   ├── /low-stock
│   │   └── GET  /            (low stock items)
│   │
│   └── /stats
│       └── GET  /            (statistics)
│
├── /health          (health check)
└── /docs            (API documentation)
```

---

**This architecture provides:**
✅ Modularity
✅ Scalability
✅ Maintainability
✅ Future-proof design
✅ Clear separation of concerns

