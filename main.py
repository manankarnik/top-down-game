import sys
from turtle import position
import pygame
from pygame.locals import *

from entity import *

WIDTH, HEIGHT = 1280, 720
FPS = 60
FRICTION_MAGNITUDE = 0.4
PLAYER_DASH_MAGNITUDE = 30
PLAYER_ACCELERATION_MAGNITUDE = 0.6
PLAYER_MAX_VELOCITY = 8
PLAYER_SIZE = 20

# Player States
PLAYER_IDLE = 0
PLAYER_MOVING = 1
PLAYER_DASHING = 2

pygame.init()
pygame.display.set_caption("Top Down")

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player_position = pygame.Vector2(WIDTH/2, HEIGHT/2)
player_accleration = pygame.Vector2(0, 0)
player_velocity = pygame.Vector2(0, 0)
player = Entity(window, player_position, player_velocity,
                player_accleration, PLAYER_MAX_VELOCITY, PLAYER_SIZE)


def main() -> None:
    player_state = PLAYER_IDLE
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYUP:
            if event.key == K_SPACE:
                mouse_position = pygame.mouse.get_pos()
                mouse_vector = pygame.Vector2(mouse_position)
                relative_distance = mouse_vector.distance_to(player.position)

                if relative_distance > player.size:
                    relative_vector = (mouse_vector - player.position) * 0.2

                    if relative_vector.magnitude() > PLAYER_DASH_MAGNITUDE:
                        relative_vector = relative_vector.normalize() * PLAYER_DASH_MAGNITUDE

                    player.applyForce(relative_vector)
                    player_state = PLAYER_DASHING

    keys = pygame.key.get_pressed()
    if keys[K_SPACE]:
        mouse_position = pygame.mouse.get_pos()
        pygame.draw.line(window, (0, 0, 0),
                         player.position, mouse_position, 3)

    if keys[K_UP] or keys[K_w]:
        player_state = PLAYER_MOVING
        player.applyForce(pygame.Vector2(0, -PLAYER_ACCELERATION_MAGNITUDE))

    if keys[K_DOWN] or keys[K_s]:
        player_state = PLAYER_MOVING
        player.applyForce(pygame.Vector2(0, PLAYER_ACCELERATION_MAGNITUDE))

    if keys[K_LEFT] or keys[K_a]:
        player_state = PLAYER_MOVING
        player.applyForce(pygame.Vector2(-PLAYER_ACCELERATION_MAGNITUDE, 0))

    if keys[K_RIGHT] or keys[K_d]:
        player_state = PLAYER_MOVING
        player.applyForce(pygame.Vector2(PLAYER_ACCELERATION_MAGNITUDE, 0))

    if player_state == PLAYER_IDLE:
        if player.velocity.magnitude() > 0:
            player.applyForce(player.velocity.normalize()
                              * -FRICTION_MAGNITUDE)
            if player.velocity.magnitude() < 0.1:
                player.velocity *= 0

    player.update((player_state, PLAYER_DASHING))
    player.render()


if __name__ == "__main__":
    while True:
        window.fill((126, 200, 80))
        main()
        clock.tick(FPS)
        pygame.display.update()
