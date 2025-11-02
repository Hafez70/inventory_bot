import sqlite3
import os
from datetime import datetime
import jdatetime

DATABASE_FILE = 'warehouse.db'

def init_database():
    """Initialize the database with all required tables."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Categories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    
    # Subcategories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subcategories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
        )
    ''')
    
    # Brands table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS brands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    
    # Measure types table (for inventory thresholds)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS measure_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            low_stock_threshold REAL NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )
    ''')
    
    # Items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            custom_code TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            category_id INTEGER NOT NULL,
            subcategory_id INTEGER NOT NULL,
            brand_id INTEGER NOT NULL,
            measure_type_id INTEGER NOT NULL,
            available_count REAL DEFAULT 0,
            video_url TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories(id),
            FOREIGN KEY (subcategory_id) REFERENCES subcategories(id),
            FOREIGN KEY (brand_id) REFERENCES brands(id),
            FOREIGN KEY (measure_type_id) REFERENCES measure_types(id)
        )
    ''')
    
    # Item images table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS item_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL,
            image_path TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
        )
    ''')
    
    # User states table (for conversation flow)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_states (
            user_id INTEGER PRIMARY KEY,
            state TEXT,
            data TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    
    # Create images directory if it doesn't exist
    if not os.path.exists('images'):
        os.makedirs('images')

def get_connection():
    """Get a database connection."""
    return sqlite3.connect(DATABASE_FILE)

# Category CRUD operations
def create_category(name, code):
    """Create a new category."""
    conn = get_connection()
    cursor = conn.cursor()
    created_at = jdatetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    try:
        cursor.execute(
            'INSERT INTO categories (code, name, created_at) VALUES (?, ?, ?)',
            (code, name, created_at)
        )
        conn.commit()
        category_id = cursor.lastrowid
        conn.close()
        return category_id
    except sqlite3.IntegrityError:
        conn.close()
        return None

def get_all_categories():
    """Get all categories."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, code, name, created_at FROM categories ORDER BY name')
    categories = cursor.fetchall()
    conn.close()
    return categories

def get_category_by_id(category_id):
    """Get a category by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, code, name, created_at FROM categories WHERE id = ?', (category_id,))
    category = cursor.fetchone()
    conn.close()
    return category

def update_category(category_id, name):
    """Update a category."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE categories SET name = ? WHERE id = ?', (name, category_id))
    conn.commit()
    conn.close()

def delete_category(category_id):
    """Delete a category."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM categories WHERE id = ?', (category_id,))
    conn.commit()
    conn.close()

# Subcategory CRUD operations
def create_subcategory(name, code, category_id):
    """Create a new subcategory."""
    conn = get_connection()
    cursor = conn.cursor()
    created_at = jdatetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    try:
        cursor.execute(
            'INSERT INTO subcategories (code, name, category_id, created_at) VALUES (?, ?, ?, ?)',
            (code, name, category_id, created_at)
        )
        conn.commit()
        subcategory_id = cursor.lastrowid
        conn.close()
        return subcategory_id
    except sqlite3.IntegrityError:
        conn.close()
        return None

def get_all_subcategories():
    """Get all subcategories with their category names."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.id, s.code, s.name, s.category_id, c.name, s.created_at
        FROM subcategories s
        JOIN categories c ON s.category_id = c.id
        ORDER BY s.name
    ''')
    subcategories = cursor.fetchall()
    conn.close()
    return subcategories

def get_subcategories_by_category(category_id):
    """Get all subcategories for a specific category."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT id, code, name, created_at FROM subcategories WHERE category_id = ? ORDER BY name',
        (category_id,)
    )
    subcategories = cursor.fetchall()
    conn.close()
    return subcategories

def get_subcategory_by_id(subcategory_id):
    """Get a subcategory by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.id, s.code, s.name, s.category_id, c.name, s.created_at
        FROM subcategories s
        JOIN categories c ON s.category_id = c.id
        WHERE s.id = ?
    ''', (subcategory_id,))
    subcategory = cursor.fetchone()
    conn.close()
    return subcategory

