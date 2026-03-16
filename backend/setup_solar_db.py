import sqlite3
import os

DB_PATH = "farmguard.db"

def setup_solar_database():
    """Create solar producer tables in the database"""
    
    print("🔧 Setting up Solar Producer Database...")
    print(f"📁 Database path: {os.path.abspath(DB_PATH)}")
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Solar Producers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS solar_producers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            village TEXT NOT NULL,
            language TEXT NOT NULL,
            plant_capacity_kw REAL,
            installation_date TEXT,
            panel_type TEXT,
            inverter_type TEXT,
            grid_connected BOOLEAN,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✅ Table 'solar_producers' ready")
    
    # 2. Solar Plants table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS solar_plants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producer_id INTEGER NOT NULL,
            plant_name TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            total_area_sqm REAL,
            panel_count INTEGER,
            tilt_angle REAL,
            azimuth_angle REAL,
            FOREIGN KEY (producer_id) REFERENCES solar_producers (id) ON DELETE CASCADE
        )
    """)
    print("✅ Table 'solar_plants' ready")
    
    # 3. Solar Analyses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS solar_analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plant_id INTEGER NOT NULL,
            analysis_date TEXT NOT NULL,
            energy_output_json TEXT NOT NULL,
            carbon_credits REAL,
            validation_json TEXT,
            FOREIGN KEY (plant_id) REFERENCES solar_plants (id) ON DELETE CASCADE
        )
    """)
    print("✅ Table 'solar_analyses' ready")
    
    # 4. Solar Transactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS solar_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producer_id INTEGER NOT NULL,
            buyer_company TEXT NOT NULL,
            credits_sold REAL NOT NULL,
            price_per_credit REAL NOT NULL,
            total_amount REAL NOT NULL,
            transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'completed',
            FOREIGN KEY (producer_id) REFERENCES solar_producers (id)
        )
    """)
    print("✅ Table 'solar_transactions' ready")
    
    # Commit changes
    conn.commit()
    
    # List all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"\n📊 All tables in database: {[t[0] for t in tables]}")
    
    conn.close()
    print(f"\n✅ Solar database setup complete!")
    print(f"📍 Database location: {os.path.abspath(DB_PATH)}")

if __name__ == "__main__":
    setup_solar_database()