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

# Creating single group of spaceship because of only one spaceship
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
    
    # Update methods of classes
    spaceship_group.update()

    # Drawing
    window.fill(bg_color)
    spaceship_group.draw(window)
    spaceship_group.sprite.lasers_group.draw(window)

    pygame.display.update()
    clock.tick(fps)

pygame.quit()