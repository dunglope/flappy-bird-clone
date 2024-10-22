import pygame
from sys import exit
from random import randint

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_X = 576
SCREEN_Y = 850

# Initialize variables
pipe1_pass = 0
pipe2_pass = 0
pipe_scroll = 0
gravity = 0
change1_height = 0
change2_height = 0
change1_dis = 0
change2_dis = 0
if_die = 1
if1_die = 0
bird_index = 0
score = 0
high_score = 0
skin_selected = 0  # Tracks the selected bird skin
MIN_GAP_SIZE = 68  # Minimum space between the upper and lower pipes
game_state = "menu"  # Tracks if the game is in the menu or game

# Load high score from a file at the start of your game
try:
    with open("high_score.txt", "r") as f:
        high_score = int(f.read())
except FileNotFoundError:
    high_score = 0  # Default to 0 if file does not exist

# Setup screen, clock, and fonts
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
pygame.display.set_caption("Floaty Bird")
clock = pygame.time.Clock()

background = pygame.image.load("imgs/background.png")

text_font = pygame.font.Font("fonts/PixelFont.ttf", 25)
menu_font = pygame.font.Font("fonts/PixelFont.ttf", 35)
bottom1_t = text_font.render("Press Space, Mouse", False, "White")
bottom2_t = text_font.render("or Up Arrow", False, "White")

score_font = pygame.font.Font("fonts/PixelFont.ttf", 18)
score_t = score_font.render(f"{score}", False, "White")
high_score_t = score_font.render(f"Previous High Score: {high_score}", False, "White")

# Load and scale bird images (three skins)
bird1_skin1 = pygame.image.load("imgs/blue/bird_down.png")
bird2_skin1 = pygame.image.load("imgs/blue/bird_middle.png")
bird3_skin1 = pygame.image.load("imgs/blue/bird_up.png")

bird1_skin2 = pygame.image.load("imgs/pink/bird_down_pink.png")  # Assuming another skin in pink
bird2_skin2 = pygame.image.load("imgs/pink/bird_middle_pink.png")
bird3_skin2 = pygame.image.load("imgs/pink/bird_up_pink.png")

bird1_skin3 = pygame.image.load("imgs/green/bird_down_green.png")  # Another skin in green
bird2_skin3 = pygame.image.load("imgs/green/bird_middle_green.png")
bird3_skin3 = pygame.image.load("imgs/green/bird_up_green.png")

# List of bird skins
bird_skins = [
    [bird3_skin1, bird2_skin1, bird1_skin1],
    [bird3_skin2, bird2_skin2, bird1_skin2],
    [bird3_skin3, bird2_skin3, bird1_skin3],
]

# Scaling bird skins
for skin in bird_skins:
    for i in range(3):
        skin[i] = pygame.transform.scale(skin[i], (68, 48))

bird_flap = bird_skins[skin_selected]  # Default to the first skin
bird_surf = bird_flap[bird_index]
bird_rect = bird_surf.get_rect(topleft=(45, 100))

# Pipe positions
pipe1_u_y = randint(500, 800)
pipe1_d_y = randint(500, 800)
pipe2_d_y = randint(500, 800)
pipe2_u_y = randint(500, 800)

pipe1_distance = randint(200, 300) + 640
pipe2_distance = randint(200, 300) + 640

# Load and scale pipe images
pipe1_u = pygame.image.load("imgs/pipe.png").convert()
Scaled_pipe1_u = pygame.transform.scale(pipe1_u, (104, 800))
pipe1_u_rect = Scaled_pipe1_u.get_rect(topleft=(700, pipe1_u_y))

pipe2_u = pygame.image.load("imgs/pipe.png").convert()
Scaled_pipe2_u = pygame.transform.scale(pipe2_u, (104, 800))
pipe2_u_rect = Scaled_pipe2_u.get_rect(topleft=(1250, pipe2_u_y))

pipe1_d = pygame.image.load("imgs/pipe.png").convert()
Scaled_pipe1_d = pygame.transform.scale(pipe1_d, (104, 604))
Rotated_pipe1_d = pygame.transform.rotate(Scaled_pipe1_d, 180)
pipe1_d_rect = Rotated_pipe1_d.get_rect(topleft=(700, pipe1_d_y - pipe1_distance))

