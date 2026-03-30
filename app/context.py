# app/context.py
import pygame
from grid import Grid
from viewport import Viewport
from patterns import ALL_PATTERNS

class AppContext:
    """All objects that are needed by any state."""
    def __init__(self, screen: pygame.Surface, grid: Grid, viewport: Viewport):
        self.screen       = screen
        self.grid         = grid
        self.viewport     = viewport
        self.panel_height = 60
        self.font         = pygame.font.SysFont("Arial", 18)

        # Pattern list for the gallery
        self.patterns = ALL_PATTERNS