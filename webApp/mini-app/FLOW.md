# 🎯 Complete Flow: How Everything Works Together

## 📊 High-Level Architecture

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│   Telegram   │◄─────►│  Mini App    │◄─────►│   FastAPI    │
│     Bot      │       │  (Angular)   │       │   Backend    │
└──────────────┘       └──────────────┘       └──────────────┘
       │                       │                       │
       │                       │                       │
       ▼                       ▼                       ▼
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│    User      │       │  Web Server  │       │   Database   │
│  (Telegram)  │       │   (cPanel)   │       │   (SQLite)   │
└──────────────┘       └──────────────┘       └──────────────┘
```

---

## 🚀 Flow 1: User Opens Mini App from Telegram

```
USER                    TELEGRAM              MINI APP              API

  │                        │                      │                   │
  │  Click Bot Menu       │                      │                   │
  ├───────────────────────>│                      │                   │
  │                        │                      │                   │
  │                        │  Open Mini App URL  │                   │
  │                        ├─────────────────────>│                   │
  │                        │                      │                   │
  │                        │  Pass initData      │                   │
  │                        │  (user info, hash)  │                   │
  │                        ├─────────────────────>│                   │
  │                        │                      │                   │
  │                        │                      │  Load Angular App │
  │                        │                      │                   │
  │                        │                      │  Show Home Page   │
  │<───────────────────────┴──────────────────────┤                   │
  │         Mini App Displayed in Telegram        │                   │
  │                                                │                   │
```

**What happens:**
1. User opens your bot in Telegram
2. User clicks menu button "📱 وب اپ"
3. Telegram opens mini app in embedded browser
4. Telegram passes user authentication data (`initData`)
5. Angular app loads with layout and home page
6. User sees the app inside Telegram

---

## 🔍 Flow 2: User Searches for Items

```
USER                    MINI APP              API                DATABASE

  │                        │                      │                   │
  │  Click Search Tab     │                      │                   │
  ├───────────────────────>│                      │                   │
  │                        │                      │                   │
  │                        │  Navigate to /search │                   │
  │                        │                      │                   │
  │  Type "کالا"          │                      │                   │
  ├───────────────────────>│                      │                   │
  │                        │                      │                   │
  │                        │  Wait 500ms (debounce)                  │
  │                        │                      │                   │
  │                        │  GET /api/items/search?q=کالا           │
  │                        │  + Telegram initData │                   │
  │                        ├─────────────────────>│                   │
  │                        │                      │                   │
  │                        │                      │  Validate initData│
  │                        │                      │                   │
  │                        │                      │  Query Database   │
  │                        │                      ├──────────────────>│
  │                        │                      │                   │
  │                        │                      │  Return Results   │
  │                        │                      │<──────────────────┤
  │                        │                      │                   │
  │                        │  { items: [...] }    │                   │
  │                        │<─────────────────────┤                   │
  │                        │                      │                   │
  │  Display Item Cards   │                      │                   │
  │<───────────────────────┤                      │                   │
  │                        │                      │                   │
```

**What happens:**
1. User types in search box
2. Angular waits 500ms (debounce) to avoid too many requests
3. SearchService calls API with query
4. HTTP Interceptor adds Telegram `initData` to headers
5. FastAPI validates user is authenticated
6. FastAPI queries SQLite database
7. Results sent back to Angular
8. Angular displays item cards with stock info

---

## 🔐 Flow 3: Authentication & Security

```
TELEGRAM               MINI APP              API              DATABASE

    │                     │                     │                  │
    │  initData:          │                     │                  │
    │  user_id=123        │                     │                  │
    │  hash=abc123...     │                     │                  │
    ├────────────────────>│                     │                  │
    │                     │                     │                  │
    │                     │  Every HTTP Request │                  │
    │                     │  Header: X-Telegram-Init-Data          │
    │                     ├────────────────────>│                  │
    │                     │                     │                  │
    │                     │                     │  Validate Hash   │
    │                     │                     │  using Bot Token │
    │                     │                     │                  │
    │                     │                     │  Check User ID   │
    │                     │                     │  in Database     │
    │                     │                     ├─────────────────>│
    │                     │                     │                  │
    │                     │                     │  User exists?    │
    │                     │                     │<─────────────────┤
    │                     │                     │                  │
    │                     │  ✅ or ❌          │                  │
    │                     │<────────────────────┤                  │
    │                     │                     │                  │
