# Physical parameters (mm)
LINK_1 = 120.0  # Base height to Shoulder
LINK_2 = 100.0  # Shoulder to Elbow
LINK_3 = 80.0   # Elbow to Wrist
LINK_4 = 40.0   # Wrist to Pen Tip

ROBOT_REACH = LINK_2 + LINK_3 # 180.0 mm

# Z-axis heights (mm)
Z_HOVER = 20.0
Z_WRITE = 0.0

# Motion parameters
MAX_VELOCITY = 50.0      # mm/s
MAX_ACCELERATION = 100.0 # mm/s^2
SAMPLE_RATE = 50.0       # Hz (waypoints per second)

# Workspace settings (Unified with GUI/settings.py)
CANVAS_WIDTH = 590
CANVAS_HEIGHT = 400

# Default mapping (before calibration)
# We want the robot (0,0) to be at the bottom-center of the canvas
DEFAULT_SCALE = 0.5 # mm/pixel
ORIGIN_PX_X = 295.0 # Center of 590
ORIGIN_PX_Y = 400.0 # Bottom of 400
