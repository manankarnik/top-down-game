import random
import sys
import pygame
from pygame.locals import *

from config import *
import entities
import camera
import objects

camera_group = camera.Camera()
player = entities.Player(pygame.Vector2(CENTER), camera_group)

for i in range(30):
    trees.append(objects.Tree(pygame.Vector2(random.randrange(-1000, 1000, 150),
                 random.randrange(-1000, 1000, 150)), camera_group))


def main() -> None:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            pass

        if event.type == KEYUP:
            player.keyup(event.key)

    player.handleInput()
    player.move()
    camera_group.update()
    camera_group.render(player)


if __name__ == "__main__":
    while True:
        configure()
        screen.fill(GRASS_GREEN)
        main()
        clock.tick(FPS)
        pygame.display.update()
