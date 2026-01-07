from runtime.api import Script, Input
import pygame

class PlayerController(Script):
    def update(self, dt):
        speed = 200 * dt
        
        move_x = 0
        move_y = 0
        
        if Input.get_key(pygame.K_w):
            move_y -= speed
        if Input.get_key(pygame.K_s):
            move_y += speed
        if Input.get_key(pygame.K_a):
            move_x -= speed
        if Input.get_key(pygame.K_d):
            move_x += speed
            
        if self.transform:
            self.transform.position[0] += move_x
            self.transform.position[1] += move_y
