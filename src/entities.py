import math
import pygame
from pygame.locals import *

from config import *
import objects


class Entity(pygame.sprite.Sprite):
    def __init__(self, position: pygame.Vector2, group: pygame.sprite.Group) -> None:
        super().__init__(group)
        self.position = position
        self.velocity = pygame.Vector2()
        self.acceleration = pygame.Vector2()
        self.collider = pygame.sprite.Sprite()

    # Returns a list of targets colliding with self
    def getCollisions(self, targets) -> list:
        collisons = []
        for target in targets:
            if self.collider.rect.colliderect(target.collider.rect):
                collisons.append(target)
        return collisons

    def applyForce(self, force: pygame.Vector2) -> None:
        self.acceleration += force

    def moveAndSlide(self, targets) -> None:
        self.velocity += self.acceleration

        # Move collider x, check for collisions
        self.collider.rect[0] += self.velocity.x
        collisions = self.getCollisions(targets)
        # Resolve collisions in x axis
        for target in collisions:
            if self.velocity.x > 0:
                self.collider.rect.right = target.collider.rect.left
            elif self.velocity.x < 0:
                self.collider.rect.left = target.collider.rect.right

        # Move collider y, check for collisions
        self.collider.rect[1] += self.velocity.y
        collisions = self.getCollisions(targets)
        # Resolve collisions in x axis
        for target in collisions:
            if self.velocity.y > 0:
                self.collider.rect.bottom = target.collider.rect.top
            elif self.velocity.y < 0:
                self.collider.rect.top = target.collider.rect.bottom

        # Set position relative to collider position
        self.position = pygame.Vector2(
            self.collider.rect.center[0], self.collider.rect.center[1] - self.rect.size[1]/2 + self.collider.image.get_rect().h/2)
        # Update position of sprite rect
        self.rect = self.image.get_rect(center=self.position)

        # Set velocity to 0 if less then friction magnitude
        if self.velocity.x > -FRICTION_MAGNITUDE and self.velocity.x < FRICTION_MAGNITUDE:
            self.velocity.x = 0
        if self.velocity.y > -FRICTION_MAGNITUDE and self.velocity.y < FRICTION_MAGNITUDE:
            self.velocity.y = 0

        # Set acceleration to zero
        self.acceleration *= 0


