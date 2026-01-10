
import unittest
import sys
import os
import json

# Add root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from shared.scene_schema import Scene, GameObject
from shared.scene_loader import save_scene, load_scene
import uuid

class TestSerialization(unittest.TestCase):
    def test_scene_round_trip(self):
        """Test that data saved to disk is identical when loaded back."""
        # Create Dummy Scene
        # Schema: Scene(metadata, objects, prefabs)
        scene = Scene(metadata={"name": "TestScene", "version": 1}, objects=[], prefabs={})
        
        # Object 1: Complex Components
        obj1 = GameObject(
            id=str(uuid.uuid4()), 
            name="Hero", 
            # Transform is Component in schema, but GameObject constructor allows passing it?
            # Looking at schema.py: GameObject(id, name, active, components)
            # It does NOT take position/rotation/scale args directly in schema.py!
            # Wait, api.py might be different from schema.py?
            # Let's use the schema's GameObject for serialization tests if that's what we are saving.
            # actually save_scene expects a DICT or object that is then dumped.
            # checking save_scene in loader... it dumps scene_data (Dict).
            # So if we pass a Scene object to save_scene, it might fail if save_scene expects a dict.
            # save_scene signature: (scene_data: Dict[str, Any], path: str)
            # So we must convert Scene object to dict first.
        )
        # Manually constructing Component Dict
        from dataclasses import asdict
        scene_dict = asdict(scene)
        
        # Add an object to the dict
        obj_id = str(uuid.uuid4())
        obj_dict = {
            "id": obj_id,
            "name": "Hero",
            "active": True,
            "components": {
                "Transform": {"position": [10, 20], "rotation": 45, "scale": [2, 2]},
                "SpriteRenderer": {"tint": [255, 0, 0, 255], "layer": 5},
                "RigidBody": {"mass": 10.0, "drag": 0.5, "use_gravity": True}
            }
        }
        scene_dict["objects"].append(obj_dict)
        
        # Save
        test_path = "tests/temp_test_scene.json"
        save_scene(scene_dict, test_path)
        
        # Load
        loaded_data = load_scene(test_path)
        
        # Verify
        self.assertEqual(scene_dict["metadata"]["name"], loaded_data["metadata"]["name"])
        self.assertEqual(len(loaded_data["objects"]), 1)
        
        loaded_obj = loaded_data["objects"][0]
        self.assertEqual(loaded_obj["name"], "Hero")
        self.assertEqual(loaded_obj["components"]["RigidBody"]["drag"], 0.5)
        
        # Cleanup
        if os.path.exists(test_path):
            os.remove(test_path)
            
    def test_malformed_json(self):
        """Test loading a broken JSON file."""
        test_path = "tests/broken.json"
        with open(test_path, "w") as f:
            f.write("{ broken json [ }")
            
        with self.assertRaises(json.JSONDecodeError):
            load_scene(test_path)
            
        if os.path.exists(test_path):
            os.remove(test_path)
    
    def test_missing_components(self):
        """Test loading an object with NO components."""
        scene_json = {
            "metadata": {"name": "EmptyObj", "version": 1},
            "objects": [
                {
                    "id": "123",
                    "name": "Ghost",
                    "active": True,
                    "components": {} 
                }
            ]
        }
        test_path = "tests/minimal.json"
        with open(test_path, "w") as f:
            json.dump(scene_json, f)
            
        data = load_scene(test_path)
        self.assertEqual(len(data["objects"]), 1)
        self.assertEqual(data["objects"][0]["name"], "Ghost")
        
        if os.path.exists(test_path):
            os.remove(test_path)

if __name__ == "__main__":
    unittest.main()
