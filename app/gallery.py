# app/gallery.py
"""
A lightweight, scrollable gallery widget that lists all patterns
defined in :py:mod:`patterns`.

Usage
-----
>>> from gallery import Gallery
>>> gallery = Gallery(surface, rect, on_select=your_callback)
"""

from __future__ import annotations

import numpy as np
import pygame
from dataclasses import dataclass, field
from typing import Callable, List

# ─────────────────────── Imports from the rest of the project ──────── #
from config import (
    FONT_NAME,
    BUTTON_HEIGHT,
    BUTTON_PADDING,
    BUTTON_COLOR,
    BUTTON_HOVER_COLOR,
    BUTTON_TEXT_COLOR,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    PREVIEW_CELL,
)
from ui import Button, CloseButton      # already defined in ui.py
from patterns import ALL_PATTERNS, Pattern

# ──────────────────────── Helper: create a preview surface ──────── #
def _make_thumb(pattern: Pattern, scale: int = 10) -> pygame.Surface:
    """Return a pygame.Surface that visualises the pattern."""
    h, w = pattern.cells.shape
    surf = pygame.Surface((w * scale, h * scale))
    surf.fill((0, 0, 0))

    alive = (255, 255, 255)
    for y in range(h):
        for x in range(w):
            if pattern.cells[y, x]:
                rect = pygame.Rect(x * scale, y * scale, scale, scale)
                surf.fill(alive, rect)
    return surf


# ──────────────────────── Data structure for a list entry ──────── #
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
        """Generate a new preview image that respects orientation / flips."""
        cells = self.pattern.cells.astype(int)

        # flips
        if self.flip_x:
            cells = np.flip(cells, axis=1)
        if self.flip_y:
            cells = np.flip(cells, axis=0)

        # rotations
        cells = np.rot90(cells, k=self.orientation)

        # create surface
        h, w = cells.shape
        scale = PREVIEW_CELL
        surf = pygame.Surface((w * scale, h * scale))
        surf.fill((0, 0, 0))
        for y in range(h):
            for x in range(w):
                if cells[y, x]:
                    rect = pygame.Rect(x * scale, y * scale, scale, scale)
                    surf.fill((255, 255, 255), rect)
        self.preview = surf


