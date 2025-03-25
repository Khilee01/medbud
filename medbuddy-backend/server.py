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

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        # Get form data from request
        form_data = request.json
        
        # Validate required fields
        required_fields = ['name', 'age', 'doctor', 'medicines']
        for field in required_fields:
            if field not in form_data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Initialize database
        initialize_database()
        
        # Submit form data
        success, message = submit_form_data(form_data)
        
        if success:
            return jsonify({'message': 'Form submitted successfully'}), 200
        else:
            return jsonify({'error': message}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        # Check if image was sent as base64
        if 'image_data' in request.json:
            # Get base64 string
            image_data = request.json['image_data']
            
            # Remove header if present
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            # Decode base64 to binary
            image_binary = base64.b64decode(image_data)
            
            # Save to temp file
            fd, temp_path = tempfile.mkstemp(suffix='.jpg')
            with os.fdopen(fd, 'wb') as f:
                f.write(image_binary)
        
        # Check if image was sent as form data
        elif 'image' in request.files:
            image_file = request.files['image']
            # Save to temp file
            fd, temp_path = tempfile.mkstemp(suffix='.jpg')
            with os.fdopen(fd, 'wb') as f:
                f.write(image_file.read())
        else:
            return jsonify({'error': 'No image data received'}), 400

        # Initialize database
        initialize_database()
        
        # Perform OCR on the image
        extracted_text = extract_text(temp_path)
        
        # Clean up the temp file
        os.unlink(temp_path)
        
        if not extracted_text:
            return jsonify({
                'error': 'Could not extract text from image',
                'message': 'Please capture a clearer image of the medication label.'
            }), 400
        
        # Extract medication name
        medication_name = extract_medication_name(extracted_text)
        
        if not medication_name:
            return jsonify({
                'error': 'Could not identify medication name',
                'message': 'Could not identify medication name from the image.'
            }), 400
        
        # Check database for medication information
        medication_info = search_medication(medication_name)
        
        # If not in database, get information from FDA
        if not medication_info:
            medication_info = get_medication_info(medication_name)
        
        if not medication_info:
            return jsonify({
                'medicine': medication_name,
                'description': 'No detailed information available for this medication.'
            })
        
        # Format response
        response = {
            'medicine': medication_info.get('name', medication_name),
            'description': medication_info.get('dosage', 'No description available'),
            'source': medication_info.get('source', 'Unknown'),
            'uses': medication_info.get('uses', 'No uses specified'),
            'side_effects': medication_info.get('side_effects', 'No side effects noted'),
            'warnings': medication_info.get('warnings', 'No specific warnings')
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Add a simple health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)