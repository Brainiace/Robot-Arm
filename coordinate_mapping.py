import config
from calibration_manager import load_calibration

class CoordinateMapper:
    def __init__(self):
        self.load_settings()

    def load_settings(self):
        cal = load_calibration()
        self.scale = cal["scale"]
        self.offset_x = cal["offset_x"]
        self.offset_y = cal["offset_y"]
        self.offset_z = cal["offset_z"]

    def screen_to_physical(self, px_x, px_y, z_mm=None):
        """
        Translates Pygame canvas-local pixels to physical coordinates in mm.
        (0,0) in canvas-local is top-left of the canvas.
        """
        if z_mm is None:
            z_mm = self.offset_z

        # Map pixels to mm relative to origin offset
        # mm_x: positive to the right
        mm_x = (px_x - self.offset_x) * self.scale
        # mm_y: positive going FORWARD (away from robot base)
        # In Pygame, Y increases DOWN.
        # If ORIGIN_PX_Y is at the bottom (400), then pixel 0 is 400 pixels away.
        mm_y = (self.offset_y - px_y) * self.scale

        return mm_x, mm_y, z_mm

    def physical_to_screen(self, mm_x, mm_y):
        """Translates physical coordinates back to canvas-local pixels."""
        px_x = (mm_x / self.scale) + self.offset_x
        px_y = self.offset_y - (mm_y / self.scale)
        return px_x, px_y
