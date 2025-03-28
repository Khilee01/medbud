import time
from win10toast import ToastNotifier

def show_notification():
    """Display notification and ask user if they took the medicine"""
    toaster = ToastNotifier()
    notification_text = "It's time to take your medicine!"
    
    # Show Windows notification
    toaster.show_toast("Medicine Reminder", notification_text, duration=5)
    
    # Ask user for confirmation
    while True:
        user_input = input("Did you take the medicine? (yes/no): ").strip().lower()
        if user_input in ["yes", "no"]:
            break
        print("Invalid input. Please type 'yes' or 'no'.")

    if user_input == "yes":
        print("Okay, will remind you for your next dose✅")
    else:
        print("okay i'll remind you in 10 mins")

if __name__ == "__main__":
    show_notification()
