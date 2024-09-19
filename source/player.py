import pygame
from pygame.math import Vector2 as Vector
from sprites import Generic


class Player(Generic):
    def __init__(self, pos, groups):
        surf = pygame.Surface((32, 64))
        surf.fill("red")
        super().__init__(pos, surf, groups)
        # MOVEMENT.
        self.direction = Vector()
        self.SPEED = 300

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def move(self, dt):
        self.rect.topleft += self.direction * self.SPEED * dt

    def update(self, dt):
        self.input()
        self.move(dt)
