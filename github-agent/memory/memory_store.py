# Simple self-learning memory (local JSON storage)
import json
import os

MEMORY_FILE = "memory/store.json"

def save_memory(data):
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            current = json.load(f)
    else:
        current = []

    current.append(data)

    with open(MEMORY_FILE, "w") as f:
        json.dump(current, f, indent=2)