pipe2_d = pygame.image.load("imgs/pipe.png").convert()
Scaled_pipe2_d = pygame.transform.scale(pipe2_d, (104, 604))
Rotated_pipe2_d = pygame.transform.rotate(Scaled_pipe2_d, 180)
pipe2_d_rect = Rotated_pipe2_d.get_rect(topleft=(1250, pipe2_d_y - pipe2_distance))

# Game over image
game_over = pygame.image.load("imgs/gameover.png")
Scaled_gameover = pygame.transform.scale(game_over, (384, 84))
gameover_rect = Scaled_gameover.get_rect(topleft=(96, 450))

# Randomize the pipe positions with a guaranteed gap
def reset_pipes():
    global pipe1_u_y, pipe1_d_y, pipe2_u_y, pipe2_d_y, pipe1_distance, pipe2_distance
    pipe1_u_y = randint(100, 600)  # Upper pipe height for pipe 1
    pipe1_d_y = pipe1_u_y - MIN_GAP_SIZE/2  # Lower pipe height for pipe 1, ensuring a minimum gap
    pipe2_u_y = randint(100, 600)  # Upper pipe height for pipe 2
    pipe2_d_y = pipe2_u_y - MIN_GAP_SIZE/2  # Lower pipe height for pipe 2, ensuring a minimum gap

    # Re-randomize pipe distances
    pipe1_distance = randint(200, 300) + 610
    pipe2_distance = randint(200, 300) + 610

# Bird animation function
def bird_animation():
    global bird_surf, bird_index
    bird_index += 0.1
    if bird_index >= len(bird_flap):
        bird_index = 0
    bird_surf = bird_flap[int(bird_index)]

