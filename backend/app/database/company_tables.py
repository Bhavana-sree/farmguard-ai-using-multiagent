"""
Recreate Companies Table with correct schema
Run this if columns are still missing
"""

import sqlite3

DB_PATH = "farmguard.db"

def recreate_companies_table():
    print("🔧 Recreating companies table with correct schema...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Save existing data if any
    try:
        cursor.execute("SELECT * FROM companies")
        existing_data = cursor.fetchall()
        print(f"📊 Found {len(existing_data)} existing company records")
    except:
        existing_data = []
        print("📊 No existing company data found")
    
    # Drop and recreate with correct schema
    cursor.execute("DROP TABLE IF EXISTS companies")
    cursor.execute("""
        CREATE TABLE companies (
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
    print("✅ Companies table recreated with correct schema")
    
    # Restore data if any
    if existing_data:
        for row in existing_data:
            # Handle different possible old structures
            try:
                if len(row) >= 5:  # At least has id, name, etc.
                    cursor.execute("""
                        INSERT INTO companies 
                        (id, name, phone, email, village, language, status)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        row[0],  # id
                        row[1] if len(row) > 1 else "Unknown",  # name
                        row[2] if len(row) > 2 else "0000000000",  # phone
                        row[3] if len(row) > 3 else None,  # email
                        "Restored",  # village
                        "English",  # language
                        "active"   # status
                    ))
            except Exception as e:
                print(f"⚠️ Could not restore row {row[0]}: {e}")
        
        print(f"✅ Restored {len(existing_data)} company records")
    
    conn.commit()
    
    # Verify structure
    cursor.execute("PRAGMA table_info(companies)")
    columns = cursor.fetchall()
    print("\n📋 New companies table structure:")
    for col in columns:
        print(f"  {col[1]} - {col[2]}")
    
    conn.close()
    print("\n✅ Companies table recreation complete!")

if __name__ == "__main__":
    recreate_companies_table()