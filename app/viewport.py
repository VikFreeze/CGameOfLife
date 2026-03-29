# app/viewport.py
from dataclasses import dataclass
from config import MIN_CELL_SIZE, MAX_CELL_SIZE

@dataclass
class Viewport:
    """Represents the current view into the grid."""
    cell_size: int
    offset_x: int
    offset_y: int
    grid_width: int
    grid_height: int
    window_width: int
    window_height: int

    def clamp_offset(self):
        """Ensure the view never leaves the bounds of the grid."""
        max_x = 0
        min_x = self.window_width - self.grid_width * self.cell_size
        max_y = 0
        min_y = self.window_height - self.grid_height * self.cell_size

        if min_x > max_x:          # grid is smaller than the window
            min_x = max_x
        if min_y > max_y:
            min_y = max_y

        self.offset_x = max(min(self.offset_x, max_x), min_x)
        self.offset_y = max(min(self.offset_y, max_y), min_y)

    def apply_zoom(self, delta: int):
        """Zoom in/out centred on the screen centre (used by keys)."""
        new_size = self.cell_size + delta
        if new_size < MIN_CELL_SIZE or new_size > MAX_CELL_SIZE:
            return

        centre_grid_x = (self.window_width / 2 - self.offset_x) / self.cell_size
        centre_grid_y = (self.window_height / 2 - self.offset_y) / self.cell_size

        self.cell_size = new_size
        self.offset_x = int(self.window_width / 2 - centre_grid_x * self.cell_size)
        self.offset_y = int(self.window_height / 2 - centre_grid_y * self.cell_size)
        self.clamp_offset()

    def apply_zoom_at(self, delta: int, pos: tuple):
        """Zoom centred on the mouse position (used by wheel)."""
        mx, my = pos
        mouse_grid_x = (mx - self.offset_x) / self.cell_size
        mouse_grid_y = (my - self.offset_y) / self.cell_size
        new_size = self.cell_size + delta
        if new_size < MIN_CELL_SIZE or new_size > MAX_CELL_SIZE:
            return

        self.cell_size = new_size
        self.offset_x = int(mx - mouse_grid_x * self.cell_size)
        self.offset_y = int(my - mouse_grid_y * self.cell_size)
        self.clamp_offset()