```

**What happens:**
1. Telegram provides signed user data (`initData`)
2. Angular stores this in memory
3. HTTP Interceptor adds it to every API request
4. FastAPI validates the signature using bot token
5. FastAPI checks if user is in `authenticated_users` table
6. If valid → process request
7. If invalid → return 401 Unauthorized

---

## 🏗️ Flow 4: Project Structure & Components

```
┌─────────────────────────────────────────────────────────────┐
│                        MINI APP                             │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │              App Component                           │  │
│  │                                                       │  │
│  │  ┌─────────────────────────────────────────────┐   │  │
│  │  │         Layout Component                     │   │  │
│  │  │                                               │   │  │
│  │  │  ┌─────────────────────────────────────┐   │   │  │
│  │  │  │     Main Content (Router Outlet)    │   │   │  │
│  │  │  │                                      │   │   │  │
│  │  │  │  ┌──────────┐   ┌──────────────┐  │   │   │  │
│  │  │  │  │   Home   │   │    Search     │  │   │   │  │
│  │  │  │  │   Page   │   │     Page      │  │   │   │  │
│  │  │  │  └──────────┘   └──────────────┘  │   │   │  │
│  │  │  │                                      │   │   │  │
│  │  │  │  Search Page Components:            │   │   │  │
│  │  │  │  ┌────────────────────────────┐   │   │   │  │
│  │  │  │  │  SearchContainerComponent  │   │   │   │  │
│  │  │  │  │  ┌──────────────────────┐ │   │   │   │  │
│  │  │  │  │  │ SearchInputComponent │ │   │   │   │  │
│  │  │  │  │  └──────────────────────┘ │   │   │   │  │
│  │  │  │  │  ┌──────────────────────┐ │   │   │   │  │
│  │  │  │  │  │SearchResultsComponent│ │   │   │   │  │
│  │  │  │  │  │  ┌────────────────┐ │ │   │   │   │  │
│  │  │  │  │  │  │ ItemCardComponent│ │   │   │   │  │
│  │  │  │  │  │  └────────────────┘ │ │   │   │   │  │
│  │  │  │  │  └──────────────────────┘ │   │   │   │  │
│  │  │  │  └────────────────────────────┘   │   │   │  │
│  │  │  └─────────────────────────────────────┘   │   │  │
│  │  │                                               │   │  │
│  │  │  ┌─────────────────────────────────────┐   │   │  │
│  │  │  │    Bottom Navigation Component       │   │   │  │
│  │  │  │    [Home] [Search]                   │   │   │  │
│  │  │  └─────────────────────────────────────┘   │   │  │
│  │  └─────────────────────────────────────────────┘   │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘

                           ▼ HTTP Calls

┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                        │
│                                                             │
│  ┌────────────────┐  ┌────────────────┐  ┌─────────────┐ │
│  │   /items       │  │  /items/search │  │   /health   │ │
│  │   /brands      │  │  /categories   │  │   /images   │ │
│  └────────────────┘  └────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘

                           ▼ SQL Queries

┌─────────────────────────────────────────────────────────────┐
│                      SQLite Database                        │
│                                                             │
│  [items] [brands] [categories] [authenticated_users] ...   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Flow 5: File Organization & Data Flow

```
Component Interaction Flow:

┌──────────────────────────────────────────────────────────┐
│                  Search Container                        │
│                  (Smart Component)                       │
│                                                          │
│  ┌────────────────────────────────────────────┐        │
│  │ State (Signals):                            │        │
│  │ - searchQuery = signal('')                 │        │
│  │ - searchResults = signal([])               │        │
│  │ - isLoading = signal(false)                │        │
│  └────────────────────────────────────────────┘        │
│                          │                              │
│                          ▼                              │
│  ┌────────────────────────────────────────────┐        │
│  │ Inject Services:                            │        │
│  │ - SearchService                             │        │
│  └────────────────────────────────────────────┘        │
│                          │                              │
│         ┌────────────────┴────────────────┐            │
│         ▼                                  ▼            │
│  ┌──────────────┐                  ┌──────────────┐   │
│  │ SearchInput  │                  │SearchResults │   │
│  │ (Dumb)       │                  │ (Dumb)       │   │
│  │              │                  │              │   │
│  │ input:       │                  │ input:       │   │
│  │ searchQuery  │                  │ items[]      │   │
│  │              │                  │ hasSearched  │   │
│  │ output:      │                  │              │   │
│  │ queryChange  │                  │   │          │   │
│  │ search       │                  │   ▼          │   │
│  └──────────────┘                  │ ┌─────────┐ │   │
│                                     │ │ItemCard │ │   │
│                                     │ │ (Dumb)  │ │   │
│                                     │ └─────────┘ │   │
│                                     └──────────────┘   │
└──────────────────────────────────────────────────────────┘

Service → API → Database Flow:

┌──────────────────┐
│ SearchService    │
│ (data-access)    │
└────────┬─────────┘
         │
         │ inject(ApiService)
         │
         ▼
┌──────────────────┐
│   ApiService     │
│ (shared/data-    │
│  access)         │
└────────┬─────────┘
         │
         │ HttpClient.get()
         │ + Interceptor adds Telegram data
         │
         ▼
┌──────────────────┐
│   FastAPI        │
│   /api/items/    │
│   search         │
└────────┬─────────┘
         │
         │ SQL Query
         │
         ▼
┌──────────────────┐
│ SQLite Database  │
│ warehouse.db     │
└──────────────────┘
```

---

## 🎬 Flow 6: Complete User Journey

