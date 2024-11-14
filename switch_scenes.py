import obsws_python as obs
import time
import json

# Load configuration from JSON file
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Connection info
host = config["host"]
port = config["port"]
password = config["password"]

# Initialize the client
client = obs.ReqClient(host=host, port=port, password=password, timeout=3)
def switch_scenes():
    try:
        # Get the current scene name from the dataclass response
        response = client.get_current_program_scene()
        current_scene = response.current_program_scene_name  # Accessing as an attribute

        # Get the list of all scenes
        scenes_response = client.get_scene_list()
        scenes = [scene['sceneName'] for scene in scenes_response.scenes]

        # Find the index of the current scene
        try:
            current_index = scenes.index(current_scene)
        except ValueError:
            print(f"The current scene '{current_scene}' is not in the list of scenes.")
            return

        # Determine the next scene in the list
        next_index = (current_index + 1) % len(scenes)
        next_scene = scenes[next_index]

        # Switch to the next scene
        client.set_current_program_scene(next_scene)
        print(f"Switched from '{current_scene}' to '{next_scene}'")

    except Exception as e:
        print("An error occurred:", e)

if __name__ == '__main__':
    while True:
        switch_scenes()
        time.sleep(2)
