import pygame
from playerspaceship import Spaceship

# Init
pygame.init()

# Window
WIDTH = 750
HEIGHT = 700
window = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Invaders")

# Game setting
fps = 60
clock = pygame.time.Clock()

# Colors
bg_color = (0,0,0)

spaceship = Spaceship(WIDTH,HEIGHT)
spaceship_group = pygame.sprite.GroupSingle()
spaceship_group.add(spaceship)

# Main loop
run = True
while run:
    
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    spaceship_group.update()

    window.fill(bg_color)
    spaceship_group.draw(window)

    pygame.display.update()
    clock.tick(fps)

pygame.quit()