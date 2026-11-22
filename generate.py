#!/usr/bin/env python3
"""One-day newspaper front page: Saturday 21 November 2026.
Built fresh from the story list in the brief. Deterministic PIL render,
1024x1024, cream paper, flat vector illustrations. No photos, no gen-AI."""
from PIL import Image, ImageDraw, ImageFont
import textwrap, os

W, H = 1024, 1024
CREAM = (248, 242, 223)
PAPER2 = (250, 245, 230)
INK = (26, 24, 20)
RED = (178, 34, 30)
REDD = (140, 22, 20)
GREY = (90, 86, 76)
LINE = (60, 55, 45)
SKY = (214, 228, 238)
LAND = (196, 210, 222)
LANDLINE = (140, 160, 180)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIFB = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIFI = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANSB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

def F(p, s):
    return ImageFont.truetype(p, s)

def wrap(draw, text, font, width):
    """Greedy word wrap by pixel width."""
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if draw.textlength(t, font=font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def para(draw, x, y, text, font, width, fill=INK, lh=None):
    lh = lh or int(font.size * 1.22)
    for ln in wrap(draw, text, font, width):
        draw.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)
# paper frame
d.rectangle([6, 6, W - 7, H - 7], outline=INK, width=2)
d.rectangle([10, 10, W - 11, H - 11], outline=(150, 140, 118), width=1)

MX = 24  # margin
RX = W - MX

