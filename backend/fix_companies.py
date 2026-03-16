"""
Fix Companies Table - Add missing columns
Run this file directly with Python
"""

import sqlite3

DB_PATH = "farmguard.db"

def fix_companies_table():
    print("🔧 Fixing companies table...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if phone column exists
    cursor.execute("PRAGMA table_info(companies)")
    columns = [col[1] for col in cursor.fetchall()]
    print(f"Current columns: {columns}")
    
    if 'phone' not in columns:
        print("📞 Adding phone column...")
        cursor.execute("ALTER TABLE companies ADD COLUMN phone TEXT")
        print("✅ Phone column added")
    
    # Update any NULL phone numbers
    cursor.execute("UPDATE companies SET phone = '9876543210' WHERE phone IS NULL OR phone = ''")
    print("✅ Set default phone numbers")
    
    conn.commit()
    
    # Show updated structure
    cursor.execute("PRAGMA table_info(companies)")
    columns = cursor.fetchall()
    print("\n📋 Updated companies table structure:")
    for col in columns:
        print(f"  {col[1]} - {col[2]}")
    
    conn.close()
    print("\n✅ Companies table fixed!")

if __name__ == "__main__":
    fix_companies_table()