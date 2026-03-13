# app/main.py
import sys
import pygame
from config import *
from grid import Grid
from renderer import render_grid
from ui import Button, Panel
from patterns import GLIDER, BLINKER, PULSAR

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Conway’s Game of Life")
    clock = pygame.time.Clock()

    # Grid occupies the whole window except the panel at the bottom
    grid_width = WINDOW_WIDTH
    grid_height = WINDOW_HEIGHT - PANEL_HEIGHT
    grid = Grid(grid_width, grid_height)

    # State machine
    running = False
    cell_size = DEFAULT_CELL_SIZE

    # Font
    font = pygame.font.SysFont(FONT_NAME, 18)

    # UI callbacks
    def start():
        nonlocal running
        running = True

    def pause():
        nonlocal running
        running = False

    def reset():
        nonlocal running
        running = False
        grid.reset()

    def set_glider():
        grid.reset(GLIDER)

    def set_blinker():
        grid.reset(BLINKER)

    def set_pulsar():
        grid.reset(PULSAR)

    def zoom_in():
        nonlocal cell_size
        if cell_size < MAX_CELL_SIZE:
            cell_size += 1

    def zoom_out():
        nonlocal cell_size
        if cell_size > MIN_CELL_SIZE:
            cell_size -= 1

    # Build buttons
    buttons = [
        Button(pygame.Rect(10, WINDOW_HEIGHT - PANEL_HEIGHT + 10, 80, BUTTON_HEIGHT), "Start", start),
        Button(pygame.Rect(100, WINDOW_HEIGHT - PANEL_HEIGHT + 10, 80, BUTTON_HEIGHT), "Pause", pause),
        Button(pygame.Rect(190, WINDOW_HEIGHT - PANEL_HEIGHT + 10, 80, BUTTON_HEIGHT), "Reset", reset),
        Button(pygame.Rect(280, WINDOW_HEIGHT - PANEL_HEIGHT + 10, 80, BUTTON_HEIGHT), "Glider", set_glider),
        Button(pygame.Rect(370, WINDOW_HEIGHT - PANEL_HEIGHT + 10, 80, BUTTON_HEIGHT), "Blinker", set_blinker),
        Button(pygame.Rect(460, WINDOW_HEIGHT - PANEL_HEIGHT + 10, 80, BUTTON_HEIGHT), "Pulsar", set_pulsar),
        Button(pygame.Rect(550, WINDOW_HEIGHT - PANEL_HEIGHT + 10, 80, BUTTON_HEIGHT), "Zoom+", zoom_in),
        Button(pygame.Rect(640, WINDOW_HEIGHT - PANEL_HEIGHT + 10, 80, BUTTON_HEIGHT), "Zoom-", zoom_out),
    ]

    panel = Panel(screen, buttons)

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            panel.handle_event(event)

        if running:
            grid.tick()

        screen.fill(BG_COLOR)
        render_grid(screen, grid, cell_size)
        panel.draw(font)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()