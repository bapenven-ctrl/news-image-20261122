#!/usr/bin/env python3
"""Render entry.png for news-image-20261122 V1 (ATM).

Fresh design, written from scratch in this session (2026-11-23):
  - DATE CHECK FIRST: a red proof strip directly under the masthead, before
    any story, naming what was left out and why.
  - THE DAY DECIDED: five verdict boxes (COP31 NO DEAL, Benghazi warship
    hit, House 258, ICJ genocide, markets -3.7%) — the day's decisions.
  - ONE WAR, FOUR SEAS: four scene panels joined by one drawn route line
    (Dymer -> Sparta II -> Benghazi -> Bahrain/Hormuz), each with one big
    number baked into its illustration.
  - THE REST OF THE DAY: 28 more stories in three region columns, 12-13 px
    type, no tiny numbered list anywhere, no footer mini-map.
Not the broadsheet of the top entries, and not the V3 map-hero of 21 Nov.
All drawings are procedural vector work in this file; no external assets.
Deterministic: no randomness, no clock, no network. Rendered at 2x then
downscaled with LANCZOS to 1024x1024.
"""
import sys
from PIL import Image, ImageDraw, ImageFont

S = 2                      # supersample factor
W, H = 1024 * S, 1024 * S
MX = 24                    # side margin
CW = 1024 - 2 * MX         # content width = 976

# ---------- palette ----------
PAPER   = (247, 242, 231)  # cream paper
INK     = (20, 20, 20)     # near-black
GREY    = (110, 108, 100)
FAINT   = (150, 148, 138)
RED     = (178, 34, 34)    # kept for the most urgent (W4)
DARKRED = (140, 20, 20)
NAVY    = (16, 24, 48)     # night sky
DUSK    = (46, 52, 84)
SEA     = (28, 52, 76)
SEA2    = (18, 38, 60)
LAND    = (223, 217, 196)
WHITE   = (255, 255, 255)
CREAMBOX = (255, 246, 240) # date-check fill
DARKBOX = (24, 42, 60)
BAND    = (20, 20, 20)
GREEN   = (46, 125, 50)    # CONFIRMED
AMBER   = (176, 124, 0)    # REPORTED
ORANGE  = (230, 126, 34)
YELLOW  = (240, 196, 60)

# region colours (W1: same colour on verdict strip, panel chip, column disc)
REGION = {
    "EUROPE":   (31, 78, 121),
    "MIDEAST":  (179, 84, 30),
    "AMERICAS": (46, 125, 50),
    "ASIA-PAC": (106, 27, 154),
    "OCEANIA":  (0, 131, 143),
    "AFRICA":   (141, 110, 0),
    "WORLD":    (55, 71, 79),
}

# ---------- fonts ----------
FD = "/usr/share/fonts/truetype/noto/"
def F(name, size):
    return ImageFont.truetype(FD + name, size * S)

