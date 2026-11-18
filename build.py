#!/usr/bin/env python3
"""Compose a 1024x1024 broadsheet front page dated 18 November 2026.

Everything is drawn with Pillow primitives so the result is deterministic.
The layout is split into a masthead, a lead column, a schematic world map,
a grid of six regional sections and a footer.
"""

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- palette
PAPER = (246, 240, 226)   # warm cream newsprint
INK = (26, 24, 22)        # near-black body ink
RED = (176, 30, 38)       # masthead accent
MUTED = (102, 94, 82)     # secondary text
RULE = (72, 66, 58)       # hairlines
PANEL = (251, 247, 237)   # lighter panel stock
WHITE = (255, 253, 248)

W = H = 1024

# ----------------------------------------------------------------- fonts
URW = "/usr/share/fonts/opentype/urw-base35/"
TTF = "/usr/share/fonts/truetype/dejavu/"
F_DISPLAY = URW + "C059-Bold.otf"
F_SERIF = URW + "NimbusRoman-Regular.otf"
F_SERIF_B = URW + "NimbusRoman-Bold.otf"
F_SERIF_I = URW + "NimbusRoman-Italic.otf"
F_SANS = TTF + "DejaVuSans.ttf"
F_SANS_B = TTF + "DejaVuSans-Bold.ttf"

_font_cache = {}


