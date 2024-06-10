import pygame
from laser import Laser

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, window_width, window_height):
        super().__init__()
        self.window_width = window_width
        self.window_height = window_height
        self.image = pygame.image.load("Img/spaceship.png")
        self.rect = self.image.get_rect(midbottom = (self.window_width/2,self.window_height))
        self.speed = 6
        self.lasers_group = pygame.sprite.Group()
        # Laser shoot time delay variables
        self.laser_ready = True
        self.laser_time = 0
        self.laser_time_delay = 300
    
    def move(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_RIGHT] and self.rect.right < self.window_width:
            self.rect.x += self.speed
        
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed

        if key[pygame.K_SPACE] and self.laser_ready:
             self.laser_ready = False
             laser = Laser(self.rect.center, 5, self.window_height)
             self.lasers_group.add(laser)
             self.laser_time = pygame.time.get_ticks()
    
    def update(self):
        self.move()
        self.lasers_group.update()
        self.recharge_laser()

    # Time delay of the shots
    def recharge_laser(self):
        if not self.laser_ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_time_delay:
                self.laser_ready = True
      