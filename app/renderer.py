# app/renderer.py
import pygame
from config import *
def render_grid(surface: pygame.Surface, grid, cell_size: int, offset: tuple):
    """Draw the grid, taking into account the current pan/zoom."""
    offset_x, offset_y = offset
    alive = CELL_ALIVE_COLOR
    for y, row in enumerate(grid.cells):
        for x, flag in enumerate(row):
            if flag:
                rect = pygame.Rect(x*cell_size + offset_x,
                                   y*cell_size + offset_y,
                                   cell_size, cell_size)
                surface.fill(alive, rect)

def draw(screen, ctx, panel, font):
    """Wrapper that draws the entire frame and flips the display."""
    screen.fill(BG_COLOR)
    render_grid(screen, ctx.grid, ctx.viewport.cell_size,
                (ctx.viewport.offset_x, ctx.viewport.offset_y))
    if panel:                 # guard against None
        panel.draw(font)
    pygame.display.flip()