import pygame, sys
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
        # GROUPS.
        self.all_sprites = CameraGroup()
        self.coin_sprites = pygame.sprite.Group()
        self.damage_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        # SETUP.
        self.build_level(layers, assets)

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # GO TO EDITOR.
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.switch_command()

    def build_level(self, layers, assets):
        # CONSTANT.
        COIN_TYPE = {4: "gold", 5: "silver", 6: "diamond"}
        FG_PALM_TYPE = {11: "small_fg", 12: "large_fg", 13: "left_fg", 14: "right_fg"}
        BG_PALM_TYPE = {15: "small_bg", 16: "large_bg", 17: "left_bg", 18: "right_bg"}
        SHELL_TYPE = {9: "left", 10: "right"}

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
                            )
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
                            )
                        case 9 | 10:
                            shell_type = SHELL_TYPE[data]
                            Shell(
                                pos=pos,
                                frames=assets["shell"],
                                groups=(self.all_sprites, self.collision_sprites),
                                orientation=shell_type,
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

    def check_collision(self):
        # PLAYER & COIN SPRITES.
        for sprite in pygame.sprite.spritecollide(self.player, self.coin_sprites, True):
            Particle(sprite.rect.center, self.particle_surfs, self.all_sprites)

    def run(self, dt):
        # EVENT.
        self.event_loop()
        # UPDATE.
        self.all_sprites.update(dt)
        self.check_collision()
        # DRAW.
        self.screen.fill(SKY_COLOR)
        self.all_sprites.draw(self.player.rect.center)
