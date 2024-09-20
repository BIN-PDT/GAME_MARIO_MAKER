import pygame, sys
from settings import *

from sprites import *
from player import Player


class Level:
    def __init__(self, assets, layers, switch_command):
        self.screen = pygame.display.get_surface()
        # CONTROL.
        self.switch_command = switch_command
        # ASSETS.
        self.particle_surfs = assets["particle"]
        # GROUPS.
        self.all_sprites = pygame.sprite.Group()
        self.coin_sprites = pygame.sprite.Group()
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
        for layer_name, layer_data in layers.items():
            for pos, data in layer_data.items():
                if layer_name == "terrain":
                    Generic(pos, assets["land"][data], self.all_sprites)
                elif layer_name == "water":
                    if data == "bottom":
                        Generic(pos, assets["water_bottom"], self.all_sprites)
                    else:
                        Animate(pos, assets["water_top"], self.all_sprites)
                else:
                    match data:
                        # PLAYER.
                        case 0:
                            self.player = Player(pos, self.all_sprites)
                        # COIN.
                        case 4 | 5 | 6:
                            coin_type = {4: "gold", 5: "silver", 6: "diamond"}[data]
                            Coin(
                                pos=pos,
                                frames=assets[coin_type],
                                groups=(self.all_sprites, self.coin_sprites),
                                coin_type=coin_type,
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
        self.all_sprites.draw(self.screen)
