# Import modules
from webcam_capture import capture_image
from ocr_processor import extract_text, extract_medication_name
from database_handler import initialize_database, search_medication
from fda_api import get_medication_info
from display_handler import show_medication_info

def main():
    """
    Main application flow that coordinates all modules.
    """
    # Initialize the database
    initialize_database()
    
    # Step 1: Capture image from webcam
    print("Starting webcam capture...")
    image_path = capture_image()
    
    if not image_path:
        print("Image capture failed or was cancelled.")
        return
    
    # Step 2: Perform OCR on the captured image
    print("Performing OCR on the captured image...")
    extracted_text = extract_text(image_path)
    
    if not extracted_text:
        print("Please capture a clearer image of the medication label.")
        return
    
    # Step 3: Extract medication name from OCR text
    medication_name = extract_medication_name(extracted_text)
    
    if not medication_name:
        print("Could not identify medication name from the image.")
        return
    
    # Step 4: Check database for medication information
    print(f"Checking database for information on {medication_name}...")
    medication_info = search_medication(medication_name)
    
    # Step 5: If not in database, get information from FDA
    if not medication_info:
        print(f"Getting information from FDA for {medication_name}...")
        medication_info = get_medication_info(medication_name)
    
    # Step 6: Display medication information
    show_medication_info(medication_info)

if __name__ == "__main__":
    main()
