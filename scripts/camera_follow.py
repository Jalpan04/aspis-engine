from runtime.api import Script, Time

class CameraFollow(Script):
    """
    Generic Camera Follow script.
    
    Properties:
    - target_name: Name of the GameObject to follow.
    - smooth_speed: Speed of interpolation (0.0 to 1.0).
    - offset_x: X offset from target.
    - offset_y: Y offset from target.
    """
    target_name = "Player"
    smooth_speed = 5.0
    offset_x = 0.0
    offset_y = 0.0
    
    def start(self):
        self.target = self.find_object(self.target_name)
        if not self.target:
            print(f"CameraFollow: Could not find target '{self.target_name}'")

    def update(self, dt):
        if not self.target:
            # Try finding it again (maybe spawned late)
            self.target = self.find_object(self.target_name)
            if not self.target: return
        
        # Current position
        cx, cy = self.game_object.position
        
        # Target position
        tx, ty = self.target.world_position
        tx += self.offset_x
        ty += self.offset_y
        
        # Smooth interpolation (Lerp)
        # new = current + (target - current) * speed * dt
        
        dx = tx - cx
        dy = ty - cy
        
        if abs(dx) > 0.1 or abs(dy) > 0.1:
            self.game_object.position[0] += dx * self.smooth_speed * dt
            self.game_object.position[1] += dy * self.smooth_speed * dt
