import pygame
from pygame.locals import *
import random

# Init pygame
pygame.init()
pygame.mixer.init()

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
button_color = (0, 255, 0)
button_hover_color = (0, 200, 0)

# variables
snake_rect_size = 10
food_rect_size = 10
border_size = 1  # Size of the black border around the head and body
score = 0
best_score = 0

# Fonts
big_font = pygame.font.Font('font/font.otf', 48)
medium_font = pygame.font.Font('font/font.otf', 32)
small_font = pygame.font.Font('font/font.otf', 16)

# Load and play background music
pygame.mixer.music.load('music/bg_music.wav') 
pygame.mixer.music.play(-1)  # Play the music in a loop
pygame.mixer.music.set_volume(0.1)

eat_sound = pygame.mixer.Sound("music/eat.mp3")
wall_hit_sound = pygame.mixer.Sound("music/wall.mp3")
body_hit_sound = pygame.mixer.Sound("music/body.wav")


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
        self.food_image = pygame.image.load("img/food.png")
        self.food_image = pygame.transform.scale(self.food_image, (food_rect_size, food_rect_size))  # Scale the image to the size of the food rectangle

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
        #food_rect = pygame.Rect(self.position[0], self.position[1], food_rect_size, food_rect_size)
        window.blit(self.food_image, self.position)
    
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
        self.eat_sound = eat_sound
        self.wall_hit_sound = wall_hit_sound
        self.body_hit_sound = body_hit_sound
        self.game_over_flag = False
        self.bg_music_volume = 0.1
        self.eat_sound_volume = 0.1
        self.wall_hit_sound_volume = 0.1
        self.body_hit_sound_volume = 0.1


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
            self.eat_sound.play()
            self.score += 5
            if self.score > self.best_score:
                self.best_score = self.score


        # Check collision with window boundaries
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            self.wall_hit_sound.play()
            self.game_over()
            

        # Check collision with the snake's body
        if (head_x, head_y) in self.snake.body[1:]:
            self.body_hit_sound.play()
            self.game_over()

    def update(self):
        if not self.game_over_flag:
            self.move_counter += 1
            if self.move_counter >= self.move_delay:
                self.snake.move()
                self.check_collision()
                self.move_counter = 0

    def game_over(self):
        self.game_over_flag = True
        self.draw_game_over_screen()

    def draw_game_over_screen(self):
        pygame.mixer.music.stop()
        game_over_text = big_font.render('Game Over', True, black_color_bg)
        play_again_text = medium_font.render('Play Again', True, black_color_bg)
        window.blit(game_over_text, ((WIDTH - game_over_text.get_width()) // 2, HEIGHT // 2 - 50))
        
        # Button for Play Again and Main menu
        play_again_rect = pygame.Rect((WIDTH - play_again_text.get_width() - 20) // 2, HEIGHT // 2 + 20,
                                    play_again_text.get_width() + 20, play_again_text.get_height() + 10)
        
        pygame.draw.rect(window, bg_color, play_again_rect)

        window.blit(play_again_text, (play_again_rect.x + 10, play_again_rect.y + 5))

    
        pygame.display.update()
        
        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if play_again_rect.collidepoint(event.pos):
                        self.restart_game()
                        waiting_for_restart = False
                        

    def restart_game(self):
        pygame.mixer.music.play(-1)
        self.score = 0
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.game_over_flag = False
    
    def draw_main_menu(self):
        window.fill(bg_color)
        title_text = big_font.render('Snake Game', True, black_color_bg)
        play_text = medium_font.render('Play', True, black_color_bg)
        options_text = medium_font.render('Options', True, black_color_bg)
        quit_text = medium_font.render('Quit', True, black_color_bg)

        window.blit(title_text, ((WIDTH - title_text.get_width()) // 2, HEIGHT // 4))
        
        # Buttons
        play_rect = pygame.Rect((WIDTH - play_text.get_width() - 20) // 2, HEIGHT // 2,
                                play_text.get_width() + 20, play_text.get_height() + 10)
        options_rect = pygame.Rect((WIDTH - options_text.get_width() - 20) // 2, HEIGHT // 2 + 50,
                                   options_text.get_width() + 20, options_text.get_height() + 10)
        quit_rect = pygame.Rect((WIDTH - quit_text.get_width() - 20) // 2, HEIGHT // 2 + 100,
                                quit_text.get_width() + 20, quit_text.get_height() + 10)
        
        pygame.draw.rect(window, bg_color, play_rect)
        pygame.draw.rect(window, bg_color, options_rect)
        pygame.draw.rect(window, bg_color, quit_rect)
        
        window.blit(play_text, (play_rect.x + 10, play_rect.y + 5))
        window.blit(options_text, (options_rect.x + 10, options_rect.y + 5))
        window.blit(quit_text, (quit_rect.x + 10, quit_rect.y + 5))
        
        pygame.display.update()
        
        return play_rect, options_rect, quit_rect

    def draw_options_menu(self):
        window.fill(bg_color)
        options_text = medium_font.render('Options', True, black_color_bg)
        speed_text_legend = small_font.render('Higher number = slower speed', True, black_color_bg)
        speed_text = small_font.render(f'Speed: {self.move_delay}', True, black_color_bg)
        volume_text = small_font.render('Volume:', True, black_color_bg)
        back_text = medium_font.render('Back', True, black_color_bg)

        window.blit(options_text, ((WIDTH - options_text.get_width()) // 2, HEIGHT // 4))
        window.blit(speed_text_legend, ((WIDTH - speed_text_legend.get_width()) // 2, HEIGHT // 2.2))

        # Speed adjustment
        speed_rect = pygame.Rect((WIDTH - speed_text.get_width() - 20) // 2, HEIGHT // 2,
                                 speed_text.get_width() + 20, speed_text.get_height() + 10)
        
        # Back text
        back_rect = pygame.Rect((WIDTH - back_text.get_width() - 20) // 2, HEIGHT - 100,
                                back_text.get_width() + 20, back_text.get_height() + 10)
        
        pygame.draw.rect(window, bg_color, speed_rect)
        pygame.draw.rect(window, bg_color, back_rect)
        
        window.blit(speed_text, (speed_rect.x + 10, speed_rect.y + 5))
        window.blit(back_text, (back_rect.x + 10, back_rect.y + 5))
        
        # Volume sliders and texts

        bg_music_text = small_font.render('Background Music:', True, black_color_bg)
        window.blit(bg_music_text, ((WIDTH - bg_music_text.get_width()) // 2 - 150, HEIGHT // 2 + 50))

        eat_sound_text = small_font.render('Eat Sound:', True, black_color_bg)
        window.blit(eat_sound_text, ((WIDTH - eat_sound_text.get_width()) // 2 - 150, HEIGHT // 2 + 90))

        wall_hit_sound_text = small_font.render('Wall Hit Sound:', True, black_color_bg)
        window.blit(wall_hit_sound_text, ((WIDTH - wall_hit_sound_text.get_width()) // 2 - 150, HEIGHT // 2 + 130))

        body_hit_sound_text = small_font.render('Body Hit Sound:', True, black_color_bg)
        window.blit(body_hit_sound_text, ((WIDTH - body_hit_sound_text.get_width()) // 2 - 150, HEIGHT // 2 + 170))

        bg_music_slider_rect = pygame.Rect((WIDTH - 200) // 2 + 60, HEIGHT // 2 + 50, 200, 20)
        eat_sound_slider_rect = pygame.Rect((WIDTH - 200) // 2 + 60, HEIGHT // 2 + 90, 200, 20)
        wall_hit_sound_slider_rect = pygame.Rect((WIDTH - 200) // 2 + 60, HEIGHT // 2 + 130, 200, 20)
        body_hit_sound_slider_rect = pygame.Rect((WIDTH - 200) // 2 + 60, HEIGHT // 2 + 170, 200, 20)
        
        pygame.draw.rect(window, (200, 200, 200), bg_music_slider_rect)
        pygame.draw.rect(window, (100, 100, 100), (bg_music_slider_rect.x, bg_music_slider_rect.y, self.bg_music_volume * 200, 20))
        
        pygame.draw.rect(window, (200, 200, 200), eat_sound_slider_rect)
        pygame.draw.rect(window, (100, 100, 100), (eat_sound_slider_rect.x, eat_sound_slider_rect.y, self.eat_sound_volume * 200, 20))
        
        pygame.draw.rect(window, (200, 200, 200), wall_hit_sound_slider_rect)
        pygame.draw.rect(window, (100, 100, 100), (wall_hit_sound_slider_rect.x, wall_hit_sound_slider_rect.y, self.wall_hit_sound_volume * 200, 20))
        
        pygame.draw.rect(window, (200, 200, 200), body_hit_sound_slider_rect)
        pygame.draw.rect(window, (100, 100, 100), (body_hit_sound_slider_rect.x, body_hit_sound_slider_rect.y, self.body_hit_sound_volume * 200, 20))
        
        pygame.display.update()
        
        return speed_rect, back_rect, bg_music_slider_rect, eat_sound_slider_rect, wall_hit_sound_slider_rect, body_hit_sound_slider_rect


game = Game()

# main cycle
running = True
in_menu = True
in_options = False
sliders = {}
music_playing = False  # Flag to manage short music play

while running:

    window.fill(bg_color)
    if in_menu:
        play_rect, options_rect, quit_rect = game.draw_main_menu()
        pygame.mixer.music.stop()  # Stop the background music when in menu
    elif in_options:
        speed_rect, back_rect, bg_music_slider_rect, eat_sound_slider_rect, wall_hit_sound_slider_rect, body_hit_sound_slider_rect = game.draw_options_menu()
        sliders = {
            'bg_music': bg_music_slider_rect,
            'eat_sound': eat_sound_slider_rect,
            'wall_hit_sound': wall_hit_sound_slider_rect,
            'body_hit_sound': body_hit_sound_slider_rect
        }
    else:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)  # Play background music on loop when game starts
        game.update()
        game.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                in_menu = not in_menu  # Toggle menu
                in_options = False  # Reset options menu flag
            elif not in_menu and not in_options:  # Only handle key presses when not in menu or options
                if event.key == pygame.K_UP and game.snake.direction != (0, 1):
                    game.snake.direction = (0, -1)
                elif event.key == pygame.K_DOWN and game.snake.direction != (0, -1):
                    game.snake.direction = (0, 1)
                elif event.key == pygame.K_LEFT and game.snake.direction != (1, 0):
                    game.snake.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and game.snake.direction != (-1, 0):
                    game.snake.direction = (1, 0)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if in_menu:
                if play_rect.collidepoint(event.pos):
                    in_menu = False
                elif options_rect.collidepoint(event.pos):
                    in_options = True
                    in_menu = False
                elif quit_rect.collidepoint(event.pos):
                    running = False
            elif in_options:
                if speed_rect.collidepoint(event.pos):
                    game.move_delay = (game.move_delay + 1) % 20  # Speed adjustment
                elif back_rect.collidepoint(event.pos):
                    in_options = False
                    in_menu = True
                else:
                    for key, rect in sliders.items():
                        if rect.collidepoint(event.pos):
                            relative_x = event.pos[0] - rect.x
                            volume = relative_x / rect.width
                            if key == 'bg_music':
                                game.bg_music_volume = volume
                                pygame.mixer.music.set_volume(volume)
                                if not music_playing:
                                    pygame.mixer.music.play()
                                    music_playing = True
                                    pygame.time.set_timer(pygame.USEREVENT, 1000)
                            elif key == 'eat_sound':
                                game.eat_sound_volume = volume
                                game.eat_sound.set_volume(volume)
                                if not music_playing:
                                    game.eat_sound.play()
                                    music_playing = True
                                    pygame.time.set_timer(pygame.USEREVENT, 1000)
                            elif key == 'wall_hit_sound':
                                game.wall_hit_sound_volume = volume
                                game.wall_hit_sound.set_volume(volume)
                                if not music_playing:
                                    game.wall_hit_sound.play()
                                    music_playing = True
                                    pygame.time.set_timer(pygame.USEREVENT, 1000)
                            elif key == 'body_hit_sound':
                                game.body_hit_sound_volume = volume
                                game.body_hit_sound.set_volume(volume)
                                if not music_playing:
                                    game.body_hit_sound.play()
                                    music_playing = True
                                    pygame.time.set_timer(pygame.USEREVENT, 1000)

        elif event.type == pygame.USEREVENT:
            if music_playing:
                pygame.mixer.music.stop()
                music_playing = False

    pygame.display.update()
    clock.tick(fps)

pygame.quit()