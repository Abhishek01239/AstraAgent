import json
import os

MEMORY_FILE = "memory.json"
MAX_SHORT_MEMORY = 6
conversation_memory = []

def add_to_memory(role, content):
    conversation_memory.append({
        "role": role,
        "content": content
    })

    if len(conversation_memory) >MAX_SHORT_MEMORY:
        conversation_memory(0)
    
def get_memory():
    return conversation_memory

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []

    try:
        with open(MEMORY_FILE,"r") as f:
            return json.load(f)
    except:
        return []

def save_memory(memory):
    with open(MEMORY_FILE,"w") as f:
        json.dump(memory, f, indent = 2)