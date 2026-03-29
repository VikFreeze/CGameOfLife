# app/input_handler.py
import pygame
from viewport import Viewport
from ui import Panel

def handle_events(events, state, panel):
    """
    Process all pending pygame events and update state accordingly.
    """
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Mouse editing
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            _handle_mouse_event(event, state)

        # Key handling – store pressed keys
        if event.type == pygame.KEYDOWN:
            state.pressed_keys.add(event.key)
            if event.key == pygame.K_SPACE:
                state.toggle_run()
        elif event.type == pygame.KEYUP:
            state.pressed_keys.discard(event.key)

        # Mouse wheel zoom
        if event.type == pygame.MOUSEWHEEL:
            mx, my = pygame.mouse.get_pos()
            state.viewport.apply_zoom_at(event.y, (mx, my))

        # Panel button events
        panel.handle_event(event)

def _handle_mouse_event(event, state):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button in (1, 3):
            state.dragging = True
            state.drag_button = event.button
            _set_cell_from_pos(event.pos, event.button, state)
    elif event.type == pygame.MOUSEMOTION and state.dragging:
        _set_cell_from_pos(event.pos, state.drag_button, state)
    elif event.type == pygame.MOUSEBUTTONUP:
        state.dragging = False

def _set_cell_from_pos(pos, button, state):
    """Translate a mouse position into a cell index and toggle it."""
    mx, my = pos
    if my < state.window_height - state.panel_height:   # inside grid area
        cx = (mx - state.viewport.offset_x) // state.viewport.cell_size
        cy = (my - state.viewport.offset_y) // state.viewport.cell_size
        if 0 <= cx < state.grid.width and 0 <= cy < state.grid.height:
            state.grid.cells[cy, cx] = 1 if button == 1 else 0