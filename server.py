from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
import base64

from ocr_processor import extract_text, extract_medication_name
from fda_api import get_medication_info
from database_handler import initialize_database, search_medication, save_form_submission

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/submit_form', methods=['POST'])
def submit_form():
    try:
        data = request.json  # Get JSON data from request

        name = data.get("name")
        age = data.get("age")
        doctor = data.get("doctor")
        medicines = data.get("medicines", [])

        if not name or not age or not doctor or not medicines:
            return jsonify({"error": "Missing required fields"}), 400

        # Save the form submission to the database
        success = save_form_submission(name, age, doctor, medicines)

        if success:
            return jsonify({"message": "Form data saved successfully"}), 201
        else:
            return jsonify({"error": "Failed to save data"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True, host='0.0.0.0', port=3000)
