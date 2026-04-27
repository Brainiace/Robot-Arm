# Physical parameters (mm)
LINK_1 = 120.0  # Base height to Shoulder
LINK_2 = 100.0  # Shoulder to Elbow
LINK_3 = 80.0   # Elbow to Wrist
LINK_4 = 40.0   # Wrist to Pen Tip

# Z-axis heights (mm)
Z_HOVER = 20.0
Z_WRITE = 0.0

# Motion parameters
MAX_VELOCITY = 50.0      # mm/s
MAX_ACCELERATION = 100.0 # mm/s^2
SAMPLE_RATE = 50.0       # Hz (waypoints per second)

# Workspace settings
SCALE_FACTOR = 1.0
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
# Offset from Pygame (0,0) to Robot (0,0) in mm
# Assuming Pygame (200, 200) is Robot (0,0)
ORIGIN_OFFSET_X = 200.0
ORIGIN_OFFSET_Y = 200.0
