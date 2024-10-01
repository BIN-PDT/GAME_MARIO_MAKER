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
            # TERRAIN.
            "land": self.land_tiles,
            "water_bottom": import_image("images", "terrain", "water", "water_bottom"),
            "water_top": import_folder_list("images", "terrain", "water", "animation"),
            "palms": import_folder_dict("images", "terrain", "palm", subordinate=True),
            # COIN.
            "gold": import_folder_list("images", "items", "gold"),
            "silver": import_folder_list("images", "items", "silver"),
            "diamond": import_folder_list("images", "items", "diamond"),
            "particle": import_folder_list("images", "items", "particle"),
            # ENEMY.
            "spike": import_image("images", "enemies", "spikes", "0"),
            "tooth": import_folder_dict("images", "enemies", "tooth", subordinate=True),
            "shell": import_folder_dict(
                "images", "enemies", "shell_left", subordinate=True
            ),
            "pearl": import_image("images", "enemies", "pearl", "0"),
            # PLAYER.
            "player": import_folder_dict("images", "player", subordinate=True),
            # CLOUDS.
            "clouds": import_folder_list("images", "clouds"),
            # SOUND.
            "music": import_sound("audio", "SuperHero.ogg", volume=0.2),
            "jump": import_sound("audio", "jump.wav", volume=0.1),
            "coin": import_sound("audio", "coin.wav", volume=0.3),
            "hit": import_sound("audio", "hit.wav", volume=0.3),
        }

    def toggle(self):
        self.level_active = not self.level_active
        # TOGGLE MOUSE.
        pygame.mouse.set_visible(not self.level_active)
        # SWITCH MUSIC.
        if not self.level_active:
            self.editor.music.play(-1)

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
