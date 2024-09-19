import pygame, sys
from pygame.math import Vector2 as Vector
from pygame.key import get_pressed as key_pressed
from pygame.mouse import get_pos as mouse_pos
from pygame.mouse import get_pressed as mouse_pressed
from settings import *
from supports import *
from timers import Timer

from menu import Menu
from canvas import CanvasTile, CanvasObject


class Editor:
    def __init__(self, land_tiles):
        self.screen = pygame.display.get_surface()
        # ASSETS.
        self.load_assets()
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

        self.canvas_objects = pygame.sprite.Group()
        self.drag_active = False
        self.object_timer = Timer(500)
        # DEPENDENT OBJECT.
        self.player = CanvasObject(
            pos=(200, WINDOW_HEIGHT / 2),
            frames=self.animations[0]["frames"],
            groups=self.canvas_objects,
            tile_id=0,
            origin=self.origin,
        )
        self.sky_handle = CanvasObject(
            pos=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2),
            frames=[self.sky_handle_surf],
            groups=self.canvas_objects,
            tile_id=1,
            origin=self.origin,
        )

    def load_assets(self):
        # DEPENDENT ASSETS.
        self.water_bot = import_image("images", "terrain", "water", "water_bottom")
        self.sky_handle_surf = import_image("images", "cursors", "handle")
        # ANIMATION ASSETS.
        self.animations = {}
        for key, value in EDITOR_DATA.items():
            if value["graphics"]:
                frames_path = value["graphics"].split("/")
                frames = import_folder_list(*frames_path)
                self.animations[key] = {
                    "frame index": 0,
                    "frames": frames,
                    "length": len(frames),
                }

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            self.event_mouse(event)
            self.event_keyboard(event)
            self.event_menu(event)
            # CANVAS EVENT.
            self.canvas_drag(event)
            self.canvas_create()
            self.canvas_delete()

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
            # ORIGIN.
            self.origin = mouse_pos() - self.pan_offset
            # OBJECT.
            for sprite in self.canvas_objects:
                sprite.pan_pos(self.origin)

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

    def get_selected_object(self):
        for sprite in self.canvas_objects:
            if sprite.rect.collidepoint(mouse_pos()):
                return sprite

    def check_neighbors(self, cell_pos):
        # LOCAL CLUSTER.
        SIZE = 3
        local_cluster = [
            (cell_pos[0] + col, cell_pos[1] + row)
            for col in range(-1, SIZE - 1)
            for row in range(-1, SIZE - 1)
        ]

        for cell in filter(lambda cell: cell in self.canvas_data, local_cluster):
            tile = self.canvas_data[cell]
            # RESET NEIGHBOR ATTRIBUTES.
            tile.terrain_neighbors.clear()
            tile.water_on_top = False
            # CHECK NEIGHBORS OF THIS TILE.
            for name, side in NEIGHBOR_DIRECTIONS.items():
                neighbor_cell = cell[0] + side[0], cell[1] + side[1]
                if neighbor_cell in self.canvas_data:
                    neighbor_tile = self.canvas_data[neighbor_cell]
                    # TERRAIN NEIGHBORS.
                    if neighbor_tile.has_terrain:
                        tile.terrain_neighbors.append(name)
                    # WATER ON TOP.
                    if name == "A" and tile.has_water and neighbor_tile.has_water:
                        tile.water_on_top = True

    def update_animation(self, dt):
        for value in self.animations.values():
            value["frame index"] += ANIMATION_SPEED * dt
            value["frame index"] %= value["length"]

    # CANVAS.
    def canvas_create(self):
        if (
            mouse_pressed()[0]
            and not self.drag_active
            and not self.menu.rect.collidepoint(mouse_pos())
        ):
            if EDITOR_DATA[self.selected_index]["type"] == "tile":
                cell = self.get_selected_cell()
                if cell != self.last_selected_cell:
                    if cell in self.canvas_data:
                        self.canvas_data[cell].add_item(self.selected_index)
                    else:
                        self.canvas_data[cell] = CanvasTile(self.selected_index)
                    # FORMAT SURROUNDING TILES.
                    if EDITOR_DATA[self.selected_index]["menu"] == "terrain":
                        self.check_neighbors(cell)
                    # PREVIOUS SELECTED CELL.
                    self.last_selected_cell = cell
            else:
                if not self.object_timer.is_active:
                    self.object_timer.activate()
                    CanvasObject(
                        pos=mouse_pos(),
                        frames=self.animations[self.selected_index]["frames"],
                        groups=self.canvas_objects,
                        tile_id=self.selected_index,
                        origin=self.origin,
                    )

    def canvas_delete(self):
        if mouse_pressed()[2] and not self.menu.rect.collidepoint(mouse_pos()):
            # OBJECT.
            selected_object = self.get_selected_object()
            if selected_object and selected_object.tile_id not in (0, 1):
                selected_object.kill()
            # TILE.
            selected_cell = self.get_selected_cell()
            if selected_cell in self.canvas_data:
                self.canvas_data[selected_cell].del_item(self.selected_index)
                # REMOVE EMPTY TILE.
                if self.canvas_data[selected_cell].is_empty:
                    del self.canvas_data[selected_cell]
                # FORMAT SURROUNDING TILES.
                if EDITOR_DATA[self.selected_index]["menu"] == "terrain":
                    self.check_neighbors(selected_cell)

    def canvas_drag(self, event):
        # START DRAG.
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_pressed()[0]:
            for sprite in self.canvas_objects:
                if sprite.rect.collidepoint(event.pos):
                    self.drag_active = True
                    sprite.start_drag()
        # END DRAG.
        if event.type == pygame.MOUSEBUTTONUP and self.drag_active:
            for sprite in self.canvas_objects:
                if sprite.is_selected:
                    self.drag_active = False
                    sprite.end_drag(self.origin)

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
        # TILE.
        for cell_pos, tile in self.canvas_data.items():
            pos = self.origin + Vector(cell_pos) * TILE_SIZE
            # WATER.
            if tile.has_water:
                if tile.water_on_top:
                    self.screen.blit(self.water_bot, pos)
                else:
                    frames = self.animations[3]["frames"]
                    index = int(self.animations[3]["frame index"])
                    surf = frames[index]
                    self.screen.blit(surf, pos)
            # TERRAIN.
            if tile.has_terrain:
                terrain_type = "".join(tile.terrain_neighbors)
                surf = self.land_tiles.get(terrain_type, self.land_tiles["X"])
                self.screen.blit(surf, pos)
            # COIN.
            if tile.coin:
                frames = self.animations[tile.coin]["frames"]
                index = int(self.animations[tile.coin]["frame index"])
                surf = frames[index]
                rect = surf.get_rect(center=Vector(pos) + COIN_OFFSET)
                self.screen.blit(surf, rect)
            # ENEMY.
            if tile.enemy:
                frames = self.animations[tile.enemy]["frames"]
                index = int(self.animations[tile.enemy]["frame index"])
                surf = frames[index]
                rect = surf.get_rect(midbottom=Vector(pos) + ENEMY_OFFSET)
                self.screen.blit(surf, rect)
        # OBJECT.
        self.canvas_objects.draw(self.screen)

    def run(self, dt):
        self.screen.fill("white")
        # EVENT LOOP.
        self.event_loop()
        # UPDATE.
        self.object_timer.update()
        self.update_animation(dt)
        self.canvas_objects.update(dt)
        # DRAW.
        self.draw_level()
        self.draw_grid()
        pygame.draw.circle(self.screen, "red", self.origin, 10)
        self.menu.display(self.selected_index)