class Player(Entity):
    def __init__(self, position: pygame.Vector2, group: pygame.sprite.Group) -> None:
        super().__init__(position, group)
        self.group = group
        self.image = pygame.image.load(
            "src/Assets/player.png").convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (50, 50))
        self.rect = self.image.get_rect(center=self.position)

        collider_size = (25, 12.5)
        collider_sprite = pygame.surface.Surface(collider_size, flags=SRCALPHA)
        collider_sprite.fill((255, 0, 0, 80))

        self.collider = objects.Sprite(
            collider_sprite, self.position + pygame.Vector2(0, self.rect.size[1]/2 - collider_size[1]/2), ui_group, group)
        self.dash_indicator_image = pygame.image.load(
            "src/Assets/dash_indicator_active.png").convert_alpha()
        self.dash_indicator_image = pygame.transform.scale(
            self.dash_indicator_image, (32, 32))

        self.dash_indicator = objects.Sprite(
            self.dash_indicator_image, self.position + pygame.Vector2(50, 0), ui_group)

        self.state = PLAYER_IDLE

        self.current_time = PLAYER_DASH_COOLDOWN * 1000
        self.last_dash = 0

    def moveAndSlide(self) -> None:
        # Call moveAndSlide defined in parent
        super().moveAndSlide(trees)

        # Velocity constains
        if self.state != PLAYER_DASHING:
            if self.state == PLAYER_WALKING and self.velocity.magnitude() > PLAYER_WALK_SPEED:
                self.velocity = self.velocity.normalize() * PLAYER_WALK_SPEED
            elif self.state == PLAYER_RUNNING and self.velocity.magnitude() > PLAYER_RUN_SPEED:
                self.velocity = self.velocity.normalize() * (PLAYER_RUN_SPEED)
        elif self.velocity.magnitude() > PLAYER_DASH_SPEED:
            self.velocity = self.velocity.normalize() * (PLAYER_DASH_SPEED)

        # Deceleration
        if self.state != PLAYER_WALKING and self.state != PLAYER_RUNNING and self.velocity.magnitude() > 0:
            self.applyForce(self.velocity.normalize() * -FRICTION_MAGNITUDE)

        if self.state != PLAYER_DASHING or self.velocity.magnitude() < FRICTION_MAGNITUDE:
            self.state = PLAYER_IDLE

        self.current_time += clock.get_time()

    def keyup(self, key):
        if key == K_SPACE:
            self.dash_indicator.kill()
            if self.current_time - self.last_dash >= PLAYER_DASH_COOLDOWN * 1000:
                self.last_dash = self.current_time
                mouse_vector = pygame.Vector2(pygame.mouse.get_pos())
                relative_distance = mouse_vector.distance_to(
                    pygame.Vector2(CENTER))
                print(relative_distance)
                if relative_distance > self.rect.size[0]:
                    relative_vector = (
                        mouse_vector - pygame.Vector2(CENTER)) * 0.2
                    print(mouse_vector, CENTER, relative_vector)

                    if relative_vector.magnitude() > PLAYER_DASH_DISTANCE:
                        relative_vector = relative_vector.normalize() * PLAYER_DASH_DISTANCE

                    self.applyForce(relative_vector)
                    self.state = PLAYER_DASHING

    def keyheld(self):
        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            if self.current_time - self.last_dash >= PLAYER_DASH_COOLDOWN * 1000:
                self.dash_indicator_image = pygame.image.load(
                    "src/Assets/dash_indicator_active.png").convert_alpha()
            else:
                self.dash_indicator_image = pygame.image.load(
                    "src/Assets/dash_indicator_inactive.png").convert_alpha()

            self.dash_indicator_image = pygame.transform.scale(
                self.dash_indicator_image, (32, 32))
            mouse_vector = pygame.Vector2(pygame.mouse.get_pos())
            relative_vector = mouse_vector - pygame.Vector2(CENTER)
            relative_distance = relative_vector.magnitude()

            if relative_distance > self.rect.size[0]:
                angle_in_rad = -math.atan2(relative_vector.y, relative_vector.x)
                angle = angle_in_rad * 180/math.pi
                offset = pygame.Vector2(
                    50 * math.cos(angle_in_rad), 50 * -math.sin(angle_in_rad))

                self.dash_indicator.image = pygame.transform.rotozoom(
                    self.dash_indicator_image, angle, 1)
                self.dash_indicator.rect = self.dash_indicator.image.get_rect(
                    center=self.position + offset)
                self.dash_indicator.add(self.group)

        if keys[K_UP] or keys[K_w] and self.state != PLAYER_DASHING:
            if keys[K_LCTRL]:
                self.state = PLAYER_RUNNING
            else:
                self.state = PLAYER_WALKING
            self.applyForce(pygame.Vector2(0, -PLAYER_ACCELERATION_MAGNITUDE))

        if keys[K_DOWN] or keys[K_s] and self.state != PLAYER_DASHING:
            if keys[K_LCTRL]:
                self.state = PLAYER_RUNNING
            else:
                self.state = PLAYER_WALKING
            self.applyForce(pygame.Vector2(0, PLAYER_ACCELERATION_MAGNITUDE))

        if keys[K_LEFT] or keys[K_a] and self.state != PLAYER_DASHING:
            if keys[K_LCTRL]:
                self.state = PLAYER_RUNNING
            else:
                self.state = PLAYER_WALKING
            self.applyForce(pygame.Vector2(-PLAYER_ACCELERATION_MAGNITUDE, 0))

        if keys[K_RIGHT] or keys[K_d] and self.state != PLAYER_DASHING:
            if keys[K_LCTRL]:
                self.state = PLAYER_RUNNING
            else:
                self.state = PLAYER_WALKING
            self.applyForce(pygame.Vector2(PLAYER_ACCELERATION_MAGNITUDE, 0))
