"""Migration script to add custom_code and description fields to items table."""

import sqlite3
import os
import sys

# Fix encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

DATABASE_FILE = 'warehouse.db'

def migrate():
    """Apply migration to add new fields to items table."""
    if not os.path.exists(DATABASE_FILE):
        print("❌ Database file not found. Creating new database with latest schema...")
        import database
        print("✅ New database created successfully!")
        return
    
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(items)")
        columns = [column[1] for column in cursor.fetchall()]
        
        needs_migration = False
        
        # Add missing columns
        if 'custom_code' not in columns:
            print("➕ Adding custom_code column...")
            cursor.execute('ALTER TABLE items ADD COLUMN custom_code TEXT')
            needs_migration = True
        
        if 'description' not in columns:
            print("➕ Adding description column...")
            cursor.execute('ALTER TABLE items ADD COLUMN description TEXT')
            needs_migration = True
        
        if 'measure_type_id' not in columns:
            print("➕ Adding measure_type_id column...")
            cursor.execute('ALTER TABLE items ADD COLUMN measure_type_id INTEGER')
            needs_migration = True
        
        if 'available_count' not in columns:
            print("➕ Adding available_count column...")
            cursor.execute('ALTER TABLE items ADD COLUMN available_count REAL DEFAULT 0')
            needs_migration = True
        
        if 'video_url' not in columns:
            print("➕ Adding video_url column...")
            cursor.execute('ALTER TABLE items ADD COLUMN video_url TEXT')
            needs_migration = True
        
        # Check if measure_types table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='measure_types'")
        if not cursor.fetchone():
            print("➕ Creating measure_types table...")
            cursor.execute('''
                CREATE TABLE measure_types (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    low_stock_threshold REAL NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL
                )
            ''')
            needs_migration = True
        
        # Check if authenticated_users table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='authenticated_users'")
        if not cursor.fetchone():
            print("➕ Creating authenticated_users table...")
            cursor.execute('''
                CREATE TABLE authenticated_users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    authenticated_at TEXT NOT NULL
                )
            ''')
            needs_migration = True
        
        if needs_migration:
            conn.commit()
            print("✅ Migration completed successfully!")
            print("\n⚠️  IMPORTANT: You need to update existing items to set measure_type_id!")
            print("    First, create some measure types, then update your items.")
        else:
            print("✅ Database is already up to date.")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    print("🔄 Running database migration...")
    migrate()

