"""
Microalgae Database Setup - Complete tables for farmer productivity
"""

import sqlite3
import os

DB_PATH = "farmguard.db"

def setup_microalgae_tables():
    print("=" * 60)
    print("🧫 MICROALGAE DATABASE SETUP")
    print("=" * 60)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Table 1: Algae Ponds
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS algae_ponds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_id INTEGER NOT NULL,
            pond_name TEXT,
            pond_type TEXT DEFAULT 'raceway',
            area_sqm REAL NOT NULL,
            depth_m REAL DEFAULT 0.3,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (farmer_id) REFERENCES farmers (id)
        )
    """)
    print("✅ Table 'algae_ponds' created")
    
    # Table 2: Algae Harvests (for carbon credits)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS algae_harvests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pond_id INTEGER NOT NULL,
            harvest_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            biomass_kg REAL NOT NULL,
            co2_captured_kg REAL,
            carbon_credits REAL,
            verification_status TEXT DEFAULT 'pending',
            FOREIGN KEY (pond_id) REFERENCES algae_ponds (id)
        )
    """)
    print("✅ Table 'algae_harvests' created")
    
    # Table 3: Algae Applications (for crop productivity)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS algae_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_id INTEGER NOT NULL,
            crop_type TEXT,
            application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            algae_used_kg REAL,
            area_applied_acres REAL,
            expected_yield_increase REAL,
            FOREIGN KEY (farmer_id) REFERENCES farmers (id)
        )
    """)
    print("✅ Table 'algae_applications' created - TRACKS CROP YIELD IMPROVEMENT")
    
    # Table 4: Algae Productivity Records
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS algae_productivity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_id INTEGER NOT NULL,
            record_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            crop_yield_before REAL,
            crop_yield_after REAL,
            yield_increase_percent REAL,
            water_saved_liters REAL,
            fertilizer_saved_kg REAL,
            notes TEXT,
            FOREIGN KEY (farmer_id) REFERENCES farmers (id)
        )
    """)
    print("✅ Table 'algae_productivity' created - MEASURES IMPROVEMENT")
    
    conn.commit()
    
    # Show all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    
    print("\n📊 All tables in database:")
    for table in tables:
        if 'algae' in table[0]:
            print(f"   🧫 {table[0]}")
        else:
            print(f"   📁 {table[0]}")
    
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ MICROALGAE DATABASE READY!")
    print("   Farmers can now:")
    print("   1. Register algae ponds")
    print("   2. Harvest algae for carbon credits")
    print("   3. Apply algae to crops for better yield")
    print("   4. Track productivity improvements")
    print("=" * 60)

if __name__ == "__main__":
    setup_microalgae_tables()