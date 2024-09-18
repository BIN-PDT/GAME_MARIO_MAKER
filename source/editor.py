import pygame, sys
from pygame.math import Vector2 as Vector
from pygame.key import get_pressed as key_pressed
from pygame.mouse import get_pos as mouse_pos
from pygame.mouse import get_pressed as mouse_pressed
from settings import *

from menu import Menu


class Editor:
    def __init__(self):
        self.screen = pygame.display.get_surface()
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

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            self.event_mouse(event)
            self.event_keyboard(event)
            self.event_menu(event)

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

    def run(self, dt):
        self.screen.fill("white")
        # EVENT LOOP.
        self.event_loop()
        # DRAW.
        self.draw_grid()
        pygame.draw.circle(self.screen, "red", self.origin, 10)
        self.menu.display(self.selected_index)
