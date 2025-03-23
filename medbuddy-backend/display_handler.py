import cv2
import numpy as np

def show_medication_info(info):
    """
    Display medication information on screen in a formatted window.
    """
    if not info:
        print("No medication information available to display.")
        return
    
    # Create a blank image to display information
    img = 255 * np.ones((400, 800, 3), dtype=np.uint8)
    
    # Add text to the image
    cv2.putText(img, f"Medication: {info['name']}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img, f"Dosage Information:", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    
    # Split dosage text into multiple lines if it's too long
    dosage_words = info['dosage'].split()
    line = ""
    y_position = 150
    
    for word in dosage_words:
        test_line = line + " " + word if line else word
        if len(test_line) < 50:  # character limit per line
            line = test_line
        else:
            cv2.putText(img, line, (50, y_position), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1)
            y_position += 40
            line = word
    
    # Add the last line
    if line:
        cv2.putText(img, line, (50, y_position), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1)
    
    # Add source information
    cv2.putText(img, f"Source: {info['source']}", (50, y_position + 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1)
    
    # Display the image
    cv2.imshow('Medication Information', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
