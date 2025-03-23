import sqlite3
import os

# Database file path
DB_PATH = 'medicine_reminder.db'

def initialize_database():
    """
    Initialize the database with required tables if they don't exist.
    """
    try:
        # Create database directory if it doesn't exist
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        
        # Connect to database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Create medicines table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            dosage TEXT,
            source TEXT
        )
        ''')
        
        conn.commit()
        conn.close()
        
        print("Database initialized successfully.")
        return True
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False

def search_medication(medication_name):
    """
    Search for medication information in the database.
    Returns a dictionary with medication info or None if not found.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Search for medication by name (case insensitive)
        cursor.execute("SELECT name, dosage, source FROM medicines WHERE LOWER(name) = LOWER(?)", (medication_name,))
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            return {
                'name': result[0],
                'dosage': result[1],
                'source': result[2]
            }
        else:
            print(f"No information found for '{medication_name}' in local database.")
            return None
            
    except Exception as e:
        print(f"Database search error: {e}")
        return None

def save_medication(medication_info):
    """
    Save medication information to the database.
    """
    if not medication_info or 'name' not in medication_info:
        return False
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT OR REPLACE INTO medicines (name, dosage, source) VALUES (?, ?, ?)",
            (
                medication_info.get('name', ''),
                medication_info.get('dosage', ''),
                medication_info.get('source', '')
            )
        )
        
        conn.commit()
        conn.close()
        
        print(f"Medication '{medication_info['name']}' saved to database.")
        return True
        
    except Exception as e:
        print(f"Error saving to database: {e}")
        return False