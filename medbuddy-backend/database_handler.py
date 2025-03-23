import sqlite3

def initialize_database():
    """
    Initialize the medications database if it doesn't exist.
    Creates a simple table with medication names and dosages.
    """
    try:
        conn = sqlite3.connect('medbuddy.db')
        cursor = conn.cursor()
        
        # Create medications table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS medications (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            dosage TEXT NOT NULL
        )
        ''')
        
        # Insert some sample data if table is empty
        cursor.execute("SELECT COUNT(*) FROM medications")
        count = cursor.fetchone()[0]
        
        if count == 0:
            sample_data = [
                ('Ibuprofen', 'Adult dosage: 200-400mg every 4-6 hours as needed, not to exceed 1200mg per day'),
                ('Acetaminophen', 'Adult dosage: 325-650mg every 4-6 hours as needed, not to exceed 3000mg per day'),
                ('Aspirin', 'Adult dosage: 325-650mg every 4-6 hours as needed, not to exceed 4000mg per day'),
                ('Loratadine', 'Adult dosage: 10mg once daily')
            ]
            
            cursor.executemany("INSERT INTO medications (name, dosage) VALUES (?, ?)", sample_data)
            print(f"Added {len(sample_data)} sample medications to database")
        
        conn.commit()
        conn.close()
        print("Database initialized successfully")
        
    except Exception as e:
        print(f"Database initialization error: {e}")

def search_medication(medication_name):
    """
    Search the database for medication information.
    Returns a dictionary with medication info or None if not found.
    """
    try:
        # Connect to SQLite database
        conn = sqlite3.connect('medbuddy.db')
        cursor = conn.cursor()
        
        # Query the database for the medication
        cursor.execute("SELECT name, dosage FROM medications WHERE name LIKE ?", ('%' + medication_name + '%',))
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            name, dosage = result
            return {
                'name': name,
                'dosage': dosage,
                'source': 'local database'
            }
        else:
            print(f"Medication '{medication_name}' not found in local database.")
            return None
            
    except Exception as e:
        print(f"Database search error: {e}")
        return None
