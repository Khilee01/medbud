import cv2
import easyocr
import os

# Initialize the OCR reader (only do this once to avoid loading the model multiple times)
reader = None

def get_reader():
    """
    Initialize and return the EasyOCR reader.
    The function ensures we only initialize the reader once.
    """
    global reader
    if reader is None:
        print("Initializing EasyOCR reader (this may take a moment)...")
        reader = easyocr.Reader(['en'])  # Initialize for English
    return reader

def extract_text(image_path):
    """
    Extract text from the image using EasyOCR.
    Returns the extracted text or None if extraction failed.
    """
    try:
        # Check if the image file exists
        if not os.path.exists(image_path):
            print(f"Error: Image file not found at {image_path}")
            return None
            
        # Read the image
        img = cv2.imread(image_path)
        
        if img is None:
            print(f"Error: Unable to read image at {image_path}")
            return None
        
        # Get the OCR reader
        reader = get_reader()
        
        # Perform OCR
        results = reader.readtext(img)
        
        # Extract text from results
        extracted_text = ' '.join([text for _, text, _ in results])
        
        if extracted_text.strip():
            print("Text extracted successfully:")
            print(extracted_text)
            return extracted_text
        else:
            print("No text could be extracted from the image.")
            return None
            
    except Exception as e:
        print(f"Error during OCR: {e}")
        return None

def extract_medication_name(text):
    """
    Extract potential medication name from OCR text.
    This is a simplified approach - in a real application, 
    you'd need more sophisticated NLP.
    """
    if not text:
        return None
    
    # Split text into words and filter for potential medication names
    words = text.split()
    potential_medication_names = [word for word in words if len(word) > 3]
    
    if not potential_medication_names:
        print("Could not identify medication name from the image.")
        return None
    
    # Use the first potential word as medication name (simplification)
    medication_name = potential_medication_names[0]
    print(f"Identified potential medication name: {medication_name}")
    
    return medication_name