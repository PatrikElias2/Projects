import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self,position, speed, window_height):
        super().__init__()
        self.image = pygame.Surface((4,15)) 
        self.image.fill((243,216,63))
        self.rect = self.image.get_rect(center = position)
        self.speed = speed
        self.window_height = window_height

    def update(self):
        self.rect.y -= self.speed
        # Removing the yellow rectangle (laser) from group when it goes outside of the window
        if self.rect.y > self.window_height + 15 or self.rect.y < 0:
            self.kill