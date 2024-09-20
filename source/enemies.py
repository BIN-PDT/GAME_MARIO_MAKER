import pygame
from pygame.math import Vector2 as Vector
from settings import *
from sprites import Generic


class Spike(Generic):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)


class Tooth(Generic):
    def __init__(self, pos, frames, groups):
        # ANIMATION.
        self.frames, self.frame_index = frames, 0
        self.orientation = "right"
        # SETUP.
        surf = self.frames[f"run_{self.orientation}"][self.frame_index]
        super().__init__(pos, surf, groups)
        self.rect.midbottom = Vector(pos) + ENEMY_OFFSET


class Shell(Generic):
    def __init__(self, pos, frames, groups, orientation):
        # ANIMATION.
        self.frames = (
            {
                key: list(map(lambda e: pygame.transform.flip(e, True, False), value))
                for key, value in frames.items()
            }
            if orientation == "right"
            else frames
        )
        self.frame_index = 0
        self.status = "idle"
        self.orientation = orientation
        # SETUP.
        surf = self.frames[self.status][self.frame_index]
        super().__init__(pos, surf, groups)
        self.rect.midbottom = Vector(pos) + ENEMY_OFFSET
