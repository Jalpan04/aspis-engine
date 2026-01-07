from runtime.api import Script

class Rotator(Script):
    def update(self, dt):
        # Rotate 90 degrees per second
        if self.transform:
            self.transform.rotation += 90 * dt