# ──────────────────────── The Gallery widget ──────────────────────── #
class Gallery:
    """
    Parameters
    ----------
    surface : pygame.Surface
        Main surface that the gallery will be drawn onto.
    rect : pygame.Rect
        Position & size of the gallery window.
    on_select : Callable[[Pattern, int, bool, bool], None]
        Called when the user presses the *Place* button for a pattern.
    on_close : Callable[[], None] | None
        Optional callback that is invoked when the gallery is closed.
    """

    ITEM_HEIGHT = 110
    ITEM_PADDING = 8
    SCROLL_STEP = 20

    def __init__(
        self,
        surface: pygame.Surface,
        rect: pygame.Rect,
        on_select: Callable[[Pattern, int, bool, bool], None],
        on_close: Callable[[], None] | None = None,
    ):
        self.surface = surface
        self.rect = rect
        self.on_select = on_select
        self.on_close = on_close

        # create a GalleryItem for each pattern
        self.items: List[GalleryItem] = [GalleryItem(p) for p in ALL_PATTERNS]

        # scrolling
        self.scroll_y = 0

        # close button
        close_rect = pygame.Rect(
            self.rect.right - 30, self.rect.top + 5, 20, 20
        )
        self.close_btn = CloseButton(close_rect, self.close)

        # font
        self.font = pygame.font.SysFont(FONT_NAME, 16)

    # ------------------------------------------------------------------ #
    #  Rendering helpers
    # ------------------------------------------------------------------ #
    def _draw_item(self, item: GalleryItem, top: int):
        """Draw a single item at the given y‑coordinate."""
        # background
        bg_rect = pygame.Rect(
            self.rect.left + self.ITEM_PADDING,
            top,
            self.rect.width - 2 * self.ITEM_PADDING,
            self.ITEM_HEIGHT,
        )
        pygame.draw.rect(self.surface, (60, 60, 60), bg_rect)

        # preview on the left
        preview_rect = item.preview.get_rect()
        preview_rect.midleft = (bg_rect.left + 30, bg_rect.centery)
        self.surface.blit(item.preview, preview_rect)

        # title (centered)
        title_surf = self.font.render(item.pattern.title, True, (255, 255, 255))
        title_rect = title_surf.get_rect()
        title_rect.midtop = (bg_rect.centerx, bg_rect.top + 5)
        self.surface.blit(title_surf, title_rect)

        # description (wrapped)
        for i, line in enumerate(self._wrap_text(item.pattern.description, 200)):
            line_surf = self.font.render(line, True, (180, 180, 180))
            line_rect = line_surf.get_rect()
            line_rect.left = preview_rect.right + 15
            line_rect.top = bg_rect.top + 5 + i * 18
            self.surface.blit(line_surf, line_rect)

        # buttons (below title)
        btns = [
            ("←", lambda: item.rotate_left()),
            ("→", lambda: item.rotate_right()),
            ("H", lambda: item.mirror_x()),
            ("V", lambda: item.mirror_y()),
            ("✚", lambda: self._place(item)),
        ]
        btn_w = 35
        btn_h = BUTTON_HEIGHT
        btn_x = bg_rect.right - (len(btns) * (btn_w + 5)) - 5
        btn_y = bg_rect.bottom - btn_h - 5
        for txt, cb in btns:
            btn_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
            btn = Button(btn_rect, txt, cb)
            btn.draw(self.surface, self.font)
            btn_x += btn_w + 5

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

    # ------------------------------------------------------------------ #
    #  Place callback (delegated to the state machine)
    # ------------------------------------------------------------------ #
    def _place(self, item: GalleryItem):
        """Invoke the user supplied callback."""
        # `on_select` receives (Pattern, orientation, flip_x, flip_y)
        self.on_select(item.pattern, item.orientation, item.flip_x, item.flip_y)

    # ------------------------------------------------------------------ #
    #  Public API
    # ------------------------------------------------------------------ #
    def draw(self, _font: pygame.font.Font | None = None):
        """Draw the entire gallery onto the main surface."""
        # 1️⃣  background & border
        pygame.draw.rect(self.surface, (30, 30, 30), self.rect)
        pygame.draw.rect(self.surface, (200, 200, 200), self.rect, 2)

        # 2️⃣  clip to window
        old_clip = self.surface.get_clip()
        self.surface.set_clip(self.rect)

        # 3️⃣  draw only the visible items
        y = self.rect.top + self.ITEM_PADDING - self.scroll_y
        for idx in range(len(self.items)):
            self._draw_item(self.items[idx], y)
            y += self.ITEM_HEIGHT
            if y > self.rect.bottom:
                break

        # 4️⃣  restore clipping
        self.surface.set_clip(old_clip)

        # 5️⃣  close button
        self.close_btn.draw(self.surface)

    def handle_event(self, event: pygame.event.Event):
        """Close button + scrolling."""
        self.close_btn.handle_event(event)

        if event.type == pygame.MOUSEWHEEL:
            new_offset = self.scroll_y - event.y * self.SCROLL_STEP
            max_offset = max(0, len(self.items) * self.ITEM_HEIGHT - self.rect.height + 2 * self.ITEM_PADDING)
            self.scroll_y = max(0, min(new_offset, max_offset))

    def close(self):
        """Set the internal closed flag and call the optional callback."""
        self.closed = True
        if self.on_close:
            self.on_close()

    @property
    def closed(self) -> bool:
        return getattr(self, "_closed", False)

    @closed.setter
    def closed(self, value: bool):
        self._closed = value