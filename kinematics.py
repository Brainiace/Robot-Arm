import config
from ik_solver import IKSolver
from path_planner import PathPlanner
from coordinate_mapping import CoordinateMapper

class WritingArmController:
    def __init__(self):
        self.ik_solver = IKSolver()
        self.path_planner = PathPlanner()
        self.mapper = CoordinateMapper()
        self.current_pos_mm = (0.0, 0.0, config.Z_HOVER)
        self.pen_down = False

    def move_to_pixel(self, px_x, px_y, pen_down=False):
        """
        Moves the arm to a pixel coordinate.
        Calculates the path and returns a list of joint configurations.
        """
        target_z = config.Z_WRITE if pen_down else config.Z_HOVER
        target_mm = self.mapper.screen_to_physical(px_x, px_y, target_z)

        # If pen state changes, perform soft landing/lift first
        path_configs = []

        if pen_down != self.pen_down:
            # Vertical movement
            lift_path = self.path_planner.soft_landing(
                self.current_pos_mm[0], self.current_pos_mm[1],
                self.current_pos_mm[2], target_z
            )
            for wp in lift_path:
                path_configs.append(self.ik_solver.solve(*wp) + [1 if pen_down else 0])
            self.current_pos_mm = (self.current_pos_mm[0], self.current_pos_mm[1], target_z)
            self.pen_down = pen_down

        # Horizontal (or 3D) movement to target
        move_path = self.path_planner.plan_linear_path(self.current_pos_mm, target_mm)
        for wp in move_path:
            path_configs.append(self.ik_solver.solve(*wp) + [1 if pen_down else 0])

        self.current_pos_mm = target_mm
        return path_configs

    def format_output(self, joints):
        """Formats the joint angles for serial communication: j1,j2,j3,j4,j5,pen\n"""
        return ",".join(map(str, joints)) + "\n"

# For backward compatibility or simpler usage
class FABRIK:
    """Legacy wrapper for the new High-Precision Controller."""
    def __init__(self):
        self.controller = WritingArmController()

    def solve(self, x, y, z, pen_down=False):
        # Note: This returns a single configuration, not a path.
        # It's intended for direct IK calls.
        joints = self.controller.ik_solver.solve(x, y, z)
        return tuple(joints + [1 if pen_down else 0])

    def format_output(self, joints):
        return self.controller.format_output(joints)
