from flask import Flask, request, jsonify
from database import get_db_connection


app = Flask(__name__)

@app.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, phone) VALUES (?, ?, ?)", 
                       (data["name"], data["email"], data["phone"]))
        conn.commit()
    return jsonify({"message": "User added successfully"}), 201

@app.route("/medications", methods=["POST"])
def add_medication():
    data = request.get_json()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO medications 
            (user_id, name, dosage, frequency, start_date, end_date, quantity, low_stock_alert) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (data["user_id"], data["name"], data["dosage"], data["frequency"], 
             data["start_date"], data["end_date"], data.get("quantity", 0), data.get("low_stock_alert", 5)))
        conn.commit()
    return jsonify({"message": "Medication added successfully"}), 201

@app.route("/reminders", methods=["POST"])
def add_reminder():
    data = request.get_json()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO reminders 
            (user_id, medication_id, reminder_time) 
            VALUES (?, ?, ?)""",
            (data["user_id"], data["medication_id"], data["reminder_time"]))
        conn.commit()
    return jsonify({"message": "Reminder added successfully"}), 201

if __name__ == "__main__":
    app.run(debug=True)
