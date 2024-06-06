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
snake_head_color = (255, 0, 0)
snake_body_color = (0, 255, 0)
black_color_bg = (0, 0, 0)

# variables
snake_rect_size = 10
food_rect_size = 10
border_size = 1  # Size of the black border around the head and body

class Snake:
    def __init__(self):
        self.body = [(300, 300), (290, 300), (280, 300), (270, 300)]
        self.direction = (0, -1)  # Initial direction set to upwards

    def move(self):
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x * snake_rect_size, head_y + dir_y * snake_rect_size)
        self.body = [new_head] + self.body[:-1]

    def grow(self):
        self.body.append(self.body[-1])

    def draw(self, window):
        for i, segment in enumerate(self.body):
            # Black background (slightly larger than the segment)
            black_rect = pygame.Rect(segment[0] - border_size, segment[1] - border_size,
                                     snake_rect_size + 2 * border_size, snake_rect_size + 2 * border_size)
            pygame.draw.rect(window, black_color_bg, black_rect)
            
            # Segment color (head or body)
            snake_rect = pygame.Rect(segment[0], segment[1], snake_rect_size, snake_rect_size)
            if i == 0:  # Head
                pygame.draw.rect(window, snake_head_color, snake_rect)  # Red head
            else:  # Body
                pygame.draw.rect(window, snake_body_color, snake_rect)  # Green body

class Food:
    def __init__(self, snake_body):
        self.snake_body = snake_body
        self.position = self.random_position()


    def random_position(self):
        # Logic to get a random position
        max_position = 600
        while True:
            x = random.randint(0, max_position)
            y = random.randint(0, max_position)
            if (x, y) not in self.snake_body:
                return (x, y)

    def draw(self, window):
        food_rect = pygame.Rect(self.position[0], self.position[1], food_rect_size, food_rect_size)
        pygame.draw.rect(window, (255, 0, 0), food_rect)

    

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.move_counter = 0
        self.move_delay = 2  # Change this value to control the speed (higher = slower)

    def draw(self):
        self.snake.draw(window)
        self.food.draw(window)

    def update(self):
        self.move_counter += 1
        if self.move_counter >= self.move_delay:
            self.snake.move()
            self.move_counter = 0
            # Future: Add collision detection, growth logic, etc.

game = Game()

# main cycle
running = True
while running:

    window.fill(bg_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
         # Optional: Add controls for changing direction
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game.snake.direction != (0, 1):
                game.snake.direction = (0, -1)
            elif event.key == pygame.K_DOWN and game.snake.direction != (0, -1):
                game.snake.direction = (0, 1)
            elif event.key == pygame.K_LEFT and game.snake.direction != (1, 0):
                game.snake.direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and game.snake.direction != (-1, 0):
                game.snake.direction = (1, 0)
    game.update()            
    game.draw()
    pygame.display.update()
    clock.tick(fps)

pygame.quit()