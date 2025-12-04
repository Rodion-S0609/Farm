import json
import os
import time

SAVE_FILE = "farm_save.json"

def save_game(state):
    """Save the current game state to a JSON file."""
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=4)

def load_game():
    """Load game state from file OR return default state."""
    if not os.path.exists(SAVE_FILE):
        return None
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_timestamp():
    """Returns current time for timer calculations."""
    return int(time.time() * 1000)