# ---------- masthead ----------
d.text((W // 2, 18), "ONE DAY  •  ONE PAGE  •  35 STORIES  •  EVERY ONE CHECKED",
       font=F(SANSB, 11), fill=GREY, anchor="mt")
d.text((W // 2, 34), "THE WORLD IN ONE DAY", font=F(SERIFB, 52), fill=RED, anchor="mt")
d.line([(MX, 92), (RX, 92)], fill=RED, width=2)
d.text((W // 2, 98), "Saturday 21 November 2026", font=F(SERIFB, 40), fill=INK, anchor="mt")
d.text((W // 2, 142), "COP31 ends day 13 with no deal  •  Three missiles downed over Riyadh  •  M6.7 quake shakes Peru",
       font=F(SANS, 13), fill=INK, anchor="mt")

# ---------- strip of 6 numbers ----------
stats = [("3", "MISSILES DOWNED\nOVER RIYADH"), ("M6.7", "QUAKE IN PERU\nJUNIN, 00:09 UTC"),
         ("146", "SAFE AFTER\nEMERGENCY LANDING"), ("$58,983", "BITCOIN, DOWN\n3.9% IN 24 HOURS"),
         ("124*", "RAHUL IN\nWELLINGTON"), ("DAY 13", "COP31 OVERTIME\nIN ANTALYA")]
sy, sh, sw = 166, 50, (RX - MX - 5 * 6) // 6
for i, (num, lab) in enumerate(stats):
    x0 = MX + i * (sw + 6)
    d.rectangle([x0, sy, x0 + sw, sy + sh], outline=LINE, width=1, fill=PAPER2)
    d.text((x0 + sw // 2, sy + 3), num, font=F(SERIFB, 19), fill=RED, anchor="mt")
    for j, ln in enumerate(lab.split("\n")):
        d.text((x0 + sw // 2, sy + 26 + j * 11), ln, font=F(SANSB, 8), fill=INK, anchor="mt")

# ---------- region bar (must sum to 35) ----------
regions = [("Europe", 5, (178, 34, 30)), ("Asia", 9, (42, 92, 140)),
           ("Middle East", 5, (196, 128, 30)), ("Africa", 2, (52, 120, 70)),
           ("Americas", 10, (90, 60, 130)), ("Oceania", 3, (20, 130, 130)),
           ("Global", 1, (120, 110, 100))]
by, bh = 224, 30
d.text((MX, by), "STORIES BY REGION", font=F(SANSB, 11), fill=INK)
d.text((RX, by), "TOTAL  35", font=F(SANSB, 11), fill=RED, anchor="rt")
bx, bw = MX, RX - MX
x = bx
for name, n, col in regions:
    wseg = bw * n / 35.0
    d.rectangle([x, by + 15, x + wseg, by + 15 + 13], fill=col, outline=CREAM)
    x += wseg
lx = MX
for name, n, col in regions:
    d.rectangle([lx, by + 31, lx + 8, by + 31 + 8], fill=col)
    d.text((lx + 11, by + 30), f"{name} {n}", font=F(SANS, 10), fill=INK)
    lx += 11 + d.textlength(f"{name} {n}", font=F(SANS, 10)) + 12

# ---------- timeline strip: THE DAY IN UTC ----------
ty = 268
d.text((MX, ty), "THE DAY IN UTC", font=F(SANSB, 11), fill=RED)
d.line([(MX, ty + 22), (RX, ty + 22)], fill=LINE, width=1)
ticks = [("00:09", "Peru quake M6.7", 0.04), ("02:00", "Riyadh blasts", 0.22),
         ("18:24", "BepiColombo burn", 0.58), ("EVENING", "Russell fastest, Vegas", 0.80),
         ("ALL DAY", "COP31, day 13", 0.96)]
for t, lab, frac in ticks:
    cx = MX + int(frac * (RX - MX))
    d.ellipse([cx - 4, ty + 18, cx + 4, ty + 26], fill=RED)
    d.text((cx, ty + 30), t, font=F(SANSB, 10), fill=INK, anchor="mt")
    d.text((cx, ty + 42), lab, font=F(SANS, 9), fill=GREY, anchor="mt")

# ---------- panels ----------
def badge(x, y, n, r=11):
    d.ellipse([x - r, y - r, x + r, y + r], fill=RED, outline=(255, 255, 255), width=2)
    d.text((x, y - r + 1), str(n), font=F(SANSB, 12), fill=(255, 255, 255), anchor="mt")

def chip(x, y, s):
    f = F(SANSB, 8)
    wch = d.textlength(s, font=f) + 8
    d.rectangle([x - wch, y, x, y + 12], fill=(235, 228, 205), outline=LINE)
    d.text((x - wch // 2, y + 1), s, font=f, fill=GREY, anchor="mt")

def hero_art(kind, x0, y0, w, h):
    """Flat vector illustration inside a hero panel."""
    if kind == "cop31":
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(198, 222, 196))
        cx, cy, r = x0 + w // 2, y0 + h // 2 + 4, 34
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 130, 180), outline=(30, 80, 60), width=2)
        d.ellipse([cx - r, cy - 12, cx + r, cy + 12], outline=(255, 255, 255), width=1)
        d.ellipse([cx - 22, cy - r, cx + 22, cy + r], outline=(255, 255, 255), width=1)
        d.pieslice([cx - r, cy - r, cx + r, cy + r], 200, 330, fill=(90, 160, 90))
        d.pieslice([cx - r, cy - r, cx + r, cy + r], 20, 90, fill=(90, 160, 90))
        d.ellipse([cx + r - 6, cy - r - 2, cx + r + 16, cy - r + 20], fill=(240, 200, 60), outline=(200, 150, 20), width=1)
        for i, fx in enumerate([x0 + 14, x0 + w - 34]):
            d.polygon([(fx, y0 + h - 12), (fx, y0 + 18), (fx + 20, y0 + 26), (fx, y0 + 34)], fill=RED if i == 0 else (42, 92, 140))
    elif kind == "riyadh":
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(38, 52, 86))
        for sx, sy2 in [(x0 + 30, y0 + 14), (x0 + 90, y0 + 8), (x0 + 160, y0 + 18), (x0 + 230, y0 + 10), (x0 + 280, y0 + 20)]:
            d.ellipse([sx, sy2, sx + 2, sy2 + 2], fill=(255, 255, 255))
        for i, (mx, my) in enumerate([(x0 + 60, y0 + 55), (x0 + 160, y0 + 40), (x0 + 255, y0 + 58)]):
            d.arc([mx - 55, my - 45, mx + 55, my + 45], 200, 340, fill=(255, 210, 90), width=2)
            d.ellipse([mx - 4, my - 4, mx + 4, my + 4], fill=(255, 120, 40), outline=(255, 220, 120), width=1)
            for k in range(6):
                import math
                a = k * 60 + i * 20
                d.line([(mx, my), (mx + 10 * math.cos(math.radians(a)), my + 10 * math.sin(math.radians(a)))], fill=(255, 180, 60), width=2)
        d.rectangle([x0, y0 + h - 16, x0 + w, y0 + h], fill=(20, 28, 50))
        for bx2, bh2 in [(x0 + 20, 10), (x0 + 60, 14), (x0 + 110, 8), (x0 + 170, 13), (x0 + 230, 9), (x0 + 275, 12)]:
            d.rectangle([bx2, y0 + h - 16 - bh2, bx2 + 22, y0 + h - 16], fill=(16, 22, 42))
    elif kind == "peru":
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(232, 214, 178))
        d.polygon([(x0, y0 + h - 34), (x0 + 60, y0 + 18), (x0 + 120, y0 + h - 34)], fill=(150, 130, 105))
        d.polygon([(x0 + 100, y0 + h - 34), (x0 + 180, y0 + 8), (x0 + 260, y0 + h - 34)], fill=(130, 110, 88))
        d.polygon([(x0 + 60, y0 + 18), (x0 + 72, y0 + 34), (x0 + 48, y0 + 34)], fill=(255, 255, 255))
        d.polygon([(x0 + 180, y0 + 8), (x0 + 194, y0 + 26), (x0 + 166, y0 + 26)], fill=(255, 255, 255))
        pts = [(x0 + 20 + i * 22, y0 + h - 20 - (14 if i % 2 else 4)) for i in range(14)]
        d.line(pts, fill=RED, width=2)
        crack = [(x0 + w // 2, y0 + h - 34), (x0 + w // 2 - 8, y0 + h - 22), (x0 + w // 2 + 6, y0 + h - 12), (x0 + w // 2 - 4, y0 + h)]
        d.line(crack, fill=(60, 45, 30), width=3)

def small_art(kind, x0, y0, w, h):
    if kind == "kryvyi":
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(226, 214, 196))
        d.rectangle([x0 + 12, y0 + h - 16, x0 + 34, y0 + h], fill=(120, 110, 95))
        d.rectangle([x0 + 40, y0 + h - 22, x0 + 66, y0 + h], fill=(140, 128, 110))
        d.polygon([(x0 + 100, y0 + 8), (x0 + 116, y0 + 22), (x0 + 132, y0 + 8), (x0 + 124, y0 + 26), (x0 + 108, y0 + 26)], fill=(255, 140, 40))
        d.ellipse([x0 + 108, y0 + 4, x0 + 124, y0 + 18], fill=(255, 200, 80))
    elif kind == "bridge":
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=SKY)
        d.rectangle([x0, y0 + h - 12, x0 + w, y0 + h], fill=(90, 140, 180))
        d.rectangle([x0 + 10, y0 + 16, x0 + w - 10, y0 + 22], fill=(120, 110, 95))
        d.line([(x0 + 30, y0 + 16), (x0 + 30, y0 + 4)], fill=INK, width=2)
        d.line([(x0 + w - 30, y0 + 16), (x0 + w - 30, y0 + 4)], fill=INK, width=2)
        d.line([(x0 + 30, y0 + 4), (x0 + w // 2, y0 + 16)], fill=INK, width=1)
        d.line([(x0 + w - 30, y0 + 4), (x0 + w // 2, y0 + 16)], fill=INK, width=1)
        d.line([(x0 + w // 2 - 8, y0 + 16), (x0 + w // 2 + 8, y0 + 16)], fill=RED, width=3)
    elif kind == "drone":
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(222, 230, 238))
        d.arc([x0 + 20, y0 - 30, x0 + w - 20, y0 + h + 30], 0, 180, fill=(140, 160, 180), width=1)
        d.arc([x0 + 40, y0 - 10, x0 + w - 40, y0 + h + 10], 0, 180, fill=(140, 160, 180), width=1)
        cx, cy = x0 + w // 2, y0 + h // 2
        d.ellipse([cx - 34, cy - 5, cx + 34, cy + 5], fill=(70, 75, 85))
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(50, 55, 65))
        d.rectangle([cx - 52, cy - 2, cx - 34, cy + 2], fill=(70, 75, 85))
        d.rectangle([cx + 34, cy - 2, cx + 52, cy + 2], fill=(70, 75, 85))
        d.ellipse([cx - 58, cy - 7, cx - 46, cy + 7], fill=(150, 155, 165))
        d.ellipse([cx + 46, cy - 7, cx + 58, cy + 7], fill=(150, 155, 165))
    elif kind == "atom":
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(228, 222, 200))
        cx, cy = x0 + w // 2, y0 + h // 2
        d.ellipse([cx - 22, cy - 12, cx + 22, cy + 12], outline=(60, 90, 140), width=2)
        d.ellipse([cx - 12, cy - 22, cx + 12, cy + 22], outline=(60, 90, 140), width=2)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
        d.ellipse([cx + 16, cy - 8, cx + 22, cy - 2], fill=(60, 90, 140))
    elif kind == "server":
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(220, 226, 232))
        for i in range(3):
            rx0 = x0 + 14 + i * 56
            d.rectangle([rx0, y0 + 6, rx0 + 46, y0 + h - 6], fill=(50, 60, 75), outline=(20, 25, 35), width=1)
            for j in range(3):
                d.rectangle([rx0 + 5, y0 + 10 + j * 10, rx0 + 30, y0 + 16 + j * 10], fill=(90, 160, 110))
                d.ellipse([rx0 + 35, y0 + 11 + j * 10, rx0 + 41, y0 + 17 + j * 10], fill=(255, 200, 60))
    elif kind == "flags":
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(238, 232, 214))
        d.rectangle([x0 + 18, y0 + 8, x0 + 78, y0 + h - 8], fill=RED)
        for sx, sy2 in [(x0 + 28, y0 + 14), (x0 + 42, y0 + 12), (x0 + 52, y0 + 20), (x0 + 42, y0 + 28), (x0 + 28, y0 + 26)]:
            d.ellipse([sx, sy2, sx + 5, sy2 + 5], fill=(255, 220, 60))
        d.rectangle([x0 + 100, y0 + 8, x0 + 160, y0 + h - 8], fill=(255, 255, 255), outline=LINE)
        d.ellipse([x0 + 118, y0 + 12, x0 + 142, y0 + h - 12], fill=RED)
    elif kind == "plane":
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=SKY)
        d.ellipse([x0 + 30, y0 + 10, x0 + 150, y0 + 26], fill=(255, 255, 255))
        cx, cy = x0 + w // 2, y0 + h // 2 + 2
        d.ellipse([cx - 55, cy - 7, cx + 55, cy + 7], fill=(230, 235, 240), outline=(90, 100, 110), width=1)
        d.polygon([(cx + 30, cy - 6), (cx + 58, cy - 20), (cx + 66, cy - 6)], fill=(200, 40, 40))
        d.polygon([(cx - 10, cy + 4), (cx + 10, cy + 18), (cx + 22, cy + 4)], fill=(200, 40, 40))
        d.line([(cx - 55, cy + 8), (cx + 55, cy + 8)], fill=(60, 60, 60), width=2)
        d.rectangle([x0, y0 + h - 6, x0 + w, y0 + h], fill=(120, 115, 100))
    elif kind == "ai":
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(224, 232, 226))
        cx, cy = x0 + w // 2, y0 + h // 2
        d.rounded_rectangle([cx - 26, cy - 18, cx + 26, cy + 18], radius=8, fill=(240, 244, 248), outline=(60, 90, 140), width=2)
        d.ellipse([cx - 14, cy - 6, cx - 6, cy + 2], fill=(60, 90, 140))
        d.ellipse([cx + 6, cy - 6, cx + 14, cy + 2], fill=(60, 90, 140))
        d.line([(cx - 8, cy + 10), (cx + 8, cy + 10)], fill=(60, 90, 140), width=2)
        d.line([(cx - 30, cy - 24), (cx - 26, cy - 18)], fill=(60, 90, 140), width=2)
        d.line([(cx + 30, cy - 24), (cx + 26, cy - 18)], fill=(60, 90, 140), width=2)
    elif kind == "bitcoin":
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(250, 238, 210))
        cx, cy = x0 + w // 2, y0 + h // 2
        d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=(247, 147, 26), outline=(200, 110, 10), width=2)
        d.text((cx, cy - 13), "B", font=F(SANSB, 26), fill=(255, 255, 255), anchor="mt")
        d.line([(x0 + w - 46, y0 + h - 10), (x0 + w - 8, y0 + h - 10)], fill=(200, 110, 10), width=2)
    elif kind == "f1":
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(40, 44, 52))
        for r in range(2):
            for c in range(8):
                if (r + c) % 2 == 0:
                    d.rectangle([x0 + 8 + c * 10, y0 + 6 + r * 10, x0 + 18 + c * 10, y0 + 16 + r * 10], fill=(255, 255, 255))
        d.rectangle([x0 + 100, y0 + 8, x0 + 175, y0 + 30], fill=RED)
        d.text((x0 + 137, y0 + 9), "1:34.041", font=F(SANSB, 13), fill=(255, 255, 255), anchor="mt")

heroes = [
    (1, "cop31", "CLIMATE TALKS DRAG INTO DAY 13",
     "COP31 in Antalya ends with no deal. A third draft with no fossil fuels splits ~200 nations.",
     "Reuters"),
    (2, "riyadh", "THREE MISSILES DOWNED OVER RIYADH",
     "A Saudi-led coalition intercepts three Houthi missiles on a third night of warnings. Two blasts heard ~02:00; no casualties.",
     "AP"),
    (3, "peru", "M6.7 QUAKE SHAKES PERU",
     "Junin / Carhuamayo, 00:09 UTC, 108 km deep. No deaths, no tsunami reported.",
     "USGS"),
]
hy, hh, hw, hg = 322, 178, 320, 84
for i, (n, kind, head, body, src) in enumerate(heroes):
    x0 = MX + i * (hw + 8)
    d.rectangle([x0, hy, x0 + hw, hy + hh], outline=LINE, width=1, fill=(255, 255, 255))
    hero_art(kind, x0 + 1, hy + 1, hw - 2, hg)
    badge(x0 + 16, hy + 16, n)
    ty2 = hy + hg + 6
    ty2 = para(d, x0 + 8, ty2, head, F(SERIFB, 15), hw - 16, lh=17)
    para(d, x0 + 8, ty2 + 2, body, F(SANS, 10), hw - 16, lh=12)
    chip(x0 + hw - 6, hy + hh - 18, src)

smalls = [
    (4, "kryvyi", "DOUBLE-TAP STRIKE ON KRYVYI RIH", "Russian attack kills 2 and injures 42.", "Reuters"),
    (5, "bridge", "ZELENSKY: CRIMEA BRIDGE \u2018WILL NOT STAY\u2019", "Speaking to NBC in Kyiv, the president vows it will not stand.", "NBC"),
    (6, "drone", "IRAN CLAIMS IT DOWNED A US DRONE", "Tehran says it shot down an MQ-9 over Hormuz \u2014 its 58th such claim. Washington has not confirmed.", "AFP"),
    (7, "atom", "IRAN: URANIUM STAYS AT HOME", "Tehran says its stockpile remains in the country, seeking a \u2018fair solution\u2019.", "Reuters"),
    (8, "server", "TRUMP VOWS TAX ON FOREIGN DATA CENTRES", "Washington: levies promised on overseas data centres, with no details yet.", "AP"),
    (9, "flags", "CHINA TELLS JAPAN TO \u2018CORRECT\u2019 TAIWAN WORDS", "Beijing demands a correction. Tokyo says its position is unchanged.", "Reuters"),
    (10, "plane", "146 SAFE AS JET LANDS IN DAVAO", "Air Niugini 767 makes an emergency landing in the Philippines; all aboard survive.", "AFP"),
    (11, "ai", "AUSTRALIA AND CHINA TO TALK AI", "Canberra: Albanese ends an 11-day trip with a deal to discuss AI.", "Reuters"),
    (12, "bitcoin", "BITCOIN SLIPS BELOW $59,000", "The coin falls 3.9% in 24 hours to $58,983.", "Markets"),
    (13, "f1", "RUSSELL FASTEST IN WET VEGAS PRACTICE", "George Russell clocks 1:34.041; Verstappen takes pole in Las Vegas.", "F1"),
]
sw2, sh2 = 190, 114
for row in range(2):
    for col in range(5):
        n, kind, head, body, src = smalls[row * 5 + col]
        x0 = MX + col * (sw2 + 6)
        y0 = 486 + row * (sh2 + 8)
        d.rectangle([x0, y0, x0 + sw2, y0 + sh2], outline=LINE, width=1, fill=(255, 255, 255))
        small_art(kind, x0 + 1, y0 + 1, sw2 - 2, 42)
        badge(x0 + 13, y0 + 13, n, r=10)
        ty3 = para(d, x0 + 6, y0 + 48, head, F(SERIFB, 11), sw2 - 12, lh=12)
        para(d, x0 + 6, ty3 + 1, body, F(SANS, 9), sw2 - 12, lh=11)
        chip(x0 + sw2 - 5, y0 + sh2 - 15, src)

# ---------- bottom: map + ALSO list ----------
by0, bh0 = 730, 176
map_x0, map_w = MX, 472
also_x0, also_w = MX + 480, RX - (MX + 480)
d.rectangle([map_x0, by0, map_x0 + map_w, by0 + bh0], outline=LINE, width=1, fill=(255, 255, 255))
d.rectangle([also_x0, by0, also_x0 + also_w, by0 + bh0], outline=LINE, width=1, fill=(255, 255, 255))
d.text((map_x0 + 8, by0 + 5), "WHERE IT HAPPENED", font=F(SANSB, 12), fill=RED)
d.text((map_x0 + map_w - 8, by0 + 5), "PINS 1\u201313 MATCH THE STORIES", font=F(SANS, 9), fill=GREY, anchor="rt")
d.text((also_x0 + 8, by0 + 5), "ALSO ON SATURDAY 21 NOVEMBER \u2014 22 MORE STORIES",
       font=F(SANSB, 11), fill=INK)

# coarse world map (lon/lat polygons, equirectangular)
MAPX, MAPY, MAPW, MAPH = map_x0 + 8, by0 + 26, map_w - 16, 118
def mx(lon):
    return MAPX + (lon + 170) / 360.0 * MAPW
def my(lat):
    return MAPY + (75 - lat) / 130.0 * MAPH
NA = [(-168,66),(-140,70),(-125,72),(-110,73),(-95,80),(-85,70),(-75,72),(-65,60),(-55,52),(-60,47),(-70,42),(-75,35),(-80,32),(-85,30),(-90,21),(-97,16),(-105,20),(-115,28),(-125,40),(-125,49),(-140,60),(-155,58),(-165,60)]
GL = [(-55,60),(-45,60),(-40,65),(-30,68),(-20,70),(-30,76),(-55,76),(-60,70)]
SA = [(-80,10),(-75,5),(-70,0),(-60,-5),(-50,-5),(-40,-10),(-35,-15),(-40,-25),(-50,-30),(-60,-35),(-65,-40),(-70,-45),(-72,-52),(-75,-40),(-75,-25),(-80,-15),(-80,-5)]
EU = [(-10,36),(-9,43),(-2,48),(0,50),(5,53),(8,57),(10,59),(18,56),(21,55),(24,58),(28,60),(30,62),(25,65),(20,70),(15,68),(10,64),(5,60),(5,58),(-2,57),(-5,50),(-9,43),(-10,37)]
AF = [(-17,15),(-15,25),(-10,30),(-5,35),(0,36),(10,37),(15,32),(20,32),(30,31),(32,28),(35,22),(38,18),(42,12),(48,11),(51,10),(48,0),(40,-10),(35,-20),(32,-28),(28,-33),(20,-35),(15,-30),(12,-18),(12,-8),(9,0),(9,4),(-8,4),(-13,8),(-17,12)]
AS = [(30,62),(40,68),(50,70),(60,70),(70,72),(80,73),(90,75),(100,77),(110,74),(120,73),(130,72),(140,72),(150,70),(160,66),(170,66),(178,65),(170,60),(162,58),(158,52),(150,45),(142,40),(140,35),(135,33),(130,31),(127,35),(122,38),(120,32),(115,25),(110,20),(108,12),(105,8),(100,6),(98,12),(95,16),(92,21),(88,22),(85,20),(80,15),(77,8),(75,12),(72,20),(68,23),(66,25),(61,25),(58,26),(56,27),(52,28),(50,30),(48,30),(44,29),(42,25),(40,20),(38,18),(35,28),(36,36),(33,36),(30,36),(28,40),(28,45),(30,50),(28,55),(30,60)]
AU = [(113,-22),(114,-30),(115,-35),(120,-34),(124,-33),(129,-32),(132,-32),(135,-35),(138,-35),(140,-38),(145,-38),(150,-37),(153,-32),(153,-27),(150,-22),(146,-19),(142,-15),(142,-11),(137,-12),(135,-15),(132,-12),(130,-13),(126,-14),(122,-17),(118,-20),(113,-22)]
JP = [(130,31),(133,34),(137,35),(140,38),(141,41),(142,44),(140,42),(138,38),(135,34),(132,33)]
IDN = [(95,5),(100,0),(105,-5),(110,-7),(115,-8),(120,-10),(125,-8),(130,-4),(135,-3),(138,-6),(132,-8),(125,-9),(118,-8),(112,-7),(105,-5),(100,-2),(96,4)]
PH = [(120,18),(122,16),(124,12),(126,8),(125,6),(122,8),(120,11),(120,15)]
NZ = [(167,-45),(170,-42),(174,-40),(176,-38),(178,-37),(175,-40),(172,-43),(168,-46)]
for poly in (NA, GL, SA, EU, AF, AS, AU, JP, IDN, PH, NZ):
    d.polygon([(mx(lo), my(la)) for lo, la in poly], fill=LAND, outline=LANDLINE)

# pins: (n, lon, lat, dx, dy)
pins = [(1, 30.7, 36.9, 0, -4), (2, 46.7, 24.7, -7, 5), (3, -75.9, -11.2, 0, 0),
        (4, 33.4, 47.9, 9, 9), (5, 30.5, 50.4, -7, -7), (6, 56.5, 26.5, 9, 7),
        (7, 51.4, 35.7, -3, -9), (8, -77.0, 38.9, -9, 5), (9, 116.4, 39.9, 0, 0),
        (10, 125.6, 7.1, 0, 0), (11, 149.1, -35.3, 0, 0), (12, -74.0, 40.7, 11, -7),
        (13, -115.1, 36.2, 0, 0)]
for n, lon, lat, dx, dy in pins:
    cx, cy = mx(lon) + dx, my(lat) + dy
    r = 8
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED, outline=(255, 255, 255), width=1)
    d.text((cx, cy - 6), str(n), font=F(SANSB, 9), fill=(255, 255, 255), anchor="mt")
d.text((map_x0 + 8, by0 + bh0 - 16),
       "HOW WE CHECKED: every story is dated 21 Nov 2026; CLAIM means unconfirmed; sources on each panel.",
       font=F(SANS, 9), fill=GREY)

# ALSO list, two columns
also = [
    (14, "Rahul 124* \u2014 India 344/2 v 368, Wellington"),
    (15, "BepiColombo reaches Mercury, 19:24 CET"),
    (16, "Rutte in Warsaw for NATO talks"),
    (17, "Funeral boat sinks, Bayelsa \u2014 4+ dead"),
    (18, "ANC falls to 31%, worst since 1994"),
    (19, "Freight train derails in Sejong, 5/21 cars"),
    (20, "Kim visits a factory in Pyongyang"),
    (21, "Taipei passes its budget"),
    (22, "Bangkok unveils an arsenic plan"),
    (23, "SCO forum meets in New Delhi"),
    (24, "Myanmar faces fresh sanctions"),
    (25, "Starc takes 7/58 \u2014 Ashes, Perth"),
    (26, "Israeli strikes on Gaza kill 6"),
    (27, "Houthis threaten Jeddah; Hodeidah hit"),
    (28, "ATP semis in Turin: Medvedev v Zverev"),
    (29, "Youth climate hearing in Vancouver"),
    (30, "Roundup settlement: $7.25bn, Missouri"),
    (31, "Texas execution takes 63 minutes"),
    (32, "Palisades fire verdict \u2014 12 dead, LA"),
    (33, "First US measles death of 2026, Virginia"),
    (34, "Vance: Iran strike is Trump\u2019s call"),
    (35, "Denmark expels Russian defence attache"),
]
af = F(SANS, 10)
ay = by0 + 26
colw = (also_w - 16) // 2
for idx, (n, txt) in enumerate(also):
    col = idx // 11
    row = idx % 11
    x = also_x0 + 8 + col * colw
    y = ay + row * 13
    d.text((x, y), f"{n}.", font=F(SANSB, 10), fill=RED)
    d.text((x + 20, y), txt, font=af, fill=INK)

# ---------- DATE CHECK + footer ----------
dy0 = 914
d.rectangle([MX, dy0, RX, dy0 + 58], outline=RED, width=2, fill=(255, 240, 235))
d.text((MX + 8, dy0 + 4), "DATE CHECK \u2014 WHAT WE LEFT OUT, AND WHY", font=F(SANSB, 11), fill=RED)
para(d, MX + 8, dy0 + 20,
     "Left out on purpose: Wall Street\u2019s slide into correction; Russia\u2019s strike on Kyiv\u2019s bridge; a missile landing in Poland; the UK\u2013EU reset deal (100,000 visas); Cyclone Akvan\u2019s landfall \u2014 all Friday 20 Nov \u2014 and Voyager 1\u2019s light-day (18 Nov). Not yet confirmed when drawn: the final COP31 text; BepiColombo\u2019s Mercury orbit insertion.",
     F(SANS, 10), RX - MX - 16, lh=12)
d.text((W // 2, 980), "Every story here happened, or was first reported, on Saturday 21 November 2026.",
       font=F(SERIFB, 12), fill=INK, anchor="mt")
d.text((W // 2, 996), "Sources: Reuters  •  AP  •  AFP  •  USGS  •  NBC  •  ESA  •  F1  •  Market data",
       font=F(SANS, 9), fill=GREY, anchor="mt")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, optimize=True)
print("saved", out, os.path.getsize(out), "bytes")
