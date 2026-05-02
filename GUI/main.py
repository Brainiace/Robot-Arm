# ================================================================
#  main.py  ←  RUN THIS FILE:  py main.py
#
#  Layout matches the design image exactly:
#
#   ┌──────────────────────────┬──────────────────────────────────┐
#   │                          │    [+X]    [+Y]    [+Z]          │
#   │   WHITE CANVAS           │   [0.0mm][0.0mm][0.0mm]          │
#   │                          │    [-X]    [-Y]    [-Z]          │
#   │                          │                                  │
#   ├──────────────────────────┤                                  │
#   │ (START)(CLEAR)(✏️)(eraser)│              BOBOT              │
#   └──────────────────────────┴──────────────────────────────────┘
#
#  Keyboard shortcuts:
#    S = save drawing to drawing.csv
#    Q = quit
# ================================================================

import pygame

# Our own modules
from settings import *
from buttons  import CircleButton, PillButton, ValueBox
from canvas   import Canvas
from saver    import save_to_csv


# ----------------------------------------------------------------
#  START PYGAME
# ----------------------------------------------------------------

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("BOBOT - Robot Drawing Controller")
clock = pygame.time.Clock()


# ----------------------------------------------------------------
#  EMOJI ICONS for the pen and eraser circle buttons
#  We render emoji characters using a font that supports them.
# ----------------------------------------------------------------

try:
    emoji_font = pygame.font.SysFont("segoe ui emoji", 38)
except:
    emoji_font = pygame.font.SysFont(None, 38)

icon_pencil = emoji_font.render("✏️", True, BLACK)
icon_eraser = emoji_font.render("🧹", True, BLACK)


# ----------------------------------------------------------------
#  CANVAS
# ----------------------------------------------------------------

canvas = Canvas()


# ----------------------------------------------------------------
#  BUTTONS — laid out to match the design image exactly
# ----------------------------------------------------------------

# ── Bottom circle buttons ──────────────────────────────────────
#  Green START, Red CLEAR, Blue+pencil, Blue+eraser
#  All same radius, evenly spaced on the left side

btn_start  = CircleButton(CX_START,  BOTTOM_CY, CIRCLE_R,
                          GREEN_FILL, GREEN_BORDER, "START", GREEN_TEXT, 17)

btn_clear  = CircleButton(CX_CLEAR,  BOTTOM_CY, CIRCLE_R,
                          RED_FILL,   RED_BORDER,   "CLEAR", RED_TEXT,   17)

btn_pen    = CircleButton(CX_PEN,    BOTTOM_CY, CIRCLE_R,
                          BLUE_FILL,  BLUE_BORDER,  "")

btn_eraser = CircleButton(CX_ERASER, BOTTOM_CY, CIRCLE_R,
                          BLUE_FILL,  BLUE_BORDER,  "")


# ── Right panel — 3×3 grid of offset controls ──────────────────
#
#  Row 1:  [+X]       [+Y]       [+Z]
#  Row 2:  [0.0mm]    [0.0mm]    [0.0mm]
#  Row 3:  [-X]       [-Y]       [-Z]
#
#  Column positions (left edges of each button)

COL1 = PANEL_X
COL2 = PANEL_X + BTN_W + BTN_GAP
COL3 = PANEL_X + (BTN_W + BTN_GAP) * 2

ROW_PLUS  = PANEL_Y                            # +X +Y +Z row
ROW_VAL   = PANEL_Y + BTN_H + BTN_GAP         # value display row
ROW_MINUS = PANEL_Y + BTN_H + BTN_GAP + VAL_H + BTN_GAP  # -X -Y -Z row

# +X  +Y  +Z
btn_plus_x = PillButton(COL1, ROW_PLUS, BTN_W, BTN_H,
                        "+X", ORANGE_FILL, ORANGE_BORDER, ORANGE_TEXT)
btn_plus_y = PillButton(COL2, ROW_PLUS, BTN_W, BTN_H,
                        "+Y", ORANGE_FILL, ORANGE_BORDER, ORANGE_TEXT)
btn_plus_z = PillButton(COL3, ROW_PLUS, BTN_W, BTN_H,
                        "+Z", ORANGE_FILL, ORANGE_BORDER, ORANGE_TEXT)

# Value display boxes (not clickable)
box_x = ValueBox(COL1, ROW_VAL, VAL_W, VAL_H)
box_y = ValueBox(COL2, ROW_VAL, VAL_W, VAL_H)
box_z = ValueBox(COL3, ROW_VAL, VAL_W, VAL_H)

# -X  -Y  -Z
btn_minus_x = PillButton(COL1, ROW_MINUS, BTN_W, BTN_H,
                         "-X", ORANGE_FILL, ORANGE_BORDER, ORANGE_TEXT)
btn_minus_y = PillButton(COL2, ROW_MINUS, BTN_W, BTN_H,
                         "-Y", ORANGE_FILL, ORANGE_BORDER, ORANGE_TEXT)
btn_minus_z = PillButton(COL3, ROW_MINUS, BTN_W, BTN_H,
                         "-Z", ORANGE_FILL, ORANGE_BORDER, ORANGE_TEXT)


# ----------------------------------------------------------------
#  BOBOT PIXEL FONT
#  Draws "BOBOT" using a 5×7 pixel grid for each letter.
#  Each letter is a list of 7 rows, each row has 5 values (1=filled).
# ----------------------------------------------------------------

