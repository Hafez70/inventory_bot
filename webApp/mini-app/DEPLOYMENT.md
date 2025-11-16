# Mini App Deployment Guide

## 🚀 Development

### Install Dependencies
```bash
cd webApp/mini-app
npm install
```

### Start Development Server
```bash
npm start
# or
nx serve mini-app
```

App will be available at `http://localhost:4200`

---

## 📦 Build for Production

```bash
npm run build
# or
nx build mini-app --configuration=production
```

Build output will be in `dist/apps/mini-app`

---

## 🌐 Deployment

### Option 1: Deploy to cPanel with API

1. **Build the app:**
```bash
nx build mini-app --configuration=production
```

2. **Upload files:**
- Upload contents of `dist/apps/mini-app` to `public_html/mini-app/` on your cPanel

3. **Configure API endpoint:**
- The app expects the API at `/api` (relative path)
- Make sure your FastAPI is accessible at `https://yourdomain.com/api`

4. **Set up Telegram Bot WebApp:**
- In BotFather, use `/setmenubutton`
- Set the URL to: `https://yourdomain.com/mini-app`

---

### Option 2: Deploy as Telegram Web App

1. **Build the app with base href:**
```bash
nx build mini-app --base-href /mini-app/
```

2. **Configure Telegram Bot:**
```python
# In your bot code
from telegram import MenuButtonWebApp, WebAppInfo

await bot.set_chat_menu_button(
    menu_button=MenuButtonWebApp(
        text="📱 وب اپ",
        web_app=WebAppInfo(url="https://yourdomain.com/mini-app")
    )
)
```

---

## 🔧 Environment Configuration

Create `apps/mini-app/src/environments/environment.prod.ts`:

```typescript
export const environment = {
  production: true,
  apiUrl: 'https://api.bazardaghigh.ir',
};
```

Then modify `api.config.ts` to use environment:

```typescript
import { environment } from '../../../environments/environment';

export const DEFAULT_API_CONFIG: ApiConfig = {
  baseUrl: environment.apiUrl || '/api',
};
```

---

## 📱 Testing in Telegram

1. **Local Development:**
   - Use ngrok or similar to expose localhost
   - Set webhook URL in BotFather

2. **Production:**
   - Deploy to your domain
   - Configure menu button in BotFather

---

## 🛠️ NX Commands

```bash
# Serve app
nx serve mini-app

# Build app
nx build mini-app

# Test all
nx test

# Lint all
nx lint

# Build specific library
nx build search

# Run tests for specific library
nx test shared-ui-layout

# Visualize project dependencies
nx graph
```

---

## 📚 Project Structure

```
webApp/mini-app/
├── apps/
│   └── mini-app/              # Main application
│       ├── src/
│       │   ├── app/           # App component & routing
│       │   └── pages/         # Page components
│       └── project.json       # App configuration
├── libs/
│   ├── shared/
│   │   ├── ui-layout/         # Layout components
│   │   └── data-access/       # API services
│   └── search/                # Search feature library
├── nx.json                    # NX workspace config
├── package.json              # Dependencies
└── tailwind.config.js        # Tailwind CSS config
```

---

## 🔐 Authentication with Telegram

The app automatically includes Telegram Web App init data in API requests via the `apiInterceptor`.

In your FastAPI backend, validate the init data:

```python
from telegram import WebAppData
from hashlib import sha256
import hmac

def validate_telegram_init_data(init_data: str, bot_token: str) -> bool:
    # Implement Telegram Web App data validation
    # See: https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
    pass
```

---

## 🎨 Customization

### Colors
Edit `tailwind.config.js` to change the primary color palette.

### RTL Support
The app is already configured for RTL (Right-to-Left) layout. See `index.html` and component styles.

### Telegram Theme
The app uses Telegram's theme variables (`--tg-theme-*`). These are automatically applied.

---

## 🐛 Troubleshooting

### Build Errors
- Make sure all dependencies are installed: `npm install`
- Clear NX cache: `nx reset`

### API Connection Issues
- Check CORS configuration in FastAPI
- Verify API base URL in `api.config.ts`
- Check browser console for errors

### Telegram Web App Issues
- Ensure you're testing in Telegram app (not browser)
- Check that the URL is HTTPS (required by Telegram)
- Verify bot token and init data validation

