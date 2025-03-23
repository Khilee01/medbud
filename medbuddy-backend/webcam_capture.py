import cv2
import time

def capture_image():
    """
    Initialize webcam and capture an image when SPACE is pressed.
    Returns the path to the saved image or None if cancelled.
    """
    # Initialize webcam
    cap = cv2.VideoCapture(0)  # 0 is usually the default webcam
    
    # Check if webcam is opened successfully
    if not cap.isOpened():
        print("Error opening webcam")
        return None
    
    print("Webcam initialized. Press SPACE to capture an image or ESC to quit.")
    
    while True:
        # Read frame from webcam
        ret, frame = cap.read()
        
        # Check if frame is read correctly
        if not ret:
            print("Error reading frame from webcam")
            break
        
        # Display the frame
        cv2.imshow('Webcam Capture', frame)
        
        # Check for key press
        key = cv2.waitKey(1)
        
        # If ESC key is pressed, exit
        if key == 27:  # ESC key
            break
        
        # If SPACE key is pressed, capture the image
        if key == 32:  # SPACE key
            # Save the captured image
            filename = f"captured_image_{int(time.time())}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Image captured and saved as {filename}")
            
            # Release the webcam and close windows
            cap.release()
            cv2.destroyAllWindows()
            
            return filename
    
    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()
    return None
