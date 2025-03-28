import sqlite3

DB_NAME = "medbuddy.db"

def get_db_connection():
    """Returns a new database connection."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Allows dict-like row access
    return conn

def initialize_database():
    """Ensures all tables exist in the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Run SQL schema updates
        cursor.executescript("""
        PRAGMA foreign_keys = ON;

        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT
        );

        CREATE TABLE IF NOT EXISTS medications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT NOT NULL,
            dosage TEXT,
            frequency TEXT NOT NULL,
            start_date TEXT,
            end_date TEXT,
            quantity INTEGER DEFAULT 0,
            low_stock_alert INTEGER DEFAULT 5,
            prescription_end_date TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );

        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            medication_id INTEGER,
            reminder_time TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            snooze_until TEXT DEFAULT NULL,
            missed_count INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (medication_id) REFERENCES medications (id)
        );

        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            doctor_name TEXT,
            appointment_date TEXT NOT NULL,
            notes TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );

        CREATE TABLE IF NOT EXISTS adherence_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            medication_id INTEGER,
            date TEXT NOT NULL,
            adherence_percentage INTEGER DEFAULT 100,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (medication_id) REFERENCES medications (id)
        );
        """)
        conn.commit()

if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully.")
