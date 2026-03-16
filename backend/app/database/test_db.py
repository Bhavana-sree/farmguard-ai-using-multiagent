import sqlite3
import time

DB_PATH = "farmguard.db"

def test_connection():
    print("🔍 Testing database connection...")
    
    for attempt in range(5):
        try:
            conn = sqlite3.connect(DB_PATH, timeout=10)  # 10 second timeout
            cursor = conn.cursor()
            
            # Test query
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            print(f"✅ Connection successful! Found {len(tables)} tables")
            conn.close()
            return True
            
        except sqlite3.OperationalError as e:
            print(f"❌ Attempt {attempt + 1}: {e}")
            time.sleep(1)
    
    return False

if __name__ == "__main__":
    test_connection()