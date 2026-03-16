"""
Company Database Setup Script
Run this from the backend folder to create company tables
"""

import sqlite3
import os
import sys

# Add the parent directory to path so we can import from app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.database.company_models import COMPANY_TABLES_SQL
except ImportError:
    print("❌ Error: Could not import company_models")
    print("Make sure the file exists at: app/database/company_models.py")
    sys.exit(1)

DB_PATH = "farmguard.db"

def setup_company_database():
    """Create all company tables in the database"""
    
    print("=" * 60)
    print("🏢 COMPANY DATABASE SETUP")
    print("=" * 60)
    
    # Check if database exists
    if os.path.exists(DB_PATH):
        print(f"📂 Found existing database: {DB_PATH}")
        size = os.path.getsize(DB_PATH)
        print(f"📊 Size: {size} bytes ({size/1024:.2f} KB)")
    else:
        print(f"🆕 Creating new database: {DB_PATH}")
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("\n🔨 Creating company tables...")
    
    # Create each table from the models
    for table_name, create_sql in COMPANY_TABLES_SQL.items():
        try:
            cursor.execute(create_sql)
            print(f"   ✅ {table_name}")
        except Exception as e:
            print(f"   ❌ {table_name}: {e}")
    
    # Commit changes
    conn.commit()
    
    # Show all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    
    print("\n📊 ALL TABLES IN DATABASE:")
    print("-" * 40)
    
    for table in tables:
        table_name = table[0]
        
        # Count rows
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        
        # Add emoji based on table type
        if 'company' in table_name:
            emoji = "🏢"
        elif 'farmer' in table_name or 'land' in table_name:
            emoji = "👨‍🌾"
        elif 'solar' in table_name:
            emoji = "☀️"
        else:
            emoji = "📁"
        
        print(f"{emoji} {table_name}: {count} rows")
    
    print("-" * 40)
    
    # Verify company tables
    required_tables = list(COMPANY_TABLES_SQL.keys())
    existing_tables = [t[0] for t in tables]
    
    print("\n🔍 VERIFICATION:")
    all_exist = True
    for table in required_tables:
        if table in existing_tables:
            print(f"   ✅ {table}")
        else:
            print(f"   ❌ {table} - MISSING")
            all_exist = False
    
    conn.close()
    
    print("\n" + "=" * 60)
    if all_exist:
        print("✅ COMPANY DATABASE SETUP COMPLETE!")
    else:
        print("⚠️ Setup completed with some issues")
    print(f"📁 Database location: {os.path.abspath(DB_PATH)}")
    print("=" * 60)

def add_sample_company():
    """Add a sample company for testing"""
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("\n📝 Adding sample company data...")
    
    # Check if companies table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='companies'")
    if not cursor.fetchone():
        print("❌ Companies table doesn't exist. Run setup first.")
        return
    
    # Insert sample company
    cursor.execute("""
        INSERT INTO companies 
        (name, phone, email, village, language, registration_number, gst_number, company_type, industry, year_established)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "GreenTech Corporation",
        "9876543210",
        "contact@greentech.com",
        "Mumbai",
        "English",
        "U12345MH2020PTC123456",
        "27AABCU1234E1Z5",
        "Private Limited",
        "Technology",
        "2020"
    ))
    
    company_id = cursor.lastrowid
    print(f"   ✅ Added company with ID: {company_id}")
    
    # Add preferences
    cursor.execute("""
        INSERT INTO company_preferences 
        (company_id, carbon_goal, annual_requirement, price_range, preferred_location)
        VALUES (?, ?, ?, ?, ?)
    """, (
        company_id,
        "Offset entire carbon footprint",
        "1000 - 5000 credits",
        "₹850 - ₹900",
        "India - All regions"
    ))
    print(f"   ✅ Added company preferences")
    
    # Add sample purchase
    cursor.execute("""
        INSERT INTO purchases 
        (company_id, seller_type, seller_id, credits_purchased, price_per_credit, total_amount, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        company_id,
        "solar",
        1,
        100.0,
        890.0,
        89000.0,
        "completed"
    ))
    print(f"   ✅ Added sample purchase")
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Sample company added with ID: {company_id}")
    return company_id

if __name__ == "__main__":
    setup_company_database()
    
    # Ask if user wants to add sample data
    response = input("\nAdd sample company data? (y/n): ").lower()
    if response == 'y':
        add_sample_company()
    
    print("\n🚀 Next steps:")
    print("   1. Start backend: python -m uvicorn app.main:app --reload")
    print("   2. Open company-register.html in browser")
    print("   3. Test registration and verify data in database")