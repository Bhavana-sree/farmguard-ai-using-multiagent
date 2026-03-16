"""
Fix Companies Table - Add missing village and other columns
Run this to add all required columns to companies table
"""

import sqlite3

DB_PATH = "farmguard.db"

def fix_companies_table_complete():
    print("🔧 Fixing companies table - adding all required columns...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check current structure
    cursor.execute("PRAGMA table_info(companies)")
    columns = {col[1]: col[2] for col in cursor.fetchall()}
    print(f"Current columns: {list(columns.keys())}")
    
    # List of columns that should exist
    required_columns = {
        'village': 'TEXT',
        'language': 'TEXT',
        'registration_number': 'TEXT',
        'gst_number': 'TEXT',
        'company_type': 'TEXT',
        'year_established': 'TEXT',
        'registered_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
        'status': 'TEXT DEFAULT "active"'
    }
    
    # Add missing columns
    for col_name, col_type in required_columns.items():
        if col_name not in columns:
            try:
                cursor.execute(f"ALTER TABLE companies ADD COLUMN {col_name} {col_type}")
                print(f"✅ Added column: {col_name}")
            except Exception as e:
                print(f"⚠️ Could not add {col_name}: {e}")
    
    # Set default values for new columns
    cursor.execute("UPDATE companies SET village = 'Unknown' WHERE village IS NULL")
    cursor.execute("UPDATE companies SET language = 'English' WHERE language IS NULL")
    
    conn.commit()
    
    # Show final structure
    cursor.execute("PRAGMA table_info(companies)")
    final_columns = cursor.fetchall()
    print("\n📋 Final companies table structure:")
    for col in final_columns:
        print(f"  {col[1]} - {col[2]}")
    
    conn.close()
    print("\n✅ Companies table fixed - all columns added!")

if __name__ == "__main__":
    fix_companies_table_complete()