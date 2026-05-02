import math
import config
from coordinate_mapping import CoordinateMapper
from GUI.canvas import Canvas
import pygame
import os

# Mock pygame for testing without a display
os.environ['SDL_VIDEODRIVER'] = 'dummy'
pygame.init()

def test_reachability():
    print("--- Testing Reachability Logic ---")
    mapper = CoordinateMapper()
    # origin (295, 400), reach 180mm, scale 0.5 -> reach 360 pixels

    canvas = Canvas()

    # Bottom center (Origin) - should be reachable
    assert canvas.is_reachable(295, 400) == True
    print("Origin (295, 400) is reachable")

    # 100mm forward (200 pixels up from 400 -> 200)
    assert canvas.is_reachable(295, 200) == True
    print("Point (295, 200) [100mm forward] is reachable")

    # 200mm forward (400 pixels up from 400 -> 0) - Out of reach (180mm max)
    assert canvas.is_reachable(295, 0) == False
    print("Point (295, 0) [200mm forward] is OUT of reach")

    # Far left corner (0,0) -> dist to (295, 400) is sqrt(295^2 + 400^2) = 497 pixels = 248.5mm
    assert canvas.is_reachable(0, 0) == False
    print("Point (0, 0) is OUT of reach")

    print("Reachability Logic Passed\n")

if __name__ == "__main__":
    test_reachability()
