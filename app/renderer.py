# app/renderer.py
import pygame
from config import *

def render_grid(surface: pygame.Surface, grid, cell_size: int):
    """Draw the grid onto the given surface."""
    cell_dead = CELL_DEAD_COLOR
    cell_alive = CELL_ALIVE_COLOR
    for y, row in enumerate(grid.cells):
        for x, alive in enumerate(row):
            color = cell_alive if alive else cell_dead
            rect = pygame.Rect(x * cell_size, y * cell_size,
                               cell_size, cell_size)
            surface.fill(color, rect)