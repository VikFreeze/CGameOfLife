python - <<'PY'
import time
from app.grid import Grid

g = Grid(1920, 1080)
g.randomize(0.3)

t0 = time.perf_counter()
for _ in range(10):
    g.tick()
t1 = time.perf_counter()
print(f"10 ticks in {t1-t0:.3f}s ({(t1-t0)/10:.3f}s per tick)")
PY