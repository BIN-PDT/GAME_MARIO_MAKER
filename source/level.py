import pygame, sys
from random import choice, randint
from settings import *

from sprites import *
from enemies import *
from player import Player
from groups import CameraGroup


class Level:
    def __init__(self, assets, layers, switch_command):
        self.screen = pygame.display.get_surface()
        # CONTROL.
        self.switch_command = switch_command
        # ASSETS.
        self.particle_surfs = assets["particle"]
        self.cloud_surfs = assets["clouds"]
        self.music = assets["music"]
        self.music.play(-1)
        self.hit_sound = assets["hit"]
        self.coin_sound = assets["coin"]
        # CLOUDS.
        self.CLOUD_TIMER = pygame.USEREVENT + 2
        pygame.time.set_timer(self.CLOUD_TIMER, 2000)
        # GROUPS.
        self.all_sprites = CameraGroup()
        self.coin_sprites = pygame.sprite.Group()
        self.damage_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        # SETUP.
        self.build_level(layers, assets)
        self.startup_clouds()

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # CLOUD EVENT.
            if event.type == self.CLOUD_TIMER:
                self.create_cloud()
            # GO TO EDITOR.
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.music.stop()
                self.switch_command()

    def build_level(self, layers, assets):
        # LEVEL LIMIT.
        self.LEVEL_LIMIT = {
            "left": -WINDOW_WIDTH,
            "right": max(layers["terrain"], key=lambda pos: pos[0], default=(0, 0))[0]
            + 500,
        }
        # CONSTANT.
        COIN_TYPE = {4: "gold", 5: "silver", 6: "diamond"}
        FG_PALM_TYPE = {11: "small_fg", 12: "large_fg", 13: "left_fg", 14: "right_fg"}
        BG_PALM_TYPE = {15: "small_bg", 16: "large_bg", 17: "left_bg", 18: "right_bg"}
        SHELL_TYPE = {9: "left", 10: "right"}
        shell_sprites = pygame.sprite.Group()

        for layer_name, layer_data in layers.items():
            for pos, data in layer_data.items():
                if layer_name == "terrain":
                    Generic(
                        pos=pos,
                        surf=assets["land"][data],
                        groups=(self.all_sprites, self.collision_sprites),
                    )
                elif layer_name == "water":
                    if data == "bottom":
                        Generic(
                            pos=pos,
                            surf=assets["water_bottom"],
                            groups=self.all_sprites,
                            z=LEVEL_LAYERS["water"],
                        )
                    else:
                        Animate(
                            pos=pos,
                            frames=assets["water_top"],
                            groups=self.all_sprites,
                            z=LEVEL_LAYERS["water"],
                        )
                else:
                    match data:
                        # PLAYER.
                        case 0:
                            self.player = Player(
                                pos=pos,
                                frames=assets["player"],
                                groups=self.all_sprites,
                                collision_sprites=self.collision_sprites,
                                jump_sound=assets["jump"],
                            )
                        # SKY.
                        case 1:
                            self.skyline = self.all_sprites.skyline = pos[1]
                        # COIN.
                        case 4 | 5 | 6:
                            coin_type = COIN_TYPE[data]
                            Coin(
                                pos=pos,
                                frames=assets[coin_type],
                                groups=(self.all_sprites, self.coin_sprites),
                                coin_type=coin_type,
                            )
                        # ENEMY.
                        case 7:
                            Spike(
                                pos=pos,
                                surf=assets["spike"],
                                groups=(self.all_sprites, self.damage_sprites),
                            )
                        case 8:
                            Tooth(
                                pos=pos,
                                frames=assets["tooth"],
                                groups=(self.all_sprites, self.damage_sprites),
                                collision_sprites=self.collision_sprites,
                            )
                        case 9 | 10:
                            Shell(
                                pos=pos,
                                frames=assets["shell"],
                                groups=(
                                    self.all_sprites,
                                    self.collision_sprites,
                                    shell_sprites,
                                ),
                                orientation=SHELL_TYPE[data],
                                pearl_surf=assets["pearl"],
                                damage_sprites=self.damage_sprites,
                            )
                        # FOREGROUND PALM.
                        case 11 | 12 | 13 | 14:
                            palm_type = FG_PALM_TYPE[data]
                            Animate(pos, assets["palms"][palm_type], self.all_sprites)
                            # COLLIABLE AREA.
                            block_offset = Vector(67 if "right" in palm_type else 17, 0)
                            Block(pos + block_offset, (46, 50), self.collision_sprites)
                        # BACKGROUND PALM.
                        case 15 | 16 | 17 | 18:
                            palm_type = BG_PALM_TYPE[data]
                            Animate(
                                pos=pos,
                                frames=assets["palms"][palm_type],
                                groups=self.all_sprites,
                                z=LEVEL_LAYERS["bg"],
                            )
        # LINK THE PLAYER TO SHELL.
        for sprite in shell_sprites:
            setattr(sprite, "player", self.player)

    def check_collision(self):
        # PLAYER & COIN SPRITES.
        for sprite in pygame.sprite.spritecollide(self.player, self.coin_sprites, True):
            self.coin_sound.play()
            Particle(sprite.rect.center, self.particle_surfs, self.all_sprites)
        # PLAYER & DAMAGE SPRITES.
        for sprite in self.damage_sprites:
            if pygame.sprite.spritecollide(
                self.player, self.damage_sprites, False, pygame.sprite.collide_mask
            ):
                self.hit_sound.play()
                self.player.get_damage()

    # BACKGROUND.
    def create_cloud(self):
        surf = choice(self.cloud_surfs)
        surf = pygame.transform.scale2x(surf) if randint(0, 4) < 2 else surf
        x = self.LEVEL_LIMIT["right"] + randint(100, 300)
        y = self.skyline - randint(-25, 500)
        Cloud((x, y), surf, self.all_sprites, self.LEVEL_LIMIT["left"])

    def startup_clouds(self):
        for _ in range(15):
            surf = choice(self.cloud_surfs)
            surf = pygame.transform.scale2x(surf) if randint(0, 4) < 2 else surf
            x = randint(self.LEVEL_LIMIT["left"], self.LEVEL_LIMIT["right"])
            y = self.skyline - randint(-25, 500)
            Cloud((x, y), surf, self.all_sprites, self.LEVEL_LIMIT["left"])

    def run(self, dt):
        # EVENT.
        self.event_loop()
        # UPDATE.
        self.all_sprites.update(dt)
        self.check_collision()
        # DRAW.
        self.all_sprites.draw(self.player.rect.center)
