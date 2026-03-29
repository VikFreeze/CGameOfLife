# app/state.py
from dataclasses import dataclass, field
import pygame
from grid import Grid
from viewport import Viewport

@dataclass
class AppState:
    """Runtime state shared between the different helper modules."""
    grid: Grid
    viewport: Viewport
    running: bool = False
    pressed_keys: set = field(default_factory=set)
    dragging: bool = False
    drag_button: int = 0
    panel_height: int = 60
    window_height: int = 1080  # will be overridden by main()

    def toggle_run(self):
        """Switch between running / paused."""
        self.running = not self.running

    def reset(self):
        """Stop simulation, clear grid and reset view."""
        self.running = False
        self.grid.reset()
        self.viewport.offset_x = self.viewport.offset_y = 0
        self.viewport.clamp_offset()

    def update_pan(self, pan_step: int):
        """Move the viewport when arrow keys are held down."""
        import pygame  # import here to avoid circular import
        if pygame.K_LEFT in self.pressed_keys:
            self.viewport.offset_x += pan_step
            self.viewport.clamp_offset()
        if pygame.K_RIGHT in self.pressed_keys:
            self.viewport.offset_x -= pan_step
            self.viewport.clamp_offset()
        if pygame.K_UP in self.pressed_keys:
            self.viewport.offset_y += pan_step
            self.viewport.clamp_offset()
        if pygame.K_DOWN in self.pressed_keys:
            self.viewport.offset_y -= pan_step
            self.viewport.clamp_offset()