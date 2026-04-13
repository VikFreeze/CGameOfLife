# app/patterns.py
import numpy as np

class Pattern:
    def __init__(self, name, cells, title, description):
        self.name: str         = name                 # internal id – useful for debugging
        self.cells: np.ndarray = cells                # 2‑D bool array (True = alive)
        self.title: str        = title                # short name shown in the gallery
        self.description: str  = description          # longer explanation

# Pattern definitions, each cell‑matrix uses ``True`` for an alive cell and ``False`` for dead.
# GLIDER
GLIDER = Pattern(
    name="glider",
    cells=np.array([[False, True,  False],
                    [False, False, True],
                    [True,  True,  True]], dtype=bool),
    title="Glider",
    description="A small spaceship that moves diagonally."
)

# BLINKER
BLINKER = Pattern(
    name="blinker",
    cells=np.array([[True,  True,  True]], dtype=bool),
    title="Blinker",
    description="The simplest oscillator – it flips back and forth."
)

# PULSAR
PULSAR = Pattern(
    name="pulsar",
    cells=np.array([
        [True,  False, True,  False, True],
        [False, False, False, False, False],
        [True,  False, True,  False, True],
        [False, False, False, False, False],
        [True,  False, True,  False, True]
    ], dtype=bool),
    title="Pulsar",
    description="A large oscillator that cycles every 3 generations."
)

# Add more patterns here – they’ll appear automatically in the gallery. #
ALL_PATTERNS = [GLIDER, BLINKER, PULSAR]