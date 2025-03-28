import time
import sqlite3
from datetime import datetime
from win10toast import ToastNotifier

toaster = ToastNotifier()
def show_notification(title, message):
    toaster.show_toast(title, message, duration=10)


# Function to fetch reminders
def get_due_reminders():
    conn = sqlite3.connect("medbuddy.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")  # Match format
    cur.execute("SELECT * FROM reminders WHERE reminder_time = ?", (current_time,))
    reminders = cur.fetchall()
    conn.close()
    
    return reminders

# Function to show notifications
def show_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name="MedBuddy",
        timeout=10  # Notification lasts for 10 seconds
    )

# Main loop to check for reminders every minute
while True:
    due_reminders = get_due_reminders()
    
    for reminder in due_reminders:
        user_id = reminder["user_id"]
        medication_id = reminder["medication_id"]
        reminder_time = reminder["reminder_time"]

        # Notification Message
        title = f"Medication Reminder"
        message = f"User {user_id}, take your medicine (ID: {medication_id}) at {reminder_time}"
        
        show_notification(title, message)
    
    time.sleep(60)  # Check every minute
