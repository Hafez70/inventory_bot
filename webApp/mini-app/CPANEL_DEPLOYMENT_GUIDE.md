# 🚀 Deploy Angular Mini-App to cPanel (Root Domain)

This guide explains how to deploy the Angular mini-app to **https://bazardaghigh.ir** (root domain).

---

## ⚠️ IMPORTANT: Root Domain Deployment

Since your website currently shows a directory listing at https://bazardaghigh.ir, we need to:
1. Replace the directory listing with your Angular app
2. Keep the API accessible at `/api`
3. Keep other folders accessible if needed

---

## 📋 Prerequisites

- ✅ cPanel access
- ✅ Node.js/npm installed locally
- ✅ Git access to your repository
- ✅ API running at `https://bazardaghigh.ir/api`

---

## 🏗️ Step 1: Build the Production App

On your **local machine** (Windows), run:

```bash
cd D:\projects\ci-farco\warehousing\webApp\mini-app
npm run build
```

This will create a production build in `dist/apps/mini-app/browser/`

---

## 📁 Step 2: Deploy to cPanel Root

### ⚠️ BACKUP FIRST!

Before deploying, backup your current `public_html`:

**On cPanel Terminal:**
```bash
cd ~
tar -czf public_html_backup_$(date +%Y%m%d).tar.gz public_html/
```

---

### Option A: Via cPanel File Manager (Recommended)

1. **Login to cPanel → File Manager**
2. **Navigate to:** `public_html/`
3. **Delete or rename:** `index.html` (if it exists)
4. **Upload all files from:** `dist/apps/mini-app/browser/`
   - Upload `index.html`
   - Upload all `.js` files
   - Upload all `.css` files
   - Upload `3rdpartylicenses.txt`
   - **DO NOT delete:** `api/`, `cgi-bin/`, or other existing folders

---

### Option B: Via cPanel Terminal

**On cPanel Terminal:**

```bash
# Go to your app directory
cd ~/app/webApp/mini-app

# Make sure it's up to date
git pull origin main

# Build on server (if Node.js is available)
npm install
npm run build

# Copy to public_html root
cd ~/public_html
cp ~/app/webApp/mini-app/dist/apps/mini-app/browser/* .

# Make sure API folder is NOT overwritten
ls -la
```

---

### Option C: Upload from Local (Manual)

1. **Build locally** (see Step 1)
2. **Download all files from:** `dist\apps\mini-app\browser\`
3. **In cPanel File Manager:**
   - Go to `public_html/`
   - Upload all files to **root** (not in a subfolder)
   - Keep existing folders (`api/`, `cgi-bin/`, etc.)

---

## 📂 Final Directory Structure

Your `public_html/` should look like:

```
~/public_html/
├── index.html              # Angular app entry point (NEW)
├── main-XXXXXX.js          # Angular main bundle (NEW)
├── polyfills-XXXXXX.js     # Angular polyfills (NEW)
├── styles-XXXXXX.css       # Angular styles (NEW)
├── 3rdpartylicenses.txt    # Licenses (NEW)
├── api/                    # Keep - API directory (existing)
├── cgi-bin/                # Keep - CGI scripts (existing)
└── .htaccess               # Create - for routing (NEW)
```

---

## ⚙️ Step 3: Configure Routing

Create `.htaccess` in `~/public_html/` for Angular routing:

**On cPanel Terminal:**

```bash
cd ~/public_html
cat > .htaccess << 'EOF'
<IfModule mod_rewrite.c>
  RewriteEngine On
  
  # Don't rewrite files or directories
  RewriteCond %{REQUEST_FILENAME} -f [OR]
  RewriteCond %{REQUEST_FILENAME} -d
  RewriteRule ^ - [L]
  
  # Don't rewrite /api requests (keep API accessible)
  RewriteCond %{REQUEST_URI} !^/api
  
  # Don't rewrite /cgi-bin requests
  RewriteCond %{REQUEST_URI} !^/cgi-bin
  
  # Rewrite everything else to index.html
  RewriteRule ^ index.html [L]
