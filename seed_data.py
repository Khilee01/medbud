import sqlite3

conn = sqlite3.connect("medbuddy.db")
cursor = conn.cursor()

# Insert sample users
cursor.execute("INSERT INTO users (name, email, phone) VALUES ('John Doe', 'john@example.com', '9876543210')")

# Insert sample medications
cursor.execute("INSERT INTO medications (user_id, name, dosage, frequency, start_date, end_date) VALUES (1, 'Paracetamol', '500mg', 'Twice a day', '2025-03-01', '2025-03-10')")

# Insert sample reminders
cursor.execute("INSERT INTO reminders (user_id, medication_id, reminder_time) VALUES (1, 1, '2025-03-01 08:00:00')")

conn.commit()
conn.close()
print("✅ Sample data inserted successfully!")
