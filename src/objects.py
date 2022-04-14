import pygame
from pygame.locals import *
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
        collider_size = (32, 3*32/4)
        collider_sprite = pygame.surface.Surface(collider_size, flags=SRCALPHA)
        collider_sprite.fill((255, 0, 0, 80))

        self.collider = Sprite(
            collider_sprite, self.position + pygame.Vector2(0, self.rect.size[1]/2 - collider_size[1]/2), ui_group, group)
