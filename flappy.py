import pygame
import sys
import time
import random

# Initializing the pygame
pygame.init()

# Frames per second
clock = pygame.time.Clock()


def draw_floor():
    """Function to draw the floor"""
    screen.blit(floor_img, (floor_x, 520))
    screen.blit(floor_img, (floor_x + 448, 520))


def create_pipes():
    """Function to create pipes"""
    pipe_y = random.choice(pipe_height)
    top_pipe = pipe_img.get_rect(midbottom=(467, pipe_y - 300)) # 300 is the gap between the pipes 
    bottom_pipe = pipe_img.get_rect(midtop=(467, pipe_y)) # 467 is the width of the window
    return top_pipe, bottom_pipe


def pipe_animation():
    global game_over, score_time
    for pipe in pipes:
        if pipe.top < 0:
            # Flipping the pipe image for the top pipe
            flipped_pipe = pygame.transform.flip(pipe_img, False, True)
            screen.blit(flipped_pipe, pipe)
        else:
            # Drawing the pipe image for the bottom pipe
            screen.blit(pipe_img, pipe)

        pipe.centerx -= 3
        if pipe.right < 0:
            # Removing the pipe from the list if it crosses the window
            pipes.remove(pipe)

        if bird_rect.colliderect(pipe):
            game_over = True


# Function to draw score
def draw_score(game_state):
    if game_state == "game_on":
        score_text = score_font.render(str(score), True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(width // 2, 66))
        screen.blit(score_text, score_rect)
    elif game_state == "game_over":
        score_text = score_font.render(f" Score: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(width // 2, 66))
        screen.blit(score_text, score_rect)

        high_score_text = score_font.render(f"High Score: {high_score}", True, (255, 255, 255))
        high_score_rect = high_score_text.get_rect(center=(width // 2, 506))
        screen.blit(high_score_text, high_score_rect)


# Function to update the score
def score_update():
    global score, score_time, high_score
    if pipes:
        for pipe in pipes:
            if 65 < pipe.centerx < 69 and score_time:
                score += 1
                score_time = False
            if pipe.left <= 0:
                score_time = True

    if score > high_score:
        high_score = score


# Game window
width, height = 350, 622
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")

# setting background and base image
back_img = pygame.image.load(r"images\background.png")
floor_img = pygame.image.load(r"images\floor.png")
floor_x = 0

# different stages of bird
bird_up = pygame.image.load(r"images\bird.png")
bird_down = pygame.image.load(r"images\bird.png")
bird_mid = pygame.image.load(r"images\bird.png")

birds = [bird_up, bird_mid, bird_down]
bird_index = 0
bird_flap = pygame.USEREVENT
pygame.time.set_timer(bird_flap, 200)
bird_img = birds[bird_index]
bird_rect = bird_img.get_rect(center=(67, 622 // 2))
bird_movement = 0
gravity = 0.17

# Loading pipe image
pipe_img = pygame.image.load(r"images\greenpipe.png")
pipe_height = [400, 350, 533, 490]

# for the pipes to appear
pipes = []
create_pipe = pygame.USEREVENT + 1
pygame.time.set_timer(create_pipe, 1200)

# Displaying game over image
game_over = False
over_img = pygame.image.load("images\gameover.png").convert_alpha ()
over_rect = over_img.get_rect(center=(width // 2, height // 2))

# setting variables and font for score
score = 0
high_score = 0
score_time = True
score_font = pygame.font.Font("freesansbold.ttf", 27)

# Game loop
running = True
while running:
    clock.tick(120)

    # for checking the events : QUIT, KEYDOWN, create_pipe, bird_flap
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # QUIT event
            running = False
            sys.exit()

        if event.type == pygame.KEYDOWN:  # Key pressed event
            if event.key == pygame.K_SPACE and not game_over:  # If space key is pressed
                # making the bird jump
                bird_movement = 0
                bird_movement = -7

            if event.key == pygame.K_SPACE and game_over:
                # Restarting the game
                game_over = False
                pipes = []
                bird_movement = 0
                bird_rect = bird_img.get_rect(center=(67, 622 // 2))
                score_time = True
                score = 0

        # To load different stages
        if event.type == bird_flap:
            bird_index += 1

            if bird_index > 2:
                bird_index = 0

            bird_img = birds[bird_index]
            bird_rect = bird_up.get_rect(center=bird_rect.center)

        # To add pipes in the list
        if event.type == create_pipe:
            pipes.extend(create_pipes())

    screen.blit(floor_img, (floor_x, 550))
    screen.blit(back_img, (0, 0))

    # Game over conditions
    if not game_over:
        bird_movement += gravity
        bird_rect.centery += bird_movement
        rotated_bird = pygame.transform.rotozoom(bird_img, bird_movement * -6, 1)

        if bird_rect.top < 5 or bird_rect.bottom >= 550:
            game_over = True

        screen.blit(rotated_bird, bird_rect)
        pipe_animation()
        score_update()
        draw_score("game_on")
    elif game_over:
        screen.blit(over_img, over_rect)
        draw_score("game_over")

    # To move the base
    floor_x -= 1
    if floor_x < -448:
        floor_x = 0

    draw_floor()

    # Update the game window
    pygame.display.update()

# quiting the pygame and sys
pygame.quit()
sys.exit()
