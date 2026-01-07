from runtime.api import Script, Time
import random

class Ball(Script):
    speed = 400.0
    
    def start(self):
        self.reset_ball()

    def reset_ball(self):
        self.transform.position = [400, 300]
        
        # Random start direction
        dir_x = 1 if random.random() > 0.5 else -1
        dir_y = random.uniform(-0.5, 0.5)
        
        self.velocity = [dir_x * self.speed, dir_y * self.speed]
        
        # Apply to Rigidbody
        if "RigidBody" in self.game_object.components:
            self.game_object.components["RigidBody"]["velocity"] = self.velocity

    def on_collision_enter(self, other):
        # Bounce!
        # The physics engine handles position resolution (stopping overlap).
        # We need to handle velocity reflection.
        # Simple Logic: Flip X velocity when hitting paddle.
        
        # Check if we hit a paddle
        if "Paddle" in other.name:
            current_vel = self.game_object.components["RigidBody"]["velocity"]
            # Flip X and add a bit of speed
            current_vel[0] *= -1.1 
            # Add some vertical noise based on paddle hit? (skipped for simplicity)
            
            self.game_object.components["RigidBody"]["velocity"] = current_vel
            print("Ball hit paddle!")
            
        elif "Wall" in other.name:
            # Physics engine might stop it, but we want it to bounce.
            # If our engine doesn't have restitution (bounciness), we do it manually.
            current_vel = self.game_object.components["RigidBody"]["velocity"]
            current_vel[1] *= -1
            self.game_object.components["RigidBody"]["velocity"] = current_vel
            print("Ball hit wall!")

    def update(self, dt):
        # Check for scoring (left/right bounds)
        pos = self.transform.position
        if pos[0] < 0:
            print("Player 2 Scored!")
            self.reset_ball()
        elif pos[0] > 800:
            print("Player 1 Scored!")
            self.reset_ball()
