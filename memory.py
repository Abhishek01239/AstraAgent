import json
import os

MEMORY_FILE = "memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []

    try:
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
    except Exception:
        return []

    if not isinstance(data, list):
        return []

    clean = []
    for item in data:
        if isinstance(item, dict) and "role" in item and "content" in item:
            clean.append(item)

    return clean

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)
