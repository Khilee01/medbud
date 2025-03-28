from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Database connection function
def get_db_connection():
    conn = sqlite3.connect("medbuddy.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# Homepage Route (GUI)
@app.route('/')
def home():
    conn = get_db_connection()
    reminders = conn.execute("SELECT * FROM reminders").fetchall()
    conn.close()
    return render_template("index.html", reminders=reminders)

# Fetch all reminders (API)
@app.route("/reminders", methods=["GET"])
def get_reminders():
    conn = get_db_connection()
    reminders = conn.execute("SELECT * FROM reminders").fetchall()
    conn.close()
    return jsonify([dict(row) for row in reminders])

# Add a new reminder (API)
@app.route("/reminders", methods=["POST"])
def add_reminder():
    data = request.json
    conn = get_db_connection()
    conn.execute("INSERT INTO reminders (user_id, medication_id, reminder_time) VALUES (?, ?, ?)",
                 (data["user_id"], data["medication_id"], data["reminder_time"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Reminder added successfully!"}), 201

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)
