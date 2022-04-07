import os
import random
import pygame
from pygame.locals import *

clock = pygame.time.Clock()


class Entity():
    def __init__(self, window: pygame.Surface, position: pygame.Vector2,
                 velocity: pygame.Vector2, acceleration: pygame.Vector2,
                 max_velocity: float, size: float) -> None:
        self.window = window
        self.position = position
        self._velocity = velocity
        self.max_velocity = max_velocity
        self._acceleration = acceleration
        self.size = size

    def applyForce(self, force: pygame.Vector2) -> None:
        self._acceleration += force

    def update(self, isDashing: bool = False) -> None:
        self._velocity += self._acceleration
        self.position += self._velocity

        # Constrain velocity if state is not dashing
        if not isDashing and self._velocity.magnitude() > self.max_velocity:
            self._velocity = self._velocity.normalize() * self.max_velocity

        # Reset acceleration to 0 every frame
        self._acceleration = pygame.Vector2(0, 0)

    # Render Player
    # TODO: Render sprite
    def render(self, color: tuple = (0, 0, 0)) -> None:
        entity = pygame.Rect(
            *self.position, self.size, self.size)
        entity.center = self.position
        pygame.draw.rect(self.window, color, entity)

    # Getters and Setters
    @property
    def acceleration(self) -> pygame.Vector2:
        return self._acceleration

    @acceleration.setter
    def acceleration(self, acceleration: pygame.Vector2) -> None:
        self._acceleration = acceleration

    @property
    def velocity(self) -> pygame.Vector2:
        return self._velocity

    @velocity.setter
    def velocity(self, velocity: pygame.Vector2) -> None:
        self._velocity = velocity


class Enemy(Entity):
    def __init__(self, window: pygame.Surface, position: pygame.Vector2,
                 velocity: pygame.Vector2, acceleration: pygame.Vector2,
                 max_velocity: float, size: float) -> None:
        super().__init__(window, position, velocity, acceleration, max_velocity, size)

    def wander(self, idle_range: tuple):
        self.applyForce(pygame.Vector2(
            random.uniform(-1, 1), random.uniform(-1, 1)))

    def follow(self, player: Entity, acceleration_magnitude: float):
        relative_distance_vector = (player.position - self.position)
        acceleration_to_player = relative_distance_vector.normalize() * \
            acceleration_magnitude

        if relative_distance_vector.magnitude() < 400:
            self.applyForce(acceleration_to_player)
        # else:
            # self.acceleration *= 0
            # self.velocity *= 0

    def constrain(self, p1: pygame.Vector2, p2: pygame.Vector2):
        if self.position.x < p1.x:
            self.applyForce(pygame.Vector2(1, 0))
            # self.position.x = p1.x + self.size/2 + 10
        elif self.position.x > p2.x:
            self.applyForce(pygame.Vector2(-1, 0))
            self.position.x = p2.x - self.size/2

        if self.position.y < p1.y:
            self.applyForce(pygame.Vector2(0, 1))
            self.position.y = p1.y + self.size/2
        elif self.position.y > p2.y:
            self.applyForce(pygame.Vector2(0, -1))
            self.position.y = p2.y - self.size/2


if __name__ == "__main__":
    os.system("main.py")