</IfModule>
EOF
```

This ensures:
- ✅ Angular routing works (no 404 on refresh)
- ✅ API remains accessible at `/api`
- ✅ Other folders remain accessible

---

## 🌐 Step 4: Test the Deployment

### Test the App:
Visit: **https://bazardaghigh.ir/**

You should see your Angular mini-app (not directory listing).

### Test the API:
Visit: **https://bazardaghigh.ir/api/health**

You should see: `{"status":"healthy","database":"connected"}`

### Test Search:
Visit: **https://bazardaghigh.ir/api/items/search?q=test**

You should see search results.

---

## 🔗 Step 5: Integrate with Telegram Bot

In your Telegram bot, use this URL for the mini-app:

```python
# In bot/handlers_item.py or wherever you show the web app button
MINI_APP_URL = "https://bazardaghigh.ir/"

# When showing the button
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

keyboard = [[
    InlineKeyboardButton(
        "🔍 جستجو کالا",
        web_app=WebAppInfo(url=MINI_APP_URL)
    )
]]
reply_markup = InlineKeyboardMarkup(keyboard)
```

---

## 🔧 Troubleshooting

### Problem: Still seeing directory listing

**Solution:** Make sure `index.html` is in the root of `public_html/`

```bash
cd ~/public_html
ls -la index.html
cat index.html | head -5
```

Should show Angular's HTML with `<app-root></app-root>`

---

### Problem: API returns 404

**Solution:** Check if API folder exists and Python App is running

```bash
cd ~/public_html
ls -la api/
ps aux | grep uvicorn
```

---

### Problem: White screen / blank page

**Solution 1:** Check browser console for errors (F12)

**Solution 2:** Verify `base href` in `index.html`:

```bash
cd ~/public_html
cat index.html | grep base
```

Should show: `<base href="/">`

---

### Problem: 404 on page refresh (Angular routes)

**Solution:** Check if `.htaccess` exists and is correct:

```bash
cd ~/public_html
cat .htaccess
```

If missing, create it (see Step 3).

---

### Problem: API calls failing (CORS)

**Solution:** Your API should already have CORS configured in `api/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🔄 Updating the App

Whenever you make changes:

1. **Build locally:**
   ```bash
   cd webApp/mini-app
   npm run build
   ```

2. **Upload new files to cPanel** (overwrite existing `index.html`, `*.js`, `*.css`)

3. **Clear browser cache** or use Ctrl+Shift+R

---

## 🎯 Quick Deploy Commands

### Local (Windows):
```bash
cd D:\projects\ci-farco\warehousing\webApp\mini-app
.\deploy.bat
```

### cPanel (copy built files):
```bash
cd ~/public_html
rm -f index.html main-*.js polyfills-*.js styles-*.css
cp ~/app/webApp/mini-app/dist/apps/mini-app/browser/* .
```

---

## 🎉 Done!

Your Angular mini-app should now be live at:
- **🌐 https://bazardaghigh.ir/** (root domain)

And your API is still accessible at:
- **🔗 https://bazardaghigh.ir/api/**

Both accessible from your Telegram bot! 🤖✨

---

## 📝 Important Notes

1. ⚠️ **Don't delete** the `api/` folder in `public_html/`
2. ⚠️ **Don't delete** the `cgi-bin/` folder
3. ✅ **Always backup** before deploying
4. ✅ The `.htaccess` file ensures Angular routing works without breaking API access
5. ✅ Your bot's database and API are in `~/app/`, completely separate from `public_html/`

---

## 🔗 URLs Summary

| Service | URL | Location |
|---------|-----|----------|
| **Mini-App (Frontend)** | https://bazardaghigh.ir/ | `~/public_html/` |
| **API (Backend)** | https://bazardaghigh.ir/api/ | `~/app/` (via Python App) |
| **Bot** | Telegram | `~/app/bot/` |
| **Database** | - | `~/app/database/warehouse.db` |
