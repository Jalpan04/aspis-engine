import json
import os
from typing import Dict, Any

def save_scene(scene_data: Dict[str, Any], path: str):
    """Saves scene data dictionary to a JSON file."""
    try:
        with open(path, 'w') as f:
            json.dump(scene_data, f, indent=2)
    except Exception as e:
        print(f"Error saving scene to {path}: {e}")
        raise

def load_scene(path: str) -> Dict[str, Any]:
    """Loads scene data from a JSON file."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Scene file not found: {path}")
    
    try:
        with open(path, 'r') as f:
            data = json.load(f)
            return data
    except Exception as e:
        print(f"Error loading scene from {path}: {e}")
        raise