def update_subcategory(subcategory_id, name):
    """Update a subcategory."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE subcategories SET name = ? WHERE id = ?', (name, subcategory_id))
    conn.commit()
    conn.close()

def delete_subcategory(subcategory_id):
    """Delete a subcategory."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM subcategories WHERE id = ?', (subcategory_id,))
    conn.commit()
    conn.close()

# Brand CRUD operations
def create_brand(name, code):
    """Create a new brand."""
    conn = get_connection()
    cursor = conn.cursor()
    created_at = jdatetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    try:
        cursor.execute(
            'INSERT INTO brands (code, name, created_at) VALUES (?, ?, ?)',
            (code, name, created_at)
        )
        conn.commit()
        brand_id = cursor.lastrowid
        conn.close()
        return brand_id
    except sqlite3.IntegrityError:
        conn.close()
        return None

def get_all_brands():
    """Get all brands."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, code, name, created_at FROM brands ORDER BY name')
    brands = cursor.fetchall()
    conn.close()
    return brands

def get_brand_by_id(brand_id):
    """Get a brand by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, code, name, created_at FROM brands WHERE id = ?', (brand_id,))
    brand = cursor.fetchone()
    conn.close()
    return brand

def update_brand(brand_id, name):
    """Update a brand."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE brands SET name = ? WHERE id = ?', (name, brand_id))
    conn.commit()
    conn.close()

def delete_brand(brand_id):
    """Delete a brand."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM brands WHERE id = ?', (brand_id,))
    conn.commit()
    conn.close()

# Measure Type CRUD operations
def create_measure_type(name, code, low_stock_threshold=0):
    """Create a new measure type."""
    conn = get_connection()
    cursor = conn.cursor()
    created_at = jdatetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    try:
        cursor.execute(
            'INSERT INTO measure_types (code, name, low_stock_threshold, created_at) VALUES (?, ?, ?, ?)',
            (code, name, low_stock_threshold, created_at)
        )
        conn.commit()
        measure_type_id = cursor.lastrowid
        conn.close()
        return measure_type_id
    except sqlite3.IntegrityError:
        conn.close()
        return None

def get_all_measure_types():
    """Get all measure types."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, code, name, low_stock_threshold, created_at FROM measure_types ORDER BY name')
    measure_types = cursor.fetchall()
    conn.close()
    return measure_types

def get_measure_type_by_id(measure_type_id):
    """Get a measure type by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, code, name, low_stock_threshold, created_at FROM measure_types WHERE id = ?', (measure_type_id,))
    measure_type = cursor.fetchone()
    conn.close()
    return measure_type

def update_measure_type(measure_type_id, name, low_stock_threshold):
    """Update a measure type."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE measure_types SET name = ?, low_stock_threshold = ? WHERE id = ?', 
                   (name, low_stock_threshold, measure_type_id))
    conn.commit()
    conn.close()

def delete_measure_type(measure_type_id):
    """Delete a measure type."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM measure_types WHERE id = ?', (measure_type_id,))
    conn.commit()
    conn.close()

# Item CRUD operations
def create_item(name, code, custom_code, category_id, subcategory_id, brand_id, measure_type_id, 
                description=None, available_count=0, video_url=None):
    """Create a new item."""
    conn = get_connection()
    cursor = conn.cursor()
    now = jdatetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    try:
        cursor.execute(
            '''INSERT INTO items (code, custom_code, name, description, category_id, subcategory_id, 
               brand_id, measure_type_id, available_count, video_url, created_at, updated_at) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (code, custom_code, name, description, category_id, subcategory_id, brand_id, 
             measure_type_id, available_count, video_url, now, now)
        )
        conn.commit()
        item_id = cursor.lastrowid
        conn.close()
        return item_id
    except sqlite3.IntegrityError:
        conn.close()
        return None

def get_all_items():
    """Get all items with their related data."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT i.id, i.code, i.custom_code, i.name, i.description,
               c.name, s.name, b.name, m.name, i.available_count, i.video_url,
               i.created_at, i.updated_at
        FROM items i
        JOIN categories c ON i.category_id = c.id
        JOIN subcategories s ON i.subcategory_id = s.id
        JOIN brands b ON i.brand_id = b.id
        JOIN measure_types m ON i.measure_type_id = m.id
        ORDER BY i.created_at DESC
    ''')
    items = cursor.fetchall()
    conn.close()
    return items

