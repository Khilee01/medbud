import sqlite3

# Connect to the database
conn = sqlite3.connect("medbuddy.db")
cursor = conn.cursor()

# Insert a reminder
cursor.execute("""
    INSERT INTO reminders (user_id, medication_id, reminder_time, status) 
    VALUES (1, 2, '2025-03-27 20:51:55', 'pending');
""")

# Commit and close
conn.commit()
conn.close()

print("✅ Reminder added successfully!")
