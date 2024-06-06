import pygame
from pygame.locals import *
import random

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

# variables
snake_rect_size = 10
food_rect_size = 10

class Snake:
    def __init__(self):
        self.body = [(300, 300)]
        self.direction = (0, 0)

    def move(self):
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x * snake_rect_size, head_y + dir_y * snake_rect_size)
        self.body = [new_head] + self.body[:-1]

    def grow(self):
        self.body.append(self.body[-1])

    def draw(self, window):
        for segment in self.body:
            snake_rect = pygame.Rect(segment[0], segment[1], snake_rect_size, snake_rect_size)
            pygame.draw.rect(window, (0, 255, 0), snake_rect)

class Food:
    def __init__(self, snake_body):
        self.snake_body = snake_body
        self.position = self.random_position()


    def random_position(self):
        # Logic to get a random position
        grid_size = 10
        max_position = 600 - grid_size
        while True:
            x = random.randint(0, max_position // grid_size) * grid_size
            y = random.randint(0, max_position // grid_size) * grid_size
            if (x, y) not in self.snake_body:
                return (x, y)

    def draw(self, window):
        food_rect = pygame.Rect(self.position[0], self.position[1], food_rect_size, food_rect_size)
        pygame.draw.rect(window, (255, 0, 0), food_rect)
    

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)

    def draw(self):
        self.snake.draw(window)
        self.food.draw(window)

game = Game()

# main cycle
running = True
while running:

    window.fill(bg_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    game.draw()
    pygame.display.update()
    clock.tick(fps)

pygame.quit()