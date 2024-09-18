import pygame
from settings import *

from editor import Editor


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Mario Maker")
        self.clock = pygame.time.Clock()
        # SETUP.
        self.editor = Editor()

    def run(self):
        while True:
            # DELTA TIME.
            delta_time = self.clock.tick() / 1000
            # GAME LOGIC.
            self.editor.run(delta_time)
            # SCREEN UPDATE.
            pygame.display.update()


if __name__ == "__main__":
    Game().run()
