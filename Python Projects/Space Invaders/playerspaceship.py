from typing import Any
import pygame

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, window_width, window_height):
        super().__init__()
        self.window_width = window_width
        self.window_height = window_height
        self.image = pygame.image.load("Img/spaceship.png")
        self.rect = self.image.get_rect(midbottom = (self.window_width/2,self.window_height))
        self.speed = 6
    
    def move(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_RIGHT] and self.rect.right < self.window_width:
            self.rect.x += self.speed
        
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed

    
    def update(self):
        self.move()
      