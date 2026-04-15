# app/events.py
import pygame
from context import AppState
from config import WINDOW_WIDTH, WINDOW_HEIGHT, MAX_SIMULATION_INTERVAL, MIN_SIMULATION_INTERVAL, STEP_PERCENTAGE

class InputHandler:
    def __init__(self, ctx):
        self.ctx = ctx
        self.dragging = False
        self.drag_button = 0

    def Handle(self, events) -> bool:
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            
            # Mouse events
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION, pygame.MOUSEWHEEL):
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
                elif event.type == pygame.MOUSEWHEEL:
                        mx, my = pygame.mouse.get_pos()
                        self.ctx.viewport.apply_zoom_at(self.ctx, event.y, (mx, my))
            
            # Key events
            elif event.type == pygame.KEYDOWN:
                # Q → quit the program
                if event.key == pygame.K_q:
                    pygame.quit()
                    return True
                elif event.key == pygame.K_PAGEDOWN:
                    self.ctx.simulation_interval = min(self.ctx.simulation_interval + max(1, int(self.ctx.simulation_interval * STEP_PERCENTAGE)), MAX_SIMULATION_INTERVAL)
                elif event.key == pygame.K_PAGEUP:
                    self.ctx.simulation_interval = max(self.ctx.simulation_interval - max(1, int(self.ctx.simulation_interval * STEP_PERCENTAGE)), MIN_SIMULATION_INTERVAL)
                elif event.key == pygame.K_n and self.ctx.state == AppState.PAUSED:
                    # Single step if simulation is paused
                    self.ctx.grid.tick()
                elif event.key == pygame.K_SPACE:
                    # Toggle Simulation State
                    self.ctx.state = AppState.RUNNING if self.ctx.state == AppState.PAUSED else AppState.PAUSED
                # F11 → toggle fullscreen / windowed
                elif event.key == pygame.K_F11:
                    # Toogle Fullscreen
                    self.ctx.fullscreen = not self.ctx.fullscreen
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) if self.ctx.fullscreen else pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                    # update viewport window size
                    self.ctx.viewport.window_width = screen.get_width()
                    self.ctx.viewport.window_height = screen.get_height()
                elif event.key == pygame.K_r:
                    # Reset
                    self.ctx.grid.reset()
                    self.ctx.viewport.offset_x = self.ctx.viewport.offset_y = 0
                    self.ctx.viewport.cell_size = 1
                    self.ctx.state = AppState.PAUSED
                elif event.key == pygame.K_k:
                    # Set grid randomly
                    self.ctx.grid.randomize(0.1)
            
            # Window events
            elif event.type == pygame.ACTIVEEVENT:
                if event.state & pygame.APPINPUTFOCUS:
                    if event.gain == 0:
                        if self.ctx.fullscreen:
                            self.ctx.fullscreen = False
                            self.ctx.viewport.window_width, self.ctx.viewport.window_height = pygame.display.get_window_size()
            elif event.type == pygame.VIDEORESIZE:
                new_w, new_h = event.w, event.h
                # Cap maximum window dimensions
                if new_w > WINDOW_WIDTH:
                    new_w = WINDOW_WIDTH
                if new_h > WINDOW_HEIGHT:
                    new_h = WINDOW_HEIGHT
                pygame.display.set_mode((new_w, new_h), pygame.RESIZABLE)
                self.ctx.viewport.window_width = new_w
                self.ctx.viewport.window_height = new_h

        
        # Continuous panning when holding the arrow keys
        keys = pygame.key.get_pressed()
        pan_step = self.ctx.viewport.cell_size * 5
        if keys[pygame.K_LEFT]:
            self.ctx.viewport.offset_x = (self.ctx.viewport.offset_x - pan_step) % (self.ctx.grid.width * self.ctx.viewport.cell_size)
        if keys[pygame.K_RIGHT]:
            self.ctx.viewport.offset_x = (self.ctx.viewport.offset_x + pan_step) % (self.ctx.grid.width * self.ctx.viewport.cell_size)
        if keys[pygame.K_UP]:
            self.ctx.viewport.offset_y = (self.ctx.viewport.offset_y - pan_step) % (self.ctx.grid.height * self.ctx.viewport.cell_size)
        if keys[pygame.K_DOWN]:
            self.ctx.viewport.offset_y = (self.ctx.viewport.offset_y + pan_step) % (self.ctx.grid.height * self.ctx.viewport.cell_size)

        return False
    
    def _set_cell_from_pos(self, pos, button):
        # Translate pixel to grid index with wrapping
        cx = ((pos[0] + self.ctx.viewport.offset_x) // self.ctx.viewport.cell_size) % self.ctx.grid.width
        cy = ((pos[1] + self.ctx.viewport.offset_y) // self.ctx.viewport.cell_size) % self.ctx.grid.height
        self.ctx.grid.cells[cy, cx] = 1 if button == 1 else 0