import pygame
from pygame.locals import *

# Pygame initialization
pygame.init()

# Window setup
WIDTH = 300
HEIGHT = 300
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# =================Variables==================
# FPS and clock
fps = 120
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)  # Line color
WHITE = (255,255,255)
GREEN = (0,102,0)
RED = (255,0,0)
BLUE = (0,0,255)
bg_color = (180, 177, 54)

# empty list for creating a board
markers = []

# variable for click event
clicked = False
pos = []

# player variable
player = 1

# check winner variables
winner = 0
game_over = False

# font
font = pygame.font.SysFont('arial', 40)

# restart rect
restart_rect = Rect(WIDTH // 2 - 100, HEIGHT // 2, 160, 50)
# =============================================

# board [
    #     [0,0,0]
    #     [0,0,0]
    #     [0,0,0]
    # ]
# Function to initialize or reset the board
def initialize_board():
    global markers
    markers = [[0 for _ in range(3)] for _ in range(3)]

# Function to draw background tiles and lines
def draw(window, line_color):

    # Background
    window.fill(bg_color)
    # Horizontal lines
    for i in range(1, 3):
        y = i * HEIGHT // 3
        pygame.draw.line(window, line_color, (0, y), (WIDTH, y), width=4)

    # Vertical lines
    for i in range(1, 3):
        x = i * WIDTH // 3
        pygame.draw.line(window, line_color, (x, 0), (x, HEIGHT), width=4)

    pygame.display.update()

def draw_markers():
    x_pos = 0
    for x in markers:
        y_pos = 0
        for y in x:
            if y == 1:
                pygame.draw.line(window, RED, (x_pos * 100 + 15, y_pos * 100 + 15), (x_pos * 100 + 85, y_pos *100 + 85), 4)
                pygame.draw.line(window, RED, (x_pos * 100 + 15, y_pos * 100 + 85), (x_pos * 100 + 85, y_pos *100 + 15), 4)
            if y == -1:
                pygame.draw.circle(window,GREEN, (x_pos * 100 + 50, y_pos * 100 + 50),38, 4)
            y_pos += 1
        x_pos += 1


def check_winner():
    global winner 
    global game_over
    y_pos = 0
    for x in markers:
        # check colums
        # winner = 1 because first player = 1 that is why sum(x) == 3
        if sum(x) == 3:
            winner = 1
            game_over = True
        # winner = 2 because second player = -1 that is why sum(x) == -3
        if sum(x) == -3:
            winner = 2
            game_over = True

        # check rows
        if markers[0][y_pos] + markers[1][y_pos] + markers[2][y_pos] == 3:
            winner = 1
            game_over = True
        if markers[0][y_pos] + markers[1][y_pos] + markers[2][y_pos] == -3:
            winner = 2
            game_over = True
        y_pos +=1

        # check cross
        if markers[0][0] + markers[1][1] + markers[2][2] == 3 or markers[2][0] + markers[1][1] + markers[0][2] == 3:
            winner = 1
            game_over = True
        if markers[0][0] + markers[1][1] + markers[2][2] == -3 or markers[2][0] + markers[1][1] + markers[0][2] == -3:
            winner = 2
            game_over = True

def check_tie():
    global game_over
    if all(cell != 0 for row in markers for cell in row) and winner == 0:
        game_over = True
    

def draw_winner(winner):
    if winner == 0:
        tie_text = 'It\'s a tie!'
        win_img = font.render(tie_text, True, WHITE)
        window.blit(win_img, (WIDTH // 2 - 55, HEIGHT // 2 - 50))
    else:
        win_text = 'Player ' + str(winner) + ' wins!'
        win_img = font.render(win_text, True, WHITE)
        window.blit(win_img, (WIDTH // 2 - 100, HEIGHT // 2 - 50))

    restart_text = 'Play again?'
    restart_img = font.render(restart_text, True, WHITE)
    window.blit(restart_img, (WIDTH // 2 - 80, HEIGHT // 2 + 10))

# Main game loop
initialize_board()
running = True
while running:
    # Draw background
    draw(window, BLACK)
    draw_markers()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over == 0:
            # checking full click cycle of the mouse, so not just click but release aswell
            if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
                clicked = True
            if event.type == pygame.MOUSEBUTTONUP and clicked == True:
                clicked = False
                # checking position of click
                pos = pygame.mouse.get_pos()
                cell_x = pos[0]
                cell_y = pos[1]
                # width,height = 300, if == 0 because it wasnt clicked there yet
                if markers[cell_x // 100][cell_y // 100] == 0:
                    markers[cell_x // 100][cell_y // 100] = player
                    player *= -1
                    check_winner()
                    check_tie()
    if game_over:
        draw_winner(winner)
        # check for mouseclick for play again
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
            clicked = True
        if event.type == pygame.MOUSEBUTTONUP and clicked == True:
            clicked = False
            pos = pygame.mouse.get_pos()
            if restart_rect.collidepoint(pos):
                # reset variables
                initialize_board()
                player = 1
                winner = 0
                game_over = False

    pygame.display.update()

    # Slow down the cycle
    clock.tick(fps)

# Quit Pygame
pygame.quit()