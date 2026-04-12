# app/main.py
import pygame
from config import *
from grid import Grid
from viewport import Viewport
from context import AppContext
from state_machine import StateMachine
from simulation_state import SimulationState

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Conway’s Game of Life")
    clock = pygame.time.Clock()

    # grid & viewport
    grid = Grid(WINDOW_WIDTH, WINDOW_HEIGHT)
    viewport = Viewport(
        cell_size=DEFAULT_CELL_SIZE,
        offset_x=0,
        offset_y=0,
        grid_width=grid.width,
        grid_height=grid.height,
        window_width=WINDOW_WIDTH,
        window_height=WINDOW_HEIGHT,
    )

    ctx = AppContext(screen, grid, viewport)
    sim_state = SimulationState(ctx)
    ctx.simulation_state = sim_state            # back‑reference for gallery
    sm = StateMachine(sim_state)                # starts in simulation mode
    ctx.state_machine = sm

    fullscreen = False

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # F11 → toggle fullscreen / windowed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                    # update viewport window size
                    viewport.window_width = screen.get_width()
                    viewport.window_height = screen.get_height()
                if event.key == pygame.K_r:
                    ctx.simulation_state.reset()
                # Q → quit the program
                if event.key == pygame.K_q:
                    pygame.quit()
                    return
        sm.handle_events(events)
        sm.update()
        sm.render()
        clock.tick(FPS)

if __name__ == "__main__":
    main()