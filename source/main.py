import pygame
from settings import *
from supports import *

from editor import Editor


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
        self.editor = Editor(self.land_tiles)

    def load_assets(self):
        # TERRAIN.
        self.land_tiles = import_folder_dict("images", "terrain", "land")

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
