import pygame, sys
from settings import *


class Editor:
    def __init__(self):
        self.screen = pygame.display.get_surface()

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def run(self, dt):
        self.screen.fill("white")
        # EVENT LOOP.
        self.event_loop()