SERIF_B = lambda s: F("NotoSerif-Bold.ttf", s)
SERIF   = lambda s: F("NotoSerif-Regular.ttf", s)
SERIF_I = lambda s: F("NotoSerif-Italic.ttf", s)
SANS    = lambda s: F("NotoSans-Regular.ttf", s)
SANS_B  = lambda s: F("NotoSans-Bold.ttf", s)
SANS_I  = lambda s: F("NotoSans-Italic.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def X(v): return v * S
def Y(v): return v * S

def text(x, y, s, font, fill=INK, anchor="la"):
    d.text((X(x), Y(y)), s, font=font, fill=fill, anchor=anchor)

def text_w(s, font):
    return d.textlength(s, font=font) / S

def fit(s, font, maxw, label):
    """Assert a line fits; fail loudly instead of overflowing silently."""
    w = text_w(s, font)
    assert w <= maxw, f"OVERFLOW {label}: {w:.1f} > {maxw} :: {s!r}"
    return w

def wrap(s, font, maxw, max_lines, label):
    """Greedy word wrap; asserts the text fits in max_lines."""
    words = s.split()
    lines, cur = [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if text_w(t, font) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    assert len(lines) <= max_lines, \
        f"WRAP {label}: {len(lines)} lines > {max_lines} :: {s!r}"
    assert all(text_w(ln, font) <= maxw for ln in lines), \
        f"WRAP-WIDTH {label} :: {s!r}"
    return lines

def rrect(x0, y0, x1, y1, fill=None, outline=None, width=1, radius=0):
    d.rounded_rectangle([X(x0), Y(y0), X(x1), Y(y1)], radius=radius * S,
                        fill=fill, outline=outline, width=width * S)

def rect(x0, y0, x1, y1, fill=None, outline=None, width=1):
    d.rectangle([X(x0), Y(y0), X(x1), Y(y1)], fill=fill,
                outline=outline, width=width * S)

def line(x0, y0, x1, y1, fill=INK, width=1):
    d.line([X(x0), Y(y0), X(x1), Y(y1)], fill=fill, width=width * S)

def section_header(y, label, right=""):
    text(MX, y, label, SANS_B(13), fill=INK)
    if right:
        text(1024 - MX, y, right, SANS(11), fill=GREY, anchor="ra")
    line(MX, y + 17, 1024 - MX, y + 17, fill=INK, width=1)

# =========================================================
# 0. TOP BAND  (y 0..26)
# =========================================================
rect(0, 0, 1024, 26, fill=BAND)
text(MX, 7, "THE WORLD IN ONE DAY", SANS_B(11), fill=WHITE)
text(1024 - MX, 7, "36 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE DATED SUNDAY 22 NOVEMBER 2026",
     SANS_B(11), fill=WHITE, anchor="ra")

# =========================================================
# 1. MASTHEAD  (y 26..118)
# =========================================================
text(512, 34, "Sunday 22 November 2026", SERIF_B(62), fill=INK, anchor="ma")
text(512, 100, "COP31 ends with no deal  \u00b7  A Russian warship is hit at Benghazi  \u00b7  Democrats take the House, 258\u2013173",
     SERIF_I(17), fill=RED, anchor="ma")

# =========================================================
# 2. DATE CHECK FIRST  (y 122..182)
# =========================================================
rrect(MX, 122, 1024 - MX, 182, fill=CREAMBOX, outline=RED, width=2)
rect(MX, 122, 168, 182, fill=RED)
text(MX + 12, 130, "DATE CHECK", SANS_B(15), fill=WHITE)
text(MX + 12, 150, "READ THIS FIRST", SANS_B(11), fill=WHITE)
text(180, 128, "Every story below happened or was first reported Sunday 22 Nov 2026 (UTC).",
     SANS_B(13), fill=INK)
dc2 = "Left out \u2014 they happened earlier: \u2018El Chapo Isidro\u2019 captured (Sat) \u00b7 Peru quake (Fri) \u00b7"
dc3 = "EU\u2013Indonesia signing (Sat) \u00b7 Kryvyi Rih (Fri) \u00b7 400-drone barrage (19\u201320 Nov) \u00b7 BepiColombo (Sat) \u00b7 Hormuz tankers (Sat)."
fit(dc2, SANS(12), 1024 - MX - 180, "datecheck-2")
fit(dc3, SANS(12), 1024 - MX - 180, "datecheck-3")
text(180, 148, dc2, SANS(12), fill=INK)
text(180, 164, dc3, SANS(12), fill=INK)

# =========================================================
# 3. THE DAY DECIDED — five verdict boxes  (y 188..316)
# =========================================================
section_header(188, "THE DAY DECIDED \u2014 FIVE VERDICTS")
# (place, region, verdict, number, fact)
VERDICTS = [
    ("ANTALYA \u00b7 CLIMATE", "EUROPE",   "NO DEAL",   "130",   "Parties said no"),
    ("BENGHAZI \u00b7 LIBYA",  "AFRICA",   "WARSHIP HIT", "6",   "6 drones, 2 hits on Merkury"),
    ("WASHINGTON \u00b7 POLITICS", "AMERICAS", "HOUSE 258", "258", "Biggest majority since 1992"),
    ("THE HAGUE \u00b7 JUSTICE", "WORLD",  "GENOCIDE",  "2017",  "The year the Rohingya fled"),
    ("NEW YORK \u00b7 MARKETS", "WORLD",   "SELL-OFF",  "-3.7%", "S&P slides; Nvidia probed"),
]
VW, VGAP = 188, 8
VY0, VY1 = 206, 316
for i, (place, region, verdict, number, fact) in enumerate(VERDICTS):
    x0 = MX + i * (VW + VGAP)
    x1 = x0 + VW
    rrect(x0, VY0, x1, VY1, fill=WHITE, outline=GREY, width=1)
    rect(x0 + 1, VY0 + 1, x1 - 1, VY0 + 7, fill=REGION[region])
    text(x0 + 10, VY0 + 14, place, SANS_B(11), fill=GREY)
    fit(verdict, SANS_B(20), VW - 20, f"verdict-{i}")
    text(x0 + 10, VY0 + 32, verdict, SANS_B(20), fill=INK)
    fit(number, SANS_B(32), VW - 20, f"verdict-num-{i}")
    text(x0 + 10, VY0 + 56, number, SANS_B(32), fill=RED)
    fit(fact, SANS(12), VW - 20, f"verdict-fact-{i}")
    text(x0 + 10, VY0 + 92, fact, SANS(12), fill=INK)

# =========================================================
# 4. ONE WAR, FOUR SEAS — arc band  (y 322..580)
# =========================================================
section_header(322, "ONE WAR, FOUR SEAS \u2014 THE SAME WAR, FOUR SEAS")
# dashed route across the whole band at scene mid-height
RY = 405
x = MX
while x < 1024 - MX:
    seg = min(8, 1024 - MX - x)
    line(x, RY, x + seg, RY, fill=RED, width=2)
    x += 16
PW, PGAP = 236, 10
PY0, PY1 = 340, 580
SCENE_H = 130

def badge(x0, y0, s, size=28):
    """Big baked number, cream disc with red ring, top-right of a scene."""
    bw = text_w(s, SANS_B(size)) + 18
    bx1 = x0 + PW - 8
    bx0 = bx1 - bw
    by0, by1 = y0 + 8, y0 + 8 + 36
    d.ellipse([X(bx0), Y(by0), X(bx1), Y(by1)], fill=PAPER,
              outline=RED, width=2 * S)
    text((bx0 + bx1) / 2, by0 + 5, s, SANS_B(size), fill=RED, anchor="ma")

def panel(i, story_no, place, region, status, headline, fact, num, draw_scene):
    x0 = MX + i * (PW + PGAP)
    x1 = x0 + PW
    rrect(x0, PY0, x1, PY1, fill=WHITE, outline=GREY, width=1)
    draw_scene(x0, PY0, x1, PY0 + SCENE_H)
    badge(x0, PY0, num)
    # story number disc on the scene, top-left
    d.ellipse([X(x0 + 8), Y(PY0 + 8), X(x0 + 30), Y(PY0 + 30)],
              fill=REGION[region])
    text(x0 + 19, PY0 + 11, str(story_no), SANS_B(12), fill=WHITE, anchor="ma")
    hy = PY0 + SCENE_H + 8
    lines = wrap(headline, SANS_B(15), PW - 16, 2, f"arc-head-{i}")
    for j, ln in enumerate(lines):
        text(x0 + 8, hy + j * 18, ln, SANS_B(15), fill=INK)
    fy = hy + len(lines) * 18 + 2
    flines = wrap(fact, SANS(12), PW - 16, 2, f"arc-fact-{i}")
    for j, ln in enumerate(flines):
        text(x0 + 8, fy + j * 15, ln, SANS(12), fill=INK)
    # chips row at the bottom
    cy = PY1 - 24
    text(x0 + 8, cy, place, SANS_B(11), fill=REGION[region])
    scol = {"CONFIRMED": GREEN, "REPORTED": AMBER, "CLAIM": RED}[status]
    sw = text_w(status, SANS_B(11)) + 12
    rrect(x1 - 8 - sw, cy - 2, x1 - 8, cy + 14, fill=scol, radius=2)
    text(x1 - 8 - sw / 2, cy, status, SANS_B(11), fill=WHITE, anchor="ma")
    # arrowhead in the gap to the next panel, on the route line
    if i < 3:
        gx = x1 + 1
        d.polygon([(X(gx), Y(RY - 6)), (X(gx), Y(RY + 6)),
                   (X(gx + 8), Y(RY))], fill=RED)

def scene_dymer(x0, y0, x1, y1):
    rect(x0, y0, x1, y1, fill=NAVY)
    # stars
    for sx, sy in [(30, 18), (80, 30), (140, 12), (180, 34), (60, 48), (200, 55)]:
        d.ellipse([X(x0 + sx), Y(y0 + sy), X(x0 + sx + 3), Y(y0 + sy + 3)], fill=WHITE)
    # apartment block, 5 storeys, lit windows
    bx0, bx1 = x0 + 28, x0 + 108
    rect(bx0, y0 + 38, bx1, y1, fill=(38, 38, 52))
    for fl in range(5):
        for wn in range(4):
            wx, wy = bx0 + 8 + wn * 19, y0 + 46 + fl * 16
            col = YELLOW if (fl + wn) % 3 else (90, 90, 110)
            rect(wx, wy, wx + 11, wy + 9, fill=col)
    # collapsed corner: dark rubble wedge
    d.polygon([(X(bx1), Y(y0 + 38)), (X(x1 - 20), Y(y0 + 70)),
               (X(bx1), Y(y0 + 92))], fill=(24, 24, 34))
    # drone silhouettes with dotted trails (light grey so they read on navy)
    for dx, dy in [(150, 40), (185, 62), (130, 78)]:
        line(x0 + dx - 34, y0 + dy - 8, x0 + dx - 6, y0 + dy - 2, fill=WHITE, width=1)
        d.ellipse([X(x0 + dx - 2), Y(y0 + dy - 6), X(x0 + dx + 10), Y(y0 + dy + 2)],
                  fill=(205, 205, 215))
        line(x0 + dx + 4, y0 + dy - 2, x0 + dx + 4, y0 + dy + 8, fill=(205, 205, 215), width=1)
    line(x0, y1 - 1, x1, y1 - 1, fill=(10, 10, 16), width=2)

def scene_sparta(x0, y0, x1, y1):
    # dusk sky + sea
    rect(x0, y0, x1, y0 + 52, fill=(214, 132, 74))
    d.ellipse([X(x0 + 112), Y(y0 + 14), X(x0 + 152), Y(y0 + 54)], fill=(240, 196, 110))
    rect(x0, y0 + 52, x1, y1, fill=SEA)
    for wy in (y0 + 70, y0 + 92, y0 + 114):
        for wx in range(0, PW, 34):
            line(x0 + wx, wy, x0 + wx + 18, wy, fill=(120, 160, 190), width=2)
    # ship: hull + containers
    rect(x0 + 30, y0 + 88, x0 + 200, y0 + 108, fill=(24, 30, 38))
    for cx, cc in [(44, (178, 34, 34)), (76, (31, 78, 121)), (108, (46, 125, 50)),
                   (140, (176, 124, 0))]:
        rect(x0 + cx, y0 + 66, x0 + cx + 28, y0 + 88, fill=cc)
    # flames + smoke over the mid containers
    for fx, fy, fs in [(96, 46, 16), (118, 40, 20), (140, 48, 14)]:
        d.polygon([(X(x0 + fx), Y(y0 + fy + fs)), (X(x0 + fx + fs // 2), Y(y0 + fy)),
                   (X(x0 + fx + fs), Y(y0 + fy + fs))], fill=ORANGE)
        d.polygon([(X(x0 + fx + 3), Y(y0 + fy + fs)), (X(x0 + fx + fs // 2), Y(y0 + fy + 6)),
                   (X(x0 + fx + fs - 3), Y(y0 + fy + fs))], fill=YELLOW)
    for sx, sy, sr in [(110, 22, 9), (130, 14, 11), (150, 24, 8)]:
        d.ellipse([X(x0 + sx - sr), Y(y0 + sy - sr), X(x0 + sx + sr), Y(y0 + sy + sr)],
                  fill=(90, 90, 96))

def scene_benghazi(x0, y0, x1, y1):
    rect(x0, y0, x1, y1, fill=NAVY)
    for sx, sy in [(24, 16), (90, 26), (160, 12), (205, 30), (60, 44)]:
        d.ellipse([X(x0 + sx), Y(y0 + sy), X(x0 + sx + 3), Y(y0 + sy + 3)], fill=WHITE)
    # dock + crane silhouettes
    rect(x0, y0 + 96, x1, y1, fill=(30, 30, 40))
    line(x0 + 30, y0 + 96, x0 + 30, y0 + 52, fill=(60, 60, 72), width=4)
    line(x0 + 30, y0 + 52, x0 + 66, y0 + 52, fill=(60, 60, 72), width=4)
    line(x0 + 66, y0 + 52, x0 + 66, y0 + 66, fill=(60, 60, 72), width=2)
    # corvette at the dock
    rect(x0 + 96, y0 + 82, x0 + 196, y0 + 98, fill=(120, 124, 132))
    rect(x0 + 120, y0 + 70, x0 + 150, y0 + 82, fill=(96, 100, 108))
    line(x0 + 132, y0 + 70, x0 + 132, y0 + 54, fill=(96, 100, 108), width=3)
    # explosion starburst on the corvette (jagged, bigger than a sun)
    ex, ey = x0 + 170, y0 + 66
    for ang in range(0, 360, 30):
        import math
        a = math.radians(ang)
        r = 22 if (ang // 30) % 2 == 0 else 13
        line(ex, ey, ex + r * math.cos(a), ey + r * math.sin(a),
             fill=ORANGE, width=3)
    d.ellipse([X(ex - 10), Y(ey - 10), X(ex + 10), Y(ey + 10)], fill=YELLOW)
    d.ellipse([X(ex + 6), Y(ey - 26), X(ex + 26), Y(ey - 6)], fill=(90, 90, 96))
    # two sea drones with dotted trails on the water
    for dx in (40, 70):
        line(x0 + dx - 22, y0 + 112, x0 + dx - 4, y0 + 112, fill=WHITE, width=1)
        d.ellipse([X(x0 + dx), Y(y0 + 108), X(x0 + dx + 12), Y(y0 + 116)],
                  fill=(10, 10, 16))
    # water lines
    for wy in (y0 + 104, y0 + 122):
        line(x0 + 8, wy, x1 - 8, wy, fill=(90, 120, 150), width=1)

def scene_bahrain(x0, y0, x1, y1):
    rect(x0, y0, x1, y1, fill=NAVY)
    for sx, sy in [(24, 18), (120, 14), (200, 26), (70, 36)]:
        d.ellipse([X(x0 + sx), Y(y0 + sy), X(x0 + sx + 3), Y(y0 + sy + 3)], fill=WHITE)
    # dotted missile arc from the top
    for t in range(0, 11):
        px = x0 + 40 + t * 12
        py = y0 + 90 - int(62 * (1 - ((t - 5) / 5.0) ** 2))
        d.ellipse([X(px), Y(py), X(px + 4), Y(py + 4)], fill=WHITE)
    # two storage tanks
    for tx in (36, 108):
        d.ellipse([X(x0 + tx), Y(y0 + 78), X(x0 + tx + 52), Y(y0 + 92)], fill=(150, 154, 160))
        rect(x0 + tx, y0 + 85, x0 + tx + 52, y0 + 122, fill=(120, 124, 132))
    # flame on the second tank + smoke
    d.polygon([(X(x0 + 118), Y(y0 + 78)), (X(x0 + 134), Y(y0 + 52)),
               (X(x0 + 150), Y(y0 + 78))], fill=ORANGE)
    d.polygon([(X(x0 + 124), Y(y0 + 78)), (X(x0 + 134), Y(y0 + 62)),
               (X(x0 + 144), Y(y0 + 78))], fill=YELLOW)
    d.ellipse([X(x0 + 122), Y(y0 + 30), X(x0 + 146), Y(y0 + 54)], fill=(90, 90, 96))
    # radar dish silhouette
    line(x0 + 186, y0 + 122, x0 + 186, y0 + 88, fill=(150, 154, 160), width=3)
    d.pieslice([X(x0 + 168), Y(y0 + 66), X(x0 + 204), Y(y0 + 102)],
               start=200, end=340, fill=(150, 154, 160))
    line(x0, y1 - 1, x1, y1 - 1, fill=(10, 10, 16), width=2)

panel(0, 6, "DYMER, UKRAINE", "EUROPE", "REPORTED",
      "Russia fires 186 drones; a Dymer block falls",
      "14 missing, 4 dead in Dymer; 161 of 186 downed. (Ukrainian Air Force)",
      "186", scene_dymer)
panel(1, 7, "GULF OF FINLAND", "EUROPE", "CONFIRMED",
      "Sparta II ablaze in the Gulf of Finland",
      "16 crew evacuated; Finland says Ukraine likely behind it. (Reuters)",
      "16", scene_sparta)
panel(2, 2, "BENGHAZI, LIBYA", "AFRICA", "REPORTED",
      "Sea drones hit a Russian warship at Benghazi",
      "Corvette Merkury hit; reports say she sank. A 2nd ship targeted. (BBC)",
      "2", scene_benghazi)
panel(3, 8, "BAHRAIN \u00b7 HORMUZ", "MIDEAST", "CLAIM",
      "Iran claims radar hits; Bahrain says 2 hurt",
      "IRGC claims 2 Patriot radars hit; Bahrain: site civil, 2 hurt. (Reuters)",
      "2", scene_bahrain)

# =========================================================
# 5. THE REST OF THE DAY — three region columns  (y 586..972)
# =========================================================
section_header(586, "THE REST OF THE DAY \u2014 28 MORE STORIES, BY REGION")

# (story_no, region, headline, summary)
COLUMNS = [
    ("EUROPE \u00b7 AFRICA \u2014 8", [
        (9,  "EUROPE",  "Denmark expels Russian attach\u00e9",
         "Plot to kill rapper Kyivstoner; 3 held (BBC)"),
        (10, "EUROPE",  "Belgium grounds all flights Monday",
         "Controllers join national strike (ST)"),
        (11, "EUROPE",  "France protests go on; 144 held",
         "Sixth weekend of marches (France 24)"),
        (12, "EUROPE",  "Istanbul marches over media seizure",
         "Thousands march as S\u00f6zc\u00fc TV seized (Le Monde)"),
        (13, "EUROPE",  "EU states agree Rwanda hubs",
         "Plus a 3% digital tax plan (El Pa\u00eds)"),
        (14, "EUROPE",  "Alcaraz wins first ATP Finals",
         "Beats Zverev 6\u20132, 7\u20136 in Turin (BBC Sport)"),
        (15, "AFRICA",  "Drones hit Khartoum homes, UN site",
         "Army blames Ethiopia (France 24)"),
        (16, "AFRICA",  "Nigeria boat capsizes; 24 dead",
         "Mourners\u2019 boat sinks; 24 rescued (Al Jazeera)"),
    ]),
    ("AMERICAS \u2014 9", [
        (17, "AMERICAS", "FBI crime database hacked",
         "Second breach in two months (BBC)"),
        (18, "AMERICAS", "Trump orders contractors to report",
         "Must flag Congress requests (Guardian)"),
        (19, "AMERICAS", "ICE arrests at Seattle airport",
         "Two detained; governor objects (Al Jazeera)"),
        (20, "AMERICAS", "Skubal agrees $450m Mets deal",
         "Richest pitcher deal in MLB history (Guardian)"),
        (21, "AMERICAS", "Wembanyama scores 50 in Spurs win",
         "50 points, 19 rebounds; Spurs 114\u201391 (BBC)"),
        (22, "AMERICAS", "Harden scores 51, passes Kobe",
         "26th career 50-point game (Guardian)"),
        (23, "AMERICAS", "KC Current win first NWSL title",
         "Beat Washington Spirit 2\u20131 (Al Jazeera)"),
        (24, "AMERICAS", "Palisades fire arsonist convicted",
         "Rinderknecht guilty; 2025 fire killed 12 (DW)"),
        (25, "AMERICAS", "Haiti, El Salvador to build prisons",
         "Three prisons agreed (Guardian)"),
    ]),
    ("ASIA-PACIFIC \u00b7 MIDEAST \u00b7 OCEANIA \u00b7 WORLD \u2014 11", [
        (26, "ASIA-PAC", "Hong Kong votes \u2014 turnout ~99%",
         "856 candidates contest 723 seats (SCMP)"),
        (27, "ASIA-PAC", "India declare 720/9 in New Zealand",
         "Record Test total; Rahul 136 (ESPN)"),
        (28, "ASIA-PAC", "Seoul minister quits over AI cheating",
         "Education chief resigns; exam chaos (BBC)"),
        (29, "WORLD",    "One-shot CRISPR cuts cholesterol 52%",
         "Gene therapy points to single treatment"),
        (30, "MIDEAST",  "Israeli strikes kill 3 in Gaza",
         "Food-aid van hit; one killed at Deir al-Balah"),
        (31, "MIDEAST",  "Houthis say they hit Saudi refinery",
         "Rabigh attacked; Saudi intercepts missile (ST)"),
        (32, "MIDEAST",  "Iran begins rationing electricity",
         "Scheduled blackouts resume from Sunday (BBC)"),
        (33, "MIDEAST",  "Basra power station fire kills 4",
         "Hartha blaze injures about 30 (Reuters)"),
        (34, "ASIA-PAC", "Cikande factory fire: 3 dead, 36 missing",
         "Search goes on after Saturday blaze (BBC)"),
        (35, "OCEANIA",  "Cyclone Xavier weakens near Cook Is.",
         "Everyone on Nassau safe, PM says (RNZ)"),
        (36, "WORLD",    "AI \u2018proves\u2019 Riemann hypothesis",
         "Claim may take years to check (NPR)"),
    ]),
]
COLW, CGAP = 317, 12
CY0, CY1 = 604, 972
for ci, (chead, stories) in enumerate(COLUMNS):
    cx0 = MX + ci * (COLW + CGAP)
    cx1 = cx0 + COLW
    # column header: colour bar + title
    rect(cx0, CY0, cx1, CY0 + 4, fill=INK)
    fit(chead, SANS_B(13), COLW, f"colhead-{ci}")
    text(cx0, CY0 + 8, chead, SANS_B(13), fill=INK)
    line(cx0, CY0 + 26, cx1, CY0 + 26, fill=GREY, width=1)
    n = len(stories)
    row_h = (CY1 - (CY0 + 34)) / n
    for ri, (no, region, head, summ) in enumerate(stories):
        ry = CY0 + 34 + ri * row_h
        # number disc
        d.ellipse([X(cx0), Y(ry + 2), X(cx0 + 16), Y(ry + 18)],
                  fill=REGION[region])
        text(cx0 + 8, ry + 4, str(no), SANS_B(11), fill=WHITE, anchor="ma")
        tx = cx0 + 22
        tw = COLW - 22
        hlines = wrap(head, SANS_B(13), tw, 2, f"col-head-{no}")
        for j, ln in enumerate(hlines):
            text(tx, ry + j * 15, ln, SANS_B(13), fill=INK)
        sy = ry + len(hlines) * 15 + 1
        # summary must fit one line; headline wrap keeps total inside the row
        fit(summ, SANS(12), tw, f"col-sum-{no}")
        text(tx, sy, summ, SANS(12), fill=(60, 60, 58))
        assert sy + 13 <= ry + row_h + 1, \
            f"ROW OVERFLOW story {no}: sy {sy:.1f} row ends {ry + row_h:.1f}"
        if ri < n - 1:
            line(cx0, ry + row_h - 5, cx1, ry + row_h - 5,
                 fill=(214, 210, 198), width=1)

# =========================================================
# 6. FOOTER  (y 978..1024)
# =========================================================
foot = ("Sources: Reuters, BBC, AFP, AP, Al Jazeera, The Guardian, SCMP, ESPN, France 24 \u2014 "
        "wires read to 01:00 UTC Mon 23 Nov 2026. Scenes are drawn illustrations of reported events, not photographs.")
flines = wrap(foot, SANS(11), 1024 - 2 * MX, 2, "footer")
for j, ln in enumerate(flines):
    text(MX, 973 + j * 13, ln, SANS(11), fill=GREY)
rect(0, 1000, 1024, 1024, fill=BAND)
text(MX, 1007, "THE WORLD IN ONE DAY", SANS_B(11), fill=WHITE)
text(1024 - MX, 1007, "SUNDAY 22 NOVEMBER 2026 \u00b7 ONE PAGE",
     SANS_B(11), fill=WHITE, anchor="ra")

# =========================================================
# SAVE — deterministic downscale
# =========================================================
out_path = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
small = img.resize((1024, 1024), Image.LANCZOS)
small.save(out_path, "PNG", optimize=True)
print("wrote", out_path, small.size)
