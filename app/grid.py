# app/grid.py
from __future__ import annotations
import random
from dataclasses import dataclass, field
from typing import List

@dataclass
class Grid:
    width: int
    height: int
    cells: List[List[bool]] = field(init=False)

    def __post_init__(self):
        self.cells = [[False for _ in range(self.width)] for _ in range(self.height)]

    def reset(self, pattern: List[List[int]] | None = None):
        """Clear grid or apply a binary pattern (1 = alive)."""
        self.cells = [[False] * self.width for _ in range(self.height)]
        if pattern:
            for y, row in enumerate(pattern):
                for x, val in enumerate(row):
                    if 0 <= x < self.width and 0 <= y < self.height:
                        self.cells[y][x] = bool(val)

    def randomize(self, density: float = 0.3):
        for y in range(self.height):
            for x in range(self.width):
                self.cells[y][x] = random.random() < density

    def tick(self):
        """Compute the next generation."""
        new_cells = [[False for _ in range(self.width)] for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                alive_neighbors = self._alive_neighbors(x, y)
                alive = self.cells[y][x]
                # Conway rules
                if alive and alive_neighbors in (2, 3):
                    new_cells[y][x] = True
                elif not alive and alive_neighbors == 3:
                    new_cells[y][x] = True
                # else remains False
        self.cells = new_cells

    def _alive_neighbors(self, x: int, y: int) -> int:
        """Count alive cells in the 8 neighbouring positions (wrap‑around)."""
        total = 0
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx = (x + dx) % self.width
                ny = (y + dy) % self.height
                if self.cells[ny][nx]:
                    total += 1
        return total