PIXEL_LETTERS = {
    'B': [
        [1,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,1,1,1,0],
    ],
    'O': [
        [0,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [0,1,1,1,0],
    ],
    'T': [
        [1,1,1,1,1],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
    ],
}

def draw_bobot(surface, x, y, scale=10):
    """
    Draw BOBOT letter by letter using filled rectangles.
    scale = size of each pixel block in screen pixels.
    """
    word    = ['B', 'O', 'B', 'O', 'T']
    spacing = scale + 2   # tiny gap between pixel blocks
    cursor  = x

    for char in word:
        grid = PIXEL_LETTERS[char]
        for row_i, row in enumerate(grid):
            for col_i, on in enumerate(row):
                if on:
                    bx = cursor + col_i * spacing
                    by = y      + row_i * spacing
                    # Main dark block
                    pygame.draw.rect(surface, BOBOT_FILL,
                                     (bx, by, scale, scale))
                    # Light border gives the chunky 3-D look
                    pygame.draw.rect(surface, BOBOT_OUTLINE,
                                     (bx, by, scale, scale), 2)
        # Move cursor right: 5 columns × spacing + gap between letters
        cursor += 5 * spacing + scale


# ----------------------------------------------------------------
#  APP STATE
# ----------------------------------------------------------------

offset_x = 0.0
offset_y = 0.0
offset_z = 0.0

message       = ""
message_timer = 0

font_msg    = pygame.font.SysFont("consolas", 17, bold=True)
font_status = pygame.font.SysFont("consolas", 13)


# ================================================================
#  MAIN LOOP
# ================================================================

running = True

while running:

    # ── Collect all events once per frame ──────────────────────
    events = pygame.event.get()

    # ── Global events ───────────────────────────────────────────
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            if event.key == pygame.K_s:
                message = save_to_csv(canvas.get_points(), offset_x, offset_y)
                message_timer = 130

    # ── Bottom circle button clicks ─────────────────────────────

    if btn_start.was_clicked(events):
        message = "Robot started!"
        message_timer = 130
        print("START pressed — trigger robot here!")

    if btn_clear.was_clicked(events):
        canvas.clear()
        message = "Canvas cleared."
        message_timer = 100

    if btn_pen.was_clicked(events):
        canvas.set_tool("pen")
        message = "Tool: Pen"
        message_timer = 70

    if btn_eraser.was_clicked(events):
        canvas.set_tool("eraser")
        message = "Tool: Eraser"
        message_timer = 70

    # ── Offset button clicks (each press = ±0.1 mm) ─────────────

    if btn_plus_x.was_clicked(events):  offset_x = round(offset_x + 0.1, 1)
    if btn_minus_x.was_clicked(events): offset_x = round(offset_x - 0.1, 1)
    if btn_plus_y.was_clicked(events):  offset_y = round(offset_y + 0.1, 1)
    if btn_minus_y.was_clicked(events): offset_y = round(offset_y - 0.1, 1)
    if btn_plus_z.was_clicked(events):  offset_z = round(offset_z + 0.1, 1)
    if btn_minus_z.was_clicked(events): offset_z = round(offset_z - 0.1, 1)

    # ── Canvas drawing ──────────────────────────────────────────
    canvas.handle_events(events)


    # ============================================================
    #  DRAW EVERYTHING
    # ============================================================

    # Gray background
    screen.fill(BG_COLOR)

    # White canvas + thick border
    canvas.draw(screen)

    # ── Bottom circle buttons ───────────────────────────────────
    btn_start.draw(screen)
    btn_clear.draw(screen)
    btn_pen.draw(screen,    icon_pencil)
    btn_eraser.draw(screen, icon_eraser)

    # Small dot under the active tool button
    if canvas.tool == "pen":
        pygame.draw.circle(screen, BLACK,
                           (CX_PEN, BOTTOM_CY + CIRCLE_R + 10), 5)
    else:
        pygame.draw.circle(screen, BLACK,
                           (CX_ERASER, BOTTOM_CY + CIRCLE_R + 10), 5)

    # ── Right panel offset grid ─────────────────────────────────
    btn_plus_x.draw(screen)
    btn_plus_y.draw(screen)
    btn_plus_z.draw(screen)

    box_x.draw(screen, offset_x)
    box_y.draw(screen, offset_y)
    box_z.draw(screen, offset_z)

    btn_minus_x.draw(screen)
    btn_minus_y.draw(screen)
    btn_minus_z.draw(screen)

    # ── BOBOT pixel text (bottom right) ────────────────────────
    draw_bobot(screen, BOBOT_X, BOBOT_Y, scale=10)

    # ── Feedback message (briefly shown after actions) ──────────
    if message_timer > 0:
        message_timer -= 1
        surf = font_msg.render(message, True, WHITE)
        # Dark semi-transparent background behind the message
        bg = pygame.Surface((surf.get_width() + 24, surf.get_height() + 12))
        bg.set_alpha(170)
        bg.fill(BLACK)
        mx = CANVAS_X + CANVAS_WIDTH  // 2 - bg.get_width()  // 2
        my = CANVAS_Y + CANVAS_HEIGHT // 2 - bg.get_height() // 2
        screen.blit(bg,   (mx, my))
        screen.blit(surf, (mx + 12, my + 6))

    # ── Status bar at the very bottom ──────────────────────────
    status = (f"Tool: {canvas.tool.upper()}  |  "
              f"Points: {len(canvas.get_points())}  |  "
              f"Strokes: {canvas.stroke_count}  |  "
              f"Offset  X={offset_x:+.1f}  Y={offset_y:+.1f}  Z={offset_z:+.1f} mm  |  "
              f"[S] Save    [Q] Quit")
    s = font_status.render(status, True, STATUS_TEXT)
    screen.blit(s, (CANVAS_X, WINDOW_HEIGHT - 18))

    # ── Flip and tick ───────────────────────────────────────────
    pygame.display.flip()
    clock.tick(60)


# ----------------------------------------------------------------
#  CLEANUP
# ----------------------------------------------------------------
pygame.quit()
print("App closed.")
