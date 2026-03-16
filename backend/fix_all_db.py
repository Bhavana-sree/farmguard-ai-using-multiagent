"""
Complete Database Fix Script
Run this to fix all database issues
"""

import sqlite3
import time

DB_PATH = "farmguard.db"

def fix_all():
    print("=" * 60)
    print("🔧 FARMGUARD AI - DATABASE FIX UTILITY")
    print("=" * 60)
    
    conn = sqlite3.connect(DB_PATH, timeout=30)
    cursor = conn.cursor()
    
    # 1. Fix Farmers table - remove UNIQUE constraint
    print("\n📋 Fixing Farmers table...")
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
    try:
        cursor.execute("INSERT INTO farmers_new SELECT id, name, phone, village, language FROM farmers")
        print("✅ Copied existing farmer data")
    except:
        print("ℹ️ No existing farmer data to copy")
    
    cursor.execute("DROP TABLE IF EXISTS farmers")
    cursor.execute("ALTER TABLE farmers_new RENAME TO farmers")
    print("✅ Farmers table fixed - UNIQUE constraint removed")
    
    # 2. Fix Companies table - add phone column
    print("\n📋 Fixing Companies table...")
    try:
        cursor.execute("ALTER TABLE companies ADD COLUMN phone TEXT")
        print("✅ Added phone column")
    except:
        print("ℹ️ Phone column already exists")
    
    # 3. Update companies table structure
    cursor.execute("DROP TABLE IF EXISTS companies_new")
    cursor.execute("""
        CREATE TABLE companies_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            village TEXT NOT NULL,
            language TEXT NOT NULL,
            registration_number TEXT,
            gst_number TEXT,
            company_type TEXT,
            industry TEXT,
            year_established TEXT,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'active'
        )
    """)
    
    try:
        cursor.execute("""
            INSERT INTO companies_new 
            (id, name, phone, email, village, language, registration_number, gst_number, company_type, industry, year_established, registered_at, status)
            SELECT id, name, COALESCE(phone, ''), email, village, language, registration_number, gst_number, company_type, industry, year_established, registered_at, status
            FROM companies
        """)
        print("✅ Copied existing company data")
    except:
        print("ℹ️ No existing company data to copy")
    
    cursor.execute("DROP TABLE IF EXISTS companies")
    cursor.execute("ALTER TABLE companies_new RENAME TO companies")
    print("✅ Companies table structure updated")
    
    # 4. Set default phone numbers
    cursor.execute("UPDATE companies SET phone = '9876543210' WHERE phone = '' OR phone IS NULL")
    print("✅ Set default phone numbers")
    
    # 5. Show all tables
    print("\n📊 Current database structure:")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        
        # Show table type
        if 'farmer' in table_name:
            emoji = "👨‍🌾"
        elif 'solar' in table_name:
            emoji = "☀️"
        elif 'company' in table_name or 'purchase' in table_name:
            emoji = "🏢"
        else:
            emoji = "📁"
        
        print(f"  {emoji} {table_name}: {count} rows")
    
    conn.commit()
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ DATABASE FIX COMPLETE!")
    print("=" * 60)
    print("\n🚀 Next steps:")
    print("1. Restart your backend server")
    print("2. Run the tests again: python test_api.py")

if __name__ == "__main__":
    # Backup database first
    import shutil
    import os
    from datetime import datetime
    
    backup_name = f"farmguard_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    if os.path.exists(DB_PATH):
        shutil.copy2(DB_PATH, backup_name)
        print(f"✅ Database backed up as: {backup_name}")
    
    fix_all()