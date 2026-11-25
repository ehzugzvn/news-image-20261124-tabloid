#!/usr/bin/env python3
"""TABLOID variant — news-image-20261124. Draws entry.png (1024x1024) with PIL.
Tabloid front page: giant date masthead, dominant Hormuz map, 3 more leads,
tier-2 grid, large-type briefs, day-in-numbers, UTC timeline, date-check strip.
All facts from STORIES.md (verified 24 Nov 2026)."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BASE = os.path.dirname(os.path.abspath(__file__))
F_B = os.path.join(BASE, "fonts", "LiberationSans-Bold.ttf")
F_R = os.path.join(BASE, "fonts", "LiberationSans-Regular.ttf")
F_SB = os.path.join(BASE, "fonts", "LiberationSerif-Bold.ttf")

def font(path, size):
    return ImageFont.truetype(path, size)

# palette
PAPER = (253, 251, 245)
INK = (12, 12, 12)
RED = (200, 16, 46)
DRED = (150, 8, 30)
BLUE = (11, 61, 145)
SEA = (127, 179, 213)
SEA2 = (168, 204, 232)
LAND = (232, 220, 192)
LAND2 = (214, 196, 158)
GOLD = (212, 160, 23)
GREY = (90, 90, 90)
LGREY = (230, 228, 222)
GREEN = (27, 120, 55)
ORANGE = (214, 110, 10)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def txt(x, y, s, f, fill=INK, anchor="la"):
    d.text((x, y), s, font=f, fill=fill, anchor=anchor)

def wrap(s, f, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def para(x, y, s, f, maxw, lh, fill=INK):
    for ln in wrap(s, f, maxw):
        d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y

def badge(x, y, label, color, fg=(255, 255, 255), fsize=13):
    f = font(F_B, fsize)
    w_ = int(d.textlength(label, font=f)) + 14
    d.rounded_rectangle([x, y, x + w_, y + 20], radius=4, fill=color)
    d.text((x + 7, y + 3), label, font=f, fill=fg)
    return w_

def flame(x, y, s):
    # simple flame: orange outer, yellow inner
    d.polygon([(x, y + s), (x + s * 0.25, y + s * 0.35), (x + s * 0.5, y + s * 0.55),
               (x + s * 0.62, y), (x + s * 0.8, y + s * 0.5), (x + s, y + s)],
              fill=ORANGE)
    d.polygon([(x + s * 0.3, y + s), (x + s * 0.45, y + s * 0.6),
               (x + s * 0.6, y + s * 0.75), (x + s * 0.72, y + s)],
              fill=GOLD)

def tanker(x, y, w_, h_, hull=RED):
    d.rectangle([x, y, x + w_, y + h_], fill=hull, outline=INK, width=2)
    d.rectangle([x + w_ * 0.62, y - h_ * 0.55, x + w_ * 0.88, y], fill=(255, 255, 255),
                outline=INK, width=2)
    d.rectangle([x + w_ * 0.10, y - h_ * 0.28, x + w_ * 0.30, y], fill=(255, 255, 255),
                outline=INK, width=2)

def mine(x, y, r):
    d.ellipse([x - r, y - r, x + r, y + r], fill=INK)
    for ang in range(0, 360, 45):
        import math
        a = math.radians(ang)
        d.line([x + r * 0.7 * math.cos(a), y + r * 0.7 * math.sin(a),
                x + r * 1.5 * math.cos(a), y + r * 1.5 * math.sin(a)],
               fill=INK, width=2)

# ============ MASTHEAD — date is the LARGEST element ============
d.rectangle([0, 0, W, 10], fill=RED)
txt(512, 16, "THE WORLD IN ONE PAGE  •  EVERY STORY CHECKED", font(F_B, 17),
    fill=GREY, anchor="ma")
# giant date
txt(512, 38, "TUESDAY 24 NOVEMBER 2026", font(F_SB, 62), fill=INK, anchor="ma")
d.rectangle([24, 112, W - 24, 116], fill=RED)
txt(512, 120, "ONE DAY  •  ONE PAGE  •  ALL THE NEWS THAT MATTERED",
    font(F_B, 15), fill=INK, anchor="ma")

# ============ LEAD MAP — STRAIT OF HORMUZ (dominant illustration) ============
MX, MY, MW, MH = 16, 142, 992, 270
d.rectangle([MX, MY, MX + MW, MY + MH], fill=SEA2, outline=INK, width=3)
# land: Iran (top), Arabia (bottom)
d.polygon([(MX, MY), (MX + MW, MY), (MX + MW, MY + 78), (MX + 640, MY + 96),
           (MX + 560, MY + 62), (MX + 300, MY + 88), (MX, MY + 66)], fill=LAND)
d.polygon([(MX, MY + MH), (MX + MW, MY + MH), (MX + MW, MY + 208),
           (MX + 700, MY + 196), (MX + 620, MY + 232), (MX + 380, MY + 214),
           (MX, MY + 238)], fill=LAND2)
# strait channel
d.polygon([(MX + 560, MY + 62), (MX + 640, MY + 96), (MX + 700, MY + 196),
           (MX + 620, MY + 232), (MX + 580, MY + 150)], fill=SEA)
txt(MX + 380, MY + 14, "IRAN", font(F_B, 26), fill=(120, 90, 40))
txt(MX + 120, MY + 58, "PERSIAN GULF", font(F_B, 17), fill=BLUE)
txt(MX + 800, MY + 196, "OMAN", font(F_B, 26), fill=(120, 90, 40))
txt(MX + 650, MY + 188, "STRAIT OF", font(F_B, 15), fill=INK, anchor="ma")
txt(MX + 650, MY + 206, "HORMUZ", font(F_B, 15), fill=INK, anchor="ma")
# 4 burning tankers in the strait
for (tx, ty) in [(MX + 300, MY + 150), (MX + 420, MY + 118), (MX + 500, MY + 178),
                 (MX + 610, MY + 120)]:
    tanker(tx, ty, 74, 22)
    flame(tx + 8, ty - 30, 22)
    flame(tx + 42, ty - 26, 18)
# mine markers
for (mx_, my_) in [(MX + 380, MY + 210), (MX + 560, MY + 96), (MX + 680, MY + 168)]:
    mine(mx_, my_, 9)
# in-picture label banner
d.rectangle([MX + 24, MY + 8, MX + 330, MY + 52], fill=RED)
txt(MX + 40, MY + 14, "4 TANKERS HIT", font(F_B, 30), fill=(255, 255, 255))
d.rectangle([MX + 700, MY + 8, MX + 968, MY + 40], fill=INK)
txt(MX + 716, MY + 13, "IRGC CLAIM — UNCONFIRMED", font(F_B, 15),
    fill=(255, 255, 255))
# map caption / lead text under banner inside panel bottom-left
d.rectangle([MX, MY + MH - 46, MX + MW, MY + MH], fill=(255, 255, 255))
txt(MX + 12, MY + MH - 42,
    "HORMUZ IN FLAMES — Iran says 4 tankers hit mines and caught fire; IRGC navy also",
    font(F_B, 16), fill=INK)
txt(MX + 12, MY + MH - 22,
    "attacked a container ship north of Khasab. Strait ordered shut, day by day.",
    font(F_R, 15), fill=INK)

# ============ THREE MORE LEADS (row) ============
LY, LH = 422, 140
LW = 322
leads = [
    ("HUAWEI GUILTY", "10 OF 12 COUNTS", RED,
     "US jury in Brooklyn: guilty of stealing trade secrets + bank fraud. Acquitted of racketeering. Appeal planned.",
     "CONFIRMED · 20:41 UTC"),
    ("UKRAINE HITS RUSSIAN SHIPS", "SPARTA II HIT", BLUE,
     "Drones struck cargo ship Sparta II in the Gulf of Finland; corvette hit off Libya — Kyiv claims it SUNK.",
     "CONFIRMED · 08:14 UTC"),
    ("CARTAGENA HOSTAGES", "25 HELD · 5 FREED", DRED,
     "Armed men seized a supermarket in Cartagena, Colombia. 25 held; 5 older women freed. Airport landings paused.",
     "OFFICIAL · 17:35 UTC"),
]
for i, (head, label, col, body, tag) in enumerate(leads):
    x0 = 16 + i * (LW + 8)
    d.rectangle([x0, LY, x0 + LW, LY + LH], outline=INK, width=2, fill=(255, 255, 255))
    d.rectangle([x0, LY, x0 + LW, LY + 34], fill=col)
    txt(x0 + 10, LY + 6, head, font(F_B, 19), fill=(255, 255, 255))
    y = para(x0 + 10, LY + 42, body, font(F_R, 14), LW - 20, 17)
    badge(x0 + 10, LY + LH - 26, label, col)
    txt(x0 + LW - 10, LY + LH - 24, tag, font(F_B, 11), fill=GREY, anchor="ra")

# ============ TIER-2 grid (2 cols x 5) ============
TY = 572
txt(16, TY, "MORE OF THE DAY", font(F_B, 20), fill=INK)
d.rectangle([16, TY + 26, W - 16, TY + 28], fill=INK)
tier2 = [
    ("PIF TOWER HIT, RIYADH", "11 wounded in Houthi drone strike on Saudi fund HQ.", "CONFIRMED"),
    ("HOUTHIS 60 KM FROM ADEN", "Fighters near Yemen's temporary capital; defence line built.", "OFFICIAL"),
    ("SENEGAL AFCON CHAMPIONS", "Reinstated as 2025 Africa Cup winners after court appeal.", "CONFIRMED"),
    ("EL CHAPO ISIDRO CAPTURED", "US drone helped capture cartel boss in Sinaloa; 20 killed.", "OFFICIAL"),
    ("TURKISH HELICOPTER CRASH", "Air Force AS-532 down after take-off; 5 crew killed.", "OFFICIAL"),
    ("VILLAVICENCIO CAR BOMB", "Blast outside government offices; 23 injured.", "REPORTED"),
    ("HAMAS SECURITY CHIEF KILLED", "Israeli strike killed Brig. Gen. Naeem Abu Nahel in Gaza.", "REPORTED"),
    ("HANOI BLAST", "Hot-pot restaurant explosion; 6 killed, 10+ injured.", "REPORTED"),
    ("MEGASPEED BLACKLISTED", "US Entity List: 7 SE Asian firms; Nvidia GPU licences needed.", "OFFICIAL"),
    ("MALAYSIA RETURNS MIGRANTS", "6,803 to Myanmar: 1,500 by ship, 5,303 by air.", "OFFICIAL"),
]
tagcol = {"CONFIRMED": GREEN, "OFFICIAL": BLUE, "REPORTED": ORANGE, "CLAIM": RED}
rowh = 24
for i, (h_, b_, t_) in enumerate(tier2):
    col = i % 2
    row = i // 2
    x0 = 16 + col * 500
    y0 = TY + 36 + row * rowh
    d.ellipse([x0, y0 + 3, x0 + 12, y0 + 15], fill=RED)
    txt(x0 + 18, y0, h_, font(F_B, 14), fill=INK)
    tw = d.textlength(h_, font=font(F_B, 14))
    # truncate body at a word boundary so it never runs under the badge
    b2 = b_
    while b2 and d.textlength(b2, font=font(F_R, 13)) > 378 - tw:
        b2 = b2.rsplit(" ", 1)[0] if " " in b2 else ""
    if b2 != b_:
        b2 = b2 + "…"
    txt(x0 + 18 + tw + 6, y0 + 1, "— " + b2, font(F_R, 13), fill=(40, 40, 40))
    badge(x0 + 420, y0, t_, tagcol[t_], fsize=10)

# ============ BRIEFS — large bold lead-ins ============
BY = TY + 36 + 5 * rowh + 8
txt(16, BY, "IN BRIEF", font(F_B, 20), fill=INK)
d.rectangle([16, BY + 26, W - 16, BY + 28], fill=INK)
briefs = [
    ("GAZA MENINGITIS ALERT:", "272 cases in Oct, 8x normal; 15 dead this year."),
    ("SAUDI STRIKES ON YEMEN:", "25 dead or missing in Lahj; 6 wounded."),
    ("IRAQ TAKES KURD OILFIELDS:", "Federal control ordered; Barzani: \"unacceptable\"."),
    ("DR CONGO PLANE MISSING:", "Cessna 208 lost; rebels claim shootdown, 4 aboard."),
    ("HAFTAR IN TURKEY:", "Libyan commander visits Ankara; to meet Erdogan."),
    ("UK SANCTIONS HOUTHIS:", "Asset freezes + travel bans on group + 4 officials."),
    ("ULLEUNGDO SHELTER ORDER:", "Russian jets enter S. Korea air-defence zone."),
    ("INDONESIA VP RACE:", "Prabowo nominates Amran + Sugiono; vote by 11 Dec."),
    ("HASINA TO RETURN:", "Ex-PM plans 16 Dec return; death sentence in absentia."),
    ("CHINA DEATH SENTENCE:", "Official Ma spying: 35 secrets, over 1m yuan."),
    ("NATO SPACE WARNING:", "Rutte vows defence; 'Sputnik-S' reports dismissed."),
    ("MARKETS:", "Nvidia -7%; Nikkei +3.9%; Seoul +6%; Brent $86.7."),
]
for i, (h_, b_) in enumerate(briefs):
    col = i % 2
    row = i // 2
    x0 = 16 + col * 500
    y0 = BY + 34 + row * 19
    txt(x0, y0, h_, font(F_B, 14), fill=INK)
    tw = d.textlength(h_, font=font(F_B, 14))
    txt(x0 + tw + 5, y0, b_, font(F_R, 13), fill=(40, 40, 40))

# ============ DAY IN NUMBERS strip ============
NY = BY + 34 + 6 * 19 + 8
d.rectangle([0, NY, W, NY + 30], fill=RED)
txt(512, NY + 5,
    "4 TANKERS  •  25 HOSTAGES  •  11 WOUNDED  •  10 OF 12 COUNTS  •  700,000+ WAR DEAD  •  NVIDIA -7%",
    font(F_B, 16), fill=(255, 255, 255), anchor="ma")

# ============ UTC TIMELINE ============
TY2 = NY + 38
txt(16, TY2, "WHEN IT BROKE (UTC)", font(F_B, 15), fill=INK)
txt(16, TY2 + 20,
    "00:00 Hormuz mines  •  02:09 El Chapo Isidro held  •  08:14 Ukraine hits ships  •  11:45 Villavicencio bomb  •  14:27 PIF tower  •  17:35 Cartagena  •  20:41 Huawei verdict",
    font(F_R, 13), fill=(40, 40, 40))

# ============ DATE CHECK ============
DY = TY2 + 40
d.rectangle([16, DY, W - 16, DY + 30], outline=RED, width=2)
txt(28, DY + 7, "DATE CHECK — NOT 24 NOV:",
    font(F_B, 14), fill=RED)
txt(28 + d.textlength("DATE CHECK — NOT 24 NOV:  ", font=font(F_B, 14)), DY + 7,
    "ICJ Myanmar ruling (19 Nov)  •  Shenzhou-24 (25 Nov)  •  Guterres AI call (23 Nov)  •  FARC anniversary (25 Nov)",
    font(F_R, 13), fill=INK)

# ============ FOOTER / HOW SURE legend ============
FY = DY + 36
txt(16, FY, "HOW SURE:  CONFIRMED = 2+ outlets or official record   •   OFFICIAL = on the record   •   REPORTED = one outlet   •   CLAIM = one side's account",
    font(F_B, 12), fill=GREY)

out = os.path.join(BASE, "entry.png")
img.save(out, optimize=True)
print("saved", out, img.size, os.path.getsize(out), "bytes")
