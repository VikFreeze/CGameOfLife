# app/gallery.py
import pygame
import numpy as np
from ui import Button
from config import PANEL_HEIGHT, FONT_NAME, BUTTON_HEIGHT, BUTTON_PADDING, \
                    BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_TEXT_COLOR, \
                    WINDOW_HEIGHT, WINDOW_WIDTH

# preview cell size
PREVIEW_CELL = 10
# height of one pattern entry in the gallery
ENTRY_HEIGHT = 120
# width of the gallery panel
GALLERY_W = 500
# background colour of the gallery (semi‑transparent)
GALLERY_BG = (0, 0, 0, 200)


class PatternGallery:
    """
    Gallery panel that is shown over the main UI.
    """
    def __init__(self, patterns, on_place_callback):
        """
        :param patterns: list of Pattern objects (from patterns.py)
        :param on_place_callback: called with (pattern, orientation, flip)
        """
        self.patterns = patterns
        self.on_place = on_place_callback
        self.selected = 0
        self.offset_y = 0
        self.closed = False          # flag set by the close button / escape

        self.width = GALLERY_W
        self.height = WINDOW_HEIGHT - PANEL_HEIGHT
        self.x = (WINDOW_WIDTH - self.width) // 2
        self.y = PANEL_HEIGHT

        # prepare UI objects for each pattern
        self.items = []          # list of dicts
        for idx, pat in enumerate(patterns):
            item = {}
            item['pattern'] = pat
            rect = pygame.Rect(self.x, self.y + idx * ENTRY_HEIGHT,
                               self.width, ENTRY_HEIGHT)
            item['rect'] = rect

            # preview surface
            h, w = pat.cells.shape
            preview_surf = pygame.Surface((w * PREVIEW_CELL, h * PREVIEW_CELL), pygame.SRCALPHA)
            for y, row in enumerate(pat.cells):
                for x, alive in enumerate(row):
                    if alive:
                        pygame.draw.rect(
                            preview_surf,
                            (255, 255, 255),
                            (x * PREVIEW_CELL, y * PREVIEW_CELL,
                             PREVIEW_CELL, PREVIEW_CELL)
                        )
            item['preview'] = preview_surf

            # buttons (rotate, mirror, place)
            btn_w = 70
            btn_h = BUTTON_HEIGHT
            btn_pad = BUTTON_PADDING
            base_x = rect.right - btn_pad - btn_w
            base_y = rect.bottom - btn_pad - btn_h

            rotate_btn = Button(pygame.Rect(base_x, base_y, btn_w, btn_h),
                                "Rotate", lambda i=idx: self.rotate(i))
            mirror_btn = Button(pygame.Rect(base_x, base_y - btn_pad - btn_h,
                                            btn_w, btn_h),
                                "Mirror", lambda i=idx: self.mirror(i))
            place_btn  = Button(pygame.Rect(base_x, base_y - 2 * (btn_pad + btn_h),
                                            btn_w, btn_h),
                                "Place", lambda i=idx: self.place(i))

            item['buttons'] = [rotate_btn, mirror_btn, place_btn]
            item['orientation'] = 0  # 0,1,2,3 (90° rotations)
            item['flip'] = False

            self.items.append(item)

        # close button (top‑right corner)
        self.close_btn = Button(
            pygame.Rect(self.x + self.width - 30, self.y + 10, 20, 20),
            "X", self.close
        )

        # font
        self.font = pygame.font.SysFont(FONT_NAME, 18)

    # ------------------------------------------------------------------
    #  Button callbacks
    # ------------------------------------------------------------------
    def rotate(self, idx):
        self.items[idx]['orientation'] = (self.items[idx]['orientation'] + 1) % 4

    def mirror(self, idx):
        self.items[idx]['flip'] = not self.items[idx]['flip']

    def place(self, idx):
        pat = self.items[idx]
        self.on_place(pat['pattern'],
                      pat['orientation'],
                      pat['flip'])
        self.close()

    def close(self):
        self.closed = True

    # ------------------------------------------------------------------
    #  Event handling
    # ------------------------------------------------------------------
    def handle_event(self, event, state):
        """
        Forward events to the buttons and handle scrolling / escape.
        :param event: pygame event
        :param state: AppState instance (not used directly, kept for
                      consistency with the interface in `input_handler`).
        """
        # close button or Escape key
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.close_btn.rect.collidepoint(event.pos):
                self.close()
                return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.close()
                return
            if event.key == pygame.K_UP and self.selected > 0:
                self.selected -= 1
                self.ensure_visible()
            if event.key == pygame.K_DOWN and self.selected < len(self.items) - 1:
                self.selected += 1
                self.ensure_visible()

        # propagate to all buttons
        for item in self.items:
            for btn in item['buttons']:
                btn.handle_event(event)
        self.close_btn.handle_event(event)

    def ensure_visible(self):
        """Scroll so that the selected item is fully visible."""
        top = self.selected * ENTRY_HEIGHT
        bottom = top + ENTRY_HEIGHT
        view_top = -self.offset_y
        view_bottom = view_top + self.height
        if top < view_top:
            self.offset_y = -top
        elif bottom > view_bottom:
            self.offset_y = -(bottom - self.height)

    # ------------------------------------------------------------------
    #  Drawing
    # ------------------------------------------------------------------
    def draw(self, surface):
        """Draw the gallery overlay."""
        # semi‑transparent background
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill(GALLERY_BG)
        surface.blit(overlay, (self.x, self.y))

        # draw each item
        for idx, item in enumerate(self.items):
            # item rectangle
            rect = item['rect'].copy()
            rect.top += self.offset_y
            if rect.bottom < 0 or rect.top > self.height:
                continue   # not visible

            # background of item
            pygame.draw.rect(surface, (50, 50, 50), rect)

            # preview
            surface.blit(item['preview'],
                         (rect.left + 10, rect.centery - item['preview'].get_height() // 2))

            # title
            title_surf = self.font.render(item['pattern'].title, True, (255, 255, 255))
            title_rect = title_surf.get_rect(center=(rect.centerx, rect.centery - 20))
            surface.blit(title_surf, title_rect)

            # description (wrapped to 200 px)
            for i, line in enumerate(self.wrap_text(item['pattern'].description, 200)):
                line_surf = self.font.render(line, True, (200, 200, 200))
                line_rect = line_surf.get_rect(
                    left=rect.left + 150,
                    top=rect.top + 10 + i * 20
                )
                surface.blit(line_surf, line_rect)

            # buttons
            for btn in item['buttons']:
                btn.rect = btn.rect.copy()
                btn.rect.topleft = (btn.rect.left, rect.top + 10)
                btn.draw(surface, self.font)

        # close button
        self.close_btn.draw(surface, self.font)

    def wrap_text(self, text, max_width):
        """Simple word‑wrap for description."""
        words = text.split()
        lines = []
        current = ""
        for w in words:
            test = current + (" " if current else "") + w
            if self.font.size(test)[0] <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = w
        if current:
            lines.append(current)
        return lines