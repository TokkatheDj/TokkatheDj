# Draws writing/img/printed-rows.svg: printed breadboard rows vs the Pico's pin numbers.
# Pico right-hand pins 21..40 sit beside printed rows 20..1 (pin n -> row 41-n), USB at the top.
OUT = r"D:\Documents\Claude Local\portfolio-profile\writing\img\printed-rows.svg"
ROWS = 25
TOP, RH = 104, 24          # first row's y, row height
W = 720
H = TOP + ROWS * RH + 70

ink, muted, line, board, pico = "#1f2a30", "#5d6b73", "#c9d2d6", "#f4f1ea", "#2f6b4f"
bad, good = "#c0392b", "#1e8449"

def y(r):  # centre of printed row r
    return TOP + (r - 1) * RH + RH / 2

o = []
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'font-family="Segoe UI, Helvetica, Arial, sans-serif" role="img" '
         f'aria-label="Breadboard printed rows next to Pico pin numbers: pin 23 sits at row 18, pin 25 at row 16; rows 21 and up connect to nothing.">')
o.append(f'<rect width="{W}" height="{H}" rx="14" fill="#ffffff"/>')
o.append(f'<text x="24" y="34" font-size="20" font-weight="700" fill="{ink}">"Holes 23 and 25" — which 23?</text>')
o.append(f'<text x="24" y="56" font-size="14" fill="{muted}">The guide counted the Pico\'s pins (white). I counted the rows printed on the board (grey).</text>')

# breadboard strip
bx, bw = 150, 300
o.append(f'<rect x="{bx}" y="{TOP-6}" width="{bw}" height="{ROWS*RH+12}" rx="8" fill="{board}" stroke="{line}"/>')
for r in range(1, ROWS + 1):
    o.append(f'<text x="{bx-12}" y="{y(r)+5}" font-size="13" text-anchor="end" fill="{muted}">{r}</text>')
    for k in range(5):
        o.append(f'<rect x="{bx+150+k*24}" y="{y(r)-4}" width="8" height="8" rx="1.5" fill="#d8d2c4"/>')
o.append(f'<text x="{bx-12}" y="{TOP-16}" font-size="12" text-anchor="end" fill="{muted}">printed row</text>')

# Pico body over rows 1..20
px, pw = bx + 20, 110
o.append(f'<rect x="{px}" y="{TOP}" width="{pw}" height="{20*RH}" rx="6" fill="{pico}"/>')
o.append(f'<rect x="{px+pw/2-18}" y="{TOP-14}" width="36" height="18" rx="3" fill="#9aa5ab"/>')
o.append(f'<text x="{px+pw/2-24}" y="{TOP-12}" font-size="11" text-anchor="end" fill="{muted}">USB</text>')
o.append(f'<text x="{px+pw/2}" y="{y(10)+5}" font-size="16" font-weight="700" text-anchor="middle" fill="#ffffff">Pico</text>')
for r in range(1, 21):
    pin = 41 - r
    o.append(f'<text x="{px+pw-8}" y="{y(r)+4}" font-size="11" text-anchor="end" fill="#d9efe3">{pin}</text>')

# rows past the Pico
o.append(f'<rect x="{bx+4}" y="{TOP+20*RH+2}" width="{bw-8}" height="{5*RH-4}" rx="6" fill="none" '
         f'stroke="{muted}" stroke-dasharray="5 4"/>')
o.append(f'<text x="{bx+75}" y="{y(23)+5}" font-size="12" text-anchor="middle" fill="{muted}">rows 21+: nothing here</text>')

def mark(r, ok, label):
    c = good if ok else bad
    cx = bx + 150 + 2 * 24 + 4  # centre of the middle hole
    if ok:
        o.append(f'<circle cx="{cx}" cy="{y(r)}" r="9" fill="none" stroke="{c}" stroke-width="3"/>')
    else:
        o.append(f'<path d="M{cx-8} {y(r)-8} l16 16 M{cx+8} {y(r)-8} l-16 16" stroke="{c}" stroke-width="3" stroke-linecap="round"/>')
    o.append(f'<line x1="{bx+bw+6}" y1="{y(r)}" x2="{bx+bw+26}" y2="{y(r)}" stroke="{c}" stroke-width="2"/>')
    o.append(f'<text x="{bx+bw+32}" y="{y(r)+5}" font-size="14" font-weight="600" fill="{c}">{label}</text>')

mark(16, True, "row 16 = pin 25 (the input)")
mark(18, True, "row 18 = pin 23 (ground)")
mark(23, False, "row 23: where I put a wire")
mark(25, False, "row 25: where I put the other")

o.append(f'<text x="24" y="{H-22}" font-size="14" fill="{ink}">Both numbers were correct. Only one of them was printed on the thing in my hand.</text>')
o.append('</svg>')

import os
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write("\n".join(o) + "\n")
print("ok", OUT)
