# app/grid.py
import numpy as np
from numba import njit, cuda, prange
from config import RENDER_ON

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
        match RENDER_ON:
            case "CPU":
                # Compute the next generation – JIT‑accelerated on CPU.
                self.cells = _tick_numba(self.cells)
            case "GPU":
                # Compute the next generation – JIT‑accelerated on GPU.
                self.cells = tick_gpu_wrapper(self.cells)

def WarmUp(width, height):
    # call the relevant function to force it to compile, so the simulation runs immediately
    match RENDER_ON:
        case "CPU":
            _ = _tick_numba(np.zeros((height, width), dtype=np.uint8))
        case "GPU":
            _ = tick_gpu_wrapper(np.zeros((height, width), dtype=np.uint8))

# CPU implementation
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

# GPU implementation
@cuda.jit
def tick_gpu(cells, new_cells, h, w):
    y, x = cuda.grid(2)
    if y >= h or x >= w:
        return

    # wrap‑around neighbours (modulo arithmetic)
    neigh = (
        cells[(y-1) % h, (x-1) % w] + cells[(y-1) % h, x] + cells[(y-1) % h, (x+1) % w] +
        cells[y, (x-1) % w]                          + cells[y, (x+1) % w] +
        cells[(y+1) % h, (x-1) % w] + cells[(y+1) % h, x] + cells[(y+1) % h, (x+1) % w]
    )

    alive = cells[y, x]
    if alive:
        new_cells[y, x] = 1 if neigh in (2, 3) else 0
    else:
        new_cells[y, x] = 1 if neigh == 3 else 0


# Helper to launch the GPU kernel
def tick_gpu_wrapper(cells: np.ndarray) -> np.ndarray:
    h, w = cells.shape

    # Allocate device memory
    d_cells = cuda.to_device(cells.astype(np.uint8))
    d_new_cells = cuda.device_array_like(d_cells)

    # Define thread block and grid dimensions
    threads_per_block = (32, 32)          # tweak for performance
    blocks_per_grid_x = (w + threads_per_block[0] - 1) // threads_per_block[0]
    blocks_per_grid_y = (h + threads_per_block[1] - 1) // threads_per_block[1]
    blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)

    # Launch kernel
    tick_gpu[blocks_per_grid, threads_per_block](d_cells, d_new_cells, h, w)

    # Copy result back to host
    return d_new_cells.copy_to_host()