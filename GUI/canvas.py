# ================================================================
#  canvas.py
#  The white drawing area on the left side.
#  Handles mouse drawing, recording points, pen/eraser switching.
# ================================================================

import pygame
from settings import (WHITE, BLACK, CANVAS_BORDER,
                      CANVAS_X, CANVAS_Y, CANVAS_WIDTH, CANVAS_HEIGHT,
                      BRUSH_SIZE, ERASER_SIZE)


class Canvas:
    """
    Manages the white drawing surface.

    Stores all drawn points as (x, y, pen_state):
      pen_state = 1  →  pen is down, robot draws here
      pen_state = 0  →  pen is up, robot just moves here
    """

    def __init__(self):
        # The white surface the user draws on
        self.surface = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
        self.surface.fill(WHITE)

        # Rectangle for hit-testing (is the mouse inside the canvas?)
        self.rect = pygame.Rect(CANVAS_X, CANVAS_Y, CANVAS_WIDTH, CANVAS_HEIGHT)

        self.recorded_points = []   # All (x, y, pen_state) tuples
        self.is_drawing      = False
        self.previous_pos    = None
        self.stroke_count    = 0
        self.tool            = "pen"   # "pen" or "eraser"

    def handle_events(self, events):
        """Process mouse events and draw on the canvas surface."""

        for event in events:

            # Mouse button pressed — start a stroke
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.is_drawing = True
                    # Convert from screen coordinates to canvas-local coordinates
                    cx = event.pos[0] - CANVAS_X
                    cy = event.pos[1] - CANVAS_Y
                    self.previous_pos = (cx, cy)
                    if self.tool == "pen":
                        self.stroke_count += 1
                        self.recorded_points.append((cx, cy, 0))  # pen up → move here

            # Mouse button released — end stroke
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.is_drawing   = False
                self.previous_pos = None

            # Mouse moved while button held — draw
            elif event.type == pygame.MOUSEMOTION and self.is_drawing:
                if self.rect.collidepoint(event.pos):
                    cx = event.pos[0] - CANVAS_X
                    cy = event.pos[1] - CANVAS_Y

                    if self.previous_pos is not None:
                        if self.tool == "pen":
                            pygame.draw.line(self.surface, BLACK,
                                             self.previous_pos, (cx, cy),
                                             BRUSH_SIZE)
                            self.recorded_points.append((cx, cy, 1))  # pen down → draw

                        elif self.tool == "eraser":
                            pygame.draw.circle(self.surface, WHITE,
                                               (cx, cy), ERASER_SIZE)

                    self.previous_pos = (cx, cy)

    def draw(self, screen):
        """Render the canvas and its border onto the screen."""
        # White drawing surface
        screen.blit(self.surface, (CANVAS_X, CANVAS_Y))

        # Thick dark border — matches the design image
        pygame.draw.rect(screen, CANVAS_BORDER, self.rect, 5)

    def clear(self):
        """Erase everything and reset all recorded data."""
        self.surface.fill(WHITE)
        self.recorded_points.clear()
        self.stroke_count = 0

    def set_tool(self, name):
        """Switch active tool: 'pen' or 'eraser'."""
        self.tool = name

    def get_points(self):
        """Return all recorded drawing points."""
        return self.recorded_points