def font(path, size):
    """Return a cached TrueType/OpenType face at the requested pixel size."""
    key = (path, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(path, size)
    return _font_cache[key]


# ---------------------------------------------------------- text helpers
def wrap(text, draw, fnt, max_width):
    """Greedy word-wrap, splitting over-long words so nothing spills out."""
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
            continue
        if current:
            lines.append(current)
        if draw.textlength(word, font=fnt) <= max_width:
            current = word
            continue
        current = ""
        for ch in word:
            if draw.textlength(current + ch, font=fnt) <= max_width:
                current += ch
            else:
                lines.append(current)
                current = ch
    if current:
        lines.append(current)
    return lines


def put_lines(draw, lines, x, y, fnt, fill, leading, floor=None):
    """Draw pre-wrapped lines top-down; never place ink above y=0 or floor."""
    for line in lines:
        if y < 0:
            raise ValueError("refusing to draw text above y=0")
        if floor is not None and y + leading > floor:
            raise ValueError("text would extend past its container")
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def right_text(draw, text, right_x, y, fnt, fill):
    draw.text((right_x - draw.textlength(text, font=fnt), y), text,
              font=fnt, fill=fill)


# -------------------------------------------------------------- editorial
LEAD_HEAD = "US STRIKE HITS QESHM ISLAND; GULF STATES INTERCEPT DRONES"
LEAD_DECK = (
    "American warplanes hit Iranian positions on Qeshm Island in the Strait "
    "of Hormuz overnight, while Saudi and Emirati defences reported shooting "
    "down a wave of retaliatory drones. Tehran pledged a response; shipping "
    "insurers promptly re-priced every tanker crossing the gulf."
)
SECONDARY = [
    "Xi and Putin meet as Trump joins a trilateral summit in Shenzhen",
    "Ukraine strikes the Kerch Bridge; Crimea rail link halted again",
]

SECTIONS = [
    ("MIDDLE EAST", (223, 190, 138), [
        "Qeshm Island struck; Hormuz insurance spikes",
        "Gulf states intercept 14 drones, no casualties",
        "Tehran vows a 'proportional response' this week",
        "Riyadh calls for an emergency GCC security summit",
        "Brent crude climbs 6% on supply-route fears",
        "UN envoy urges an immediate de-escalation corridor",
    ]),
    ("ASIA", (178, 200, 224), [
        "Xi hosts Putin ahead of the Shenzhen trilateral",
        "Three-way summit set for Friday, trade atop agenda",
        "Beijing unveils fresh semiconductor export curbs",
        "Tokyo and Seoul share missile-warning data",
        "Monsoon floods displace 40,000 in Bangladesh",
        "India launches lunar orbiter Chandrayaan-4",
    ]),
    ("EUROPE", (203, 185, 218), [
        "Ukraine hits the Kerch Bridge, rail traffic stops",
        "Kyiv says the strike used domestically built missiles",
        "EU ministers weigh a new sanctions package on Moscow",
        "Berlin and Paris push joint arms procurement",
        "UK inflation cools to 2.1%, a cut looks likely",
        "Rome passes first reading of migration reform",
    ]),
    ("AMERICAS", (176, 212, 182), [
        "Trump prepares to join the Shenzhen trilateral",
        "Congress passes stopgap funding, shutdown averted",
        "Fed holds rates, signals one cut before year-end",
        "Brazil opens an Amazon protection summit",
        "Canada posts a record grain harvest",
        "Chile begins voting in nationwide local polls",
    ]),
    ("AFRICA", (232, 205, 150), [
        "Sahel states form a joint counter-insurgency force",
        "Nigeria launches a national digital ID scheme",
        "Ethiopia and Eritrea sign a port-access deal",
        "South Africa reports a novel flu strain",
        "Kenya opens a large solar farm at Nakuru",
        "AU summit adopts a free-trade timetable",
    ]),
    ("WORLD & SCIENCE", (188, 213, 216), [
        "Webb detects water vapour on exoplanet K2-18b",
        "Antarctic ice loss hits a seasonal record",
        "Fusion test sustains net energy gain for 30 seconds",
        "WHO warns of rising antimicrobial resistance",
        "Private lander reaches the lunar south pole",
        "Study links ocean warming to coral decline",
    ]),
]

# -------------------------------------------------------- schematic map
CONTINENTS = [
    [(0.04, 0.07), (0.16, 0.05), (0.23, 0.09), (0.20, 0.19),
     (0.15, 0.23), (0.13, 0.32), (0.08, 0.28), (0.05, 0.17)],
    [(0.13, 0.32), (0.18, 0.34), (0.20, 0.41), (0.17, 0.43)],
    [(0.19, 0.42), (0.27, 0.44), (0.29, 0.57), (0.25, 0.73),
     (0.21, 0.85), (0.18, 0.78), (0.17, 0.60), (0.16, 0.48)],
    [(0.28, 0.03), (0.37, 0.02), (0.39, 0.10), (0.31, 0.12)],
    [(0.46, 0.14), (0.55, 0.12), (0.58, 0.18), (0.53, 0.25),
     (0.47, 0.25), (0.44, 0.19)],
    [(0.45, 0.28), (0.56, 0.27), (0.59, 0.41), (0.55, 0.58),
     (0.50, 0.69), (0.46, 0.60), (0.43, 0.44), (0.42, 0.34)],
    [(0.57, 0.10), (0.76, 0.05), (0.91, 0.12), (0.92, 0.24),
     (0.86, 0.31), (0.80, 0.24), (0.73, 0.28), (0.66, 0.25),
     (0.60, 0.21)],
    [(0.70, 0.30), (0.75, 0.30), (0.74, 0.41), (0.71, 0.38)],
    [(0.81, 0.34), (0.87, 0.36), (0.85, 0.44), (0.80, 0.42)],
    [(0.83, 0.55), (0.92, 0.54), (0.94, 0.66), (0.86, 0.68),
     (0.81, 0.62)],
]

PINS = [
    (0.630, 0.285),  # 1 Qeshm Island
    (0.675, 0.330),  # 2 Strait of Hormuz
    (0.575, 0.385),  # 3 Riyadh
    (0.530, 0.185),  # 4 Kyiv
    (0.578, 0.165),  # 5 Kerch Bridge
    (0.855, 0.320),  # 6 Shenzhen
    (0.495, 0.435),  # 7 Sahel
    (0.598, 0.240),  # 8 Gaza
]
LEGEND = [
    "1 Qeshm Is.   2 Hormuz   3 Riyadh   4 Kyiv",
    "5 Kerch Br.   6 Shenzhen   7 Sahel   8 Gaza",
]


def draw_map(draw, box, title_font, legend_font, num_font):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=PANEL, outline=RULE, width=2)
    draw.rectangle([x0 + 4, y0 + 4, x1 - 4, y1 - 4], outline=RULE, width=1)
    draw.text((x0 + 12, y0 + 10), "THE DAY'S THEATRES",
              font=title_font, fill=INK)

    mx0, my0, mx1, my1 = x0 + 14, y0 + 30, x1 - 12, y1 - 58
    mw, mh = mx1 - mx0, my1 - my0
    for poly in CONTINENTS:
        pts = [(mx0 + px * mw, my0 + py * mh) for px, py in poly]
        draw.polygon(pts, fill=(214, 206, 188), outline=(120, 112, 98))

    for i, (px, py) in enumerate(PINS, start=1):
        cx, cy = mx0 + px * mw, my0 + py * mh
        r = 9
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED,
                     outline=WHITE, width=1)
        label = str(i)
        lw = draw.textlength(label, font=num_font)
        draw.text((cx - lw / 2, cy - 7), label, font=num_font, fill=WHITE)

    ly = y1 - 50
    for line in LEGEND:
        draw.text((x0 + 12, ly), line, font=legend_font, fill=MUTED)
        ly += 17


