# app/grid.py
from __future__ import annotations
import random
import numpy as np
from dataclasses import dataclass, field
from typing import List

from numba import njit, prange

@dataclass
class Grid:
    width: int
    height: int
    cells: np.ndarray = field(init=False)

    def __post_init__(self):
        # 0 = dead, 1 = alive
        self.cells = np.zeros((self.height, self.width), dtype=np.uint8)

    def reset(self, pattern: List[List[int]] | None = None):
        """Clear grid or load a binary pattern (1 = alive)."""
        self.cells[:] = 0
        if pattern:
            for y, row in enumerate(pattern):
                for x, val in enumerate(row):
                    if 0 <= x < self.width and 0 <= y < self.height:
                        self.cells[y + 10, x + 10] = 1

    def randomize(self, density: float = 0.3):
        self.cells = (np.random.rand(self.height, self.width) < density).astype(np.uint8)

    def tick(self):
        """Compute the next generation – JIT‑accelerated."""
        self.cells = _tick_numba(self.cells)

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