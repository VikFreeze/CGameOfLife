# app/events.py
import pygame
from context import AppState

class InputHandler:
    def __init__(self, ctx):
        self.ctx = ctx
        self.pressed_keys = set()
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
                self.pressed_keys.add(event.key)
                # F11 → toggle fullscreen / windowed
                if event.key == pygame.K_SPACE:
                    # Toggle Simulation State
                    self.ctx.state = AppState.RUNNING if self.ctx.state == AppState.PAUSED else AppState.PAUSED
                if event.key == pygame.K_F11:
                    # Toogle Fullscreen
                    self.ctx.fullscreen = not self.ctx.fullscreen
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) if self.ctx.fullscreen else pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                    # update viewport window size
                    self.ctx.viewport.window_width = screen.get_width()
                    self.ctx.viewport.window_height = screen.get_height()
                if event.key == pygame.K_r:
                    self.ctx.grid.reset()
                    self.ctx.viewport.offset_x = self.ctx.viewport.offset_y = 0
                    self.ctx.viewport.cell_size = 1
                    self.ctx.state = AppState.PAUSED
                # Q → quit the program
                if event.key == pygame.K_q:
                    pygame.quit()
                    return True
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                    self._handlePanning()
            
            elif event.type == pygame.KEYUP:
                self.pressed_keys.discard(event.key)
        return False
    
    def _handlePanning(self):
        pan_step = self.ctx.viewport.cell_size * 5
        if pygame.K_LEFT in self.pressed_keys:
            self.ctx.viewport.offset_x = (self.ctx.viewport.offset_x - pan_step) % (self.ctx.grid.width * self.ctx.viewport.cell_size)
        if pygame.K_RIGHT in self.pressed_keys:
            self.ctx.viewport.offset_x = (self.ctx.viewport.offset_x + pan_step) % (self.ctx.grid.width * self.ctx.viewport.cell_size)
        if pygame.K_UP in self.pressed_keys:
            self.ctx.viewport.offset_y = (self.ctx.viewport.offset_y - pan_step) % (self.ctx.grid.height * self.ctx.viewport.cell_size)
        if pygame.K_DOWN in self.pressed_keys:
            self.ctx.viewport.offset_y = (self.ctx.viewport.offset_y + pan_step) % (self.ctx.grid.height * self.ctx.viewport.cell_size)
    
    def _set_cell_from_pos(self, pos, button):
        mx, my = pos
        # Translate pixel to grid index with wrapping
        cx = ((mx + self.ctx.viewport.offset_x) // self.ctx.viewport.cell_size) % self.ctx.grid.width
        cy = ((my + self.ctx.viewport.offset_y) // self.ctx.viewport.cell_size) % self.ctx.grid.height

        self.ctx.grid.cells[cy, cx] = 1 if button == 1 else 0