# ---------------------------------------------------------- section box
def draw_section(draw, box, colour, title, stories, title_font):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=colour, outline=RULE, width=2)
    draw.text((x0 + 10, y0 + 7), title, font=title_font, fill=INK)
    rule_y = y0 + 27
    draw.line([(x0 + 8, rule_y), (x1 - 8, rule_y)], fill=RULE, width=1)

    inner_w = (x1 - x0) - 20
    floor = y1 - 7
    start = rule_y + 6

    # Shrink the body face until every numbered story fits the box.
    for size in (11, 10, 9, 8):
        body = font(F_SANS, size)
        leading = size + 3
        blocks = []
        for n, story in enumerate(stories, start=1):
            blocks.append(wrap("%d  %s" % (n, story), draw, body, inner_w))
        needed = sum(len(b) for b in blocks) * leading + 3 * (len(blocks) - 1)
        if start + needed <= floor:
            break
    else:
        raise ValueError("section %s cannot fit its stories" % title)

    y = start
    for block in blocks:
        y = put_lines(draw, block, x0 + 10, y, body, INK, leading, floor=floor)
        y += 3


# ------------------------------------------------------------------ page
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # top bar and masthead furniture
    d.rectangle([0, 0, W, 16], fill=RED)
    d.text((28, 25), "AN INDEPENDENT SURVEY OF THE DAY'S EVENTS",
           font=font(F_SANS_B, 11), fill=MUTED)
    right_text(d, "35 STORIES / SIX CONTINENTS", W - 28, 25,
               font(F_SANS_B, 11), MUTED)
    d.text((22, 42), "THE WORLD", font=font(F_DISPLAY, 68), fill=INK)
    d.line([(28, 112), (996, 112)], fill=RULE, width=1)

    # red dateline band
    d.rectangle([0, 117, W, 151], fill=RED)
    date_font = font(F_SANS_B, 22)
    date_str = "WEDNESDAY · 18 NOVEMBER 2026"
    date_w = d.textlength(date_str, font=date_font)
    d.text(((W - date_w) / 2, 122), date_str, font=date_font, fill=WHITE)

    # double rule under the dateline
    d.line([(28, 157), (996, 157)], fill=INK, width=2)
    d.line([(28, 161), (996, 161)], fill=INK, width=1)

    # ---- lead column
    y = 172
    head_font = font(F_SERIF_B, 35)
    y = put_lines(d, wrap(LEAD_HEAD, d, head_font, 528), 28, y,
                  head_font, INK, 40, floor=300) + 9

    deck_font = font(F_SERIF_I, 15)
    y = put_lines(d, wrap(LEAD_DECK, d, deck_font, 528), 28, y,
                  deck_font, MUTED, 19, floor=392) + 12

    d.line([(28, y), (558, y)], fill=RULE, width=1)
    y += 9
    sec_font = font(F_SERIF_B, 18)
    for item in SECONDARY:
        y = put_lines(d, wrap(item, d, sec_font, 528), 28, y,
                      sec_font, INK, 22, floor=520) + 9

    # ---- schematic map, upper right
    draw_map(d, (574, 172, 996, 520), font(F_SANS_B, 11),
             font(F_SANS, 10), font(F_SANS_B, 10))

    # ---- six regional boxes, two rows of three
    col_x = [28, 354, 680]
    rows = [(532, 724), (736, 928)]
    grid_font = font(F_SANS_B, 13)
    for idx, (title, colour, stories) in enumerate(SECTIONS):
        cx = col_x[idx % 3]
        ry0, ry1 = rows[idx // 3]
        draw_section(d, (cx, ry0, cx + 314, ry1), colour, title,
                     stories, grid_font)

    # ---- footer
    d.line([(28, 944), (996, 944)], fill=RULE, width=1)
    d.text((28, 953), "Compiled from reports of 18 November 2026",
           font=font(F_SANS, 12), fill=MUTED)
    right_text(d, "the-commons.web.id", 996, 953,
               font(F_SANS_B, 12), RULE)

    img.save("entry.png", format="PNG", optimize=True)
    return img


if __name__ == "__main__":
    build()
