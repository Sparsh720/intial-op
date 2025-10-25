import pygame
import random

# Initialize Pygame
pygame.init()

# Get the device's screen info
info = pygame.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Coin Collector")

# Calculate scaling factors based on screen size
SCALE_X = WIDTH / 800  # Base width
SCALE_Y = HEIGHT / 600  # Base height

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Player properties
PLAYER_SIZE = int(30 * min(SCALE_X, SCALE_Y))
player = pygame.Rect(WIDTH // 2, HEIGHT - 2 * PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE)
PLAYER_SPEED = 5 * min(SCALE_X, SCALE_Y)

# Coin properties
COIN_SIZE = int(20 * min(SCALE_X, SCALE_Y))
coin = pygame.Rect(random.randint(0, WIDTH - COIN_SIZE), 
                  random.randint(0, HEIGHT - COIN_SIZE), 
                  COIN_SIZE, COIN_SIZE)

# Obstacle properties
OBSTACLE_SIZE = int(40 * min(SCALE_X, SCALE_Y))
obstacles = [pygame.Rect(random.randint(0, WIDTH - OBSTACLE_SIZE), 
                       random.randint(0, HEIGHT - OBSTACLE_SIZE), 
                       OBSTACLE_SIZE, OBSTACLE_SIZE) for _ in range(3)]

# Virtual joystick properties
JOYSTICK_RADIUS = int(50 * min(SCALE_X, SCALE_Y))
joystick_pos = (JOYSTICK_RADIUS + 20, HEIGHT - JOYSTICK_RADIUS - 20)
joystick_touch = None
joystick_vector = (0, 0)

# Game properties
clock = pygame.time.Clock()
score = 0
game_over = False
font = pygame.font.Font(None, int(36 * min(SCALE_X, SCALE_Y)))

def draw_joystick():
    # Draw outer circle
    pygame.draw.circle(WINDOW, WHITE, joystick_pos, JOYSTICK_RADIUS, 2)
    
    if joystick_touch is not None:
        # Draw inner circle (stick position)
        stick_pos = (
            int(joystick_pos[0] + joystick_vector[0] * JOYSTICK_RADIUS),
            int(joystick_pos[1] + joystick_vector[1] * JOYSTICK_RADIUS)
        )
        pygame.draw.circle(WINDOW, BLUE, stick_pos, JOYSTICK_RADIUS // 3)

def draw_game():
    WINDOW.fill(BLACK)
    
    # Draw player
    pygame.draw.rect(WINDOW, WHITE, player)
    
    # Draw coin
    pygame.draw.rect(WINDOW, YELLOW, coin)
    
    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(WINDOW, RED, obstacle)
    
    # Draw joystick
    draw_joystick()
    
    # Draw score
    score_text = font.render(f'Score: {score}', True, WHITE)
    WINDOW.blit(score_text, (10, 10))
    
    if game_over:
        game_over_text = font.render('Game Over! Tap to restart', True, WHITE)
        text_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        WINDOW.blit(game_over_text, text_rect)
    
    pygame.display.update()

def handle_touch_input():
    global joystick_touch, joystick_vector
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        
        if event.type == pygame.FINGERDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            # Convert touch/mouse position to screen coordinates
            if event.type == pygame.FINGERDOWN:
                x = event.x * WIDTH
                y = event.y * HEIGHT
            else:
                x, y = event.pos
                
            # Check if touch is in joystick area
            dx = x - joystick_pos[0]
            dy = y - joystick_pos[1]
            if (dx * dx + dy * dy) <= JOYSTICK_RADIUS * JOYSTICK_RADIUS:
                joystick_touch = (x, y)
        
        elif event.type == pygame.FINGERUP or event.type == pygame.MOUSEBUTTONUP:
            joystick_touch = None
            joystick_vector = (0, 0)
        
        elif event.type == pygame.FINGERMOTION or event.type == pygame.MOUSEMOTION:
            if joystick_touch is not None:
                # Convert touch/mouse position to screen coordinates
                if event.type == pygame.FINGERMOTION:
                    x = event.x * WIDTH
                    y = event.y * HEIGHT
                else:
                    x, y = event.pos
                
                # Calculate joystick vector
                dx = x - joystick_pos[0]
                dy = y - joystick_pos[1]
                length = (dx * dx + dy * dy) ** 0.5
                if length > 0:
                    joystick_vector = (dx / length, dy / length)
                else:
                    joystick_vector = (0, 0)
    
    return True

# Game loop
running = True
while running:
    clock.tick(60)
    
    running = handle_touch_input()
    
    if game_over:
        # Check for tap to restart
        for event in pygame.event.get():
            if event.type in (pygame.FINGERDOWN, pygame.MOUSEBUTTONDOWN):
                # Reset game
                player.x = WIDTH // 2
                player.y = HEIGHT - 2 * PLAYER_SIZE
                score = 0
                game_over = False
                # Reset obstacles and coin
                coin.x = random.randint(0, WIDTH - COIN_SIZE)
                coin.y = random.randint(0, HEIGHT - COIN_SIZE)
                obstacles = [pygame.Rect(random.randint(0, WIDTH - OBSTACLE_SIZE), 
                                      random.randint(0, HEIGHT - OBSTACLE_SIZE), 
                                      OBSTACLE_SIZE, OBSTACLE_SIZE) for _ in range(3)]
    
    if not game_over and joystick_vector != (0, 0):
        # Move player based on joystick
        new_x = player.x + joystick_vector[0] * PLAYER_SPEED
        new_y = player.y + joystick_vector[1] * PLAYER_SPEED
        
        # Keep player within bounds
        if 0 <= new_x <= WIDTH - PLAYER_SIZE:
            player.x = new_x
        if 0 <= new_y <= HEIGHT - PLAYER_SIZE:
            player.y = new_y
        
        # Check coin collision
        if player.colliderect(coin):
            score += 1
            coin.x = random.randint(0, WIDTH - COIN_SIZE)
            coin.y = random.randint(0, HEIGHT - COIN_SIZE)
        
        # Check obstacle collisions
        for obstacle in obstacles:
            if player.colliderect(obstacle):
                game_over = True
    
    draw_game()

pygame.quit()