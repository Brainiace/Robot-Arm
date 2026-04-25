from kinematics import FABRIK
import math

def test_kinematics():
    fabrik = FABRIK()

    test_cases = [
        {"target": (100, 0, 0), "pen": True, "label": "Reachable point on X-axis"},
        {"target": (0, 100, 0), "pen": False, "label": "Reachable point on Y-axis"},
        {"target": (300, 0, 0), "pen": True, "label": "Far point (Maximum reach test)"},
        {"target": (0, 0, 0), "pen": False, "label": "Origin (Minimum reach test)"},
        {"target": (50, 50, 20), "pen": True, "label": "Point with height (Z > 0)"}
    ]

    for case in test_cases:
        x, y, z = case["target"]
        pen = case["pen"]
        joints = fabrik.solve(x, y, z, pen_down=pen)
        serial_out = fabrik.format_output(joints)

        print(f"--- {case['label']} ---")
        print(f"Input: Target=({x}, {y}, {z}), Pen={pen}")
        print(f"Output Joints: {joints}")
        print(f"Serial String: {serial_out.strip()}")

        # Basic validation
        assert len(joints) == 5, "Should return 5 values"
        for j in joints[:4]:
            assert 0 <= j <= 180, f"Joint angle {j} out of range (0-180)"
        assert joints[4] in [0, 1], "Pen value should be 0 or 1"

        # Verify Link 4 constraint indirectly:
        # Since theta_l4 is fixed to -90, j4 = 180 + (-90 - theta_l3) = 90 - theta_l3.
        # This is already handled in the solve method, but we can check the math.
        # However, testing the actual end-effector position would require forward kinematics.

        print("Test Passed\n")

def test_forward_kinematics_check():
    """
    Optional: Check if the calculated angles actually reach the target (approximately).
    Forward Kinematics for this specific setup (in 2D r-z plane).
    """
    fabrik = FABRIK()
    # Test a point that should be reachable
    tx, ty, tz = 100, 0, 0
    j1, j2, j3, j4, pen = fabrik.solve(tx, ty, tz)

    # Map back from servo angles to link angles
    # j1 = 90 + base_angle => base_angle = j1 - 90
    # j2 = 90 + theta_l2 => theta_l2 = j2 - 90
    # j3 = 180 + (theta_l3 - theta_l2) => theta_l3 = j3 - 180 + theta_l2
    # j4 = 180 + (theta_l4 - theta_l3) => theta_l4 = j4 - 180 + theta_l3

    theta_base = math.radians(j1 - 90)
    theta_l2 = math.radians(j2 - 90)
    theta_l3 = math.radians(j3 - 180 + (j2 - 90))
    theta_l4 = math.radians(j4 - 180 + (j3 - 180 + (j2 - 90)))

    # Calculate positions
    # Shoulder is at (0, 0, L1)
    x0, y0, z0 = 0, 0, fabrik.L1

    # Elbow 1
    r1 = fabrik.L2 * math.cos(theta_l2)
    x1 = r1 * math.cos(theta_base)
    y1 = r1 * math.sin(theta_base)
    z1 = z0 + fabrik.L2 * math.sin(theta_l2)

    # Elbow 2 (Wrist)
    r2 = r1 + fabrik.L3 * math.cos(theta_l3)
    x2 = r2 * math.cos(theta_base)
    y2 = r2 * math.sin(theta_base)
    z2 = z1 + fabrik.L3 * math.sin(theta_l3)

    # Pen Tip
    r3 = r2 + fabrik.L4 * math.cos(theta_l4)
    x3 = r3 * math.cos(theta_base)
    y3 = r3 * math.sin(theta_base)
    z3 = z2 + fabrik.L4 * math.sin(theta_l4)

    print(f"--- Forward Kinematics Verification for ({tx}, {ty}, {tz}) ---")
    print(f"Calculated End Effector: ({x3:.2f}, {y3:.2f}, {z3:.2f})")

    error = math.sqrt((tx-x3)**2 + (ty-y3)**2 + (tz-z3)**2)
    print(f"Error: {error:.4f} mm")

    # Link 4 vertical check
    # theta_l4 should be -90 degrees (-pi/2 radians)
    print(f"Link 4 angle: {math.degrees(theta_l4):.2f} degrees (Target: -90.00)")

    assert error < 2.0, "FK error too high (clamping/rounding might cause small errors)"
    assert abs(math.degrees(theta_l4) + 90) < 1.0, "Link 4 is not vertical"

if __name__ == "__main__":
    test_kinematics()
    test_forward_kinematics_check()
