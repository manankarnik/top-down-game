import sys
import pygame
from pygame.locals import *

from player import *

WIDTH, HEIGHT = 1280, 720
FPS = 60
FRICTION = 0.4
PLAYER_ACCELERATION = 0.4
MAX_VELOCITY = 8
PLAYER_SIZE = 20

pygame.init()
pygame.display.set_caption("Top Down")

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
player_position = pygame.Vector2(WIDTH/2, HEIGHT/2)
player_accleration = pygame.Vector2(0, 0)
player_velocity = pygame.Vector2(0, 0)
player = Player(window, player_position, player_velocity,
                player_accleration, MAX_VELOCITY, PLAYER_SIZE)


def main() -> None:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[K_UP] or keys[K_w]:
        player.applyForce(pygame.Vector2(0, -PLAYER_ACCELERATION))
        print(player.velocity)

    if keys[K_DOWN] or keys[K_s]:
        player.applyForce(pygame.Vector2(0, PLAYER_ACCELERATION))
        print(player.velocity)

    if keys[K_LEFT] or keys[K_a]:
        player.applyForce(pygame.Vector2(-PLAYER_ACCELERATION, 0))
        print(player.velocity)

    if keys[K_RIGHT] or keys[K_d]:
        player.applyForce(pygame.Vector2(PLAYER_ACCELERATION, 0))
        print(player.velocity)

    if not keys[K_UP] and not keys[K_w] and not keys[K_DOWN] and not keys[K_s]:
        if player.velocity.y < -0.5:
            player.applyForce(pygame.Vector2(0, FRICTION))
        elif player.velocity.y > 0.5:
            player.applyForce(pygame.Vector2(0, -FRICTION))
        else:
            player.acceleration.y = 0
            player.velocity.y = 0

    if not keys[K_LEFT] and not keys[K_a] and not keys[K_RIGHT] and not keys[K_d]:
        if player.velocity.x < -0.5:
            player.applyForce(pygame.Vector2(FRICTION, 0))
        elif player.velocity.x > 0.5:
            player.applyForce(pygame.Vector2(-FRICTION, 0))
        else:
            player.acceleration.x = 0
            player.velocity.x = 0

    window.fill((126, 200, 80))
    player.update()
    player.render()


if __name__ == "__main__":
    while True:
        main()
        clock.tick(FPS)
        pygame.display.update()
