"""Render a dense newspaper front page for 18 November 2026."""
from PIL import Image, ImageDraw, ImageFont
import os

W = H = 1024
PAPER = (247, 244, 237)
INK = (17, 20, 26)
MUTED = (75, 80, 88)
RED = (166, 32, 32)
BLUE = (22, 60, 110)
GREEN = (20, 92, 66)
GOLD = (150, 100, 15)
RULE = (198, 192, 180)

F = "/usr/share/fonts/truetype/dejavu/"
def fnt(n, bold=False, serif=False):
    name = ("DejaVuSerif-Bold.ttf" if serif else "DejaVuSans-Bold.ttf") if bold else ("DejaVuSerif.ttf" if serif else "DejaVuSans.ttf")
    return ImageFont.truetype(F + name, n)

im = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(im)

def text(xy, s, font, fill=INK, anchor=None):
    d.text(xy, s, font=font, fill=fill, anchor=anchor)

def rtext(x, y, s, font, fill=INK):
    text((x, y), s, font, fill, anchor="ra")

def wrap(s, font, maxw):
    out, cur = [], ""
    for w in s.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur: out.append(cur)
            cur = w
    if cur: out.append(cur)
    return out

def para(x, y, s, font, maxw, fill=INK, lh=None, maxlines=None):
    lh = lh or (font.size + 4)
    lines = wrap(s, font, maxw)
    if maxlines: lines = lines[:maxlines]
    for ln in lines:
        text((x, y), ln, font, fill)
        y += lh
    return y

def rpara(x, y, s, font, maxw, fill=INK, lh=None, maxlines=None):
    lh = lh or (font.size + 4)
    lines = wrap(s, font, maxw)
    if maxlines: lines = lines[:maxlines]
    for ln in lines:
        rtext(x, y, ln, font, fill)
        y += lh
    return y

# masthead
d.rectangle((0, 0, W, 7), fill=RED)
text((40, 22), "THE WORLD", fnt(56, bold=True, serif=True), anchor="lt")
text((370, 34), "A ONE-DAY GLOBAL BRIEF", fnt(15, bold=True), MUTED, anchor="lt")
text((40, 86), "WEDNESDAY  ·  18 NOVEMBER 2026", fnt(22, bold=True), RED, anchor="lt")
text((W - 40, 26), "35 STORIES", fnt(18, bold=True), BLUE, anchor="ra")
text((W - 40, 52), "SIX CONTINENTS", fnt(18, bold=True), BLUE, anchor="ra")
d.line((40, 116, W - 40, 116), fill=INK, width=3)
d.line((40, 120, W - 40, 120), fill=INK, width=1)

# lead block, left 620px
LX, LW = 40, 620
lead = "US STRIKES IRAN ISLAND AS GULF STATES INTERCEPT DRONES"
y = para(LX, 134, lead, fnt(27, bold=True, serif=True), LW, INK, 31, 2)
y = para(LX, y + 5,
    "US warplanes hit an IRGC missile site on Qeshm Island in the Strait of Hormuz. "
    "Iran said it targeted a US base in Kuwait. Bahrain and Kuwait reported intercepting drones.",
    fnt(14), LW, MUTED, 18, 3)
d.line((LX, y + 7, LX + LW, y + 7), fill=RULE, width=1)
y += 16
for hd, sub in [
    ("XI AND PUTIN MEET BEFORE TRILATERAL SUMMIT WITH TRUMP",
     "Leaders gather in Shenzhen; Ukraine and nuclear arms on the agenda."),
    ("UKRAINE STRIKES KERCH BRIDGE IN BIGGEST DRONE ATTACK",
     "Road link severed; Russia says it downed 2,000 drones in 24 hours."),
]:
    y = para(LX, y, hd, fnt(18, bold=True), LW, INK, 22, 2)
    y = para(LX, y + 3, sub, fnt(13), LW, MUTED, 17, 2) + 9
    d.line((LX, y, LX + LW, y), fill=RULE, width=1)
    y += 9

# map panel (bottom must stay above sections at y=352)
MX, MY, MW, MH = 680, 134, 304, 202
d.rectangle((MX, MY, MX + MW, MY + MH), outline=INK, width=2)
text((MX + 12, MY + 8), "THE DAY ON THE MAP", fnt(13, bold=True), BLUE)
d.line((MX + 12, MY + 27, MX + MW - 12, MY + 27), fill=RULE, width=1)
def lonlat(lon, lat):
    return (MX + 16 + (lon + 180) / 360 * (MW - 32),
            MY + 34 + (90 - lat) / 180 * (MH - 70))
