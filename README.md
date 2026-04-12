
# CGameOfLife

Conway’s Game of Life - zero players, one grid, four rules, infinit possibilities.  
This is a full‑screen, zoomable, wrap‑around, interactable simulation written in Python for experimentation with patterns.
It uses **Pygame** for graphics and **uv** for packaging and dependency management.

---

## 📋 Table of Contents

- [Features](#features)
- [Why Pygame?](#why-pygame)
- [Installation](#installation)
- [Running the App](#running-the-app)
- [Controls](#controls)
- [Zoom & Wrap‑around](#zoom--wrap-around)

---

## 🎯 Features

| Feature | Description |
|---------|-------------|
| **Adjust values in config.py** | Adjust the values in config.py, mainly the window size.<br />Idealy you should set it to the same as your monitors resolution for<br />fullscreen mode but, larger window sizes will also lead to slower performance |
| **Fullscreen window** | Drag the window to the desired monitor and toggle fullscreen with F11 |
| **Decide who lives** | Click individual cells to set them to alive state, or click and drag to leave flurishing life in your wake. |
| **And who does not** | Right-click individual cells to set them to dead state, or right-click and drag to leave a baren wasteland in your wake. |
| **Play God** | Stop the simulation and clear the grid with R |
| **Run simulation** | Toggle the simulation on and off with space bar |
| **Zoom & Pan** | See something interesting? Place the mouse over it and zoom in with the scroll wheel. You can also pan with the arrow keys or by holding the middle mouse button |
| **Toroidal grid** | The grid is infinit so we ~~faked~~ acchieved this with a bit of modulo arithemetic |

---

## 🛠️ Why Pygame?

| Aspect | Reason |
|--------|--------|
| **Event loop** | `pygame.event` handles keyboard, mouse, timers out of the box. |
| **Cross‑platform** | Runs on Windows, macOS, and Linux with the same code. |
| **Low overhead** | No heavyweight UI framework – just pure Python. |

---

## ⚙️ Installation

The project uses **uv** – a fast, modern Python package manager.

```bash
# 1. Clone the repo
git clone https://github.com/VikFreeze/CGameOfLife
cd CGameOfLife

# 2. Create/activate the virtual environment and install deps
uv sync  # or `uv install` if you already have a venv
```

> **Tip:**  
> `uv sync` automatically reads `pyproject.toml`. No need for a separate `requirements.txt`.

---

## ▶️ Running the App

```bash
uv run app.main
```

You’ll see a black window with the grid and a bottom control panel.

---

## 🎮 Controls

| Button | Action |
|--------|--------|
| **F11** | Toggle fullscreen |
| **Click/drag** | Revive cells |
| **Right-click/drag** | Euthanise cells |
| **R** | Reset |
| **Space** | Toggle simulation |
| **Mouse Wheel** | Zoom |
| **Middle Mouse/Arrow Keys** | Pan |
| **Q** | Quit |

---



