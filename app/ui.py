# app/ui.py
import pygame
from typing import Callable

# ------------------------------------------------------------------ #
#  “x” button for the gallery window
# ------------------------------------------------------------------ #
class CloseButton:
    def __init__(self, rect: pygame.Rect, callback: Callable):
        # self.rect = rect
        # self.callback = callback
        # self.hover = False
        pass

    def draw(self, surface: pygame.Surface):
        # color = (100, 100, 100) if self.hover else (70, 70, 70)
        # pygame.draw.rect(surface, color, self.rect)
        # # draw the “x”
        # x1, y1 = self.rect.topleft
        # x2, y2 = self.rect.bottomright
        # pygame.draw.line(surface, (255, 255, 255), (x1 + 5, y1 + 5), (x2 - 5, y2 - 5), 2)
        # pygame.draw.line(surface, (255, 255, 255), (x1 + 5, y2 - 5), (x2 - 5, y1 + 5), 2)
        pass

    def handle_event(self, event: pygame.event.Event):
        # if event.type == pygame.MOUSEMOTION:
        #     self.hover = self.rect.collidepoint(event.pos)
        # elif event.type == pygame.MOUSEBUTTONDOWN and self.hover and event.button == 1:
        #     self.callback()
        pass