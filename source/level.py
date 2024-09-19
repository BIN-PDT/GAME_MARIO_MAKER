import pygame, sys
from settings import *


class Level:
    def __init__(self, layers, switch_command):
        self.screen = pygame.display.get_surface()
        # CONTROL.
        self.switch_command = switch_command
        # DATA.
        self.layers = layers

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # GO TO EDITOR.
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.switch_command()

    def run(self, dt):
        # EVENT.
        self.event_loop()
        # DRAW.
        self.screen.fill("red")
