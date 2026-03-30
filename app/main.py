# app/main.py
import pygame
from config import *
from grid import Grid
from viewport import Viewport
from context import AppContext
from state_machine import StateMachine
from simulation_state import SimulationState
# no longer need to import draw

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Conway’s Game of Life")
    clock = pygame.time.Clock()

    # ------------------ grid & viewport ------------------
    grid = Grid(WINDOW_WIDTH, WINDOW_HEIGHT - PANEL_HEIGHT)
    viewport = Viewport(
        cell_size=DEFAULT_CELL_SIZE,
        offset_x=0,
        offset_y=0,
        grid_width=grid.width,
        grid_height=grid.height,
        window_width=WINDOW_WIDTH,
        window_height=WINDOW_HEIGHT
    )

    # ------------------ shared context ------------------
    ctx = AppContext(screen, grid, viewport)

    # ------------------ states & state machine ----------
    sim_state = SimulationState(ctx)
    ctx.simulation_state = sim_state          # give the gallery a back‑reference
    sm = StateMachine(sim_state)             # starts in simulation mode
    ctx.state_machine = sm

    # ------------------ main loop -----------------------
    while True:
        events = pygame.event.get()
        sm.handle_events(events)
        sm.update()
        sm.render()
        clock.tick(FPS)

if __name__ == "__main__":
    main()