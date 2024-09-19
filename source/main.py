import pygame
from settings import *
from supports import *

from editor import Editor
from level import Level
from transition import Transition


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Mario Maker")
        self.clock = pygame.time.Clock()
        # CURSOR.
        cursor_surf = import_image("images", "cursors", "mouse")
        cursor = pygame.cursors.Cursor((0, 0), cursor_surf)
        pygame.mouse.set_cursor(cursor)
        # SETUP.
        self.load_assets()
        self.level = None
        self.level_active = False
        self.transition = Transition(self.toggle)
        self.editor = Editor(self.land_tiles, self.switch)

    def load_assets(self):
        # GENERAL ASSETS.
        self.land_tiles = import_folder_dict("images", "terrain", "land")
        # LEVEL ASSETS.
        self.level_assets = {
            "land": self.land_tiles,
        }

    def toggle(self):
        self.level_active = not self.level_active

    def switch(self, layers=None):
        self.transition.is_active = True
        # SWITCH FROM EDITOR TO LEVEL.
        if layers:
            self.level = Level(self.level_assets, layers, self.switch)

    def run(self):
        while True:
            # DELTA TIME.
            delta_time = self.clock.tick() / 1000
            # GAME LOGIC.
            if self.level_active:
                self.level.run(delta_time)
            else:
                self.editor.run(delta_time)
            # TRANSITION.
            if self.transition.is_active:
                self.transition.display(delta_time)
            # SCREEN UPDATE.
            pygame.display.update()


if __name__ == "__main__":
    Game().run()
