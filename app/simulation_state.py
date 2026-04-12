# app/simulation_state.py
import pygame
from renderer import draw
from gallery_state import GalleryState

class SimulationState:
    """Runs the cellular automaton and handles user input."""
    def __init__(self, ctx):
        self.ctx = ctx
        self.running = False
        self.pressed_keys = set()
        self.dragging = False
        self.drag_button = 0

    # ---------- UI callbacks ----------
    def toggle_run(self):
        self.running = not self.running
        self._update_caption()

    def reset(self):
        self.ctx.grid.reset()
        self.ctx.viewport.offset_x = self.ctx.viewport.offset_y = 0
        self.ctx.viewport.clamp_offset()
        self.running = False
        self._update_caption()

    def zoom_in(self):
        self.ctx.viewport.apply_zoom(+1)

    def zoom_out(self):
        self.ctx.viewport.apply_zoom(-1)

    def open_gallery(self):
        self.dragging = False
        self.drag_button = 0
        self.ctx.state_machine.switch(GalleryState(self.ctx))

    # ---------- Helper ----------
    def _update_caption(self):
        state = "Running" if self.running else "Paused"

    # ---------- Event handling ----------
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Mouse editing
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                self._handle_mouse(event)

            # Key handling
            elif event.type == pygame.KEYDOWN:
                self.pressed_keys.add(event.key)
                if event.key == pygame.K_SPACE:
                    self.toggle_run()
            elif event.type == pygame.KEYUP:
                self.pressed_keys.discard(event.key)

            # Mouse wheel zoom
            elif event.type == pygame.MOUSEWHEEL:
                mx, my = pygame.mouse.get_pos()
                self.ctx.viewport.apply_zoom_at(self.ctx, event.y, (mx, my))

    def _handle_mouse(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in (1, 3):
                self.dragging = True
                self.drag_button = event.button
                self._set_cell_from_pos(event.pos, event.button)
            elif event.button == 2:
                self.dragging = True
                self.drag_button = 2
                self.drag_start = event.pos
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            if self.drag_button in (1, 3):
                self._set_cell_from_pos(event.pos, self.drag_button)
            elif self.drag_button == 2:
                dx, dy = event.rel
                self.ctx.viewport.offset_x = (self.ctx.viewport.offset_x - dx) % (self.ctx.grid.width * self.ctx.viewport.cell_size)
                self.ctx.viewport.offset_y = (self.ctx.viewport.offset_y - dy) % (self.ctx.grid.height * self.ctx.viewport.cell_size)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

    def _set_cell_from_pos(self, pos, button):
        mx, my = pos
        # Translate pixel to grid index with wrapping
        cx = ((mx + self.ctx.viewport.offset_x) // self.ctx.viewport.cell_size) % self.ctx.grid.width
        cy = ((my + self.ctx.viewport.offset_y) // self.ctx.viewport.cell_size) % self.ctx.grid.height

        self.ctx.grid.cells[cy, cx] = 1 if button == 1 else 0

    # ---------- Simulation logic ----------
    def update(self):
        pan_step = self.ctx.viewport.cell_size * 5
        if pygame.K_LEFT in self.pressed_keys:
            self.ctx.viewport.offset_x = (self.ctx.viewport.offset_x - pan_step) % (self.ctx.grid.width * self.ctx.viewport.cell_size)
            # self.ctx.viewport.clamp_offset()
        if pygame.K_RIGHT in self.pressed_keys:
            self.ctx.viewport.offset_x = (self.ctx.viewport.offset_x + pan_step) % (self.ctx.grid.width * self.ctx.viewport.cell_size)
            # self.ctx.viewport.clamp_offset()
        if pygame.K_UP in self.pressed_keys:
            self.ctx.viewport.offset_y = (self.ctx.viewport.offset_y - pan_step) % (self.ctx.grid.height * self.ctx.viewport.cell_size)
            # self.ctx.viewport.clamp_offset()
        if pygame.K_DOWN in self.pressed_keys:
            self.ctx.viewport.offset_y = (self.ctx.viewport.offset_y + pan_step) % (self.ctx.grid.height * self.ctx.viewport.cell_size)
            # self.ctx.viewport.clamp_offset()
        if self.running:
            self.ctx.grid.tick()

    # ---------- Rendering ----------
    def render(self):
        draw(self.ctx.screen, self.ctx)