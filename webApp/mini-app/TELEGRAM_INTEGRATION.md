# 🔗 Integrating Mini App with Telegram Bot

This guide explains how to integrate the Angular mini app with your Telegram bot.

## 🎯 Overview

The mini app can be accessed from your Telegram bot in two ways:
1. **Menu Button** - Always visible at bottom of chat
2. **Inline Button** - In bot messages

---

## 📱 Method 1: Menu Button (Recommended)

### Using BotFather

1. Open [@BotFather](https://t.me/BotFather) in Telegram

2. Send command:
```
/setmenubutton
```

3. Select your bot: `@your_bot_username`

4. Choose "Edit Menu Button Text"

5. Send button text:
```
📱 وب اپ
```

6. Choose "Edit Menu Button URL"

7. Send URL:
```
https://yourdomain.com/mini-app
```

### Using Python Code

Add this to your bot initialization:

```python
# bot/bot.py
from telegram import MenuButtonWebApp, WebAppInfo

async def setup_menu_button(application):
    """Set up the mini app menu button"""
    await application.bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="📱 وب اپ",
            web_app=WebAppInfo(url="https://yourdomain.com/mini-app")
        )
    )

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    # ... add handlers ...
    
    # Set up menu button
    application.post_init = setup_menu_button
    
    application.run_polling()
```

---

## 📨 Method 2: Inline Button in Messages

### Send Mini App Button in Bot Message

```python
# bot/bot.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message with mini app button"""
    
    keyboard = [
        [
            InlineKeyboardButton(
                "🔍 جستجوی کالا",
                web_app=WebAppInfo(url="https://yourdomain.com/mini-app")
            )
        ],
        [
            InlineKeyboardButton(
                "📦 مدیریت انبار",
                web_app=WebAppInfo(url="https://yourdomain.com/mini-app/search")
            )
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "خوش آمدید! 👋\n\n"
        "برای استفاده از وب اپ، روی دکمه زیر کلیک کنید:",
        reply_markup=reply_markup
    )
```

---

## 🔐 Authentication & Data Exchange

### Receiving User Data from Telegram

The mini app automatically receives user data via `window.Telegram.WebApp.initData`

**What data is included:**
- User ID
- Username
- First/Last name
- Language code
- Auth date
- Hash for verification

### In Angular (Already Implemented)

```typescript
// libs/shared/data-access/src/data-access/api.interceptor.ts
export const apiInterceptor: HttpInterceptorFn = (req, next) => {
  const tgWebApp = window.Telegram?.WebApp;
  
  if (tgWebApp?.initData) {
    req = req.clone({
      setHeaders: {
        'X-Telegram-Init-Data': tgWebApp.initData,
      },
    });
  }
  
  return next(req);
};
```

### In FastAPI (You need to add this)

```python
# api/main.py
from fastapi import FastAPI, Header, HTTPException
import hmac
import hashlib
from urllib.parse import parse_qsl

app = FastAPI()

def validate_telegram_init_data(init_data: str, bot_token: str) -> dict:
    """
    Validate Telegram Web App init data
    Docs: https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
    """
    try:
        # Parse init data
        data_dict = dict(parse_qsl(init_data))
        
        # Extract and remove hash
        received_hash = data_dict.pop('hash', None)
        if not received_hash:
            return None
        
        # Create data check string
        data_check_arr = [f"{k}={v}" for k, v in sorted(data_dict.items())]
        data_check_string = '\n'.join(data_check_arr)
        
        # Calculate hash
        secret_key = hmac.new(
            "WebAppData".encode(),
            bot_token.encode(),
            hashlib.sha256
        ).digest()
        
        calculated_hash = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256
        ).hexdigest()
        
        # Verify hash
        if calculated_hash != received_hash:
            return None
        
        return data_dict
        
    except Exception as e:
        print(f"Error validating init data: {e}")
        return None

@app.get("/api/items/search")
async def search_items(
    q: str,
    x_telegram_init_data: str = Header(None)
):
    """Search items - Protected endpoint"""
    
    # Validate Telegram data
    if x_telegram_init_data:
        user_data = validate_telegram_init_data(
            x_telegram_init_data,
            BOT_TOKEN
        )
        
        if not user_data:
            raise HTTPException(status_code=401, detail="Invalid Telegram data")
        
        user_id = user_data.get('user', {}).get('id')
        # Check if user is authenticated in database
        # ... your authentication logic ...
    
    # Return items
    items = search_items_in_db(q)
    return {"items": items, "total": len(items)}
```

---

## 🎨 Telegram Theme Integration

The mini app automatically adapts to Telegram's theme.

### Available CSS Variables

```css
/* Already used in styles.scss */
:root {
  --tg-theme-bg-color: /* Background color */
  --tg-theme-text-color: /* Text color */
  --tg-theme-hint-color: /* Hint/secondary text */
  --tg-theme-link-color: /* Link color */
  --tg-theme-button-color: /* Button color */
  --tg-theme-button-text-color: /* Button text */
  --tg-theme-secondary-bg-color: /* Secondary background */
}
```

### JavaScript API

```typescript
// Access Telegram WebApp API
const tg = window.Telegram.WebApp;

// Expand to full height
tg.expand();

// Show/hide back button
tg.BackButton.show();
tg.BackButton.onClick(() => {
  // Handle back button
});

// Show confirmation before closing
tg.enableClosingConfirmation();

// Send data back to bot
tg.sendData(JSON.stringify({ action: 'selected_item', item_id: 123 }));

// Close mini app
tg.close();
```

---

## 🔄 Sending Data from Mini App to Bot

### In Angular Component

```typescript
// ui/item-card/item-card.component.ts
handleItemSelect(item: Item): void {
  const tg = (window as any).Telegram?.WebApp;
  
  if (tg) {
    // Send data to bot
    tg.sendData(JSON.stringify({
      action: 'item_selected',
      item_id: item.id,
      item_name: item.name
    }));
    
    // Close mini app
    tg.close();
  }
}
```

### In Bot (Receive Data)

```python
# bot/bot.py
from telegram import Update
from telegram.ext import ContextTypes

async def handle_web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle data sent from mini app"""
    
    web_app_data = update.message.web_app_data.data
    data = json.loads(web_app_data)
    
    if data['action'] == 'item_selected':
        item_id = data['item_id']
        item_name = data['item_name']
        
        await update.message.reply_text(
            f"✅ شما کالای '{item_name}' را انتخاب کردید"
        )

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handler for web app data
    application.add_handler(
        MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_web_app_data)
    )
    
    application.run_polling()
```

---

## 📊 Complete Integration Example

```python
# bot/bot.py - Complete example

from telegram import (
    Update, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    MenuButtonWebApp,
    WebAppInfo
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# Mini app URL (change for production)
MINI_APP_URL = "https://yourdomain.com/mini-app"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command with mini app button"""
    
    keyboard = [
        [
            InlineKeyboardButton(
                "🔍 باز کردن وب اپ",
                web_app=WebAppInfo(url=MINI_APP_URL)
            )
        ]
    ]
    
    await update.message.reply_text(
        "سلام! 👋\n\n"
        "به ربات انبارداری خوش آمدید.\n"
        "برای استفاده از وب اپ، دکمه زیر را بزنید:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle data from mini app"""
    
    data = json.loads(update.message.web_app_data.data)
    
    await update.message.reply_text(
        f"✅ داده دریافت شد:\n{json.dumps(data, indent=2, ensure_ascii=False)}"
    )

async def setup_menu_button(application):
    """Set permanent menu button"""
    await application.bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="📱 وب اپ",
            web_app=WebAppInfo(url=MINI_APP_URL)
        )
    )

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_web_app_data)
    )
    
    # Setup menu button
    application.post_init = setup_menu_button
    
    # Start bot
    application.run_polling()

if __name__ == "__main__":
    main()
```

---

## ✅ Checklist

- [ ] Mini app URL is HTTPS
- [ ] Mini app is accessible from internet
- [ ] Menu button configured in BotFather
- [ ] Bot code updated to handle web app data
- [ ] FastAPI validates Telegram init data
- [ ] CORS enabled for mini app domain
- [ ] Tested in Telegram app (not browser)

---

## 🐛 Troubleshooting

### Mini app doesn't open
- Check URL is HTTPS
- Check URL is accessible
- Check Telegram app is updated

### "Invalid init data" error
- Check bot token matches
- Check validation logic in FastAPI
- Check headers are being sent

### Can't send data to bot
- Check `tg.sendData()` is called correctly
- Check bot has handler for `WEB_APP_DATA`
- Check data is valid JSON

---

## 📚 Resources

- [Telegram Mini Apps Docs](https://core.telegram.org/bots/webapps)
- [Bot API - Web Apps](https://core.telegram.org/bots/api#webapps)
- [python-telegram-bot Examples](https://docs.python-telegram-bot.org/)

