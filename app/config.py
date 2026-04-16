# app/config.py

# Window
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
FPS = 60

# Accelerator CPU/GPU
RENDER_ON = "CPU"

# Grid zoom
DEFAULT_CELL_SIZE = 1            # 1 cell == 1 pixel
MIN_CELL_SIZE = 1
MAX_CELL_SIZE = 32

# Colours
CELL_DEAD_COLOR = (0, 0, 0)
CELL_ALIVE_COLOR = (255, 255, 255)

# Simulation speed in miliseconds, a lower value is faster
SIMULATION_INTERVAL = 0          # default value, 0 = unlimited
MAX_SIMULATION_INTERVAL = 1000   # Maximum value, slowest simulation speed
MIN_SIMULATION_INTERVAL = 0      # Minimum value, fastest simulation speed
STEP_PERCENTAGE = 0.10           # Step up/down in 10%(0.10) increments
