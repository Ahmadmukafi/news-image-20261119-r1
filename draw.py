#!/usr/bin/env python3
"""Draw the front page for news-image-20261119: THE WORLD TODAY.

Layout (1024x1024, cream paper):
  masthead (navy) | Vice City sunset hero + 'VICE CITY OPENS' |
  three story columns (Shenzhen summit / Gulf / Washington) | ticker | footer.
All text is PIL-drawn, fully deterministic (no randomness, no network).
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 28
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

NAVY = (14, 27, 46)
CREAM = (247, 242, 231)
PAPER = (247, 242, 231)
INK = (18, 18, 18)
RED = (178, 34, 34)
DARK = (26, 16, 51)
NEON_PINK = (255, 46, 136)
NEON_CYAN = (0, 229, 255)
GOLD = (255, 226, 154)


def font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(text, f, max_w):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if f.getlength(t) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def gradient(d, box, stops):
    x0, y0, x1, y1 = box
    n = y1 - y0
    for y in range(y0, y1):
        t = (y - y0) / max(1, n - 1)
        # find segment
        seg = min(int(t * (len(stops) - 1)), len(stops) - 2)
        lt = t * (len(stops) - 1) - seg
        c = lerp(stops[seg], stops[seg + 1], lt)
        d.line([(x0, y), (x1, y)], fill=c)


def palm(d, x, y, s, color):
    """Simple palm silhouette: curved trunk + 6 fronds. s = height scale."""
    # trunk: series of short segments curving right
    pts = []
    steps = 8
    for i in range(steps + 1):
        t = i / steps
        pts.append((x + 14 * s * t * t, y - 90 * s * t))
    d.line(pts, fill=color, width=max(3, int(7 * s)))
    tx, ty = pts[-1]
    # fronds: arcs drooping from the crown
    for ang, ln in [(-160, 46), (-120, 52), (-80, 54), (-40, 52), (0, 44), (30, 38)]:
        import math
        r = math.radians(ang)
        ex = tx + ln * s * math.cos(r)
        ey = ty + ln * s * math.sin(r) * 0.55 + 12 * s
        d.line([(tx, ty), (ex, ey)], fill=color, width=max(2, int(4 * s)))
        # droop tip
        d.line([(ex, ey), (ex + 6 * s, ey + 14 * s)], fill=color, width=max(2, int(3 * s)))
    # coconuts
    d.ellipse([tx - 5 * s, ty - 2 * s, tx + 1 * s, ty + 4 * s], fill=color)
    d.ellipse([tx + 1 * s, ty - 2 * s, tx + 7 * s, ty + 4 * s], fill=color)


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.rectangle([0, 0, W, 118], fill=NAVY)
    title = "THE WORLD TODAY"
    tf = SERIF_B(62)
    d.text(((W - tf.getlength(title)) / 2, 14), title, font=tf, fill=CREAM)
    d.line([(MARGIN, 108), (W - MARGIN, 108)], fill=RED, width=2)
    df = SANS_B(21)
    d.text((MARGIN, 80), "THURSDAY 19 NOVEMBER 2026", font=df, fill=CREAM)
    right = "ONE DAY  ·  ONE PAGE"
    d.text((W - MARGIN - df.getlength(right), 80), right, font=df, fill=GOLD)
    d.rectangle([0, 118, W, 122], fill=RED)

    # ---------- hero: Vice City sunset ----------
    hy0, hy1 = 122, 400
    gradient(d, (0, hy0, W, hy1), [(255, 179, 71), (255, 107, 107), (150, 84, 190), (72, 52, 130)])
    # sun with glow, riding low over the skyline (glow radii keep the disc
    # inside the hero box: top of the outer ring stays below y=122)
    cx, cy, r = 512, 235, 72
    for rr, col in [(110, (255, 214, 130)), (88, (255, 226, 154)), (r, (255, 243, 176))]:
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col)
    # birds
    for bx, by, s in [(180, 180, 14), (230, 165, 11), (820, 200, 13), (870, 175, 10)]:
        d.line([(bx - s, by), (bx, by - 7), (bx + s, by)], fill=DARK, width=3)
    # skyline silhouette (central towers kept low so the sun shows)
    base = hy1
    buildings = [
        (0, 120, 150), (60, 90, 210), (140, 130, 250), (250, 100, 190),
        (340, 120, 185), (470, 95, 160), (560, 120, 205), (690, 95, 180),
        (770, 135, 240), (880, 105, 200), (960, 125, 170),
    ]
    # windows first (on the buildings, before silhouette? draw silhouette then windows)
    for bx, bw, bh in buildings:
        d.rectangle([bx, base - bh, bx + bw, base], fill=DARK)
    # lit windows (deterministic grid)
    for bx, bw, bh in buildings:
        for wy in range(base - bh + 12, base - 10, 22):
            for wx in range(bx + 10, bx + bw - 8, 20):
                if (wx * 7 + wy * 13) % 5 < 2:
                    d.rectangle([wx, wy, wx + 6, wy + 8], fill=GOLD)
    # neon VICE CITY billboard on the right tower face
    d.rectangle([756, 248, 992, 310], fill=DARK, outline=NEON_PINK, width=4)
    sf = SANS_B(30)
    st = "VICE CITY"
    d.text(((756 + 992 - sf.getlength(st)) / 2, 264), st, font=sf, fill=NEON_PINK)
    # palms: tall crowns rising above the skyline into the sunset
    palm(d, 40, base, 2.0, DARK)
    palm(d, 990, base, 1.8, DARK)
    palm(d, 300, base, 0.8, DARK)

    # ---------- headline band ----------
    d.rectangle([0, 400, W, 512], fill=NAVY)
    hf = SERIF_B(60)
    head = "VICE CITY OPENS"
    d.text(((W - hf.getlength(head)) / 2, 408), head, font=hf, fill=CREAM)
    sub = "GTA VI launches worldwide after a 13-year wait"
    suf = SANS(24)
    d.text(((W - suf.getlength(sub)) / 2, 476), sub, font=suf, fill=GOLD)

    # ---------- three columns ----------
    cols = [
        ("SUMMIT", "TRUMP, XI AND PUTIN MEET IN SHENZHEN",
         "First-ever trilateral summit on the APEC margins. Trump says he will raise the Iran war with Xi and Putin."),
        ("GULF", "IRAN HITS U.S. BASE IN KUWAIT",
         "Tehran widens its strikes to Gulf states; Bahrain is hit again and tankers are struck in Hormuz. No U.S. troops hurt, CENTCOM says."),
        ("WASHINGTON", "JEFFRIES TO BE FIRST BLACK SPEAKER",
         "Democrats nominate Hakeem Jeffries to lead the House after taking the Senate — a first for an African-American."),
    ]
    col_w = (W - 2 * MARGIN - 2 * 24) / 3
    y0 = 532
    kf = SANS_B(20)
    hdf = SERIF_B(29)
    bf = SANS(18)
    for i, (kick, head, body) in enumerate(cols):
        x = MARGIN + i * (col_w + 24)
        d.rectangle([x, y0, x + col_w, y0 + 4], fill=RED)
        d.text((x, y0 + 12), kick, font=kf, fill=RED)
        y = y0 + 42
        for line in wrap(head, hdf, col_w):
            d.text((x, y), line, font=hdf, fill=INK)
            y += 34
        y += 6
        d.line([(x, y), (x + col_w, y)], fill=(150, 150, 150), width=1)
        y += 10
        for line in wrap(body, bf, col_w):
            d.text((x, y), line, font=bf, fill=(40, 40, 40))
            y += 24

    # ---------- mini row: markets / science / sport ----------
    d.line([(MARGIN, 798), (W - MARGIN, 798)], fill=(150, 150, 150), width=1)
    minis = [
        ("MARKETS", "Oil slips as Gulf risk rises and traders turn cautious"),
        ("SCIENCE", "Earth's missing billion years — scientists may know why"),
        ("SPORT", "Duckett's 133 puts England on top in the third ODI"),
    ]
    mkf = SANS_B(15)
    mhf = SERIF_B(19)
    for i, (kick, head) in enumerate(minis):
        x = MARGIN + i * (col_w + 24)
        d.text((x, 810), kick, font=mkf, fill=RED)
        y = 832
        for line in wrap(head, mhf, col_w):
            d.text((x, y), line, font=mhf, fill=INK)
            y += 23

    # ---------- ticker ----------
    ty0, ty1 = 920, 992
    d.rectangle([0, ty0, W, ty1], fill=NAVY)
    tick = ("ALSO TODAY:  Cyclone Akvan nears India's east coast  •  "
            "Voyager 1 reaches a light-day from Earth  •  "
            "Nvidia halts H-series chip shipments to China  •  "
            "EU proposes a €45bn Ukraine loan")
    tkf = SANS_B(19)
    tkf2 = SANS(19)
    # bold lead + regular rest
    lead = "ALSO TODAY:  "
    d.text((MARGIN, ty0 + 12), lead, font=tkf, fill=GOLD)
    rest = tick[len(lead):]
    lines = wrap(rest, tkf2, W - 2 * MARGIN - tkf.getlength(lead))
    d.text((MARGIN + tkf.getlength(lead), ty0 + 12), lines[0], font=tkf2, fill=CREAM)
    if len(lines) > 1:
        d.text((MARGIN, ty0 + 38), lines[1], font=tkf2, fill=CREAM)

    # ---------- footer ----------
    ff = SANS(13)
    foot = "Sources: AP · Reuters · BBC · NDTV — drawn with PIL, no photograph"
    d.text(((W - ff.getlength(foot)) / 2, 1002), foot, font=ff, fill=(110, 110, 110))

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    draw()
