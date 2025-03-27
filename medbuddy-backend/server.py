from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
import base64
import re

# Import our custom modules
from ocr_processor import extract_text, extract_medication_name
from fda_api import get_medication_info
from database_handler import initialize_database, submit_form_data, search_medication
from dosage_tracker import DosageTracker  # Import the new DosageTracker class

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Add a health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """
    Simple health check endpoint to verify the server is running.
    """
    return jsonify({
        'status': 'healthy',
        'message': 'Backend service is running successfully'
    }), 200

@app.route('/upload', methods=['POST'])
def upload_image():
    """
    Endpoint to receive image uploads from the frontend,
    process them, and return medication information.
    """
    try:
        # Get image data from the request
        data = request.json
        if not data or 'image_data' not in data:
            return jsonify({'error': 'No image data provided'}), 400
        
        # Extract base64 data if full data URL is provided
        image_data = data['image_data']
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]
        
        # Create a temporary file to store the uploaded image
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp:
            temp.write(base64.b64decode(image_data))
            temp_filename = temp.name
        
        try:
            # Process the image with OCR to extract text
            extracted_text = extract_text(temp_filename)
            
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
            
            # If not found in database, fallback to FDA API simulation
            if not medication_info:
                medication_info = get_medication_info(medication_name)
            
            # Format the response for the frontend
            return jsonify({
                'medicine': medication_info.get('name', medication_name),
                'description': medication_info.get('dosage', 'No dosage information available'),
                'source': medication_info.get('source', 'Unknown'),
                'uses': medication_info.get('uses', 'No uses information available'),
                'side_effects': medication_info.get('side_effects', 'No side effects information available'),
                'warnings': medication_info.get('warnings', 'No warnings available')
            })
        
        finally:
            # Clean up the temporary file
            os.unlink(temp_filename)
        
    except Exception as e:
        return jsonify({'error': 'Server error', 'message': str(e)}), 500

@app.route('/submit-form', methods=['POST'])
def submit_form():
    """
    Endpoint to submit user medication form data.
    """
    try:
        # Get form data from the request
        form_data = request.json
        
        # Validate required fields
        if not form_data:
            return jsonify({
                'error': 'No form data provided',
                'message': 'Please provide complete form information'
            }), 400
        
        # Submit form data to database
        success, message = submit_form_data(form_data)
        
        if success:
            return jsonify({
                'status': 'success',
                'message': message
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': message
            }), 400
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/track-dosage', methods=['POST'])
def track_dosage():
    """
    Endpoint to track medication dosage for a user.
    
    Expected JSON payload:
    {
        "user_name": "John Doe",
        "medicine_name": "Aspirin"
    }
    """
    try:
        # Get data from request
        data = request.json
        
        # Validate required fields
        if not data or 'user_name' not in data or 'medicine_name' not in data:
            return jsonify({
                'error': 'Missing required fields',
                'message': 'Please provide user_name and medicine_name'
            }), 400
        
        # Create DosageTracker instance
        tracker = DosageTracker(data['user_name'], data['medicine_name'])
        
        # Track dosage
        tracking_result = tracker.track_dosage()
        
        # Return tracking result
        return jsonify(tracking_result)
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/medication-details', methods=['POST'])
def get_medication_details():
    """
    Endpoint to retrieve medication details for a user.
    
    Expected JSON payload:
    {
        "user_name": "John Doe",
        "medicine_name": "Aspirin"
    }
    """
    try:
        # Get data from request
        data = request.json
        
        # Validate required fields
        if not data or 'user_name' not in data or 'medicine_name' not in data:
            return jsonify({
                'error': 'Missing required fields',
                'message': 'Please provide user_name and medicine_name'
            }), 400
        
        # Create DosageTracker instance
        tracker = DosageTracker(data['user_name'], data['medicine_name'])
        
        # Get medication details
        details = tracker.get_medication_details()
        
        if details is None:
            return jsonify({
                'status': 'not_found',
                'message': 'No medication details found for the given user and medicine'
            }), 404
        
        return jsonify({
            'status': 'success',
            'details': details
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/dose-history', methods=['POST'])
def get_dose_history():
    """
    Endpoint to retrieve dose history for a user's medication.
    
    Expected JSON payload:
    {
        "user_name": "John Doe",
        "medicine_name": "Aspirin",
        "days": 7  # Optional, defaults to 7 if not provided
    }
    """
    try:
        # Get data from request
        data = request.json
        
        # Validate required fields
        if not data or 'user_name' not in data or 'medicine_name' not in data:
            return jsonify({
                'error': 'Missing required fields',
                'message': 'Please provide user_name and medicine_name'
            }), 400
        
        # Create DosageTracker instance
        tracker = DosageTracker(data['user_name'], data['medicine_name'])
        
        # Get number of days (default to 7 if not provided)
        days = data.get('days', 7)
        
        # Get dose history
        history = tracker.get_dose_history(days)
        
        return jsonify({
            'status': 'success',
            'history': history
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    # Initialize database on startup
    initialize_database()
    
    # Run the Flask application
    app.run(debug=True, host='0.0.0.0', port=5000)