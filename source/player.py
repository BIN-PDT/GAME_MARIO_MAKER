import pygame
from pygame.math import Vector2 as Vector
from sprites import Generic


class Player(Generic):
    def __init__(self, pos, groups, collision_sprites):
        surf = pygame.Surface((80, 64))
        surf.fill("red")
        super().__init__(pos, surf, groups)
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

    def input(self):
        keys = pygame.key.get_pressed()
        # MOVE.
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0
        # JUMP.
        if keys[pygame.K_SPACE] and self.on_floor:
            self.direction.y = -2

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
        self.floor_rect.top = self.hitbox.bottom
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

    def update(self, dt):
        self.input()
        self.apply_gravity(dt)
        self.move(dt)
        self.check_on_floor()
