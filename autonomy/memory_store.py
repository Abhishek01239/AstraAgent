import json
import os

MEMORY_FILE = "discussion_memory.json"

def load_discussion():
    """Load past discussion from file"""

    if not os.path.exists(MEMORY_FILE):
        return []
    
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_discussion(chat_log):
    """Save discussion to file"""   

    with open(MEMORY_FILE, "w") as f:
        json.dump(chat_log, f, indent = 2)
         
    