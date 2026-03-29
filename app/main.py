# app/main.py
import sys
import pygame
from config import *
from grid import Grid
from viewport import Viewport
from state import AppState
from input_handler import handle_events
from renderer import draw          # ← updated import
from ui import Button, Panel
from patterns import GLIDER, BLINKER, PULSAR

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Conway’s Game of Life")
    clock = pygame.time.Clock()

    # ---------- grid + view state ----------
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
    state = AppState(grid=grid, viewport=viewport,
                     window_height=WINDOW_HEIGHT, panel_height=PANEL_HEIGHT)

    # ---------- UI ----------
    font = pygame.font.SysFont(FONT_NAME, 18)

    def toggle_run():
        state.toggle_run()
        toggle_btn.text = "Pause" if state.running else "Start"

    def reset():
        state.reset()
        toggle_btn.text = "Start"

    def set_glider():
        state.grid.reset(GLIDER.cells.astype(int).tolist())
        state.viewport.offset_x = state.viewport.offset_y = 0

    def set_blinker():
        state.grid.reset(BLINKER.cells.astype(int).tolist())
        state.viewport.offset_x = state.viewport.offset_y = 0

    def set_pulsar():
        state.grid.reset(PULSAR.cells.astype(int).tolist())
        state.viewport.offset_x = state.viewport.offset_y = 0

    def zoom_in():
        viewport.apply_zoom(+1)

    def zoom_out():
        viewport.apply_zoom(-1)

    toggle_btn = Button(pygame.Rect(10, 10, 80, BUTTON_HEIGHT), "Start", toggle_run)
    buttons = [
        toggle_btn,
        Button(pygame.Rect(100, 10, 80, BUTTON_HEIGHT), "Reset", reset),
        Button(pygame.Rect(190, 10, 80, BUTTON_HEIGHT), "Glider", set_glider),
        Button(pygame.Rect(280, 10, 80, BUTTON_HEIGHT), "Blinker", set_blinker),
        Button(pygame.Rect(370, 10, 80, BUTTON_HEIGHT), "Pulsar", set_pulsar),
        Button(pygame.Rect(460, 10, 80, BUTTON_HEIGHT), "Zoom+", zoom_in),
        Button(pygame.Rect(550, 10, 80, BUTTON_HEIGHT), "Zoom-", zoom_out),
    ]
    panel = Panel(screen, buttons, panel_height=PANEL_HEIGHT)

    # ---------- main loop ----------
    while True:
        events = pygame.event.get()
        handle_events(events, state, panel)

        pan_step = viewport.cell_size * 5
        state.update_pan(pan_step)

        if state.running:
            state.grid.tick()

        draw(screen, state, panel, font)
        clock.tick(FPS)

if __name__ == "__main__":
    main()