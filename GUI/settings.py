# ================================================================
#  settings.py
#  All measurements and colors taken directly from the design image.
# ================================================================

# --- Window (matches the design image proportions) ---
WINDOW_WIDTH  = 1200
WINDOW_HEIGHT = 620

# --- Canvas (white drawing area — top left) ---
# In the image the canvas starts near top-left with a margin,
# is very wide, and stops above the bottom buttons.
CANVAS_X      = 40
CANVAS_Y      = 30
CANVAS_WIDTH  = 590
CANVAS_HEIGHT = 400

# --- Right Panel — 3x3 offset button grid ---
# Visually centered in the right half of the screen
PANEL_X = 720    # left edge of the 3-column grid
PANEL_Y = 100    # top of the +X +Y +Z row

# Each orange pill button size
BTN_W   = 120
BTN_H   = 55
BTN_GAP = 20     # gap between buttons in the grid

# Value display row (0.0mm boxes) — sits between +row and -row
VAL_W   = 120
VAL_H   = 45

# --- Bottom row of circle buttons ---
# They sit below the canvas, horizontally spread on the left side
BOTTOM_CY = 530   # vertical center of all 4 circles
CIRCLE_R  = 52    # radius of each circle

# Horizontal centers of the 4 circles
CX_START  = 150
CX_CLEAR  = 290
CX_PEN    = 415
CX_ERASER = 540

# --- BOBOT text position (bottom right) ---
BOBOT_X   = 740
BOBOT_Y   = 480

# ---------------------------------------------------------------
#  COLORS  (sampled directly from the design image)
# ---------------------------------------------------------------

# Background — medium gray
BG_COLOR      = (155, 155, 155)

WHITE         = (255, 255, 255)
BLACK         = (0,   0,   0  )

# Canvas border — very dark gray, almost black
CANVAS_BORDER = (30,  30,  30 )

# Orange pill buttons (fill and border)
ORANGE_FILL   = (240, 155, 50 )   # bright orange fill
ORANGE_BORDER = (210, 110, 20 )   # darker orange outline
ORANGE_TEXT   = (200, 70,  10 )   # dark burnt-orange text

# Value display boxes
VAL_FILL      = (255, 255, 255)   # white fill
VAL_BORDER    = (30,  30,  30 )   # almost black border
VAL_TEXT      = (20,  20,  20 )   # near-black text

# START button — bright green fill, green border, green text
GREEN_FILL    = (80,  210, 80 )
GREEN_BORDER  = (30,  170, 30 )
GREEN_TEXT    = (10,  120, 10 )

# CLEAR button — bright red fill, dark red border, red text
RED_FILL      = (230, 60,  60 )
RED_BORDER    = (170, 20,  20 )
RED_TEXT      = (255, 255, 255)

# PEN / ERASER circle — light blue fill, dark blue border
BLUE_FILL     = (185, 210, 245)
BLUE_BORDER   = (50,  80,  185)

# BOBOT pixel font colors
BOBOT_FILL    = (70,  70,  70 )   # dark gray blocks
BOBOT_OUTLINE = (130, 130, 130)   # lighter outline on blocks

# Status bar text
STATUS_TEXT   = (50,  50,  50 )

# ---------------------------------------------------------------
#  BRUSH
# ---------------------------------------------------------------
BRUSH_SIZE    = 3
ERASER_SIZE   = 20

# ---------------------------------------------------------------
#  ROBOT
# ---------------------------------------------------------------
ROBOT_RANGE_MM = 200.0
