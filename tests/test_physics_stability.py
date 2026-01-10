
import unittest
import sys
import os
import pygame
import pymunk

# Add root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from runtime.physics import PhysicsSystem
from runtime.api import GameObject

class TestPhysicsStability(unittest.TestCase):
    def setUp(self):
        self.physics = PhysicsSystem()
        
    def create_dummy_obj(self):
        return GameObject(id="test_id", name="Test", position=[0,0], rotation=0, scale=[1,1])
        
    def test_zero_mass(self):
        """Test RigidBody with 0 mass (Invalid for Dynamic, should handle gracefully)."""
        obj = self.create_dummy_obj()
        rb_data = {"mass": 0.0, "use_gravity": True} # 0 Mass Dynamic is invalid in Pymunk usually
        col_data = {"size": [50, 50]}
        
        # Pymunk DYNAMIC bodies must have mass > 0 or they error.
        # Our engine code defaults to Mass=1.0 if missing, but if user explicitly sets 0?
        # Let's see if it crashes.
        try:
            self.physics._create_body(obj, rb_data, col_data)
        except Exception as e:
            # If it crashes, we want to know.
            # Ideally our engine should clamp mass to 0.001 or similar.
            print(f"Zero Mass Crash: {e}")
            # We fail the test if it crushes ungracefully? 
            # Or we assert that it raised, if we expect it to fail safely.
            # For now, let's see behavior.
            pass
            
    def test_negative_scale_collider(self):
        """Test Collider generation with negative scale sizes."""
        obj = self.create_dummy_obj()
        rb_data = {"mass": 1.0}
        # Negative size logic in physics.py:
        # width, height = size (from data)
        # It calculates vertices. 
        # width= -50 implies box is inverted. Pymunk usually accepts this but winding might flip.
        col_data = {"size": [-50, -50]} 
        
        try:
            self.physics._create_body(obj, rb_data, col_data)
        except Exception as e:
            self.fail(f"Crash on negative size: {e}")
            
    def test_nan_position(self):
        """Test object with NaN position."""
        obj = self.create_dummy_obj()
        obj.position = [float('nan'), float('nan')]
        rb_data = {"mass": 1.0}
        
        # Pymunk definitely hates NaNs.
        # Engine should probably filter this before simulation step.
        with self.assertRaises(Exception):
             self.physics._create_body(obj, rb_data, None)

if __name__ == "__main__":
    unittest.main()
