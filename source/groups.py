import pygame
from pygame.math import Vector2 as Vector
from settings import *


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        # SETUP.
        self.offset = Vector()

    def draw(self, player_pos):
        self.offset.x = -(player_pos[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(player_pos[1] - WINDOW_HEIGHT / 2)
        # DRAW.
        for sprite in sorted(self, key=lambda sprite: sprite.z):
            self.screen.blit(sprite.image, sprite.rect.topleft + self.offset)
