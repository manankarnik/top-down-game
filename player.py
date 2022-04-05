import pygame
from pygame.locals import *


class Player():
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

    def update(self) -> None:
        self._velocity += self._acceleration
        self.position += self._velocity

        # Constrain velocity
        if self._velocity.magnitude() > self.max_velocity:
            self._velocity = self._velocity.normalize() * self.max_velocity

        # Reset acceleration to 0 every frame
        self._acceleration = pygame.Vector2(0, 0)

    # Render Player
    # TODO: Render sprite
    def render(self) -> None:
        pygame.draw.circle(self.window, (0, 0, 0), self.position, self.size)

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
