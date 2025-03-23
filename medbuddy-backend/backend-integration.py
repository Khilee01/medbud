from flask import Flask, request, jsonify
import os
from flask_cors import CORS
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import tempfile

# Import your existing modules
from ocr_processor import extract_text, extract_medication_name
from database_handler import initialize_database, search_medication
from fda_api import get_medication_info

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the database on startup
initialize_database()

@app.route('/upload', methods=['POST'])
def upload_image():
    """
    Endpoint to receive image uploads from the frontend,
    process them, and return medication information.
    """
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
        
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
        
    try:
        # Create a temporary file to store the uploaded image
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp:
            temp_filename = temp.name
            file.save(temp_filename)
        
        # Process the image with OCR to extract text
        extracted_text = extract_text(temp_filename)
        
        # Clean up the temporary file
        os.unlink(temp_filename)
        
        if not extracted_text:
            return jsonify({
                'error': 'Could not extract text from image', 
                'message': 'Please take a clearer photo of the medication label'
            }), 400
            
        # Extract the medication name from the OCR text
        medication_name = extract_medication_name(extracted_text)
        
        if not medication_name:
            return jsonify({
                'error': 'Could not identify medication',
                'message': 'Unable to identify medication from the image'
            }), 400
            
        # Search for medication information in local database
        medication_info = search_medication(medication_name)
        
        # If not found in database, you can implement fallback to FDA API
        # For demo purposes, providing a generic response if not found
        if not medication_info:
            # You would normally call get_medication_info(medication_name) here
            # For now, return a placeholder response
            return jsonify({
                'medicine': medication_name,
                'description': 'Information not found in database. In a complete implementation, this would fetch data from FDA API.',
                'dosage': 'Unknown',
                'uses': 'Unknown',
                'side_effects': 'Unknown',
                'warnings': 'Consult with your healthcare provider for accurate information.'
            })
        
        # Format the response for the frontend
        return jsonify({
            'medicine': medication_info['name'],
            'description': medication_info['dosage'],
            'source': medication_info['source']
        })
        
    except Exception as e:
        return jsonify({'error': 'Server error', 'message': str(e)}), 500

# Define the FDA API simulation (stub) function if not already implemented
def get_medication_info(medication_name):
    """
    Stub function for FDA API integration.
    This would be replaced with actual API calls in production.
    """
    # In a real implementation, this would make API calls
    # For now, just return a simple placeholder
    return {
        'name': medication_name,
        'dosage': f'Generic information for {medication_name}. Please consult your doctor.',
        'source': 'FDA API simulation'
    }

if __name__ == '__main__':
    app.run(debug=True, port=5000)
