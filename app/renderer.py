# app/renderer.py
import pygame
from config import *

def render_grid(surface: pygame.Surface, grid, cell_size: int, offset: tuple):
    """Draw the grid, taking into account the current pan/zoom."""
    offset_x, offset_y = offset
    dead  = CELL_DEAD_COLOR
    alive = CELL_ALIVE_COLOR

    # Very small optimisation: skip cells that are completely off screen
    for y, row in enumerate(grid.cells):
        for x, alive_flag in enumerate(row):
            if alive_flag:
                rect = pygame.Rect(
                    x * cell_size + offset_x,
                    y * cell_size + offset_y,
                    cell_size,
                    cell_size
                )
                surface.fill(alive, rect)


def draw(screen, state, panel, font):
    """Wrapper that draws the entire frame (grid + UI) and flips the display."""
    screen.fill(BG_COLOR)
    render_grid(
        screen,
        state.grid,
        state.viewport.cell_size,
        (state.viewport.offset_x, state.viewport.offset_y)
    )
    panel.draw(font)
    pygame.display.flip()