# Menu display function
def display_menu():
    screen.fill((0, 0, 0))  # Black background for menu
    title_text = menu_font.render("Select Bird Skin", False, "White")
    screen.blit(title_text, (SCREEN_X // 2 - title_text.get_width() // 2, 100))
    
    # Display skins in menu
    for idx, skin in enumerate(bird_skins):
        skin_preview = skin[1]  # Display middle frame of the bird
        skin_rect = skin_preview.get_rect(center=(SCREEN_X // 4 * (idx + 1), SCREEN_Y // 2))
        screen.blit(skin_preview, skin_rect)
    
    # Highlight the selected skin
    highlight_rect = pygame.Rect(SCREEN_X // 4 * (skin_selected + 1) - 40, SCREEN_Y // 2 - 40, 80, 80)
    pygame.draw.rect(screen, "Yellow", highlight_rect, 5)

# Game reset function
def reset_game():
    global score, bird_rect, gravity, pipe1_u_rect, pipe2_u_rect, pipe1_d_rect, pipe2_d_rect, if_die, if1_die
    # Reset score and gravity
    score = 0
    gravity = 0
    # Reset bird position
    bird_rect.topleft = (45, 300)
    # Reset pipes position and re-randomize the gap
    reset_pipes()
    pipe1_u_rect.topleft = (700, pipe1_u_y)
    pipe2_u_rect.topleft = (1250, pipe2_u_y)
    pipe1_d_rect.topleft = (700, pipe1_d_y - pipe1_distance)
    pipe2_d_rect.topleft = (1250, pipe2_d_y - pipe2_distance)
    # Reset game state
    if_die = 0
    if1_die = 0

# Collision detection function
def check_collision():
    global if_die, if1_die, gravity
    if not immortal_mode:  # Only check for collisions if not in immortal mode
        if (bird_rect.colliderect(pipe1_u_rect) or bird_rect.colliderect(pipe2_u_rect) or
            bird_rect.colliderect(pipe1_d_rect) or bird_rect.colliderect(pipe2_d_rect) or 
            bird_rect.y <= 0 or bird_rect.y >= SCREEN_Y - 100):  # 100 as a buffer for ground
            if_die = 1
            if1_die = 1
            gravity = 0  # Reset gravity when the bird dies
        
# Score update function
def update_score():
    global score, pipe1_pass, pipe2_pass, high_score
    if pipe1_u_rect.x + Scaled_pipe1_u.get_width() < bird_rect.x and pipe1_pass == 0:  # Bird passes pipe1
        score += 1
        pipe1_pass = 1  # Avoid double counting the same pipe
    if pipe2_u_rect.x + Scaled_pipe2_u.get_width() < bird_rect.x and pipe2_pass == 0:  # Bird passes pipe2
        score += 1
        pipe2_pass = 1  # Avoid double counting the same pipe

    if score > high_score:  # Update high score
        high_score = score
        # Save high score to a file when it updates
        with open("high_score.txt", "w") as f:
            f.write(str(high_score))

######################### FOR DEBUGING ONLY #########################
# Variable to track immortality
immortal_mode = False

# Cheat code function
def toggle_immortal():
    global immortal_mode
    immortal_mode = not immortal_mode  # Toggle the immortality state

# Check for cheat code input
def check_cheat_code(event):
    if event.type == pygame.KEYDOWN:
        # Example: Press 'I' to toggle immortality
        if event.key == pygame.K_i:
            toggle_immortal()
#########################################################################

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        # Check for cheat code input
        check_cheat_code(event)

        # Menu controls
        if game_state == "menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    skin_selected = (skin_selected + 1) % len(bird_skins)  # Cycle to the right
                elif event.key == pygame.K_LEFT:
                    skin_selected = (skin_selected - 1) % len(bird_skins)  # Cycle to the left
                elif event.key == pygame.K_SPACE:
                    bird_flap = bird_skins[skin_selected]  # Apply selected skin
                    game_state = "game"  # Start the game
                    reset_game()  # Reset game elements

        # Game controls
        elif game_state == "game":
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_SPACE, pygame.K_w, pygame.K_UP] and if_die == 0:
                    gravity = -7.734
                elif if1_die == 1 and event.key == pygame.K_SPACE:  # Press space after death
                    reset_game()  # Reset the game

    # Clear the screen and fill with background color
    screen.fill((0, 0, 0))  # Optional, in case the background doesn't load
    if game_state == "menu":
        display_menu()
    elif game_state == "game":
        # Game logic
        if if_die == 0:
            gravity += 0.09
            bird_rect.y += gravity/2

        # Check for collisions
        check_collision()

        # Update score
        update_score()

        # Blit background and game elements
        screen.blit(background, (0, 0))  # Make sure background loads correctly

        # Pipe movement logic
        if if_die == 0:
            pipe_scroll = -4
            pipe1_u_rect.x += pipe_scroll
            pipe2_u_rect.x += pipe_scroll
            pipe1_d_rect.x += pipe_scroll
            pipe2_d_rect.x += pipe_scroll

            # Reset pipes when off-screen and handle scoring
            if pipe1_u_rect.x <= -104:
                pipe1_u_rect.x = 700
                pipe1_d_rect.x = 700
                reset_pipes()  # Reset pipe positions with new gap logic
                pipe1_pass = 0  # Reset the pass flag for pipe1

            if pipe2_u_rect.x <= -104:
                pipe2_u_rect.x = 1250
                pipe2_d_rect.x = 1250
                reset_pipes()  # Reset pipe positions with new gap logic
                pipe2_pass = 0  # Reset the pass flag for pipe2

            # Score update logic
            if pipe1_u_rect.x + Scaled_pipe1_u.get_width() < bird_rect.x and pipe1_pass == 0:
                score += 1
                score_t = score_font.render(f"{score}", False, "White")
                pipe1_pass = 1  # Avoid double counting the same pipe

            if pipe2_u_rect.x + Scaled_pipe2_u.get_width() < bird_rect.x and pipe2_pass == 0:
                score += 1
                score_t = score_font.render(f"{score}", False, "White")
                pipe2_pass = 1  # Avoid double counting the same pipe

        # Render game elements
        screen.blit(Scaled_pipe1_u, pipe1_u_rect)
        screen.blit(Scaled_pipe2_u, pipe2_u_rect)
        screen.blit(Rotated_pipe1_d, pipe1_d_rect)
        screen.blit(Rotated_pipe2_d, pipe2_d_rect)
        screen.blit(bird_surf, bird_rect)
        screen.blit(score_t, (250, 100))

        bird_animation()

        # When the player dies, display "Game Over" and check for Space press to reset
        if if1_die == 1:
            screen.blit(Scaled_gameover, gameover_rect)
            screen.blit(high_score_t, (SCREEN_X // 4, 300))

            # Check if the player presses space to restart
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                reset_game()

    # Update the display
    pygame.display.update()
    clock.tick(60)
