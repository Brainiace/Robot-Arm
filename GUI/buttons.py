# ================================================================
#  buttons.py
#  Three button types that match the design exactly:
#
#  CircleButton  — big filled circle (START, CLEAR, PEN, ERASER)
#  PillButton    — orange rounded rectangle (+X, -X, etc.)
#  ValueBox      — white rounded rectangle showing offset value
# ================================================================

import pygame
from settings import WHITE, BLACK


# ----------------------------------------------------------------
#  CircleButton
#  The 4 big round buttons at the bottom of the screen.
# ----------------------------------------------------------------

class CircleButton:
    """
    A large circle button with a colored fill and darker border.
    Can show text OR an icon image inside.

    Usage:
        btn = CircleButton(cx, cy, radius, fill, border, "LABEL", text_color)
        btn.draw(screen)              # draw it every frame
        btn.was_clicked(events)       # True only on the click frame
    """

    def __init__(self, cx, cy, radius, fill_color, border_color,
                 label="", text_color=WHITE, font_size=18):
        self.cx           = cx
        self.cy           = cy
        self.radius       = radius
        self.fill_color   = fill_color
        self.border_color = border_color
        self.label        = label
        self.text_color   = text_color
        self.font         = pygame.font.SysFont("consolas", font_size, bold=True)

    def draw(self, surface, icon=None):
        """
        Draw the circle. Pass an icon Surface to show an image instead of text.
        """
        # Draw filled circle
        pygame.draw.circle(surface, self.fill_color,
                           (self.cx, self.cy), self.radius)
        # Draw border (4px thick)
        pygame.draw.circle(surface, self.border_color,
                           (self.cx, self.cy), self.radius, 4)

        if icon:
            # Center the icon image inside the circle
            ix = self.cx - icon.get_width()  // 2
            iy = self.cy - icon.get_height() // 2
            surface.blit(icon, (ix, iy))
        elif self.label:
            text = self.font.render(self.label, True, self.text_color)
            surface.blit(text, (
                self.cx - text.get_width()  // 2,
                self.cy - text.get_height() // 2
            ))

    def was_clicked(self, events):
        """
        Returns True only on the exact frame the mouse is clicked
        inside this circle. Uses circle collision (not rectangle).
        """
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                dx = event.pos[0] - self.cx
                dy = event.pos[1] - self.cy
                if (dx * dx + dy * dy) <= (self.radius * self.radius):
                    return True
        return False


# ----------------------------------------------------------------
#  PillButton
#  The orange rounded-rectangle buttons: +X +Y +Z -X -Y -Z
# ----------------------------------------------------------------

class PillButton:
    """
    An orange pill-shaped (heavily rounded rectangle) button.
    Has a slightly darker orange border around it.

    Usage:
        btn = PillButton(x, y, w, h, "+X", fill, border, text_color)
        btn.draw(screen)
        btn.was_clicked(events)   # True only on the click frame
    """

    def __init__(self, x, y, w, h, label,
                 fill_color, border_color, text_color):
        self.rect         = pygame.Rect(x, y, w, h)
        self.label        = label
        self.fill_color   = fill_color
        self.border_color = border_color
        self.text_color   = text_color
        self.font         = pygame.font.SysFont("consolas", 22, bold=True)
        # Corner radius — large value makes it a true pill shape
        self.radius       = h // 2

    def draw(self, surface):
        # Draw filled orange pill
        pygame.draw.rect(surface, self.fill_color,
                         self.rect, border_radius=self.radius)
        # Draw darker orange border (3px)
        pygame.draw.rect(surface, self.border_color,
                         self.rect, 3, border_radius=self.radius)

        # Draw centered label
        text = self.font.render(self.label, True, self.text_color)
        surface.blit(text, (
            self.rect.centerx - text.get_width()  // 2,
            self.rect.centery - text.get_height() // 2
        ))

    def was_clicked(self, events):
        """Returns True only on the exact frame this button is clicked."""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    return True
        return False


# ----------------------------------------------------------------
#  ValueBox
#  White rounded rectangle that shows the current offset value.
#  This is display-only, not clickable.
# ----------------------------------------------------------------

class ValueBox:
    """
    A white oval/rounded box showing a value like '0.0mm'.
    Not interactive — just displays the number.

    Usage:
        box = ValueBox(x, y, w, h)
        box.draw(screen, 0.0)   # pass the current value
    """

    def __init__(self, x, y, w, h):
        self.rect   = pygame.Rect(x, y, w, h)
        self.font   = pygame.font.SysFont("consolas", 18, bold=True)
        self.radius = h // 2   # fully rounded ends

    def draw(self, surface, value):
        # White fill
        pygame.draw.rect(surface, WHITE,
                         self.rect, border_radius=self.radius)
        # Thick dark border
        pygame.draw.rect(surface, BLACK,
                         self.rect, 3, border_radius=self.radius)

        # Value text centered
        text = self.font.render(f"{value:.1f}mm", True, BLACK)
        surface.blit(text, (
            self.rect.centerx - text.get_width()  // 2,
            self.rect.centery - text.get_height() // 2
        ))
