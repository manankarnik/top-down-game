import pygame

from config import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self, image: pygame.surface.Surface, position: pygame.Vector2, *groups: pygame.sprite.Group) -> None:
        super().__init__(*groups)

        self.image = image
        self.rect = self.image.get_rect(center=position)


class Object(pygame.sprite.Sprite):
    def __init__(self, position: pygame.Vector2, group: pygame.sprite.Group) -> None:
        super().__init__(group)
        self.position = position
        self.movable = True


class Tree(Object):
    def __init__(self, position: pygame.Vector2, group: pygame.sprite.Group) -> None:
        super().__init__(position, group)
        self.image = pygame.image.load("src/Assets/tree.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, SPRITE_SCALE)
        self.rect = self.image.get_rect(center=position)