cont = {
 "NA": [(-168,65),(-140,70),(-100,72),(-60,60),(-55,45),(-80,25),(-97,16),(-118,32),(-125,50)],
 "SA": [(-81,12),(-60,10),(-35,-5),(-40,-25),(-55,-55),(-72,-50),(-78,-10)],
 "EU": [(-10,36),(0,55),(30,70),(60,65),(45,38),(20,35)],
 "AF": [(-17,35),(10,37),(35,30),(50,10),(40,-30),(15,-35),(-10,-5)],
 "AS": [(35,30),(60,70),(140,70),(150,40),(120,5),(95,8),(75,20),(55,25)],
 "OC": [(112,-12),(155,-12),(150,-40),(120,-38)],
}
for pts in cont.values():
    pp = [lonlat(a, b) for a, b in pts]
    d.polygon(pp, fill=(216, 226, 216), outline=(96, 116, 96))
pins = [(-50, 27, "1"), (-75, 40, "2"), (114, 25, "3"), (37, 52, "4"),
        (24, -12, "5"), (-100, 60, "6"), (136, -25, "7"), (-60, -10, "8")]
for lon, lat, n in pins:
    x, yy = lonlat(lon, lat)
    d.ellipse((x-8, yy-8, x+8, yy+8), fill=RED, outline=PAPER, width=1)
    text((x, yy), n, fnt(10, bold=True), (255,255,255), anchor="mm")
text((MX + 12, MY + MH - 26), "1 Gulf   2 Washington   3 China   4 Europe", fnt(9), MUTED)
text((MX + 12, MY + MH - 14), "5 Africa   6 N. America   7 Oceania   8 S. America", fnt(9), MUTED)

# section grid
SECTIONS = [
 ("MIDDLE EAST", RED, [
  "Iran says it struck US base at Kuwait's Ali al-Salem airbase",
  "Bahrain says air defences intercepted Iranian attacks",
  "USS Theodore Roosevelt arrives: third US carrier in region",
  "Trump warns Iran will 'pay a price' over dirty-bomb report",
  "Iran foreign minister denies nuclear-plot report as baseless",
  "UK and Australia sanction Israeli settlement expansion",
 ]),
 ("ASIA", BLUE, [
  "Xi tells APEC summit to back AI cooperation and free trade",
  "Putin says trilateral summit should be 'highly useful'",
  "Trump in Manila for ASEAN summit, expands defence ties",
  "US chips to four Southeast Asian nations need export licence",
  "Trump says he may hold one-on-one talks with Kim Jong Un",
  "Quad leaders Australia, Japan, India meet this term",
 ]),
 ("EUROPE", GREEN, [
  "Ukraine says Kerch Bridge road link severed by drone strike",
  "Russia reports 2,000 drones and four missiles downed in 24h",
  "Italy approves law against antisemitism",
  "Israel's parliament elects new Knesset speaker",
  "Netanyahu faces claims of interference in October election",
  "Kyiv and Europe fear being sidelined at Shenzhen talks",
 ]),
 ("AMERICAS", GOLD, [
  "Democrat Mary Peltola wins Alaska Senate, ousts Sullivan",
  "Navy secretary nominee says Iran war strains military",
  "Trump says he will raise Ukraine at trilateral summit",
  "Pakistani man gets 27 years for plotting to kill Trump",
  "Apple services hit disruption: iCloud, Pay, App Store",
  "Latin America could grow 5.1% more by riding AI, IDB says",
 ]),
 ("AFRICA", (90,60,120), [
  "UN: 2,230 civilians killed in Sudan since January, mostly drones",
  "Nigeria says US intelligence helps target militants",
  "13 African states elected to ITU Council at Doha conference",
  "Nigeria disputes report that South Africa rebuked its envoy",
  "UN appeals for emergency aid for Nigerian refugees in Niger",
  "Kordofan records two thirds of verified Sudan deaths",
 ]),
 ("WORLD & SCIENCE", (30,100,120), [
  "Voyager 1 signal now takes 24 hours to reach Earth",
  "Gaza ceasefire strains as aid deliveries fall short",
  "Saudi-led coalition intercepts Houthi missile near Riyadh",
  "Small island states press for action at UN climate talks",
  "School phone bans may help recover learning loss, study says",
  "UN official warns methamphetamine spreads in Middle East",
 ]),
]
GX, GY, GW, GH = 40, 422, 302, 272
for i, (title, col, stories) in enumerate(SECTIONS):
    cx = GX + (i % 3) * (GW + 11)
    cy = GY + (i // 3) * (GH + 14)
    d.rectangle((cx, cy, cx + GW, cy + 27), fill=col)
    text((cx + 8, cy + 4), title, fnt(14, bold=True), (255, 255, 255))
    yy = cy + 33
    for j, s in enumerate(stories):
        text((cx + 6, yy), s[0], fnt(12, bold=True), col)
        yy2 = para(cx + 19, yy, s[1:], fnt(11), GW - 25, INK, 14, 2)
        yy = yy2 + 4
    d.rectangle((cx, cy, cx + GW, cy + GH), outline=RULE, width=1)

d.line((40, H - 22, W - 40, H - 22), fill=INK, width=1)
text((40, H - 18), "Compiled from reports of 18 November 2026", fnt(10), MUTED)
rtext(W - 40, H - 18, "the-commons.web.id", fnt(10, bold=True), RED)

out = "entry.png"
im.save(out, optimize=True)
print("bytes", os.path.getsize(out))
