"""
Fix Farmers Table - Remove UNIQUE constraint on phone
Run this file directly with Python
"""

import sqlite3

DB_PATH = "farmguard.db"

def fix_farmers_table():
    print("🔧 Fixing farmers table...")
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create new table without UNIQUE constraint
    cursor.execute("DROP TABLE IF EXISTS farmers_new")
    cursor.execute("""
        CREATE TABLE farmers_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            village TEXT NOT NULL,
            language TEXT NOT NULL
        )
    """)
    
    # Copy data from old table if it exists
    try:
        cursor.execute("INSERT INTO farmers_new SELECT id, name, phone, village, language FROM farmers")
        print("✅ Copied existing farmer data")
    except Exception as e:
        print(f"ℹ️ No data to copy or error: {e}")
    
    # Drop old table and rename new one
    cursor.execute("DROP TABLE IF EXISTS farmers")
    cursor.execute("ALTER TABLE farmers_new RENAME TO farmers")
    
    conn.commit()
    conn.close()
    
    print("✅ Farmers table fixed - UNIQUE constraint removed")
    
    # Verify the fix
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='farmers'")
    schema = cursor.fetchone()[0]
    print(f"\n📋 New farmers table schema:")
    print(schema)
    conn.close()

if __name__ == "__main__":
    fix_farmers_table()
