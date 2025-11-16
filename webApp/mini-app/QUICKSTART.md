# 🚀 Quick Start Guide - Telegram Mini App

## 📋 Prerequisites

- Node.js 18+ installed
- npm installed
- A Telegram Bot (with BotFather)
- Your FastAPI backend running

---

## 🏃 Step 1: Local Development

### 1.1 Install Dependencies

```bash
cd webApp/mini-app
npm install
```

This will install all required packages (Angular, NX, Tailwind, etc.)

### 1.2 Start Development Server

```bash
npm start
```

The app will run at: `http://localhost:4200`

You can now open your browser and test the app locally!

---

## 🔗 Step 2: Connect to Your API

The app is already configured to connect to your FastAPI backend.

### For Local Testing:

The app will connect to `http://localhost:8001` (defined in `environment.ts`)

**Make sure your FastAPI is running:**
```bash
# In your main project directory
cd ~/app
source ~/virtualenv/app/3.11/bin/activate
python -m uvicorn api.main:app --host 0.0.0.0 --port 8001
```

---

## 📱 Step 3: Test in Telegram (Development)

### Option A: Using ngrok (Recommended for testing)

1. **Install ngrok** (if not already): https://ngrok.com/download

2. **Start ngrok:**
```bash
ngrok http 4200
```

You'll get a URL like: `https://abc123.ngrok.io`

3. **Configure Telegram Bot:**

Open Telegram, find [@BotFather](https://t.me/BotFather):

```
/setmenubutton
@your_bot_username
Button text: 📱 وب اپ
URL: https://abc123.ngrok.io
```

4. **Test:** Open your bot in Telegram and click the menu button!

### Option B: Using Telegram Test Environment

1. Install Telegram Desktop
2. Open Developer Tools (Ctrl+Shift+F12)
3. Test Web Apps locally

---

## 🌐 Step 4: Production Deployment

### 4.1 Build for Production

```bash
npm run build
```

Output will be in: `dist/apps/mini-app/`

### 4.2 Upload to cPanel

1. **Build the app:**
```bash
cd webApp/mini-app
npm run build
```

2. **Upload to cPanel:**
   - Go to cPanel File Manager
   - Navigate to `public_html/`
   - Create folder: `mini-app/`
   - Upload all files from `dist/apps/mini-app/` to `public_html/mini-app/`

3. **Configure API endpoint:**

Your app will automatically connect to `/api` (same domain)

Make sure your FastAPI is accessible at: `https://yourdomain.com/api`

### 4.3 Configure Telegram Bot

In [@BotFather](https://t.me/BotFather):

```
/setmenubutton
@your_bot_username
Button text: 📱 وب اپ
URL: https://yourdomain.com/mini-app
```

---

## 🎯 Complete Flow Diagram

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│  USER OPENS TELEGRAM BOT                           │
│                                                     │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│                                                     │
│  CLICKS "وب اپ" BUTTON IN BOT MENU                 │
│                                                     │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│                                                     │
│  TELEGRAM OPENS MINI APP                           │
│  URL: https://yourdomain.com/mini-app              │
│                                                     │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│                                                     │
│  ANGULAR APP LOADS                                 │
│  - Layout with bottom navigation                   │
│  - Home page shown by default                      │
│                                                     │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│                                                     │
│  USER NAVIGATES                                    │
│  - Home (/)                                        │
│  - Search (/search)                                │
│                                                     │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│                                                     │
│  USER SEARCHES FOR ITEMS                           │
│  Angular → API Call → FastAPI Backend             │
│  GET /api/items/search?q=کالا                     │
│                                                     │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│                                                     │
│  RESULTS DISPLAYED                                 │
│  - Item cards with images                          │
│  - Stock information                               │
│  - Click to view details (future)                  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🔐 Authentication Flow

```
Telegram Opens Mini App
         │
         ▼
Telegram.WebApp.initData contains user info
         │
         ▼
Angular HTTP Interceptor adds init data to headers
         │
         ▼
FastAPI validates Telegram data
         │
         ▼
API responds with data
```

---

## 🛠️ Development Workflow

### Daily Development:

```bash
# 1. Start API
cd ~/app
source ~/virtualenv/app/3.11/bin/activate
python -m uvicorn api.main:app --host 0.0.0.0 --port 8001

# 2. In another terminal, start Angular
cd webApp/mini-app
npm start

# 3. Open browser: http://localhost:4200
```

### Testing in Telegram:

```bash
# 1. Start ngrok
ngrok http 4200

# 2. Update bot menu button with ngrok URL
# 3. Open bot in Telegram and test
```

---

## 📦 Project Structure Reference

```
webApp/mini-app/
├── apps/mini-app/
│   └── src/
│       ├── app/
│       │   ├── app.component.ts      # Root component
│       │   ├── app.routes.ts         # Routing config
│       │   └── pages/                # Page components
│       │       ├── home/
│       │       └── search/
│       └── environments/
│           ├── environment.ts        # Dev config (localhost:8001)
│           └── environment.prod.ts   # Prod config (/api)
│
├── libs/
│   ├── search/                       # Search feature library
│   │   ├── ui/                       # Components
│   │   ├── data-access/              # Services
│   │   └── domain/                   # Models
│   └── shared/
│       ├── ui-layout/                # Layout components
│       └── data-access/              # API services
│
├── package.json                      # Dependencies
├── nx.json                          # NX config
└── tailwind.config.js               # Tailwind config
```

---

## 🐛 Troubleshooting

### App doesn't load in browser?

```bash
# Check if dependencies are installed
npm install

# Try clearing cache
rm -rf node_modules .angular dist
npm install
npm start
```

### Can't connect to API?

1. Check API is running: `curl http://localhost:8001/health`
2. Check CORS is enabled in FastAPI
3. Check `environment.ts` has correct API URL

### Telegram shows "Mini App Failed to Load"?

1. Check URL is HTTPS (required by Telegram)
2. Check URL is accessible from internet
3. Check no errors in browser console
4. Try opening URL in regular browser first

### ngrok URL changes every time?

- Free ngrok URLs change on restart
- Use paid ngrok for permanent URLs
- Or deploy to production server

---

## ✅ Checklist Before Production

- [ ] Build completes without errors
- [ ] All components work in local browser
- [ ] API connection works
- [ ] Search functionality works
- [ ] Bottom navigation works
- [ ] App works in Telegram (via ngrok)
- [ ] Telegram init data is being sent
- [ ] API validates Telegram data
- [ ] HTTPS is configured
- [ ] Bot menu button is configured

---

## 🎯 Common Commands

```bash
# Development
npm start                    # Start dev server
npm run build                # Build for production
npm test                     # Run tests
npm run lint                 # Lint code

# NX Commands
nx serve mini-app            # Serve app
nx build mini-app            # Build app
nx graph                     # View dependencies
```

---

## 📚 Next Steps

1. **Test locally** - Make sure everything works in browser
2. **Test with ngrok** - Make sure it works in Telegram
3. **Deploy to production** - Upload to cPanel
4. **Configure bot** - Set menu button in BotFather
5. **Test production** - Make sure it works live

---

## 🆘 Need Help?

- Check `ARCHITECTURE.md` for code structure
- Check `DEPLOYMENT.md` for deployment details
- Check `README.detailed.md` for comprehensive docs
- Open an issue on GitHub

---

## 🎉 You're Ready!

Start with local development, test with ngrok, then deploy to production!

