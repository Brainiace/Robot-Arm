import math
import config

class PathPlanner:
    def __init__(self, max_v=config.MAX_VELOCITY, max_a=config.MAX_ACCELERATION, rate=config.SAMPLE_RATE):
        self.max_v = max_v
        self.max_a = max_a
        self.rate = rate

    def plan_linear_path(self, start_pos, end_pos):
        """
        Generates a list of (x, y, z) waypoints between start and end.
        Uses trapezoidal velocity profiling.
        start_pos, end_pos: (x, y, z) in mm.
        """
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        dz = end_pos[2] - start_pos[2]

        distance = math.sqrt(dx**2 + dy**2 + dz**2)
        if distance == 0:
            return [start_pos]

        # Check if we can reach max_v
        d_to_reach_v = (self.max_v**2) / (2 * self.max_a)

        if distance >= 2 * d_to_reach_v:
            # Trapezoidal
            v_peak = self.max_v
            t_accel = self.max_v / self.max_a
            s_accel = d_to_reach_v
            s_cruise = distance - 2 * s_accel
            t_cruise = s_cruise / self.max_v
        else:
            # Triangular
            s_accel = distance / 2
            v_peak = math.sqrt(2 * self.max_a * s_accel)
            t_accel = v_peak / self.max_a
            s_cruise = 0
            t_cruise = 0

        t_total = 2 * t_accel + t_cruise
        num_steps = max(2, int(t_total * self.rate))
        waypoints = []

        for i in range(num_steps):
            t = (i / (num_steps - 1)) * t_total

            if t <= t_accel:
                s = 0.5 * self.max_a * t**2
            elif t <= (t_accel + t_cruise):
                s = s_accel + v_peak * (t - t_accel)
            else:
                t_dec = t - (t_accel + t_cruise)
                s = s_accel + s_cruise + v_peak * t_dec - 0.5 * self.max_a * t_dec**2

            # Clamp s to distance to handle floating point errors
            s = max(0, min(s, distance))

            ratio = s / distance
            curr_x = start_pos[0] + dx * ratio
            curr_y = start_pos[1] + dy * ratio
            curr_z = start_pos[2] + dz * ratio
            waypoints.append((curr_x, curr_y, curr_z))

        return waypoints

    def soft_landing(self, x, y, start_z, end_z):
        """Generates waypoints for vertical pen movement."""
        return self.plan_linear_path((x, y, start_z), (x, y, end_z))
