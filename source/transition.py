import pygame
from settings import WINDOW_WIDTH, WINDOW_HEIGHT


class Transition:
    def __init__(self, toggle_command):
        self.screen = pygame.display.get_surface()
        # CONTROL.
        self.toggle_command = toggle_command
        self.is_active = False
        # SETUP.
        self.CENTER = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
        self.RADIUS = pygame.math.Vector2(self.CENTER).magnitude()
        self.THRESHOLD = 1, self.RADIUS + 100
        self.border_width = self.THRESHOLD[0]
        self.direction = 1

    def display(self, dt):
        # UPDATE.
        self.border_width += self.direction * 1000 * dt
        # REVERSE ANIMATION.
        if self.border_width > self.THRESHOLD[1]:
            self.border_width = self.THRESHOLD[1]
            self.direction = -1
            self.toggle_command()
        # STOP ANIMATION.
        if self.border_width < self.THRESHOLD[0]:
            self.border_width = self.THRESHOLD[0]
            self.direction = 1
            self.is_active = False
        # DRAW.
        pygame.draw.circle(
            self.screen, "black", self.CENTER, self.RADIUS, int(self.border_width)
        )
