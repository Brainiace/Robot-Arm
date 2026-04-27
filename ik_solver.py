import math
import config

class IKSolver:
    """
    Inverse Kinematics solver using DH-parameters for a 5-DOF setup.
    DH Table:
    | Link | alpha(i-1) | a(i-1) | d(i) | theta(i) |
    |------|------------|--------|------|----------|
    | 1    | 0          | 0      | L1   | q1       |
    | 2    | 90         | 0      | 0    | q2       |
    | 3    | 0          | L2     | 0    | q3       |
    | 4    | 0          | L3     | 0    | q4       |
    | 5    | 90         | 0      | L4   | q5       |
    """
    def __init__(self):
        self.L1 = config.LINK_1
        self.L2 = config.LINK_2
        self.L3 = config.LINK_3
        self.L4 = config.LINK_4

    def solve(self, x, y, z):
        """
        Calculates joint angles q1-q5.
        Constraint: Link 4 (and L5) remains vertical.
        """
        # q1: Base rotation
        q1 = math.atan2(y, x)

        # In the plane (r, z), we have a 3-link arm (L2, L3, L4)
        # But we want L4 to be vertical.
        # Wrist position (end of L3) must be at:
        r_target = math.sqrt(x**2 + y**2)
        z_wrist = z + self.L4

        # Relative to shoulder at (0, L1)
        r_rel = r_target
        z_rel = z_wrist - self.L1

        dist_sq = r_rel**2 + z_rel**2
        dist = math.sqrt(dist_sq)

        # Reachability check
        if dist > (self.L2 + self.L3):
            scale = (self.L2 + self.L3) / dist
            r_rel *= scale
            z_rel *= scale
            dist = self.L2 + self.L3
            dist_sq = dist**2
        elif dist < abs(self.L2 - self.L3):
            if dist == 0: r_rel = 0.0001
            scale = abs(self.L2 - self.L3) / dist
            r_rel *= scale
            z_rel *= scale
            dist = abs(self.L2 - self.L3)
            dist_sq = dist**2

        # Solve 2-link planar IK for q2, q3
        cos_q3 = (dist_sq - self.L2**2 - self.L3**2) / (2 * self.L2 * self.L3)
        cos_q3 = max(-1, min(1, cos_q3))
        q3 = -math.acos(cos_q3) # Elbow up

        q2 = math.atan2(z_rel, r_rel) - math.atan2(self.L3 * math.sin(q3), self.L2 + self.L3 * math.cos(q3))

        # q4: Wrist Pitch to keep L4 vertical.
        # Angles relative to horizontal: q2 + q3 + q4 = -90 degrees
        q4 = -math.pi/2 - q2 - q3

        # q5: Wrist Roll, kept at 0 for standard writing
        q5 = 0.0

        # Map to servo angles (0-180) and clamp
        s1 = max(0, min(180, 90 + math.degrees(q1)))
        s2 = max(0, min(180, 90 + math.degrees(q2)))
        s3 = max(0, min(180, 180 + math.degrees(q3)))
        s4 = max(0, min(180, 180 + math.degrees(q4)))
        s5 = max(0, min(180, 90 + math.degrees(q5)))

        return [s1, s2, s3, s4, s5]
