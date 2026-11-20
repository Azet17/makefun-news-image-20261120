#!/usr/bin/env python3
"""Render the front page for news-image-20261120.

Draws a 1024x1024 newspaper front page ("THE WORLD TODAY") with a 2x3
grid of six stories from Friday 20 November 2026. All artwork is
geometric shapes drawn in code with Pillow -- no photos, no copied art.

Deterministic: same input always produces the same PNG bytes.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

PAPER = (246, 241, 229)
INK = (26, 26, 26)
PANEL_BG = (255, 253, 247)
RULE = (164, 30, 34)
MUTED = (90, 84, 72)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if font_getlen(fnt, trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def font_getlen(fnt, text):
    return fnt.getlength(text)


# ---------------------------------------------------------------- stories
# Headlines/summaries verified against reporting published 19-20 Nov 2026.
STORIES = [
    {
        "tag": "POLITICS",
        "tag_bg": (164, 30, 34),
        "pic_bg": (250, 232, 228),
        "pic": "summit",
        "headline": "Three leaders, one table",
        "summary": "Trump, Xi and Putin meet in China for a first-ever trilateral summit at the APEC meeting in Shenzhen.",
    },
    {
        "tag": "JUSTICE",
        "tag_bg": (30, 58, 95),
        "pic_bg": (226, 234, 246),
        "pic": "scales",
        "headline": "UN court: Myanmar committed genocide",
        "summary": "The ICJ rules 9-6 that the 2017 crackdown on the Rohingya was genocide - a first ruling against a state.",
    },
    {
        "tag": "WEATHER",
        "tag_bg": (14, 116, 144),
        "pic_bg": (224, 242, 246),
        "pic": "cyclone",
        "headline": "Cyclone Akvan bears down on Odisha",
        "summary": "80,000 people evacuated as the severe storm nears India's east coast, with landfall expected today.",
    },
    {
        "tag": "TECH",
        "tag_bg": (88, 28, 135),
        "pic_bg": (238, 228, 248),
        "pic": "ipo",
        "headline": "Anthropic's $1.5 trillion debut",
        "summary": "The Claude maker raises a record $81bn in the biggest IPO ever and starts trading on the Nasdaq.",
    },
    {
        "tag": "SPORT",
        "tag_bg": (22, 101, 52),
        "pic_bg": (228, 242, 230),
        "pic": "cricket",
        "headline": "Nicholls century steadies New Zealand",
        "summary": "An unbeaten 113 lifts the hosts to 243 for 5 on day one of the first Test against India in Wellington.",
    },
    {
        "tag": "MARKETS",
        "tag_bg": (146, 64, 14),
        "pic_bg": (250, 238, 224),
        "pic": "chart",
        "headline": "Sensex storms past 83,000",
        "summary": "India's benchmark jumps 1.2% to a record close at 83,021.75 as banks and auto stocks lead the rally.",
    },
]

SOURCES = ("Sources: The Times of India - Reuters - NPR - Business Day - "
           "Jagran Josh - UN IIMM  |  20 November 2026")


# ------------------------------------------------------------- pictograms
def pic_summit(d, cx, cy, s):
    """Three leaders around one table: three circles, one table."""
    cols = [(185, 28, 28), (29, 78, 216), (180, 83, 9)]
    for i, c in enumerate(cols):
        x = cx + (i - 1) * int(30 * s)
        r = int(17 * s)
        d.ellipse([x - r, cy - r, x + r, cy + r], fill=c,
                  outline=(255, 255, 255), width=2)
    # table
    d.rectangle([cx - int(52 * s), cy + int(26 * s),
                 cx + int(52 * s), cy + int(31 * s)], fill=INK)
    d.line([cx - int(44 * s), cy + int(31 * s),
            cx - int(44 * s), cy + int(44 * s)], fill=INK, width=3)
    d.line([cx + int(44 * s), cy + int(31 * s),
            cx + int(44 * s), cy + int(44 * s)], fill=INK, width=3)


def pic_scales(d, cx, cy, s):
    """Scales of justice."""
    # pillar and base
    d.line([cx, cy - int(40 * s), cx, cy + int(40 * s)], fill=INK, width=4)
    d.line([cx - int(22 * s), cy + int(40 * s),
            cx + int(22 * s), cy + int(40 * s)], fill=INK, width=4)
    # beam
    d.line([cx - int(48 * s), cy - int(28 * s),
            cx + int(48 * s), cy - int(28 * s)], fill=INK, width=4)
    d.ellipse([cx - 5, cy - int(45 * s), cx + 5, cy - int(35 * s)],
              fill=(180, 150, 40))
    for side in (-1, 1):
        px = cx + side * int(48 * s)
        d.line([px, cy - int(28 * s), px, cy - int(2 * s)], fill=INK, width=3)
        # pan: half-disc
        d.pieslice([px - int(20 * s), cy - int(2 * s),
                    px + int(20 * s), cy + int(30 * s)],
                   start=0, end=180, fill=(180, 150, 40))


def pic_cyclone(d, cx, cy, s):
    """Spiral storm with rain."""
    for i, r in enumerate((14, 24, 34, 44)):
        start = 200 + i * 55
        d.arc([cx - r, cy - r, cx + r, cy + r], start=start,
              end=start + 210, fill=(14, 116, 144), width=5)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(14, 116, 144))
    # rain drops
    for dx in (-52, -38, 38, 52):
        x = cx + int(dx * s)
        d.line([x, cy + int(30 * s), x - 4, cy + int(44 * s)],
               fill=(56, 130, 160), width=3)


def pic_ipo(d, cx, cy, s):
    """Rising bars with an upward arrow."""
    heights = (18, 30, 44, 58)
    bw = int(16 * s)
    gap = int(10 * s)
    x0 = cx - int((4 * bw + 3 * gap) / 2)
    for i, h in enumerate(heights):
        x = x0 + i * (bw + gap)
        y = cy + int(34 * s) - int(h * s)
        d.rectangle([x, y, x + bw, cy + int(34 * s)],
                    fill=(88, 28, 135))
    # arrow
    d.line([cx - int(52 * s), cy + int(18 * s),
            cx + int(52 * s), cy - int(40 * s)], fill=(22, 101, 52), width=5)
    d.line([cx + int(52 * s), cy - int(40 * s),
            cx + int(30 * s), cy - int(40 * s)], fill=(22, 101, 52), width=5)
    d.line([cx + int(52 * s), cy - int(40 * s),
            cx + int(52 * s), cy - int(18 * s)], fill=(22, 101, 52), width=5)


def pic_cricket(d, cx, cy, s):
    """Bat and ball."""
    # bat: rotated rectangle (polygon)
    d.polygon([(cx - int(34 * s), cy - int(8 * s)),
               (cx - int(6 * s), cy - int(36 * s)),
               (cx + int(8 * s), cy - int(22 * s)),
               (cx - int(20 * s), cy + int(6 * s))],
              fill=(146, 96, 44))
    # handle
    d.line([cx - int(6 * s), cy - int(36 * s),
            cx + int(8 * s), cy - int(50 * s)], fill=INK, width=5)
    # ball
    bx, by = cx + int(34 * s), cy + int(22 * s)
    d.ellipse([bx - 13, by - 13, bx + 13, by + 13], fill=(185, 28, 28))
    d.arc([bx - 13, by - 13, bx + 13, by + 13], start=200, end=340,
          fill=(255, 255, 255), width=2)
    # stumps
    for i in range(3):
        sx = cx - int(46 * s) + i * 8
        d.line([sx, cy + int(26 * s), sx, cy + int(46 * s)],
               fill=(200, 160, 60), width=3)


def pic_chart(d, cx, cy, s):
    """Rising market line with points."""
    pts = [(-56, 26), (-32, 12), (-10, 18), (14, -6), (34, -16), (56, -34)]
    pts = [(cx + int(x * s), cy + int(y * s)) for x, y in pts]
    d.line(pts, fill=(146, 64, 14), width=5, joint="curve")
    for x, y in pts:
        d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(146, 64, 14))
    # arrowhead at the end
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - 16, ey + 2), (ex - 4, ey + 14)],
              fill=(146, 64, 14))
    # baseline
    d.line([cx - int(62 * s), cy + int(40 * s),
            cx + int(62 * s), cy + int(40 * s)], fill=MUTED, width=2)


PICS = {
    "summit": pic_summit,
    "scales": pic_scales,
    "cyclone": pic_cyclone,
    "ipo": pic_ipo,
    "cricket": pic_cricket,
    "chart": pic_chart,
}


# ---------------------------------------------------------------- render
def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead
    f_mast = font(SERIF_B, 84)
    f_date = font(SANS_B, 30)
    f_sub = font(SANS, 18)

    d.rectangle([28, 26, W - 28, 30], fill=RULE)
    title = "THE WORLD TODAY"
    tw = f_mast.getlength(title)
    d.text(((W - tw) / 2, 40), title, font=f_mast, fill=INK)
    d.rectangle([28, 138, W - 28, 142], fill=INK)
    date_line = "FRIDAY 20 NOVEMBER 2026"
    dw = f_date.getlength(date_line)
    d.text(((W - dw) / 2, 152), date_line, font=f_date, fill=RULE)
    tagline = "Six stories that sum up the day - from Shenzhen to The Hague to Wellington"
    sw = f_sub.getlength(tagline)
    d.text(((W - sw) / 2, 188), tagline, font=f_sub, fill=MUTED)

    # --- 2x3 grid
    margin = 32
    gap = 16
    pw = (W - 2 * margin - gap) // 2
    grid_top, grid_bottom = 224, 956
    ph = (grid_bottom - grid_top - 2 * gap) // 3

    f_tag = font(SANS_B, 16)
    f_head = font(SERIF_B, 22)
    f_sum = font(SANS, 14)

    for i, st in enumerate(STORIES):
        row, col = divmod(i, 2)
        x = margin + col * (pw + gap)
        y = grid_top + row * (ph + gap)

        d.rectangle([x, y, x + pw, y + ph], fill=PANEL_BG,
                    outline=(200, 192, 172), width=1)
        # tag chip
        tag = st["tag"]
        tw = f_tag.getlength(tag)
        chip_w = int(tw) + 20
        d.rectangle([x + 12, y + 10, x + 12 + chip_w, y + 34],
                    fill=st["tag_bg"])
        d.text((x + 22, y + 12), tag, font=f_tag, fill=(255, 255, 255))

        # pictogram band
        band_y0, band_y1 = y + 44, y + 128
        d.rectangle([x + 12, band_y0, x + pw - 12, band_y1],
                    fill=st["pic_bg"])
        PICS[st["pic"]](d, x + pw // 2, (band_y0 + band_y1) // 2, 0.9)

        # headline (max 2 lines)
        lines = wrap(st["headline"], f_head, pw - 28)[:2]
        hy = band_y1 + 8
        for ln in lines:
            d.text((x + 14, hy), ln, font=f_head, fill=INK)
            hy += 25
        # summary (max 2 lines)
        slines = wrap(st["summary"], f_sum, pw - 28)[:2]
        sy = band_y1 + 8 + 2 * 25 + 4
        for ln in slines:
            d.text((x + 14, sy), ln, font=f_sum, fill=(64, 60, 52))
            sy += 18

    # --- footer
    f_foot = font(SANS, 14)
    fw = f_foot.getlength(SOURCES)
    d.text(((W - fw) / 2, 972), SOURCES, font=f_foot, fill=MUTED)
    d.rectangle([28, 996, W - 28, 998], fill=(200, 192, 172))

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    render()
