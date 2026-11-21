"""Draw the front page of THE WORLD TODAY for Saturday 21 November 2026.

Deterministic: fixed fonts, fixed coordinates, no randomness, no clock,
no network. Renders a 1024x1024 PNG with Pillow and writes it next to
this file as news_image.png. Run: python3 render.py
"""

import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 36
CW = W - 2 * MARGIN  # content width: 952

PAPER = (247, 242, 231)
INK = (18, 18, 18)
RULE = (120, 110, 95)
MUTED = (90, 84, 72)
RED = (178, 34, 34)
NAVY = (16, 28, 52)
SEA = (46, 92, 128)
GOLD = (212, 160, 44)
TEAL = (32, 110, 110)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF = FONT_DIR + "DejaVuSerif.ttf"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, fill=INK):
    """Draw a wrapped paragraph; return the y below it."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def headline(draw, x, y, text, size, max_w, leading=None):
    """Draw a bold serif headline, wrapped; return the y below it."""
    fnt = font(SERIF_B, size)
    leading = leading or int(size * 1.08)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=INK)
        y += leading
    return y


def kicker(draw, x, y, text, color=RED, width=None):
    """Small-caps section label with a rule beneath; return y below rule."""
    if width is None:
        width = CW
    fnt = font(SANS_B, 15)
    draw.text((x, y), text.upper(), font=fnt, fill=color)
    y += 22
    draw.line([(x, y), (x + width, y)], fill=RULE, width=1)
    return y + 8


def rule(draw, y, width=2):
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=width)
    return y + width


def panel(img, scene, x, y, w, h):
    """Render a scene onto its own layer so nothing spills past its box."""
    layer = Image.new("RGB", (w, h), PAPER)
    d = ImageDraw.Draw(layer)
    scene(d, 0, 0, w, h)
    img.paste(layer, (x, y))


def lead_scene(draw, x, y, w, h):
    """Night sky over Polish fields: a missile trail and a distant burst."""
    draw.rectangle([x, y, x + w, y + h], fill=NAVY)
    stars = [(18, 10), (70, 26), (140, 8), (210, 22), (300, 10), (360, 28),
             (430, 12), (520, 24), (600, 8), (690, 20), (760, 10), (830, 24),
             (900, 10), (250, 36), (480, 38), (700, 36)]
    for sx, sy in stars:
        draw.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1],
                     fill=(220, 220, 200))
    trail = [(x + 90, y + h - 18), (x + 220, y + 82), (x + 360, y + 62),
             (x + 500, y + 52), (x + 640, y + 50)]
    draw.line(trail, fill=(240, 230, 200), width=3)
    draw.ellipse([x + 82, y + h - 26, x + 98, y + h - 10], fill=(255, 210, 120))
    bx, by = x + 700, y + 50
    for r, col in [(40, (255, 190, 60)), (29, (255, 140, 40)),
                   (19, (255, 220, 120)), (10, (255, 244, 200))]:
        draw.ellipse([bx - r, by - r, bx + r, by + r], fill=col)
    for dx, dy in [(-58, -14), (-44, 18), (52, -20), (58, 16), (0, -42),
                   (-26, -34), (36, 34)]:
        draw.line([(bx, by), (bx + dx, by + dy)], fill=(255, 180, 60), width=3)
    ground = h - 34
    draw.polygon([(x, y + h), (x, y + ground), (x + 200, y + ground - 12),
                  (x + 420, y + ground + 2), (x + 640, y + ground - 8),
                  (x + w, y + ground + 2), (x + w, y + h)], fill=(10, 18, 12))
    for hx in (120, 300, 560, 820):
        draw.rectangle([x + hx, y + ground - 18, x + hx + 30, y + ground],
                       fill=(8, 12, 10))
        draw.polygon([(x + hx - 3, y + ground - 18), (x + hx + 15, y + ground - 30),
                      (x + hx + 33, y + ground - 18)], fill=(8, 12, 10))
        draw.rectangle([x + hx + 11, y + ground - 11, x + hx + 18, y + ground - 5],
                       fill=(255, 200, 90))
    draw.text((x + 10, y + h - 20),
              "A Russian missile trail over south-east Poland, Friday.",
              font=font(SANS, 12), fill=(210, 205, 190))


def market_chart(draw, x, y, w, h):
    """Falling line chart of Friday's rout."""
    draw.rectangle([x, y, x + w, y + h], outline=RULE, width=1)
    for i in range(1, 4):
        gy = y + i * h // 4
        draw.line([(x + 8, gy), (x + w - 8, gy)], fill=(210, 200, 180), width=1)
    pts = [(x + 14, y + 30), (x + 70, y + 34), (x + 130, y + 32),
           (x + 190, y + 42), (x + 250, y + 40), (x + 310, y + 50),
           (x + 370, y + 48), (x + 420, y + 58), (x + w - 14, y + h - 10)]
    draw.line(pts, fill=RED, width=3)
    draw.ellipse([pts[-1][0] - 4, pts[-1][1] - 4, pts[-1][0] + 4, pts[-1][1] + 4],
                 fill=RED)
    draw.text((x + 10, y + 5), "S&P 500  -3.7%     NASDAQ  -5.3%     DOW  -1.9%",
              font=font(SANS_B, 14), fill=RED)


