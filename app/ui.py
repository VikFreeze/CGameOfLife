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
            if self.hover and event.button == 1:   # left click
                self.callback()

class Panel:
    """Bottom panel that holds a list of buttons."""
    def __init__(self, surface: pygame.Surface, buttons: List[Button]):
        self.surface = surface
        self.buttons = buttons
        self.rect = pygame.Rect(0, WINDOW_HEIGHT - PANEL_HEIGHT,
                                WINDOW_WIDTH, PANEL_HEIGHT)

    def draw(self, font: pygame.font.Font):
        pygame.draw.rect(self.surface, (50, 50, 50), self.rect)
        for btn in self.buttons:
            btn.draw(self.surface, font)

    def handle_event(self, event: pygame.event.Event):
        for btn in self.buttons:
            btn.handle_event(event)