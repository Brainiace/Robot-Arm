import math

class FABRIK:
    def __init__(self):
        """
        Initializes the FABRIK solver with link lengths from Agents.md.
        - Link 1 (Shoulder): 120mm (treated as vertical offset from base to shoulder joint)
        - Link 2 (Elbow 1): 100mm
        - Link 3 (Elbow 2): 80mm
        - Link 4 (Wrist/Pen holder): 40mm
        """
        self.L1 = 120.0  # Base height to Shoulder Joint
        self.L2 = 100.0  # Shoulder to Elbow 1
        self.L3 = 80.0   # Elbow 1 to Elbow 2 (Wrist Joint)
        self.L4 = 40.0   # Wrist Joint to Pen Tip

        self.tolerance = 0.1
        self.max_iterations = 100

    def solve(self, target_x, target_y, target_z, pen_down=False):
        """
        Calculate joint angles for target (x, y, z) using FABRIK.
        Constraint: Link 4 must remain vertical (perpendicular to the surface).

        Args:
            target_x (float): Target X coordinate in mm.
            target_y (float): Target Y coordinate in mm.
            target_z (float): Target Z coordinate (height) in mm.
            pen_down (bool): Whether the pen is in the 'down' position.

        Returns:
            tuple: (j1, j2, j3, j4, pen) as integers (0-180 for servos).
        """
        # 1. Base rotation (Joint 1)
        # j1 = 90 is centered along the X-axis.
        j1_angle = math.degrees(math.atan2(target_y, target_x))
        out_j1 = 90 + j1_angle

        # 2. Reduce to 2D problem in the (r, z) plane
        # r is the horizontal distance from the base.
        r_target = math.sqrt(target_x**2 + target_y**2)
        z_target = target_z

        # Constraint: Link 4 must be vertical.
        # This means the Wrist Joint (Joint 4) must be directly above the pen tip.
        # Position of Joint 4 in (r, z) plane:
        r_j4 = r_target
        z_j4 = z_target + self.L4

        # Fixed point: Shoulder Joint (Joint 2) is at (0, L1) in (r, z) plane.
        p0 = [0.0, self.L1]
        p2_target = [r_j4, z_j4]

        # Check reachability for the 2-link chain (L2, L3) between Shoulder and Wrist
        dist = math.sqrt((p2_target[0] - p0[0])**2 + (p2_target[1] - p0[1])**2)

        if dist > (self.L2 + self.L3):
            # Target is unreachable (too far) - stretch towards it
            scale = (self.L2 + self.L3) / dist
            p2_target[0] = p0[0] + (p2_target[0] - p0[0]) * scale
            p2_target[1] = p0[1] + (p2_target[1] - p0[1]) * scale
        elif dist < abs(self.L2 - self.L3):
            # Target is unreachable (too close) - move to minimum reach
            if dist == 0:
                p2_target = [0.1, p0[1]]
            else:
                scale = abs(self.L2 - self.L3) / dist
                p2_target[0] = p0[0] + (p2_target[0] - p0[0]) * scale
                p2_target[1] = p0[1] + (p2_target[1] - p0[1]) * scale

        # FABRIK iteration for Joint 3 (p1)
        # Chain: Shoulder (p0) -> Elbow 1 (p1) -> Wrist (p2)
        # Initialize p1 (Elbow 1) with a guess
        p1 = [p2_target[0] / 2, (p0[1] + p2_target[1]) / 2 + 20]
        p2 = [p2_target[0], p2_target[1]]

        for _ in range(self.max_iterations):
            # Backward reach: Wrist is at target
            p2_b = p2_target
            p1_b = self._move_towards(p2_b, p1, self.L3)

            # Forward reach: Shoulder is fixed
            p0_f = p0
            p1_f = self._move_towards(p0_f, p1_b, self.L2)
            p2_f = self._move_towards(p1_f, p2_b, self.L3)

            # Check convergence
            error = math.sqrt((p2_f[0] - p2_target[0])**2 + (p2_f[1] - p2_target[1])**2)
            p1, p2 = p1_f, p2_f
            if error < self.tolerance:
                break

        # 3. Calculate Joint Angles from Positions
        # theta_l2: Angle of Link 2 relative to horizontal
        theta_l2 = math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0]))
        # theta_l3: Angle of Link 3 relative to horizontal
        theta_l3 = math.degrees(math.atan2(p2[1] - p1[1], p2[0] - p1[0]))
        # theta_l4: Angle of Link 4 relative to horizontal (must be -90 for vertical down)
        theta_l4 = -90.0

        # Convert to servo values (0-180 degrees)
        # Joint 2 (Shoulder): 90 is horizontal, 180 is vertical up, 0 is vertical down
        out_j2 = 90 + theta_l2
        # Joint 3 (Elbow 1): 180 is straight, 90 is a 90-degree bend
        out_j3 = 180 + (theta_l3 - theta_l2)
        # Joint 4 (Elbow 2): 180 is straight, 90 is a 90-degree bend
        out_j4 = 180 + (theta_l4 - theta_l3)

        # Pen servo: 0 for UP, 1 for DOWN (or as required by Arduino logic)
        pen_val = 1 if pen_down else 0

        # Clamp values to 0-180 range
        joints = [
            max(0, min(180, round(out_j1))),
            max(0, min(180, round(out_j2))),
            max(0, min(180, round(out_j3))),
            max(0, min(180, round(out_j4))),
            pen_val
        ]

        return tuple(joints)

    def _move_towards(self, p_fixed, p_moving, length):
        """Helper to move p_moving towards p_fixed at a specified distance."""
        dx = p_moving[0] - p_fixed[0]
        dy = p_moving[1] - p_fixed[1]
        dist = math.sqrt(dx**2 + dy**2)
        if dist == 0:
            return [p_fixed[0] + length, p_fixed[1]]
        return [p_fixed[0] + dx * length / dist, p_fixed[1] + dy * length / dist]

    def format_output(self, joints):
        """Formats the joint angles for serial communication."""
        return f"{joints[0]},{joints[1]},{joints[2]},{joints[3]},{joints[4]}\n"

if __name__ == "__main__":
    fabrik = FABRIK()
    # Example: Reach to (100, 0, 0)
    res = fabrik.solve(100, 0, 0, pen_down=True)
    print(f"Target (100, 0, 0) -> Joints: {res}")
    print(f"Serial: {fabrik.format_output(res)}")
