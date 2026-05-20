from PIL import Image, ImageDraw, ImageFont
import math

W, H = 640, 400
BG = (30, 30, 50)

# Bojack's color palette
HORSE_BROWN = (139, 90, 43)
HORSE_DARK  = (100, 60, 20)
MANE_YELLOW = (220, 180, 50)
SKIN        = (230, 190, 140)
SHIRT_BLUE  = (70, 110, 180)
JEAN_BLUE   = (60, 80, 140)
WHITE       = (255, 255, 255)
BLACK       = (10, 10, 10)
BUBBLE_CLR  = (255, 252, 240)
EYE_WHITE   = (240, 240, 240)
EYE_DARK    = (40, 20, 10)
NOSE_CLR    = (110, 65, 25)
MOUTH_CLR   = (80, 40, 10)

LINES = [
    "It gets easier.",
    "Every day it gets a little easier.",
    "But you gotta do it every day.",
    "That's the hard part.",
    "But it does get easier.",
]

def draw_frame(draw, tick, line_idx):
    # Sky / background gradient suggestion
    draw.rectangle([0, 0, W, H], fill=BG)
    # Floor
    draw.rectangle([0, 300, W, H], fill=(20, 20, 35))

    # ---- Body ----
    bx, by = 200, 220   # anchor: center-bottom of torso

    # Legs (two visible)
    leg_swing = int(8 * math.sin(tick * 0.18))
    draw.rectangle([bx - 28, by, bx - 12, by + 70], fill=JEAN_BLUE)
    draw.rectangle([bx + 12, by, bx + 28, by + 70 + leg_swing], fill=JEAN_BLUE)
    # Hooves
    draw.ellipse([bx - 32, by + 65, bx - 8, by + 78], fill=HORSE_DARK)
    draw.ellipse([bx + 8,  by + 68 + leg_swing, bx + 32, by + 81 + leg_swing], fill=HORSE_DARK)

    # Torso
    draw.rounded_rectangle([bx - 45, by - 80, bx + 45, by + 5], radius=20, fill=SHIRT_BLUE)

    # Tail (behind body)
    tail_wag = int(6 * math.sin(tick * 0.25))
    for i in range(12):
        ox = bx - 45 - i * 4
        oy = by - 40 + tail_wag + i * 3
        draw.ellipse([ox - 5, oy - 5, ox + 5, oy + 5], fill=MANE_YELLOW)

    # Arms
    arm_swing = int(10 * math.sin(tick * 0.18 + math.pi))
    # Left arm
    draw.rounded_rectangle([bx - 65, by - 70 + arm_swing, bx - 40, by - 25 + arm_swing], radius=10, fill=HORSE_BROWN)
    # Right arm
    draw.rounded_rectangle([bx + 40, by - 70 - arm_swing, bx + 65, by - 25 - arm_swing], radius=10, fill=HORSE_BROWN)
    # Hands
    draw.ellipse([bx - 70, by - 30 + arm_swing, bx - 38, by - 15 + arm_swing], fill=HORSE_BROWN)
    draw.ellipse([bx + 38, by - 30 - arm_swing, bx + 70, by - 15 - arm_swing], fill=HORSE_BROWN)

    # ---- Horse head / neck ----
    nx = bx + 10
    ny = by - 80
    # Neck
    draw.rounded_rectangle([nx - 18, ny - 30, nx + 18, ny + 10], radius=12, fill=HORSE_BROWN)
    # Head (elongated horse snout)
    hx, hy = nx, ny - 60
    draw.ellipse([hx - 35, hy - 30, hx + 35, hy + 30], fill=HORSE_BROWN)
    # Snout
    draw.ellipse([hx + 10, hy - 10, hx + 55, hy + 20], fill=HORSE_BROWN)
    # Nostrils
    draw.ellipse([hx + 30, hy + 5, hx + 40, hy + 14], fill=NOSE_CLR)
    draw.ellipse([hx + 20, hy + 5, hx + 30, hy + 14], fill=NOSE_CLR)
    # Mouth (talking animation)
    mouth_open = int(6 * abs(math.sin(tick * 0.4))) if line_idx >= 0 else 0
    draw.ellipse([hx + 15, hy + 12, hx + 45, hy + 22 + mouth_open], fill=MOUTH_CLR)
    if mouth_open > 2:
        draw.ellipse([hx + 18, hy + 14, hx + 42, hy + 20 + mouth_open], fill=(180, 60, 60))
    # Eye
    draw.ellipse([hx - 20, hy - 15, hx - 2, hy + 2], fill=EYE_WHITE)
    # pupil slight drift
    pupil_dx = int(2 * math.sin(tick * 0.07))
    draw.ellipse([hx - 16 + pupil_dx, hy - 11, hx - 6 + pupil_dx, hy - 2], fill=EYE_DARK)
    # Eyebrow (sad/pensive)
    draw.line([hx - 22, hy - 22, hx - 2, hy - 18], fill=HORSE_DARK, width=3)
    # Mane
    for i in range(8):
        mx = hx - 30 + i * 2
        my = hy - 28 - i * 4
        draw.ellipse([mx - 8, my - 8, mx + 8, my + 8], fill=MANE_YELLOW)
    # Ear
    draw.polygon([(hx - 15, hy - 28), (hx - 25, hy - 50), (hx - 5, hy - 45)], fill=HORSE_BROWN)

    # ---- Speech bubble ----
    if line_idx >= 0:
        text = LINES[line_idx]
        bub_x1, bub_y1 = 300, 50
        bub_x2, bub_y2 = 620, 130
        # Bubble
        draw.rounded_rectangle([bub_x1, bub_y1, bub_x2, bub_y2], radius=18,
                                fill=BUBBLE_CLR, outline=BLACK, width=2)
        # Tail pointing toward Bojack's head
        tail_pts = [(bub_x1 + 30, bub_y2), (bub_x1 + 10, bub_y2 + 30), (bub_x1 + 60, bub_y2)]
        draw.polygon(tail_pts, fill=BUBBLE_CLR)
        draw.line([(bub_x1 + 10, bub_y2 + 30), (bub_x1 + 30, bub_y2)], fill=BLACK, width=2)
        draw.line([(bub_x1 + 10, bub_y2 + 30), (bub_x1 + 60, bub_y2)], fill=BLACK, width=2)

        # Text — wrap manually
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
        except Exception:
            font = ImageFont.load_default()

        # Wrap text to fit bubble
        words = text.split()
        lines_wrapped = []
        cur = ""
        for w in words:
            test = (cur + " " + w).strip()
            bbox = draw.textbbox((0, 0), test, font=font)
            if bbox[2] - bbox[0] > (bub_x2 - bub_x1 - 20):
                if cur:
                    lines_wrapped.append(cur)
                cur = w
            else:
                cur = test
        if cur:
            lines_wrapped.append(cur)

        ty = bub_y1 + 15
        for ln in lines_wrapped:
            draw.text((bub_x1 + 15, ty), ln, fill=BLACK, font=font)
            bbox = draw.textbbox((0, 0), ln, font=font)
            ty += (bbox[3] - bbox[1]) + 6

    # ---- Show name label ----
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except Exception:
        title_font = ImageFont.load_default()
    draw.text((10, H - 25), "BoJack Horseman", fill=(150, 150, 180), font=title_font)


FPS = 12
# seconds per line
SPL = 3
TOTAL_LINES = len(LINES)
INTRO_FRAMES = FPS * 1       # 1 second of just Bojack
FRAMES_PER_LINE = FPS * SPL
OUTRO_FRAMES = FPS * 1

all_frames = []

# intro
for t in range(INTRO_FRAMES):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    draw_frame(d, t, -1)
    all_frames.append(img)

# dialogue
tick = INTRO_FRAMES
for li, line in enumerate(LINES):
    for f in range(FRAMES_PER_LINE):
        img = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(img)
        draw_frame(d, tick, li)
        all_frames.append(img)
        tick += 1

# outro
for t in range(OUTRO_FRAMES):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    draw_frame(d, tick, -1)
    all_frames.append(img)
    tick += 1

out_path = "/home/user/ai-text-detector/bojack.gif"
all_frames[0].save(
    out_path,
    save_all=True,
    append_images=all_frames[1:],
    loop=0,
    duration=int(1000 / FPS),
    optimize=False,
)
print(f"Saved {len(all_frames)} frames -> {out_path}")
