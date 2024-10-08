import pygame
from pygame.math import Vector2 as Vector
from settings import *
from timers import Timer
from sprites import Generic


class Player(Generic):
    def __init__(self, pos, frames, groups, collision_sprites, jump_sound):
        # ASSETS.
        self.jump_sound = jump_sound
        # ANIMATION.
        self.frames, self.frame_index = frames, 0
        self.status, self.orientation = "idle", "right"
        # SETUP.
        surf = self.frames[f"{self.status}_{self.orientation}"][self.frame_index]
        super().__init__(pos, surf, groups)
        self.mask = pygame.mask.from_surface(self.image)
        # MOVEMENT.
        self.direction = Vector()
        self.SPEED = 300
        # GRAVITY.
        self.on_floor = False
        self.GRAVITY = 4
        # COLLISION.
        self.collision_sprites = collision_sprites
        self.hitbox = self.rect.inflate(-50, 0)
        self.floor_rect = pygame.Rect(self.hitbox.bottomleft, (self.hitbox.width, 2))
        # DAMAGE.
        self.invul_timer = Timer(200)

    def input(self):
        keys = pygame.key.get_pressed()
        # MOVE.
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.orientation = "right"
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.orientation = "left"
        else:
            self.direction.x = 0
        # JUMP.
        if keys[pygame.K_SPACE] and self.on_floor:
            self.jump_sound.play()
            self.direction.y = -1.5

    # ANIMATION.
    def check_status(self):
        if self.direction.y < 0:
            self.status = "jump"
        elif self.direction.y > 0:
            self.status = "fall"
        else:
            self.status = "idle" if self.direction.x == 0 else "run"

    def animate(self, dt):
        animation = self.frames[f"{self.status}_{self.orientation}"]
        self.frame_index += ANIMATION_SPEED * dt
        self.frame_index %= len(animation)

        self.image = animation[int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)
        # DAMAGED ANIMATION.
        if self.invul_timer.is_active:
            mask = self.mask.to_surface()
            mask.set_colorkey("black")
            self.image = mask

    # MOVEMENT & COLLISION.
    def move(self, dt):
        # HORIZONTAL.
        self.rect.x += self.direction.x * self.SPEED * dt
        self.hitbox.centerx = self.rect.centerx
        self.collide("horizontal")
        # VERTICAL.
        self.rect.y += self.direction.y * self.SPEED * dt
        self.hitbox.centery = self.rect.centery
        self.collide("vertical")

    def apply_gravity(self, dt):
        self.direction.y += self.GRAVITY * dt
        self.rect.y += self.direction.y

    def check_on_floor(self):
        self.floor_rect.topleft = self.hitbox.bottomleft
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.floor_rect):
                self.on_floor = True
                break
        else:
            self.on_floor = False

    def collide(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox):
                if direction == "horizontal":
                    # MOVING RIGHT.
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.rect.left
                    # MOVING LEFT.
                    elif self.direction.x < 0:
                        self.hitbox.left = sprite.rect.right
                    self.rect.centerx = self.hitbox.centerx
                else:
                    # JUMPING.
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.rect.bottom
                    # FALLING.
                    elif self.direction.y > 0:
                        self.hitbox.bottom = sprite.rect.top
                    self.rect.centery = self.hitbox.centery
                    # RESET GRAVITY.
                    self.direction.y = 0

    # DAMAGE.
    def get_damage(self):
        if not self.invul_timer.is_active:
            self.invul_timer.activate()
            self.direction.y = -1.25

    def update(self, dt):
        self.invul_timer.update()
        self.input()

        self.apply_gravity(dt)
        self.move(dt)
        self.check_on_floor()

        self.check_status()
        self.animate(dt)
