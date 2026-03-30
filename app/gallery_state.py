# app/gallery_state.py
import pygame
from ui import Button, Panel
from renderer import render_grid
from state_machine import BaseState

class GalleryState(BaseState):
    """Modal overlay that shows the pattern gallery."""

    def __init__(self, ctx):
        super().__init__(ctx)

        # Remember if the simulation was running
        self.was_running = ctx.simulation_state.running
        ctx.simulation_state.running = False

        # Build a full‑screen panel that will hold the pattern buttons
        self.panel = Panel(
            ctx.screen,
            self._create_pattern_buttons(),
            panel_height=ctx.screen.get_height()   # full height
        )
        # Override the panel’s height so `Panel.update_rects()` puts it at (0,0)
        self.panel.panel_height = ctx.screen.get_height()

    # ------------------------------------------------------------------
    # Helper – build pattern buttons
    # ------------------------------------------------------------------
    def _create_pattern_buttons(self):
        buttons = []
        btn_w, btn_h = 120, 80
        margin = 10

        for idx, pat in enumerate(self.ctx.patterns):
            x = margin + (idx % 4) * (btn_w + margin)
            y = margin + (idx // 4) * (btn_h + margin)

            # capture the pattern in the callback
            btn = Button(pygame.Rect(x, y, btn_w, btn_h), pat.title,
                         lambda p=pat: self.place_pattern(p))
            buttons.append(btn)

        # Close button
        close_btn = Button(
            pygame.Rect(10, self.ctx.screen.get_height() - 60, 80, 40),
            "Close", self.close)
        buttons.append(close_btn)

        return buttons

    # ------------------------------------------------------------------
    # Pattern placement
    # ------------------------------------------------------------------
    def place_pattern(self, pattern):
        """Place the selected pattern centred in the viewport."""
        cells = pattern.cells
        ph, pw = cells.shape
        cs = self.ctx.viewport.cell_size

        # Position in *grid* coordinates
        cx = ((self.ctx.viewport.window_width // 2 - pw * cs // 2
               - self.ctx.viewport.offset_x) // cs)
        cy = ((self.ctx.viewport.window_height // 2 - ph * cs // 2
               - self.ctx.viewport.offset_y) // cs)

        for y in range(ph):
            for x in range(pw):
                if cells[y, x]:
                    gx = cx + x
                    gy = cy + y
                    if 0 <= gx < self.ctx.grid.width and 0 <= gy < self.ctx.grid.height:
                        self.ctx.grid.cells[gy, gx] = 1

    # ------------------------------------------------------------------
    # Close gallery
    # ------------------------------------------------------------------
    def close(self):
        self.ctx.simulation_state.running = self.was_running
        self.ctx.state_machine.switch(self.ctx.simulation_state)

    # ------------------------------------------------------------------
    # Event handling
    # ------------------------------------------------------------------
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Let the gallery panel handle its own UI events
            self.panel.handle_event(event)

            # All other events are deliberately ignored

    # ------------------------------------------------------------------
    # Update – nothing to do, simulation stays paused
    # ------------------------------------------------------------------
    def update(self):
        pass

    # ------------------------------------------------------------------
    # Rendering – dark overlay + grid + gallery panel
    # ------------------------------------------------------------------
    def render(self):
        # Dark translucent overlay
        overlay = pygame.Surface(self.ctx.screen.get_size(), flags=pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.ctx.screen.blit(overlay, (0, 0))

        # Grid underneath
        render_grid(self.ctx.screen, self.ctx.grid, self.ctx.viewport.cell_size,
                    (self.ctx.viewport.offset_x, self.ctx.viewport.offset_y))

        # Gallery panel
        self.panel.draw(self.ctx.font)

        pygame.display.flip()