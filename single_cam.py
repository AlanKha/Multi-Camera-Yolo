import cv2
from ultralytics import YOLO

# Load the model
model = YOLO("yolo11n.pt")

# Open a connection to the webcam (0 is the default camera, use 1, 2 for other cameras)
cap = cv2.VideoCapture(1)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not access the webcam.")
    exit()

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Failed to grab frame.")
        break
    
    # Perform object detection on the frame
    results = model(frame)
    
    # Display results on the frame
    frame_with_boxes = results[0].plot()  # Plot detected boxes on the frame
    
    # Show the frame with detections
    cv2.namedWindow("Webcam Object Detection", cv2.WINDOW_NORMAL)  # Make the window resizable
    cv2.imshow("Webcam Object Detection", frame_with_boxes)
    
    # Break the loop if the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
