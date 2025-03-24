import sqlite3
import os

# Database file path
DB_PATH = 'medicine_reminder.db'

def initialize_database():
    """Initialize the database with required tables if they don't exist."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            doctor TEXT NOT NULL
        )
        ''')

        # Create medicines table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            dosage TEXT,
            source TEXT
        )
        ''')

        # Create prescriptions table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS prescriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            medicine_name TEXT NOT NULL,
            doses INTEGER NOT NULL,
            times TEXT NOT NULL,  -- Store times as comma-separated values
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
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
    """Search for medication information in the database."""
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

def save_form_submission(name, age, doctor, medicines):
    """Save user form data and prescriptions into the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Insert user info and get user_id
        cursor.execute("INSERT INTO users (name, age, doctor) VALUES (?, ?, ?)", (name, age, doctor))
        user_id = cursor.lastrowid

        # Insert medicines into prescriptions table
        for med in medicines:
            cursor.execute(
                "INSERT INTO prescriptions (user_id, medicine_name, doses, times) VALUES (?, ?, ?, ?)",
                (user_id, med["name"], med["doses"], ",".join(med["times"]))
            )

        conn.commit()
        conn.close()
        print("Form data saved successfully.")
        return True

    except Exception as e:
        print(f"Error saving form data: {e}")
        return False
