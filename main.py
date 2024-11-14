import cv2
from ultralytics import YOLO
import obsws_python as obs
import time
import json

class YOLOSceneSwitcher:
    def __init__(self, config_path="config.json", model_path="yolo11n.pt", camera_index=1):
        # Load configuration from JSON file
        with open(config_path, "r") as config_file:
            config = json.load(config_file)

        # Initialize attributes for the OBS WebSocket
        self.host = config["host"]
        self.port = config["port"]
        self.password = config["password"]

        # Load the YOLO model
        self.model = YOLO(model_path)

        # Open a connection to the webcam
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise Exception("Error: Could not access the webcam.")

        # Initialize the OBS client
        self.client = obs.ReqClient(host=self.host, port=self.port, password=self.password, timeout=3)

        # Load scenes from OBS once at initialization
        self.scenes = self._get_scenes()
        self.current_scene_index = 0

    def _get_scenes(self):
        """Retrieve the list of scenes from OBS."""
        try:
            scenes_response = self.client.get_scene_list()
            return [scene['sceneName'] for scene in scenes_response.scenes]
        except Exception as e:
            print("Error retrieving scenes:", e)
            return []

    def switch_to_next_scene(self):
        """Switch to the next scene in the list."""
        try:
            # Determine the next scene in the list
            self.current_scene_index = (self.current_scene_index + 1) % len(self.scenes)
            next_scene = self.scenes[self.current_scene_index]

            # Switch to the next scene
            self.client.set_current_program_scene(next_scene)
            print(f"Switched to '{next_scene}'")
        except Exception as e:
            print("An error occurred while switching scenes:", e)

    def detect_and_switch_scene(self):
        """Main loop for detecting objects and switching scenes."""
        while True:
            # Read a frame from the webcam
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Failed to grab frame.")
                break

            # Perform object detection on the frame
            results = self.model(frame)

            # Get prediction details
            predictions = results[0].names
            detected_classes = results[0].boxes.cls.tolist()

            # Print the detected classes
            print("Predictions:", [predictions[cls] for cls in detected_classes])

            # Switch scenes based on detection
            self.switch_to_next_scene()

            # Display results on the frame
            frame_with_boxes = results[0].plot()  # Plot detected boxes on the frame
            
            # Show the frame with detections
            cv2.namedWindow("Webcam Object Detection", cv2.WINDOW_NORMAL)  # Make the window resizable
            cv2.imshow("Webcam Object Detection", frame_with_boxes)

            # Break the loop if the user presses 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Optional delay to control processing speed
            time.sleep(0)

    def release_resources(self):
        """Release resources."""
        self.cap.release()
        cv2.destroyAllWindows()

# Usage
if __name__ == '__main__':
    switcher = YOLOSceneSwitcher()
    try:
        switcher.detect_and_switch_scene()
    finally:
        switcher.release_resources()
