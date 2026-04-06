# app/gallery.py
import numpy as np
import pygame
from dataclasses import dataclass, field
from typing import Callable, List
# Imports from the rest of the project
from config import (
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    PREVIEW_CELL,
)
from patterns import ALL_PATTERNS, Pattern

# ----------------------------------------------------------------------
#  Helper: create a preview surface
# ----------------------------------------------------------------------
def _make_thumb(pattern: Pattern, scale: int = 8) -> pygame.Surface:
    h, w = pattern.cells.shape
    surf = pygame.Surface((w * scale, h * scale))
    surf.fill(CELL_DEAD_COLOR)
    alive = CELL_ALIVE_COLOR
    for y in range(h):
        for x in range(w):
            if pattern.cells[y, x]:
                rect = pygame.Rect(x * scale, y * scale, scale, scale)
                surf.fill(alive, rect)
    return surf

# ----------------------------------------------------------------------
#  Gallery item data
# ----------------------------------------------------------------------
@dataclass
class GalleryItem:
    pattern: Pattern
    orientation: int = 0          # 0–3  (90° rotations)
    flip_x: bool = False
    flip_y: bool = False
    preview: pygame.Surface = field(default_factory=lambda: None)

    def __post_init__(self):
        self.update_preview()

    def rotate_left(self):
        self.orientation = (self.orientation - 1) % 4
        self.update_preview()

    def rotate_right(self):
        self.orientation = (self.orientation + 1) % 4
        self.update_preview()

    def mirror_x(self):
        self.flip_x = not self.flip_x
        self.update_preview()

    def mirror_y(self):
        self.flip_y = not self.flip_y
        self.update_preview()

    def update_preview(self):
        cells = self.pattern.cells.astype(int)
        if self.flip_x:
            cells = np.flip(cells, axis=1)
        if self.flip_y:
            cells = np.flip(cells, axis=0)
        cells = np.rot90(cells, k=self.orientation)
        h, w = cells.shape
        surf = pygame.Surface((w * PREVIEW_CELL, h * PREVIEW_CELL))
        surf.fill(CELL_DEAD_COLOR)
        alive = CELL_ALIVE_COLOR
        for y in range(h):
            for x in range(w):
                if cells[y, x]:
                    rect = pygame.Rect(x * PREVIEW_CELL, y * PREVIEW_CELL,
                                       PREVIEW_CELL, PREVIEW_CELL)
                    surf.fill(alive, rect)
        self.preview = surf

# ----------------------------------------------------------------------
#  Gallery widget – keyboard only
# ----------------------------------------------------------------------
class Gallery:
    ITEM_HEIGHT = 60
    PADDING = 10
    SCROLL_STEP = 20

    def __init__(self, surface: pygame.Surface, rect: pygame.Rect,
                 on_select: Callable[[Pattern, int, bool, bool], None]):
        self.surface = surface
        self.rect = rect
        self.on_select = on_select
        self.items: List[GalleryItem] = [GalleryItem(p) for p in ALL_PATTERNS]
        self.scroll_y = 0
        self.selected_index = 0
        self.font = pygame.font.SysFont(FONT_NAME, 16)

    # ------------------------------------------------------------------
    #  Rendering helpers
    # ------------------------------------------------------------------
    def _draw_item(self, item: GalleryItem, top: int, selected: bool):
        bg_rect = pygame.Rect(
            self.rect.left + self.PADDING,
            top,
            self.rect.width - 2 * self.PADDING,
            self.ITEM_HEIGHT,
        )
        pygame.draw.rect(self.surface, (60, 60, 60), bg_rect)
        if selected:
            pygame.draw.rect(self.surface, (200, 200, 200), bg_rect, 3)

        # preview
        preview_rect = item.preview.get_rect()
        preview_rect.midleft = (bg_rect.left + 30, bg_rect.centery)
        self.surface.blit(item.preview, preview_rect)

        # title
        title_surf = self.font.render(item.pattern.title, True, (255, 255, 255))
        title_rect = title_surf.get_rect()
        title_rect.midtop = (bg_rect.centerx, bg_rect.top + 5)
        self.surface.blit(title_surf, title_rect)

        # description
        for i, line in enumerate(self._wrap_text(item.pattern.description, 200)):
            line_surf = self.font.render(line, True, (180, 180, 180))
            line_rect = line_surf.get_rect()
            line_rect.left = preview_rect.right + 15
            line_rect.top = bg_rect.top + 5 + i * 18
            self.surface.blit(line_surf, line_rect)

    def _wrap_text(self, text: str, max_width: int) -> List[str]:
        words = text.split()
        lines: List[str] = []
        cur = ""
        for w in words:
            test = cur + (" " if cur else "") + w
            if self.font.size(test)[0] <= max_width:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    # ------------------------------------------------------------------
    #  Place callback
    # ------------------------------------------------------------------
    def _place(self):
        item = self.items[self.selected_index]
        self.on_select(item.pattern, item.orientation,
                       item.flip_x, item.flip_y)

    # ------------------------------------------------------------------
    #  Public API
    # ------------------------------------------------------------------
    def draw(self, _font: pygame.font.Font | None = None):
        pygame.draw.rect(self.surface, (30, 30, 30), self.rect)
        pygame.draw.rect(self.surface, (200, 200, 200), self.rect, 2)

        # clip to window
        old_clip = self.surface.get_clip()
        self.surface.set_clip(self.rect)

        y = self.rect.top + self.PADDING - self.scroll_y
        for idx, item in enumerate(self.items):
            self._draw_item(item, y, idx == self.selected_index)
            y += self.ITEM_HEIGHT
            if y > self.rect.bottom:
                break

        self.surface.set_clip(old_clip)

    # ------------------------------------------------------------------
    #  Event handling – keyboard + mouse wheel
    # ------------------------------------------------------------------
    def handle_event(self, event: pygame.event.Event):
        # close on ESC (handled by parent)
        if event.type == pygame.MOUSEWHEEL:
            new_offset = self.scroll_y - event.y * self.SCROLL_STEP
            max_offset = max(0,
                             len(self.items) * self.ITEM_HEIGHT - (self.rect.height - 2 * self.PADDING))
            self.scroll_y = max(0, min(new_offset, max_offset))
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if self.selected_index < len(self.items) - 1:
                    self.selected_index += 1
                    # ensure visible
                    self._ensure_visible()
            elif event.key == pygame.K_UP:
                if self.selected_index > 0:
                    self.selected_index -= 1
                    self._ensure_visible()
            elif event.key == pygame.K_LEFT:
                self.items[self.selected_index].rotate_left()
            elif event.key == pygame.K_RIGHT:
                self.items[self.selected_index].rotate_right()
            elif event.key == pygame.K_h:
                self.items[self.selected_index].mirror_x()
            elif event.key == pygame.K_v:
                self.items[self.selected_index].mirror_y()
            elif event.key == pygame.K_p:
                self._place()

    def _ensure_visible(self):
        """Scroll the list so that the selected item stays on‑screen."""
        idx = self.selected_index
        item_top = idx * self.ITEM_HEIGHT
        visible_top = self.scroll_y
        visible_bottom = self.scroll_y + self.rect.height - 2 * self.PADDING
        if item_top < visible_top:
            self.scroll_y = item_top
        elif item_top + self.ITEM_HEIGHT > visible_bottom:
            self.scroll_y = item_top + self.ITEM_HEIGHT - (self.rect.height - 2 * self.PADDING)

    def close(self):
        """No-op – the caller (GalleryState) handles the close."""
        pass