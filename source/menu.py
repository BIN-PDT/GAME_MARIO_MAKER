import pygame
from settings import *
from supports import import_image


class Menu:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        # SETUP.
        self.load_assets()
        self.create_menu()

    def load_assets(self):
        self.menu_surfs = {}
        for item_key, item_data in EDITOR_DATA.items():
            menu_key = item_data["menu"]
            if menu_key:
                surf_path = item_data["menu_surf"].removesuffix(".png").split("/")
                menu_item = item_key, import_image(*surf_path)
                if menu_key in self.menu_surfs:
                    self.menu_surfs[menu_key].append(menu_item)
                else:
                    self.menu_surfs[menu_key] = [menu_item]

    def create_menu(self):
        # MENU AREA.
        SIZE, MARGIN = 180, 6
        POS = WINDOW_WIDTH - SIZE - MARGIN, WINDOW_HEIGHT - SIZE - MARGIN
        self.rect = pygame.Rect(POS, (SIZE, SIZE))
        # BUTTON AREA.
        SIZE, MARGIN = SIZE / 2, MARGIN - 1
        GENERIC_RECT = pygame.Rect(POS, (SIZE, SIZE)).inflate(-MARGIN, -MARGIN)
        self.tile_rects = {
            "terrain": GENERIC_RECT.copy(),
            "coin": GENERIC_RECT.move(SIZE, 0),
            "palm": GENERIC_RECT.move(0, SIZE),
            "enemy": GENERIC_RECT.move(SIZE, SIZE),
        }
        # BUTTON GROUP.
        self.buttons = pygame.sprite.Group()
        for tile_name, tile_rect in self.tile_rects.items():
            if tile_name != "palm":
                Button(
                    groups=self.buttons,
                    rect=tile_rect,
                    items=self.menu_surfs[tile_name],
                )
            else:
                Button(
                    groups=self.buttons,
                    rect=tile_rect,
                    items=self.menu_surfs[f"{tile_name} fg"],
                    alt_items=self.menu_surfs[f"{tile_name} bg"],
                )

    def event_click(self, mouse_pos, mouse_buttons):
        for sprite in self.buttons:
            if sprite.rect.collidepoint(mouse_pos):
                # MIDDLE CLICK: SWITCH BETWEEEN 'MAIN' & 'ALT' TYPE.
                if mouse_buttons[1] and sprite.items["alt"]:
                    sprite.main_active = not sprite.main_active
                # RIGHT CLICK: SWITCH ITEM.
                if mouse_buttons[2]:
                    sprite.switch()
                return sprite.get_item_key()

    def draw_highlight(self, index):
        tile_name = EDITOR_DATA[index]["menu"].split(" ")[0]
        rect = self.tile_rects[tile_name].inflate(4, 4)
        pygame.draw.rect(self.screen, BUTTON_LINE_COLOR, rect, 5, 4)

    def display(self, index):
        self.buttons.update()
        self.buttons.draw(self.screen)
        self.draw_highlight(index)


class Button(pygame.sprite.Sprite):
    def __init__(self, groups, rect, items, alt_items=None):
        super().__init__(groups)
        # SETUP.
        self.image = pygame.Surface(rect.size)
        self.rect = rect
        # ITEMS.
        self.items = {"main": items, "alt": alt_items}
        self.item_type, self.item_index = "main", 0

    @property
    def main_active(self):
        return self.item_type == "main"

    @main_active.setter
    def main_active(self, value):
        self.item_type = "main" if value else "alt"

    def get_item_key(self):
        return self.items[self.item_type][self.item_index][0]

    def switch(self):
        self.item_index += 1
        self.item_index %= len(self.items[self.item_type])

    def update(self):
        self.image.fill(BUTTON_BG_COLOR)
        # DRAW ITEM.
        surf = self.items[self.item_type][self.item_index][1]
        rect = surf.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
        self.image.blit(surf, rect)
