
import unittest
import sys
import os
import shutil

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from runtime.api import Script, GameObject

class TestScripting(unittest.TestCase):
    def setUp(self):
        # Create a temp script folder
        self.script_dir = os.path.join(PROJECT_ROOT, "tests", "scripts")
        if not os.path.exists(self.script_dir):
            os.makedirs(self.script_dir)
            
        sys.path.append(self.script_dir) # Allow importing from here
        
    def tearDown(self):
        if os.path.exists(self.script_dir):
            shutil.rmtree(self.script_dir)
        sys.path.remove(self.script_dir)
            
    def test_missing_script(self):
        """Test loading a script that does not exist."""
        obj = GameObject("test", "Test", [0,0], 0, [1,1])
        # Script class usually instantiated by Runtime using importlib
        # Here we mock the behavior of Script Component
        
        script_name = "NonExistentScript"
        # The runtime `init_script` tries to import `scripts.{script_name}`
        # We need to test the IMPORT logic, which is in game_loop or api? 
        # Actually logic is in game_loop.start_scripts
        
        # Since we can't easily spin up GameLoop here, we test importlib behavior
        import importlib.util
        spec = importlib.util.find_spec(f"scripts.{script_name}")
        self.assertIsNone(spec, "Should not find non-existent script")
        
    def test_syntax_error_script(self):
        """Test import behavior on broken script."""
        script_name = "BrokenScript"
        path = os.path.join(self.script_dir, f"{script_name}.py")
        with open(path, "w") as f:
            f.write("class BrokenScript\n    pass") # Missing colon
            
        # We simulate what game_loop does
        try:
            # We must trick python to look in tests/scripts as if it were root/scripts?
            # Or just import directly from path
            import importlib.util
            spec = importlib.util.spec_from_file_location(script_name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.fail("Should have raised SyntaxError")
        except SyntaxError:
            pass # Success
        except Exception as e:
            self.fail(f"Raised wrong exception: {e}")

if __name__ == "__main__":
    unittest.main()