def tanker_scene(draw, x, y, w, h):
    """Tankers massing at anchor off Kharg Island."""
    draw.rectangle([x, y, x + w, y + h], fill=(214, 228, 236))
    draw.rectangle([x, y + h - 22, x + w, y + h], fill=SEA)
    draw.ellipse([x + w - 56, y + 6, x + w - 20, y + 42], fill=GOLD)
    for tx, tw, th in [(16, 150, 22), (120, 120, 17), (250, 90, 13)]:
        ty = y + h - 22 - th
        draw.rectangle([x + tx, ty, x + tx + tw, ty + th], fill=(52, 52, 52))
        draw.rectangle([x + tx + tw - 30, ty - 11, x + tx + tw - 10, ty],
                       fill=(52, 52, 52))
        draw.line([(x + tx + 8, ty), (x + tx + 8, ty - 14)], fill=(52, 52, 52),
                  width=2)
    for wy in (y + h - 15, y + h - 7):
        for wx in range(x + 10, x + w - 30, 46):
            draw.line([(wx, wy), (wx + 22, wy)], fill=(255, 255, 255), width=2)


def cyclone_scene(draw, x, y, w, h):
    """Spiral storm over the Bay of Bengal coast."""
    draw.rectangle([x, y, x + w, y + h], fill=(226, 232, 236))
    cx, cy = x + w // 2, y + h // 2 + 2
    for r in range(10, 30, 8):
        draw.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=300,
                 fill=(70, 110, 140), width=3)
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(70, 110, 140))
    for rx in range(x + 12, x + w - 12, 26):
        draw.line([(rx, y + h - 16), (rx - 5, y + h - 5)], fill=(120, 150, 170),
                  width=2)


