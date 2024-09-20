import pygame
from pygame.math import Vector2 as Vector
from settings import *


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        # SETUP.
        self.offset = Vector()

    def draw_sky(self, skyline):
        # SUN.
        pygame.draw.circle(
            self.screen, HORIZON_TOP_COLOR, (WINDOW_WIDTH / 2, skyline), 100
        )
        # HORIZON.
        rect = pygame.Rect(0, skyline - 10, WINDOW_WIDTH, 10)
        pygame.draw.rect(self.screen, HORIZON_TOP_COLOR, rect)
        rect = pygame.Rect(0, skyline - 16, WINDOW_WIDTH, 4)
        pygame.draw.rect(self.screen, HORIZON_TOP_COLOR, rect)
        rect = pygame.Rect(0, skyline - 20, WINDOW_WIDTH, 2)
        pygame.draw.rect(self.screen, HORIZON_TOP_COLOR, rect)
        # SEA.
        rect = pygame.Rect(0, skyline, WINDOW_WIDTH, WINDOW_HEIGHT)
        pygame.draw.rect(self.screen, SEA_COLOR, rect)
        # SEPERATOR.
        pygame.draw.line(
            self.screen, HORIZON_COLOR, (0, skyline), (WINDOW_WIDTH, skyline), 3
        )

    def draw_background(self):
        skyline = self.skyline + self.offset.y
        if skyline > 0:
            # SKY BACKGROUND.
            self.screen.fill(SKY_COLOR)
            # SKY FOREGROUND.
            if skyline < WINDOW_HEIGHT:
                self.draw_sky(skyline)
        # SEA BACKGROUND.
        else:
            self.screen.fill(SEA_COLOR)

    def draw(self, player_pos):
        self.offset.x = -(player_pos[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(player_pos[1] - WINDOW_HEIGHT / 2)
        # DRAW.
        self.draw_background()
        for sprite in sorted(self, key=lambda sprite: sprite.z):
            self.screen.blit(sprite.image, sprite.rect.topleft + self.offset)
