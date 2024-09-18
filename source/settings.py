TILE_SIZE = 64
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
COLS = WINDOW_WIDTH // TILE_SIZE
ROWS = WINDOW_HEIGHT // TILE_SIZE
ANIMATION_SPEED = 8
# OFFSET INFORMATION.
TEXT_OFFSET = TILE_SIZE - 10, 0
COIN_OFFSET = TILE_SIZE // 2, TILE_SIZE // 2  # FROM THE TOPLEFT.
ENEMY_OFFSET = TILE_SIZE // 2, TILE_SIZE  # FROM THE MIDBOTTOM.
# COLOUR INFORMATION.
SKY_COLOR = "#DDC6A1"
SEA_COLOR = "#92A9CE"
HORIZON_COLOR = "#F5F1DE"
HORIZON_TOP_COLOR = "#D1AA9D"
LINE_COLOR = "#000000"
BUTTON_BG_COLOR = "#33323D"
BUTTON_LINE_COLOR = "#F5F1DE"
# TILE LAYER.
LEVEL_LAYERS = {
    "clouds": 1,
    "ocean": 2,
    "bg": 3,
    "water": 4,
    "main": 5,
}
NEIGHBOR_DIRECTIONS = {
    "A": (0, -1),
    "B": (1, -1),
    "C": (1, 0),
    "D": (1, 1),
    "E": (0, 1),
    "F": (-1, 1),
    "G": (-1, 0),
    "H": (-1, -1),
}
EDITOR_DATA = {
    0: {
        "style": "player",
        "type": "object",
        "menu": None,
        "menu_surf": None,
        "preview": None,
        "graphics": "images/player/idle_right",
    },
    1: {
        "style": "sky",
        "type": "object",
        "menu": None,
        "menu_surf": None,
        "preview": None,
        "graphics": None,
    },
    2: {
        "style": "terrain",
        "type": "tile",
        "menu": "terrain",
        "menu_surf": "images/menu/land.png",
        "preview": "images/preview/land.png",
        "graphics": None,
    },
    3: {
        "style": "water",
        "type": "tile",
        "menu": "terrain",
        "menu_surf": "images/menu/water.png",
        "preview": "images/preview/water.png",
        "graphics": "images/terrain/water/animation",
    },
    4: {
        "style": "coin",
        "type": "tile",
        "menu": "coin",
        "menu_surf": "images/menu/gold.png",
        "preview": "images/preview/gold.png",
        "graphics": "images/items/gold",
    },
    5: {
        "style": "coin",
        "type": "tile",
        "menu": "coin",
        "menu_surf": "images/menu/silver.png",
        "preview": "images/preview/silver.png",
        "graphics": "images/items/silver",
    },
    6: {
        "style": "coin",
        "type": "tile",
        "menu": "coin",
        "menu_surf": "images/menu/diamond.png",
        "preview": "images/preview/diamond.png",
        "graphics": "images/items/diamond",
    },
    7: {
        "style": "enemy",
        "type": "tile",
        "menu": "enemy",
        "menu_surf": "images/menu/spikes.png",
        "preview": "images/preview/spikes.png",
        "graphics": "images/enemies/spikes",
    },
    8: {
        "style": "enemy",
        "type": "tile",
        "menu": "enemy",
        "menu_surf": "images/menu/tooth.png",
        "preview": "images/preview/tooth.png",
        "graphics": "images/enemies/tooth/idle",
    },
    9: {
        "style": "enemy",
        "type": "tile",
        "menu": "enemy",
        "menu_surf": "images/menu/shell_left.png",
        "preview": "images/preview/shell_left.png",
        "graphics": "images/enemies/shell_left/idle",
    },
    10: {
        "style": "enemy",
        "type": "tile",
        "menu": "enemy",
        "menu_surf": "images/menu/shell_right.png",
        "preview": "images/preview/shell_right.png",
        "graphics": "images/enemies/shell_right/idle",
    },
    11: {
        "style": "palm_fg",
        "type": "object",
        "menu": "palm fg",
        "menu_surf": "images/menu/small_fg.png",
        "preview": "images/preview/small_fg.png",
        "graphics": "images/terrain/palm/small_fg",
    },
    12: {
        "style": "palm_fg",
        "type": "object",
        "menu": "palm fg",
        "menu_surf": "images/menu/large_fg.png",
        "preview": "images/preview/large_fg.png",
        "graphics": "images/terrain/palm/large_fg",
    },
    13: {
        "style": "palm_fg",
        "type": "object",
        "menu": "palm fg",
        "menu_surf": "images/menu/left_fg.png",
        "preview": "images/preview/left_fg.png",
        "graphics": "images/terrain/palm/left_fg",
    },
    14: {
        "style": "palm_fg",
        "type": "object",
        "menu": "palm fg",
        "menu_surf": "images/menu/right_fg.png",
        "preview": "images/preview/right_fg.png",
        "graphics": "images/terrain/palm/right_fg",
    },
    15: {
        "style": "palm_bg",
        "type": "object",
        "menu": "palm bg",
        "menu_surf": "images/menu/small_bg.png",
        "preview": "images/preview/small_bg.png",
        "graphics": "images/terrain/palm/small_bg",
    },
    16: {
        "style": "palm_bg",
        "type": "object",
        "menu": "palm bg",
        "menu_surf": "images/menu/large_bg.png",
        "preview": "images/preview/large_bg.png",
        "graphics": "images/terrain/palm/large_bg",
    },
    17: {
        "style": "palm_bg",
        "type": "object",
        "menu": "palm bg",
        "menu_surf": "images/menu/left_bg.png",
        "preview": "images/preview/left_bg.png",
        "graphics": "images/terrain/palm/left_bg",
    },
    18: {
        "style": "palm_bg",
        "type": "object",
        "menu": "palm bg",
        "menu_surf": "images/menu/right_bg.png",
        "preview": "images/preview/right_bg.png",
        "graphics": "images/terrain/palm/right_bg",
    },
}
