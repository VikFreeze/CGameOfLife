# app/viewport.py
from config import DEFAULT_CELL_SIZE, MIN_CELL_SIZE, MAX_CELL_SIZE

class Viewport:
    def __init__(self, window_width, window_height):
        self.cell_size = DEFAULT_CELL_SIZE
        self.offset_x = 0
        self.offset_y = 0
        self.grid_width = window_width
        self.grid_height = window_height
        self.window_width = window_width
        self.window_height = window_height

    def apply_zoom_at(self, ctx, delta: int, mouse_position: tuple):
        # Check if new zoom level is valid
        new_cell_size = self.cell_size + delta
        if new_cell_size < MIN_CELL_SIZE or new_cell_size > MAX_CELL_SIZE:
            return
        
        # Viewport mouse x,y to grid cell coordinates that the mouse is hovering over
        cx = ((mouse_position[0] + self.offset_x) // self.cell_size) % ctx.grid.width
        cy = ((mouse_position[1] + self.offset_y) // self.cell_size) % ctx.grid.height

        # Set new viewport offset so that the grid cell cx, cy is centered in the viewport
        self.offset_x = cx * new_cell_size - ctx.viewport.window_width // 2
        self.offset_y = cy * new_cell_size - ctx.viewport.window_height // 2
        self.cell_size = new_cell_size