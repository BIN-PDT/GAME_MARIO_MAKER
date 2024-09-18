from settings import *


class CanvasTile:
    def __init__(self, tile_id):
        # TERRAIN.
        self.has_terrain = False
        self.terrain_neighbors = []
        # WATER.
        self.has_water = False
        self.water_on_top = False
        # COIN.
        self.coin = None
        # ENEMY.
        self.enemy = None
        # OBJECT.
        self.objects = []
        # SETUP.
        self.add_item(tile_id)

    @property
    def is_empty(self):
        return not any((self.has_terrain, self.has_water, self.coin, self.enemy))

    def add_item(self, tile_id):
        match EDITOR_DATA[tile_id]["style"]:
            case "terrain":
                self.has_terrain = True
            case "water":
                self.has_water = True
            case "coin":
                self.coin = tile_id
            case "enemy":
                self.enemy = tile_id

    def del_item(self, tile_id):
        match EDITOR_DATA[tile_id]["style"]:
            case "terrain":
                self.has_terrain = False
            case "water":
                self.has_water = False
            case "coin":
                self.coin = None
            case "enemy":
                self.enemy = None
