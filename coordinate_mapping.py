import config

class CoordinateMapper:
    def __init__(self, scale=config.SCALE_FACTOR, offset_x=config.ORIGIN_OFFSET_X, offset_y=config.ORIGIN_OFFSET_Y):
        self.scale = scale
        self.offset_x = offset_x
        self.offset_y = offset_y

    def screen_to_physical(self, px_x, px_y, z_mm=config.Z_WRITE):
        """
        Translates Pygame screen pixels to physical coordinates in mm.
        Pygame (0,0) is top-left.
        """
        # Map pixels to mm relative to origin offset
        # Example: if offset is (200, 200), then pixel (200, 200) becomes (0, 0) mm.
        mm_x = (px_x - self.offset_x) * self.scale
        # Y is often inverted in screen coordinates
        mm_y = (self.offset_y - px_y) * self.scale

        return mm_x, mm_y, z_mm

    def physical_to_screen(self, mm_x, mm_y):
        """Translates physical coordinates back to screen pixels (for visualization/debugging)."""
        px_x = (mm_x / self.scale) + self.offset_x
        px_y = self.offset_y - (mm_y / self.scale)
        return px_x, px_y
