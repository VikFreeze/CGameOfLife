# app/main.py
import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from grid import Grid, WarmUp
from viewport import Viewport
from context import AppContext, AppState
from events import InputHandler
from renderer import Draw

def main():
    # Kickstart jit on the tick function
    WarmUp(WINDOW_WIDTH, WINDOW_HEIGHT)

    # Initialize window
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Conway’s Game of Life")
    clock = pygame.time.Clock()

    # grid, viewport, context and inputs
    grid = Grid(WINDOW_WIDTH, WINDOW_HEIGHT)
    viewport = Viewport(WINDOW_WIDTH, WINDOW_HEIGHT)
    ctx = AppContext(screen, grid, viewport)
    inputs = InputHandler(ctx)

    while True:
        app_closeing = inputs.Handle(pygame.event.get())
        if app_closeing:
            break
        
        if ctx.state == AppState.RUNNING:
            ctx.grid.tick()
        Draw(ctx)
        clock.tick(FPS)

if __name__ == "__main__":
    main()