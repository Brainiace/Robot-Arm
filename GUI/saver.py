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
from coordinate_mapping import CoordinateMapper

# Initialize mapper globally or pass it in
_mapper = CoordinateMapper()

def save_to_csv(points, offset_x=None, offset_y=None):
    """
    Write all points to drawing.csv.
    Returns a short status message string.
    """
    if not points:
        return "Nothing to save! Draw first."

    # Refresh mapper if needed or use passed offsets if they are different
    # For now, we trust CoordinateMapper to have the latest via load_settings
    _mapper.load_settings()

    with open("drawing.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["x_pixel", "y_pixel", "robot_x_mm", "robot_y_mm", "pen_state"])
        for (px, py, pen) in points:
            rx, ry, rz = _mapper.screen_to_physical(px, py)
            writer.writerow([px, py, round(rx, 2), round(ry, 2), pen])

    print(f"[SAVED] {len(points)} points → drawing.csv")
    return f"Saved {len(points)} points!"
