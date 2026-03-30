# app/ui.py
import pygame
from typing import Callable, List
from config import *

# --------------------------------------------------------------------------- #
#  Simple button used by the modal window
# --------------------------------------------------------------------------- #
class Button:
    def __init__(self, rect: pygame.Rect, text: str, callback: Callable):
        self.rect = rect
        self.text = text
        self.callback = callback
        self.hover = False

    def draw(self, surface: pygame.Surface, font: pygame.font.Font):
        color = BUTTON_HOVER_COLOR if self.hover else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect)

        txt = font.render(self.text, True, BUTTON_TEXT_COLOR)
        txt_rect = txt.get_rect(center=self.rect.center)
        surface.blit(txt, txt_rect)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.hover and event.button == 1:
            self.callback()

# --------------------------------------------------------------------------- #
#  Bottom‑right panel (the old “Panel” implementation)
# --------------------------------------------------------------------------- #
class Panel:
    def __init__(self, surface: pygame.Surface,
                 buttons: List[Button],
                 panel_height: int = 50):
        self.surface = surface
        self.buttons = buttons
        self.panel_height = panel_height
        self.base_rects = [b.rect.copy() for b in buttons]
        self.rect = pygame.Rect(0, 0, surface.get_width(), panel_height)

    def update_rects(self):
        self.rect.x = 0
        self.rect.y = self.surface.get_height() - self.panel_height
        for i, button in enumerate(self.buttons):
            button.rect = self.base_rects[i].move(self.rect.topleft)

    def draw(self, font: pygame.font.Font):
        self.update_rects()
        pygame.draw.rect(self.surface, PANEL_BG_COLOR, self.rect)
        for button in self.buttons:
            button.draw(self.surface, font)

    def handle_event(self, event: pygame.event.Event):
        for button in self.buttons:
            button.handle_event(event)

# --------------------------------------------------------------------------- #
#  “x” button for the gallery window
# --------------------------------------------------------------------------- #
class CloseButton:
    def __init__(self, rect: pygame.Rect, callback: Callable):
        self.rect = rect
        self.callback = callback
        self.hover = False

    def draw(self, surface: pygame.Surface):
        color = BUTTON_HOVER_COLOR if self.hover else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect)

        # draw the “x”
        x1, y1 = self.rect.topleft
        x2, y2 = self.rect.bottomright
        pygame.draw.line(surface, BUTTON_TEXT_COLOR, (x1+5, y1+5), (x2-5, y2-5), 2)
        pygame.draw.line(surface, BUTTON_TEXT_COLOR, (x1+5, y2-5), (x2-5, y1+5), 2)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.hover and event.button == 1:
            self.callback()

# --------------------------------------------------------------------------- #
#  Gallery – scrollable window with a close button
# --------------------------------------------------------------------------- #
class Gallery:
    ITEM_HEIGHT = 60          # height of each pattern row
    PADDING = 10              # inner padding
    SCROLL_STEP = 20          # pixels per wheel tick

    def __init__(self, surface: pygame.Surface, rect: pygame.Rect,
                 patterns: List,
                 on_select: Callable[[object], None]):
        self.surface = surface
        self.rect = rect
        self.patterns = patterns
        self.on_select = on_select

        # scroll offset in pixels
        self.scroll_y = 0

        # create a thumbnail for each pattern
        self.thumbs = [self._make_thumb(p) for p in patterns]

        # close button (top‑right corner of the window)
        self.close_btn = CloseButton(
            pygame.Rect(rect.right-30, rect.top+5, 20, 20), self.close)

        # content height (without padding)
        self.content_height = len(patterns) * self.ITEM_HEIGHT

    # --------------------------------------------------------------------- #
    #  create a tiny surface that visualises the pattern
    # --------------------------------------------------------------------- #
    def _make_thumb(self, pattern):
        thumb_w = self.ITEM_HEIGHT - 10
        thumb_h = self.ITEM_HEIGHT - 10
        thumb = pygame.Surface((thumb_w, thumb_h))
        thumb.fill(CELL_DEAD_COLOR)

        cell_size = max(thumb_w // pattern.cells.shape[1], 1)
        for y, row in enumerate(pattern.cells):
            for x, val in enumerate(row):
                if val:
                    rect = pygame.Rect(x*cell_size, y*cell_size, cell_size, cell_size)
                    thumb.fill(CELL_ALIVE_COLOR, rect)

        return thumb

    # --------------------------------------------------------------------- #
    #  draw the window, the list, and the close button
    # --------------------------------------------------------------------- #
    def draw(self, font: pygame.font.Font):
        # background + border
        pygame.draw.rect(self.surface, PANEL_BG_COLOR, self.rect)
        pygame.draw.rect(self.surface, (255,255,255), self.rect, 2)

        # clip the drawing to the window
        clip = self.surface.get_clip()
        self.surface.set_clip(self.rect)

        y_start = self.rect.top + self.PADDING - self.scroll_y
        for idx, pat in enumerate(self.patterns):
            item_rect = pygame.Rect(
                self.rect.left + self.PADDING,
                y_start + idx*self.ITEM_HEIGHT,
                self.rect.width - 2*self.PADDING,
                self.ITEM_HEIGHT)

            # item background
            pygame.draw.rect(self.surface, (70,70,70), item_rect)

            # thumbnail
            thumb = self.thumbs[idx]
            thumb_rect = thumb.get_rect()
            thumb_rect.centery = item_rect.centery
            thumb_rect.left = item_rect.left + 5
            self.surface.blit(thumb, thumb_rect)

            # title
            txt = font.render(pat.title, True, BUTTON_TEXT_COLOR)
            txt_rect = txt.get_rect()
            txt_rect.midleft = (thumb_rect.right + 10, item_rect.centery)
            self.surface.blit(txt, txt_rect)

        # restore clip
        self.surface.set_clip(clip)

        # close button
        self.close_btn.draw(self.surface)

    # --------------------------------------------------------------------- #
    #  event handling – scrolling, pattern click, close button
    # --------------------------------------------------------------------- #
    def handle_event(self, event: pygame.event.Event):
        self.close_btn.handle_event(event)

        # left‑click inside the list
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            list_area = pygame.Rect(
                self.rect.left + self.PADDING,
                self.rect.top + self.PADDING,
                self.rect.width - 2*self.PADDING,
                self.rect.height - 2*self.PADDING)

            if list_area.collidepoint(pos):
                rel_y = pos[1] - list_area.top + self.scroll_y
                idx = rel_y // self.ITEM_HEIGHT
                if 0 <= idx < len(self.patterns):
                    self.on_select(self.patterns[idx])

        # mouse wheel for scrolling
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_y -= event.y * self.SCROLL_STEP
            max_scroll = max(0, self.content_height - (self.rect.height - 2*self.PADDING))
            self.scroll_y = max(0, min(self.scroll_y, max_scroll))

    # --------------------------------------------------------------------- #
    #  callback invoked by the close button
    # --------------------------------------------------------------------- #
    def close(self):
        if hasattr(self, 'on_close'):
            self.on_close()