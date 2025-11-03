# Telegram Bot Module

This module contains the Telegram bot implementation for warehouse management.

## Files

- `bot.py` - Main bot application
- `messages.py` - Persian UI messages
- `handlers_*.py` - Command and callback handlers for different entities
- `__init__.py` - Module initialization

## Running the Bot

### Local Development (Windows):
```cmd
start_bot.bat
```

### Linux/cPanel:
```bash
./start_bot.sh
```

Or from project root:
```bash
python bot/bot.py
```

## Environment Variables

Create a `.env` file in the project root:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
BOT_PASSWORD=ciFarco@1213#3221
```

## Features

- ✅ User authentication with password
- ✅ Full CRUD operations for items, categories, brands, measure types
- ✅ Image upload for items
- ✅ Low stock alerts
- ✅ Search items by text, brand, category
- ✅ Shamsi (Persian) date system
- ✅ Inline keyboard navigation

## Handler Modules

- `handlers_category.py` - Category management
- `handlers_subcategory.py` - Subcategory management  
- `handlers_brand.py` - Brand management
- `handlers_measure_type.py` - Measurement unit management
- `handlers_item.py` - Item/product management
- `handlers_low_stock.py` - Low stock item display

## Dependencies

All dependencies are managed at the project root level. See `/requirements.txt`.

