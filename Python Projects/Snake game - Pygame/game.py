import pygame
from pygame.locals import *

# Init pygame
pygame.init()

# Window
WIDTH = 600
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Game setting
fps = 60
clock = pygame.time.Clock()

# Colors
bg_color = (255, 200, 150)
body1 = (50,175,25)
body2 = (100,100,200)
head_color = (255,0,0)

# variables
snake_rect_size = 10
food_rect_size = 10

def draw_window():
    window.fill(bg_color)


# main cycle
running = True
while running:

    draw_window()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
      
    pygame.display.update()
    clock.tick(fps)

pygame.quit()