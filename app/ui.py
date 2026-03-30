# app/ui.py
import pygame
from config import *
from typing import Callable, List

class Button:
    def __init__(self, rect: pygame.Rect, text: str, callback: Callable):
        self.rect = rect
        self.text = text
        self.callback = callback
        self.hover = False

    def draw(self, surface: pygame.Surface, font: pygame.font.Font):
        color = BUTTON_HOVER_COLOR if self.hover else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect)
        txt_surf = font.render(self.text, True, BUTTON_TEXT_COLOR)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        surface.blit(txt_surf, txt_rect)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hover and event.button == 1:
                self.callback()

class Panel:
    def __init__(self, surface: pygame.Surface, buttons: List[Button], panel_height: int = 50):
        self.surface      = surface
        self.buttons      = buttons
        self.panel_height = panel_height
        # Remember the base rectangles to rebuild the panel each draw
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