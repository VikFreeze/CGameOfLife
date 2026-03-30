# app/simulation_state.py
import pygame
from ui import Panel, Button
from state_machine import BaseState
from renderer import draw
from viewport import Viewport
from gallery_state import GalleryState

class SimulationState(BaseState):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.running = False
        self.pressed_keys = set()
        self.dragging = False
        self.drag_button = 0

        # UI – bottom panel
        self.panel = Panel(
            ctx.screen,
            [
                Button(pygame.Rect(10, 10, 80, 40), "Start", self.toggle_run),
                Button(pygame.Rect(100, 10, 80, 40), "Reset", self.reset),
                Button(pygame.Rect(190, 10, 80, 40), "Zoom+", self.zoom_in),
                Button(pygame.Rect(280, 10, 80, 40), "Zoom-", self.zoom_out),
                Button(pygame.Rect(370, 10, 80, 40), "Patterns", self.open_gallery),
            ],
            ctx.panel_height
        )
        self.toggle_text = "Start"

    # ------------------------------------------------------------------
    # UI callbacks
    # ------------------------------------------------------------------
    def toggle_run(self):
        self.running = not self.running
        self.toggle_text = "Pause" if self.running else "Start"

    def reset(self):
        self.ctx.grid.reset()
        self.ctx.viewport.offset_x = self.ctx.viewport.offset_y = 0
        self.ctx.viewport.clamp_offset()
        self.running = False

    def zoom_in(self):
        self.ctx.viewport.apply_zoom(+1)

    def zoom_out(self):
        self.ctx.viewport.apply_zoom(-1)

    def open_gallery(self):
        self.ctx.state_machine.switch(GalleryState(self.ctx))

    # ------------------------------------------------------------------
    # Event handling
    # ------------------------------------------------------------------
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Mouse editing
            if event.type in (pygame.MOUSEBUTTONDOWN,
                               pygame.MOUSEBUTTONUP,
                               pygame.MOUSEMOTION):
                self.handle_mouse(event)

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
                self.ctx.viewport.apply_zoom_at(event.y, (mx, my))

            # Panel button events
            self.panel.handle_event(event)

    def handle_mouse(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in (1, 3):
                self.dragging = True
                self.drag_button = event.button
                self.set_cell_from_pos(event.pos, event.button)
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.set_cell_from_pos(event.pos, self.drag_button)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

    def set_cell_from_pos(self, pos, button):
        mx, my = pos
        if my < self.ctx.screen.get_height() - self.ctx.panel_height:
            cx = (mx - self.ctx.viewport.offset_x) // self.ctx.viewport.cell_size
            cy = (my - self.ctx.viewport.offset_y) // self.ctx.viewport.cell_size
            if 0 <= cx < self.ctx.grid.width and 0 <= cy < self.ctx.grid.height:
                self.ctx.grid.cells[cy, cx] = 1 if button == 1 else 0

    # ------------------------------------------------------------------
    # Simulation logic
    # ------------------------------------------------------------------
    def update(self):
        pan_step = self.ctx.viewport.cell_size * 5
        if pygame.K_LEFT in self.pressed_keys:
            self.ctx.viewport.offset_x += pan_step
            self.ctx.viewport.clamp_offset()
        if pygame.K_RIGHT in self.pressed_keys:
            self.ctx.viewport.offset_x -= pan_step
            self.ctx.viewport.clamp_offset()
        if pygame.K_UP in self.pressed_keys:
            self.ctx.viewport.offset_y += pan_step
            self.ctx.viewport.clamp_offset()
        if pygame.K_DOWN in self.pressed_keys:
            self.ctx.viewport.offset_y -= pan_step
            self.ctx.viewport.clamp_offset()

        if self.running:
            self.ctx.grid.tick()

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------
    def render(self):
        draw(self.ctx.screen, self.ctx, self.panel, self.ctx.font)