def cop_scene(draw, x, y, w, h):
    """Sun and globe for the climate talks."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 232, 216))
    cx = x + w // 2
    sun_y = y + 16
    for a in range(0, 360, 45):
        x1 = cx + 20 * math.cos(math.radians(a))
        y1 = sun_y + 20 * math.sin(math.radians(a))
        x2 = cx + 28 * math.cos(math.radians(a))
        y2 = sun_y + 28 * math.sin(math.radians(a))
        draw.line([(x1, y1), (x2, y2)], fill=GOLD, width=2)
    draw.ellipse([cx - 14, sun_y - 14, cx + 14, sun_y + 14], fill=GOLD)
    gy = y + h - 24
    draw.ellipse([cx - 34, gy - 12, cx + 34, gy + 22], fill=SEA)
    draw.polygon([(cx - 24, gy), (cx - 4, gy - 8), (cx + 8, gy + 6),
                  (cx - 2, gy + 16), (cx - 20, gy + 12)], fill=(74, 140, 74))


def quake_scene(draw, x, y, w, h):
    """Seismograph trace across the panel."""
    draw.rectangle([x, y, x + w, y + h], fill=(236, 230, 220))
    mid = y + h // 2
    pts = [(x + 10, mid)]
    spikes = [0, 3, -4, 7, -14, 18, -20, 12, -6, 4, -2, 0]
    step = (w - 20) // len(spikes)
    for i, s in enumerate(spikes):
        pts.append((x + 10 + (i + 1) * step, mid + s))
    pts.append((x + w - 10, mid))
    draw.line(pts, fill=RED, width=3)
    draw.text((x + 10, y + 5), "M 6.7", font=font(SANS_B, 14), fill=RED)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- masthead ----
    draw.text((MARGIN, 18), "THE WORLD TODAY",
              font=font(SERIF_B, 60), fill=INK)
    y = 92
    y = rule(draw, y, 3)
    y += 6
    dateline = "SATURDAY, 21 NOVEMBER 2026  ·  ONE DAY'S WORLD NEWS IN ONE PAGE"
    draw.text((MARGIN, y), dateline, font=font(SANS_B, 17), fill=INK)
    draw.text((W - MARGIN - draw.textlength("No. 326", font=font(SANS_B, 17)),
               y), "No. 326", font=font(SANS_B, 17), fill=INK)
    y += 28
    y = rule(draw, y, 1)

    # ---- lead headline ----
    y += 8
    y = headline(draw, MARGIN, y, "RUSSIAN MISSILES FALL ON POLAND",
                 46, CW)
    y += 2
    y = para(draw, MARGIN, y,
             "Warsaw calls it a deliberate provocation as NATO jets scramble",
             font(SERIF, 20), CW, 26, fill=MUTED)
    y += 8

    # ---- lead picture ----
    panel(img, lead_scene, MARGIN, y, CW, 120)
    y += 120 + 6

    # ---- lead body, two columns ----
    col_w = (CW - 24) // 2
    left = ("Russia fired more than 400 drones and 110 missiles at Ukraine "
            "in its largest air assault this month, killing at least eight "
            "in Kyiv. Two cruise missiles and a drone came down in Poland.")
    right = ("Prime Minister Donald Tusk said the timing was no coincidence. "
             "NATO called it a grave violation, scrambled jets from three "
             "nations, and its chief visits Poland today.")
    y1 = para(draw, MARGIN, y, left, font(SERIF, 15), col_w, 19)
    y2 = para(draw, MARGIN + col_w + 24, y, right, font(SERIF, 15), col_w, 19)
    y = max(y1, y2) + 6
    y = rule(draw, y, 1)
    y += 8

    # ---- second row: markets + gulf ----
    half = (CW - 24) // 2
    y_top = y
    y = kicker(draw, MARGIN, y, "Markets · Wall Street", width=half)
    yy = headline(draw, MARGIN, y, "AI ROUT DRAGS STOCKS INTO CORRECTION",
                  24, half, 26)
    yy = para(draw, MARGIN, yy + 4,
              "The S&P 500 fell 3.7% on Friday as doubts over AI spending "
              "spread; the Nasdaq slid 5.3%. The SEC is examining Nvidia, "
              "and Anthropic slid again after its debut.",
              font(SERIF, 14), half, 17)
    panel(img, market_chart, MARGIN, yy + 6, half, 66)
    left_end = yy + 6 + 66
    y_right = kicker(draw, MARGIN + half + 24, y_top, "Gulf · Standoff at sea",
                     width=half)
    y_right = headline(draw, MARGIN + half + 24, y_right,
                       "IRAN'S TANKERS MASS TO TEST U.S. BLOCKADE", 24, half, 26)
    y_right = para(draw, MARGIN + half + 24, y_right + 4,
                   "More than 14 Iranian-flagged tankers gather at Kharg "
                   "Island to sail as a convoy. Houthi missiles aimed at "
                   "Riyadh were stopped for a third night.",
                   font(SERIF, 14), half, 17)
    panel(img, tanker_scene, MARGIN + half + 24, y_right + 6, half, 66)
    y = max(left_end, y_right + 6 + 66) + 6
    y = rule(draw, y, 1)
    y += 8

    # ---- third row: three stories ----
    third = (CW - 48) // 3
    x3 = [MARGIN, MARGIN + third + 24, MARGIN + 2 * (third + 24)]
    y_top = y
    stories = [
        ("Weather · India", "AKVAN FADES, RAIN ALERT STAYS",
         "Cyclone Akvan weakened to a low over Odisha with no major damage "
         "and no lives lost; 440,000 people had moved to safety.",
         cyclone_scene),
        ("Climate · Antalya", "COP31 MISSES ITS DEADLINE",
         "The climate summit ran past its deadline as the draft dropped any "
         "mention of fossil fuels. Pacific nations warned of the cost.",
         cop_scene),
        ("Quake · Peru", "TREMOR SHAKES LIMA",
         "A magnitude 6.7 earthquake struck Peru's Andean region, sending "
         "residents of the capital into the streets.",
         quake_scene),
    ]
    y_max = y_top
    for (kick, head, body, scene), x in zip(stories, x3):
        yy = kicker(draw, x, y_top, kick, width=third)
        yy = headline(draw, x, yy, head, 20, third, 22)
        yy = para(draw, x, yy + 4, body, font(SERIF, 13), third, 16)
        panel(img, scene, x, yy + 6, third, 50)
        y_max = max(y_max, yy + 6 + 50)
    y = y_max + 8
    y = rule(draw, y, 1)
    y += 6

    # ---- briefs strip ----
    draw.text((MARGIN, y), "IN BRIEF", font=font(SANS_B, 15), fill=RED)
    y += 22
    briefs = [
        "Cancer hope: pancreatic pill trial: tumours gone in 1 in 12.",
        "UK and EU seal reset: food checks to go, youth mobility scheme.",
        "Trump and Xi agree humans must stay in charge of military AI.",
        "Brazil storm kills three and wrecks 5,000 homes in Tupanciretã.",
        "Myanmar ruling may bolster the Gaza case at the UN court.",
    ]
    fnt_b = font(SERIF, 13)
    col_w = (CW - 24) // 2
    row_h = 17
    for i, b in enumerate(briefs):
        bx = MARGIN if i % 2 == 0 else MARGIN + col_w + 24
        by = y + (i // 2) * row_h
        draw.text((bx, by), "•  " + b, font=fnt_b, fill=INK)
    y = y + ((len(briefs) + 1) // 2) * row_h + 4
    y = rule(draw, y, 1)

    # ---- footer ----
    draw.text((MARGIN, y + 8),
              "THE WORLD TODAY  ·  Saturday, 21 November 2026  ·  Sources: AP, BBC, Reuters, IMD, RNZ",
              font=font(SANS, 13), fill=MUTED)

    img.save("news_image.png")
    print("wrote news_image.png", img.size)


if __name__ == "__main__":
    build()
