# app/renderer.py
import pygame
from config import *

def render_grid(surface: pygame.Surface, grid, cell_size: int, offset: tuple):
    """
    Draw the grid with wrap‑around using a single blit.

    Parameters
    ----------
    surface : pygame.Surface
        Destination surface (the screen).
    grid : object
        The simulation grid; must expose `cells`, `width`, `height`.
    cell_size : int
        Size of one cell in pixels.
    offset : tuple[int, int]
        Pan offset in pixels (offset_x, offset_y).
    """
    # ------------------------------------------------------------------
    # 1. Create a cached surface that contains the entire grid once
    #    – we only rebuild it if the grid changes.  For brevity we rebuild
    #    every call here; in a real app keep a reference and update only
    #    when `grid.cells` changes.
    # ------------------------------------------------------------------
    grid_surf = pygame.Surface((grid.width * cell_size, grid.height * cell_size))
    grid_surf.fill(CELL_DEAD_COLOR)

    # Draw every alive cell once on the grid surface
    alive = CELL_ALIVE_COLOR
    for y, row in enumerate(grid.cells):
        for x, flag in enumerate(row):
            if flag:
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                grid_surf.fill(alive, rect)

    # ------------------------------------------------------------------
    # 2. Create a wrapped surface (2× in each dimension) so that any
    #    offset can be satisfied with a single blit.
    # ------------------------------------------------------------------
    wrap_surf = pygame.Surface((grid_surf.get_width() * 2, grid_surf.get_height() * 2))
    wrap_surf.blit(grid_surf, (0, 0))
    wrap_surf.blit(grid_surf, (grid_surf.get_width(), 0))
    wrap_surf.blit(grid_surf, (0, grid_surf.get_height()))
    wrap_surf.blit(grid_surf, (grid_surf.get_width(), grid_surf.get_height()))

    # ------------------------------------------------------------------
    # 3. Compute the rectangle that the viewport wants to see.  Because
    #    we have a 2× tiled surface we can simply take a sub‑rect that
    #    starts at (offset_x % total_width, offset_y % total_height).
    # ------------------------------------------------------------------
    total_w = wrap_surf.get_width()
    total_h = wrap_surf.get_height()

    src_x = offset[0] % (grid.width * cell_size)
    src_y = offset[1] % (grid.height * cell_size)

    viewport_rect = pygame.Rect(src_x, src_y, surface.get_width(), surface.get_height())

    # ------------------------------------------------------------------
    # 4. Finally blit the required portion onto the screen.
    # ------------------------------------------------------------------
    surface.blit(wrap_surf, (0, 0), viewport_rect)

def draw(screen, ctx):
    """Wrapper that draws the entire frame and flips the display."""
    screen.fill(BG_COLOR)
    render_grid(screen, ctx.grid, ctx.viewport.cell_size, (ctx.viewport.offset_x, ctx.viewport.offset_y))
    pygame.display.flip()