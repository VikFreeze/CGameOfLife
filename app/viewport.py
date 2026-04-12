# app/viewport.py
from dataclasses import dataclass
from config import MIN_CELL_SIZE, MAX_CELL_SIZE

@dataclass
class Viewport:
    cell_size: int
    offset_x: int
    offset_y: int
    grid_width: int
    grid_height: int
    window_width: int
    window_height: int

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