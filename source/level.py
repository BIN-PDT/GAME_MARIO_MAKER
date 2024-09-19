import pygame, sys
from settings import *

from sprites import *
from player import Player


class Level:
    def __init__(self, assets, layers, switch_command):
        self.screen = pygame.display.get_surface()
        # CONTROL.
        self.switch_command = switch_command
        # GROUPS.
        self.all_sprites = pygame.sprite.Group()
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
                else:
                    match data:
                        # PLAYER.
                        case 0:
                            self.player = Player(pos, self.all_sprites)

    def run(self, dt):
        # EVENT.
        self.event_loop()
        # UPDATE.
        self.all_sprites.update(dt)
        # DRAW.
        self.screen.fill(SKY_COLOR)
        self.all_sprites.draw(self.screen)
