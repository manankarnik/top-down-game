import pygame

from config import *


class Camera(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def centerCamera(self, player):
        self.offset.x = player.rect.centerx - WIDTH//2
        self.offset.y = player.rect.centery - HEIGHT//2

    def render(self, player) -> None:
        ysorted_sprites = sorted(
            self.sprites(), key=lambda sprite: sprite.rect.bottom)

        # Append UI elements at the end to always draw on top
        for i in range(len(ysorted_sprites) - 1, -1, -1):
            if ui_group in ysorted_sprites[i].groups():
                ysorted_sprites.append(ysorted_sprites.pop(i))

        for sprite in ysorted_sprites:
            self.centerCamera(player)
            offset_pos = sprite.rect.topleft - self.offset
            self.screen.blit(sprite.image, offset_pos)
