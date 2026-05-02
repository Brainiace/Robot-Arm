# ================================================================
#  canvas.py
#  The white drawing area on the left side.
#  Handles mouse drawing, recording points, pen/eraser switching.
# ================================================================

import pygame
import math
from settings import (WHITE, BLACK, CANVAS_BORDER,
                      CANVAS_X, CANVAS_Y, CANVAS_WIDTH, CANVAS_HEIGHT,
                      BRUSH_SIZE, ERASER_SIZE)
import config
from coordinate_mapping import CoordinateMapper

class Canvas:
    """
    Manages the white drawing surface.
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

        self.mapper = CoordinateMapper()

    def is_reachable(self, cx, cy):
        """Checks if a canvas-local coordinate is within robot reach."""
        mx, my, mz = self.mapper.screen_to_physical(cx, cy)
        dist = math.sqrt(mx**2 + my**2)
        return dist <= config.ROBOT_REACH

    def handle_events(self, events):
        """Process mouse events and draw on the canvas surface."""

        for event in events:

            # Mouse button pressed — start a stroke
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    cx = event.pos[0] - CANVAS_X
                    cy = event.pos[1] - CANVAS_Y

                    if self.is_reachable(cx, cy):
                        self.is_drawing = True
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

                    if self.is_reachable(cx, cy):
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
                    else:
                        # If we move out of reach while drawing, stop the stroke
                        self.is_drawing = False
                        self.previous_pos = None

    def draw(self, screen):
        """Render the canvas and its border onto the screen."""
        # White drawing surface
        screen.blit(self.surface, (CANVAS_X, CANVAS_Y))

        # Draw reach visualization
        self.draw_reach_limit(screen)

        # Thick dark border — matches the design image
        pygame.draw.rect(screen, CANVAS_BORDER, self.rect, 5)

    def draw_reach_limit(self, screen):
        """Draws the semi-transparent reach limit on the canvas."""
        # Center and radius in pixels
        # mapper.physical_to_screen returns canvas-local coords
        px_x, px_y = self.mapper.physical_to_screen(0, 0)
        reach_px = config.ROBOT_REACH / self.mapper.scale

        # 1. Create a surface for the shading
        temp_surface = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
        temp_surface.set_colorkey((0, 255, 0)) # Green is transparent
        temp_surface.fill((255, 100, 100))     # Light red (before alpha)

        # 2. Draw the safe zone as a green circle (will be transparent due to colorkey)
        # Clamp coordinates to ensure it draws within surface if needed,
        # though pygame.draw.circle handles out-of-bounds.
        pygame.draw.circle(temp_surface, (0, 255, 0), (int(px_x), int(px_y)), int(reach_px))

        # 3. Set overall transparency for the red out-of-bounds area
        temp_surface.set_alpha(60)

        # 4. Blit to screen
        screen.blit(temp_surface, (CANVAS_X, CANVAS_Y))

        # 5. Draw the circle boundary (arc/line) for better visibility
        pygame.draw.circle(screen, (200, 0, 0),
                           (int(px_x + CANVAS_X), int(px_y + CANVAS_Y)),
                           int(reach_px), 2)

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
