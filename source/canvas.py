import pygame
from pygame.math import Vector2 as Vector
from pygame.mouse import get_pos as mouse_pos
from settings import *


class CanvasTile:
    def __init__(self, tile_id, object_offset=None):
        # TERRAIN.
        self.has_terrain = False
        self.terrain_neighbors = []
        # WATER.
        self.has_water = False
        self.water_on_top = False
        # COIN.
        self.coin = None
        # ENEMY.
        self.enemy = None
        # OBJECT.
        self.objects = []
        # SETUP.
        self.add_item(tile_id, object_offset)

    @property
    def is_empty(self):
        return not any((self.has_terrain, self.has_water, self.coin, self.enemy))

    @property
    def water_type(self):
        return "top" if self.water_on_top else "bottom"

    @property
    def terrain_type(self):
        return "".join(self.terrain_neighbors)

    def add_item(self, tile_id, object_offset=None):
        match EDITOR_DATA[tile_id]["style"]:
            case "terrain":
                self.has_terrain = True
            case "water":
                self.has_water = True
            case "coin":
                self.coin = tile_id
            case "enemy":
                self.enemy = tile_id
            case _:
                if (tile_id, object_offset) not in self.objects:
                    self.objects.append((tile_id, object_offset))

    def del_item(self, tile_id):
        match EDITOR_DATA[tile_id]["style"]:
            case "terrain":
                self.has_terrain = False
            case "water":
                self.has_water = False
            case "coin":
                self.coin = None
            case "enemy":
                self.enemy = None


class CanvasObject(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, tile_id, origin):
        super().__init__(groups)
        # ANIMATION.
        self.frames, self.frame_index = frames, 0
        # SETUP.
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.tile_id = tile_id
        # PAN MOVEMENT.
        self.distance_to_origin = self.rect.topleft - origin
        # DRAG MOVEMENT.
        self.is_selected = False
        self.mouse_offset = Vector()

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        self.frame_index %= len(self.frames)

        self.image = self.frames[int(self.frame_index)]
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    # PAN EVENT.
    def pan_pos(self, origin):
        self.rect.topleft = origin + self.distance_to_origin

    # DRAG EVENT.
    def start_drag(self):
        self.is_selected = True
        self.mouse_offset = Vector(mouse_pos()) - self.rect.topleft

    def drag(self):
        if self.is_selected:
            self.rect.topleft = Vector(mouse_pos()) - self.mouse_offset

    def end_drag(self, origin):
        self.is_selected = False
        self.distance_to_origin = self.rect.topleft - origin

    def update(self, dt):
        self.animate(dt)
        self.drag()
