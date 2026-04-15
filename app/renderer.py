# app/renderer.py
import pygame
import numpy as np
from context import AppState
from config import CELL_ALIVE_COLOR, CELL_DEAD_COLOR, WINDOW_WIDTH, WINDOW_HEIGHT

def render_grid(surface: pygame.Surface, grid, cell_size: int, offset: tuple):
    # Grid cells to surface
    alive_color = np.array([CELL_ALIVE_COLOR], dtype=np.uint8)
    dead_color = np.array([CELL_DEAD_COLOR], dtype=np.uint8)
    rgb_grid = np.where(grid.cells[:, :, None] == 1, alive_color, dead_color)
    grid_surface = pygame.surfarray.make_surface(rgb_grid.swapaxes(0, 1))

    # 2 x 2 tile to enable toroidal viewport behaviour
    gw, gh = grid_surface.get_size()
    wrap_surf = pygame.Surface((gw * 2, gh * 2))
    wrap_surf.blit(grid_surface, (0, 0))
    wrap_surf.blit(grid_surface, (gw, 0))
    wrap_surf.blit(grid_surface, (0, gh))
    wrap_surf.blit(grid_surface, (gw, gh))

    # Scale offset down to native resolution
    ox, oy = offset[0] // cell_size, offset[1] // cell_size

    # The viewport in native pixels
    view_w_native = surface.get_width() // cell_size
    view_h_native = surface.get_height() // cell_size

    # Clamp coordinates to native resolution
    ox %= gw
    oy %= gh

    # Calculate the area to be shown in the viewport and copy it to the screen
    src_rect = pygame.Rect(ox, oy, min(view_w_native, WINDOW_WIDTH), min(view_h_native, WINDOW_HEIGHT))
    surface.blit(pygame.transform.scale(wrap_surf.subsurface(src_rect), surface.get_size()), (0, 0))

def draw_state_indicator(ctx):
    font = pygame.font.SysFont(None, 36)
    text = f'State: {"RUNNING" if ctx.state == AppState.RUNNING else "PAUSED"}  Speed: {ctx.ticks_per_second()}'
    color = (255, 255, 255)   # white
    surface = font.render(text, True, color)

    # Center at top of viewport
    x = ctx.viewport.window_width // 2 - surface.get_width() // 2
    y = 10   # 10 pixels from the top
    text_rect = surface.get_rect(topleft=(x, y))

    padding_w, padding_h = 20, 10
    poly = [
        (text_rect.left - padding_w, text_rect.top - padding_h),
        (text_rect.right + padding_w, text_rect.top - padding_h),
        (text_rect.right + padding_w - 15, text_rect.bottom + padding_h),
        (text_rect.left - padding_w + 15, text_rect.bottom + padding_h)
    ]

    pygame.draw.polygon(ctx.screen, (0, 120, 255), poly)
    ctx.screen.blit(surface, text_rect.topleft)

def Draw(ctx):
    # Wrapper that draws the entire frame and flips the display
    ctx.screen.fill(CELL_DEAD_COLOR)
    render_grid(ctx.screen, ctx.grid, ctx.viewport.cell_size, (ctx.viewport.offset_x, ctx.viewport.offset_y))
    draw_state_indicator(ctx)
    pygame.display.flip()