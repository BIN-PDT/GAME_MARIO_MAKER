import pygame
from settings import *


class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        # SETUP.
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
