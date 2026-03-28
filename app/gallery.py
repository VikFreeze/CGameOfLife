# app/gallery.py
import pygame
import math
import textwrap
from .config import *
from .patterns import PATTERNS

# --------------------------------------------------------------------
# Utility functions
# --------------------------------------------------------------------
def rotate_matrix(mat, k):
    """Rotate `mat` by 90° `k` times (clockwise)."""
    return np.rot90(mat, -k)   # -k for clockwise

def mirror_matrix(mat):
    """Mirror horizontally."""
    return np.fliplr(mat)

# --------------------------------------------------------------------
# A single gallery item
# --------------------------------------------------------------------
class GalleryItem:
    def __init__(self, pattern):
        self.name        = pattern['name']
        self.description = pattern['description']
        self.base_matrix = pattern['matrix']
        self.matrix      = pattern['matrix']      # will be transformed
        self.rotation    = 0                      # 0–3 (90° each)
        self.mirrored    = False

        # create a preview surface that we will keep scaled to 1:1
        self.preview_surf = self._make_preview()

    # --------------------------------------------------------------------
    def _make_preview(self):
        h, w = self.matrix.shape
        surf = pygame.Surface((w * CELL_SIZE, h * CELL_SIZE), pygame.SRCALPHA)
        for y in range(h):
            for x in range(w):
                if self.matrix[y, x]:
                    pygame.draw.rect(surf, (200,200,200,255),
                                     pygame.Rect(x*CELL_SIZE, y*CELL_SIZE,
                                                 CELL_SIZE, CELL_SIZE))
        return surf

    # --------------------------------------------------------------------
    def update_preview(self):
        self.matrix = rotate_matrix(self.base_matrix, self.rotation)
        if self.mirrored:
            self.matrix = mirror_matrix(self.matrix)
        self.preview_surf = self._make_preview()

    # --------------------------------------------------------------------
    def on_wheel(self, delta):
        self.rotation = (self.rotation + delta) % 4
        self.update_preview()

    def on_right_click(self):
        self.mirrored = not self.mirrored
        self.update_preview()

# --------------------------------------------------------------------
# The whole gallery
# --------------------------------------------------------------------
class Gallery:
    """Overlay gallery – draws on top of the grid and blocks all other input."""
    def __init__(self, surface, font):
        self.surface = surface
        self.font    = font

        # build items from the global PATTERNS list
        self.items   = [GalleryItem(p) for p in PATTERNS]

        # scrolling state
        self.scroll_y = 0
        self.item_height = 200
        self.item_margin = 10

        # button to confirm placement (created later per item)
        self.place_button_cls = None  # will hold a reference to Button class

    # --------------------------------------------------------------------
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:          # wheel up
                self.scroll_y = min(self.scroll_y + 20, 0)
            elif event.button == 5:        # wheel down
                max_scroll = min(0, self.surface.get_height() - len(self.items)*(self.item_height+self.item_margin))
                self.scroll_y = max(self.scroll_y - 20, max_scroll)
            elif event.button == 3:        # right click – mirror
                mx, my = event.pos
                self._try_mirror(mx, my)
            elif event.button == 1:        # left click – maybe a button
                mx, my = event.pos
                self._try_select(mx, my)

    # --------------------------------------------------------------------
    def _try_mirror(self, mx, my):
        """If the mouse is over a preview, mirror that item."""
        for idx, item in enumerate(self.items):
            preview_rect = self._preview_rect(idx)
            if preview_rect.collidepoint(mx, my):
                item.on_right_click()
                break

    def _try_select(self, mx, my):
        """If the click is on a Place button, return that item."""
        for idx, item in enumerate(self.items):
            button_rect = self._button_rect(idx)
            if button_rect.collidepoint(mx, my):
                # user chose this pattern
                self.selected_item = item
                return item
        return None

    # --------------------------------------------------------------------
    def _preview_rect(self, idx):
        """Rect of the preview part of item `idx` – relative to screen."""
        x = 20
        y = 20 + idx * (self.item_height + self.item_margin) + self.scroll_y
        w = self.item_height
        h = self.item_height
        return pygame.Rect(x, y, w, h)

    def _button_rect(self, idx):
        """Rect of the 'Place on grid' button for item `idx`."""
        x = 20 + self.item_height + 20
        y = 20 + idx * (self.item_height + self.item_margin) + self.scroll_y + self.item_height // 2
        w = 120
        h = BUTTON_HEIGHT
        return pygame.Rect(x, y, w, h)

    # --------------------------------------------------------------------
    def draw(self):
        # draw a semi‑transparent background
        overlay = pygame.Surface(self.surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.surface.blit(overlay, (0, 0))

        # draw each item
        for idx, item in enumerate(self.items):
            # background box
            box_rect = pygame.Rect(20, 20 + idx*(self.item_height+self.item_margin)+self.scroll_y,
                                   self.surface.get_width()-40, self.item_height)
            pygame.draw.rect(self.surface, (30,30,30), box_rect)

            # preview
            preview_rect = self._preview_rect(idx)
            self.surface.blit(item.preview_surf, preview_rect)

            # title
            title_surf = self.font.render(item.name, True, (255,255,255))
            self.surface.blit(title_surf, (preview_rect.right+10, preview_rect.top))

            # description – wrap
            desc_lines = textwrap.wrap(item.description, 60)
            for i, line in enumerate(desc_lines):
                line_surf = self.font.render(line, True, (200,200,200))
                self.surface.blit(line_surf,
                                  (preview_rect.right+10, preview_rect.top + 20 + i*15))

            # Place button
            button_rect = self._button_rect(idx)
            pygame.draw.rect(self.surface, BUTTON_BG_COLOR, button_rect)
            btn_text = self.font.render('Place on grid', True, (255,255,255))
            self.surface.blit(btn_text,
                              button_rect.move((button_rect.width - btn_text.get_width())//2,
                                               (button_rect.height - btn_text.get_height())//2))