# app/patterns.py
# ─────────────────────────────────────────────────────────────────────────────
# 1.  Use a tiny Pattern data‑class that stores the cell‑matrix,
#     a short title and a human‑readable description.
# 2.  All patterns are defined as 2‑D ``numpy`` bool‑arrays.
# 3.  A convenience list ``ALL_PATTERNS`` is exported for the gallery.

from dataclasses import dataclass
import numpy as np

# --------------------------------------------------------------------------- #
@dataclass
class Pattern:
    """Single pattern definition used by the gallery."""
    name: str                      # internal id – useful for debugging
    cells: np.ndarray              # 2‑D bool array (True = alive)
    title: str                     # short name shown in the gallery
    description: str               # tooltip / longer explanation


# --------------------------------------------------------------------------- #
# Pattern definitions ---------------------------------------------------------
# Each cell‑matrix uses ``True`` for an alive cell and ``False`` for empty.

# --- GLIDER --------------------------------------------------------------- #
GLIDER = Pattern(
    name="glider",
    cells=np.array([[False, True,  False],
                    [False, False, True],
                    [True,  True,  True]], dtype=bool),
    title="Glider",
    description="A small spaceship that moves diagonally."
)

# --- BLINKER -------------------------------------------------------------- #
BLINKER = Pattern(
    name="blinker",
    cells=np.array([[True,  True,  True]], dtype=bool),
    title="Blinker",
    description="The simplest oscillator – it flips back and forth."
)

# --- PULSAR --------------------------------------------------------------- #
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

# --- Add more patterns here – they’ll appear automatically in the gallery. #
# --------------------------------------------------------------------------- #
ALL_PATTERNS = [GLIDER, BLINKER, PULSAR]