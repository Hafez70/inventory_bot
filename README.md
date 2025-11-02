# Telegram Warehouse Management Bot

A comprehensive Telegram bot for managing warehouse inventory with support for items, categories, subcategories, brands, and images.

## Features

✨ **Persian Interface** - All messages and interactions are in Persian (Farsi)
📅 **Shamsi Date Support** - Uses Jalali (Persian) calendar for all dates
📁 **Category Management** - Create, read, update, and delete categories
📂 **Subcategory Management** - Organize items with subcategories
🏷️ **Brand Management** - Manage product brands
📦 **Item Management** - Full CRUD operations on inventory items
📷 **Image Support** - Upload and store multiple images per item
🔐 **System-Generated Codes** - Automatic unique code generation for all entities
🎯 **Button-Based Interface** - All commands accessible via inline keyboard buttons

## Requirements

- Python 3.8 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))

## Installation

1. **Clone or download this project**

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure the bot**

Create a `.env` file in the project root with your Telegram bot token:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

To get a bot token:
- Open Telegram and search for [@BotFather](https://t.me/botfather)
- Send `/newbot` command
- Follow the instructions to create your bot
- Copy the token provided by BotFather

4. **Run the bot**
```bash
python bot.py
```

## Usage

### Starting the Bot

1. Open Telegram and search for your bot
2. Send `/start` command
3. Use the inline keyboard buttons to navigate

### Main Features

#### Categories (دسته‌بندی‌ها)
- **Create**: Add new categories with auto-generated codes
- **List**: View all categories
- **Edit**: Update category names
- **Delete**: Remove categories (warning: deletes related items)

#### Subcategories (زیردسته‌ها)
- **Create**: Add subcategories linked to categories
- **List**: View all subcategories with their parent categories
- **Edit**: Update subcategory names
- **Delete**: Remove subcategories

#### Brands (برندها)
- **Create**: Add new brands
- **List**: View all brands
- **Edit**: Update brand names
- **Delete**: Remove brands

#### Items (کالاها)
- **Create**: Add new items with:
  - Category selection
  - Subcategory selection (optional)
  - Brand selection
  - Item name
  - Auto-generated item code
  - Multiple image uploads
- **List**: View all items
- **View**: See detailed item information
- **Edit**: Update item details or add more images
- **Delete**: Remove items (deletes all related images)
- **View Images**: Display all images for an item

### Code Generation

The system automatically generates unique codes for all entities:
- Categories: `CAT######`
- Subcategories: `SUB######`
- Brands: `BRD######`
- Items: `ITM######`

### Image Storage

All uploaded images are stored in the `images/` folder with naming format:
```
item_{item_id}_{image_number}.jpg
```

## Database

The bot uses SQLite database (`warehouse.db`) to store all data:
- Categories
- Subcategories
- Brands
- Items
- Item Images
- User States (for conversation flow)

## Project Structure

```
.
├── bot.py                      # Main bot file
├── database.py                 # Database operations
├── messages.py                 # Persian text messages
├── utils.py                    # Utility functions
├── handlers_category.py        # Category handlers
├── handlers_subcategory.py     # Subcategory handlers
├── handlers_brand.py           # Brand handlers
├── handlers_item.py            # Item handlers
├── requirements.txt            # Python dependencies
├── .env                        # Bot configuration (create this)
├── warehouse.db               # SQLite database (auto-created)
├── images/                    # Image storage (auto-created)
└── README.md                  # This file
```

## Dependencies

- `python-telegram-bot==20.7` - Telegram Bot API wrapper
- `jdatetime==4.1.1` - Shamsi (Jalali) date support
- `Pillow==10.1.0` - Image processing
- `python-dotenv==1.0.0` - Environment variable management

## Notes

- The bot supports multiple users simultaneously
- Each user can have their own conversation flow
- All dates are displayed in Shamsi (Jalali) format
- Images are stored permanently in the `images/` folder
- Database is created automatically on first run
- The bot uses inline keyboards for all interactions (no text commands)

## Troubleshooting

### Bot doesn't respond
- Check if the bot is running
- Verify the bot token in `.env` file
- Make sure you've sent `/start` command

### Images not uploading
- Check if `images/` folder exists and has write permissions
- Verify image format (JPG, PNG supported)

### Database errors
- Delete `warehouse.db` file to reset (WARNING: deletes all data)
- The database will be recreated on next run

## License

This project is provided as-is for warehouse management purposes.

## Support

For issues or questions, please check the code comments or modify as needed for your specific use case.

---

**Created for CI-FARCO Warehousing Project**

مدیریت انبار با ربات تلگرام 🏪

