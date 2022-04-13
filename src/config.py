import pygame


# Configuration Constants
FPS = 60
WIDTH, HEIGHT = 1280, 720
SPRITE_SCALE = 100, 100

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRASS_GREEN = (126, 200, 80)

CENTER = WIDTH//2, HEIGHT//2

ui_group = pygame.sprite.Group()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


def configure():
    # Initialize Pygame
    pygame.init()
    pygame.display.set_caption("Top Down")
