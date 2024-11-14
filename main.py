import cv2
from ultralytics import YOLO
import obsws_python as obs
import time
import json

# Load configuration from JSON file
with open("config.json", "r") as config_file:
    config = json.load(config_file)


# Load the YOLO model
model = YOLO("yolo11n.pt")

# Open a connection to the webcam (0 is the default camera, use 1, 2 for other cameras)
cap = cv2.VideoCapture(1)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not access the webcam.")
    exit()

# OBS WebSocket connection details
host = config["host"]
port = config["port"]
password = config["password"]

# Initialize the OBS client
client = obs.ReqClient(host=host, port=port, password=password, timeout=3)

def switch_scenes():
    try:
        # Get the current scene name
        response = client.get_current_program_scene()
        current_scene = response.current_program_scene_name

        # Get the list of all scenes
        scenes_response = client.get_scene_list()
        scenes = [scene['sceneName'] for scene in scenes_response.scenes]

        # Find the index of the current scene
        current_index = scenes.index(current_scene)

        # Determine the next scene in the list
        next_index = (current_index + 1) % len(scenes)
        next_scene = scenes[next_index]

        # Switch to the next scene
        client.set_current_program_scene(next_scene)
        print(f"Switched from '{current_scene}' to '{next_scene}'")

    except Exception as e:
        print("An error occurred:", e)

def main():
    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Failed to grab frame.")
            break

        # Perform object detection on the frame
        results = model(frame)
        
        # Get prediction details
        predictions = results[0].names
        detected_classes = results[0].boxes.cls.tolist()
        
        # Print the detected classes and their predictions
        print("Predictions:", [predictions[cls] for cls in detected_classes])
            
        # Optional: add time delay to slow down the detection process
        time.sleep(0)
        
        # Switch scenes after detecting an object

        switch_scenes()

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

if __name__ == '__main__':
    main()
