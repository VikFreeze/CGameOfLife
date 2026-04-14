# app/context.py
import pygame
from enum import Enum, auto
from grid import Grid
from viewport import Viewport
from patterns import ALL_PATTERNS
    
class AppContext:
    def __init__(self, screen: pygame.Surface, grid: Grid, viewport: Viewport):
        self.screen          = screen
        self.grid            = grid
        self.viewport        = viewport
        self.fullscreen      = False
        self.state: AppState = AppState.PAUSED
        self.patterns        = ALL_PATTERNS

class AppState(Enum):
    PAUSED          = auto()   # Simulation is paused
    RUNNING         = auto()   # Simulation is running
    GALLERY_OPEN    = auto()   # The pattern gallery UI is visible simulation is paused
    PLACING_PATTERN = auto()   # User is placeing a pattern from the gallery