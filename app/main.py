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

    # ---------- grid + view state ----------
    grid = Grid(WINDOW_WIDTH, WINDOW_HEIGHT - PANEL_HEIGHT)

    running     = False
    cell_size   = DEFAULT_CELL_SIZE
    offset_x    = 0
    offset_y    = 0

    # ---------- helper: keep view inside grid ----------
    def clamp_offset():
        nonlocal offset_x, offset_y
        max_x = 0
        min_x = WINDOW_WIDTH - grid.width * cell_size
        max_y = 0
        min_y = WINDOW_HEIGHT - grid.height * cell_size

        if min_x > max_x:  # grid smaller than the window
            min_x = max_x
        if min_y > max_y:
            min_y = max_y

        offset_x = max(min(offset_x, max_x), min_x)
        offset_y = max(min(offset_y, max_y), min_y)

    # ---------- helper: zoom ----------
    def apply_zoom(delta: int):
        """Zoom in/out centred on the screen centre (used by keys)."""
        nonlocal cell_size, offset_x, offset_y
        new_size = cell_size + delta
        if new_size < MIN_CELL_SIZE or new_size > MAX_CELL_SIZE:
            return

        # centre *in grid coordinates* before the zoom
        centre_grid_x = (WINDOW_WIDTH / 2 - offset_x) / cell_size
        centre_grid_y = (WINDOW_HEIGHT / 2 - offset_y) / cell_size

        cell_size = new_size

        # reposition offset so that the same grid point stays in the centre
        offset_x = int(WINDOW_WIDTH / 2 - centre_grid_x * cell_size)
        offset_y = int(WINDOW_HEIGHT / 2 - centre_grid_y * cell_size)

        clamp_offset()

    def apply_zoom_at(delta: int, pos: tuple):
        """Zoom centred on *mouse* position (used by wheel)."""
        nonlocal cell_size, offset_x, offset_y

        # grid coordinate of the mouse before the zoom
        mx, my = pos
        mouse_grid_x = (mx - offset_x) / cell_size
        mouse_grid_y = (my - offset_y) / cell_size

        new_size = cell_size + delta
        if new_size < MIN_CELL_SIZE or new_size > MAX_CELL_SIZE:
            return

        cell_size = new_size

        # new offset so the same grid point stays under the cursor
        offset_x = int(mx - mouse_grid_x * cell_size)
        offset_y = int(my - mouse_grid_y * cell_size)

        clamp_offset()

    # ---------- UI ----------
    font = pygame.font.SysFont(FONT_NAME, 18)

    def toggle_run():
        nonlocal running
        running = not running
        toggle_btn.text = "Pause" if running else "Start"

    def reset():
        nonlocal running, offset_x, offset_y
        running = False
        toggle_btn.text = "Start"
        grid.reset()
        offset_x = offset_y = 0      # reset view

    def set_glider():   grid.reset(GLIDER)
    def set_blinker():  grid.reset(BLINKER)
    def set_pulsar():   grid.reset(PULSAR)
    def zoom_in():      apply_zoom(+1)
    def zoom_out():     apply_zoom(-1)

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

    # ---------- mouse editing helper ----------
    dragging = False
    drag_button = 0

    def _set_cell_from_pos(pos, button):
        mx, my = pos
        if my < WINDOW_HEIGHT - PANEL_HEIGHT:   # inside grid area
            cx, cy = (mx - offset_x) // cell_size, (my - offset_y) // cell_size
            if 0 <= cx < grid.width and 0 <= cy < grid.height:
                grid.cells[cy, cx] = 1 if button == 1 else 0

    # ---------- continuous arrow‑key panning ----------
    pressed_keys = set()          # holds pygame key constants while held

    # ---------- main loop ----------
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # 1️⃣  mouse editing
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button in (1, 3):
                        dragging = True
                        drag_button = event.button
                        _set_cell_from_pos(event.pos, event.button)
                elif event.type == pygame.MOUSEMOTION and dragging:
                    _set_cell_from_pos(event.pos, drag_button)
                elif event.type == pygame.MOUSEBUTTONUP:
                    dragging = False

            # 2️⃣  key handling – store pressed keys
            if event.type == pygame.KEYDOWN:
                pressed_keys.add(event.key)
                # space toggles simulation
                if event.key == pygame.K_SPACE:
                    toggle_run()
            elif event.type == pygame.KEYUP:
                pressed_keys.discard(event.key)

            # 3️⃣  mouse wheel zoom – focus on cursor
            if event.type == pygame.MOUSEWHEEL:
                mx, my = pygame.mouse.get_pos()
                apply_zoom_at(event.y, (mx, my))

            # 4️⃣  panel (buttons)
            panel.handle_event(event)

        # ---------- continuous arrow‑key panning ----------
        pan_step = cell_size * 5          # tweak for speed
        if pygame.K_LEFT  in pressed_keys:
            offset_x += pan_step
            clamp_offset()
        if pygame.K_RIGHT in pressed_keys:
            offset_x -= pan_step
            clamp_offset()
        if pygame.K_UP    in pressed_keys:
            offset_y += pan_step
            clamp_offset()
        if pygame.K_DOWN  in pressed_keys:
            offset_y -= pan_step
            clamp_offset()

        # ---------- simulation step ----------
        if running:
            grid.tick()

        # ---------- draw ----------
        screen.fill(BG_COLOR)
        render_grid(screen, grid, cell_size, (offset_x, offset_y))
        panel.draw(font)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()