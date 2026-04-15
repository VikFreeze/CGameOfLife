# app/grid.py
import numpy as np
from numba import njit, prange

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = np.zeros((self.height, self.width), dtype=np.uint8)
    
    def reset(self):
        self.cells[:] = 0
    
    def randomize(self, temperature: float = 0.3):
        temp = max(0.0, min(1.0, temperature))
        self.cells[:] = np.random.binomial(1, temp, size=(self.height, self.width)).astype(np.uint8)

    def tick(self):
        # Compute the next generation – JIT‑accelerated.
        self.cells = _tick_numba(self.cells)

def WarmUp(width, height):
    # call the numba function to force it to compile, so the simulation runs immediately
    _tick_numba(np.zeros((height, width), dtype=np.uint8))

# Calculate next state using numba optimization
@njit(parallel=True)
def _tick_numba(cells: np.ndarray) -> np.ndarray:
    h, w = cells.shape
    new_cells = np.zeros_like(cells)
    for y in prange(h):                      # <- parallel loop
        for x in range(w):
            # wrap‑around neighbours (modulo arithmetic)
            neigh = (
                cells[(y-1)%h, (x-1)%w] + cells[(y-1)%h,  x] + cells[(y-1)%h, (x+1)%w] +
                cells[ y     , (x-1)%w]                      + cells[ y     , (x+1)%w] +
                cells[(y+1)%h, (x-1)%w] + cells[(y+1)%h,  x] + cells[(y+1)%h, (x+1)%w]
            )

            alive = cells[y, x]
            # Conway rules – booleans cast to uint8 (0/1)
            if alive:
                new_cells[y, x] = 1 if neigh in (2, 3) else 0
            else:
                new_cells[y, x] = 1 if neigh == 3 else 0
    return new_cells