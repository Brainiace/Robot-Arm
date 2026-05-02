# ================================================================
#  saver.py
#  Saves recorded drawing points to drawing.csv
#
#  Output format:
#    x_pixel, y_pixel, robot_x_mm, robot_y_mm, pen_state
#    pen_state 1 = robot draws to this point
#    pen_state 0 = robot lifts pen and moves to this point
# ================================================================

import csv
from settings import CANVAS_WIDTH, CANVAS_HEIGHT, ROBOT_RANGE_MM


def pixels_to_mm(px, py, offset_x, offset_y):
    """Convert canvas pixel (px, py) into robot millimeter coordinates."""
    rx = round((px / CANVAS_WIDTH)  * ROBOT_RANGE_MM + offset_x, 2)
    ry = round((py / CANVAS_HEIGHT) * ROBOT_RANGE_MM + offset_y, 2)
    return rx, ry


def save_to_csv(points, offset_x, offset_y):
    """
    Write all points to drawing.csv.
    Returns a short status message string.
    """
    if not points:
        return "Nothing to save! Draw first."

    with open("drawing.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["x_pixel", "y_pixel", "robot_x_mm", "robot_y_mm", "pen_state"])
        for (px, py, pen) in points:
            rx, ry = pixels_to_mm(px, py, offset_x, offset_y)
            writer.writerow([px, py, rx, ry, pen])

    print(f"[SAVED] {len(points)} points → drawing.csv")
    return f"Saved {len(points)} points!"
