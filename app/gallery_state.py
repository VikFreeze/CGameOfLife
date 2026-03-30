# app/gallery_state.py
import pygame
from state_machine import BaseState
from ui import Gallery
from renderer import draw

class GalleryState(BaseState):
    """A modal overlay that shows the pattern gallery."""

    def __init__(self, ctx):
        super().__init__(ctx)
        # Remember if the simulation was running so we can restore it
        self.was_running = ctx.simulation_state.running
        ctx.simulation_state.running = False

        # Define the rectangle for the gallery window
        gw, gh = 600, ctx.screen.get_height() - 100                 # width × height of the modal
        center_x = ctx.screen.get_width() // 2 - gw // 2
        center_y = ctx.screen.get_height() // 2 - gh // 2
        self.gallery_rect = pygame.Rect(center_x, center_y, gw, gh)

        # Create the Gallery widget
        self.gallery = Gallery(
            ctx.screen,
            self.gallery_rect,
            ctx.patterns,
            on_select=self.place_pattern
        )
        # allow the widget to call back when close button pressed
        self.gallery.on_close = self.close

    # --------------------------------------------------------------------- #
    # Pattern placement callback
    # --------------------------------------------------------------------- #
    def place_pattern(self, pattern):
        cells = pattern.cells
        ph, pw = cells.shape
        # compute target top‑left corner (in cell coordinates)
        cx = (self.ctx.viewport.window_width // 2 - pw // 2 -
              self.ctx.viewport.offset_x // self.ctx.viewport.cell_size)
        cy = (self.ctx.viewport.window_height // 2 - ph // 2 -
              self.ctx.viewport.offset_y // self.ctx.viewport.cell_size)

        for y in range(ph):
            for x in range(pw):
                if cells[y, x]:
                    gx = cx + x
                    gy = cy + y
                    if 0 <= gx < self.ctx.grid.width and 0 <= gy < self.ctx.grid.height:
                        self.ctx.grid.cells[gy, gx] = 1

    # --------------------------------------------------------------------- #
    # UI callbacks
    # --------------------------------------------------------------------- #
    def close(self):
        # restore simulation state
        self.ctx.simulation_state.running = self.was_running
        self.ctx.state_machine.switch(self.ctx.simulation_state)

    # --------------------------------------------------------------------- #
    # event handling – delegate everything to the widget
    # --------------------------------------------------------------------- #
    def handle_events(self, events):
        """Forward every event to the gallery widget – plus ESC → close."""
        for event in events:
            # ← already handled by the gallery widget
            self.gallery.handle_event(event)

            # ESC → close the gallery (no other state will be affected)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.close()

    # --------------------------------------------------------------------- #
    # update – nothing to do (simulation stays paused)
    # --------------------------------------------------------------------- #
    def update(self):
        pass

    # --------------------------------------------------------------------- #
    # rendering – draw normal grid + dark overlay + gallery window
    # --------------------------------------------------------------------- #
    def render(self):
        # 1️⃣  draw darkened background
        overlay = pygame.Surface(self.ctx.screen.get_size(), flags=pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.ctx.screen.blit(overlay, (0, 0))

        # 2️⃣  draw the grid underneath
        draw(self.ctx.screen, self.ctx, None, self.ctx.font)

        # 3️⃣  draw the gallery window on top
        self.gallery.draw(self.ctx.font)
        pygame.display.flip()