# Database Module

This module contains database layer and utility functions.

## Files

- `database.py` - SQLite database operations (CRUD functions)
- `utils.py` - Utility functions (code generation, date formatting)
- `warehouse.db` - SQLite database file (created at runtime)
- `__init__.py` - Module initialization

## Database Schema

### Tables

1. **categories** - Product categories (دسته‌بندی‌ها)
2. **subcategories** - Product subcategories (زیردسته‌ها)
3. **brands** - Product brands (برندها)
4. **measure_types** - Measurement units (واحدهای اندازه‌گیری)
5. **items** - Products/items (کالاها)
6. **item_images** - Item images (تصاویر کالاها)
7. **user_states** - Bot conversation states
8. **authenticated_users** - Authenticated bot users

## Key Functions

### Items
- `create_item()` - Create new item
- `get_all_items()` - Get all items
- `get_item_by_id()` - Get item details
- `search_items()` - Search items by text
- `get_items_by_brand()` - Get items by brand
- `get_items_by_subcategory()` - Get items by subcategory
- `get_low_stock_items()` - Get low stock items
- `update_item()` - Update item
- `delete_item()` - Delete item

### Categories, Brands, Measure Types
- Similar CRUD functions for each entity

### Authentication
- `is_user_authenticated()` - Check user authentication
- `authenticate_user()` - Save authenticated user

## Usage

```python
from database import database as db

# Get all items
items = db.get_all_items()

# Search items
results = db.search_items("keyword")

# Get item by ID
item = db.get_item_by_id(1)
```

## Backup

The database file `warehouse.db` is automatically backed up daily (see `backup_db.sh` in project root).

## Database Type

**SQLite** - Simple, file-based, serverless database.

Perfect for:
- ✅ Single application access
- ✅ No server setup required  
- ✅ Easy backup (just copy the file)
- ✅ Fast for read operations
- ✅ ACID compliant

