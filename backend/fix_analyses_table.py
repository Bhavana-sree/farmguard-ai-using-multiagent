"""
Fix analyses table - Add missing result_json column
Run this script to fix the database schema
"""

import sqlite3
import os

DB_PATH = "farmguard.db"

def fix_analyses_table():
    print("🔧 Fixing analyses table...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check current columns
    cursor.execute("PRAGMA table_info(analyses)")
    columns = [col[1] for col in cursor.fetchall()]
    print(f"Current columns: {columns}")
    
    # Add missing columns
    if 'result_json' not in columns:
        cursor.execute("ALTER TABLE analyses ADD COLUMN result_json TEXT")
        print("✅ Added column: result_json")
    else:
        print("✅ Column result_json already exists")
    
    if 'carbon_credits' not in columns:
        cursor.execute("ALTER TABLE analyses ADD COLUMN carbon_credits REAL")
        print("✅ Added column: carbon_credits")
    
    if 'validation_status' not in columns:
        cursor.execute("ALTER TABLE analyses ADD COLUMN validation_status TEXT")
        print("✅ Added column: validation_status")
    
    conn.commit()
    
    # Verify new structure
    cursor.execute("PRAGMA table_info(analyses)")
    columns = cursor.fetchall()
    print("\n📋 Updated analyses table structure:")
    for col in columns:
        print(f"   {col[1]} - {col[2]}")
    
    conn.close()
    print("\n✅ Database fix complete!")

if __name__ == "__main__":
    fix_analyses_table()