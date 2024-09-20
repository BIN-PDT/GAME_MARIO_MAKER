import pygame
from random import choice
from pygame.math import Vector2 as Vector
from settings import *
from timers import Timer
from sprites import Generic


class Spike(Generic):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)


class Shell(Generic):
    def __init__(self, pos, frames, groups, orientation, pearl_surf, damage_sprites):
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
        # PEARL.
        self.pearl_surf = pearl_surf
        self.has_shot = False
        self.attack_timer = Timer(2000)
        self.damage_sprites = damage_sprites

    def check_status(self):
        if (
            not self.attack_timer.is_active
            and Vector(self.player.rect.center).distance_to(self.rect.center) < 500
        ):
            self.status = "attack"
        else:
            self.status = "idle"

    def animate(self, dt):
        animation = self.frames[self.status]
        self.frame_index += ANIMATION_SPEED * dt
        if self.frame_index >= len(animation):
            self.frame_index = 0
            # COOLDOWN.
            if self.has_shot:
                self.has_shot = False
                self.attack_timer.activate()

        self.image = animation[int(self.frame_index)]
        # ATTACK.
        if self.status == "attack" and not self.has_shot and int(self.frame_index) == 2:
            self.has_shot = True
            # CREATE PEARL.
            direction = -1 if self.orientation == "left" else 1
            offset = Vector(-50 if self.orientation == "left" else 20, -10)
            Pearl(
                pos=self.rect.center + offset,
                surf=self.pearl_surf,
                groups=(self.groups()[0], self.damage_sprites),
                direction=direction,
            )

    def update(self, dt):
        self.attack_timer.update()
        self.check_status()
        self.animate(dt)


class Pearl(Generic):
    def __init__(self, pos, surf, groups, direction):
        super().__init__(pos, surf, groups)
        # MOVEMENT.
        self.direction = direction
        self.SPEED = 150
        # TIMER.
        self.life_timer = Timer(6000)
        self.life_timer.activate()

    def update(self, dt):
        # MOVEMENT.
        self.rect.x += self.direction * self.SPEED * dt
        # TIMER.
        self.life_timer.update()
        if not self.life_timer.is_active:
            self.kill()


class Tooth(Generic):
    def __init__(self, pos, frames, groups, collision_sprites):
        # ANIMATION.
        self.frames, self.frame_index = frames, 0
        self.orientation = choice(("left", "right"))
        # SETUP.
        surf = self.frames[f"run_{self.orientation}"][self.frame_index]
        super().__init__(pos, surf, groups)
        self.rect.midbottom = Vector(pos) + ENEMY_OFFSET
        # MOVEMENT.
        self.direction = -1 if self.orientation == "left" else 1
        self.SPEED = 120
        # COLLISION.
        self.collision_sprites = collision_sprites
        # DESTROY IF NOT ON FLOOR.
        if not self.collide_point(self.rect.midbottom + Vector(0, 10)):
            self.kill()

    def collide_point(self, point):
        for sprite in self.collision_sprites:
            if sprite.rect.collidepoint(point):
                return True
        return False

    def animate(self, dt):
        animation = self.frames[f"run_{self.orientation}"]
        self.frame_index += ANIMATION_SPEED * dt
        self.frame_index %= len(animation)

        self.image = animation[int(self.frame_index)]

    def move(self, dt):
        # REVERSE DIRECTION.
        if self.direction > 0:
            RIGHT_WALL = self.rect.midright + Vector(1, 0)
            RIGHT_FLOOR = self.rect.bottomright + Vector(1, 1)
            if self.collide_point(RIGHT_WALL) or not self.collide_point(RIGHT_FLOOR):
                self.direction = -1
                self.orientation = "left"
        else:
            LEFT_WALL = self.rect.midleft + Vector(-1, 0)
            LEFT_FLOOR = self.rect.bottomleft + Vector(-1, 1)
            if self.collide_point(LEFT_WALL) or not self.collide_point(LEFT_FLOOR):
                self.direction = 1
                self.orientation = "right"
        # MOVEMENT.
        self.rect.x += self.direction * self.SPEED * dt

    def update(self, dt):
        self.move(dt)
        self.animate(dt)