def get_item_by_id(item_id):
    """Get an item by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT i.id, i.code, i.custom_code, i.name, i.description,
               i.category_id, c.name,
               i.subcategory_id, s.name,
               i.brand_id, b.name,
               i.measure_type_id, m.name,
               i.available_count, i.video_url,
               i.created_at, i.updated_at
        FROM items i
        JOIN categories c ON i.category_id = c.id
        JOIN subcategories s ON i.subcategory_id = s.id
        JOIN brands b ON i.brand_id = b.id
        JOIN measure_types m ON i.measure_type_id = m.id
        WHERE i.id = ?
    ''', (item_id,))
    item = cursor.fetchone()
    conn.close()
    return item

def update_item(item_id, name, custom_code, category_id, subcategory_id, brand_id, measure_type_id,
                description=None, available_count=0, video_url=None):
    """Update an item."""
    conn = get_connection()
    cursor = conn.cursor()
    updated_at = jdatetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    cursor.execute(
        '''UPDATE items SET name = ?, custom_code = ?, description = ?, category_id = ?, 
           subcategory_id = ?, brand_id = ?, measure_type_id = ?, available_count = ?, 
           video_url = ?, updated_at = ? WHERE id = ?''',
        (name, custom_code, description, category_id, subcategory_id, brand_id, measure_type_id,
         available_count, video_url, updated_at, item_id)
    )
    conn.commit()
    conn.close()

def get_low_stock_items():
    """Get items that are below their measure type's low stock threshold."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT i.id, i.code, i.custom_code, i.name, i.available_count,
               c.name, s.name, b.name, m.name, m.low_stock_threshold
        FROM items i
        JOIN categories c ON i.category_id = c.id
        JOIN subcategories s ON i.subcategory_id = s.id
        JOIN brands b ON i.brand_id = b.id
        JOIN measure_types m ON i.measure_type_id = m.id
        WHERE i.available_count <= m.low_stock_threshold
        ORDER BY i.available_count ASC
    ''')
    items = cursor.fetchall()
    conn.close()
    return items

def delete_item(item_id):
    """Delete an item and its images."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get all image paths
    cursor.execute('SELECT image_path FROM item_images WHERE item_id = ?', (item_id,))
    images = cursor.fetchall()
    
    # Delete image files
    for image in images:
        image_path = image[0]
        if os.path.exists(image_path):
            os.remove(image_path)
    
    # Delete from database
    cursor.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()

# Item images operations
def add_item_image(item_id, image_path):
    """Add an image to an item."""
    conn = get_connection()
    cursor = conn.cursor()
    created_at = jdatetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    cursor.execute(
        'INSERT INTO item_images (item_id, image_path, created_at) VALUES (?, ?, ?)',
        (item_id, image_path, created_at)
    )
    conn.commit()
    conn.close()

def get_item_images(item_id):
    """Get all images for an item."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, image_path, created_at FROM item_images WHERE item_id = ?', (item_id,))
    images = cursor.fetchall()
    conn.close()
    return images

def delete_item_image(image_id):
    """Delete an item image."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get image path
    cursor.execute('SELECT image_path FROM item_images WHERE id = ?', (image_id,))
    result = cursor.fetchone()
    if result:
        image_path = result[0]
        if os.path.exists(image_path):
            os.remove(image_path)
        cursor.execute('DELETE FROM item_images WHERE id = ?', (image_id,))
    
    conn.commit()
    conn.close()

# User state management
def set_user_state(user_id, state, data=None):
    """Set user state for conversation flow."""
    conn = get_connection()
    cursor = conn.cursor()
    import json
    # Always store data as JSON string, even if empty dict
    if data is None:
        data = {}
    data_str = json.dumps(data)
    cursor.execute(
        'INSERT OR REPLACE INTO user_states (user_id, state, data) VALUES (?, ?, ?)',
        (user_id, state, data_str)
    )
    conn.commit()
    conn.close()

def get_user_state(user_id):
    """Get user state."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT state, data FROM user_states WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        import json
        state, data = result
        # Always return a dict, even if empty
        return state, json.loads(data) if data else {}
    return None, {}

def clear_user_state(user_id):
    """Clear user state."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM user_states WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

# Initialize database on import
init_database()

