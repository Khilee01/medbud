import sqlite3
import os

# Database file path
DB_PATH = 'medicine_reminder.db'

def initialize_database():
    """Initialize the database with required tables if they don't exist."""
    # This function can be removed or kept as a placeholder if you want to check for existing tables.
    print("Database initialization is not required as tables are assumed to exist.")
    return True

def submit_form_data(form_data):
    """
    Submit form data to the database.
    
    Args:
        form_data (dict): Dictionary containing form submission details
    
    Returns:
        tuple: (success_boolean, message)
    """
    try:
        # Establish database connection
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Start a transaction
        conn.execute('BEGIN')

        # Insert or get doctor ID
        cursor.execute('''
            INSERT OR IGNORE INTO doctors (name) 
            VALUES (?)
        ''', (form_data['doctor'],))
        cursor.execute('SELECT doctor_id FROM doctors WHERE name = ?', (form_data['doctor'],))
        doctor_id = cursor.fetchone()[0]

        # Insert user information
        cursor.execute('''
            INSERT INTO users (name, age) 
            VALUES (?, ?)
        ''', (form_data['name'], form_data['age']))
        
        # Get the last inserted user ID
        user_id = cursor.lastrowid

        # Process medicines and prescriptions
        for med in form_data['medicines']:
            # First, insert or get the medicine ID
            cursor.execute('''
                INSERT OR IGNORE INTO medicines (name) 
                VALUES (?)
            ''', (med['name'],))
            
            # Get the medicine ID (either newly inserted or existing)
            cursor.execute('SELECT medicine_id FROM medicines WHERE name = ?', (med['name'],))
            medicine_id = cursor.fetchone()[0]

            # Insert prescription
            cursor.execute('''
                INSERT INTO prescriptions (user_id, doctor_id, medicine_id, doses_per_day) 
                VALUES (?, ?, ?, ?)
            ''', (user_id, doctor_id, medicine_id, med['doses']))
            
            # Get the last inserted prescription ID
            prescription_id = cursor.lastrowid

            # Insert dosage times
            for time in med['times']:
                cursor.execute('''
                    INSERT INTO dosage_times (prescription_id, time_of_day) 
                    VALUES (?, ?)
                ''', (prescription_id, time))

        # Commit the transaction
        conn.commit()
        conn.close()

        return True, "Form data saved successfully"

    except sqlite3.Error as e:
        # Rollback in case of error
        conn.rollback()
        print(f"Database error: {e}")
        return False, f"Database error: {str(e)}"

    except Exception as e:
        # Rollback in case of any other error
        conn.rollback()
        print(f"Error saving form data: {e}")
        return False, f"Error saving form data: {str(e)}"

def search_medication(medication_name):
    """Search for medication information in the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Search for medication by name (case insensitive)
        cursor.execute("SELECT name FROM medicines WHERE LOWER(name) = LOWER(?)", (medication_name,))
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            return {
                'name': result[0],
                'source': 'Local Database'
            }
        else:
            print(f"No information found for '{medication_name}' in local database.")
            return None
            
    except Exception as e:
        print(f"Database search error: {e}")
        return None