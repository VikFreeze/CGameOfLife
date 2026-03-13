
# CGameOfLife

Conway’s Game of Life – a full‑screen, zoomable, wrap‑around simulation written in Python.  
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
| **Fullscreen window** | Occupies the entire screen with the same resolution as the display. |
| **Wrap‑around grid** | Off‑screen neighbors wrap to the opposite edge (toroidal topology). |
| **Zoom** | 1 cell can be 1×1, 2×2, 3×3 … pixels. Press *Zoom+* / *Zoom‑* to adjust. |
| **Control panel** | Bottom panel with Start, Pause, Reset, preset patterns (Glider, Blinker, Pulsar), Zoom controls. |

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
| **Start** | Run the simulation. |
| **Pause** | Pause the simulation. |
| **Reset** | Stop and clear the grid. |
| **Glider / Blinker / Pulsar** | Load a predefined pattern. |
| **Zoom+ / Zoom‑** | Increase / decrease the pixel size of a cell. |

*Keyboard shortcuts* can be added later – currently only mouse interaction is supported.

---

## 🔍 Zoom & Wrap‑around

*Wrap‑around* is handled entirely in the `Grid` logic using modulo arithmetic (`%`).  
*Zoom* only changes the `cell_size` used when drawing; the logical grid size stays constant.  

---


