import pygame
import os
import math
import config
from coordinate_mapping import CoordinateMapper
from settings import CANVAS_WIDTH, CANVAS_HEIGHT

os.environ['SDL_VIDEODRIVER'] = 'dummy'
pygame.init()

def test_visualization():
    print("--- Testing Visualization Surface Logic ---")
    mapper = CoordinateMapper()
    px_x, px_y = mapper.physical_to_screen(0, 0)
    reach_px = config.ROBOT_REACH / mapper.scale

    # 1. Test the "Hole" logic
    temp_surface = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
    temp_surface.set_colorkey((0, 255, 0)) # Green is transparent
    temp_surface.fill((255, 100, 100)) # Red
    pygame.draw.circle(temp_surface, (0, 255, 0), (int(px_x), int(px_y)), int(reach_px))

    # Check if center is green. (px_x, px_y) is (295, 400), which is bottom center.
    # get_at uses (x, y). (295, 399) should be green.
    test_px_y = int(px_y) - 1
    center_color = temp_surface.get_at((int(px_x), test_px_y))
    corner_color = temp_surface.get_at((0, 0))

    print(f"Center-ish color at (295, 399): {center_color}")
    print(f"Corner color: {corner_color}")

    assert center_color == (0, 255, 0, 255)
    assert corner_color == (255, 100, 100, 255)

    print("Visualization Logic Passed\n")

if __name__ == "__main__":
    test_visualization()
