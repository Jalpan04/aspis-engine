import pygame
from runtime.api import Script, Input, KeyCode, Time
import math

class TankController(Script):
    speed = 150.0
    turn_speed = 120.0
    
    def start(self):
        # Find the turret child to rotate it independently
        self.turret = None
        for child in self.game_object.children:
            if child.name == "Turret":
                self.turret = child
                break
    
    def update(self, dt):
        # 1. Move Body (Tank Controls)
        if Input.get_key(KeyCode.W):
            # Move forward in direction of rotation
            # Convert degrees to radians
            # Note: Pygame rotation is counter-clockwise, standard math is usually CCW too.
            # But screen Y is down.
            rad = math.radians(self.transform.rotation)
            
            # If rotation 0 is "Right":
            # x = cos, y = sin
            
            # If rotation 0 is "Up" (which is common for sprites):
            # We might need to adjust. Let's assume 0 is Right for now.
            
            vx = math.cos(rad) * self.speed
            vy = math.sin(rad) * self.speed
            
            self.transform.position[0] += vx * dt
            self.transform.position[1] += vy * dt
            
        if Input.get_key(KeyCode.A):
            self.transform.rotation -= self.turn_speed * dt
        if Input.get_key(KeyCode.S): # Backwards
            rad = math.radians(self.transform.rotation)
            vx = math.cos(rad) * self.speed
            vy = math.sin(rad) * self.speed
            self.transform.position[0] -= vx * dt
            self.transform.position[1] -= vy * dt
            
        if Input.get_key(KeyCode.D): # Right
            self.transform.rotation += self.turn_speed * dt
            
        # 2. Rotate Turret (Aiming)
        if self.turret:
            # S/D to rotate turret maybe? Or Q/E?
            # Let's use Q/E
            pass
            
    def on_collision_enter(self, other):
        print(f"Tank hit {other}")
