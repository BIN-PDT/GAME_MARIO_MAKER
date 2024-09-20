import pygame
from settings import *


class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        # SETUP.
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)


class Animate(Generic):
    def __init__(self, pos, frames, groups):
        # ANIMATION.
        self.frames, self.frame_index = frames, 0
        # SETUP.
        super().__init__(pos, self.frames[self.frame_index], groups)

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        self.frame_index %= len(self.frames)

        self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)


class Coin(Animate):
    def __init__(self, pos, frames, groups, coin_type):
        super().__init__(pos, frames, groups)
        # SETUP.
        self.rect = self.image.get_rect(center=pos)
        self.coin_type = coin_type


class Particle(Animate):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)
        # SETUP.
        self.rect = self.image.get_rect(center=pos)

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()