```
1. USER OPENS TELEGRAM
   │
   ▼
2. USER OPENS BOT (@your_bot)
   │
   ▼
3. USER SEES MENU BUTTON "📱 وب اپ"
   │
   ▼
4. USER CLICKS MENU BUTTON
   │
   ▼
5. TELEGRAM OPENS MINI APP
   - URL: https://yourdomain.com/mini-app
   - Embedded browser inside Telegram
   - Passes user authentication data
   │
   ▼
6. ANGULAR APP LOADS
   - Shows loading spinner (brief)
   - Initializes routing
   - Sets up layout
   │
   ▼
7. HOME PAGE DISPLAYS
   - Welcome message
   - Dashboard placeholder
   - Bottom navigation visible
   │
   ▼
8. USER CLICKS "SEARCH" TAB
   - Router navigates to /search
   - SearchContainerComponent loads
   │
   ▼
9. SEARCH PAGE DISPLAYS
   - Title: "جستجوی کالا"
   - Search input box
   - Empty state message
   │
   ▼
10. USER TYPES "کالا"
    - Input updates searchQuery signal
    - Effect triggers after 500ms
    │
    ▼
11. SEARCH EXECUTES
    - SearchService.searchItems('کالا')
    - HTTP GET /api/items/search?q=کالا
    - Interceptor adds X-Telegram-Init-Data header
    │
    ▼
12. API PROCESSES
    - Validates Telegram data
    - Checks user authentication
    - Queries database
    │
    ▼
13. RESULTS RETURN
    - JSON: { items: [...], total: 5 }
    - Angular receives data
    │
    ▼
14. RESULTS DISPLAY
    - Item cards appear
    - Each card shows:
      * Image or placeholder
      * Item name
      * Custom code badge
      * Brand badge
      * Description
      * Stock status
    │
    ▼
15. USER CLICKS ITEM (future feature)
    - Navigate to item details
    - Or send data back to bot
```

---

## 💻 Flow 7: Development to Production

```
LOCAL DEVELOPMENT:

1. Developer Machine (Windows)
   ├─ Angular Dev Server (localhost:4200)
   ├─ FastAPI Dev Server (localhost:8001)
   └─ ngrok → HTTPS tunnel
      └─ Public URL → Telegram

TESTING:

2. ngrok Exposes Local App
   ├─ ngrok http 4200
   ├─ Gets URL: https://abc123.ngrok.io
   └─ Configure in BotFather
      └─ Users can test in Telegram

PRODUCTION:

3. Build & Deploy
   ├─ npm run build
   ├─ Upload to cPanel/public_html/mini-app/
   ├─ FastAPI running via Passenger
   └─ Configure permanent URL in BotFather
      └─ https://yourdomain.com/mini-app

File Flow:
┌───────────────┐    build     ┌───────────────┐
│ Source Code   │ ───────────> │ dist/         │
│ TypeScript    │              │ JavaScript    │
│ SCSS          │              │ CSS           │
│ Components    │              │ Bundles       │
└───────────────┘              └───────────────┘
                                       │
                                       │ upload
                                       ▼
                               ┌───────────────┐
                               │ cPanel        │
                               │ public_html/  │
                               │ mini-app/     │
                               └───────────────┘
```

---

## 🔧 Flow 8: Request Lifecycle

```
1. User Action (Click, Type, etc.)
   │
   ▼
2. Component Event Handler
   │
   ▼
3. Signal Update
   signal.set(newValue)
   │
   ▼
4. Effect Triggers (if watching signal)
   │
   ▼
5. Service Method Called
   searchService.searchItems(query)
   │
   ▼
6. HTTP Request Created
   HttpClient.get('/api/items/search?q=...')
   │
   ▼
7. HTTP Interceptor Runs
   Adds Telegram initData header
   │
   ▼
8. Request Sent to API
   GET https://api.yourdomain.com/...
   │
   ▼
9. FastAPI Receives Request
   - Validates headers
   - Authenticates user
   │
   ▼
10. Database Query
    - SQLite query executed
    - Results fetched
    │
    ▼
11. Response Sent Back
    JSON: { items: [...] }
    │
    ▼
12. Observable Emits
    Service returns Observable<Item[]>
    │
    ▼
13. Component Subscribes
    .subscribe({ next: (items) => ... })
    │
    ▼
14. Signal Updates
    searchResults.set(items)
    │
    ▼
15. Template Updates
    Angular Change Detection
    │
    ▼
16. UI Re-renders
    User sees results
```

---

## 📚 Summary

**Key Points:**

1. **Mini app runs inside Telegram** - Not a separate app
2. **Telegram provides authentication** - via initData
3. **Angular communicates with FastAPI** - via HTTP
4. **FastAPI queries SQLite** - your existing database
5. **Everything is connected** - Bot + Mini App + API + Database

**Next Steps:**

1. Read `QUICKSTART.md` - How to run locally
2. Run `setup.bat` - Setup development environment  
3. Test with `npm start` - See it in browser
4. Use ngrok - Test in Telegram
5. Deploy to cPanel - Go live!

---

For detailed instructions, see:
- `QUICKSTART.md` - Running the app
- `TELEGRAM_INTEGRATION.md` - Telegram bot integration
- `ARCHITECTURE.md` - Code structure
- `DEPLOYMENT.md` - Production deployment

