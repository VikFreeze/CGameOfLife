
# Conway’s Game of Life – Python / Pygame Implementation

**Author:** _VikFreeze_  
**Repository:** https://github.com/VikFreeze/CGameOfLife

> Conway’s Game of Life - zero players, one grid, four rules, infinite possibilities.  
> This is a lightweight, fast, and fully-interactive simulation of Conway’s Game of Life written in Python, built on **Pygame** and **uv**, with **Numba**-accelerated cell updates and a toroidal viewport.

---

## 📋 Table of Contents

| Section | Description |
|---------|-------------|
| [Introduction](#introduction) | What this project is and why it matters |
| [Technology Stack](#technology-stack) | Pygame, uv, Numba – why we chose them |
| [Technical Challenges & Optimisations](#technical-challenges--optimisations) | Parallelisation, Numba, blitting & toroidal logic |
| [Getting Started – Run the App](#getting-started--run-the-app) | OS‑agnostic instructions for end users |
| [Getting Started – Development](#getting-started--development) | How to clone, build, and extend the code |
| [Controls](#controls) | Keyboard & mouse shortcuts |
| [About Conway’s Game of Life](#about-conways-game-of-life) | History, patterns, and biological parallels |
| [Personal Motivation](#personal-motivation) | From Turbo Pascal to modern Python |
| [Future Work](#future-work) | Planned gallery UI & other enhancements |
| [Patterns & Experiments](#patterns--experiments) | Fun patterns you can try immediately |

---

## 🎯 Introduction

Conway’s Game of Life is one of the most celebrated cellular automata.  With just four simple rules, an initially static grid can evolve into complex, often self-replicating, structures that mimic biological growth.  
This repository contains a fast, fully-interactive Python implementation with these features:

| Feature | Description |
|---------|-------------|
| **Adjust values in config.py** | Adjust the values in `config.py`, mainly the window size. Ideally, set it to your monitor’s resolution for fullscreen mode. However, larger window sizes will also lead to slower performance |
| **Fullscreen window** | Drag the window to the desired monitor and toggle fullscreen with **F11**. |
| **Decide who lives** | `Left‑click` individual cells (while paused or running) to set them to an alive state, or `left-click and drag` to leave flurishing life in your wake. |
| **And who does not** | `Right-click` individual cells (while paused or running) to set them to a dead state, or `right-click and drag` to leave a baren wasteland in your wake. |
| **Play God** | Stop the simulation and clear the grid with **R** |
| **Run simulation** | Toggle the simulation on and off with `Space bar` |
| **Speed control** | The simulation starts at unlimited speed; adjust it with **Page Up** / **Page Down**. |
| **Zoom & Pan** | See something interesting? Hover over it and zoom in with the **scroll wheel**. You can also pan with the `arrow keys` or by holding the `middle mouse button` |
| **Step thru generations** | When the simulation is paused you can step thru one tick at a time with `N` |
| **Anarchy** | No inspiration? Randomize the grid with `K` and let the chips fall where they may |
| **Toroidal grid** | The grid is infinite, we ~~faked~~ achieved this with a bit of modulo arithmetic |
| **Optimized rendering** | The rendering code uses `pygame.Surface.blit` and modulo arithmetic to keep overhead low while delivering the intended toroidal viewport behavior - see `renderer.py`. |
| **Optimized computations with Numba and Numpy** | Calculating the next tick can be done in parallel for each cell, so the `tick_gpu` function is implemented with CUDA support to run on the GPU. However this might not work for everyone so we also included the function `_tick_numba`, that runs on the CPU. To set the accelerator, just edit `config.py` accordingly. The grid is defined as a Numpy array for C-like calculation performance |

The goal is to provide an educational sandbox for both beginners and researchers to experiment with patterns, while keeping the code base clean and extensible.

---

## 🛠️ Technology Stack

| Technology | Purpose | Why it was chosen |
|------------|---------|--------------------|
| **Python 3.13** | Core language | Rapid prototyping, large ecosystem |
| **Pygame** | 2-D graphics & event handling | Mature, cross-platform, simple to use |
| **uv** | Dependency manager & packaging | Small, zero-config, works on all major OSes |
| **Numba** | Just-in-time compilation of the tick loop, for both GPU and CPU | Turns Python loops into highly-optimised CUDA/C-like code |
| **NumPy** | Efficient array operations | Core data structure for the grid |

---

## Technical Challenges & Optimisations

1. **Parallelisable Next-Generation Calculation**  
   Each cell’s next state depends only on its eight neighbours, so the calculation can be fully parallelised.  Python’s GIL, however, prevents true multi-threading in pure Python.  To avoid the usual performance bottleneck, we use **Numba** to JIT-compile the respective methods for GPU/CPU, giving us near-native performance.

2. **Blitting vs. Per-Pixel Drawing**  
   Drawing each cell individually is extremely slow, instead, the `render_grid` function builds a pre-generated surface containing the whole grid then uses that to builds a 2 x 2 tile and then copies and scales the relevant section to the screen. This, along with some modulo arithmetic, handles toroidal (wrap‑around) coordinates, ensuring seamless panning and zooming.  

   > *Source:* Rendering logic and toroidal handling are in `renderer.py` [1].

3. **Wrap-Around (Toroidal) Grid**  
   The simulation treats the grid as a torus: cells on the edge see neighbours on the opposite edge.  All neighbour calculations use `% WIDTH` / `% HEIGHT`.

4. **UI-less Design**  
   An earlier iteration included a bottom-bar control UI.  It was removed to streamline the experience and because the project’s focus shifted toward a future gallery UI.  All interactions are now handled via keyboard shortcuts and mouse events.

---

## ⚙️ Getting Started – Run the App

1. **Clone the repo**

   ```bash
   git clone https://github.com/VikFreeze/CGameOfLife
   cd CGameOfLife
   ```

2. **Install dependencies**

   ```bash
   uv sync
   ```

3. **Run the application**

   ```bash
   uv run app/main.py
   ```

Drag the window to the desired monitor and hit `F11` for full screen.  Press `Space` to start/stop the simulation, `N` to step one tick, and use the mouse to paint cells.
See [Controls](#controls) section for more information

---

## Getting Started – Development

1. **Set up a development environment**

   ```bash
   git clone https://github.com/VikFreeze/CGameOfLife
   cd CGameOfLife
   ```

2. **Install dependencies**

   ```bash
   uv sync --dev
   ```

3. **Edit the source**

   * `app/main.py` – entry point  
   * `app/renderer.py` – rendering logic  
   * `grid.py`, `viewport.py`, `events.py` – core game mechanics  

4. **Build a distributable**

   ```bash
   uv pack
   ```

   This creates a wheel you can install with `pip install dist/*.whl`.

---

## 🎮 Controls

| Button | Action |
|--------|--------|
| **F11** | Toggle fullscreen |
| **Mouse Left Click / Drag** | Revive cells |
| **Mouse Right Click / Drag** | Euthanize cells |
| **R** | Reset |
| **Space** | Run / pause simulation |
| **N** | Step one tick (when paused) |
| **Page up/down** | Simulation speed control |
| **Mouse Wheel** | Zoom in / out |
| **Middle Mouse/Arrow Keys** | Pan |
| **K** | Set grid randomly |
| **G** | Toggle gallery (future feature) |
| **Q** | Quit |

---

## About Conway’s Game of Life

Conway’s Game of Life is a **zero-player game** where the only input is the initial configuration.  Its four rules:

1. Any live cell with fewer than two live neighbours dies (under-population).  
2. Any live cell with two or three live neighbours lives on.  
3. Any live cell with more than three live neighbours dies (over-population).  
4. Any dead cell with exactly three live neighbours becomes a live cell (reproduction).

Despite its simplicity, the system exhibits:

* **Self-organising patterns** (e.g., gliders, pulsars).  
* **Computational universality** – it can emulate a universal Turing machine.  
* **Biologically analogous behaviour** – some patterns mimic cellular growth, bacterial colonies, or even social dynamics.  
* **Infinite possibilities** – new patterns can be discovered endlessly, its even possible to create the Game of Life inside the Game of Life

---

For the project’s history and the author’s original motivation, see [History.md](/History.md).

---

## Future Work

* **Gallery UI** – triggered by `G`, showing all patterns from `patterns.py` with preview, title, description, a search bar and the ability to select and place a pattern on the grid.  
* **Pattern persistence** – ability to save and load custom patterns.  

> *If you’re interested, feel free to fork, extend, submit PRs as well as use the app to experiment with patterns!*

---

## Patterns & Experiments

Here are a few patterns that i came across during development:

1. **Straight Line** – a single-cell-wide line(run the mouse along the monitor edge), try different lenghts.  
2. **Edge-to-Edge Line** – same as before, a single-cell-wide line but this time run it from edge to edge. Due to the toroidal nature of the grid this line will have no ends, observer how this behaves compared to the first example that does have ends.
3. **Goku going super-saiyan** – I found Goku going super‑saiyan, complete with waving hair and particle effects. Don’t believe me? Give this a try and tell me if you see it.

**Try it yourself**:
1. In a empty grid, zoom in and make a plus sign with 5 cells but leave the middle dead, so 4 live cells and the one in the middle dead then hit space to run the simulation. And as you can see, you see nothing, this pattern is stable and does not change.
2. To get to the next step, place a live cell right under the lowest live cell on the grid, making a cross shape, you can pause to do this and step thru with N or do it while the simulation is running. Either way if you did it right, in 2 ticks you should get a oval shape, another stable pattern.
3. Again, as before, place one live cell right under the lowest live cell on the grid. If you did it right, in 16 ticks, you will be presented with four ovals in a radial pattern, this is the final stable pattern.
4. Third times the charm, one last time, place one live cell right below the lowest live cell on the grid, then watch the resulting reaction.
![SSJ Goku](https://github.com/VikFreeze/CGameOfLife/blob/main/images/readme/ssj_goku.gif?raw=true)
