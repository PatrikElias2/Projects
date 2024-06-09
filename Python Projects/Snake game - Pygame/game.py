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
score = 0
best_score = 0

# Fonts
big_font = pygame.font.Font('font/font.otf', 64)
small_font = pygame.font.Font('font/font.otf', 16)



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
        # Add a new segment to the snake's body at the position of the last segment
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
    
    def respawn(self):
        self.position = self.random_position()


class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.score = score
        self.best_score = best_score
        self.move_counter = 0
        self.move_delay = 4  # Change this value to control the speed (higher = slower)

    def draw_score(self):
        score_text = small_font.render(f'Score: {self.score}', True, black_color_bg)
        best_score_text = small_font.render(f'Best Score: {self.best_score}', True, black_color_bg)
        window.blit(score_text, (10, 40))
        window.blit(best_score_text, (10, 10))
    
    def draw(self):
        self.snake.draw(window)
        self.food.draw(window)
        self.draw_score()

    def check_collision(self):
        # x and y position of snake's head
        head_x, head_y = self.snake.body[0]

        # Check if the snake's head is at the same position as the food
        if self.snake.body[0] == self.food.position:
            self.snake.grow()
            self.food.respawn()
            self.score += 5
            if self.score > self.best_score:
                self.best_score = self.score

        # Check collision with window boundaries
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            self.game_over()

        # Check collision with the snake's body
        if (head_x, head_y) in self.snake.body[1:]:
            self.game_over()

    def update(self):
        self.move_counter += 1
        if self.move_counter >= self.move_delay:
            self.snake.move()
            self.check_collision()
            self.move_counter = 0

    def game_over(self):
        # For simplicity, we will just reset the game
        self.score = 0
        self.snake = Snake()
        self.food = Food(self.snake.body)
    
    

game = Game()

# main cycle
running = True
while running:

    window.fill(bg_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Add controls for changing direction
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