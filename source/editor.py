import pygame, sys
from pygame.math import Vector2 as Vector
from pygame.key import get_pressed as key_pressed
from pygame.mouse import get_pos as mouse_pos
from pygame.mouse import get_pressed as mouse_pressed
from settings import *

from menu import Menu
from canvas import CanvasTile


class Editor:
    def __init__(self, land_tiles):
        self.screen = pygame.display.get_surface()
        # ASSETS.
        self.land_tiles = land_tiles
        # CONTROL POINT.
        self.origin = Vector()
        self.pan_active = False
        self.pan_offset = Vector()
        # GRID.
        self.grid = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.grid.set_colorkey("green")
        self.grid.set_alpha(30)
        # MENU.
        self.menu = Menu()
        self.selected_index = 2
        # CANVAS.
        self.canvas_data = {}
        self.last_selected_cell = None

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            self.event_mouse(event)
            self.event_keyboard(event)
            self.event_menu(event)
            # CANVAS EVENT.
            self.canvas_create()

    # INPUT.
    def event_mouse(self, event):
        # CHECK MIDDLE MOUSE PRESS.
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_pressed()[1]:
            self.pan_active = True
            self.pan_offset = mouse_pos() - self.origin
        # CHECK MIDDLE MOUSE RELEASE.
        if not mouse_pressed()[1]:
            self.pan_active = False
        # CHECK MOUSE WHEEL.
        if event.type == pygame.MOUSEWHEEL:
            if key_pressed()[pygame.K_LCTRL]:
                self.origin.y -= event.y * TILE_SIZE
            else:
                self.origin.x -= event.y * TILE_SIZE
        # PANNING UPDATE.
        if self.pan_active:
            self.origin = mouse_pos() - self.pan_offset

    def event_keyboard(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.selected_index += 1
            if event.key == pygame.K_LEFT:
                self.selected_index -= 1
        self.selected_index = max(2, min(18, self.selected_index))

    def event_menu(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.menu.rect.collidepoint(mouse_pos()):
                self.selected_index = self.menu.event_click(
                    mouse_pos(), mouse_pressed()
                )

    # SUPPORT.
    def get_selected_cell(self):
        # CO-ORDINATE OF CELL IN GIRD.
        coordinate = (mouse_pos() - self.origin) // TILE_SIZE
        return tuple(map(int, coordinate))

    def check_neighbors(self, cell_pos):
        # LOCAL CLUSTER.
        SIZE = 3
        local_cluster = [
            (cell_pos[0] + col, cell_pos[1] + row)
            for col in range(-1, SIZE - 1)
            for row in range(-1, SIZE - 1)
        ]

        for cell in filter(lambda cell: cell in self.canvas_data, local_cluster):
            # RESET NEIGHBOR ATTRIBUTES.
            self.canvas_data[cell].terrain_neighbors.clear()
            # CHECK NEIGHBORS OF THIS CELL.
            for name, side in NEIGHBOR_DIRECTIONS.items():
                neighbor_cell = cell[0] + side[0], cell[1] + side[1]
                if neighbor_cell in self.canvas_data:
                    if self.canvas_data[neighbor_cell].has_terrain:
                        self.canvas_data[cell].terrain_neighbors.append(name)

    # CANVAS.
    def canvas_create(self):
        if mouse_pressed()[0] and not self.menu.rect.collidepoint(mouse_pos()):
            selected_cell = self.get_selected_cell()
            if selected_cell != self.last_selected_cell:
                if selected_cell in self.canvas_data:
                    self.canvas_data[selected_cell].add_item(self.selected_index)
                else:
                    self.canvas_data[selected_cell] = CanvasTile(self.selected_index)
                # FORMAT SURROUNDING TILES.
                self.check_neighbors(selected_cell)
                # PREVIOUS SELECTED CELL.
                self.last_selected_cell = selected_cell

    # DRAW.
    def draw_grid(self):
        origin_offset = Vector(
            self.origin.x - (self.origin.x // TILE_SIZE) * TILE_SIZE,
            self.origin.y - (self.origin.y // TILE_SIZE) * TILE_SIZE,
        )
        # DRAW GRID.
        self.grid.fill("green")
        for col in range(COLS):
            x = origin_offset.x + col * TILE_SIZE
            pygame.draw.line(self.grid, LINE_COLOR, (x, 0), (x, WINDOW_HEIGHT))
        for row in range(ROWS):
            y = origin_offset.y + row * TILE_SIZE
            pygame.draw.line(self.grid, LINE_COLOR, (0, y), (WINDOW_WIDTH, y))
        self.screen.blit(self.grid, (0, 0))

    def draw_level(self):
        for cell_pos, tile in self.canvas_data.items():
            pos = self.origin + Vector(cell_pos) * TILE_SIZE
            # WATER.
            if tile.has_water:
                surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
                surf.fill("blue")
                self.screen.blit(surf, pos)
            # TERRAIN.
            if tile.has_terrain:
                terrain_type = "".join(tile.terrain_neighbors)
                surf = self.land_tiles.get(terrain_type, self.land_tiles["X"])
                self.screen.blit(surf, pos)
            # COIN.
            if tile.coin:
                surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
                surf.fill("yellow")
                self.screen.blit(surf, pos)
            # ENEMY.
            if tile.enemy:
                surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
                surf.fill("red")
                self.screen.blit(surf, pos)

    def run(self, dt):
        self.screen.fill("white")
        # EVENT LOOP.
        self.event_loop()
        # DRAW.
        self.draw_level()
        self.draw_grid()
        pygame.draw.circle(self.screen, "red", self.origin, 10)
        self.menu.display(self.selected_index)
