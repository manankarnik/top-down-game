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

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


def configure():
    # Initialize Pygame
    pygame.init()
    pygame.display.set_caption("Top Down")


class CustomSprite(pygame.sprite.Sprite):
    def __init__(self, image: pygame.surface.Surface, position: pygame.math.Vector2, sprite_scale: tuple = SPRITE_SCALE, group=None) -> None:
        if group is None:
            super().__init__()
        else:
            super().__init__(group)

        self.image = image
        self.image = pygame.transform.scale(self.image, sprite_scale)
        self.rect = self.image.get_rect(center=position)

    def setPosition(self, position):
        self.rect = self.image.get_rect(center=position)
