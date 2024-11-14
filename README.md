# Multi-Camera-Yolo

Python script that uses yolo and obs web socket to constantly make predictions on rotating scenes.

# Requirements

- Python 3.10+
- OBS Studio version 28
- Ultralytics
- opencv-python

Using these dependencies, I was able to make a script, [main.py](https://github.com/AlanKha/Multi-Camera-Yolo/blob/main/main.py), that rotates through each scene, makes a prediction, and prints it to the terminal.

Also worth noting: for optimal performance, set OBS's 'Scene Transition' to Cut. By default, it is set to fade which hinders visibility in the short frame given to YOLO.

# Usage:

1. Enable WenSocketServer by going to tools -> WenSocketServer Settings -> Plugin Settings -> Enable WenSocket server
2. In that same window, set up the server port and password in the Server Settings section.
3. Adjust ```config.json``` to reflect the port and password from step 2
4. Set Scene Transitions to Cut to avoid any effects from hindering YOLO's performance
5. Make the scenes
6. Start an OBS Virtual Camera
   - Note: You may need to adjust the camera index in ```main.py``` depending on the number of cameras you have plugged into your computer.
8. run main.py to start the script
