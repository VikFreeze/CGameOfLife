# app/gallery_state.py
import pygame
from state_machine import BaseState
from gallery import Gallery
from renderer import draw

class GalleryState(BaseState):
    """Modal overlay that shows the pattern gallery."""
    def __init__(self, ctx):
        super().__init__(ctx)
        self.was_running = ctx.simulation_state.running
        ctx.simulation_state.running = False

        # gallery window
        gw, gh = 600, ctx.screen.get_height() - 100
        center_x = ctx.screen.get_width() // 2 - gw // 2
        center_y = ctx.screen.get_height() // 2 - gh // 2
        self.gallery_rect = pygame.Rect(center_x, center_y, gw, gh)

        self.gallery = Gallery(
            ctx.screen,
            self.gallery_rect,
            on_select=self.place_pattern,
        )
        # Close callback is handled by ESC inside Gallery

    # ---------- Pattern placement ----------
    def place_pattern(self, pattern, orientation, flip_x, flip_y):
        cells = pattern.cells.astype(int)
        if flip_x:
            cells = np.flip(cells, axis=1)
        if flip_y:
            cells = np.flip(cells, axis=0)
        cells = np.rot90(cells, k=orientation)
        ph, pw = cells.shape
        cx = (
            self.ctx.viewport.window_width // 2
            - pw // 2
            - self.ctx.viewport.offset_x // self.ctx.viewport.cell_size
        )
        cy = (
            self.ctx.viewport.window_height // 2
            - ph // 2
            - self.ctx.viewport.offset_y // self.ctx.viewport.cell_size
        )
        for y in range(ph):
            for x in range(pw):
                if cells[y, x]:
                    gx = cx + x
                    gy = cy + y
                    if 0 <= gx < self.ctx.grid.width and 0 <= gy < self.ctx.grid.height:
                        self.ctx.grid.cells[gy, gx] = 1

    # ---------- State transition ----------
    def close(self):
        self.ctx.simulation_state.running = self.was_running
        self.ctx.state_machine.switch(self.ctx.simulation_state)

    # ---------- Event handling ----------
    def handle_events(self, events):
        for event in events:
            self.gallery.handle_event(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.close()

    # ---------- Update ----------
    def update(self):
        pass

    # ---------- Rendering ----------
    def render(self):
        overlay = pygame.Surface(self.ctx.screen.get_size(), flags=pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.ctx.screen.blit(overlay, (0, 0))
        draw(self.ctx.screen, self.ctx, None, self.ctx.font)
        self.gallery.draw(self.ctx.font)
        pygame.display.flip()