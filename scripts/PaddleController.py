from runtime.api import Script
import pygame

class PaddleController(Script):
    speed = 300.0
    up_key = "w"
    down_key = "s"

    def start(self):
        print(f"Paddle initialized on {self.game_object.name}")

    def update(self, dt):
        movement = 0.0
        
        # Check keys (Input._keys is a list of booleans from pygame.key.get_pressed())
        # We need a better Input API in the future, but for now we access raw pygame keys if needed,
        # or just rely on simplistic string checks if mapped.
        # But wait, Input global in API is not fully fleshed out with key mapping.
        # Let's inspect Input class or just use pygame directly since we import it.
        
        keys = pygame.key.get_pressed()
        
        up_k = getattr(pygame, f"K_{self.up_key}", pygame.K_w)
        down_k = getattr(pygame, f"K_{self.down_key}", pygame.K_s)

        if keys[up_k]:
            movement = -1.0
        elif keys[down_k]:
            movement = 1.0

        # Move via Transform
        # We also need to update velocity for physics, but paddles are "Kinematic" (infinite mass/force)
        # For our simple engine, we can just teleport them (transform position) or set velocity.
        # Setting velocity is better for physics interactions if we had friction, but teleport is fine here.
        
        pos = self.transform.position
        pos[1] += movement * self.speed * dt
        
        # Clamp to screen (approximate)
        if pos[1] < 50:
            pos[1] = 50
        if pos[1] > 550:
            pos[1] = 550
