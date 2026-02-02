import json
import os

MEMORY_FILE = "memory.json"
MAX_MEMORY = 6

# Load memory at startup
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
        if (
            isinstance(item, dict)
            and "role" in item
            and "content" in item
            and isinstance(item["content"], str)
        ):
            clean.append(item)

    return clean[:MAX_MEMORY]


# Global in-memory state
conversation_memory = load_memory()


def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(conversation_memory, f, indent=2)


def add_to_memory(role, content):
    conversation_memory.append({
        "role": role,
        "content": content
    })

    if len(conversation_memory) > MAX_MEMORY:
        conversation_memory.pop(0)

    save_memory()


def get_memory():
    return conversation_memory
