import os
from typing import List, Dict, Any
from shared.component_defs import COMPONENT_SPRITE_RENDERER, COMPONENT_SCRIPT

def validate_scene(scene_data: Dict[str, Any], project_root: str) -> List[str]:
    """
    Validates the scene data.
    Returns a list of error messages. Empty list means valid.
    """
    errors = []
    
    # Check structure
    if "objects" not in scene_data:
        errors.append("Scene missing 'objects' list.")
        return errors

    objects = scene_data.get("objects", [])
    seen_ids = set()

    for obj in objects:
        # Check ID
        obj_id = obj.get("id")
        if not obj_id:
            errors.append(f"Object missing ID: {obj.get('name', 'Unknown')}")
        elif obj_id in seen_ids:
            errors.append(f"Duplicate Object ID found: {obj_id} on '{obj.get('name')}'")
        else:
            seen_ids.add(obj_id)

        # Check Components
        components = obj.get("components", {})
        
        # SpriteRenderer Validation
        if COMPONENT_SPRITE_RENDERER in components:
            comp = components[COMPONENT_SPRITE_RENDERER]
            path = comp.get("sprite_path")
            if path:
                # Resolve path relative to valid asset dirs or project root
                # Assuming path is relative to 'assets' or absolute
                # The user said "Assets referenced by relative path"
                # Let's assume relative to project_root
                full_path = os.path.join(project_root, path)
                if not os.path.exists(full_path):
                    errors.append(f"Missing sprite asset: '{path}' in object '{obj.get('name')}'")

        # Script Validation
        if COMPONENT_SCRIPT in components:
            comp = components[COMPONENT_SCRIPT]
            path = comp.get("script_path")
            if path:
                full_path = os.path.join(project_root, path)
                if not os.path.exists(full_path):
                    errors.append(f"Missing script file: '{path}' in object '{obj.get('name')}'")

    return errors
