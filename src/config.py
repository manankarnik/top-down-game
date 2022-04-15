import pygame


# Configuration Constants
FPS = 60
WIDTH, HEIGHT = (1280, 720)
SPRITE_SCALE = (128, 128)
CENTER = (WIDTH//2, HEIGHT//2)


# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRASS_GREEN = (126, 200, 80)


# Player Constants
PLAYER_ACCELERATION_MAGNITUDE = 0.6
PLAYER_WALK_SPEED = 4
PLAYER_RUN_SPEED = 6
PLAYER_DASH_SPEED = 14
FRICTION_MAGNITUDE = 0.4
PLAYER_DASH_COOLDOWN = 2
PLAYER_DASH_DISTANCE = 50

# Player States
PLAYER_IDLE = 0
PLAYER_WALKING = 1
PLAYER_RUNNING = 2
PLAYER_DASHING = 3

# Group for sprites always drawn on top
ui_group = pygame.sprite.Group()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

trees = []


def configure():
    # Initialize Pygame
    pygame.init()
    pygame.display.set_caption("Top Down")
