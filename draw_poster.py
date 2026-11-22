"""Draw the 21 November 2026 world-news poster, version 2 (1024x1024 PNG).

Second entry for the make.fun news-image-20261121 bounty. Bigger type
than v1, nine stories instead of seven, and corrected numbers: Kryvyi
Rih is "dozens hurt" (reports differed on the exact count), and a
dengue breakthrough in Brazil joins the grid for breadth.

Run locally with Pillow:  python3 draw_poster.py
Writes entry.png next to this file. The grader cannot install Pillow,
so the submitted entrypoint (main.py) ships the rendered PNG and
copies it to /output/entry.png deterministically.
All facts were checked against BBC / Reuters / AP / Al Jazeera /
The Guardian / WSJ reporting for Saturday 21 November 2026.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

NAVY = (15, 30, 58)
NAVY2 = (22, 44, 82)
GOLD = (232, 180, 60)
RED = (198, 48, 38)
CREAM = (248, 244, 232)
INK = (24, 28, 36)
GREY = (88, 96, 110)
WHITE = (255, 255, 255)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, color, max_w, leading=None):
    lines = wrap(draw, text, fnt, max_w)
    lh = leading or int(fnt.size * 1.28)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=color)
        y += lh
    return y


def burst(draw, cx, cy, r, color):
    import math
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=color)
    draw.ellipse([cx - r * 0.32, cy - r * 0.32, cx + r * 0.32, cy + r * 0.32],
                 fill=(255, 220, 120))


img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)

# ---- masthead ----
d.rectangle([0, 0, W, 148], fill=NAVY)
d.rectangle([0, 148, W, 154], fill=GOLD)
d.text((32, 20), "THE WORLD IN ONE DAY", font=font(SERIF_B, 60), fill=WHITE)
d.text((32, 96), "SATURDAY  •  21 NOVEMBER 2026", font=font(SANS_B, 32), fill=GOLD)
d.text((712, 96), "9 STORIES", font=font(SANS_B, 28), fill=(180, 200, 230))

# ---- lead story: Iran / Bahrain ----
LX, LY, LW, LH = 24, 172, 976, 240
d.rounded_rectangle([LX, LY, LX + LW, LY + LH], radius=14, fill=WHITE,
                    outline=(210, 205, 190), width=2)
d.rounded_rectangle([LX, LY, LX + 300, LY + LH], radius=14, fill=(18, 58, 74))
d.rectangle([LX, LY + LH - 14, LX + 300, LY + LH], fill=(18, 58, 74))
d.rectangle([LX + 286, LY, LX + 300, LY + LH], fill=(18, 58, 74))
d.ellipse([LX + 55, LY + 140, LX + 245, LY + 212], fill=(38, 110, 130))
d.ellipse([LX + 95, LY + 152, LX + 205, LY + 200], fill=(232, 180, 60))
burst(d, LX + 150, LY + 88, 58, (240, 120, 40))
d.text((LX + 62, LY + 212), "BAHRAIN", font=font(SANS_B, 22), fill=WHITE)
d.text((LX + 18, LY + 18), "GULF", font=font(SANS_B, 20), fill=(150, 200, 215))
tx = LX + 326
d.text((tx, LY + 16), "IRAN STRIKES BAHRAIN", font=font(SANS_B, 44), fill=RED)
d.text((tx, LY + 70), "US BASES TARGETED", font=font(SANS_B, 28), fill=INK)
text_block(d, tx, LY + 112,
           "Tehran says it hit two US bases at al-Riffa and Awali. "
           "Bahrain says a civilian industrial site caught fire — no injuries reported.",
           font(SANS, 24), INK, 620)
d.text((tx, LY + 212), "IRAN  •  BAHRAIN  •  GULF", font=font(SANS_B, 20), fill=GREY)

# ---- eight stories, 4 x 2 grid ----
stories = [
    ("KRYVYI RIH, UKRAINE", "MISSILE HITS KRYVYI RIH",
     "2 killed, dozens hurt in Zelenskyy's hometown.",
     (90, 70, 80), "skyline"),
    ("NEW YORK, USA", "AI SELL-OFF",
     "S&P -3.7%, Dow -950 pts. Nasdaq -5.3%. Nvidia -14%.",
     (150, 40, 40), "chart"),
    ("ANTALYA, TURKEY", "CLIMATE TALKS IN OVERTIME",
     "No deal by the deadline; fossil fuels left out.",
     (30, 110, 70), "globe"),
    ("THE HAGUE", "GENOCIDE RULING",
     "World court finds Myanmar guilty over the Rohingya.",
     (40, 70, 140), "scales"),
    ("SINALOA, MEXICO", "CHAPO ISIDRO CAPTURED",
     "Most-wanted cartel boss seized; 11+ dead after.",
     (20, 110, 110), "shield"),
    ("MATHS / AI", "RIEMANN PROOF CLAIMED",
     "Mathematician says Claude helped prove it.",
     (90, 50, 130), "primes"),
    ("BRAZIL", "DENGUE BREAKTHROUGH",
     "Bacteria-carrying mosquitoes cut dengue in children.",
     (20, 120, 90), "mosquito"),
    ("RIYADH / BALTIC", "WAR SPILLS OVER",
     "Houthi missiles stopped; Russian ship hit by drones.",
     (120, 60, 60), "spillover"),
]
GX, GY = 24, 424
CW, CH, GAP = 235, 252, 12
for i, (place, title, body, col, kind) in enumerate(stories):
    x = GX + (i % 4) * (CW + GAP)
    y = GY + (i // 4) * (CH + GAP)
    d.rounded_rectangle([x, y, x + CW, y + CH], radius=12, fill=WHITE,
                        outline=(210, 205, 190), width=2)
    # illustration band
    d.rounded_rectangle([x, y, x + CW, y + 72], radius=12, fill=col)
    d.rectangle([x, y + 58, x + CW, y + 72], fill=col)
    if kind == "chart":
        pts = [(x + 16, y + 54), (x + 64, y + 36), (x + 112, y + 44),
               (x + 160, y + 18), (x + 200, y + 26), (x + 220, y + 58)]
        d.line(pts, fill=WHITE, width=6, joint="curve")
        d.polygon([(x + 220, y + 58), (x + 204, y + 48), (x + 208, y + 64)],
                  fill=WHITE)
    elif kind == "skyline":
        for bx, bh in [(16, 30), (48, 44), (84, 26), (116, 40), (148, 32),
                       (180, 46), (204, 28)]:
            d.rectangle([x + bx, y + 66 - bh, x + bx + 24, y + 66],
                        fill=(255, 255, 255))
        burst(d, x + 116, y + 30, 20, (240, 120, 40))
    elif kind == "globe":
        d.ellipse([x + 168, y + 8, x + 224, y + 62], fill=(120, 200, 130))
        d.ellipse([x + 178, y + 16, x + 214, y + 54], fill=(60, 160, 90))
        d.text((x + 18, y + 18), "COP31", font=font(SANS_B, 28), fill=WHITE)
    elif kind == "scales":
        d.line([x + 118, y + 12, x + 118, y + 58], fill=WHITE, width=5)
        d.line([x + 78, y + 20, x + 158, y + 20], fill=WHITE, width=5)
        d.ellipse([x + 64, y + 20, x + 92, y + 44], outline=WHITE, width=4)
        d.ellipse([x + 144, y + 20, x + 172, y + 44], outline=WHITE, width=4)
    elif kind == "primes":
        d.text((x + 16, y + 10), "2  3  5  7  11  13", font=font(SANS_B, 24),
               fill=WHITE)
        d.text((x + 16, y + 38), "ζ(s) = 0  ?", font=font(SANS_B, 24),
               fill=(255, 220, 120))
    elif kind == "shield":
        d.polygon([(x + 118, y + 8), (x + 152, y + 18), (x + 152, y + 40),
                   (x + 118, y + 62), (x + 84, y + 40), (x + 84, y + 18)],
                  outline=WHITE, width=5)
        d.text((x + 107, y + 24), "★", font=font(SANS_B, 26), fill=WHITE)
    elif kind == "mosquito":
        d.ellipse([x + 96, y + 22, x + 140, y + 50], fill=WHITE)
        d.ellipse([x + 70, y + 12, x + 106, y + 34], outline=WHITE, width=4)
        d.ellipse([x + 130, y + 12, x + 166, y + 34], outline=WHITE, width=4)
        d.line([x + 100, y + 50, x + 88, y + 64], fill=WHITE, width=4)
        d.line([x + 118, y + 50, x + 118, y + 66], fill=WHITE, width=4)
        d.line([x + 136, y + 50, x + 148, y + 64], fill=WHITE, width=4)
    elif kind == "spillover":
        burst(d, x + 62, y + 36, 22, (240, 120, 40))
        burst(d, x + 172, y + 36, 22, (240, 120, 40))
    d.text((x + 12, y + 82), place, font=font(SANS_B, 17), fill=GREY)
    yy = text_block(d, x + 12, y + 104, title, font(SANS_B, 24), INK,
                    CW - 24, leading=28)
    text_block(d, x + 12, yy + 6, body, font(SANS, 18), (50, 56, 68), CW - 24,
               leading=23)

# ---- also strip + footer ----
AY = GY + 2 * CH + GAP
d.rounded_rectangle([24, AY, 1000, AY + 38], radius=10, fill=NAVY2)
d.text((40, AY + 10), "ALSO:  Iran says it downed a US drone near Qeshm  •  "
       "Two tankers struck in the Strait of Hormuz",
       font=font(SANS_B, 17), fill=WHITE)
d.text((32, AY + 46), "Sources: BBC, Reuters, AP, Al Jazeera, The Guardian, WSJ  •  "
       "Claims are attributed where they were not independently verified.",
       font=font(SANS, 15), fill=GREY)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
