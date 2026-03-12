# app/patterns.py
# 2D list of 0/1, 1 = alive, 0 = dead
# These are *small* patterns; feel free to add more!
GLIDER = [
    [0, 0, 1],
    [1, 0, 1],
    [0, 1, 1],
]

BLINKER = [
    [1, 1, 1],
]

PULSAR = [
    [0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0],
]