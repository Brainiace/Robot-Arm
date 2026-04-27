import math
import config
from kinematics import WritingArmController, FABRIK
from ik_solver import IKSolver
from path_planner import PathPlanner
from coordinate_mapping import CoordinateMapper

def test_coordinate_mapping():
    print("--- Testing Coordinate Mapping ---")
    mapper = CoordinateMapper(scale=1.0, offset_x=200, offset_y=200)

    # Center of screen should be (0,0) mm
    x, y, z = mapper.screen_to_physical(200, 200, 0)
    print(f"Screen (200, 200) -> Physical ({x}, {y}, {z})")
    assert x == 0 and y == 0

    # Top-left (0,0) should be (-200, 200) mm
    x, y, z = mapper.screen_to_physical(0, 0, 10)
    print(f"Screen (0, 0) -> Physical ({x}, {y}, {z})")
    assert x == -200 and y == 200 and z == 10
    print("Coordinate Mapping Passed\n")

def test_ik_vertical_constraint():
    print("--- Testing IK Vertical Constraint ---")
    ik = IKSolver()
    # Test multiple points
    test_points = [(100, 0, 0), (0, 100, 0), (50, 50, 10)]

    for pt in test_points:
        joints = ik.solve(*pt)
        # joints = [s1, s2, s3, s4, s5]
        # s2 = 90 + q2
        # s3 = 180 + q3
        # s4 = 180 + q4
        # constraint: q2 + q3 + q4 = -90
        q2 = math.radians(joints[1] - 90)
        q3 = math.radians(joints[2] - 180)
        q4 = math.radians(joints[3] - 180)

        sum_angles = math.degrees(q2 + q3 + q4)
        print(f"Point {pt} -> Sum of angles: {sum_angles:.2f} degrees")
        # For points that might be clamped, we check if the constraint is still reasonable
        # or if we should skip asserting for clamped points.
        # However, even clamped points in my current logic should maintain q2+q3+q4=-90
        # unless they hit servo limits.
        if all(0 < j < 180 for j in joints[1:4]):
             assert abs(sum_angles + 90) < 1.0
        else:
             print(f"  Point {pt} hit servo limits: {joints}")
    print("IK Vertical Constraint Passed\n")

def test_path_planning():
    print("--- Testing Path Planning (Trapezoidal Velocity) ---")
    planner = PathPlanner(max_v=50, max_a=100, rate=50)
    start = (0, 0, 0)
    end = (100, 0, 0)

    waypoints = planner.plan_linear_path(start, end)
    print(f"Path (0,0,0) to (100,0,0) generated {len(waypoints)} waypoints")

    assert len(waypoints) > 2
    assert waypoints[0] == start
    # Final point might have small float error if not clamped,
    # but my implementation clamps it.
    assert math.isclose(waypoints[-1][0], 100, abs_tol=0.1)

    # Check for straight line
    for wp in waypoints:
        assert abs(wp[1]) < 0.001
        assert abs(wp[2]) < 0.001
    print("Path Planning Passed\n")

def test_controller_motion():
    print("--- Testing Controller Motion (Pixels to Joint Paths) ---")
    controller = WritingArmController()

    # Move to pixel (250, 250) with pen down
    # This should include a vertical "soft landing" and a horizontal move
    paths = controller.move_to_pixel(250, 250, pen_down=True)

    print(f"Generated {len(paths)} joint configurations for move to (250, 250) pen down")
    assert len(paths) > 0
    for cfg in paths:
        assert len(cfg) == 6 # j1, j2, j3, j4, j5, pen
        for j in cfg[:5]:
            assert 0 <= j <= 180
        assert cfg[5] in [0, 1]

    # Last config should be pen down (1)
    assert paths[-1][5] == 1
    print("Controller Motion Passed\n")

if __name__ == "__main__":
    test_coordinate_mapping()
    test_ik_vertical_constraint()
    test_path_planning()
    test_controller_motion()
